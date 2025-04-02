from state import State_Types
class Transition:
    source = None
    target = None
    symbol = None
    replacement = None
    memory_symbol=None
    memory_object=None
    transition_type=None


    def __init__(self, source, target, symbol, replacement, memory_symbol, memory_object, transition_type):
        self.source = source
        self.target = target
        self.symbol = symbol
        self.replacement = replacement
        self.memory_symbol=memory_symbol
        self.memory_object=memory_object
        self.transition_type=transition_type

    def __str__(self):
        if self.transition_type==State_Types.PRINT:
            return f"{self.transition_type.value} Transition {self.source} -> {self.target} output: {self.symbol} WRITES/READS: {self.replacement} on the memory object: {self.memory_object}"
        return f"{self.transition_type.value} Transition {self.source} -> {self.target} on a {self.symbol} WRITES/READS: {self.memory_symbol} on the memory object: {self.memory_object}"