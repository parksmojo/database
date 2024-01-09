from .predicate import Predicate

class Rule:
    def __init__(self, name) -> None:
        self.head_predicate: Predicate = Predicate(name)
        self.body_predicates: list[Predicate] = []

    def add_pred(self, name) -> None:
        self.body_predicates.append(Predicate(name))

    def add_param(self, param) -> None:
        if len(self.body_predicates) == 0:
            self.head_predicate.add_param(param)
        else:
            self.body_predicates[-1].add_param(param)
    
    def to_string(self) -> str:
        output = ""
        pred_strings = []
        
        for pred in self.body_predicates:
            pred_strings.append(pred.to_string())
        output = f"{self.head_predicate.to_string()} :- {','.join(pred_strings)}"
        return output
