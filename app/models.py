class Comments:
    def __init__(self, _id=str(), name=str(), email=str(), movie_id=str(), comment_type=str(), date=str()):
        self._id = _id
        self.name = name
        self.email = email
        self.movie_id = movie_id
        self.comment_type = comment_type
        self.date = date


class Users:
    def __init__(self, _id=str(), name=str(), email=str(), password=str()):
        self._id = _id
        self.name = name
        self.email = email
        self.password = password


class Response:
    def __init__(self, _id=str()) -> None:
        self._id = _id
