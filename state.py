from enum import Enum
class State_Types(Enum):
    NORMAL = "NORMAL"
    SCAN_RIGHT = "SCAN_RIGHT"
    SCAN_LEFT = "SCAN_LEFT"
    SCAN = "SCAN"
    PRINT = "PRINT"
    READ = "READ"
    WRITE = "WRITE"
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    UP = "UP"
    DOWN = "DOWN"
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"


class State:
    name = None
    transitions = []
    is_initial = False
    is_final = False
    state_type = None

    def __init__(self, name, is_initial, is_final, state_type):
        self.name = name
        self.is_initial = is_initial
        self.is_final = is_final
        self.transitions = []
        if state_type=="NORMAL":
            self.state_type=State_Types.NORMAL
        elif state_type=="SCAN RIGHT":
            self.state_type=State_Types.SCAN_RIGHT
        elif state_type=="SCAN LEFT":
            self.state_type=State_Types.SCAN_LEFT
        elif state_type=="SCAN":
            self.state_type=State_Types.SCAN
        elif state_type=="PRINT":
            self.state_type=State_Types.PRINT
        elif state_type=="READ":
            self.state_type=State_Types.READ
        elif state_type=="WRITE":
            self.state_type=State_Types.WRITE
        elif state_type=="RIGHT":
            self.state_type=State_Types.RIGHT
        elif state_type=="LEFT":
            self.state_type=State_Types.LEFT
        elif state_type=="UP":
            self.state_type=State_Types.UP
        elif state_type=="DOWN":
            self.state_type=State_Types.DOWN
        elif state_type=="ACCEPT":
            self.state_type=State_Types.ACCEPT
        elif state_type=="REJECT":
            self.state_type=State_Types.REJECT
    def get_name(self):
        return self.name
    
    def is_initial(self):
        return self.is_initial
    
    def is_final(self):
        return self.is_final
    
    def add_transition(self, transition):
        self.transitions.append(transition)

    #state the output if the state is printed
    def __str__(self):
        return "State: " + self.name + "\nis_initial: " + str(self.is_initial) + "\nis_final: " + str(self.is_final) + "\nstate_type: " + str(self.state_type) + "\ntransitions: " + str(self.transitions) 