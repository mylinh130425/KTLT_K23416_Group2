from PyQt6.QtWidgets import QMessageBox
from pymongo import MongoClient

class SignupHandler:
    def __init__(self, ui):
        self.ui = ui
        self.client = MongoClient("mongodb://localhost:27017/")  # Update if needed
        self.db = self.client["mealmatch"]  # Change this to your database name
        self.users_collection = self.db["Users"]

        # Connect the signup button to the signup function
        self.ui.signup_button.clicked.connect(self.signup)

    def signup(self):
        full_name = self.ui.full_name_lineEdit.text().strip()
        username = self.ui.signup_username_lineEdit.text().strip()
        email = self.ui.signup_email_lineEdit.text().strip()
        password = self.ui.signup_password_lineEdit.text().strip()

        # Check for empty fields
        if not full_name or not username or not email or not password:
            QMessageBox.warning(self.ui, "Signup Failed", "All fields are required.")
            return

        # Check if username or email already exists
        if self.users_collection.find_one({"username": username}):
            QMessageBox.warning(self.ui, "Signup Failed", "Username already exists.")
            return

        if self.users_collection.find_one({"email": email}):
            QMessageBox.warning(self.ui, "Signup Failed", "Email already in use.")
            return

        # Create user document
        user_data = {
            "username": username,
            "email": email,
            "password": password,  # Storing plain text password (not recommended)
            "fullName": full_name,
            "avatar": "",  # Default avatar URL or empty
            "role": "user",
            "createdAt": self.db.command("serverStatus")["localTime"],
            "statistics": {
                "history_view": {"restaurant": [], "menu_item": []},
                "past_review": {"restaurant": [], "menu_item": []}
            }
        }

        # Insert into MongoDB
        self.users_collection.insert_one(user_data)

        # Show success message
        return QMessageBox.information(self.ui, "Signup Successful", "Account created successfully!")
