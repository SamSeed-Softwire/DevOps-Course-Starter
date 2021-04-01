from flask_login import current_user

class UserViewModel:

    def __init__(self, users):
        self._users = users


    # Properties

    @property
    def all_except_current_user(self):
        users = [user for user in self._users if user.id != current_user.id]
        return sorted(users, key = lambda user: user.id)

    @property
    def current_user(self):
        return current_user