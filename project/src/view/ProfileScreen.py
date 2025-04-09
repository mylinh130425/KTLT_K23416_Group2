from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QUrl, QRectF
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QFileDialog
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt6.QtCore import Qt

from project.src.view.ClickableLabel import ClickableLabel

class ProfileScreen(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        print("Setting up Profile Screen")
        self.parent = parent
        
        # Khởi tạo NetworkAccessManager để xử lý hình ảnh
        self.image_manager = QNetworkAccessManager()
        self.image_manager.finished.connect(self.set_image)
        
        # Lưu trữ đường dẫn hình ảnh đã upload
        self.uploaded_image_path = None
        
        # Chuẩn bị các ảnh mặc định sẵn sàng
        self.default_profile_pixmap = self.load_and_round_image("../../image/profile_panel_icon.png", 90)
        self.default_sidebar_pixmap = self.load_and_round_image("../../image/profile_panel_icon.png", 60)
        
        # Thiết lập UI
        self.setup_ui()
        self.process_signals_slots()

    def load_and_round_image(self, image_path, size):
        """Load ảnh từ đường dẫn và tạo phiên bản tròn với kích thước xác định"""
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            return self.get_rounded_pixmap(pixmap, size)
        return None

    def setup_ui(self):
        # MAIN PROFILE PHOTO - Ảnh lớn ở giữa trên cùng
        if hasattr(self.parent, 'profile_photo_label'):
            # Xóa widget cũ
            original_photo = self.parent.profile_photo_label
            photo_parent = original_photo.parent()
            photo_layout = photo_parent.layout()
            
            # Nếu có layout, gỡ bỏ widget cũ
            if photo_layout:
                photo_layout.removeWidget(original_photo)
            
            original_photo.hide()
            original_photo.deleteLater()
            
            # Tạo widget mới với kích thước cố định và style giống trong ảnh 2
            new_photo_label = ClickableLabel(photo_parent)
            new_photo_label.setMinimumSize(QtCore.QSize(90, 90))
            new_photo_label.setMaximumSize(QtCore.QSize(90, 90))
            new_photo_label.setStyleSheet("border-radius: 45px; border: 1.5px solid #333;")
            new_photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            new_photo_label.setCursor(Qt.CursorShape.PointingHandCursor)
            new_photo_label.setScaledContents(True)
            
            # Thiết lập ảnh mặc định ngay lập tức
            if self.default_profile_pixmap:
                new_photo_label.setPixmap(self.default_profile_pixmap)
            else:
                new_photo_label.setText("Click to upload")
            
            # Thêm vào đúng vị trí trong layout với alignment là AlignHCenter
            # Đây là trick quan trọng để đặt ảnh ở giữa như trong mẫu
            if photo_layout:
                # Xóa widget trong index 0 của layout (nếu có)
                if photo_layout.count() > 0:
                    item = photo_layout.itemAt(0)
                    if item and item.widget():
                        item.widget().setParent(None)
                
                # Thêm widget mới vào vị trí đầu tiên với alignment là AlignHCenter
                photo_layout.insertWidget(0, new_photo_label, 0, Qt.AlignmentFlag.AlignHCenter)
            
            # Lưu tham chiếu
            self.parent.profile_photo_label = new_photo_label

            # Kết nối sự kiện click
            self.parent.profile_photo_label.clicked.connect(self.upload_profile_image)
        
        # SIDEBAR PROFILE PHOTO - Ảnh nhỏ ở sidebar bên trái
        if hasattr(self.parent, 'profilesidebar_photo_label'):
            # Dựa trên cấu trúc UI, profilesidebar_photo_label nằm trong:
            # profile_panel > verticalLayout_44 > verticalLayout_45 > horizontalLayout_23
            
            # Lấy widget gốc 
            original_sidebar = self.parent.profilesidebar_photo_label
            profile_panel = None
            
            # Tìm profile_panel - cha của tất cả các widget trong sidebar
            if hasattr(self.parent, 'profile_panel'):
                profile_panel = self.parent.profile_panel
            
            if profile_panel:
                # Tìm các layout cần thiết
                verticalLayout_44 = None
                verticalLayout_45 = None
                horizontalLayout_23 = None
                
                # Lấy verticalLayout_44 (layout chính của profile_panel)
                if profile_panel.layout():
                    verticalLayout_44 = profile_panel.layout()
                    
                    # Tìm verticalLayout_45 trong verticalLayout_44
                    for i in range(verticalLayout_44.count()):
                        item = verticalLayout_44.itemAt(i)
                        if item.layout() and item.layout().objectName() == "verticalLayout_45":
                            verticalLayout_45 = item.layout()
                            break
                    
                    # Tìm horizontalLayout_23 trong verticalLayout_45
                    if verticalLayout_45:
                        for i in range(verticalLayout_45.count()):
                            item = verticalLayout_45.itemAt(i)
                            if item.layout() and item.layout().objectName() == "horizontalLayout_23":
                                horizontalLayout_23 = item.layout()
                                break
                
                # Xóa sidebar_photo_label khỏi horizontalLayout_23
                if horizontalLayout_23:
                    for i in range(horizontalLayout_23.count()):
                        item = horizontalLayout_23.itemAt(i)
                        if item.widget() == original_sidebar:
                            horizontalLayout_23.removeWidget(original_sidebar)
                            break
                
                # Xóa cũ
                original_sidebar.hide()
                original_sidebar.deleteLater()
                
                # Tạo ClickableLabel mới
                new_sidebar_label = ClickableLabel(profile_panel)
                new_sidebar_label.setMinimumSize(QtCore.QSize(60, 60))
                new_sidebar_label.setMaximumSize(QtCore.QSize(60, 60))
                new_sidebar_label.setStyleSheet("border-radius: 30px; border: 1.5px solid white;")
                new_sidebar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                new_sidebar_label.setCursor(Qt.CursorShape.PointingHandCursor)
                new_sidebar_label.setScaledContents(True)
                
                # Thiết lập ảnh mặc định ngay lập tức
                if self.default_sidebar_pixmap:
                    new_sidebar_label.setPixmap(self.default_sidebar_pixmap)
                else:
                    new_sidebar_label.setText("Click to upload")
                
                # Thêm vào horizontalLayout_23
                if horizontalLayout_23:
                    horizontalLayout_23.addWidget(new_sidebar_label)
                    
                    # Kiểm tra và đảm bảo horizontalLayout_23 ở vị trí đầu tiên của verticalLayout_45
                    if verticalLayout_45:
                        # Xóa horizontalLayout_23 khỏi vị trí hiện tại (nếu có)
                        for i in range(verticalLayout_45.count()):
                            item = verticalLayout_45.itemAt(i)
                            if item.layout() == horizontalLayout_23:
                                verticalLayout_45.removeItem(item)
                                break
                        
                        # Thêm lại horizontalLayout_23 vào vị trí đầu tiên
                        verticalLayout_45.insertLayout(0, horizontalLayout_23)
                else:
                    # Nếu không tìm thấy layout, tạo mới và thêm vào
                    horizontalLayout_23 = QtWidgets.QHBoxLayout()
                    horizontalLayout_23.setObjectName("horizontalLayout_23")
                    horizontalLayout_23.addWidget(new_sidebar_label)
                    
                    if verticalLayout_45:
                        verticalLayout_45.insertLayout(0, horizontalLayout_23)
                    elif verticalLayout_44:
                        verticalLayout_44.insertLayout(0, horizontalLayout_23)
            else:
                # Xử lý trường hợp không tìm thấy profile_panel
                original_sidebar.hide()
                original_sidebar.deleteLater()
                
                # Tạo widget mới với vị trí tuyệt đối
                sidebar_parent = original_sidebar.parent()
                new_sidebar_label = ClickableLabel(sidebar_parent)
                new_sidebar_label.setMinimumSize(QtCore.QSize(60, 60))
                new_sidebar_label.setMaximumSize(QtCore.QSize(60, 60))
                new_sidebar_label.setStyleSheet("border-radius: 30px; border: 1.5px solid white;")
                new_sidebar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                new_sidebar_label.setCursor(Qt.CursorShape.PointingHandCursor)
                new_sidebar_label.setScaledContents(True)
                new_sidebar_label.setGeometry(QtCore.QRect(20, 20, 60, 60))
                
                # Thiết lập ảnh mặc định ngay lập tức
                if self.default_sidebar_pixmap:
                    new_sidebar_label.setPixmap(self.default_sidebar_pixmap)
                else:
                    new_sidebar_label.setText("Click to upload")
                
                new_sidebar_label.show()
            
            # Lưu tham chiếu
            self.parent.profilesidebar_photo_label = new_sidebar_label
            
            # Kết nối sự kiện click
            self.parent.profilesidebar_photo_label.clicked.connect(self.upload_profile_image)

    def process_signals_slots(self):
        # Kết nối các tín hiệu và slots
        if hasattr(self.parent, 'profile_save_button'):
            self.parent.profile_save_button.clicked.connect(self.save_profile)
    
    def upload_profile_image(self):
        """Xử lý sự kiện click để upload ảnh mới"""
        print("Upload profile image clicked")
        # Sử dụng QFileDialog thay vì ClickableLabel.open_file_dialog để đảm bảo độ tin cậy
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent,
            "Open Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
            
        if file_path:
            self.uploaded_image_path = file_path
            print(f"Selected image: {file_path}")
            
            # Load và hiển thị ảnh dưới dạng tròn
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                # Tạo phiên bản tròn cho cả hai ảnh
                rounded_pixmap_small = self.get_rounded_pixmap(pixmap, 60)  # Nhỏ cho sidebar
                rounded_pixmap_large = self.get_rounded_pixmap(pixmap, 90)  # Lớn cho ảnh chính
                
                # Cập nhật cả hai ảnh
                if hasattr(self.parent, 'profile_photo_label'):
                    self.parent.profile_photo_label.setPixmap(rounded_pixmap_large)
                    self.parent.profile_photo_label.setScaledContents(True)
                    # Clear any text that might be showing
                    self.parent.profile_photo_label.setText("")
                    print("Updated main profile photo")
                
                if hasattr(self.parent, 'profilesidebar_photo_label'):
                    self.parent.profilesidebar_photo_label.setPixmap(rounded_pixmap_small)
                    self.parent.profilesidebar_photo_label.setScaledContents(True)
                    # Clear any text that might be showing
                    self.parent.profilesidebar_photo_label.setText("")
                    print("Updated sidebar profile photo")
                
                print(f"Image uploaded successfully: {file_path}")
                # Sẽ lưu ảnh này vào DB khi lưu profile
            else:
                print(f"Failed to load image from {file_path}")

    def get_rounded_pixmap(self, pixmap, size):
        """Chuyển đổi QPixmap thành hình tròn hoàn hảo, không bị cắt méo."""
        # Scale ảnh, giữ tỷ lệ, mở rộng để lấp đầy
        scaled_pixmap = pixmap.scaled(
            size, size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        
        # Cắt thành hình vuông (cắt từ giữa)
        width = scaled_pixmap.width()
        height = scaled_pixmap.height()
        x = (width - size) // 2
        y = (height - size) // 2
        cropped_pixmap = scaled_pixmap.copy(x, y, size, size)
        
        # Tạo pixmap hình tròn
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

    def load_default_images(self):
        """Load ảnh mặc định cho profile và chuyển thành hình tròn"""
        print("Loading default profile images")
        
        # Sử dụng ảnh đã được chuẩn bị hoặc tải lại nếu cần
        if not self.default_profile_pixmap:
            self.default_profile_pixmap = self.load_and_round_image("../../image/profile_panel_icon.png", 90)
            
        if not self.default_sidebar_pixmap:
            self.default_sidebar_pixmap = self.load_and_round_image("../../image/profile_panel_icon.png", 60)
        
        # Áp dụng ảnh cho các widget
        if hasattr(self.parent, 'profile_photo_label'):
            if self.default_profile_pixmap:
                print("Applying default profile image")
                self.parent.profile_photo_label.setPixmap(self.default_profile_pixmap)
                self.parent.profile_photo_label.setScaledContents(True)
                self.parent.profile_photo_label.setText("")  # Clear any text
            else:
                self.parent.profile_photo_label.setText("Click to upload")
                
        if hasattr(self.parent, 'profilesidebar_photo_label'):
            if self.default_sidebar_pixmap:
                print("Applying default sidebar image")
                self.parent.profilesidebar_photo_label.setPixmap(self.default_sidebar_pixmap)
                self.parent.profilesidebar_photo_label.setScaledContents(True)
                self.parent.profilesidebar_photo_label.setText("")  # Clear any text
            else:
                self.parent.profilesidebar_photo_label.setText("Click to upload")

    def save_profile(self):
        """Lưu thông tin profile, bao gồm cả ảnh mới nếu có"""
        if self.uploaded_image_path:
            # Trong ứng dụng thực tế, bạn sẽ:
            # 1. Upload ảnh lên server
            # 2. Lấy URL của ảnh đã upload
            # 3. Lưu URL đó vào cơ sở dữ liệu
            
            # Ở đây, chúng ta chỉ lưu đường dẫn cục bộ
            print(f"Đang cập nhật profile với ảnh mới: {self.uploaded_image_path}")
            # Code lưu ảnh vào DB sẽ được thêm vào đây
        
        # Tiếp tục với phương thức lưu hiện tại của parent
        if hasattr(self.parent, 'updateProfile'):
            self.parent.updateProfile()

    def set_image(self, reply):
        """Cập nhật QLabel với ảnh từ URL."""
        data = reply.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(data)

        if not pixmap.isNull():  # Kiểm tra xem ảnh có hợp lệ không
            # Đảm bảo các label đã được khởi tạo đúng
            if hasattr(self.parent, 'profile_photo_label') and hasattr(self.parent, 'profilesidebar_photo_label'):
                # Tạo phiên bản hình tròn của ảnh
                rounded_pixmap_large = self.get_rounded_pixmap(pixmap, 90)
                rounded_pixmap_small = self.get_rounded_pixmap(pixmap, 60)
                
                # Đặt ảnh cho các label
                self.parent.profile_photo_label.setPixmap(rounded_pixmap_large)
                self.parent.profile_photo_label.setScaledContents(True)
                self.parent.profile_photo_label.setText("")  # Clear any text
                
                self.parent.profilesidebar_photo_label.setPixmap(rounded_pixmap_small)
                self.parent.profilesidebar_photo_label.setScaledContents(True)
                self.parent.profilesidebar_photo_label.setText("")  # Clear any text
            else:
                print("profile_photo_label or profilesidebar_photo_label not found in parent widget")
        else:
            # Nếu không tải được, sử dụng ảnh mặc định đã được chuẩn bị
            if hasattr(self.parent, 'profile_photo_label'):
                if self.default_profile_pixmap:
                    self.parent.profile_photo_label.setPixmap(self.default_profile_pixmap)
                    self.parent.profile_photo_label.setScaledContents(True)
                    self.parent.profile_photo_label.setText("")
                else:
                    self.parent.profile_photo_label.setText("Click to upload")
                    
            if hasattr(self.parent, 'profilesidebar_photo_label'):
                if self.default_sidebar_pixmap:
                    self.parent.profilesidebar_photo_label.setPixmap(self.default_sidebar_pixmap)
                    self.parent.profilesidebar_photo_label.setScaledContents(True)
                    self.parent.profilesidebar_photo_label.setText("")
                else:
                    self.parent.profilesidebar_photo_label.setText("Click to upload")

    def update_profile_photo(self, image_url):
        """Gửi request để tải ảnh từ URL."""
        request = QNetworkRequest(QUrl(image_url))
        self.image_manager.get(request)
        print(f"Sending request to load profile image from: {image_url}") 