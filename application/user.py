from flask_login import UserMixin

from application.valid_roles import ValidRoles

class User(UserMixin):

    def __init__(self, id, role = "reader"):
        self.id = id
        self.role = role


    # Properties

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, new_role):
        if new_role not in ValidRoles.__members__:
            raise ValueError(f"""'{new_role}' is not a valid role! Acceptable choices are {[role for role in ValidRoles.__members__]}.""")
        else:
            self._role = new_role