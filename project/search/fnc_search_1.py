from pymongo import MongoClient, errors

# Kết nối tới MongoDB server
try:
    client = MongoClient('mongodb://localhost:27017/MealMatch', serverSelectionTimeoutMS=5000)
    client.server_info()  # Kích hoạt lỗi nếu không kết nối được
    print("Kết nối thành công tới MongoDB server")
except errors.ServerSelectionTimeoutError as e:
    print(f"Lỗi kết nối tới MongoDB: {e}")
    client = None

if client:
    # Chọn database và collection
    db = client['MealMatch']  # Tên database
    collection = db['Restaurants']  # Tên collection

    # Hàm tìm kiếm nhà hàng dựa trên nhiều giá trị
    def search_restaurant(keyword):
        try:
            # Tìm kiếm trong collection với điều kiện regex (không phân biệt hoa thường)
            results = collection.find({
                "$or": [
                    {"name": {"$regex": keyword, "$options": "i"}},
                    {"description": {"$regex": keyword, "$options": "i"}},
                    {"address": {"$regex": keyword, "$options": "i"}},
                    {"phone": {"$regex": keyword, "$options": "i"}},
                    {"price_range": {"$regex": keyword, "$options": "i"}}
                ]
            })
            return list(results)
        except errors.PyMongoError as e:
            print(f"Lỗi khi tìm kiếm nhà hàng: {e}")
            return []

    # Ví dụ sử dụng hàm tìm kiếm
    search_keyword = input("Nhập từ khóa để tìm kiếm nhà hàng (ví dụ: 'Gỏi Gì'): ")
    results = search_restaurant(search_keyword)

    # Hiển thị kết quả
    if results:
        print(f"Kết quả tìm kiếm cho '{search_keyword}':")
        for result in results:
            print(f"- Tên: {result['name']}")
            print(f"  Mô tả: {result.get('description', 'Không có')}")
            print(f"  Địa chỉ: {result.get('address', 'Không có')}")
            print(f"  Điện thoại: {result.get('phone', 'Không có')}")
            print(f"  Giá: {result.get('price_range', 'Không có')}")
    else:
        print(f"Không tìm thấy nhà hàng nào với từ khóa '{search_keyword}'.")

    # Đóng kết nối
    client.close()
