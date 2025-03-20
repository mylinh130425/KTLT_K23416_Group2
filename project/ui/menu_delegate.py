from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import requests
from io import BytesIO


class ImageLoader(QThread): #Thêm vào để đỡ lag khi Scroll xuống
    """Luồng để tải hình ảnh bất đồng bộ."""
    image_loaded = pyqtSignal(int, QPixmap)  # Tín hiệu gửi về khi hình ảnh tải xong

    def __init__(self, row, url):
        super().__init__()
        self.row = row
        self.url = url

    def run(self):
        try:
            response = requests.get(self.url)
            pixmap = QPixmap()
            pixmap.loadFromData(BytesIO(response.content).getvalue())
            if not pixmap.isNull():
                pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)
                self.image_loaded.emit(self.row, pixmap)
        except Exception as e:
            print(f"Error loading image for row {self.row}: {e}")


class MenuDelegate(QTableWidget):
    def __init__(self):
        super().__init__()
        table_headers = ["_id", " ", "Food", "Rate", "Price", "Description", "Review"]
        self.setColumnCount(len(table_headers))
        self.setHorizontalHeaderLabels(table_headers)

        # Kích hoạt chế độ chọn hàng
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        # Tùy chỉnh màu sắc của QTableWidget
        self.setStyleSheet("""
            QTableWidget {
                background-color: #fff8ee;  /* Màu nền bảng: be nhạt */
                gridline-color: #d3d3d3;    /* Màu đường kẻ: xám nhạt */
            }
            QTableWidget::item {
                color: #000000;             /* Màu chữ: đen */
            }
            QTableWidget::item:selected {
                background-color: #d3d3d3;  /* Màu highlight khi chọn hàng: xám */
                color: #000000;             /* Màu chữ khi chọn: đen */
            }
            QHeaderView::section {
                background-color: #FFA55A;  /* Màu nền tiêu đề: cam */
                color: #000000;             /* Màu chữ tiêu đề: đen */
                font-weight: bold;          /* In đậm chữ tiêu đề */
                padding: 4px;               /* Khoảng cách trong tiêu đề */
                border: 1px solid #d3d3d3;  /* Đường viền tiêu đề: xám nhạt */
            }
        """)

        # Bộ nhớ đệm cho hình ảnh
        self.image_cache = {}  # Lưu trữ hình ảnh đã tải
        self.image_loaders = {}  # Lưu trữ các luồng tải hình ảnh
        self.image_urls = {}  # Lưu trữ URL hình ảnh cho từng hàng

        # Kết nối tín hiệu cuộn để tải hình ảnh theo nhu cầu
        self.verticalScrollBar().valueChanged.connect(self.load_visible_images)

    def load_more_menu(self, menu_items): #Chỉnh
        """Nạp dữ liệu vào bảng."""
        if not menu_items:
            print("No menu items to display.")
            return

        # Tắt cập nhật giao diện để tăng hiệu suất
        self.setUpdatesEnabled(False)

        current_row_count = self.rowCount()
        self.setRowCount(current_row_count + len(menu_items))

        for i, item in enumerate(menu_items):
            row = current_row_count + i
            print(f"Loading item: {item}")

            # Cột 0: _id (ẩn)
            self.setItem(row, 0, QTableWidgetItem(str(item.get("_id", "N/A"))))

            # Cột 1: Hình ảnh (featured_image) - Ban đầu để trống, sẽ tải sau
            image_item = QTableWidgetItem("Loading...")
            image_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row, 1, image_item)
            # Lưu URL để tải sau
            feature_img = item.get("featured_image", "")
            self.image_urls[row] = feature_img

            # Cột 2: Food (Item)
            self.setItem(row, 2, QTableWidgetItem(item.get("Item", "N/A")))

            # Cột 3: Rate (Sử dụng QTableWidgetItem thay vì QLabel)
            rating = float(item.get("Rate", 0.0))
            display_rating = round(rating * 2) / 2
            full_stars = int(rating)
            decimal_part = rating - full_stars
            half_star = 1 if decimal_part >= 0.3 else 0
            empty_stars = 5 - full_stars - half_star
            stars_display = "★" * full_stars + "⯪" * half_star + "☆" * empty_stars
            rating_text = f"{display_rating:.1f}\n{stars_display}"
            rating_item = QTableWidgetItem(rating_text)
            rating_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row, 3, rating_item)

            # Cột 4: Price (Định dạng với dấu phân cách hàng nghìn và căn giữa)
            price = item.get("Price", 0)
            try:
                price = float(price)
                formatted_price = "{:,.0f} đ".format(price).replace(",", ".")
            except (ValueError, TypeError):
                formatted_price = "N/A"
            price_item = QTableWidgetItem(formatted_price)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row, 4, price_item)

            # Cột 5: Description
            self.setItem(row, 5, QTableWidgetItem(item.get("Description", "N/A")))

            # Cột 6: Review
            reviews = item.get("Review", [])
            review_text = "; ".join(reviews) if reviews else "No Review"
            self.setItem(row, 6, QTableWidgetItem(review_text))

        # Ẩn cột _id
        self.setColumnHidden(0, True)

        # Điều chỉnh kích thước cột và hàng
        self.setColumnWidth(1, 60)   # Cột hình ảnh
        self.setColumnWidth(2, 150)  # Cột Food
        self.setColumnWidth(3, 100)  # Cột Rate
        self.setColumnWidth(4, 100)  # Cột Price
        self.setColumnWidth(5, 200)  # Cột Description
        self.setColumnWidth(6, 200)  # Cột Review
        self.resizeRowsToContents()

        # Bật lại cập nhật giao diện
        self.setUpdatesEnabled(True)

        # Tải hình ảnh cho các hàng đang hiển thị
        self.load_visible_images()

    def load_visible_images(self): #Phần thêm mới
        """Tải hình ảnh cho các hàng đang hiển thị trong viewport."""
        first_visible_row = max(0, self.rowAt(self.viewport().rect().top()))
        last_visible_row = min(self.rowCount() - 1, self.rowAt(self.viewport().rect().bottom()))

        for row in range(first_visible_row, last_visible_row + 1):
            if row not in self.image_urls:
                continue

            url = self.image_urls[row]
            if not url:
                continue

            # Kiểm tra bộ nhớ đệm
            if url in self.image_cache:
                pixmap = self.image_cache[url]
                self.set_image(row, pixmap)
            else:
                # Nếu đang tải, không tạo luồng mới
                if row in self.image_loaders:
                    continue
                # Tạo luồng tải hình ảnh
                loader = ImageLoader(row, url)
                loader.image_loaded.connect(self.on_image_loaded)
                self.image_loaders[row] = loader
                loader.start()

    def on_image_loaded(self, row, pixmap): #Phần thêm mới
        """Xử lý khi hình ảnh tải xong."""
        if row in self.image_urls:
            url = self.image_urls[row]
            self.image_cache[url] = pixmap  # Lưu vào bộ nhớ đệm
            self.set_image(row, pixmap)
            # Xóa luồng khỏi danh sách
            if row in self.image_loaders:
                del self.image_loaders[row]

    def set_image(self, row, pixmap): #Phần thêm mới
        """Hiển thị hình ảnh trong ô."""
        item = QTableWidgetItem()
        if pixmap.isNull():
            item.setText("No Image")
        else:
            item.setData(Qt.ItemDataRole.DecorationRole, pixmap)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setItem(row, 1, item)

