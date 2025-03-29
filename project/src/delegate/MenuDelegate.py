from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QHeaderView
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath
from PyQt6.QtCore import QThreadPool

from project.src.ImageLoader import ImageLoader
from project.src.model.MenuModel import MenuModel

class MenuDelegate(QTableWidget):
    IMAGE_SIZE = 80  # Kích thước hình ảnh
    ROW_HEIGHT = 100  # Độ cao của hàng
    MAX_CONCURRENT_THREADS = 5  # Giới hạn số thread tải ảnh đồng thời
    MAX_CACHE_SIZE = 50  # Giới hạn số ảnh trong cache

    def __init__(self, place_id=None):  # Thêm giá trị mặc định là None
        super().__init__()
        self.place_id = place_id
        if place_id is None:
            table_headers = ["_id", "", "Item", "Rate", "Price", "Restaurant","Category","Description", "Review"]
        else:
            table_headers = ["_id", "", "Item", "Rate", "Price", "Description", "Review"]

        self.num_columns=len(table_headers)
        self.setColumnCount(self.num_columns)
        self.setHorizontalHeaderLabels(table_headers)

        # Selection: entire row, single selection
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        # Image cache and loaders
        self.image_widgets = {}  # row -> QLabel
        self.image_loaders = {}  # row -> ImageLoader
        self.image_cache = {}  # url -> QPixmap (cache ảnh đã tải)
        self.thread_pool = QThreadPool.globalInstance()
        self.thread_pool.setMaxThreadCount(self.MAX_CONCURRENT_THREADS)

        # Set column widths
        self.setColumnWidth(0, 0)  # _id (ẩn)
        self.setColumnWidth(1, 150)  # Featured Image
        self.setColumnWidth(2, 150)  # Item
        self.setColumnWidth(3, 150)   # Rate (tăng độ rộng để hiển thị sao)
        self.setColumnWidth(4, 100)  # Price
        self.setColumnWidth(self.num_columns-2, 300)  # Description (tăng độ rộng để hiển thị đầy đủ)
        self.setColumnWidth(self.num_columns-1, 200)  # Review
        if place_id is None:
            self.setColumnWidth(5, 150)  # Restaurant
            self.setColumnWidth(6, 80)  # Category

        # Ẩn cột _id
        self.setColumnHidden(0, True)

        # Style the table
        self.style_table()

    def load_more_menu(self, menu_items):
        if not menu_items:
            print("MenuDelegate: No menu items to load.")
            self.clearContents()
            self.setRowCount(1)
            item = QTableWidgetItem("No menu items available.")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(0, 0, item)
            return

        print(f"MenuDelegate: Loading {len(menu_items)} menu items")
        for menu_item in menu_items:
            row = self.rowCount()
            self.insertRow(row)
            # Cột _id (ẩn đi)
            self.setItem(row, 0, QTableWidgetItem(str(menu_item.get("_id", "N/A"))))
            # Cột Featured Image (tải ảnh bất đồng bộ)
            self.setCellWidget(row, 1, self.create_image_widget(row, menu_item.get("featured_image", "")))
            # Cột Item
            item = QTableWidgetItem(menu_item.get("Item", "N/A"))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row, 2, item)
            # Cột Rate (hiển thị số sao + biểu tượng sao)
            self.setCellWidget(row, 3, self.create_star_widget(menu_item.get("Rate", 0)))
            # Cột Price (định dạng với dấu phân cách hàng nghìn)
            price = menu_item.get("Price", 0)
            formatted_price = "{:,}".format(int(price))  # Định dạng giá: 79000 -> 79,000
            price_item = QTableWidgetItem(formatted_price)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row, 4, price_item)
            # Cột Description
            description_item = QTableWidgetItem(menu_item.get("Description", "N/A"))
            description_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.setItem(row, self.num_columns-2, description_item)
            # Cột Review
            review_item = QTableWidgetItem("\n".join(menu_item.get("Review", [])))
            review_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.setItem(row, self.num_columns-1, review_item)

            if self.place_id is None:
                # Cót Restaurant
                self.setItem(row, 5, QTableWidgetItem(menu_item.get("restaurant_name", "N/A")))
                # Cót Category
                self.setItem(row, 6, QTableWidgetItem(menu_item.get("category", "N/A")))
            # Tăng độ cao hàng
            self.setRowHeight(row, self.ROW_HEIGHT)

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
        """Cập nhật ảnh sau khi tải xong."""
        if row not in self.image_widgets:
            print(f"Row {row} not found in image_widgets, skipping update")
            if row in self.image_loaders:
                del self.image_loaders[row]
            return

        label = self.image_widgets[row]
        if not label:  # Kiểm tra xem label có còn tồn tại không
            print(f"Label for row {row} has been deleted, skipping update")
            if row in self.image_loaders:
                del self.image_loaders[row]
            return

        if pixmap.isNull():
            label.setText("Image Load Error")
        else:
            # Lưu vào cache
            url = next((loader.url for loader in self.image_loaders.values() if loader.row == row), None)
            if url and url not in self.image_cache:
                self.image_cache[url] = pixmap
                # Giới hạn kích thước cache
                if len(self.image_cache) > self.MAX_CACHE_SIZE:
                    oldest_url = next(iter(self.image_cache))
                    del self.image_cache[oldest_url]

            # Chuyển ảnh thành hình tròn
            rounded_pixmap = self.get_rounded_pixmap(pixmap)
            label.setPixmap(rounded_pixmap)
            label.setScaledContents(True)

        # Xóa loader sau khi hoàn thành
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

    def style_table(self):
        """Tạo màu header bảng thành màu đen 343131 và đảm bảo highlight toàn bộ hàng."""
        self.setStyleSheet("""
            QHeaderView::section {
                background-color: #343131;
                color: #FABC3F;
                font-weight: bold;
                padding: 8px;
                border: 1px solid #d67a2c;
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
        # Cho phép các cột tự động điều chỉnh kích thước
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Không kéo dài cột cuối cùng, để các cột chia đều không gian
        self.horizontalHeader().setStretchLastSection(False)

    def load_more_menu(self, menu_items):
        if not menu_items:
            print("MenuDelegate: No menu items to load.")
            self.clearContents()
            self.setRowCount(1)
            item = QTableWidgetItem("No menu items available.")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(0, 0, item)
            return

        print(f"MenuDelegate: Loading {len(menu_items)} menu items")
        for menu_item in menu_items:
            row = self.rowCount()
            self.insertRow(row)
            # Cột _id (ẩn đi)
            self.setItem(row, 0, QTableWidgetItem(str(menu_item.get("_id", "N/A"))))
            # Cột Featured Image (tải ảnh bất đồng bộ)
            self.setCellWidget(row, 1, self.create_image_widget(row, menu_item.get("featured_image", "")))
            # Cột Item
            item = QTableWidgetItem(menu_item.get("Item", "N/A"))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row, 2, item)
            # Cột Rate (hiển thị số sao + biểu tượng sao)
            self.setCellWidget(row, 3, self.create_star_widget(menu_item.get("Rate", 0)))
            # Cột Price (định dạng với dấu phân cách hàng nghìn)
            price = menu_item.get("Price", 0)
            formatted_price = "{:,}".format(int(price))  # Định dạng giá: 79000 -> 79,000
            price_item = QTableWidgetItem(formatted_price)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row, 4, price_item)
            # Cột Description
            description_item = QTableWidgetItem(menu_item.get("Description", "N/A"))
            description_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.setItem(row, self.num_columns - 2, description_item)
            # Cột Review
            review_item = QTableWidgetItem("\n".join(menu_item.get("Review", [])))
            review_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.setItem(row, self.num_columns - 1, review_item)

            if self.place_id is None:
                # Cột Restaurant
                self.setItem(row, 5, QTableWidgetItem(menu_item.get("restaurant_name", "N/A")))
                # Cột Category
                self.setItem(row, 6, QTableWidgetItem(menu_item.get("category", "N/A")))
            # Tăng độ cao hàng
            self.setRowHeight(row, self.ROW_HEIGHT)

    def closeEvent(self, event):
        """Xử lý khi đóng widget để tránh crash."""
        self.thread_pool.clear()
        self.thread_pool.waitForDone()
        self.image_loaders.clear()
        self.image_widgets.clear()
        self.image_cache.clear()
        super().closeEvent(event)