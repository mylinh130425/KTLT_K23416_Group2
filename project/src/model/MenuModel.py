from project.src.DatabaseManager import DatabaseManager

class MenuModel:
    def __init__(self, place_id):
        self.db_manager = DatabaseManager()
        self.place_id = place_id
        # self.menu = []  # Lưu danh sách món ăn tại local cache
        self.offset=0
        self.limit=15

    def get_menu(self):
        """Lấy danh sách món ăn từ database theo place_id."""
        menu = self.db_manager.get_menu_by_place_id(self.place_id, self.offset,self.limit)
        self.offset+=len(menu)
        return menu
