from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, PyMongoError
import re

# Giả sử UserModel đã được định nghĩa
from project.src.model.UserModel import UserModel

class DatabaseManager:
    _instance = None  # Class attribute to hold the singleton instance
    def __new__(cls, *args, **kwargs):
        # Ensure that only one instance is created
        if not cls._instance:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    def __init__(self, uri="mongodb://localhost:27017", db_name="MealMatch"):
        """
        Initialize a DatabaseManager object.

        :param uri: The MongoDB URI for establishing the connection.
                    Defaults to "mongodb://localhost:27017".
        :param db_name: The name of the MongoDB database to connect to.
                        Defaults to "MealMatch".

        :type uri: str
        :type db_name: str
        TODO: all documents should have timestamp fields: created_at, last_updated
        TODO: maybe save edit history in the future
        """
        if not hasattr(self, '_initialized'):  # Prevent reinitialization
            self._initialized = True
            try:
                self.client = MongoClient(uri)
                self.db = self.client[db_name]
                self.users = self.db["Users"]
                self.users.create_index("username", unique=True)
                self.users.create_index("email", unique=True)
                # Thêm log để kiểm tra cơ sở dữ liệu và collection
                print(f"DatabaseManager: Available databases: {self.client.list_database_names()}")
                print(f"DatabaseManager: Available collections in {db_name}: {self.db.list_collection_names()}")
                print("DatabaseManager: Connected to MongoDB successfully.")
            except Exception as e:
                print(f"DatabaseManager: Failed to connect to MongoDB: {e}")
                self.db = None
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            self.users = self.db["Users"]
            self.restaurants=self.db["Restaurants"]
            self.menu_collection = self.db["Menu"]

            # Đảm bảo username và email là duy nhất
            self.users.create_index("username", unique=True)
            # self.users.create_index("email", unique=True)

    def add_restaurant_to_db(self, restaurant_data: dict) -> bool:
        try:
            self.restaurants.insert_one(restaurant_data)
            print(f"Restaurant {restaurant_data['name']} added to DB!")
            return True
        except Exception as e:
            print(f"Error adding restaurant: {e}")
            raise e
    def update_restaurant_to_db(self, _id,restaurant_data: dict) -> bool:
        self.restaurants.update_one({"_id":_id},{"$set":restaurant_data})
        print(f"Restaurant {restaurant_data['name']} added to DB!")

    def get_restaurants(self, offset=0, limit=15):
        if self.db is None:
            print("DatabaseManager: Cannot fetch restaurants - MongoDB connection failed.")
            return []

        try:
            collection = self.db["Restaurants"]
            restaurant_data = collection.find({}).skip(offset).limit(limit)
            restaurants = []

            for data in restaurant_data:
                hours_data = data.get("workday_timing", "N/A")
                if hours_data == "N/A" and "hours" in data:
                    hours_data = self.format_hours(data.get("hours", []))
                about_data = data.get("about", [])
                accessibility_texts = self.format_accessibility(about_data) if isinstance(about_data, list) else []
                restaurant = {
                    "_id": str(data.get("_id", "")),  # Chuyển ObjectId thành chuỗi
                    "featured_image": data.get("featured_image"),
                    "name": data.get("name", ""),
                    "rating": data.get("rating", 0),
                    "open_hours": hours_data,
                    "category": "\n".join(data.get("categories", [])),
                    "address": data.get("address", ""),
                    "hotline": data.get("phone", ""),
                    "accessibility": "\n".join(accessibility_texts),
                }
                restaurants.append(restaurant)

            print(f"DatabaseManager: Retrieved {len(restaurants)} restaurants")
            return restaurants
        except Exception as e:
            print(f"DatabaseManager: Error in get_restaurants: {e}")
            return []

    def get_menu_by_place_id(self, place_id, offset=0, limit=15):
        print(f"DB received place_id: {place_id}")
        if self.db is None:
            print("DatabaseManager: Cannot fetch menu - MongoDB connection failed.")
            return []

        try:
            print(f"Type of place_id: {type(place_id)}")
            print(f"Total documents in Menu collection: {self.menu_collection.count_documents({})}")

            # Chuyển place_id từ chuỗi sang ObjectId
            place_id_obj = ObjectId(place_id)
            print(f"Converted place_id to ObjectId: {place_id_obj}")

            # Tìm tài liệu có place_id khớp với _id của nhà hàng
            menu_data = self.menu_collection.find_one({"place_id": place_id_obj})
            print(f"Raw menu data: {menu_data}")

            if not menu_data:
                print(f"DatabaseManager: No menu found for place_id {place_id}.")
                all_menus = self.menu_collection.find({"place_id": place_id_obj})
                print(f"Debug: All documents with place_id {place_id}: {list(all_menus)}")
                all_place_ids = self.menu_collection.distinct("place_id")
                print(f"All place_ids in Menu collection: {all_place_ids}")
                return []

            menu_items = menu_data.get("menu", [])
            if not menu_items:
                print(f"DatabaseManager: No menu items found for place_id {place_id}.")
                return []

            if limit is not None:
                menu_items = menu_items[offset:offset + limit]
            else:
                menu_items = menu_items[offset:]

            menu_list = []
            for item in menu_items:
                menu_entry = {
                    "_id": item.get("product_id", "N/A"),
                    "Item": item.get("name", "N/A"),
                    "category": item.get("category", "N/A"),
                    "featured_image": item.get("feature_img", ""),
                    "Rate": item.get("rating", 0.0),
                    "Price": item.get("pricing", [{}])[0].get("price", 0),
                    "Description": item.get("description", "N/A"),
                    "Review": [review.get("review_text", "") for review in item.get("item_review", [])]
                }
                menu_list.append(menu_entry)
            print(f"{len(menu_list)} items returned from db")
            print(menu_list[0])
            return menu_list
        except Exception as e:
            print(f"DatabaseManager: Error in get_menu_by_place_id: {e}")
            return []

    def get_all_menus(self, offset=0, limit=15):
        if self.db is None:
            print("DatabaseManager: Cannot fetch menus - MongoDB connection failed.")
            return []

        try:
            all_menus = []
            menu_documents = self.menu_collection.find()

            for menu_data in menu_documents:
                menu_items = menu_data.get("menu", [])
                for item in menu_items:
                    item["restaurant_name"] = menu_data.get("restaurant_name", "Unknown Restaurant")
                all_menus.extend(menu_items)

            if not all_menus:
                print("DatabaseManager: No menu items found from all restaurants.")
                return []

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
                    "category": item.get("category", "N/A"),
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
        if not isinstance(hours_list, list) or not hours_list:
            return "No Data"

        day_hours = []
        for day in hours_list:
            if "day" in day and "times" in day:
                times = day["times"]
                if isinstance(times, list) and times:
                    times = times[0]
                times = times.replace("\u202f", " ").strip()
                day_hours.append((day['day'][:3], times))

        grouped_hours = []
        temp_group = [day_hours[0][0]]
        prev_hours = day_hours[0][1]

        for i in range(1, len(day_hours)):
            current_day, current_hours = day_hours[i]
            if current_hours == prev_hours:
                temp_group.append(current_day)
            else:
                if len(temp_group) > 1:
                    grouped_hours.append(f"{temp_group[0]}-{temp_group[-1]}: {prev_hours}")
                else:
                    grouped_hours.append(f"{temp_group[0]}: {prev_hours}")
                temp_group = [current_day]
                prev_hours = current_hours

        if len(temp_group) > 1:
            grouped_hours.append(f"{temp_group[0]}-{temp_group[-1]}: {prev_hours}")
        else:
            grouped_hours.append(f"{temp_group[0]}: {prev_hours}")

        return " | ".join(grouped_hours)

    def format_accessibility(self, about_list):
        accessibility_texts = []
        for about_item in about_list:
            if about_item["id"] in ["payments", "parking"]:
                for option in about_item["options"]:
                    accessibility_texts.append(option["name"])
        return accessibility_texts

    def register_user(self, username: str, fullname: str, password: str) -> bool:
        user = UserModel(username, fullname, password)
        try:
            self.users.insert_one(user.to_dict())
            print(f"User {fullname} signed up successfully!")
            return True
        except DuplicateKeyError:
            print("Error: Username or email existed in the database!")
            return False

    def login_user(self, username: str, password: str) -> bool:
        user_data = self.users.find_one({"username": username})
        if user_data:
            user = UserModel(user_data["username"], user_data["fullName"], user_data["passwordHash"], is_hashed=True)
            if user.verify_password(password):
                print("Successfully logged in!")
                return True
            else:
                print("Wrong password!")
                return False
        else:
            print("User Not Found!")
            return False

    def logout_user(self, username: str) -> bool:
        user_data = self.users.find_one({"username": username})
        if user_data:
            self.users.update_one({"username": username}, {"$set": {"lastLogin": datetime.now()}})
            print("Successfully logged out!")
            return True
        else:
            print("User Not Found!")
            return False

    def close_connection(self):
        if self.client:
            self.client.close()
            print("DatabaseManager: MongoDB connection closed.")


    def get_restaurant_by_id(self, restaurant_id: str):
        try:
            restaurant_data = self.restaurants.find_one({"_id": ObjectId(restaurant_id)})
            print(type(restaurant_data))
            if not restaurant_data:
                return None

            return restaurant_data
        except Exception as e:
            print(f"Error fetching restaurant: {e}")
            return None

    def get_restaurants_by_keywords(self, keywords: str, offset=0,limit=15):
        # price_pattern=r"([<>]=?|>=|<=|dưới |trên )?(\d+)(k|000| ngàn)?( đồng|\s?VND)?"
        #
        # pricing = re.findall(price_pattern,
        #                              keywords, re.IGNORECASE)
        # pricing_keywords = []
        # if pricing:
        #     for match in pricing:
        #         if match:
        #             print(match)
        #             pricing_keywords.append("".join(match))  # Join the matched groups into a single string
        # exclude = " ".join(pricing_keywords)
        # print(exclude)
        # keyword = "|".join([word for word in keywords.split() if word not in exclude])
        # print(keyword)
        keyword = re.sub(r"\s", "|", keywords)


        try:
            # Tìm kiếm trong collection với điều kiện regex (không phân biệt hoa thường)
            results = self.restaurants.find({
                "$or": [
                    {"name": {"$regex": keyword, "$options": "i"}},
                    {"description": {"$regex": keyword, "$options": "i"}},
                    {"address": {"$regex": keyword, "$options": "i"}},
                    {"phone": {"$regex": keyword, "$options": "i"}},
                    # {"price_range": {"$regex": keyword, "$options": "i"}}
                ]
            })
            return list(results)
        except PyMongoError as e:
            print(f"Lỗi khi tìm kiếm nhà hàng: {e}")
            return []
        # self.close_connection()


    def get_menu_items_by_keywords(self,keywords: str, offset=0,limit=15):
        pass

    def delete_restaurant_by_id(self, _id):
        success = self.restaurants.delete_one({"_id": ObjectId(_id)})

        print("result of delete restaurant by id", success)
        return success


