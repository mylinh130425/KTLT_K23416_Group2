from PyQt6 import QtWidgets

class ModifyRestaurantScreen(QtWidgets.QWidget):
    def __init__(self, parent=None, isCreating=True):
        super().__init__()
        self.parent = parent
        # self.restaurant_model = restaurant_model
        self.isCreating = isCreating # True "create" or False "edit"
        self.current_restaurant_id = None  # Only used in edit mode
        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        # Initialize all the UI components here
        # === Global QPushButton Style ===
        button_style = """
            QPushButton {
                background-color: #FF914D;       /* Vibrant orange */
                color: white;
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF7A2E;
            }
            QPushButton:pressed {
                background-color: #E66300;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #666666;
            }
        """
        # Apply the style to all QPushButtons in this screen
        self.parent.add_restaurant_page.setStyleSheet(button_style)

    def setup_signals(self):
        self.create_button.clicked.connect(self.handle_submit)

    # === MODE SELECTORS ===
    def create_mode(self):
        self.mode = "create"
        self.clear_fields()
        self.create_button.setText("Create")
        self.show()  # or use switch_screen from ExtInterface

    def edit_mode(self, restaurant_data):
        self.mode = "edit"
        self.current_restaurant_id = restaurant_data["_id"]
        self.populate_fields(restaurant_data)
        self.create_button.setText("Update")
        self.show()

    # === FIELD MANAGEMENT ===
    def clear_fields(self):
        # Clear all input fields
        pass

    def populate_fields(self, data):
        # Populate UI with existing restaurant data
        self.name_lineEdit.setText(data.get("name", ""))
        self.city_lineEdit.setText(data.get("city", ""))
        self.details_address_lineEdit.setText(data.get("details_address", ""))
        # Populate other fields...

    # === SUBMIT HANDLER ===
    def handle_submit(self):
        restaurant_data = self.get_restaurant_data()
        if self.mode == "create":
            success, message = self.restaurant_model.add_restaurant(restaurant_data)
        else:
            success, message = self.restaurant_model.update_restaurant(self.current_restaurant_id, restaurant_data)

        if success:
            self.show_message("Success", message)
            self.switch_screen("restaurant_list")  # Example navigation
        else:
            self.show_message("Error", message, success=False)

    # === DATA GATHERING FROM USER INPUT ===

    def get_restaurant_data(self):
        data = {
            "name": self.name_lineEdit.text().strip(),
            "category": self.category_comboBox.currentText(),
            "country": self.country_lineEdit.text().strip(),
            "city": self.city_lineEdit.text().strip(),
            "area": self.area_lineEdit.text().strip(),
            "details_address": self.details_address_lineEdit.text().strip(),
            "hotline": self.hotline_lineEdit.text().strip(),
            "email": self.email_lineEdit.text().strip(),
            "website": self.website_lineEdit.text().strip(),
            "opening_hours": self.get_opening_hours(),
            "services": self.get_services(),
            "social_media": self.get_social_links()
        }
        return data

    def get_opening_hours(self):
        # Collect opening/closing times, handle "Same All Days"
        hours = {}
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            day_checkbox = getattr(self, f"{day.lower()}_checkbox")
            if day_checkbox.isChecked():
                open_time = getattr(self, f"{day.lower()}_open").text().strip()
                close_time = getattr(self, f"{day.lower()}_close").text().strip()
                hours[day] = {"open": open_time, "close": close_time}
        return hours
    #
    # def get_services(self):
    #     services = {
    #         "parking": self.parking_checkbox.isChecked(),
    #         "reservations": self.reservations_checkbox.isChecked(),
    #         "delivery": self.delivery_checkbox.isChecked(),
    #         "service_options": {
    #             "delivery": self.delivery_option_checkbox.isChecked(),
    #             "dine_in": self.dinein_checkbox.isChecked(),
    #             "takeout": self.takeout_checkbox.isChecked(),
    #             "air_conditioner": self.ac_checkbox.isChecked(),
    #             "outdoor_seating": self.outdoor_checkbox.isChecked()
    #         },
    #         "notes": {
    #             "parking_note": self.parking_note_lineEdit.text().strip(),
    #             "reservations_note": self.reservations_note_lineEdit.text().strip(),
    #             "delivery_note": self.delivery_note_lineEdit.text().strip()
    #         }
    #     }
    #     return services
    #
    # def get_social_links(self):
    #     return {
    #         "facebook": self.facebook_link,  # e.g., from a button or field
    #         "instagram": self.instagram_link,
    #         "tiktok": self.tiktok_link
    #     }
