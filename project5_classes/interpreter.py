from .database import Database
from .relation import Relation
from .row import Row
from .header import Header
from typing import Dict
from .previous_classes.datalogprogram import DatalogProgram
from .previous_classes.rule import Rule
from .previous_classes.predicate import Predicate
from .graph import Graph
import copy


class Interpreter:
    def __init__(self) -> None:
        self.output_str: str = ""
        self.database: Database = Database()
    
    def run(self, datalog_program: DatalogProgram) -> str:
        self.datalog_program: DatalogProgram = datalog_program
        self.interpret_schemes()
        self.interpret_facts()
        self.interpret_rules()
        self.interpret_queries()
        return self.output_str
    
    def interpret_schemes(self) -> None:
        for scheme in self.datalog_program.schemes:
            parameters: list[str] = []
            for param in scheme.parameters:
                parameters.append(param.to_string())
            self.database.relations[scheme.name] = Relation(scheme.name, Header(parameters))      
    
    def interpret_facts(self) -> None:
        for fact in self.datalog_program.facts:
            parameters: list[str] = []
            for param in fact.parameters:
                parameters.append(param.to_string())
            self.database.relations.get(fact.name).add_row(Row(parameters))
    
    def interpret_queries(self) -> None:
        queries: list[Predicate] = self.datalog_program.queries
        self.output_str += "\nQuery Evaluation\n"
        for query in queries:
            answer: Relation = self.evaluate_predicate(query)
            self.output_str += query.to_string()
            self.output_str += "? "
            if len(answer.rows) == 0:
                self.output_str += "No"
            else:
                self.output_str += f"Yes({len(answer.rows)})"
            self.output_str += '\n'
            self.output_str += f"{self.evaluate_predicate(query)}"

    
    def evaluate_predicate(self, pred: Predicate) -> Relation:
        rel: Relation = copy.deepcopy(self.database.relations[pred.name])
        var: list[str] = []
        col: list[int] = []

        #print(rel.__str__())
        for i in range(len(pred.parameters)):
            curr_param = pred.parameters[i]
            #print(f"[{i}] = {curr_param.to_string()}")
            if curr_param.is_id():
                if curr_param.to_string() in var:
                    rel = rel.select2(col[var.index(curr_param.to_string())], i)
                else:
                    var.append(curr_param.to_string())
                    col.append(i)
            else:
                rel = rel.select1(curr_param.to_string(), i)
            #print(rel.__str__())

        #print(f"projecting, vars: {col}")
        rel = rel.project(col)
        #print(rel.__str__())
        #print(f"renaming, cols: {var}")
        rel = rel.rename(Header(var))
        #print(rel.__str__())
        return rel
    
    def interpret_rules(self) -> None:
        graph: Graph = Graph(len(self.datalog_program.rules))

        for rulex in self.datalog_program.rules:
            for child in rulex.body_predicates:
                for ruley in self.datalog_program.rules:
                    if child.name == ruley.head_predicate.name:
                        x = self.datalog_program.rules.index(rulex)
                        y = self.datalog_program.rules.index(ruley)
                        graph.mk_edge(x,y)
        graph.mk_reverse_graph()
        sccs: list[list[int]] = graph.find_sccs()

        self.output_str += "Dependency Graph\n"
        self.output_str += f"{graph.to_string()}\n"
        self.output_str += "Rule Evaluation\n"
        for scc in sccs:
            self.output_str += f"SCC: "
            scc_rules = ""
            sep = ""
            for x in sorted(scc):
                scc_rules += sep
                scc_rules += f"R{x}"
                sep = ","
            self.output_str += f"{scc_rules}\n"

            run_fixed_point = True
            if len(scc) == 1:
                for pred in self.datalog_program.rules[scc[0]].body_predicates:
                    if pred.name == self.datalog_program.rules[scc[0]].head_predicate.name:
                        run_fixed_point = True
                        break
                    else:
                        run_fixed_point = False

            passes = 0
            if run_fixed_point:
                changed = True
                while(changed):
                    passes += 1
                    changed = False
                    for rule_num in sorted(scc):
                        self.output_str += f"{self.datalog_program.rules[rule_num].to_string()}.\n"
                        if self.evaluate_rule(self.datalog_program.rules[rule_num]) > 0:
                            changed = True
            else:
                passes = 1
                self.output_str += f"{self.datalog_program.rules[scc[0]].to_string()}.\n"
                self.evaluate_rule(self.datalog_program.rules[scc[0]])
            self.output_str += f"{passes} passes: {scc_rules}\n"
    
    def evaluate_rule(self, rule: Rule) -> int:
        # print(f"evaluating a rule: {rule.to_string()}\n")
        base_rel: Relation = self.database.relations[rule.head_predicate.name]

        evaluated_relations: list[Relation] = []
        for body_predicate in rule.body_predicates:
            evaluated_relations.append(self.evaluate_predicate(body_predicate))
        # print(f"Step 1 Relations:")
        # for rel in evaluated_relations: print(rel)
        # print()

        #TODO: check for an empty list?
        result: Relation = evaluated_relations.pop(0)
        # print(f"initial result:\n{result}")
        if len(evaluated_relations) != 0:
            for rel in evaluated_relations:
                result = result.natural_join(rel)
        # print(f"Step 2 relation:\n{result}\n")

        col: list[int] = []
        params: list[str] = []
        for param in rule.head_predicate.parameters:
            params.append(param.to_string())
        # print(result.header.values)
        # print(params)
        for i in range(len(params)):
            if params[i] in result.header.values:
                col.append(result.header.values.index(params[i]))
        result = result.project(col)
        # print(col)
        # print(f"Step 3 relation:\n{result}\n")

        result = result.rename(base_rel.header)
        # print(f"final result:\n{result}")

        # print(f"original relation:\n{base_rel}")
        size_before: int = len(base_rel.rows)
        self.output_str += base_rel.union(result)
        size_after: int = len(base_rel.rows)
        size_diff = size_after - size_before
        # print(f"New Relation: {size_after - size_before} added rows\n{base_rel}")
        
        return size_diff