from PyQt6 import QtWidgets
from PyQt6.QtCore import QUrl, QRectF
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QFileDialog, QCheckBox, QLineEdit, QMessageBox
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt6.QtCore import Qt

from project.src.model.RestaurantModel import Restaurant
from project.src.view.ClickableLabel import ClickableLabel


class ModifyRestaurantScreen(QtWidgets.QWidget):
    def __init__(self, parent=None, isCreating=True, restaurant_id=None):
        super().__init__()
        print("setting up Modify Restaurant Screen")
        self.parent = parent
        self.restaurant_data = None
        self.current_restaurant=None
        self.isCreating = isCreating # True "create" or False "edit"
        self.current_restaurant_id = restaurant_id  # Only used in edit mode
        # Tạo NetworkAccessManager ngay khi khởi tạo
        self.image_manager = QNetworkAccessManager()
        self.image_manager.finished.connect(self.set_image)
        # Store uploaded image path
        self.restaurant_image_path = None


        # Weekday order to ensure proper chronological updates
        self.weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

        # Dictionaries to hold references to widgets
        self.checkboxes = {}
        self.opening_lineEdits = {}
        self.closing_lineEdits = {}
        self.hours=[]

        # Collect existing widgets
        self.collect_widgets()
        if not isCreating:
            self.setup_ui_edit()
        else:
            self.setup_ui_create()
        self.processSignalsSlots()




    def processSignalsAndSlotsOnCreate(self):
        self.parent.create_restaurant_button.clicked.connect(self.add_restaurant)
        # Connect checkboxes to update function
        # self.collect_widgets()
        for checkbox in self.checkboxes.values():
            checkbox.stateChanged.connect(self.update_weekday_fields)
        for lineEdit in self.opening_lineEdits.values():
            lineEdit.textChanged.connect(self.update_opening_fields)
        for lineEdit in self.closing_lineEdits.values():
            lineEdit.textChanged.connect(self.update_closing_fields)
        self.parent.all_days_checkBox.stateChanged.connect(self.update_weekday_fields)
    def update_closing_fields(self):
        if self.sender().text().strip() != "":
            day = self.sender().objectName().split("_")[0]
            self.checkboxes[day].setChecked(True)
        if self.parent.all_days_checkBox.isChecked():
            for day, lineEdit in self.closing_lineEdits.items():
                if self.checkboxes[day].isChecked():
                    lineEdit.setText(self.sender().text())

    def update_opening_fields(self):
        if self.sender().text().strip() !="":
            day=self.sender().objectName().split("_")[0]
            self.checkboxes[day].setChecked(True)
        if self.parent.all_days_checkBox.isChecked():
            for day, lineEdit in self.opening_lineEdits.items():
                if self.checkboxes[day].isChecked():
                    lineEdit.setText(self.sender().text())

    def collect_widgets(self):
        """Find all existing QLineEdit and QCheckBox widgets dynamically."""
        for day in self.weekdays:
            # Find QCheckBox
            checkbox = getattr(self.parent, f"{day}_checkBox")
            self.checkboxes[day] = checkbox

            # Find QLineEdit fields
            lineedit_1 = getattr(self.parent, f"{day}_1")
            lineedit_2 = getattr(self.parent, f"{day}_2")
            if lineedit_1:
                self.opening_lineEdits[day] = lineedit_1
            if lineedit_2:
                self.closing_lineEdits[day] = lineedit_2

    def get_timings(self):
        """Get all timings from existing QLineEdit and QCheckBox widgets dynamically."""
        for day in self.weekdays:
            # Find QCheckBox
            checkbox = getattr(self.parent, f"{day}_checkBox")
            if checkbox.isChecked():
                # Find QLineEdit fields
                opening_hour = getattr(self.parent, f"{day}_1").text().strip()
                closing_hour = getattr(self.parent, f"{day}_2").text().strip()
                self.hours.append({"day":day.title(),"times":["-".join([opening_hour, closing_hour])]})
    def update_weekday_fields(self):
        """Update all checked weekdays' QLineEdit fields based on the first non-empty value found."""
        print("checkbox connected")

        first_value_1 = None
        first_value_2 = None
        # Find the first non-empty _1 and _2 values
        for day in self.weekdays:
            if self.checkboxes.get(day, None) and self.checkboxes[day].isChecked():
                if first_value_1 is None and day in self.opening_lineEdits:
                    first_value_1 = self.opening_lineEdits[day].text()
                if first_value_2 is None and day in self.closing_lineEdits:
                    first_value_2 = self.closing_lineEdits[day].text()

        # Apply found values to all checked checkboxes' QLineEdit fields
        if self.parent.all_days_checkBox.isChecked():
            for day in self.weekdays:
                if self.checkboxes.get(day, None) and self.checkboxes[day].isChecked():
                    if first_value_1 is not None and day in self.opening_lineEdits:
                        self.opening_lineEdits[day].setText(first_value_1)
                        print(self.opening_lineEdits[day].objectName(),first_value_1)
                    if first_value_2 is not None and day in self.closing_lineEdits:
                        self.closing_lineEdits[day].setText(first_value_2)
                        print(self.closing_lineEdits[day].objectName(),first_value_2)

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
            # Đảm bảo restaurant_photo_label đã được khởi tạo đúng
            if hasattr(self.parent, 'restaurant_photo_label'):
                # Create rounded version of the images - use different sizes
                rounded_pixmap_small = self.get_rounded_pixmap(pixmap, 75)  # Smaller for avatar
                rounded_pixmap_large = self.get_rounded_pixmap(pixmap, 200)  # Larger for main photo
                
                # Set the rounded images to the labels
                self.parent.restaurant_photo_label.setPixmap(rounded_pixmap_large)
                self.parent.restaurant_photo_label.setScaledContents(True)
                self.parent.restaurant_photo_label.setStyleSheet("background-color: transparent; border: none;")

                self.parent.restaurant_info_avatar.setPixmap(rounded_pixmap_small)
                self.parent.restaurant_info_avatar.setScaledContents(True)
                self.parent.restaurant_info_avatar.setStyleSheet("background-color: transparent; border: none;")
                
                # If these are ClickableLabel objects, make sure we don't overwrite their click behavior
                if isinstance(self.parent.restaurant_photo_label, ClickableLabel):
                    self.parent.restaurant_photo_label.setText("")  # Clear any text
                
                if isinstance(self.parent.restaurant_info_avatar, ClickableLabel):
                    self.parent.restaurant_info_avatar.setText("")  # Clear any text
            else:
                print("restaurant_photo_label not found in parent widget")
        else:
            if hasattr(self.parent, 'restaurant_photo_label'):
                if isinstance(self.parent.restaurant_photo_label, ClickableLabel):
                    self.parent.restaurant_photo_label.setText("Click to upload image")
                else:
                    self.parent.restaurant_photo_label.setText("Failed to load image")
            else:
                print("restaurant_photo_label not found in parent widget")
    
    def get_rounded_pixmap(self, pixmap, size):
        """Chuyển đổi QPixmap thành hình tròn hoàn hảo, không bị cắt méo."""
        # Scale image, keeping aspect ratio, expanding to fill
        scaled_pixmap = pixmap.scaled(
            size, size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        
        # Crop to square (center the crop)
        width = scaled_pixmap.width()
        height = scaled_pixmap.height()
        x = (width - size) // 2
        y = (height - size) // 2
        cropped_pixmap = scaled_pixmap.copy(x, y, size, size)
        
        # Create circular pixmap
        rounded_pixmap = QPixmap(size, size)
        rounded_pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addEllipse(QRectF(0, 0, size, size))
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, cropped_pixmap)
        painter.end()
        
        return rounded_pixmap

    def setup_ui_create(self):
        self.processSignalsAndSlotsOnCreate()


        # Replace restaurant_info_avatar with ClickableLabel
        if hasattr(self.parent, 'form_photo'):
            # Store reference to the original label's parent and position
            original_avatar = self.parent.form_photo
            print(original_avatar)
            avatar_parent = original_avatar.parent()
            print(avatar_parent)
            avatar_layout = avatar_parent.layout()
            print(avatar_layout)
            avatar_position = avatar_layout.indexOf(original_avatar)
            avatar_size = original_avatar.size()

            # Remove the original label
            avatar_layout.removeWidget(original_avatar)
            original_avatar.deleteLater()

            # Create new ClickableLabel
            new_photo=ClickableLabel(avatar_parent)
            self.parent.form_photo = new_photo
            self.parent.form_photo.setFixedSize(60,60)
            self.parent.form_photo.setText("Click to upload")
            self.parent.form_photo.setWordWrap(True)
            self.parent.form_photo.setFixedSize(avatar_size)
            self.parent.form_photo.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Add to layout at same position - use addWidget which works with all layouts
            avatar_layout.addWidget(self.parent.form_photo)

            # Connect click signal to upload function
            self.parent.form_photo.clicked.connect(self.getPhotoFromFile)

        # Also make the main restaurant photo label clickable
        if hasattr(self.parent, 'restaurant_photo_label'):
            # Store reference to the original label's parent and position
            original_photo = self.parent.restaurant_photo_label
            photo_parent = original_photo.parent()
            photo_layout = photo_parent.layout()
            photo_position = photo_layout.indexOf(original_photo)
            photo_size = original_photo.size()

            # Remove the original label
            photo_layout.removeWidget(original_photo)
            original_photo.deleteLater()

            # Create new ClickableLabel
            self.parent.restaurant_photo_label = ClickableLabel(photo_parent)
            self.parent.restaurant_photo_label.setText("Click to upload")
            self.parent.restaurant_photo_label.setFixedSize(photo_size)
            self.parent.restaurant_photo_label.setStyleSheet("background-color: transparent; border: none;")
            self.parent.restaurant_photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Add to layout at same position - use addWidget which works with all layouts
            photo_layout.addWidget(self.parent.restaurant_photo_label)

            # Connect click signal to upload function
            self.parent.restaurant_photo_label.clicked.connect(self.getPhotoFromFile)

        self.restaurant_new_image_path = self.parent.form_photo.file_path  # Variable to store the image path

    def getPhotoFromFile(self):
        file_path = self.sender().open_file_dialog()
        # Get the file path after selection
        if file_path:
            self.restaurant_image_path = file_path

            # Load and display the image as circular
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                # Create rounded version for both avatar and main image
                rounded_pixmap_small = self.get_rounded_pixmap(pixmap, 75)  # Smaller for avatar
                rounded_pixmap_large = self.get_rounded_pixmap(pixmap, 200)  # Larger for main photo

                # Update avatar
                self.parent.restaurant_info_avatar.setPixmap(rounded_pixmap_small)
                self.parent.restaurant_info_avatar.setScaledContents(True)

                # Update main photo too if it exists
                if hasattr(self.parent, 'restaurant_photo_label'):
                    self.parent.form_photo.setPixmap(rounded_pixmap_large)
                    self.parent.form_photo.setScaledContents(True)

                print(f"Image uploaded successfully: {file_path}")

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
        # self.restaurant_data = self.parent.db_manager.get_restaurant_byid(self.current_restaurant_id)
        self.current_restaurant=Restaurant(_id=self.current_restaurant_id)
        self.restaurant_data=self.current_restaurant.to_dict()
        self.parent.restaurant_name_label.setText(self.restaurant_data["name"])
        self.parent.restaurant_name_label.setWordWrap(True)
        print(self.current_restaurant_id)
        # print(f"Restaurant data in modify restaurant screen: {self.restaurant_data}")
        if not self.restaurant_data:
            print("Không tìm thấy dữ liệu nhà hàng")
            return
        # self.parent.restaurant_info_avatar.setText(self.restaurant_data["name"])
        self.parent.restaurant_photo_label.setScaledContents(True)

        # Gọi hàm cập nhật ảnh với URL mong muốn
        self.update_restaurant_photo(self.restaurant_data["featured_image"])

        # Replace restaurant_form_photo_label with ClickableLabel
        self.parent.restaurant_form_photo_label = ClickableLabel()
        self.parent.restaurant_form_photo_label.setText("Restaurant")
        self.parent.restaurant_form_photo_label.setStyleSheet("border: 1px solid gray; padding: 5px;")
        self.parent.restaurant_form_photo_label.setFixedSize(200, 200)  # Adjust size as needed

        # Replace restaurant_info_avatar with ClickableLabel
        if hasattr(self.parent, 'restaurant_info_avatar'):
            # Store reference to the original label's parent and position
            original_avatar = self.parent.restaurant_info_avatar
            avatar_parent = original_avatar.parent()
            avatar_layout = avatar_parent.layout()
            avatar_position = avatar_layout.indexOf(original_avatar)
            avatar_size = original_avatar.size()

            # Remove the original label
            avatar_layout.removeWidget(original_avatar)
            original_avatar.deleteLater()

            # Create new ClickableLabel
            self.parent.restaurant_info_avatar = ClickableLabel(avatar_parent)
            self.parent.restaurant_info_avatar.setText("Click to upload")
            self.parent.restaurant_info_avatar.setFixedSize(avatar_size)
            self.parent.restaurant_info_avatar.setStyleSheet("background-color: transparent; border: none;")
            self.parent.restaurant_info_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Add to layout at same position - use addWidget which works with all layouts
            avatar_layout.addWidget(self.parent.restaurant_info_avatar)

            # Connect click signal to upload function
            self.parent.restaurant_info_avatar.clicked.connect(self.upload_avatar_image)

        # Also make the main restaurant photo label clickable
        if hasattr(self.parent, 'restaurant_photo_label'):
            # Store reference to the original label's parent and position
            original_photo = self.parent.restaurant_photo_label
            photo_parent = original_photo.parent()
            photo_layout = photo_parent.layout()
            photo_position = photo_layout.indexOf(original_photo)
            photo_size = original_photo.size()

            # Remove the original label
            photo_layout.removeWidget(original_photo)
            original_photo.deleteLater()

            # Create new ClickableLabel
            self.parent.restaurant_photo_label = ClickableLabel(photo_parent)
            self.parent.restaurant_photo_label.setText("Click to upload")
            self.parent.restaurant_photo_label.setFixedSize(photo_size)
            self.parent.restaurant_photo_label.setStyleSheet("background-color: transparent; border: none;")
            self.parent.restaurant_photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Add to layout at same position - use addWidget which works with all layouts
            photo_layout.addWidget(self.parent.restaurant_photo_label)

            # Connect click signal to upload function
            self.parent.restaurant_photo_label.clicked.connect(self.upload_photo_image)

        self.restaurant_new_image_path = self.parent.restaurant_form_photo_label.file_path  # Variable to store the image path

        try:
            self.parent.modifyrestaurant_name_lineEdit.setText(self.restaurant_data["name"])

            self.parent.modifyrestaurant_category_lineEdit.setText(", ".join(self.restaurant_data["categories"]))

            address = self.restaurant_data["detailed_address"]
            # address_str = f"{address['street']}, {address['ward']}, {address['city']}, {address['state']}"
            self.parent.modifyrestaurant_country_lineEdit.setText("Viet Nam")
            self.parent.modifyrestaurant_city_lineEdit.setText(self.restaurant_data["detailed_address"]["city"])
            self.parent.modifyrestaurant_area_lineEdit.setText(self.restaurant_data["detailed_address"]["state"])
            self.parent.modifyrestaurant_detailedaddress_lineEdit.setText(self.restaurant_data["address"])
            self.parent.modifyrestaurant_website_lineEdit.setText(self.restaurant_data["website"])
            self.parent.modifyrestaurant_phone_lineEdit.setText(self.restaurant_data["phone"])
            for info in self.restaurant_data["about"]:
                if info["id"] == "service_options":
                    for option in info["options"]:
                        if option["name"].lower() == "delivery":
                            self.parent.modifyrestaurant_delivery_checkBox.setChecked(option["enabled"])
                        elif option["name"].lower() == "dine-in":
                            self.parent.modifyrestaurant_dinein_checkBox.setChecked(option["enabled"])
                        elif option["name"].lower() == "takeaway":
                            self.parent.modifyrestaurant_takeaway_checkBox.setChecked(option["enabled"])
                elif info["id"] == "payments":
                    self.parent.modifyrestaurant_payments_checkBox.setChecked(option["enabled"])
                    for option in info["options"]:
                        payment_note = "; ".join([option["name"] for option in info["options"]])
                        print(payment_note)
                        self.parent.modifyrestaurant_payments_lineEdit.setText(payment_note)
                elif info["id"]=="parking" and len(info["options"])>0:
                    self.parent.modifyrestaurant_parking_checkBox.setChecked(True)
                    parking_note = "; ".join([option["name"] for option in info["options"]])
                    print(parking_note)
                    self.parent.modifyrestaurant_parking_lineEdit.setText(parking_note)
                # elif info["id"]=="planning":
                #     for option in info["options"]:
                #         if len(self.restaurant_data["reservations"])>0:
                #             self.parent.modifyrestaurant_reservations_checkBox.setChecked(True)
                #             reservations_note= [ "; ".join(reservation.values()) for reservation in self.restaurant_data["reservations"] ]
                #             self.parent.modifyrestaurant_reservations_lineEdit.setText("; ".join(self.restaurant_data["reservations"]))
            isSameHours=True
            time = ""
            hours=[]
            for day in self.restaurant_data["hours"]:
                for times in day["times"]:
                    opening = "; ".join(times)
                    if time=="":
                        time = opening
                    else:
                        if time!= opening:
                            isSameHours=False
                    hours.append(opening)
            #TODO: finish filling in the UI opening hours, preferably using the same for loops
        except Exception as e:
            print(f"error: {e}")
        self.parent.restaurantinfo_update_button.clicked.connect(self.update_restaurant)
        self.parent.restaurantinfo_delete_button.clicked.connect(self.delete_restaurant)

    def delete_restaurant(self):
        print("clicked delete res button")
        confirmation = QMessageBox.warning(self.parent.modify_restaurant_widget, f"Delete Restaurant {self.restaurant_data['name']}", "Are you sure you want to delete this restaurant?")
        if confirmation:
            try:
                res=self.parent.db_manager.delete_restaurant_by_id(self.restaurant_data['_id'])
                if res:
                    QMessageBox.information(self.parent.modify_restaurant_widget, "Success", "Restaurant deleted successfully")
                    self.parent.goRestaurant()
                else:
                    QMessageBox.critical(self.parent.modify_restaurant_widget, "Unknown Error", "Failed to delete restaurant")
            except Exception as e:
                QMessageBox.critical(self.parent.modify_restaurant_widget, "Error", f"Failed to delete restaurant: {e}")
    def update_restaurant(self):
        print("clicked update res button")
        self.form_res_name = self.parent.modifyrestaurant_name_lineEdit.text()
        print(self.form_res_name)
        # self.form_description = self.parent.modifyrestaurant_description_lineEdit.text()
        self.form_category = self.parent.modifyrestaurant_category_lineEdit.text()
        print(self.form_category)
        self.form_country = self.parent.modifyrestaurant_country_lineEdit.text()
        self.form_city  = self.parent.modifyrestaurant_city_lineEdit.text()
        print(self.form_city)

        self.form_area = self.parent.modifyrestaurant_area_lineEdit.text()
        self.form_address = self.parent.modifyrestaurant_detailedaddress_lineEdit.text()
        self.form_phone = self.parent.modifyrestaurant_phone_lineEdit.text()
        self.form_mail=self.parent.modifyrestaurant_email_lineEdit.text()
        self.form_website = self.parent.modifyrestaurant_website_lineEdit.text()
        if self.parent.all_days_checkBox.isChecked():
            self.update_weekday_fields()
        self.get_timings()

        self.new_restaurant = Restaurant(name=self.form_res_name,
                                         main_category=self.form_category, city=self.form_city,
                                         detailed_address={'ward':self.form_area, 'country':self.form_country},
                                         featured_image = self.restaurant_image_path,
                                         address=self.form_address,hours=self.hours,
                                         phone=self.form_phone, email=self.form_mail, website=self.form_website)
        try:
            self.current_restaurant.compare_and_update(self.new_restaurant)
            print("Updated restaurant with the following data", self.current_restaurant.to_dict())
            self.current_restaurant.update_restaurant_by_id()
        except  Exception as e:
            QMessageBox.critical(self.parent.body_stackedWidget, "Error", f"Failed to update restaurant due to {e}")

    def add_restaurant(self):
        print("clicked create res button")
        self.form_res_name = self.parent.form_res_name.text()
        self.form_category = self.parent.form_category.text()
        self.form_country = self.parent.form_country.text()
        self.form_city  = self.parent.form_city.text()

        self.form_area = self.parent.form_country.text()
        self.form_address = self.parent.form_address.text()
        self.form_phone = self.parent.form_phone.text()
        self.form_mail=self.parent.form_mail.text()
        self.form_website = self.parent.form_website.text()
        if self.parent.all_days_checkBox.isChecked():
            self.update_weekday_fields()
        self.get_timings()
        try:
            self.new_restaurant = Restaurant(name=self.form_res_name,main_category=self.form_category, city=self.form_city,
                                         detailed_address={'ward':self.form_area, 'country':self.form_country},
                                         featured_image = self.restaurant_image_path,
                                         address=self.form_address,hours=self.hours,
                                         phone=self.form_phone, email=self.form_mail, website=self.form_website)
            print(self.new_restaurant.to_dict())

            # self.parent.db_manager.add_restaurant_to_db(self.new_restaurant.to_dict())
            success, message = self.new_restaurant.add_restaurant()
            if success:
                QMessageBox.information(self, "Success", message)
            else:
                QMessageBox.critical(self, "Error", message)
            # self.parent.db_manager.close_connection()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot add restaurant due to {e}")
            print(f"Cannot add restaurant due to {e}")


    def processSignalsSlots(self):
        #TODO refactor - totally remove - the logic should belong to ext_interface
        #TODO not signal and slot but when click create button in restaurant screen the current restaurant should be None
        self.parent.restaurant_info_button.clicked.connect(self.goInfo)
        self.parent.restaurant_menu_button.clicked.connect(self.goMenu)
        self.parent.restaurant_review_button.clicked.connect(self.goReview)
        
        # # Connect save button if it exists
        # if hasattr(self.parent, 'modifyrestaurant_save_button'):
        #     self.parent.modifyrestaurant_save_button.clicked.connect(self.save_restaurant_changes)

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
        
        # Add the uploaded image path to the restaurant data if available
        if self.restaurant_image_path:
            # For a real application, you would typically:
            # 1. Copy the image to a server or upload it
            # 2. Get a URL or path to the uploaded file
            # 3. Store that URL in the database
            
            # For this example, we'll just store the local path
            restaurant_data["featured_image"] = self.restaurant_image_path
            print(f"Updating restaurant with new image: {self.restaurant_image_path}")
        
        if self.mode == "create":
            success, message = self.restaurant_model.add_restaurant(restaurant_data)
        else:
            success, message = self.restaurant_model.update_restaurant_by_id(self.current_restaurant_id, restaurant_data)

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
            "opening_hours": self.hours,
            "services": self.get_services(),
            "social_media": self.get_social_links()
        }
        return data

    #
    def get_services_input(self):
        services = {
            "parking": self.parking_checkbox.isChecked(),
            # "reservations": self.reservations_checkbox.isChecked(),
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

    def goInfo(self):
        self.parent.restaurant_stackedWidget.setCurrentWidget(self.parent.modify_restaurant_page)
    def goMenu(self):
        self.parent.restaurant_stackedWidget.setCurrentWidget(self.parent.menu_page)
    def goReview(self):
        self.parent.restaurant_stackedWidget.setCurrentWidget(self.parent.review_restaurant_page)

    def upload_avatar_image(self):
        """Handle click event on avatar to upload a new image"""
        self.parent.restaurant_info_avatar.open_file_dialog()
        
        # Get the file path after selection
        file_path = self.parent.restaurant_info_avatar.file_path
        if file_path:
            self.restaurant_image_path = file_path
            
            # Load and display the image as circular
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                # Create rounded version for both avatar and main image
                rounded_pixmap_small = self.get_rounded_pixmap(pixmap, 75)  # Smaller for avatar
                rounded_pixmap_large = self.get_rounded_pixmap(pixmap, 200)  # Larger for main photo
                
                # Update avatar
                self.parent.restaurant_info_avatar.setPixmap(rounded_pixmap_small)
                self.parent.restaurant_info_avatar.setScaledContents(True)
                
                # Update main photo too if it exists
                if hasattr(self.parent, 'restaurant_photo_label'):
                    self.parent.restaurant_photo_label.setPixmap(rounded_pixmap_large)
                    self.parent.restaurant_photo_label.setScaledContents(True)
                
                print(f"Image uploaded successfully: {file_path}")
                
                # TODO: Add code to save this image to database when saving restaurant

    def upload_photo_image(self):
        """Handle click event on main photo to upload a new image"""
        self.parent.restaurant_photo_label.open_file_dialog()
        
        # Get the file path after selection
        file_path = self.parent.restaurant_photo_label.file_path
        if file_path:
            self.restaurant_image_path = file_path
            
            # Load and display the image as circular
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                # Create rounded version for both avatar and main image
                rounded_pixmap_small = self.get_rounded_pixmap(pixmap, 75)  # Smaller for avatar
                rounded_pixmap_large = self.get_rounded_pixmap(pixmap, 200)  # Larger for main photo
                
                # Update main photo
                self.parent.restaurant_photo_label.setPixmap(rounded_pixmap_large)
                self.parent.restaurant_photo_label.setScaledContents(True)
                
                # Update avatar too
                if hasattr(self.parent, 'restaurant_info_avatar'):
                    self.parent.restaurant_info_avatar.setPixmap(rounded_pixmap_small)
                    self.parent.restaurant_info_avatar.setScaledContents(True)
                
                print(f"Image uploaded successfully: {file_path}")

    # def save_restaurant_changes(self):
    #     """Save changes to the restaurant, including the new image if uploaded"""
    #     if not self.current_restaurant_id:
    #         print("No restaurant ID to update")
    #         return
    #
    #     # Collect data from the form
    #     updated_data = {}
    #     updated_data["name"] = self.parent.modifyrestaurant_name_lineEdit.text().strip()
    #     updated_data["category"] = [cat.strip() for cat in self.parent.modifyrestaurant_category_lineEdit.text().split(",")]
    #
    #     # Address data
    #     updated_data["address"] = {
    #         "city": self.parent.modifyrestaurant_city_lineEdit.text().strip(),
    #         "state": self.parent.modifyrestaurant_area_lineEdit.text().strip(),
    #         "country": self.parent.modifyrestaurant_country_lineEdit.text().strip()
    #     }
    #
    #     # Contact info
    #     updated_data["phone"] = self.parent.modifyrestaurant_phone_lineEdit.text().strip()
    #     updated_data["website"] = self.parent.modifyrestaurant_website_lineEdit.text().strip()
    #
    #     # Add the uploaded image if available
    #     if self.restaurant_image_path:
    #         # In a real application, you would:
    #         # 1. Upload the image to a server
    #         # 2. Get the URL of the uploaded image
    #         # 3. Store the URL in the database
    #
    #         # For this example, we'll just store the local path
    #         updated_data["featured_image"] = self.restaurant_image_path
    #         print(f"Updating restaurant with new image: {self.restaurant_image_path}")
    #
    #     try:
    #         # Update the restaurant in the database
    #         success = self.parent.db_manager.update_restaurant(self.current_restaurant_id, updated_data)
    #         if success:
    #             print("Restaurant updated successfully")
    #             # Optionally show a success message or navigate to another screen
    #         else:
    #             print("Failed to update restaurant")
    #     except Exception as e:
    #         print(f"Error updating restaurant: {e}")