from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id, role = "reader"):
        self.id = id
        self.role = role

    valid_roles = ['admin', 'reader', 'writer']


    # Properties

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, new_role):
        if new_role not in self.valid_roles:
            raise ValueError(f"""'{new_role}' is not a valid role! Acceptable choices are {[role for role in self.valid_roles]}.""")
        else:
            self._role = new_role