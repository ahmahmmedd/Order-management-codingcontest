class User:
    def __init__(self,username, password, role):
        self._username = username
        self._password = password
        self._role = role

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
            self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if value in ["Admin", "User"]:
            self._role = value
        else:
            raise ValueError("Role must be either 'Admin' or 'User'")

    def __str__(self):
        return f"User ID: {self.user_id}, Username: {self.username}, Role: {self.role}"