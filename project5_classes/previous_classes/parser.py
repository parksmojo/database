from typing import Callable as function
from .token import Token
from .datalogprogram import DatalogProgram
from .parameter import Parameter
from .predicate import Predicate
from .rule import Rule

class Parser:
    def __init__(self):
        pass

    def run(self, tokens: list[Token]) -> DatalogProgram:
        #print("running")
        self.tokens = tokens
        self.index = 0
        self.data_pro: DatalogProgram = DatalogProgram()
        self.curr_type: str = "None"

        try:
            self.parse_datalog_program()
        except ValueError as ve:
            print(f"Failure!\n  {ve}")

        return self.data_pro

    def reset(self) -> None:
        self.index = 0
        self.tokens.clear()

    def throw_error(self):
        if self.index >= len(self.tokens):
            self.index = self.index - 1
        raise ValueError(f"{self.get_current_token().to_string()}")

    def get_current_token(self) -> Token:
        #print("getting current token")
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        else:
            self.throw_error()

    def get_prev_token_value(self) -> str:
        return self.tokens[self.index - 1].value

    def advance(self) -> None:
        #print("advancing")
        if self.index < len(self.tokens):
            self.index += 1
        else:
            self.throw_error()

    def match(self, target_token: str) -> None:
        #print("matching")
        current_token = self.get_current_token().token_type
        if current_token == target_token:
            #print(f"Matched: {current_token}")
            self.advance()
        else:
            self.throw_error()

    # datalogProgram -> SCHEMES COLON scheme schemeList FACTS COLON factList RULES COLON ruleList QUERIES COLON query queryList EOF       
    def parse_datalog_program(self) -> None:
        self.match("SCHEMES")
        self.match("COLON")
        self.parse_scheme()
        self.parse_scheme_list()
        self.match("FACTS")
        self.match("COLON")
        self.parse_fact_list()
        self.match("RULES")
        self.match("COLON")
        self.parse_rule_list()
        self.match("QUERIES")
        self.match("COLON")
        self.parse_query()
        self.parse_query_list()
        self.match("EOF")

    # schemeList	->	scheme schemeList | lambda
    def parse_scheme_list(self) -> None:
        if self.get_current_token().token_type != "FACTS":
            self.parse_scheme()
            self.parse_scheme_list()
        else:
            return

    # factList	->	fact factList | lambda
    def parse_fact_list(self) -> None:
        if self.get_current_token().token_type != "RULES":
            self.parse_fact()
            self.parse_fact_list()
        else:
            return

    # ruleList	->	rule ruleList | lambda
    def parse_rule_list(self) -> None:
        if self.get_current_token().token_type != "QUERIES":
            self.parse_rule()
            self.parse_rule_list()
        else:
            return

    # queryList	->	query queryList | lambda
    def parse_query_list(self) -> None:
        if self.get_current_token().token_type != "EOF":
            self.parse_query()
            self.parse_query_list()
        else:
            return

    # scheme   	-> 	ID LEFT_PAREN ID idList RIGHT_PAREN
    def parse_scheme(self) -> None:
        self.curr_type = "scheme"
        self.match("ID")
        self.data_pro.new_pred(self.curr_type, self.get_prev_token_value())
        self.match("LEFT_PAREN")
        self.match("ID")
        self.data_pro.add_param_to(self.curr_type, self.get_prev_token_value())
        self.parse_id_list()
        self.match("RIGHT_PAREN")
        self.curr_type = "None"
        
    # fact    	->	ID LEFT_PAREN STRING stringList RIGHT_PAREN PERIOD
    def parse_fact(self) -> None:
        self.curr_type = "fact"
        self.match("ID")
        self.data_pro.new_pred(self.curr_type, self.get_prev_token_value())
        self.match("LEFT_PAREN")
        self.match("STRING")
        self.data_pro.add_param_to(self.curr_type, self.get_prev_token_value())
        self.parse_string_list()
        self.match("RIGHT_PAREN")
        self.match("PERIOD")
        self.curr_type = "None"

    # rule    	->	headPredicate COLON_DASH predicate predicateList PERIOD
    def parse_rule(self) -> None:
        self.curr_type = "rule"
        self.parse_head_predicate()
        self.match("COLON_DASH")
        self.parse_predicate()
        self.parse_predicate_list()
        self.match("PERIOD")
        self.curr_type = "None"

    # query	        ->      predicate Q_MARK
    def parse_query(self) -> None:
        self.curr_type = "query"
        self.parse_predicate()
        self.match("Q_MARK")
        self.curr_type = "None"

    # headPredicate	->	ID LEFT_PAREN ID idList RIGHT_PAREN
    def parse_head_predicate(self) -> None:
        self.match("ID")
        self.data_pro.new_rule(self.get_prev_token_value())
        self.match("LEFT_PAREN")
        self.match("ID")
        self.data_pro.add_param_to(self.curr_type, self.get_prev_token_value())
        self.parse_id_list()
        self.match("RIGHT_PAREN")

    # predicate	->	ID LEFT_PAREN parameter parameterList RIGHT_PAREN
    def parse_predicate(self) -> None:
        self.match("ID")
        self.data_pro.new_pred(self.curr_type, self.get_prev_token_value())
        self.match("LEFT_PAREN")
        self.parse_parameter()
        self.parse_parameter_list()
        self.match("RIGHT_PAREN")

    # predicateList	->	COMMA predicate predicateList | lambda
    def parse_predicate_list(self) -> None:
        if self.get_current_token().token_type == "COMMA":
            self.match("COMMA")
            self.parse_predicate()
            self.parse_predicate_list()
        else:
            return

    # parameterList	-> 	COMMA parameter parameterList | lambda
    def parse_parameter_list(self) -> None:
        if self.get_current_token().token_type == "COMMA":
            self.match("COMMA")
            self.parse_parameter()
            self.parse_parameter_list()
        else:
            return

    # stringList	-> 	COMMA STRING stringList | lambda
    def parse_string_list(self) -> None:
        if self.get_current_token().token_type == "COMMA":
            self.match("COMMA")
            self.match("STRING")
            self.data_pro.add_param_to(self.curr_type, self.get_prev_token_value())
            self.parse_string_list()
        else:
            return

    # idList  	-> 	COMMA ID idList | lambda
    def parse_id_list(self) -> None:
        if self.get_current_token().token_type == "COMMA":
            self.match("COMMA")
            self.match("ID")
            self.data_pro.add_param_to(self.curr_type, self.get_prev_token_value())
            self.parse_id_list()
        else:
            return

    # parameter	->	STRING | ID 
    def parse_parameter(self) -> None:
        if self.get_current_token().token_type == "STRING":
            self.match("STRING")
        else:
            self.match("ID")
        self.data_pro.add_param_to(self.curr_type, self.get_prev_token_value())