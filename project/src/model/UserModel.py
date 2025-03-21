import datetime

import bcrypt


class UserModel:
    AVATAR_URL = "https://wallpapers.com/images/high/anime-profile-picture-jioug7q8n43yhlwn.jpg"
    def __init__(self, username: str, fullname: str, password: str, is_hashed=False):
        self.username = username
        self.fullname = fullname
        if is_hashed:
            self.password_hash = password  # Already hashed from DB
        else:
            self.password_hash = self.hash_password(password)  # Hash when registering

    @staticmethod
    def hash_password(password: str) -> str:
        """Mã hóa mật khẩu với bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """Xác thực mật khẩu đã nhập với mật khẩu đã lưu"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self):
        """Chuyển đổi dữ liệu thành dict để lưu vào MongoDB"""
        return {
            "username": self.username,
            "email":"",
            "passwordHash": self.password_hash,
            "fullName": self.fullname,
            "avatar":UserModel.AVATAR_URL,
            "role": "user",
            "createdAt": datetime.datetime.now(),
            "lastLogin": datetime.datetime.now(),
            "statistics": {
                "history_view":{
                    "restaurant":[],
                    "menu_item":[]
                },
                "past_review":{
                    "review":[],
                    "menu_item":[],
                }
            }
        }
