from bson import ObjectId

from project.src.DatabaseManager import DatabaseManager

class ReviewModel:
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

    def get_review_list_by_restaurant(self, use_pagination=True):
        if not self.place_id:
            print("ReviewModel: No place_id provided, cannot fetch reviews.")
            return []

        print(f"ReviewModel: Querying reviews for place_id {self.place_id}")
        try:
            if use_pagination:
                review = self.db_manager.get_menu_by_place_id(self.place_id, self._offset, self._limit)
                self._offset += len(review)
                if self._total_items == 0:
                    restaurant_collection = self.db_manager.db["Restaurants"]
                    self._total_items = restaurant_collection.count_documents({"place_id": ObjectId(self.place_id)})
                self._has_more = self._offset < self._total_items
            else:
                review = self.db_manager.get_menu_by_place_id(self.place_id, offset=0, limit=None)
                self._has_more = False
            print(f"ReviewModel: Retrieved {len(review)} review items")
            return review
        except Exception as e:
            print(f"ReviewModel: Error retrieving review list: {e}")
            return []
    def add_review_to_menu(self, review):
        """Thêm đánh giá vào menu của nhà hàng."""
        if not self.place_id:
            print("ReviewModel: No place_id provided, cannot add review.")
            return False

        try:
            review["place_id"] = ObjectId(self.place_id)  # Ensure place_id is an ObjectId
            success = self.db_manager.add_review_to_menu(review)
            if success:
                print("ReviewModel: Review successfully added.")
            else:
                print("ReviewModel: Failed to add review.")
            return success
        except Exception as e:
            print(f"ReviewModel: Error adding review: {e}")
            return False




    def get_review_list_by_food(self, product_id=None,use_pagination=True):
        if not product_id:
            print("ReviewModel: No product_id provided, cannot fetch reviews.")
            return []

        print(f"ReviewModel: Querying reviews for product_id {self.product_id}")
        try:
            if use_pagination:
                review = self.db_manager.get_review_list_by_food(self.product_id, self._offset, self._limit)
                self._offset += len(review)
                if self._total_items == 0:
                    self._total_items = self.menu.count_documents({"product_id": ObjectId(self.place_id)})
                self._has_more = self._offset < self._total_items
            else:
                review = self.db_manager.get_review_list_by_food(self.product_id, offset=0, limit=None)
                self._has_more = False
            print(f"ReviewModel: Retrieved {len(review)} review items")
            return review
        except Exception as e:
            print(f"ReviewModel: Error retrieving review list: {e}")
            return []

    def has_more(self):
        return self._has_more

    def offset(self):
        return self._offset

    def close_connection(self):
        self.db_manager.close_connection()