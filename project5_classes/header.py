class Header:
    def __init__(self, values: list[str]) -> None:
        self.values: list[str] = values
    
    def __str__(self) -> str:
        return f"{', '.join(self.values)}"