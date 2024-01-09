from .fsa import FSA
from typing import Callable as function

class FactsFSA(FSA):
    def __init__(self) -> None:
        FSA.__init__(self, "FACTS") # You must invoke the __init__ of the parent class
        self.accept_states.add(self.s5) # Since self.accept_states is defined in parent class, I can use it here
    
    def s0(self) -> function:
        #print("In ColonDash State 0")
        current_input: str = self._get_current_input()
        next_state: function = None
        if current_input == 'F': next_state = self.s1
        else: next_state = self.s_err
        self.num_chars_read += 1
        self.num_token_chars += 1
        return next_state

    def s1(self) -> function:
        #print("In ColonDash State 0")
        current_input: str = self._get_current_input()
        next_state: function = None
        if current_input == 'a': next_state = self.s2
        else: next_state = self.s_err
        self.num_chars_read += 1
        self.num_token_chars += 1
        return next_state
    
    def s2(self) -> function:
        #print("In ColonDash State 0")
        current_input: str = self._get_current_input()
        next_state: function = None
        if current_input == 'c': next_state = self.s3
        else: next_state = self.s_err
        self.num_chars_read += 1
        self.num_token_chars += 1
        return next_state
    
    def s3(self) -> function:
        #print("In ColonDash State 0")
        current_input: str = self._get_current_input()
        next_state: function = None
        if current_input == 't': next_state = self.s4
        else: next_state = self.s_err
        self.num_chars_read += 1
        self.num_token_chars += 1
        return next_state
    
    def s4(self) -> function:
        #print("In ColonDash State 0")
        current_input: str = self._get_current_input()
        next_state: function = None
        if current_input == 's': next_state = self.s5
        else: next_state = self.s_err
        self.num_chars_read += 1
        self.num_token_chars += 1
        return next_state
    
    def s5(self) -> function:
        #print("In ColonDash State 0")
        next_state = self.s5
        self.num_chars_read += 1
        return next_state

    def s_err(self) -> function:
        #print("In ColonDash State Error")
        next_state: function = self.s_err # loop in state s_err
        self.num_chars_read += 1
        return next_state

'''if __name__ == "__main__":
    test_fsa = ColonDashFSA()
    print("token length: ", test_fsa.run(":-bad"))'''