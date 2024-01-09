from .parameter import Parameter

class Predicate:
    def __init__(self, name):
        self.parameters: list[Parameter] = []
        self.name: str = name

    def add_param(self, param: str):
        self.parameters.append(Parameter(param))
    
    def to_string(self) -> str:
        param_strings = []
        for param in self.parameters:
            param_strings.append(param.to_string())
        output = f"{self.name}({','.join(param_strings)})"
        return output
