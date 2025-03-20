# import requests
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QPixmap, QPainter, QBrush, QPainterPath
# from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QLabel
# from project.src.model.RestaurantModel import RestaurantModel
#
# class RestaurantDelegate(QTableWidget):
#     def __init__(self):
#         super().__init__()
#         self.model = RestaurantModel()  # Gọi model để lấy dữ liệu
#         self.setColumnCount(9)
#         self.setHorizontalHeaderLabels([
#             "_id", "", "Restaurant", "Rate", "Open - Close", "Category", "Address", "Hotline", "Accessibility"
#         ])
#         self.load_more_restaurants()
#
#     def load_more_restaurants(self):
#         """Nạp thêm dữ liệu vào bảng."""
#         restaurants = self.model.get_restaurants()
#         if not restaurants:
#             return
#
#         current_row_count = self.rowCount()
#         self.setRowCount(current_row_count + len(restaurants))
#         """
#         TODO:Bản - tìm cách để QTableWidgetItem hiển thị được các Widget hình ảnh, label thay
#         vì chỉ có text
#         """
#         for i, restaurant in enumerate(restaurants):
#             row = current_row_count + i
#             self.setItem(row, 0, QTableWidgetItem(str(restaurant["_id"])))  # Cột ẩn
#             self.setItem(row,1, QTableWidgetItem(str(restaurant["featured_image"]))) #đang hiển thị link chưa hiển thị hình ảnh
#             self.setItem(row, 2, QTableWidgetItem(restaurant["name"]))
#             self.setItem(row, 3, QTableWidgetItem(f"{restaurant['rating']} ⭐"))
#             self.setItem(row, 4, QTableWidgetItem(restaurant["open_hours"]))
#             self.setItem(row, 5, QTableWidgetItem(restaurant["category"]))
#             self.setItem(row, 6, QTableWidgetItem(restaurant["address"]))
#             self.setItem(row, 7, QTableWidgetItem(restaurant["hotline"]))
#             self.setItem(row, 8, QTableWidgetItem(str(restaurant["accessibility"])))
#
#             self.model.offset += len(restaurants)  # Cập nhật offset
#
#     def create_image_widget(self, image_url):
#         """Tạo widget chứa ảnh từ URL."""
#         label = QLabel()
#         pixmap = self.get_pixmap_from_url(image_url)
#         if pixmap:
#             label.setPixmap(pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio))
#         return label
#
#     def get_pixmap_from_url(self, url):
#         """Tải ảnh từ URL và chuyển thành QPixmap."""
#         try:
#             response = requests.get(url, timeout=5)
#             response.raise_for_status()
#             pixmap = QPixmap()
#             pixmap.loadFromData(response.content)
#             return pixmap
#         except requests.RequestException as e:
#             print(f"Lỗi tải ảnh: {e}")
#             return None
#

""" Version 3"""

