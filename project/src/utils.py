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

def create_fuzzy_regex(keyword):
    """
    Tạo regex fuzzy từ từ khóa bằng cách loại bỏ các ký tự lặp lại liên tiếp
    và cho phép mỗi ký tự xuất hiện 1 hoặc nhiều lần.
    Ví dụ: "Gogiii" -> "gogi" -> regex: "g+o+g+i+"
    """
    # Chuyển sang chữ thường để chuẩn hóa
    keyword = keyword.lower()
    # Loại bỏ các ký tự lặp lại liên tiếp
    compressed = re.sub(r'(.)\1+', r'\1', keyword)
    # Tạo pattern regex: cho phép mỗi ký tự xuất hiện 1 hoặc nhiều lần
    pattern = ''.join([f"{re.escape(c)}+" for c in compressed])
    return pattern

def search_restaurants_fuzzy(keyword, limit=10):
    """
    Tìm kiếm nhà hàng bằng cách sử dụng regex fuzzy:
    - Xây dựng pattern fuzzy từ từ khóa
    - Truy vấn MongoDB với regex này và giới hạn số kết quả trả về
    
    :param keyword: Từ khóa tìm kiếm
    :param limit: Số lượng kết quả tối đa trả về
    :return: Danh sách các tài liệu nhà hàng khớp với pattern fuzzy
    """
    db = MongoDBConnection().get_database()
    pattern = create_fuzzy_regex(keyword)
    query = {"name": {"$regex": pattern, "$options": "i"}}
    try:
        cursor = db["Restaurants"].find(query).limit(limit)
        return list(cursor)
    except Exception as e:
        logger.error(f"Lỗi khi tìm kiếm nhà hàng: {str(e)}")
        return []

# Ví dụ sử dụng hàm fuzzy search
if __name__ == "__main__":
    connection = MongoDBConnection()
    if connection.connect():
        keyword = "Gogiii"  # từ khóa nhập vào
        restaurants = search_restaurants_fuzzy(keyword, limit=5)
        if restaurants:
            for restaurant in restaurants:
                print(restaurant)
        else:
            print("Không tìm thấy nhà hàng phù hợp.")
        connection.close_connection()
