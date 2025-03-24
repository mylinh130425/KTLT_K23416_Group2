from project.src.DatabaseManager import DatabaseManager


class RestaurantModel:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.limit = 15
        self.offset = 0
        self._has_more = True

    def get_restaurants(self):
        restaurants = self.db_manager.get_restaurants(
            offset=self.offset,
            limit=self.limit
        )

        print(f"RestaurantModel: Retrieved {len(restaurants)} restaurants")
        if len(restaurants) < self.limit:
            self._has_more = False
        else:
            self.offset += self.limit

        return restaurants

    def has_more(self):
        return self._has_more

    def reset_pagination(self):
        self.offset = 0
        self._has_more = True