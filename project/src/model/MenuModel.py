from project.src.DatabaseManager import DatabaseManager
from bson.objectid import ObjectId


class MenuModel:
    def __init__(self, place_id=None):
        """Khởi tạo MenuModel với place_id (tùy chọn, là _id của nhà hàng)."""
        self.db_manager = DatabaseManager()
        self.place_id = place_id
        self.menu_cache = []  # Lưu danh sách món ăn tại local cache
        self.offset = 0
        self.limit = 15 # Có thể tăng lên nếu muốn hiển thị nhiều mục hơn
        self.has_more_data = True  # Biến để kiểm tra xem còn dữ liệu để tải không

    def get_menu(self, use_pagination=True): #Chỉnh
        """
        Lấy danh sách món ăn từ database theo place_id (_id của nhà hàng).
        Args:
            use_pagination (bool): Nếu True, lấy theo phân trang; nếu False, lấy toàn bộ.
        Returns:
            list: Danh sách món ăn.
        """
        if not self.place_id:
            print("MenuModel: place_id is not provided. Use get_all_menus() to fetch all menus.")
            return []

        try:
            # Chuyển place_id thành ObjectId để truy vấn
            place_id_obj = ObjectId(self.place_id)
        except Exception as e:
            print(f"MenuModel: Invalid place_id {self.place_id}: {e}")
            return []

        try:
            if use_pagination:
                # Lấy dữ liệu theo phân trang
                menu = self.db_manager.get_menu_by_place_id(place_id_obj, self.offset, self.limit)
                print(len(menu), " items gotten in MenuModel get_menu")

                if menu:
                    self.menu_cache.extend(menu)  # Lưu vào cache
                    self.offset += len(menu)  # Cập nhật offset
                    print(f"MenuModel: Loaded {len(menu)} items for place_id {self.place_id} (offset: {self.offset}).")
                    # Nếu số lượng mục trả về nhỏ hơn limit, có thể đã hết dữ liệu
                    if len(menu) < self.limit:
                        self.has_more_data = False
                        print("MenuModel: No more data to load for this place_id.")
                else:
                    self.has_more_data = False
                    print(f"MenuModel: No more items found for place_id {self.place_id}.")
                return menu
            else:
                # Lấy toàn bộ dữ liệu
                menu = self.db_manager.get_menu_by_place_id(place_id_obj, 0, None)
                print(len(menu), " items gotten in MenuModel get_menu pagination")

                if menu:
                    self.menu_cache = menu  # Lưu toàn bộ vào cache
                    self.offset = len(menu)  # Cập nhật offset
                    self.has_more_data = False
                    print(f"MenuModel: Loaded {len(menu)} items for place_id {self.place_id} (all items).")
                else:
                    self.has_more_data = False
                    print(f"MenuModel: No items found for place_id {self.place_id}.")
                return menu
        except Exception as e:
            print(f"MenuModel: Error loading menu for place_id {self.place_id}: {e}")
            return []

    def get_all_menus(self, use_pagination=True): #Phần thêm mới
        """
        Lấy toàn bộ menu từ tất cả nhà hàng.
        Args:
            use_pagination (bool): Nếu True, lấy theo phân trang; nếu False, lấy toàn bộ.
        Returns:
            list: Danh sách tất cả món ăn từ tất cả nhà hàng.
        """
        try:
            if use_pagination:
                menus = self.db_manager.get_all_menus(self.offset, self.limit)
                if menus:
                    self.menu_cache.extend(menus)
                    self.offset += len(menus)
                    print(f"MenuModel: Loaded {len(menus)} items from all restaurants (offset: {self.offset}).")
                    # Nếu số lượng mục trả về nhỏ hơn limit, có thể đã hết dữ liệu
                    if len(menus) < self.limit:
                        self.has_more_data = False
                        print("MenuModel: No more data to load from all restaurants.")
                else:
                    self.has_more_data = False
                    print("MenuModel: No more items found from all restaurants.")
                return menus
            else:
                menus = self.db_manager.get_all_menus(0, None)
                if menus:
                    self.menu_cache = menus
                    self.offset = len(menus)
                    self.has_more_data = False
                    print(f"MenuModel: Loaded {len(menus)} items from all restaurants (all items).")
                else:
                    self.has_more_data = False
                    print("MenuModel: No items found from all restaurants.")
                return menus
        except Exception as e:
            print(f"MenuModel: Error loading all menus: {e}")
            return []

    def reset_pagination(self): #Phần thêm mới
        """Đặt lại offset và xóa cache để bắt đầu lấy dữ liệu từ đầu."""
        self.offset = 0
        self.menu_cache = []
        self.has_more_data = True
        print("MenuModel: Pagination reset.")

    def get_cached_menu(self): #Phần thêm mới
        """Lấy danh sách món ăn từ cache."""
        return self.menu_cache

    def close_connection(self): #Phần thêm mới
        """Đóng kết nối database (nếu DatabaseManager không tự quản lý)."""
        try:
            self.db_manager.close_connection()
            print("MenuModel: Database connection closed.")
        except Exception as e:
            print(f"MenuModel: Error closing database connection: {e}")

    def has_more(self): #Phần thêm mới
        """Kiểm tra xem còn dữ liệu để tải không."""
        return self.has_more_data