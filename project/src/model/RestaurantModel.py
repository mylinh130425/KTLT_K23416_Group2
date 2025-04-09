from project.src.DatabaseManager import DatabaseManager


class Restaurant:
    def __init__(self, _id=None, name=None, address=None, city=None, detailed_address=None, description=None, reviews=None,
                 rating=None, competitors=None, website=None, phone=None,
                 featured_image=None, main_category=None, categories=None,
                 workday_timing=None, is_temporarily_closed=False, is_permanently_closed=False,
                 closed_on=None, review_keywords=None, link=None, status=None,
                 price_range=None, reviews_per_rating=None, featured_question=None, reviews_link=None,
                 coordinates=None, email=None,
                 about=None, images=None, hours=None, most_popular_times=None,
                 popular_times=None, menu=None, reservations=None, order_online_links=None,
                 featured_reviews=None, detailed_reviews=None):
        self.db_manager = DatabaseManager()
        if _id is not None:
            restaurant_data = self.db_manager.get_restaurant_by_id(_id)
            # print("restaurant data directly from db", restaurant_data)
            for key, value in restaurant_data.items():
                setattr(self, key, value)
            # self._id = _id
        else:
            if name is None or city is None or address is None or len(name)==0 or len(city)==0 or len(address)==0:
                raise ValueError("Required fields - name, city, address - are invalid")
            self.name = name  # Restaurant name *
            self.description = description or ""  # Restaurant description
            self.reviews = reviews or 0  # Number of reviews
            self.rating = rating  # Average rating
            self.competitors = competitors or []  # List of competitors
            self.website = website or ""  # Restaurant website
            self.phone = phone or ""  # Phone number
            self.featured_image = featured_image  # Featured image
            self.main_category = main_category  # Main category of the restaurant
            self.categories = categories or []  # List of subcategories
            self.workday_timing = workday_timing or ""  # Working hours
            self.is_temporarily_closed = is_temporarily_closed or False  # Is the restaurant temporarily closed?
            self.is_permanently_closed = is_permanently_closed or False  # Is the restaurant permanently closed?
            self.closed_on = closed_on or ""  # Closing date (if applicable)
            self.address = address  # Restaurant address *
            self.review_keywords = review_keywords or ""  # Review keywords
            self.link = link or ""  # Link to restaurant details page
            self.status = status or ""  # Operating status
            self.email=email or "" #email
            self.price_range = price_range or ""  # Price range
            self.reviews_per_rating = reviews_per_rating or []  # Number of reviews per rating level
            self.featured_question = featured_question or {}  # Featured question about the restaurant
            self.reviews_link = reviews_link or ""  # Link to reviews
            self.coordinates = coordinates or []  # Geographic coordinates (longitude, latitude)
            self.detailed_address = detailed_address or {"street": "", "state": "",
                                                         "postal_code": None, "country": "Vietnam","ward":"",
                                                         "country_code":"VN"}  # Detailed address
            self.detailed_address["city"]= city #city*
            self.about = about or []  # Additional information about the restaurant
            self.images = images or []  # List of restaurant images
            self.hours = hours or []  # Opening hours for each day
            self.most_popular_times = most_popular_times or []  # Peak hours
            self.popular_times = popular_times or {}  # Popular times
            self.menu = menu or []  # Menu items
            self.reservations = reservations or []  # Reservation information
            self.order_online_links = order_online_links or []  # Online ordering links
            self.featured_reviews = featured_reviews or []  # Featured reviews
            self.detailed_reviews = detailed_reviews or []  # List of detailed reviews


    def to_dict(self):
        """Convert the object into a dictionary for MongoDB storage."""
        json_data = self.__dict__.copy()
        del json_data["db_manager"]
        return json_data

    @staticmethod
    def from_dict(data):
        """Initialize an object from a dictionary (data from MongoDB)."""
        return Restaurant(**data)

    def add_restaurant(self):
        # Basic validation
        if len(self.name.strip())==0 or len(self.detailed_address["city"].strip())==0 or  len(self.address.strip())==0:
            print("⚠️ Required fields missing!")
            return False, "Restaurant name, city, and address are required."
        else:
            restaurant_data = self.to_dict()
            print("adding restaurant with the following data", restaurant_data)
            self.db_manager.add_restaurant_to_db(restaurant_data)
            return True, "Restaurant added successfully!"
        self.db_manager.close_connection()
    def update_restaurant_by_id(self):
        if self._id is None or len(self.name.strip())==0 or len(self.detailed_address["city"].strip())==0 or  len(self.address.strip())==0:
            print("⚠️ Required fields missing!")
            return False, "_id, Restaurant name, city, and address are required."
        else:
            restaurant_data = self.to_dict()
            print("adding restaurant with the following data", restaurant_data)
            self.db_manager.update_restaurant_to_db(self._id,restaurant_data)
            return True, "Restaurant added successfully!"
        self.db_manager.close_connection()

    def update_fields(self, source, target):
        """
        Recursively update fields in the target object with values from the source object
        if they differ and are not None or empty (after stripping).
        """
        if isinstance(source, dict) and isinstance(target, dict):
            for key in source:
                if key in target:
                    if isinstance(source[key], (dict, list)):
                        # Recursive call for nested dicts or lists
                        self.update_fields(source[key], target[key])
                    else:
                        # Check if values are different and non-empty
                        if (
                            source[key] is not None
                            and isinstance(source[key], str)
                            and source[key].strip() != ""
                            and target[key] != source[key]
                        ):
                            target[key] = source[key]
                else:
                    # Add missing key from source
                    target[key] = source[key]
        elif isinstance(source, list) and isinstance(target, list):
            # Update lists element by element
            for i in range(min(len(source), len(target))):
                if isinstance(source[i], (dict, list)):
                    self.update_fields(source[i], target[i])
                elif (
                    source[i] is not None
                    and isinstance(source[i], str)
                    and source[i].strip() != ""
                    and target[i] != source[i]
                ):
                    target[i] = source[i]

    def compare_and_update(self, new_restaurant):
        """
        Compare and update fields of this Restaurant instance with the new_restaurant data.
        """
        self.update_fields(new_restaurant.to_dict(), self.to_dict())

class RestaurantModel:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.limit = 200
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
    def add_restaurant(self, restaurant_data=None):
        # Basic validation
        if not len(self.name.strip())>0 or not len(self.city.strip())>0 or not len(self.details_address)>0:
            if not restaurant_data["name"] or not restaurant_data["city"] or not restaurant_data["details_address"]:
                print("⚠️ Required fields missing!")
                return False, "Restaurant name, city, and address are required."
            else:
                success = self.db_manager.add_restaurant_to_db(restaurant_data)
        else:
            success = self.db_manager.add_restaurant_to_db(self.to_dict())
        if success:
            return True, "Restaurant added successfully!"
        else:
            return False, "Failed to add restaurant (maybe duplicate or DB error)."
        self.db_manager.close_connection()

    def delete_restaurant_by_id(self,_id):
        return self.db_manager.delete_restaurant_by_id(_id)