# import requests
# from io import BytesIO
# from PyQt6.QtCore import Qt, QRectF
# from PyQt6.QtGui import QPixmap, QPainter, QPainterPath
# from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QLabel
# from project.src.model.RestaurantModel import RestaurantModel
#
#
# class RestaurantDelegate(QTableWidget):
#     IMAGE_SIZE = 50  # Kích thước ảnh vuông
#
#     def __init__(self):
#         super().__init__()
#         self.model = RestaurantModel()
#         self.setColumnCount(9)
#         self.setHorizontalHeaderLabels([
#             "_id", "", "Restaurant", "Rate", "Open - Close", "Category", "Address", "Hotline", "Accessibility"
#         ])
#         self.load_more_restaurants()
#
#     def load_more_restaurants(self):
#         """Nạp thêm dữ liệu vào bảng."""
#         restaurants = self.model.get_restaurants()
#         if not restaurants:
#             return
#
#         current_row_count = self.rowCount()
#         self.setRowCount(current_row_count + len(restaurants))
#
#         for i, restaurant in enumerate(restaurants):
#             row = current_row_count + i
#             self.setItem(row, 0, QTableWidgetItem(str(restaurant["_id"])))  # Cột ẩn
#             self.setCellWidget(row, 1, self.create_image_label(restaurant["featured_image"]))  # Hiển thị ảnh tròn
#             self.setItem(row, 2, QTableWidgetItem(restaurant["name"]))
#             self.setItem(row, 3, QTableWidgetItem(f"{restaurant['rating']} ⭐"))
#             self.setItem(row, 4, QTableWidgetItem(restaurant["open_hours"]))
#             self.setItem(row, 5, QTableWidgetItem(restaurant["category"]))
#             self.setItem(row, 6, QTableWidgetItem(restaurant["address"]))
#             self.setItem(row, 7, QTableWidgetItem(restaurant["hotline"]))
#             self.setItem(row, 8, QTableWidgetItem(str(restaurant["accessibility"])))
#
#             self.model.offset += len(restaurants)  # Cập nhật offset
#
#     def create_image_label(self, image_url):
#         """Tạo QLabel chứa hình ảnh dạng tròn từ URL."""
#         label = QLabel()
#         label.setFixedSize(self.IMAGE_SIZE, self.IMAGE_SIZE)  # Đặt kích thước cố định
#
#         # Tải ảnh từ URL
#         try:
#             response = requests.get(image_url, timeout=5)
#             if response.status_code == 200:
#                 image_data = BytesIO(response.content)
#                 pixmap = QPixmap()
#                 pixmap.loadFromData(image_data.read())
#                 rounded_pixmap = self.get_rounded_pixmap(pixmap)  # Chuyển thành hình tròn
#                 label.setPixmap(rounded_pixmap)
#         except requests.exceptions.RequestException:
#             label.setText("Image Load Error")  # Hiển thị lỗi nếu ảnh không tải được
#
#         return label
#
#     def get_rounded_pixmap(self, pixmap):
#         """Chuyển đổi QPixmap thành hình tròn."""
#         size = min(pixmap.width(), pixmap.height())  # Đảm bảo kích thước vuông
#         pixmap = pixmap.scaled(self.IMAGE_SIZE, self.IMAGE_SIZE, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
#
#         rounded_pixmap = QPixmap(self.IMAGE_SIZE, self.IMAGE_SIZE)
#         rounded_pixmap.fill(Qt.GlobalColor.transparent)
#
#         painter = QPainter(rounded_pixmap)
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#         path = QPainterPath()
#         path.addEllipse(QRectF(0, 0, self.IMAGE_SIZE, self.IMAGE_SIZE))
#         painter.setClipPath(path)
#         painter.drawPixmap(0, 0, pixmap)
#         painter.end()
#
#         return rounded_pixmap

""" Version 5"""

