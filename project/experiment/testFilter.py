import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QTextEdit, QComboBox
from PyQt6.QtCore import Qt
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MealMatchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MEALMATCH - Bộ lọc món ăn")
        self.setGeometry(100, 100, 600, 400)

        # Tạo widget chính và layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Danh mục (Category)
        self.category_label = QLabel("Danh mục:")
        self.layout.addWidget(self.category_label)
        self.category_combo = QComboBox()
        self.category_combo.addItems(["", "food", "drink"])  # Danh sách danh mục
        self.layout.addWidget(self.category_combo)

        # Thanh kéo giá (Price)
        self.price_label = QLabel("Price: From 0 to 1,000,000 VND")
        self.layout.addWidget(self.price_label)

        # Thanh kéo cho min_price
        self.min_price_label = QLabel("From:")
        self.layout.addWidget(self.min_price_label)
        self.min_price_slider = QSlider(Qt.Orientation.Horizontal)
        self.min_price_slider.setMinimum(0)
        self.min_price_slider.setMaximum(1000000)
        self.min_price_slider.setValue(0)
        self.min_price_slider.setTickInterval(50000)
        self.min_price_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.min_price_slider.valueChanged.connect(self.update_price_label)
        self.layout.addWidget(self.min_price_slider)

        # Thanh kéo cho max_price
        self.max_price_label = QLabel("To:")
        self.layout.addWidget(self.max_price_label)
        self.max_price_slider = QSlider(Qt.Orientation.Horizontal)
        self.max_price_slider.setMinimum(0)
        self.max_price_slider.setMaximum(1000000)
        self.max_price_slider.setValue(1000000)
        self.max_price_slider.setTickInterval(50000)
        self.max_price_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.max_price_slider.valueChanged.connect(self.update_price_label)
        self.layout.addWidget(self.max_price_slider)

        # Đánh giá tối thiểu (Review)
        self.rating_label = QLabel("Đánh giá tối thiểu (0-5 sao):")
        self.layout.addWidget(self.rating_label)
        self.rating_combo = QComboBox()
        self.rating_combo.addItems(["0", "1", "2", "3", "4", "5"])
        self.layout.addWidget(self.rating_combo)

        # Sắp xếp giá (Sort Order)
        self.sort_label = QLabel("Sắp xếp giá:")
        self.layout.addWidget(self.sort_label)
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["1 (Thấp đến cao)", "-1 (Cao đến thấp)"])
        self.layout.addWidget(self.sort_combo)

        # Nút tìm kiếm
        self.search_button = QPushButton("Tìm kiếm")
        self.search_button.clicked.connect(self.query_dishes)
        self.layout.addWidget(self.search_button)

        # Khu vực kết quả (dùng QTextEdit để hỗ trợ cuộn)
        self.result_text = QTextEdit("Kết quả sẽ hiển thị ở đây")
        self.result_text.setReadOnly(True)
        self.layout.addWidget(self.result_text)

    def update_price_label(self):
        min_price = self.min_price_slider.value()
        max_price = self.max_price_slider.value()
        # Đảm bảo min_price không lớn hơn max_price
        if min_price > max_price:
            self.min_price_slider.setValue(max_price)
            min_price = max_price
        self.price_label.setText(f"Price: From {min_price:,} to {max_price:,} VND")

    def query_dishes(self):
        try:
            # Lấy dữ liệu từ giao diện
            category = self.category_combo.currentText() or None
            min_price = self.min_price_slider.value()
            max_price = self.max_price_slider.value()
            min_rating = float(self.rating_combo.currentText())
            sort_order = 1 if self.sort_combo.currentText() == "1 (Thấp đến cao)" else -1

            # Kiểm tra tham số đầu vào
            if min_price > max_price:
                self.result_text.setText("Lỗi: Giá tối thiểu phải nhỏ hơn hoặc bằng giá tối đa")
                return
            if not 0 <= min_rating <= 5:
                self.result_text.setText("Lỗi: Đánh giá phải trong khoảng 0-5")
                return

            # Kết nối MongoDB
            client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
            client.admin.command("ping")  # Kiểm tra kết nối có thành công không
            db = client["MealMatch"]
            collection = db["Menu"]

            # Kiểm tra dữ liệu trong collection
            total_docs = collection.count_documents({})
            logger.info(f"Total documents in Menu: {total_docs}")
            if total_docs == 0:
                logger.warning("Collection Menu is empty! Please insert data.")
                sample_doc = collection.find_one()
                logger.info(f"Sample document: {sample_doc}")
                self.result_text.setText("Không tìm thấy món nào! Collection trống.")
                return

            # Xây dựng pipeline
            pipeline = [
                {
                    "$facet": {
                        "nested_items": [  # Xử lý dữ liệu dạng lồng nhau (nested) - object
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
                            {"$match": {  # Chỉ lấy món ăn có giá nằm trong khoảng min-max
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
                        "flat_items": [  # Xử lý dữ liệu dạng phẳng (flat) - array
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
                {"$project": {
                    "items": {"$concatArrays": ["$nested_items", "$flat_items"]}
                }},
                {"$unwind": "$items"}
            ]

            # Lọc category sau khi gộp dữ liệu
            if category:
                pipeline.append({"$match": {"items.category": {"$regex": f"^{category}$", "$options": "i"}}})
                # $regex --> tìm category chính xác (drink-drinks)
                # $options: i --> ko phân biệt hoa thường

            # Tính trung bình rating
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
            logger.info(f"Checking for drink in results: {[doc for doc in results if 'drink' in str(doc).lower()]}")
            logger.info(f"Found {len(results)} dishes")

            # Hiển thị kết quả
            output = ""
            if not results:
                output = "Không tìm thấy món nào!\n"
            else:
                output += "\nNAME RES\tFOOD\t\tRATE\tPRICE\tDESCRIPTION\n"
                output += "-" * 60 + "\n"
                for dish in results:
                    stars = int(dish["average_rating"])
                    rate_display = "*" * stars + f" ({stars})" if stars > 0 else "N/A"
                    output += f"{dish['restaurant_name'][:10]:<10}\t{dish['dish_name'][:15]:<15}\t{rate_display:<8}\t{dish['price']:<8}\t{dish['description']}\n"
            self.result_text.setText(output)

        except ServerSelectionTimeoutError as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            self.result_text.setText(f"Lỗi: {e}")
        except OperationFailure as e:
            logger.error(f"Query failed: {e}")
            self.result_text.setText(f"Lỗi: {e}")
        except ValueError as e:
            logger.error(f"Invalid input: {e}")
            self.result_text.setText(f"Lỗi: {e}")
        finally:
            if 'client' in locals():
                client.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MealMatchApp()
    window.show()
    sys.exit(app.exec())