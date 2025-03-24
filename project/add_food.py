import json
from pymongo import MongoClient

# 1. Kết nối với MongoDB (local hoặc Atlas)
try:
    # Kết nối với MongoDB local (localhost:27017)
    client = MongoClient('localhost', 27017)

    # Kiểm tra kết nối
    client.admin.command('ping')
    print("Kết nối MongoDB thành công!")

except Exception as e:
    print(f"Lỗi kết nối MongoDB: {e}")
    exit()

# 2. Chọn database và collection
db = client['MealMatch']  # Database "MealMatch"
collection = db['Menu']  # Collection "Menu"

# 3. Đọc file JSON
json_file = "menu_data.json"  # Thay bằng đường dẫn file JSON của bạn

try:
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 4. Đẩy dữ liệu vào MongoDB
    if isinstance(data, list):  # Nếu file JSON là mảng (nhiều document)
        result = collection.insert_many(data)
        print(f"Đã đẩy {len(result.inserted_ids)} document vào collection 'Menu'.")
    elif isinstance(data, dict):  # Nếu file JSON là object (một document)
        result = collection.insert_one(data)
        print(f"Đã đẩy 1 document vào collection 'Menu'.")
    else:
        print("Định dạng JSON không hợp lệ!")

except FileNotFoundError:
    print(f"Không tìm thấy file: {json_file}")
except json.JSONDecodeError as e:
    print(f"Lỗi phân tích JSON: {e}")
except Exception as e:
    print(f"Lỗi đẩy dữ liệu vào MongoDB: {e}")

# 5. Đóng kết nối
client.close()
print("Đã đóng kết nối MongoDB.")