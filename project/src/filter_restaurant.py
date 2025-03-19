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

def filter_restaurants(min_rating, limit=10):
    """
    Tìm kiếm nhà hàng dựa trên rating tối thiểu sử dụng Aggregation Pipeline
    
    Args:
        min_rating (float): Rating tối thiểu của nhà hàng
        limit (int): Số lượng kết quả tối đa trả về
        
    Returns:
        list: Danh sách các nhà hàng có rating cao hơn min_rating, 
             sắp xếp theo rating giảm dần
    """
    try:
        db_connection = MongoDBConnection()
        if not db_connection.connect():
            logger.error("Không thể kết nối đến database")
            return []

        db = db_connection.get_database()
        
        # Tạo aggregation pipeline
        pipeline = [
            # Stage 1: Lọc theo rating
            {
                "$match": {
                    "rating": {"$gt": float(min_rating)}
                }
            },
            # Stage 2: Sắp xếp kết quả theo rating giảm dần
            {
                "$sort": {
                    "rating": -1
                }
            },
            # Stage 3: Giới hạn số lượng kết quả
            {
                "$limit": limit
            }
        ]
        
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
            # Test với rating > 3
            min_rating = 3
            restaurants = filter_restaurants(min_rating, limit=5)
            
            print(f"\nNhà hàng có rating > {min_rating}:")
            if restaurants:
                for restaurant in restaurants:
                    print(f"- {restaurant['name']}: {restaurant['rating']} sao")
                    
            else:
                print("Không tìm thấy nhà hàng phù hợp.")
    except Exception as e:
        logger.error(f"Lỗi: {str(e)}")
    finally:
        connection.close_connection()
