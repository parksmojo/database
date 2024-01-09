from .fsa import FSA
from typing import Callable as function

class RightParenFSA(FSA):
    def __init__(self):
        FSA.__init__(self, "RIGHT_PAREN") # You must invoke the __init__ of the parent class
        self.accept_states.add(self.s1)

    def s0(self) -> function:
        """ define the start state in the derived class """
        #print("In state s0. s0's information is ",self.s0)
        current_input: str = self._get_current_input()
        next_state: function = None
        if current_input != ')': next_state = self.s_err
        else: next_state = self.s1
        self.num_chars_read += 1
        self.num_token_chars += 1
        return next_state

    def s1(self) -> function:
        #print("In state s1. s1's information is ",self.s1)
        next_state: function = self.s1
        self.num_chars_read += 1
        return next_state

    def s_err(self) -> function:
        #print("In state s_err. s_err's information is ",self.s_err)
        next_state: function = self.s_err # stay in error state on all inputs
        self.num_chars_read += 1
        return next_state

'''if __name__ == "__main__":
    test_fsa = RightParenFSA()
    print("token length: ", test_fsa.run(")asdfass"))'''