from .fsa import FSA
from typing import Callable as function

class IDFSA(FSA):
    def __init__(self) -> None:
        FSA.__init__(self, "ID") # You must invoke the __init__ of the parent class
        self.accept_states.add(self.s1)
        self.accept_states.add(self.s2)

    def s0(self) -> function:
        #print("ID state 0")
        current_input: str = self._get_current_input()
        next_state: function = None
        if current_input.isalpha(): next_state = self.s1
        else: next_state = self.s_err
        self.num_chars_read += 1
        self.num_token_chars += 1
        return next_state

    def s1(self) -> function:
        #print("ID state 1")
        current_input: str = self._get_current_input()
        next_state: function = None
        if current_input.isalpha() or current_input.isnumeric(): next_state = self.s1
        else:
            next_state = self.s2
            self.num_token_chars -= 1
        self.num_chars_read += 1
        self.num_token_chars += 1
        return next_state
    
    def s2(self) -> function:
        #print("ID state 2")
        next_state: function = self.s2 # stay in error state on all inputs
        self.num_chars_read += 1
        return next_state

    def s_err(self) -> function:
        #print("ID state err")
        next_state: function = self.s_err # stay in error state on all inputs
        self.num_chars_read += 1
        return next_state
    
if __name__ == "__main__":
    test_fsa = IDFSA()
    print("token length: ", test_fsa.run("Schemes"))