# import requests
# from io import BytesIO
# from PyQt6.QtCore import Qt, QRectF
# from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QColor
# from PyQt6.QtWidgets import (
#     QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QWidget, QHBoxLayout
# )
# from project.src.model.RestaurantModel import RestaurantModel
#
# class RestaurantDelegate(QTableWidget):
#     IMAGE_SIZE = 80  # Kích thước hình ảnh
#     ROW_HEIGHT = 130  # Độ cao của hàng
#
#     def __init__(self):
#         super().__init__()
#         self.model = RestaurantModel()
#         self.setColumnCount(9)
#         self.setHorizontalHeaderLabels([
#             "_id", "", "Restaurant", "Rate", "Open - Close", "Category", "Address", "Hotline", "Accessibility"
#         ])
#
#         self.load_more_restaurants()
#         self.format_table()
#         self.style_table()
#
#     def load_more_restaurants(self):
#         """Nạp thêm dữ liệu vào bảng."""
#         restaurants = self.model.get_restaurants()
#         if not restaurants:
#             return
#
#         current_row_count = self.rowCount()
#         self.setRowCount(current_row_count + len(restaurants))
#
#         for i, restaurant in enumerate(restaurants):
#             row = current_row_count + i
#             self.setItem(row, 0, QTableWidgetItem(str(restaurant["_id"])))  # Cột ID (ẩn đi)
#             self.setCellWidget(row, 1, self.create_image_widget(restaurant["featured_image"]))  # Ảnh tròn căn giữa
#             self.setItem(row, 2, QTableWidgetItem(restaurant["name"]))
#             self.setCellWidget(row, 3, self.create_star_widget(restaurant["rating"]))  # Hiển thị rating dạng sao
#             self.setItem(row, 4, self.create_multiline_text(restaurant["open_hours"]))  # Xuống dòng Open - Close
#             self.setItem(row, 5, QTableWidgetItem(restaurant["category"]))
#             self.setItem(row, 6, QTableWidgetItem(restaurant["address"]))
#             self.setItem(row, 7, QTableWidgetItem(restaurant["hotline"]))
#             self.setItem(row, 8, QTableWidgetItem(str(restaurant["accessibility"])))
#
#             # Tăng độ cao hàng
#             self.setRowHeight(row, self.ROW_HEIGHT)
#
#         self.model.offset += len(restaurants)  # Cập nhật offset
#
#     def create_image_widget(self, image_url):
#         """Tạo Widget chứa hình ảnh tròn và căn giữa."""
#         container = QWidget()
#         layout = QHBoxLayout()
#         layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Căn giữa hình ảnh
#         label = QLabel()
#         label.setFixedSize(self.IMAGE_SIZE, self.IMAGE_SIZE)
#
#         # Tải ảnh từ URL
#         try:
#             response = requests.get(image_url, timeout=5)
#             if response.status_code == 200:
#                 image_data = BytesIO(response.content)
#                 pixmap = QPixmap()
#                 pixmap.loadFromData(image_data.read())
#                 rounded_pixmap = self.get_rounded_pixmap(pixmap)  # Chuyển thành ảnh tròn
#                 label.setPixmap(rounded_pixmap)
#         except requests.exceptions.RequestException:
#             label.setText("Image Load Error")  # Hiển thị lỗi nếu ảnh không tải được
#
#         layout.addWidget(label)
#         container.setLayout(layout)
#         return container
#
#     def get_rounded_pixmap(self, pixmap):
#         """Chuyển đổi QPixmap thành hình tròn."""
#         pixmap = pixmap.scaled(self.IMAGE_SIZE, self.IMAGE_SIZE, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
#
#         rounded_pixmap = QPixmap(self.IMAGE_SIZE, self.IMAGE_SIZE)
#         rounded_pixmap.fill(Qt.GlobalColor.transparent)
#
#         painter = QPainter(rounded_pixmap)
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#         path = QPainterPath()
#         path.addEllipse(QRectF(0, 0, self.IMAGE_SIZE, self.IMAGE_SIZE))
#         painter.setClipPath(path)
#         painter.drawPixmap(0, 0, pixmap)
#         painter.end()
#
#         return rounded_pixmap
#
#     def create_multiline_text(self, text):
#         """Tạo text xuống dòng (mỗi thứ trên 1 dòng)."""
#         return QTableWidgetItem("\n".join(text.split("|")))
#
#     def create_star_widget(self, rating):
#         """Tạo Widget hiển thị số sao theo rating."""
#         full_stars = int(rating)
#         half_star = (rating - full_stars) >= 0.5
#         empty_stars = 5 - full_stars - (1 if half_star else 0)
#
#         star_text = "⭐" * full_stars  # Sao vàng
#         if half_star:
#             star_text += "⭐½"  # Sao nửa vàng nửa xám
#         star_text += "✩" * empty_stars  # Sao xám
#
#         label = QLabel(star_text)
#         label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Căn giữa sao
#         return label
#
#     def format_table(self):
#         """Cấu hình bảng: Ẩn cột ID, điều chỉnh độ rộng cột."""
#         self.setColumnHidden(0, True)  # Ẩn cột ID
#
#         # Đặt độ rộng cho từng cột
#         self.setColumnWidth(1, 100)  # Ảnh
#         self.setColumnWidth(2, 150)  # Restaurant name
#         self.setColumnWidth(3, 100)  # Rate
#         self.setColumnWidth(4, 200)  # Open - Close (cố định)
#         self.setColumnWidth(5, 120)  # Category
#         self.setColumnWidth(6, 250)  # Address (cố định)
#         self.setColumnWidth(7, 120)  # Hotline
#         self.setColumnWidth(8, 100)  # Accessibility
#
#         # Các cột khác sẽ tự động giãn theo nội dung
#         self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
#         self.horizontalHeader().setStretchLastSection(True)  # Cột cuối sẽ kéo dãn
#
#     def style_table(self):
#         """Tạo màu header bảng thành màu cam FF862F."""
#         self.setStyleSheet("""
#             QHeaderView::section {
#                 background-color: #FF862F;
#                 color: white;
#                 font-weight: bold;
#                 padding: 8px;
#                 border: 1px solid #d67a2c;
#             }
#         """)
""" Version 6"""

