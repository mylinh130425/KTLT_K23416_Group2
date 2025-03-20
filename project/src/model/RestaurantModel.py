from project.src.DatabaseManager import DatabaseManager

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
