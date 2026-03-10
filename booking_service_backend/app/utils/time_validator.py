import datetime

class FutureTimeValidator:

    def __init__(self, date: datetime.datetime = None):
        if date is None:
            self.date = datetime.datetime.now()
        

    def __set_name__(self, obj_type, name):
        self.name = name
        self.private_name = '_' + name


    def __get__(self, obj, obj_type=None):
        if obj is None:
            return self
        
        return getattr(obj_type, self.private_name, None)
    

    def __set__(self, obj, value):
        if value <= self.date:
            raise ValueError(f"Invalid '{self.private_name}' date.")
        
        setattr(obj, self.private_name, value)