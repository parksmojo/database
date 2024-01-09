from .fsa import FSA
from typing import Callable as function

class QueriesFSA(FSA):
    def __init__(self) -> None:
        FSA.__init__(self, "QUERIES") # You must invoke the __init__ of the parent class
        self.accept_states.add(self.s7) # Since self.accept_states is defined in parent class, I can use it here
    
    def s0(self) -> function:
        #print("In ColonDash State 0")
        current_input: str = self._get_current_input()
        next_state: function = None
        if current_input == 'Q': next_state = self.s1
        else: next_state = self.s_err
        self.num_chars_read += 1
        self.num_token_chars += 1
        return next_state

    def s1(self) -> function:
        #print("In ColonDash State 0")
        current_input: str = self._get_current_input()
        next_state: function = None
        if current_input == 'u': next_state = self.s2
        else: next_state = self.s_err
        self.num_chars_read += 1
        self.num_token_chars += 1
        return next_state
    
    def s2(self) -> function:
        #print("In ColonDash State 0")
        current_input: str = self._get_current_input()
        next_state: function = None
        if current_input == 'e': next_state = self.s3
        else: next_state = self.s_err
        self.num_chars_read += 1
        self.num_token_chars += 1
        return next_state
    
    def s3(self) -> function:
        #print("In ColonDash State 0")
        current_input: str = self._get_current_input()
        next_state: function = None
        if current_input == 'r': next_state = self.s4
        else: next_state = self.s_err
        self.num_chars_read += 1
        self.num_token_chars += 1
        return next_state
    
    def s4(self) -> function:
        #print("In ColonDash State 0")
        current_input: str = self._get_current_input()
        next_state: function = None
        if current_input == 'i': next_state = self.s5
        else: next_state = self.s_err
        self.num_chars_read += 1
        self.num_token_chars += 1
        return next_state
    
    def s5(self) -> function:
        #print("In ColonDash State 0")
        current_input: str = self._get_current_input()
        next_state: function = None
        if current_input == 'e': next_state = self.s6
        else: next_state = self.s_err
        self.num_chars_read += 1
        self.num_token_chars += 1
        return next_state
    
    def s6(self) -> function:
        #print("In ColonDash State 0")
        current_input: str = self._get_current_input()
        next_state: function = None
        if current_input == 's': next_state = self.s7
        else: next_state = self.s_err
        self.num_chars_read += 1
        self.num_token_chars += 1
        return next_state
    
    def s7(self) -> function:
        #print("In ColonDash State 0")
        next_state = self.s7
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