# import requests
# from io import BytesIO
# from PyQt6.QtCore import Qt, QRectF
# from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QColor
# from PyQt6.QtWidgets import (
#     QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QWidget, QHBoxLayout
# )
# from project.src.model.RestaurantModel import RestaurantModel
#
# class RestaurantDelegate(QTableWidget):
#     IMAGE_SIZE = 80  # Kích thước hình ảnh
#     ROW_HEIGHT = 130  # Độ cao của hàng
#
#     def __init__(self):
#         super().__init__()
#         self.model = RestaurantModel()
#         self.setColumnCount(9)
#         self.setHorizontalHeaderLabels([
#             "_id", "", "Restaurant", "Rate", "Open - Close", "Category", "Address", "Hotline", "Accessibility"
#         ])
#
#         self.load_more_restaurants()
#         self.format_table()
#         self.style_table()
#
#     def load_more_restaurants(self):
#         """Nạp thêm dữ liệu vào bảng."""
#         restaurants = self.model.get_restaurants()
#         if not restaurants:
#             return
#
#         current_row_count = self.rowCount()
#         self.setRowCount(current_row_count + len(restaurants))
#
#         for i, restaurant in enumerate(restaurants):
#             row = current_row_count + i
#             self.setItem(row, 0, QTableWidgetItem(str(restaurant["_id"])))  # Cột ID (ẩn đi)
#             self.setCellWidget(row, 1, self.create_image_widget(restaurant["featured_image"]))  # Ảnh tròn căn giữa
#             self.setItem(row, 2, QTableWidgetItem(restaurant["name"]))
#             self.setCellWidget(row, 3, self.create_star_widget(restaurant["rating"]))  # Hiển thị rating dạng sao
#             self.setItem(row, 4, self.create_multiline_text(restaurant["open_hours"]))  # Xuống dòng Open - Close
#
#             # Căn giữa nội dung cột "Category" và "Hotline"
#             category_item = QTableWidgetItem(restaurant["category"])
#             category_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
#             self.setItem(row, 5, category_item)
#
#             self.setItem(row, 6, QTableWidgetItem(restaurant["address"]))
#
#             hotline_item = QTableWidgetItem(restaurant["hotline"])
#             hotline_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
#             self.setItem(row, 7, hotline_item)
#
#             self.setItem(row, 8, QTableWidgetItem(str(restaurant["accessibility"])))
#
#             # Tăng độ cao hàng
#             self.setRowHeight(row, self.ROW_HEIGHT)
#
#         self.model.offset += len(restaurants)  # Cập nhật offset
#
#     def create_image_widget(self, image_url):
#         """Tạo Widget chứa hình ảnh tròn và căn giữa."""
#         container = QWidget()
#         layout = QHBoxLayout()
#         layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Căn giữa hình ảnh
#         label = QLabel()
#         label.setFixedSize(self.IMAGE_SIZE, self.IMAGE_SIZE)
#
#         # Tải ảnh từ URL
#         try:
#             response = requests.get(image_url, timeout=5)
#             if response.status_code == 200:
#                 image_data = BytesIO(response.content)
#                 pixmap = QPixmap()
#                 pixmap.loadFromData(image_data.read())
#                 rounded_pixmap = self.get_rounded_pixmap(pixmap)  # Chuyển thành ảnh tròn
#                 label.setPixmap(rounded_pixmap)
#         except requests.exceptions.RequestException:
#             label.setText("Image Load Error")  # Hiển thị lỗi nếu ảnh không tải được
#
#         layout.addWidget(label)
#         container.setLayout(layout)
#         return container
#
#     def get_rounded_pixmap(self, pixmap):
#         """Chuyển đổi QPixmap thành hình tròn hoàn hảo, không bị cắt méo."""
#         pixmap = pixmap.scaled(self.IMAGE_SIZE, self.IMAGE_SIZE, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
#
#         rounded_pixmap = QPixmap(self.IMAGE_SIZE, self.IMAGE_SIZE)
#         rounded_pixmap.fill(Qt.GlobalColor.transparent)
#
#         painter = QPainter(rounded_pixmap)
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#         path = QPainterPath()
#         path.addEllipse(QRectF(0, 0, self.IMAGE_SIZE, self.IMAGE_SIZE))
#         painter.setClipPath(path)
#         painter.drawPixmap(0, 0, pixmap)
#         painter.end()
#
#         return rounded_pixmap
#
#     def create_multiline_text(self, text):
#         """Tạo text xuống dòng (mỗi thứ trên 1 dòng) và loại bỏ khoảng trắng thừa."""
#         lines = [line.strip() for line in text.split("|")]  # Xóa khoảng trắng đầu & cuối
#         return QTableWidgetItem("\n".join(lines))
#
#     def create_star_widget(self, rating):
#         """Tạo Widget hiển thị số sao theo rating + số điểm."""
#         full_stars = int(rating)  # Chỉ lấy phần nguyên của số sao
#
#         star_text = "⭐" * full_stars  # Sao vàng
#         text = f"{rating} \n {star_text}"  # Thêm số điểm trước sao
#
#         label = QLabel(text)
#         label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Căn giữa sao + số điểm
#         return label
#
#     def format_table(self):
#         """Cấu hình bảng: Ẩn cột ID, điều chỉnh độ rộng cột."""
#         self.setColumnHidden(0, True)  # Ẩn cột ID
#
#         # Đặt độ rộng cho từng cột
#         self.setColumnWidth(1, 100)  # Ảnh
#         self.setColumnWidth(2, 150)  # Restaurant name
#         self.setColumnWidth(3, 120)  # Rate
#         self.setColumnWidth(4, 200)  # Open - Close (cố định)
#         self.setColumnWidth(5, 120)  # Category (căn giữa)
#         self.setColumnWidth(6, 250)  # Address (cố định)
#         self.setColumnWidth(7, 120)  # Hotline (căn giữa)
#         self.setColumnWidth(8, 100)  # Accessibility
#
#         # Các cột khác sẽ tự động giãn theo nội dung
#         self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
#         self.horizontalHeader().setStretchLastSection(True)  # Cột cuối sẽ kéo dãn
#
#     def style_table(self):
#         """Tạo màu header bảng thành màu cam FF862F."""
#         self.setStyleSheet("""
#             QHeaderView::section {
#                 background-color: #FF862F;
#                 color: white;
#                 font-weight: bold;
#                 padding: 8px;
#                 border: 1px solid #d67a2c;
#             }
#         """)

