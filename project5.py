from project5_classes.previous_classes.lexer_fsm import LexerFSM as Lexer
from project5_classes.previous_classes.parser import Parser
from project5_classes.previous_classes.token import Token
from project5_classes.previous_classes.datalogprogram import DatalogProgram
from project5_classes.interpreter import Interpreter

#Return your program output here for grading (can treat this function as your "main")
def project5(input: str) -> str:
    lexer: Lexer = Lexer()
    tokens: list[Token] = lexer.run(input)

    parser: Parser = Parser()
    datalog_program: DatalogProgram = parser.run(tokens)

    interpreter: Interpreter = Interpreter()
    return interpreter.run(datalog_program)

def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read() 

#Use this to run and debug code within VS
if __name__ == "__main__":
    # input_contents = read_file_contents("./project5-passoff/80/input7.txt")
    input_contents = read_file_contents("./testinput.txt")
    print(project5(input_contents))
