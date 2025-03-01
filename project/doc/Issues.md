# FAQs

## Qt Designer and pyuic

1. Trong quá trình chỉnh sửa ```.ui``` files, nếu mở trực tiếp Qt Designer từ PyCharm hoặc double click file này để mở thì QtDesigner sẽ thêm những QtFlag vào trong 1 số giá trị của tag liên quan đến layout trong file ui gây ra lỗi khi pyuic tạo ra file ```py``` tương ứng tự động.

> **Giải pháp**
>
> Mở Qt Designer trước rồi mới dùng chức năng Open để mở file ui

## Blocking bugs
1. Chỉ mới thiết kế 3/4 số giao diện cần thiết mà đã cần tới gần 2gb ram để chạy file main trong dev mode, khả năng tràn bộ nhớ là rất cao. Hiện chạy file ```main.py``` rất lâu nhưng không thấy cửa sổ ứng dụng xuất hiện. Cần debug thử xem chỉ là tràn ram hay có lỗi trong file ui