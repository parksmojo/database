from .fsa_classes.fsa import FSA
from .fsa_classes.colon_dash_fsa import ColonDashFSA
from .fsa_classes.colon_fsa import ColonFSA
from .fsa_classes.left_paren_fsa import LeftParenFSA
from .fsa_classes.right_paren_fsa import RightParenFSA
from .fsa_classes.comment_fsa import CommentFSA
from .fsa_classes.comma_fsa import CommaFSA
from .fsa_classes.period_fsa import PeriodFSA
from .fsa_classes.add_fsa import AddFSA
from .fsa_classes.multiply_fsa import MultiplyFSA
from .fsa_classes.q_mark_fsa import QMarkFSA
from .fsa_classes.string_fsa import StringFSA
from .fsa_classes.schemes_fsa import SchemesFSA
from .fsa_classes.facts_fsa import FactsFSA
from .fsa_classes.rules_fsa import RulesFSA
from .fsa_classes.queries_fsa import QueriesFSA
from .fsa_classes.id_fsa import IDFSA
from .token import Token

class LexerFSM:
    def __init__(self):
        self.tokens: list[Token] = []
        self.fsas: list[FSA] = []
        self.fsas.append(ColonDashFSA())
        self.fsas.append(ColonFSA())
        self.fsas.append(LeftParenFSA())
        self.fsas.append(RightParenFSA())
        self.fsas.append(CommentFSA())
        self.fsas.append(CommaFSA())
        self.fsas.append(PeriodFSA())
        self.fsas.append(AddFSA())
        self.fsas.append(MultiplyFSA())
        self.fsas.append(QMarkFSA()) 
        self.fsas.append(StringFSA())
        self.fsas.append(SchemesFSA())
        self.fsas.append(FactsFSA())
        self.fsas.append(RulesFSA())
        self.fsas.append(QueriesFSA())
        self.fsas.append(IDFSA())
    
    def run(self, input: str) -> list[Token]:
        output: str = ""
        read = True

        # Splits the input by line and lexes each line
        line: list[str] = input.split('\n')
        for i in range(len(line)):
            read = self.lex(line[i], i + 1)
            if not read: break

        # Formats and returns token list
        if i + 1 == len(line): self.tokens.append(Token("EOF", "", i + 1))
        return self.tokens

        '''for token in self.tokens:
            output += token.to_string()
        if read: output += f"Total Tokens = {len(self.tokens)}"
        else: output += f"\nTotal Tokens = Error on line {i + 1}"
        return output'''
        
    def lex(self, input: str, line_num: int) -> bool:
        while input != "":
            # Removes leading whitespace
            while input[0].isspace(): 
                input = input[1:]
                if input == "": return True

            # Runs the FSAs on the input and cuts off the read section
            #print(f"Input of size {len(input)}: \"{input}\"")
            token_len = self.__manager_fsm__(input, line_num)
            if token_len == 0: return False
            input = input[token_len:]
            #print(f"New string of size {len(input)}: \"{input}\"\n")
        return True  
        
    def __manager_fsm__(self, input: str, line_num: int) -> int:
        token_len = 0
        token_type = ""

        # Finds the FSA that approved the most input
        for cur_fsa in self.fsas:
            #print(f"Trying FSA: {cur_fsa.fsa_name}, current length: {token_len}")
            if cur_fsa.run(input) > token_len:
                token_len = cur_fsa.num_token_chars
                token_type = cur_fsa.fsa_name
            cur_fsa.reset()

        # Adds the chosen Token to the list and returns the token's length
        #print(f"{token_type}: \"{input[:token_len]}\" found on line {line_num}, cutting {token_len} characters")

        if token_type != "COMMENT":
            if token_len > 0: self.tokens.append(Token(token_type, input[:token_len], line_num))
            else: self.tokens.append(Token("UNDEFINED", input[:1], line_num))
        return token_len

    def reset(self) -> None:
        self.tokens.clear()