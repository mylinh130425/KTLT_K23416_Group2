from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def query_dishes_interactive():
    try:
        # Kết nối MongoDB
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        client.admin.command("ping") # kiểm tra kết nối có thành công không
        db = client["MealMatch"]
        collection = db["Menu"]

        # Nhập dữ liệu từ người dùng
        print("\n=== Bộ lọc món ăn (MEALMATCH) ===")
        category = input("Nhập danh mục (VD: food, drink, để trống nếu không lọc): ").strip() or None
        min_price = float(input("Nhập giá tối thiểu (VND, mặc định 0): ").strip() or 0)
        max_price = float(input("Nhập giá tối đa (VND, mặc định 1,000,000): ").strip() or 1_000_000)
        min_rating = float(input("Nhập đánh giá tối thiểu (1-5 sao, mặc định 0): ").strip() or 0)
        sort_order = int(input("Sắp xếp giá (1: thấp đến cao, -1: cao đến thấp, mặc định 1): ").strip() or 1)

        #1. Xây dựng pipeline - MongoDB aggregation pipeline giúp lọc và xử lý dữ liệu hiệu quả.
        pipeline = [
            {
                "$facet": {
                    "nested_items": [ # Xử lý dữ liệu dạng lồng nhau (nested) - object
                        {"$set": {
                            "menu": {
                                "$cond": {
                                    "if": {"$isArray": "$menu"},
                                    "then": "$menu",
                                    "else": {
                                        "$reduce": {
                                            "input": {"$objectToArray": "$menu"},
                                            "initialValue": [],
                                            "in": {"$concatArrays": ["$$value", "$$this.v"]}
                                        }
                                    }
                                }
                            }
                        }},
                        {"$unwind": "$menu"},
                        {"$unwind": "$menu.pricing"},
                        {"$match": { #Chỉ lấy món ăn có giá nằm trong khoảng min-max
                            "menu.pricing.price": {"$gte": min_price, "$lte": max_price},
                            "$or": [
                                {"menu.pricing.required": True},
                                {"menu.pricing.required": {"$exists": False}}
                            ]
                        }},
                        {"$project": {
                            "place_id": "$place_id",
                            "restaurant_name": "$name",
                            "dish_name": "$menu.name",
                            "price": "$menu.pricing.price",
                            "category": {"$ifNull": ["$menu.category", "N/A"]},
                            "food_review": "$menu.food_review",
                            "description": {"$ifNull": ["$menu.pricing.note", "Không có mô tả!"]}
                        }}
                    ],
                    "flat_items": [ ## Xử lý dữ liệu dạng phẳng (flat) - array
                        {"$match": {
                            "pricing.price": {"$gte": min_price, "$lte": max_price}
                        }},
                        {"$unwind": "$pricing"},
                        {"$match": {
                            "$or": [
                                {"pricing.required": True},
                                {"pricing.required": {"$exists": False}}
                            ]
                        }},
                        {"$project": {
                            "place_id": "$product_id",
                            "restaurant_name": "$name",
                            "dish_name": "$name",
                            "price": "$pricing.price",
                            "category": {"$ifNull": ["$category", "N/A"]},
                            "food_review": "$food_review",
                            "description": {"$ifNull": ["$pricing.note", "Không có mô tả!"]}
                        }}
                    ]
                }
            },
            #2. Gộp dữ liệu từ 2 nhánh ($concatArrays) - Giải nén ($unwind) để xử lý từng món ăn.
            {"$project": {
                "items": {"$concatArrays": ["$nested_items", "$flat_items"]}
            }},
            {"$unwind": "$items"}
        ]

        #3. Lọc category sau khi gộp dữ liệu (Fix lỗi lọc category bị sai)
        if category:
            pipeline.append({"$match": {"items.category": {"$regex": f"^{category}$", "$options": "i"}}})
            #$regex --> tìm category chính xác (drink-drinks)
            #$options: i --> ko phân biệt hoa thường

        #4. Tính trung bình rating
        pipeline.append({
            "$addFields": {
                "items.average_rating": {
                    "$cond": {
                        "if": {"$gt": [{"$size": {"$ifNull": ["$items.food_review", []]}}, 0]},
                        "then": {
                            "$avg": [
                                {"$ifNull": [{"$arrayElemAt": ["$items.food_review.rating.taste", 0]}, 0]},
                                {"$ifNull": [{"$arrayElemAt": ["$items.food_review.rating.portion", 0]}, 0]},
                                {"$ifNull": [{"$arrayElemAt": ["$items.food_review.rating.hygiene", 0]}, 0]}
                            ]
                        },
                        "else": 0
                    }
                }
            }
        })

        # Lọc theo rating
        if min_rating > 0:
            pipeline.append({"$match": {"items.average_rating": {"$gte": min_rating}}})

        # Định dạng đầu ra
        pipeline.append({
            "$project": {
                "_id": 0,
                "place_id": "$items.place_id",
                "restaurant_name": "$items.restaurant_name",
                "dish_name": "$items.dish_name",
                "price": "$items.price",
                "category": "$items.category",
                "average_rating": "$items.average_rating",
                "description": "$items.description"
            }
        })

        # Sắp xếp theo giá
        pipeline.append({"$sort": {"price": sort_order}})

        # Thực thi truy vấn
        results = list(collection.aggregate(pipeline))

        # Kiểm tra nếu Gogi có trong kết quả
        logger.info(f"Checking for Gogi in results: {[doc for doc in results if 'gogi' in str(doc).lower()]}")
        logger.info(f"Found {len(results)} dishes")

        # Hiển thị kết quả
        if not results:
            print("Không tìm thấy món nào!")
        else:
            print("\nNAME RES\tFOOD\t\tRATE\tPRICE\tDESCRIPTION")
            print("-" * 60)
            for dish in results:
                stars = int(dish["average_rating"])
                rate_display = "*" * stars + f" ({stars})" if stars > 0 else "N/A"
                print(f"{dish['restaurant_name'][:10]:<10}\t{dish['dish_name'][:15]:<15}\t{rate_display:<8}\t{dish['price']:<8}\t{dish['description']}")

        return results

    except ServerSelectionTimeoutError as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
    except OperationFailure as e:
        logger.error(f"Query failed: {e}")
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
    finally:
        if client:
            client.close()

# Test Hàm
if __name__ == "__main__":
    filtered_dishes = query_dishes_interactive()
