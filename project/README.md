# Developer Guide

## Windows
### Getting Started

1. Tải xuống và cài đặt [GTK+2 for Windows Runtime Environment](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/download/2022-01-04/gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe)

2. Tạo môi trường ảo (.venv) với Python 3.9. File-> Settings -> Add Interpreter-> Add Local Interpreter
3. ![Add_interpreter](doc_photo\img.jpg)
![setup .venv](doc_photo\setup_venv.jpg)

Tick chọn inherit packages from base interpreters

Trong môi trường  (.venv)
    
    Cập nhật pip bằng lệnh sau:
    python.exe -m pip install --upgrade pip

    Tải xuống và cài đặt PySide, PyQt6, pyQt6-tools, Custom Widgets::
    pip install PyQt6
    pip install PySide6
    pip install PyQt6-tools
    pip install QT-PyQt-PySide-Custom-Widgets

3. Fork dự án từ GitHub của Mỹ Linh nếu chưa Fork
https://github.com/mylinh130425/KTLT_K23416_Group2

```git clone``` fork repo của mình về máy nếu chưa clone về (chưa có thư mục KTL_K23416_group2 trong máy)

4. Mở dự án trong PyCharm và chạy ```main.py``` để kiểm tra xem mọi thứ có hoạt động không. Nhớ cài đặt Python Interpreter chỉa vào Python.exe trong môi trường .venv có Python 3.9 và các thư viện cần thiết trước khi chạy nếu chạy bằng PyCharm/VS Code. Còn chạy lệnh  ```python main.py``` thì nhớ activate (.venv) trước khi chạy


5. Mỗi lần trước khi code đều nhớ gõ ```git status```, nếu phát hiện code của Mỹ Linh có thay đổi mới so với code của mình thì  thì dùng ```git pull``` để đồng bộ với repo chính (Mỹ Linh), giải quyết các conflict trong máy, sau đó ngay lập tức ```git push``` lên fork repo cuẩ bản thân. 
> !!! Nếu chỉ làm bước này khi chuẩn bị tạo pull request bên repo chính (Mỹ Linh) thì sẽ phải giải quyết rất nhiều conflict cùng 1 lúc.

Thường xuyên ```git add .```, ```git commit -a -m ``` (ghi commit message rõ ràng cụ thể, nếu được thì 1 commit 1 chức năng/ update mới), ```git push``` để cập nhật fork của mình khi thay đổi file trong máy cá nhân


### Hướng dẫn lập trình:

1. Nhớ kiểm tra ```git status``` và đồng bộ với repo gốc, giải quyết conflict trước khi thay đổi code (bước 5 Getting Started)
2. Truy cập vào thư mục của dự án và đảm bảo là đang chạy Python interpreter trong đúng môi trường ảo ```.venv``` (Python 3.9, PyQt6, PySide6, PyQt6-tools, CustomWidgets). **Chạy `main.py`** để kiểm tra xem mọi thứ có hoạt động không.
3. **Mở dòng lệnh (command line/terminal) bên trong thư mục `project/` và chạy**:
   ```cmd
   Custom_Widgets --monitor-ui ui --qt-library PyQt6
   ```
   **Giữ cửa sổ command line/terminal này mở** trong khi chỉnh sửa giao diện UI bên trong Qt Designer để nó tự động cập nhật tệp `ui_interface.py`.
4. **Mở Qt Designer**, sau đó mở tệp `interface.ui` trong Qt Designer. **Tránh sử dụng "External tool" trong PyCharm** để mở tệp `.ui` vì nó có thể tiêu tốn quá nhiều RAM và làm PyCharm crash.
5. **Bắt đầu thiết kế/lập trình giao diện trong Qt Designer.** Nhớ thường xuyên lưu lại và git commit với thông điệp có ý nghĩa.


### Hướng dẫn dùng Widget 

