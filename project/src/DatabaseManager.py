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
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

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
        TODO: Bản - Cần check lại dữ liệu xem hiển thị
          thông tin gì ở cột Accessibility thì ok
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


if __name__ == "__main__":
    """ phần code để test kết nối db trong file này, 
       có thể sửa lại code bên dưới để test theo nhu cầu"""
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
