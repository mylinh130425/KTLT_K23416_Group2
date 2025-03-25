from PyQt6 import QtWidgets
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QFileDialog, QCheckBox, QLineEdit
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest

from project.src.model.RestaurantModel import Restaurant
from project.src.view.ClickableLabel import ClickableLabel


class ModifyRestaurantScreen(QtWidgets.QWidget):
    def __init__(self, parent=None, isCreating=True, restaurant_id=None):
        super().__init__()
        print("setting up Modify Restaurant Screen")
        self.parent = parent
        self.restaurant_data = None
        self.isCreating = isCreating # True "create" or False "edit"
        self.current_restaurant_id = restaurant_id  # Only used in edit mode
        # Tạo NetworkAccessManager ngay khi khởi tạo
        self.image_manager = QNetworkAccessManager()
        self.image_manager.finished.connect(self.set_image)

        if not isCreating:
            self.setup_ui_edit()
        else:
            self.setup_ui_create()
        self.processSignalsSlots()
        self.parent.restaurant_form_photo_label = ClickableLabel()
        self.parent.restaurant_form_photo_label.setText("Restaurant")
        self.parent.restaurant_form_photo_label.setStyleSheet("border: 1px solid gray; padding: 5px;")
        self.parent.restaurant_form_photo_label.setFixedSize(200, 200)  # Adjust size as needed

        self.restaurant_new_image_path = ""  # Variable to store the image path

        # Connect click signal to function
        self.parent.restaurant_form_photo_label.clicked.connect(self.open_file_dialog)


        # Weekday order to ensure proper chronological updates
        self.weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

        # Dictionaries to hold references to widgets
        self.checkboxes = {}
        self.opening_hours = {}
        self.closing_hours = {}

        # Collect existing widgets
        self.collect_widgets()

        # Update fields based on checkbox selection
        self.update_weekday_fields()

        # Connect checkboxes to update function
        for checkbox in self.checkboxes.values():
            checkbox.stateChanged.connect(self.update_weekday_fields)

        self.parent.create_restaurant_button.clicked.connect(self.add_restaurant)

    def collect_widgets(self):
        """Find all existing QLineEdit and QCheckBox widgets dynamically."""
        for day in self.weekdays:
            # Find QCheckBox
            checkbox = self.parent.findChild(QCheckBox, f"{day}_checkBox")
            if checkbox:
                self.checkboxes[day] = checkbox

            # Find QLineEdit fields
            lineedit_1 = self.parent.findChild(QLineEdit, f"{day}_1")
            lineedit_2 = self.parent.findChild(QLineEdit, f"{day}_2")

            if lineedit_1:
                self.opening_hours[day] = lineedit_1
            if lineedit_2:
                self.closing_hours[day] = lineedit_2

    def update_weekday_fields(self):
        """Update all checked weekdays' QLineEdit fields based on the first non-empty value found."""
        first_value_1 = None
        first_value_2 = None

        # Find the first non-empty _1 and _2 values
        for day in self.weekdays:
            if self.checkboxes.get(day, None) and self.checkboxes[day].isChecked():
                if first_value_1 is None and day in self.opening_hours:
                    first_value_1 = self.opening_hours[day].text()
                if first_value_2 is None and day in self.closing_hours:
                    first_value_2 = self.closing_hours[day].text()

        # Apply found values to all checked checkboxes' QLineEdit fields
        for day in self.weekdays:
            if self.checkboxes.get(day, None) and self.checkboxes[day].isChecked():
                if first_value_1 is not None and day in self.opening_hours:
                    self.opening_hours[day].setText(first_value_1)
                if first_value_2 is not None and day in self.closing_hours:
                    self.closing_hours[day].setText(first_value_2)

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None, "Select an Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if file_path:  # If a file is selected
            self.restaurant_new_image_path = file_path  # Save the path
            self.restaurant_form_photo_label.setPixmap(QPixmap(file_path).scaled(
                self.restaurant_form_photo_label.width(),
                self.restaurant_form_photo_label.height()
            ))  # Load image to QLabel instantly
        print(self.restaurant_new_image_path)

    def update_restaurant_photo(self, image_url):
        """Gửi request để tải ảnh từ URL."""
        request = QNetworkRequest(QUrl(image_url))
        self.image_manager.get(request)

        print(request)




    def set_image(self, reply):
        """Cập nhật QLabel với ảnh từ URL."""
        data = reply.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(data)

        if not pixmap.isNull():  # Kiểm tra xem ảnh có hợp lệ không
            self.restaurant_photo_label.setPixmap(pixmap)
            self.restaurant_photo_label.setFixedSize(pixmap.size())
        else:
            self.restaurant_photo_label.setText("Failed to load image")

    def setup_ui_create(self):
        pass
    def setup_ui_edit(self):
        # Initialize all the UI components here
        # === Global QPushButton Style ===
        add_edit_restaurant_style = """
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
            QLineEdit{
            
            }
        """
        # Apply the style to all QPushButtons and QLineEdits in this screen
        self.parent.modify_restaurant_page.setStyleSheet(add_edit_restaurant_style)
        self.restaurant_data = self.parent.db_manager.get_restaurant_byid(self.current_restaurant_id)
        print(self.current_restaurant_id)
        print(f"Restaurant data in modify restaurant screen: {self.restaurant_data}")
        if not self.restaurant_data:
            print("Không tìm thấy dữ liệu nhà hàng")
            return
        # self.setup_Ui()


    def setup_Ui(self):
        # self.parent.restaurant_info_avatar.setText(self.restaurant_data["name"])
        self.parent.restaurant_photo_label.setScaledContents(True)
        # Tạo NetworkAccessManager để tải ảnh
        self.image_manager = QNetworkAccessManager()
        self.image_manager.finished.connect(self.set_image)
        # Gọi hàm cập nhật ảnh với URL mong muốn
        self.update_restaurant_photo(self.restaurant_data["featured_image"])
        self.parent.form_res_name.setText(self.restaurant_data["name"])

        self.parent.form_category.setText(", ".join(self.restaurant_data["category"]))

        address = self.restaurant_data["detailed_address"]
        # address_str = f"{address['street']}, {address['ward']}, {address['city']}, {address['state']}"
        self.parent.form_country.setText("Viet Nam")
        self.parent.form_city.setText(self.restaurant_data["address"]["city"])

        self.parent.form_area.setText(self.restaurant_data["address"]["state"])
        self.parent.website_input.setText(self.restaurant_data["website"])
        self.parent.about_input.setText("\n".join(self.restaurant_data["about"]))


    def add_restaurant(self):
        print("clicked create res button")
        self.form_res_name = self.parent.form_res_name
        self.form_category = self.parent.form_category
        self.form_country = self.parent.form_country
        self.form_city  = self.parent.form_city

        self.form_area = self.parent.form_country
        self.form_address = self.parent.form_address
        self.form_phone = self.parent.form_phone
        self.form_mail=self.parent.form_mail
        self.form_website = self.parent.form_website

        if self.parent.all_days_checkBox.isChecked():
            self.update_weekday_fields()
        self.new_restaurant = Restaurant(name=self.form_res_name,main_category=self.form_category,
                                         detailed_address={'ward':self.form_area, 'country':self.form_country, 'city':self.form_city},
                                         phone=self.form_phone, mail=self.mail, website=self.form_website)
        try:
            self.parent.db_manager.add_restaurant_to_db(self.new_restaurant.to_dict())
            self.parent.db_manager.close_connection()
        except Exception as e:
            print(f"Cannot add restaurant due to {e}")


    def processSignalsSlots(self):

        self.parent.restaurant_info_button.clicked.connect(self.goInfo)
        self.parent.restaurant_menu_button.clicked.connect(self.goMenu)
        self.parent.restaurant_review_button.clicked.connect(self.goReview)

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

    def get_restaurant_data_input(self):
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

    def get_opening_hours_input(self):
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
    def get_services_input(self):
        services = {
            "parking": self.parking_checkbox.isChecked(),
            "reservations": self.reservations_checkbox.isChecked(),
            "delivery": self.delivery_checkbox.isChecked(),
            "service_options": {
                "delivery": self.delivery_option_checkbox.isChecked(),
                "dine_in": self.dinein_checkbox.isChecked(),
                "takeout": self.takeout_checkbox.isChecked(),
                "air_conditioner": self.ac_checkbox.isChecked(),
                "outdoor_seating": self.outdoor_checkbox.isChecked()
            },
            "notes": {
                "parking_note": self.parking_note_lineEdit.text().strip(),
                "reservations_note": self.reservations_note_lineEdit.text().strip(),
                "delivery_note": self.delivery_note_lineEdit.text().strip()
            }
        }
        return services

    # def get_social_links(self):
    #     return {
    #         "facebook": self.facebook_link,  # e.g., from a button or field
    #         "instagram": self.instagram_link,
    #         "tiktok": self.tiktok_link
    #     }

    def goInfo(self):
        self.parent.restaurant_stackedWidget.setCurrentWidget(self.parent.modify_restaurant_page)
    def goMenu(self):
        self.parent.restaurant_stackedWidget.setCurrentWidget(self.parent.menu_page)
    def goReview(self):
        self.parent.restaurant_stackedWidget.setCurrentWidget(self.parent.review_restaurant_page)