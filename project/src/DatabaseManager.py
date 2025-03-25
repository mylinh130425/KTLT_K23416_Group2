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
        self.menu = self.db["Menu"]
        # Đảm bảo username và email là duy nhất
        self.users.create_index("username", unique=True)
        # self.users.create_index("email", unique=True)

    def get_review_list_by_restaurant_id(self, restaurant_id):
        return self.restaurants.find_one({"_id": ObjectId(restaurant_id)})["detailed_reviews"]
    def get_review_list_by_food(self, product_id):
        return self.menu.find_one(
            {"menu.product_id": product_id},
            {"menu.$": 1, "_id": 0}  # Exclude _id if not needed
        )["menu"][0]["item_review"]

    def add_restaurant_to_db(self, restaurant_data: dict) -> bool:
        try:
            self.restaurants.insert_one(restaurant_data)
            print(f"✅ Restaurant {restaurant_data['name']} added to DB!")
            return True
        except Exception as e:
            print(f"❌ Error adding restaurant: {e}")
            return False

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
    # def get_review_by_place_id(self, place_id, offset=0, limit=15):
    #     print(f"DB received place_id: {place_id}")
    #     if self.db is None:
    #         print("DatabaseManager: Cannot fetch reviews - MongoDB connection failed.")
    #         return []
    #
    #     try:
    #         collection = self.db["Restaurants"]
    #         print(f"Type of place_id: {type(place_id)}")
    #         print(f"Total documents in Menu collection: {collection.count_documents({})}")
    #
    #         # Chuyển place_id từ chuỗi sang ObjectId
    #         place_id_obj = ObjectId(place_id)
    #         print(f"Converted place_id to ObjectId: {place_id_obj}")
    #
    #         # Tìm tài liệu có place_id khớp với _id của nhà hàng
    #         restaurant_reviews = collection.find_one({"place_id": place_id_obj})
    #         print(f"Raw menu data: {restaurant_reviews}")
    #
    #         if not restaurant_reviews:
    #             print(f"DatabaseManager: No review found for place_id {place_id}.")
    #             all_restaurant_reviews = collection.find({"place_id": place_id_obj})
    #             print(f"Debug: All documents with place_id {place_id}: {list(all_restaurant_reviews)}")
    #             all_place_ids = collection.distinct("place_id")
    #             print(f"All place_ids in Restaurant collection: {all_place_ids}")
    #             return []
    #
    #         review_list_data = restaurant_reviews.get("detailed_reviews", [])
    #         if not review_list_data:
    #             print(f"DatabaseManager: No reviews found for place_id {place_id}.")
    #             return []
    #
    #         if limit is not None:
    #             review_list_data = review_list_data[offset:offset + limit]
    #         else:
    #             review_list_data = review_list_data[offset:]
    #
    #         review_list = []
    #         for item in review_list_data:
    #             review_entry = {}
    #             for key, value in item.items():
    #                 setattr(review_entry, key, value)
    #             review_list.append(review_entry)
    #         print(f"{len(review_list)} items returned from db")
    #         print(review_list[0])
    #         return review_list
    #     except Exception as e:
    #         print(f"DatabaseManager: Error in get_menu_by_place_id: {e}")
    #         return []

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


    def get_restaurant_byid(self, restaurant_id: str):
        try:
            restaurant_data = self.restaurants.find_one({"_id": ObjectId(restaurant_id)})
            print(type(restaurant_data))
            if not restaurant_data:
                return None

            # return {
            #     "featured_image": restaurant_data.get("featured_image", ""),
            #     "name": restaurant_data.get("name", "Unknown"),
            #     "category": restaurant_data.get("categories", []),
            #     "address": {
            #         "city": restaurant_data.get("detailed_address", {}).get("city", ""),
            #         "state": restaurant_data.get("detailed_address", {}).get("state", ""),
            #         "ward": restaurant_data.get("detailed_address", {}).get("ward", ""),
            #         "street": restaurant_data.get("detailed_address", {}).get("street", "")
            #     },
            #     "detailed_address": restaurant_data.get("address", ""),
            #     "phone": restaurant_data.get("phone", "N/A"),
            #     "website": restaurant_data.get("website", "N/A"),
            #     "hours": restaurant_data.get("hours", []),
            #     "about": restaurant_data.get("about", [])
            # }
            restaurant_data
        except Exception as e:
            print(f"Error fetching restaurant: {e}")
            return None
    def add_review_to_menu(self, review, product_id):
        try:
            result = self.restaurants.update_one(
                {
                    # "place_id": review["place_id"],
                    "menu.product_id": product_id
                },
                {
                    "$push": {
                        "menu.$.item_review": review["review"]
                    }
                }
            )

            if result.modified_count > 0:
                print("Review added successfully.")
                return True
            else:
                print("No matching food item found.")
                return False

        except Exception as e:
            print(f"Error adding review: {e}")
            return False


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
    restaurant_data = db_manager.get_restaurant_byid(restaurant_id)
    if restaurant_data:
        print("Restaurant data:", restaurant_data)
    else:
        print("No restaurant data found!")

    review_data = db_manager.get_review_list_by_food("HC0001")
    if review_data:
        print("Review data:", review_data)
    else:
        print("No review data found!")