""" Version 7"""
import requests
from io import BytesIO
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QColor
from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QWidget, QHBoxLayout, QVBoxLayout
)
from project.src.model.RestaurantModel import RestaurantModel

class RestaurantDelegate(QTableWidget):
    IMAGE_SIZE = 80  # Kích thước hình ảnh
    ROW_HEIGHT = 130  # Độ cao của hàng

    def __init__(self):
        super().__init__()
        self.model = RestaurantModel()
        self.setColumnCount(9)
        self.setHorizontalHeaderLabels([
            "_id", "", "Restaurant", "Rate", "Open - Close", "Category", "Address", "Hotline", "Accessibility"
        ])

        self.load_more_restaurants()
        self.format_table()
        self.style_table()

    def load_more_restaurants(self):
        """Nạp thêm dữ liệu vào bảng."""
        restaurants = self.model.get_restaurants()
        if not restaurants:
            return

        current_row_count = self.rowCount()
        self.setRowCount(current_row_count + len(restaurants))

        for i, restaurant in enumerate(restaurants):
            row = current_row_count + i
            self.setItem(row, 0, QTableWidgetItem(str(restaurant["_id"])))  # Cột ID (ẩn đi)
            self.setCellWidget(row, 1, self.create_image_widget(restaurant["featured_image"]))  # Ảnh tròn căn giữa
            self.setItem(row, 2, QTableWidgetItem(restaurant["name"]))
            self.setCellWidget(row, 3, self.create_star_widget(restaurant["rating"]))  # Hiển thị rating dạng sao
            self.setItem(row, 4, self.create_multiline_text(restaurant["open_hours"]))  # Xuống dòng Open - Close

            # Căn giữa nội dung cột "Category" và "Hotline"
            category_item = QTableWidgetItem(restaurant["category"])
            category_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row, 5, category_item)

            self.setItem(row, 6, QTableWidgetItem(restaurant["address"]))

            hotline_item = QTableWidgetItem(restaurant["hotline"])
            hotline_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row, 7, hotline_item)

            self.setItem(row, 8, QTableWidgetItem(str(restaurant["accessibility"])))

            # Tăng độ cao hàng
            self.setRowHeight(row, self.ROW_HEIGHT)

        self.model.offset += len(restaurants)  # Cập nhật offset

    def create_image_widget(self, image_url):
        """Tạo Widget chứa hình ảnh tròn và căn giữa."""
        container = QWidget()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Căn giữa hình ảnh
        label = QLabel()
        label.setFixedSize(self.IMAGE_SIZE, self.IMAGE_SIZE)

        # Tải ảnh từ URL
        try:
            response = requests.get(image_url, timeout=5)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                pixmap = QPixmap()
                pixmap.loadFromData(image_data.read())
                rounded_pixmap = self.get_rounded_pixmap(pixmap)  # Chuyển thành ảnh tròn
                label.setPixmap(rounded_pixmap)
        except requests.exceptions.RequestException:
            label.setText("Image Load Error")  # Hiển thị lỗi nếu ảnh không tải được

        layout.addWidget(label)
        container.setLayout(layout)
        return container

    def get_rounded_pixmap(self, pixmap):
        """Chuyển đổi QPixmap thành hình tròn hoàn hảo, không bị cắt méo."""
        pixmap = pixmap.scaled(self.IMAGE_SIZE, self.IMAGE_SIZE, Qt.AspectRatioMode.KeepAspectRatioByExpanding)

        rounded_pixmap = QPixmap(self.IMAGE_SIZE, self.IMAGE_SIZE)
        rounded_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addEllipse(QRectF(0, 0, self.IMAGE_SIZE, self.IMAGE_SIZE))
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        return rounded_pixmap

    def create_multiline_text(self, text):
        """Tạo text xuống dòng (mỗi thứ trên 1 dòng) và loại bỏ khoảng trắng thừa."""
        lines = [line.strip() for line in text.split("|")]  # Xóa khoảng trắng đầu & cuối
        return QTableWidgetItem("\n".join(lines))

    def create_star_widget(self, rating):
        """Tạo Widget hiển thị số sao + số điểm xuống dòng."""
        full_stars = int(rating)  # Số sao vàng nguyên
        half_star = 1 if rating - full_stars >= 0.5 else 0  # Nếu có 0.5 thì thêm nửa sao
        empty_stars = 5 - (full_stars + half_star)  # Phần còn lại là sao xám

        star_layout = QVBoxLayout()
        star_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Hàng sao
        star_row = QLabel("⭐" * full_stars + "🌗" * half_star + "☆" * empty_stars)
        star_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Hàng số điểm
        rating_label = QLabel(f"{rating}")
        rating_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        star_layout.addWidget(star_row)
        star_layout.addWidget(rating_label)

        container = QWidget()
        container.setLayout(star_layout)
        return container

    def format_table(self):
        """Cấu hình bảng: Ẩn cột ID, điều chỉnh độ rộng cột."""
        self.setColumnHidden(0, True)  # Ẩn cột ID

        # Đặt độ rộng cho từng cột
        self.setColumnWidth(1, 100)  # Ảnh
        self.setColumnWidth(2, 150)  # Restaurant name
        self.setColumnWidth(3, 120)  # Rate
        self.setColumnWidth(4, 200)  # Open - Close (cố định)
        self.setColumnWidth(5, 120)  # Category (căn giữa)
        self.setColumnWidth(6, 250)  # Address (cố định)
        self.setColumnWidth(7, 120)  # Hotline (căn giữa)
        self.setColumnWidth(8, 100)  # Accessibility

        # Các cột khác sẽ tự động giãn theo nội dung
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.horizontalHeader().setStretchLastSection(True)  # Cột cuối sẽ kéo dãn

    def style_table(self):
        """Tạo màu header bảng thành màu cam FF862F."""
        self.setStyleSheet("""
            QHeaderView::section {
                background-color: #FF862F;
                color: white;
                font-weight: bold;
                padding: 8px;
                border: 1px solid #d67a2c;
            }
        """)

""" Version 8"""
