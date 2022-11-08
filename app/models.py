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
    def __init__(self, report_name=str(), status=str(), date=str()) -> None:
        self.report_name = report_name
        self.status = status
        self.date = date


class CreateResponse:
    def __init__(self, _id=str()):
        self._id = _id


class ResponseMetadata:
    def __init__(self, next=str(), previous=str(), has_next=False, has_previous=False) -> None:
        self.has_next = has_next
        self.has_previous = has_previous
        self.previous = previous
        self.next = next


class PaginatedResponse:
    def __init__(self, data=list, metadata=dict):
        self.data = data
        self.metadata = metadata
