import re
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongoDBConnection:
    _instance = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
            cls._instance._client = None
        return cls._instance

    def connect(self):
        """Tạo kết nối đến MongoDB"""
        try:
            if not self._client:
                self._client = MongoClient('mongodb://localhost:27017/')
                self._client.admin.command('ping')
                self._db = self._client['MealMatch']
                logger.info("Kết nối MongoDB thành công!")
            return True
        except ConnectionFailure as e:
            logger.error(f"Không thể kết nối đến MongoDB: {str(e)}")
            return False

    def get_database(self):
        """Trả về database instance"""
        if self._db is None:
            self.connect()
        return self._db

    def close_connection(self):
        """Đóng kết nối"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            logger.info("Đã đóng kết nối MongoDB")


def filter_restaurants(min_rating=None, name=None, limit=10):
    """
    Tìm kiếm nhà hàng dựa trên rating tối thiểu và tên sử dụng Aggregation Pipeline

    Args:
        min_rating (float): Rating tối thiểu của nhà hàng
        name (str): Tên nhà hàng (hỗ trợ tìm kiếm gần đúng)
        limit (int): Số lượng kết quả tối đa trả về

    Returns:
        list: Danh sách các nhà hàng thỏa mãn các tiêu chí, sắp xếp theo rating giảm dần
    """
    try:
        db_connection = MongoDBConnection()
        if not db_connection.connect():
            logger.error("Không thể kết nối đến database")
            return []

        db = db_connection.get_database()

        # Tạo pipeline cho aggregation
        pipeline = []

        # Thêm các điều kiện lọc nếu có
        match_conditions = {}
        if min_rating is not None:
            match_conditions["rating"] = {"$gt": float(min_rating)}
        if name:
            match_conditions["name"] = {"$regex": name, "$options": "i"}  # Tìm kiếm không phân biệt hoa thường

        if match_conditions:
            pipeline.append({"$match": match_conditions})

        # Đảm bảo các trường cần thiết được trả về, với giá trị mặc định nếu thiếu
        pipeline.append({
            "$project": {
                "_id": 1,
                "name": {"$ifNull": ["$name", "N/A"]},
                "rating": {"$ifNull": ["$rating", 0]},
                "open_hours": {"$ifNull": ["$workday_timing", "N/A"]},
                "category": {"$ifNull": ["$category", "N/A"]},
                "address": {"$ifNull": ["$address", "N/A"]},
                "hotline": {"$ifNull": ["$hotline", "N/A"]},
                "accessibility": {"$ifNull": ["$accessibility", "N/A"]},
                "featured_image": {"$ifNull": ["$featured_image", ""]}
            }
        })

        # Sắp xếp theo rating giảm dần
        pipeline.append({"$sort": {"rating": -1}})

        # Giới hạn số lượng kết quả
        pipeline.append({"$limit": limit})

        # Thực thi pipeline và trả về kết quả
        results = list(db.Restaurants.aggregate(pipeline))
        return results

    except Exception as e:
        logger.error(f"Lỗi khi tìm kiếm nhà hàng: {str(e)}")
        return []


if __name__ == "__main__":
    try:
        connection = MongoDBConnection()
        if connection.connect():
            # Test với rating > 3 và tên chứa "pizza"
            restaurants = filter_restaurants(min_rating=3, name="pizza")
            print("\nNhà hàng thỏa mãn các tiêu chí:")
            if restaurants:
                for restaurant in restaurants:
                    print(f"- {restaurant['name']}: {restaurant['rating']} sao")
            else:
                print("Không tìm thấy nhà hàng phù hợp.")
    except Exception as e:
        logger.error(f"Lỗi: {str(e)}")
    finally:
        connection.close_connection()