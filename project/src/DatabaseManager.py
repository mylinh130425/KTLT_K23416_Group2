from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

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
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.users = self.db["Users"]
        # Đảm bảo username và email là duy nhất
        self.users.create_index("username", unique=True)
        self.users.create_index("email", unique=True)


    def get_restaurants(self, offset=0, limit=15):
        """Fetch a batch of restaurants with pagination."""
        collection = self.db["Restaurants"]
        restaurant_data = collection.find({}).skip(offset).limit(limit)
        restaurants = []

        for data in restaurant_data:
            # Extract open hours safely
            hours_data = data.get("hours", [])
            open_hours = self.format_hours(hours_data)
            about_data = data.get("about",[])
            accessibility_texts = self.format_accessibility(about_data)
            restaurant = {
                "_id":data.get("_id",""),
                "featured_image": data.get("featured_image"),
                "name": data.get("name", ""),
                "rating": data.get("rating", 0),
                "open_hours": open_hours,
                "category": "\n".join(data.get("categories", "")),
                "address": data.get("address", ""),
                "hotline": data.get("phone", ""),
                "accessibility": "\n".join(accessibility_texts),
            }
            restaurants.append(restaurant)

        return restaurants

    def get_menu_by_place_id(self, place_id, offset=0,limit=15):
        """Trả về danh sách món ăn của nhà hàng dựa trên place_id với các trường cụ thể."""
        menu_collection = self.db["Menu"]
        menu_data = menu_collection.find_one({"place_id": place_id}).skip(offset).limit(limit)

        menu_list = []
        for item in menu_data["menu"]:
            menu_entry = {
                "_id": item.get("product_id"),
                "Item": item.get("name"),
                "featured_image":item.get("feature_image"),
                "Rate": item.get("rating"),
                "Price": [price_info["price"] for price_info in item.get("pricing", [])],
                "Description": item.get("description"),
                "Review": [review["review_text"] for review in item.get("item_review", [])]
            }
            menu_list.append(menu_entry)

        return menu_list



    def format_hours(self, hours_list):
        """Convert list of opening hours into a readable string.
         TODO: Bản - Cần chỉnh lại format của giờ hiển thị
          nên gom lại giờ giống nhau vào 1 nơi"""
        if not isinstance(hours_list, list) or not hours_list:
            return "No Data"

        formatted_hours = []

        for day in hours_list:
            if "day" in day and "times" in day:
                # Extract first time range if it's a list
                times = day["times"]
                if isinstance(times, list) and times:
                    times = times[0]  # Get the first element if it's a list

                # Fix Unicode escape sequences like "\u202f" (narrow no-break space)
                times = times.replace("\u202f", " ").strip()

                # Format: "Mon: 10 AM - 9 PM"
                formatted_hours.append(f"{day['day'][:3]}: {times}")

        return " | ".join(formatted_hours)

        # Database connection
    def format_accessibility(self, about_list):
        """
        :param about_list:
        :return:
        """
        accessibility_texts = []
        # if "about" in restaurant:
        for about_item in about_list:
            # if "options" in about_item:
            if about_item["id"] == "payments" or about_item["id"]=="parking":
                for option in about_item["options"]:
                    accessibility_texts.append(option["name"])
        # Cập nhật giá trị mới cho accessibility
        return accessibility_texts

    def register_user(self, username: str, fullname: str, password: str) -> bool:
        """Đăng ký người dùng mới"""
        user = UserModel(username, fullname, password)

        try:
            self.users.insert_one(user.to_dict())
            print(f"✅ User {fullname} signed up successfully!")
            return True
        except DuplicateKeyError:
            print(f"⚠️ Error: Username or email existed in the database!")
            return False

    def login_user(self, username: str, password: str) -> bool:
        """Xác thực đăng nhập người dùng"""
        user_data = self.users.find_one({"username": username})

        if user_data:
            user = UserModel(user_data["username"], user_data["fullName"], user_data["passwordHash"], is_hashed=True)
            if user.verify_password(password):
                print("✅ Successfully logged in!")
                return True
            else:
                print("❌ Wrong password!")
                return False
        else:
            print("❌ User Not Found!")
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
