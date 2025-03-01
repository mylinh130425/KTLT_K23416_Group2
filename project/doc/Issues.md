# Tool Issues

## Qt Designer and pyuic

1. Trong quá trình chỉnh sửa ```.ui``` files, nếu mở trực tiếp Qt Designer từ PyCharm hoặc double click file này để mở thì QtDesigner sẽ thêm những QtFlag vào trong 1 số giá trị của tag liên quan đến layout trong file ui gây ra lỗi khi pyuic tạo ra file ```py``` tương ứng tự động.

> **Giải pháp**
>
> Mở Qt Designer trước rồi mới dùng chức năng Open để mở file ui
