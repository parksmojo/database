from typing import Callable

class FSA():
    def __init__(self, name: str):
        self.fsa_name: str = name
        self.start_state: function = self.s0
        self.accept_states: set[function] = set()
        self.input_string: str = ""
        self.num_chars_read: int = 0
        self.num_token_chars: int = 0
    
    def s0(self) -> Callable:
        raise NotImplementedError()
    
    def run(self, input_string: str) -> int:
        self.input_string = input_string
        current_state: function = self.start_state
        while self.num_chars_read < len(self.input_string):
            #print(f"characters read: {self.num_chars_read}")
            current_state = current_state()
        if current_state in self.accept_states:
            #print("correct")
            return self.num_token_chars
        else:
            #print("not correct")
            return 0

    def reset(self) -> None:
        self.num_chars_read = 0
        self.num_token_chars = 0
        self.input_string = ""

    def get_name(self) -> str: 
        return self.fsa_name

    def set_name(self, FSA_name) -> None:
        self.fsa_name = FSA_name

    def _get_current_input(self) -> str:
        return self.input_string[self.num_chars_read]


if __name__ == "__main__":  
    test_fsa = FSA("name")
    print(test_fsa.fsa_name)