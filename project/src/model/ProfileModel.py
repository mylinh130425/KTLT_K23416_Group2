from PyQt6.QtCore import pyqtSignal, QObject
from project.src.model.UserModel import UserModel

class ProfileModel(QObject):
    profileUpdated = pyqtSignal(str)  # Emits username when profile is updated
    profileDeleted = pyqtSignal()  # Emits when user is deleted
    errorOccurred = pyqtSignal(str)  # Emits error messages

    def __init__(self, database, username):
        """Initialize ProfileDelegate with a database instance from ProfileScreen."""
        super().__init__()
        self.database = database  # Pass database from ProfileScreen
        self.current_user = None
        print("saved current user", self.load_profile(username))

    def load_profile(self, username: str):
        """Load user details from the database"""
        user_data = self.database.users.find_one({"username": username})

        if user_data:
            self.current_user = UserModel(
                user_data["username"],
                user_data["fullName"],
                user_data["passwordHash"],
                is_hashed=True
            )
            return True
                # {
                # "username": self.current_user.username,
                # "fullname": self.current_user.fullname
            # }
        else:
            # self.errorOccurred.emit("❌ User not found!")
            print("❌ User not found!")
            return False

    def update_profile(self, old_username: str, new_username: str, new_fullname: str, current_password: str, new_password: str, confirm_password: str):
        """Update user profile details"""
        if not self.current_user:
            # self.errorOccurred.emit("❌ No user loaded!")
            error= "❌ No user loaded!"
            print(error)
            return False, error

        if not self.current_user.verify_password(current_password):
            # self.errorOccurred.emit("❌ Incorrect current password!")
            error= "❌ Incorrect current password!"
            print(error)
            return False, error

        if new_password and new_password != confirm_password:
            error="❌ New passwords do not match!"
            print(error)
            # self.errorOccurred.emit("❌ New passwords do not match!")
            return False, error

        update_data = {"username": new_username, "fullName": new_fullname}
        if new_password:
            update_data["passwordHash"] = UserModel.hash_password(new_password)

        result = self.database.users.update_one({"username": old_username}, {"$set": update_data})

        if result or result.modified_count > 0:
            # self.profileUpdated.emit(new_username)  # Notify UI
            print("Profile updated: ", self.load_profile(new_username))
            status="update successfully"
            return True, status

        else:
            # self.errorOccurred.emit("⚠️ No changes made!")
            status ="⚠️ No changes made!"
            print(status)
            return False,status

    def delete_profile(self, username: str):
        """Delete user from the database"""
        if not self.current_user:
            # self.errorOccurred.emit("❌ No user loaded!")
            print("❌ No user loaded!")
            return False

        result = self.database.users.delete_one({"username": username})

        if result or result.deleted_count > 0:
            # self.profileDeleted.emit()  # Notify UI to navigate away
            print("✅ User deleted!")
            return True
        else:
            # self.errorOccurred.emit("❌ Failed to delete user!")
            print("❌ Failed to delete user!")
            return False