if __name__ == "__main__":
    """ testing db connection and functionality """
    db_manager = DatabaseManager()

    # Set pagination parameters
    offset = 0  # Track loaded data position
    limit = 8  # Load 8 restaurants per batch

    # Fetch restaurants and print the first one to test
    restaurants = db_manager.get_restaurants(offset, limit)

    if restaurants:
        print(restaurants[0])  # Print first restaurant for debugging
    else:
        print("No restaurants found!")
    # Test get_menu_by_place_id
    place_id = "67acf97c194023cfe5152311"  # Thay bằng _id của nhà hàng
    menu_items = db_manager.get_menu_by_place_id(place_id, offset=0, limit=15)
    if menu_items:
        print("Menu items:", menu_items)
    else:
        print("No menu items found!")

    # Test get_restaurant_byid
    restaurant_id = "67acf919194023cfe51522b0"  # Thay bằng _id của nhà hàng
    restaurant_data = db_manager.get_restaurant_by_id(restaurant_id)
    if restaurant_data:
        print("Restaurant data:", restaurant_data)
    else:
        print("No restaurant data found!")

        # Ví dụ sử dụng hàm tìm kiếm
    # search_keyword = input("Nhập từ khóa để tìm kiếm nhà hàng (ví dụ: 'Gỏi Gì'): ")
    search_keyword = "cơm tấm dưới 25000, phở trên 15k, 35 ngàn đồng, 100k VND, <14k"
    results = db_manager.get_restaurants_by_keywords(search_keyword)

    # # Hiển thị kết quả
    # if results:
    #     print(f"Kết quả tìm kiếm cho '{search_keyword}':")
    #     for result in results:
    #         print(f"- Tên: {result['name']}")
    #         print(f"  Mô tả: {result.get('description', 'Không có')}")
    #         print(f"  Địa chỉ: {result.get('address', 'Không có')}")
    #         print(f"  Điện thoại: {result.get('phone', 'Không có')}")
    #         print(f"  Giá: {result.get('price_range', 'Không có')}")
    # else:
    #     print(f"Không tìm thấy nhà hàng nào với từ khóa '{search_keyword}'.")

