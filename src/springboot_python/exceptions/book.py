from springboot_python.exceptions.base import Conflict, NotFound

class BookNotFound(NotFound):
    def __init__(self) -> None:
        detail = "Book with the given id doesn't exist" 
        super().__init__(detail)

class BookLinkedToAnotherObject(Conflict):
    def __init__(self) -> None:
        detail = "Book is linked to another object and can't be deleted"
        super().__init__(detail)