### Sử dụng các Widget hiện đại trong thư viện Custom Widget
> Hiện project đã được setup để hoàn toàn tương thích với thư viện [Custom Widget](https://khamisikibet.github.io/Docs-QT-PyQt-PySide-Custom-Widgets/docs/widgets), nên hãy tự do khám phá các widget trong đây và lựa chọn cái phù hợp để áp dụng vào thiết kế.
>
> Hãy xem kỹ hướng dẫn cho mỗi thành phần vì chúng đều khác nhau. 
> 
!!! Chú ý file interface.ui chưa được setup với bất kỳ thành phần nào trong thư viện mà hoàn toàn thuần thúy tạo bởi các thành phần có sẵn của PyQt6.

#### Hướng dẫn sử dụng các thành phần trong Custom Widget


### Chỉnh SCSS cho các thành phần
1. Copy tên của thành phần trong Qt Designer 
2. Mở ```Qss/scss/defaultStyle.css```. Dán ```#<tên thành phần>{}``` vào như mẫu có sẵn trong file này
3. Thêm các thuộc tính mới dựa trên [Style Sheet reference](https://doc.qt.io/qt-6/stylesheet-reference.html), chú ý danh sách thuộc tính bên tay phải
![Style Sheet reference](doc_photo/Pasted image 20250218010439.png)
4. Riêng giá trị cho màu sắc bao gồm tên tiếng Anh và chuỗi rgb vd: white, #fff, #ffffff, rgb(255,255,255) đều là màu trắng
5. Cần thử nghiệm xem các đơn vị nào của CSS áp dụng được trong QSS/scss. Hiện tại ```px``` là đơn vị chắc chắn áp dụng được

### File Structure 

**Description:**

- **README.md:** Description of the project.
- **requirements.txt:** List of Python dependencies required for the project.
- **main.py:** Entry point of the application.
- **ui/:** Directory containing UI-related files.
    - **main_window.ui:** Main window layout file.
    - Other UI-related files.
- **src/:** Source code directory.
    - **_\_init__.py:** Package initialization file.
    - **utils.py:** Utility functions.
    - **helper_functions.py:** Additional helper functions.
    - **ui_main_window.py:** Automatically generated Python code from main_window.ui.
- **qss/:** Directory for Qt Style Sheets (QSS) and icons.
    - **scss/:** SCSS files for styling.
    - **icons/:** Icon images.
- **logs/:** Directory for log files.
    - **custom_widgets.log:** Log file.
- **json_styles/:** Directory for JSON style files.
-   **style.json:** Example JSON style file.
- **generated-files/:** Directory for files auto-generated by the custom widgets module.
    - Example generated files include **UI's** and **JSon** files

This structure allows for automatic conversion of UI files to Python code and placement within the src folder, simplifying the development process for users.

For more, visit https://github.com/KhamisiKibet/QT-PyQt-PySide-Custom-Widgets


### Installation Guide:

1. Download and install [GTK+2 for Windows Runtime Environement - fix for cairo-2](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
2. Create a .venv with Python 3.9 (in the picture it shows 3.8 because I have already installed Python 3.9)
![setup .venv](doc_photo/Pasted image 20250217193556.png)
3. update pip
```
python.exe -m pip install --upgrade pip
```
4. Download and install PySide, PyQt6
```cmd
pip install PyQt6
pip install PySide6
```
5. Download and install pyQt6-tools
```bash
pip install PyQt6-tools
```
6. Download and install Custom Widgets:
```cmd
pip install QT-PyQt-PySide-Custom-Widgets
```
7. pull the project from github and go to the directory of the project
8. Inside the ```project/``` folder, open command line/ terminal and run
```cmd
Custom_Widgets --monitor-ui ui --qt-library PyQt6
```
Keep this command line open while you change the UI inside Qt Designer so it may autoamtically update the generated ```ui_interface.py``` file for you
9. Open Qt Designer and open file ui_interface inside Qt Designer. Try NOT to use "External tool" inside PyCharm to open ui file with Qt Designer as it may use too much Ram and cause PyCharm to crash.
10. Open the project in PyCharm and run ```main.py``` to check if everything works
11. Start Designing/Coding your Screen inside the QtDesigner. Remember to save often.

### Required packages
Check your libraries with ```pip list```. Currently, the following libraries and versions are enough to get the code running on Windows 11.

| Package                       | Version   |
|-------------------------------|-----------|
| cairocffi                     | 1.7.1     |
| CairoSVG                      | 2.7.1     |
| cffi                          | 1.17.1    |
| contourpy                     | 1.3.0     |
| cssselect2                    | 0.7.0     |
| cycler                        | 0.12.1    |
| defusedxml                    | 0.7.1     |
| fonttools                     | 4.56.0    |
| importlib_resources           | 6.5.2     |
| kids.cache                    | 0.0.7     |
| kiwisolver                    | 1.4.7     |
| libsass                       | 0.23.0    |
| lxml                          | 5.3.1     |
| matplotlib                    | 3.9.4     |
| mock                          | 5.1.0     |
| numpy                         | 2.0.2     |
| packaging                     | 24.2      |
| perlin-noise                  | 1.13      |
| pillow                        | 11.1.0    |
| pip                           | 25.0.1    |
| pycparser                     | 2.22      |
| pyparsing                     | 3.2.1     |
| PyQt6                         | 6.8.1     |
| PyQt6-Qt6                     | 6.8.2     |
| PyQt6_sip                     | 13.10.0   |
| PySide6                       | 6.8.2.1   |
| PySide6_Addons                | 6.8.2.1   |
| PySide6_Essentials            | 6.8.2.1   |
| python-dateutil               | 2.9.0.post0 |
| QT-PyQt-PySide-Custom-Widgets | 1.0.2     |
| QtPy                          | 2.4.3     |
| qtsass                        | 0.4.0     |
| setuptools                    | 68.2.0    |
| shiboken6                     | 6.8.2.1   |
| six                           | 1.17.0    |
| termcolor                     | 2.5.0     |
| tinycss2                      | 1.4.0     |
| watchdog                      | 6.0.0     |
| webencodings                  | 0.5.1     |
| wheel                         | 0.41.2    |
| zipp                          | 3.21.0    |
