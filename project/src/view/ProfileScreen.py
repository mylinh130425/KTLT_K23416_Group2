from PyQt6 import QtWidgets
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
        
        # Thiết lập UI
        self.setup_ui()
        self.process_signals_slots()

    def setup_ui(self):
        print("Setting up profile UI")
        # Thay thế hoàn toàn QLabel bằng ClickableLabel (giống cách của ModifyRestaurantScreen)
        
        # Thay thế profile_photo_label chính
        if hasattr(self.parent, 'profile_photo_label'):
            # Lưu thông tin về vị trí và kích thước của label cũ
            original_photo = self.parent.profile_photo_label
            photo_parent = original_photo.parent()
            photo_layout = photo_parent.layout()
            photo_position = photo_layout.indexOf(original_photo)
            photo_size = original_photo.size()
            photo_style = original_photo.styleSheet()
            
            # Xóa label cũ
            photo_layout.removeWidget(original_photo)
            original_photo.deleteLater()
            
            # Tạo ClickableLabel mới
            self.parent.profile_photo_label = ClickableLabel(photo_parent)
            self.parent.profile_photo_label.setText("Click to upload")
            self.parent.profile_photo_label.setFixedSize(photo_size)
            self.parent.profile_photo_label.setStyleSheet("border-radius: 45px; border: 1.5px solid #333; cursor: pointer;")
            self.parent.profile_photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Thêm vào layout
            photo_layout.addWidget(self.parent.profile_photo_label, 0, Qt.AlignmentFlag.AlignHCenter)
            
            # Kết nối tín hiệu click để upload ảnh
            self.parent.profile_photo_label.clicked.connect(self.upload_profile_image)
            print(f"Main photo label replaced with ClickableLabel: {self.parent.profile_photo_label}")
        
        # Thay thế profilesidebar_photo_label
        if hasattr(self.parent, 'profilesidebar_photo_label'):
            # Lưu thông tin về vị trí và kích thước của label cũ
            original_sidebar = self.parent.profilesidebar_photo_label
            sidebar_parent = original_sidebar.parent()
            sidebar_layout = sidebar_parent.layout()
            sidebar_position = sidebar_layout.indexOf(original_sidebar)
            sidebar_size = original_sidebar.size()
            
            # Xóa label cũ
            sidebar_layout.removeWidget(original_sidebar)
            original_sidebar.deleteLater()
            
            # Tạo ClickableLabel mới
            self.parent.profilesidebar_photo_label = ClickableLabel(sidebar_parent)
            self.parent.profilesidebar_photo_label.setText("Click")
            self.parent.profilesidebar_photo_label.setFixedSize(sidebar_size)
            self.parent.profilesidebar_photo_label.setStyleSheet("border-radius: 30px; border: 1.5px solid white; cursor: pointer;")
            self.parent.profilesidebar_photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            try:
                # Thêm vào layout - sử dụng addWidget thay vì insertWidget để tương thích với tất cả loại layout
                sidebar_layout.addWidget(self.parent.profilesidebar_photo_label)
                
                # Kết nối tín hiệu click để upload ảnh
                self.parent.profilesidebar_photo_label.clicked.connect(self.upload_profile_image)
                print(f"Sidebar photo label replaced with ClickableLabel: {self.parent.profilesidebar_photo_label}")
            except Exception as e:
                print(f"Error adding widget to layout: {e}")
        
        # Load ảnh profile mặc định (đã làm tròn)
        self.load_default_images()

    def process_signals_slots(self):
        # Kết nối các tín hiệu và slots
        if hasattr(self.parent, 'profile_save_button'):
            self.parent.profile_save_button.clicked.connect(self.save_profile)
    
    def upload_profile_image(self):
        """Xử lý sự kiện click để upload ảnh mới"""
        print("Upload profile image clicked")
        
        # Tìm ra đối tượng nào được click (main photo hoặc sidebar photo)
        sender = self.sender()
        print(f"Sender: {sender}")
        
        if isinstance(sender, ClickableLabel):
            print(f"Detected ClickableLabel click: {sender}")
            # Mở dialog để chọn file bằng phương thức có sẵn trong ClickableLabel
            sender.open_file_dialog()
            file_path = sender.file_path
            print(f"Selected file path: {file_path}")
            
            if file_path and file_path.strip():
                self.uploaded_image_path = file_path
                
                # Load và hiển thị ảnh dưới dạng tròn
                pixmap = QPixmap(file_path)
                if not pixmap.isNull():
                    print(f"Loading pixmap from {file_path}, size: {pixmap.width()}x{pixmap.height()}")
                    # Tạo phiên bản tròn cho cả hai ảnh
                    rounded_pixmap_small = self.get_rounded_pixmap(pixmap, 60)  # Nhỏ cho sidebar
                    rounded_pixmap_large = self.get_rounded_pixmap(pixmap, 90)  # Lớn cho ảnh chính
                    
                    # Cập nhật cả hai ảnh
                    self.parent.profile_photo_label.setPixmap(rounded_pixmap_large)
                    self.parent.profile_photo_label.setScaledContents(True)
                    self.parent.profile_photo_label.setText("")
                    
                    self.parent.profilesidebar_photo_label.setPixmap(rounded_pixmap_small)
                    self.parent.profilesidebar_photo_label.setScaledContents(True)
                    self.parent.profilesidebar_photo_label.setText("")
                    
                    print(f"Image uploaded successfully: {file_path}")
                else:
                    print(f"Failed to load pixmap from {file_path}")
            else:
                print("No file path or file path is empty")
        else:
            print(f"Unknown sender type: {type(sender)}")

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
        # Load ảnh profile chính
        default_profile_path = "project/image/profile_icon.png"
        profile_pixmap = QPixmap(default_profile_path)
        if not profile_pixmap.isNull():
            print(f"Loading default profile image from {default_profile_path}")
            rounded_profile = self.get_rounded_pixmap(profile_pixmap, 90)
            self.parent.profile_photo_label.setPixmap(rounded_profile)
            self.parent.profile_photo_label.setScaledContents(True)
            self.parent.profile_photo_label.setText("")
        else:
            print(f"Failed to load default profile image from {default_profile_path}")
        
        # Load ảnh sidebar
        default_sidebar_path = "project/image/profile_panel_icon.png"
        sidebar_pixmap = QPixmap(default_sidebar_path)
        if not sidebar_pixmap.isNull():
            print(f"Loading default sidebar image from {default_sidebar_path}")
            rounded_sidebar = self.get_rounded_pixmap(sidebar_pixmap, 60)
            self.parent.profilesidebar_photo_label.setPixmap(rounded_sidebar)
            self.parent.profilesidebar_photo_label.setScaledContents(True)
            self.parent.profilesidebar_photo_label.setText("")
        else:
            print(f"Failed to load default sidebar image from {default_sidebar_path}")

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
                self.parent.profile_photo_label.setText("")
                
                self.parent.profilesidebar_photo_label.setPixmap(rounded_pixmap_small)
                self.parent.profilesidebar_photo_label.setScaledContents(True)
                self.parent.profilesidebar_photo_label.setText("")
            else:
                print("profile_photo_label or profilesidebar_photo_label not found in parent widget")
        else:
            print("Failed to load image from network reply") 