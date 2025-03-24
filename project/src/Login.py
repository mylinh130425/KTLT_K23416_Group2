from PyQt6.QtWidgets import QMessageBox
from pymongo import MongoClient
from datetime import datetime

class LoginHandler:
    def __init__(self, ui):
        self.ui = ui
        self.client = MongoClient("mongodb://localhost:27017/")  # Update if needed
        self.db = self.client["mealmatch"]  # Change this to your database name
        self.users_collection = self.db["users"]

        # Connect the login button to the login function
        self.ui.login_button.clicked.connect(self.login)

    def login(self):
        username_or_email = self.ui.login_username_lineEdit.text().strip()
        password = self.ui.login_password_lineEdit.text().strip()

        # 1. Check for empty fields
        if not username_or_email or not password:
            QMessageBox.warning(self.ui, "Login Failed", "All fields are required.")
            return

        # 2. Find user by username or email
        user = self.users_collection.find_one({
            "$or": [
                {"username": username_or_email},
                {"email": username_or_email}
            ]
        })

        if not user:
            QMessageBox.warning(self.ui, "Login Failed", "User not found.")
            return

        # 3. Check password (plain text comparison)
        if user["password"] != password:
            QMessageBox.warning(self.ui, "Login Failed", "Incorrect password.")
            return

        # 4. Update last login timestamp
        self.users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"lastLogin": datetime.utcnow()}}
        )

        # 5. Show success message
        return QMessageBox.information(self.ui, "Login Successful", f"Welcome back, {user['fullName']}!")
