from project.src.DatabaseManager import DatabaseManager

class Restaurant:
    def __init__(self, name, ):
        self._id = None
        self.name = None
        self.rating = None
        self.open_hours = None
        self.category = None
        self.address = None
        self.hotline = None
        self.accessibility = None
class RestaurantModel:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.offset = 0
        self.limit = 15  # Load 15 records per batch

    def get_restaurants(self):
        """Lấy danh sách nhà hàng theo phân trang."""
        restaurants = self.db_manager.get_restaurants(self.offset, self.limit)
        self.offset += len(restaurants)  # Cập nhật offset

        return restaurants
    """
        TODO: Xóa bớt dòng chứa nhà hàng đã scroll qua từ lâu (vd khi scroll tới nhà hàng thứ 20 thì nhà hàng 1-5 bị xóa)
        TODO: Load lại nhà hàng đã xóa trước đó khi scroll ngược về
    """

    def add_restaurant(self, restaurant_data):
        # Basic validation
        if not restaurant_data["name"] or not restaurant_data["city"] or not restaurant_data["details_address"]:
            print("⚠️ Required fields missing!")
            return False, "Restaurant name, city, and address are required."

        # You can format any data here if needed (e.g., trim strings, ensure correct formats)

        success = self.db_manager.add_restaurant_to_db(restaurant_data)
        if success:
            return True, "Restaurant added successfully!"
        else:
            return False, "Failed to add restaurant (maybe duplicate or DB error)."

