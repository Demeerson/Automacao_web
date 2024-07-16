class UserModel:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

class DateRangeModel:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date
