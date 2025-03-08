from pymongo import MongoClient


def connect_db():
    """Kết nối tới MongoDB server và trả về collection."""
    client = MongoClient('mongodb://localhost:27017/')
    db = client['MealMatch']  # Database
    return db['Restaurants']  # Collection


def search_restaurant(name=None, address=None, cuisine=None, price_range=None, min_rating=None):
    """Tìm kiếm nhà hàng theo nhiều tiêu chí."""
    collection = connect_db()
    query = {}

    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if address:
        query["address"] = {"$regex": address, "$options": "i"}
    if cuisine:
        query["cuisine"] = {"$regex": cuisine, "$options": "i"}
    if price_range:
        query["price_range"] = price_range  # Tìm chính xác theo mức giá
    if min_rating:
        query["rating"] = {"$gte": min_rating}  # Tìm các nhà hàng có đánh giá lớn hơn hoặc bằng

    results = collection.find(query)
    return list(results)


# Nhập thông tin tìm kiếm từ người dùng
name = input("Nhập tên nhà hàng (hoặc bỏ qua): ").strip()
address = input("Nhập địa chỉ (hoặc bỏ qua): ").strip()
cuisine = input("Nhập loại món ăn (hoặc bỏ qua): ").strip()
price_range = input("Nhập mức giá (ví dụ: '$', '$$', '$$$') hoặc bỏ qua: ").strip()
min_rating = input("Nhập đánh giá tối thiểu (1-5) hoặc bỏ qua: ").strip()
min_rating = float(min_rating) if min_rating else None

# Tìm kiếm nhà hàng phù hợp
results = search_restaurant(name, address, cuisine, price_range, min_rating)

# Hiển thị kết quả
if results:
    print("\nKết quả tìm kiếm:")
    for res in results:
        print(f"- Tên: {res.get('name', 'Không có')}")
        print(f"  Mô tả: {res.get('description', 'Không có')}")
        print(f"  Địa chỉ: {res.get('address', 'Không có')}")
        print(f"  Loại món ăn: {res.get('cuisine', 'Không có')}")
        print(f"  Giá: {res.get('price_range', 'Không có')}")
        print(f"  Đánh giá: {res.get('rating', 'Không có')}")
        print("-------------------------------------")
else:
    print("Không tìm thấy nhà hàng phù hợp.")
