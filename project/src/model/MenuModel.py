from bson import ObjectId

from project.src.DatabaseManager import DatabaseManager

class MenuModel:
    def __init__(self, place_id=None):
        self.db_manager = DatabaseManager()
        self.place_id = place_id
        self._offset = 0
        self._limit = 15
        self._has_more = True
        self._total_items = 0  # Thêm biến để lưu tổng số mục

    def set_place_id(self, place_id):
        """Cập nhật place_id và reset offset, has_more."""
        if self.place_id != place_id:
            self.place_id = place_id
            self._offset = 0
            self._has_more = True
            self._total_items = 0
            print(f"MenuModel: place_id updated to {self.place_id}, offset reset to 0")

    def get_menu(self, use_pagination=True):
        if not self.place_id:
            print("MenuModel: No place_id provided, cannot fetch menu.")
            return []

        print(f"MenuModel: Querying menu for place_id {self.place_id}")
        try:
            if use_pagination:
                menu_items = self.db_manager.get_menu_by_place_id(self.place_id, self._offset, self._limit)
                self._offset += len(menu_items)
                if self._total_items == 0:
                    menu_collection = self.db_manager.db["Menu"]
                    self._total_items = menu_collection.count_documents({"place_id": ObjectId(self.place_id)})
                self._has_more = self._offset < self._total_items
            else:
                menu_items = self.db_manager.get_menu_by_place_id(self.place_id, offset=0, limit=None)
                self._has_more = False
            print(f"MenuModel: Retrieved {len(menu_items)} menu items")
            return menu_items
        except Exception as e:
            print(f"MenuModel: Error retrieving menu: {e}")
            return []

    def get_all_menus(self, use_pagination=True):
        try:
            if use_pagination:
                menu_items = self.db_manager.get_all_menus(self._offset, self._limit)
                self._offset += len(menu_items)
                # Kiểm tra tổng số mục để xác định has_more
                if self._total_items == 0:
                    menu_collection = self.db_manager.db["Menu"]
                    self._total_items = menu_collection.count_documents({})
                self._has_more = self._offset < self._total_items
            else:
                menu_items = self.db_manager.get_all_menus(offset=0, limit=None)
                self._has_more = False
            print(f"MenuModel: Retrieved {len(menu_items)} menu items from all menus")
            return menu_items
        except Exception as e:
            print(f"MenuModel: Error retrieving all menus: {e}")
            return []

    def has_more(self):
        return self._has_more

    def offset(self):
        return self._offset

    def close_connection(self):
        self.db_manager.close_connection()