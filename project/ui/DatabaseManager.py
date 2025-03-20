from pymongo import MongoClient

class DatabaseManager:
    def __init__(self, uri="mongodb://localhost:27017", db_name="MealMatch"):
        """
        Initialize a DatabaseManager object.

        :param uri: The MongoDB URI for establishing the connection.
                    Defaults to "mongodb://localhost:27017".
        :param db_name: The name of the MongoDB database to connect to.
                        Defaults to "MealMatch".

        :type uri: str
        :type db_name: str
        """
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            print("DatabaseManager: Connected to MongoDB successfully.")
        except Exception as e:
            print(f"DatabaseManager: Failed to connect to MongoDB: {e}")
            self.client = None
            self.db = None

    def get_restaurants(self, offset=0, limit=15): #Chỉnh
        """Fetch a batch of restaurants with pagination."""
        if self.db is None:
            print("DatabaseManager: Cannot fetch restaurants - MongoDB connection failed.")
            return []

        try:
            collection = self.db["Restaurants"]
            restaurant_data = collection.find({}).skip(offset).limit(limit)
            restaurants = []

            for data in restaurant_data:
                # Extract open hours safely
                hours_data = data.get("hours", [])
                open_hours = self.format_hours(hours_data)
                about_data = data.get("about", [])
                accessibility_texts = self.format_accessibility(about_data)
                restaurant = {
                    "_id": str(data.get("_id", "")),  # Chuyển _id thành chuỗi
                    "featured_image": data.get("featured_image", ""),
                    "name": data.get("name", ""),
                    "rating": data.get("rating", 0),
                    "open_hours": open_hours,
                    "category": "\n".join(data.get("categories", [])),
                    "address": data.get("address", ""),
                    "hotline": data.get("phone", ""),
                    "accessibility": "\n".join(accessibility_texts),
                }
                restaurants.append(restaurant)

            if not restaurants:
                print("DatabaseManager: No restaurants found.")
            return restaurants
        except Exception as e:
            print(f"DatabaseManager: Error in get_restaurants: {e}")
            return []

    def get_menu_by_place_id(self, place_id, offset=0, limit=15):
        """
        Trả về danh sách món ăn của nhà hàng dựa trên place_id với các trường cụ thể.
        Args:
            place_id: ObjectId của nhà hàng (trong Restaurant Collection).
            offset: Vị trí bắt đầu của phân trang.
            limit: Số lượng món ăn tối đa (None để lấy tất cả).
        Returns:
            list: Danh sách món ăn.
        """
        if self.db is None:
            print("DatabaseManager: Cannot fetch menu - MongoDB connection failed.")
            return []

        try:
            menu_collection = self.db["Menu"]
            menu_data = menu_collection.find_one({"place_id": place_id})

            if not menu_data:
                print(f"DatabaseManager: No menu found for place_id {place_id}.")
                return []

            menu_items = menu_data.get("menu", [])
            if not menu_items:
                print(f"DatabaseManager: No menu items found for place_id {place_id}.")
                return []

            # Áp dụng phân trang trên mảng menu_items
            if limit is not None:
                menu_items = menu_items[offset:offset + limit]
            else:
                menu_items = menu_items[offset:]

            menu_list = []
            for item in menu_items:
                menu_entry = {
                    "_id": item.get("product_id", "N/A"),
                    "Item": item.get("name", "N/A"),
                    "featured_image": item.get("feature_img", ""),  # Sửa thành feature_img (theo dữ liệu JSON)
                    "Rate": item.get("rating", 0.0),
                    "Price": item.get("pricing", [{}])[0].get("price", 0),  # Chỉ lấy giá đầu tiên
                    "Description": item.get("description", "N/A"),
                    "Review": [review.get("review_text", "") for review in item.get("item_review", [])]
                }
                menu_list.append(menu_entry)

            return menu_list
        except Exception as e:
            print(f"DatabaseManager: Error in get_menu_by_place_id: {e}")
            return []

    def get_all_menus(self, offset=0, limit=15): #Phần thêm mới
        """
        Lấy toàn bộ menu từ tất cả nhà hàng.
        Args:
            offset: Vị trí bắt đầu.
            limit: Số lượng món ăn tối đa (None để lấy tất cả).
        Returns:
            list: Danh sách tất cả món ăn.
        """
        if self.db is None:
            print("DatabaseManager: Cannot fetch menus - MongoDB connection failed.")
            return []

        try:
            menu_collection = self.db["Menu"]
            all_menus = []
            menu_documents = menu_collection.find()

            for menu_data in menu_documents:
                menu_items = menu_data.get("menu", [])
                for item in menu_items:
                    item["restaurant_name"] = menu_data.get("restaurant_name", "Unknown Restaurant")
                all_menus.extend(menu_items)

            if not all_menus:
                print("DatabaseManager: No menu items found from all restaurants.")
                return []

            # Áp dụng phân trang
            if limit is not None:
                all_menus = all_menus[offset:offset + limit]
            else:
                all_menus = all_menus[offset:]

            menu_list = []
            for item in all_menus:
                menu_entry = {
                    "_id": item.get("product_id", "N/A"),
                    "Item": item.get("name", "N/A"),
                    "featured_image": item.get("feature_img", ""),
                    "Rate": item.get("rating", 0.0),
                    "Price": item.get("pricing", [{}])[0].get("price", 0),
                    "Description": item.get("description", "N/A"),
                    "Review": [review.get("review_text", "") for review in item.get("item_review", [])],
                    "restaurant_name": item.get("restaurant_name", "Unknown Restaurant")
                }
                menu_list.append(menu_entry)

            return menu_list
        except Exception as e:
            print(f"DatabaseManager: Error in get_all_menus: {e}")
            return []

    def format_hours(self, hours_list):
        """Convert list of opening hours into a readable string."""
        if not isinstance(hours_list, list) or not hours_list:
            return "No Data"

        formatted_hours = []
        for day in hours_list:
            if "day" in day and "times" in day:
                times = day["times"]
                if isinstance(times, list) and times:
                    times = times[0]
                times = times.replace("\u202f", " ").strip()
                formatted_hours.append(f"{day['day'][:3]}: {times}")

        return " | ".join(formatted_hours)

    def format_accessibility(self, about_list):
        accessibility_texts = []
        for about_item in about_list:
            if about_item.get("id") in ["payments", "parking"]:
                for option in about_item.get("options", []):
                    accessibility_texts.append(option.get("name", ""))
        return accessibility_texts

    def close_connection(self): #Phần thêm mới
        """Đóng kết nối MongoDB."""
        if self.client:
            self.client.close()
            print("DatabaseManager: MongoDB connection closed.")

if __name__ == "__main__":
    """Phần code để test kết nối db trong file này."""
    db_manager = DatabaseManager()

    # Test get_restaurants
    offset = 0
    limit = 8
    restaurants = db_manager.get_restaurants(offset, limit)
    if restaurants:
        print("Restaurants:", restaurants[0])
    else:
        print("No restaurants found!")

    # Test get_menu_by_place_id
    place_id = "67acf97c194023cfe5152311"  # Thay bằng _id của nhà hàng
    menu_items = db_manager.get_menu_by_place_id(place_id, offset=0, limit=15)
    if menu_items:
        print("Menu items:", menu_items)
    else:
        print("No menu items found!")