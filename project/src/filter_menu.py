from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def query_dishes(category=None, min_price=0, max_price=1_000_000, min_rating=0, sort_order=1, skip=0, limit=10):
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        db = client["MealMatch"]
        collection = db["Menu"]

        pipeline = [
            {
                "$facet": {
                    "nested_items": [
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
                        {"$match": {
                            "menu.pricing.price": {"$gte": min_price, "$lte": max_price},
                            "$or": [
                                {"menu.pricing.required": True},
                                {"menu.pricing.required": {"$exists": False}}
                            ]
                        }},
                        {"$project": {
                            "place_id": "$place_id",
                            "restaurant_name": "$restaurant_name",
                            "dish_name": "$menu.name",
                            "price": "$menu.pricing.price",
                            "category": {"$ifNull": ["$menu.category", "N/A"]},
                            "food_review": "$menu.item_review",  # Sửa: lấy $menu.item_review
                            "description": {"$ifNull": ["$menu.pricing.note", "Không có mô tả!"]},
                            "feature_img": "$menu.feature_img",
                            "rating": "$menu.rating"
                        }}
                    ],
                    "flat_items": [
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
                            "restaurant_name": "$restaurant_name",
                            "dish_name": "$name",
                            "price": "$pricing.price",
                            "category": {"$ifNull": ["$category", "N/A"]},
                            "food_review": "$item_review",  # Đúng: lấy $item_review
                            "description": {"$ifNull": ["$pricing.note", "Không có mô tả!"]},
                            "feature_img": "$feature_img",
                            "rating": "$rating"
                        }}
                    ]
                }
            },
            {"$project": {
                "items": {"$concatArrays": ["$nested_items", "$flat_items"]}
            }},
            {"$unwind": "$items"}
        ]

        if category:
            pipeline.append({"$match": {"items.category": {"$regex": f"^{category}$", "$options": "i"}}})

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
                },
                # Thêm bước để lấy review_text từ food_review
                "items.review_text": {
                    "$map": {
                        "input": {"$ifNull": ["$items.food_review", []]},
                        "as": "review",
                        "in": "$$review.review_text"
                    }
                }
            }
        })

        if min_rating > 0:
            pipeline.append({"$match": {"items.average_rating": {"$gte": min_rating}}})

        pipeline.append({
            "$project": {
                "_id": 0,
                "place_id": "$items.place_id",
                "restaurant_name": "$items.restaurant_name",
                "dish_name": "$items.dish_name",
                "price": "$items.price",
                "category": "$items.category",
                "average_rating": "$items.average_rating",
                "description": "$items.description",
                "feature_img": "$items.feature_img",
                "food_review": "$items.food_review",
                "review_text": "$items.review_text",
                "rating": "$items.rating"
            }
        })

        pipeline.append({"$sort": {"price": sort_order}})
        pipeline.append({"$skip": skip})
        pipeline.append({"$limit": limit})

        results = list(collection.aggregate(pipeline))
        logger.info(f"Found {len(results)} dishes")
        return results

    except ServerSelectionTimeoutError as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        return []
    except OperationFailure as e:
        logger.error(f"Query failed: {e}")
        return []
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return []
    finally:
        if 'client' in locals():
            client.close()