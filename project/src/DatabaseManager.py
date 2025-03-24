from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Giả sử UserModel đã được định nghĩa
from project.src.model.UserModel import UserModel

class DatabaseManager:
    def __init__(self, uri="mongodb://localhost:27017", db_name="MealMatch"):
        """
        Initialize a DatabaseManager object.
        """
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
                accessibility_texts = self.format_accessibility(about_data)
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
            menu_collection = self.db["Menu"]
            print(f"Type of place_id: {type(place_id)}")
            print(f"Total documents in Menu collection: {menu_collection.count_documents({})}")

            # Chuyển place_id từ chuỗi sang ObjectId
            place_id_obj = ObjectId(place_id)
            print(f"Converted place_id to ObjectId: {place_id_obj}")

            # Tìm tài liệu có place_id khớp với _id của nhà hàng
            menu_data = menu_collection.find_one({"place_id": place_id_obj})
            print(f"Raw menu data: {menu_data}")

            if not menu_data:
                print(f"DatabaseManager: No menu found for place_id {place_id}.")
                all_menus = menu_collection.find({"place_id": place_id_obj})
                print(f"Debug: All documents with place_id {place_id}: {list(all_menus)}")
                all_place_ids = menu_collection.distinct("place_id")
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
                    "featured_image": item.get("feature_img", ""),
                    "Rate": item.get("rating", 0.0),
                    "Price": item.get("pricing", [{}])[0].get("price", 0),
                    "Description": item.get("description", "N/A"),
                    "Review": [review.get("review_text", "") for review in item.get("item_review", [])]
                }
                menu_list.append(menu_entry)
            print(f"{len(menu_list)} items returned from db")
            return menu_list
        except Exception as e:
            print(f"DatabaseManager: Error in get_menu_by_place_id: {e}")
            return []

    def get_all_menus(self, offset=0, limit=15):
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