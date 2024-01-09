from .fsa import FSA
from typing import Callable as function

class CommaFSA(FSA):
    def __init__(self) -> None:
        FSA.__init__(self, "COMMA") # You must invoke the __init__ of the parent class
        self.accept_states.add(self.s1)

    def s0(self) -> function:
        current_input: str = self._get_current_input()
        next_state: function = None
        if current_input != ',': next_state = self.s_err
        else: next_state = self.s1
        self.num_chars_read += 1
        self.num_token_chars += 1
        return next_state

    def s1(self) -> function:
        next_state: function = self.s1
        self.num_chars_read += 1
        return next_state

    def s_err(self) -> function:
        next_state: function = self.s_err # stay in error state on all inputs
        self.num_chars_read += 1
        return next_state
    
'''if __name__ == "__main__":
    test_fsa = ColonFSA()
    print("token length: ", test_fsa.run(":bad"))'''