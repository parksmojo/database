class Parameter:
    def __init__(self, value):
        self.value: str = value

    def is_id(self) -> bool:
        if self.value[0] == '\'':
            return False
        else:
            return True
    
    def to_string(self) -> str:
        return self.value
