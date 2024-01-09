from .rule import Rule
from .predicate import Predicate

class DatalogProgram:
    def __init__(self):
        self.schemes: list[Predicate] = []
        self.facts: list[Predicate] = []
        self.rules: list[Rule] = []
        self.queries: list[Predicate] = []

    def new_rule(self, name) -> None:
        self.rules.append(Rule(name))
    
    def new_pred(self, type, name) -> None:
        if type == "scheme":
            self.schemes.append(Predicate(name))
        elif type == "fact":
            self.facts.append(Predicate(name))
        elif type == "rule":
            self.rules[-1].add_pred(name)
            pass
        elif type == "query":
            self.queries.append(Predicate(name))
        else:
            print(f"Invalid new DatalogProgram type: {type}")
        
    def add_param_to(self, type, param) -> None:
        if type == "scheme":
            self.schemes[-1].add_param(param)
        elif type == "fact":
            self.facts[-1].add_param(param)
        elif type == "rule":
            self.rules[-1].add_param(param)
        elif type == "query":
            self.queries[-1].add_param(param)
        else:
            print(f"Invalid current DatalogProgram type: {type}")

    def to_string(self) -> str:
        domain: list[str] = []
        for fact in self.facts:
            for param in fact.parameters:
                param_string = param.to_string()
                if param_string not in domain:
                    domain.append(param_string)
        domain.sort()

        output = f"Schemes({len(self.schemes)}):"
        for scheme in self.schemes:
            output += f"\n  {scheme.to_string()}"

        output += f"\nFacts({len(self.facts)}):"
        for fact in self.facts:
            output += f"\n  {fact.to_string()}."

        output += f"\nRules({len(self.rules)}):"
        for rule in self.rules:
            output += f"\n  {rule.to_string()}."

        output += f"\nQueries({len(self.queries)}):"
        for query in self.queries:
            output += f"\n  {query.to_string()}?"

        output += f"\nDomain({len(domain)}):"
        for string in domain:
            output += f"\n  {string}"
        
        return output
