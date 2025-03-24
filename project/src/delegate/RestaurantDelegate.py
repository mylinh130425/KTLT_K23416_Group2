from io import BytesIO
from PyQt6.QtCore import Qt, QRectF, QThreadPool
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QColor
from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QWidget, QHBoxLayout, QVBoxLayout
)

from project.src.ImageLoader import ImageLoader
from project.src.model.RestaurantModel import RestaurantModel
class RestaurantDelegate(QTableWidget):
    IMAGE_SIZE = 80  # Kích thước hình ảnh
    ROW_HEIGHT = 130  # Độ cao của hàng
    MAX_CONCURRENT_THREADS = 5  # Giới hạn số thread tải ảnh đồng thời
    MAX_CACHE_SIZE = 50  # Giới hạn số ảnh trong cache

    def __init__(self):
        super().__init__()
        self.model = RestaurantModel()
        self.setColumnCount(9)  # Đầy đủ các cột: _id, Image, Restaurant, Rate, Open - Close, Category, Address, Hotline, Accessibility
        self.setHorizontalHeaderLabels([
            "_id", "Image", "Restaurant", "Rate", "Open - Close", "Category", "Address", "Hotline", "Accessibility"
        ])

        # Selection: entire row, single selection
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        # Image cache and loaders
        self.image_widgets = {}  # row -> QLabel
        self.image_loaders = {}  # row -> ImageLoader
        self.image_cache = {}  # url -> QPixmap (cache ảnh đã tải)
        self.thread_pool = QThreadPool.globalInstance()
        self.thread_pool.setMaxThreadCount(self.MAX_CONCURRENT_THREADS)

        self.load_more_restaurants()
        self.format_table()
        self.style_table()

    def load_more_restaurants(self):
        # Dừng tất cả các thread ImageLoader cũ trước khi tải thêm
        self.thread_pool.clear()
        self.thread_pool.waitForDone()
        self.image_loaders.clear()
        self.image_widgets.clear()

        restaurants = self.model.get_restaurants()
        if not restaurants:
            print("RestaurantDelegate: No restaurants to display.")
            self.clearContents()
            self.setRowCount(1)
            item = QTableWidgetItem("No restaurants available.")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(0, 0, item)
            return

        print(f"RestaurantDelegate: Loading {len(restaurants)} restaurants")
        current_row_count = self.rowCount()
        self.setRowCount(current_row_count + len(restaurants))
        for i, restaurant in enumerate(restaurants):
            row = current_row_count + i
            # Cột _id (ẩn đi)
            item = QTableWidgetItem(str(restaurant["_id"]))
            self.setItem(row, 0, item)

            # Cột Image (ảnh tròn căn giữa)
            self.setCellWidget(row, 1, self.create_image_widget(row, restaurant.get("featured_image", "")))

            # Cột Restaurant (name)
            self.setItem(row, 2, QTableWidgetItem(restaurant["name"]))

            # Cột Rate (hiển thị rating dạng sao)
            self.setCellWidget(row, 3, self.create_star_widget(restaurant["rating"]))

            # Cột Open - Close (open_hours)
            self.setItem(row, 4, QTableWidgetItem(restaurant["open_hours"]))

            # Cột Category (căn giữa)
            category_item = QTableWidgetItem(restaurant["category"])
            category_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row, 5, category_item)

            # Cột Address
            self.setItem(row, 6, QTableWidgetItem(restaurant["address"]))

            # Cột Hotline (căn giữa)
            hotline_item = QTableWidgetItem(restaurant["hotline"] if restaurant["hotline"] else "N/A")
            hotline_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row, 7, hotline_item)

            # Cột Accessibility
            self.setItem(row, 8, QTableWidgetItem(restaurant["accessibility"]))

            # Tăng độ cao hàng
            self.setRowHeight(row, self.ROW_HEIGHT)

        self.model.offset += len(restaurants)  # Cập nhật offset

    def create_image_widget(self, row, image_url):
        """Tạo Widget chứa hình ảnh tròn và căn giữa, tải ảnh bất đồng bộ."""
        container = QWidget()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Căn giữa hình ảnh
        label = QLabel()
        label.setFixedSize(self.IMAGE_SIZE, self.IMAGE_SIZE)
        label.setText("Loading...")  # Hiển thị "Loading..." trong khi tải ảnh
        layout.addWidget(label)
        container.setLayout(layout)

        # Lưu label để cập nhật sau khi tải ảnh
        self.image_widgets[row] = label

        # Kiểm tra cache trước khi tải
        if image_url in self.image_cache:
            print(f"Using cached image for row {row}: {image_url}")
            rounded_pixmap = self.get_rounded_pixmap(self.image_cache[image_url])
            label.setPixmap(rounded_pixmap)
            label.setScaledContents(True)
        elif image_url:
            print(f"Loading image for row {row}: {image_url}")
            loader = ImageLoader(row, image_url)
            loader.signals.image_loaded.connect(self.update_image)
            self.image_loaders[row] = loader
            self.thread_pool.start(loader)  # Sử dụng QThreadPool để quản lý thread
        else:
            label.setText("No Image")  # Nếu không có URL, hiển thị "No Image"

        return container

    def update_image(self, row, pixmap):
        print(f"Updating image for row {row}")
        if row not in self.image_widgets:
            print(f"Row {row} not found in image_widgets, skipping update")
            if row in self.image_loaders:
                del self.image_loaders[row]
            return

        label = self.image_widgets[row]
        if not label:
            print(f"Label for row {row} has been deleted, skipping update")
            if row in self.image_loaders:
                del self.image_loaders[row]
            return

        if pixmap.isNull():
            label.setText("Image Load Error")
        else:
            url = next((loader.url for loader in self.image_loaders.values() if loader.row == row), None)
            if url and url not in self.image_cache:
                self.image_cache[url] = pixmap
                if len(self.image_cache) > self.MAX_CACHE_SIZE:
                    oldest_url = next(iter(self.image_cache))
                    del self.image_cache[oldest_url]
            rounded_pixmap = self.get_rounded_pixmap(pixmap)
            label.setPixmap(rounded_pixmap)
            label.setScaledContents(True)

        if row in self.image_loaders:
            del self.image_loaders[row]

    def get_rounded_pixmap(self, pixmap):
        """Chuyển đổi QPixmap thành hình tròn hoàn hảo, không bị cắt méo."""
        scaled_pixmap = pixmap.scaled(self.IMAGE_SIZE, self.IMAGE_SIZE,
                                      Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                      Qt.TransformationMode.SmoothTransformation)

        width = scaled_pixmap.width()
        height = scaled_pixmap.height()
        x = (width - self.IMAGE_SIZE) // 2
        y = (height - self.IMAGE_SIZE) // 2
        cropped_pixmap = scaled_pixmap.copy(x, y, self.IMAGE_SIZE, self.IMAGE_SIZE)

        rounded_pixmap = QPixmap(self.IMAGE_SIZE, self.IMAGE_SIZE)
        rounded_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addEllipse(QRectF(0, 0, self.IMAGE_SIZE, self.IMAGE_SIZE))
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, cropped_pixmap)
        painter.end()

        return rounded_pixmap

    def create_star_widget(self, rating):
        """Tạo Widget hiển thị số sao + số điểm xuống dòng."""
        full_stars = int(rating)  # Số sao vàng nguyên
        half_star = 1 if rating - full_stars >= 0.5 else 0  # Nếu có 0.5 thì thêm nửa sao
        empty_stars = 5 - (full_stars + half_star)  # Phần còn lại là sao xám

        star_layout = QVBoxLayout()
        star_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Hàng số điểm
        rating_label = QLabel(f"{rating:.1f}")
        rating_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Hàng sao
        star_row = QLabel("★" * full_stars + "⯪" * half_star + "☆" * empty_stars)
        star_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        star_layout.addWidget(rating_label)
        star_layout.addWidget(star_row)

        container = QWidget()
        container.setLayout(star_layout)
        return container

    def format_table(self):
        """Cấu hình bảng: Ẩn cột ID, điều chỉnh độ rộng cột."""
        self.setColumnHidden(0, True)  # Ẩn cột ID

        # Đặt độ rộng cho từng cột
        self.setColumnWidth(1, 100)  # Ảnh
        self.setColumnWidth(2, 200)  # Restaurant name
        self.setColumnWidth(3, 150)  # Rate
        self.setColumnWidth(4, 150)  # Open - Close
        self.setColumnWidth(5, 150)  # Category (căn giữa)
        self.setColumnWidth(6, 300)  # Address
        self.setColumnWidth(7, 120)  # Hotline (căn giữa)
        self.setColumnWidth(8, 120)  # Accessibility

        # Các cột khác sẽ tự động giãn theo nội dung
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.horizontalHeader().setStretchLastSection(True)  # Cột cuối sẽ kéo dãn

    def style_table(self):
        """Tạo màu header bảng thành màu cam FF862F và đảm bảo highlight toàn bộ hàng."""
        self.setStyleSheet("""
            QHeaderView::section {
                background-color: #343131;
                color: #FABC3F;
                font-weight: bold;
                padding: 8px;
                border: 1px solid #FABC3F;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #ADD8E6;  /* Màu highlight khi chọn hàng */
                color: black;
            }
            QTableWidget QWidget {  /* Áp dụng cho các widget con (QLabel, v.v.) */
                background-color: transparent;  /* Đảm bảo widget con không che màu highlight */
            }
            QTableWidget QWidget:selected {  /* Khi widget con nằm trong hàng được chọn */
                background-color: #ADD8E6;  /* Highlight cùng màu với hàng */
            }
        """)

    def closeEvent(self, event):
        """Xử lý khi đóng widget để tránh crash."""
        self.thread_pool.clear()
        self.thread_pool.waitForDone()
        self.image_loaders.clear()
        self.image_widgets.clear()
        self.image_cache.clear()
        super().closeEvent(event)