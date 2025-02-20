from springboot_python.exceptions.base import Conflict, NotFound

class StudentNotFound(NotFound):
    def __init__(self) -> None:
        detail = "Student with the given id doesn't exist" 
        super().__init__(detail)

class StudentLinkedToAnotherObject(Conflict):
    def __init__(self) -> None:
        detail = "Student is linked to another object and can't be deleted"
        super().__init__(detail)