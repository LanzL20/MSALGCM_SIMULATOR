from enum import Enum
from datastructure import Stack, Queue, Tape, Tape_2D
from state import State
from state import State_Types
from transition import Transition
import copy


class Status(Enum):
    RUNNING = 1
    ACCEPTED = 2
    REJECTED = 3
    NOT_STARTED = 4
class Machine:
    states = []
    initial_state = None
    current_state = None
    stacks = []
    queues = []
    tapes = []
    input_string = ""
    output_string = ""
    string_pointer = -1
    status=None

    def __init__(self):
        self.status = Status.NOT_STARTED
    
    def get_current_state(self):
        return self.current_state
    
    def set_current_state(self, state):
        self.current_state = state

    def get_states(self):
        return self.states
    
    def set_input_string(self, input_string):
        self.input_string = input_string
        self.output_string = ""
    
    def get_transitions(self):
        transitions = []
        for state in self.states:
            transitions.append(state.transitions)
        return transitions
    
    def get_initial_state(self):
        return self.initial_state

    
    def create_stack(self, name):
        stack=Stack(name)
        self.stacks.append(stack)

    def create_queue(self, name):
        queue=Queue(name)
        self.queues.append(queue)

    def create_tape(self, name):
        tape=Tape(name)
        self.tapes.append(tape)

    def create_tape_2D(self, name):
        tape_2D=Tape_2D(name)
        self.tapes.append(tape_2D)
    
    def add_state(self, state):
        self.states.append(state)
        if(state.is_initial):
            self.initial_state=state

    #TODO: check the initialization of machine with the start state.
    def start(self):
        self.current_state=self.initial_state
        self.string_pointer=-1
        self.status=Status.RUNNING
        reject_state=State("reject", False, True, "REJECT")
        accept_state=State("accept", False, True, "ACCEPT")
        print("Accept state: ", accept_state.state_type)
        print("Reject state: ", reject_state.state_type)
        self.states.append(reject_state)
        self.states.append(accept_state)
        if len(self.tapes)>0:
            self.tapes[0].put_input_string(self.input_string)


    def save_copy(self):
        copy_machine=copy.deepcopy(self)
        return copy_machine
    
    def reject_machine(self):
        self.status=Status.REJECTED
    
    def load_copy(self, copy_machine):
        self.states=copy_machine.states
        self.initial_state=copy_machine.initial_state
        self.current_state=copy_machine.current_state
        self.stacks=copy_machine.stacks
        self.queues=copy_machine.queues
        self.tapes=copy_machine.tapes
        self.input_string=copy_machine.input_string
        self.output_string=copy_machine.output_string
        self.string_pointer=copy_machine.string_pointer

    def testing_save_load(self):
        machines=[]
        for i in range(1, 4):
            current_machine=self.save_copy()
            current_machine.string_pointer+=i
            machines.append(current_machine)
        self.load_copy(machines[0])
        machines.pop(0)
        return machines


    def step_WRITE(self, state):
        viable_transitions = state.transitions
        save_point = self.save_copy()
        machines = []
        for transition in viable_transitions:
            #look for the memory object in the stacks, queues, then add the symbol to the memory object
            for stack in self.stacks:
                if stack.name == transition.memory_object:
                    stack.push(transition.memory_symbol)
                    break
            for queue in self.queues:
                if queue.name == transition.memory_object:
                    queue.enqueue(transition.memory_symbol)
                    break
            #look for the next state in the states, then set the current state to the next state
            for state in self.states:
                if state.name == transition.target:
                    self.set_current_state(state)
                    break
            machines.append(self.save_copy())
            self.load_copy(save_point)
        
        self.load_copy(machines[0])
        machines.pop(0)
        return machines
    
    def step_READ(self, state):
        transitions = state.transitions
        viable_transitions = []
        memory_object_name = transitions[0].memory_object
        read_symbol = transitions[0].memory_symbol
        memory_object = None
        for stack in self.stacks:
            if stack.name == memory_object_name:
                memory_object = stack
                break
        for queue in self.queues:
            if queue.name == memory_object_name:
                memory_object = queue
                break
        if memory_object == None:
            self.reject_machine()
            return None
        if(memory_object.is_empty()):
            self.reject_machine()
            return None
        
        for transition in transitions:
            if transition.memory_symbol == memory_object.peek():
                viable_transitions.append(transition)
        if len(viable_transitions) == 0:
            self.reject_machine()
            return None
        machines = []
        for transition in viable_transitions:
            modified_machine = self.save_copy()
            #look for the memory object in the stacks, queues, then add the symbol to the memory object
            for stack in modified_machine.stacks:
                if stack.name == transition.memory_object:
                    stack.pop(transition.memory_symbol)
                    break
            for queue in modified_machine.queues:
                if queue.name == transition.memory_object:
                    queue.dequeue(transition.memory_symbol)
                    break
            #look for the next state in the states, then set the current state to the next state
            for state in modified_machine.states:
                if state.name == transition.target:
                    modified_machine.set_current_state(state)
                    break
            machines.append(modified_machine)
        self.load_copy(machines[0])
        machines.pop(0)
        return machines

    def step_SCAN_RIGHT(self, state):
        transitions = state.transitions
        viable_transitions = []
        if self.string_pointer+1>=len(self.input_string):
            next_char='#'
        else:
            next_char=self.input_string[self.string_pointer+1]

        for transition in transitions:
            if transition.symbol==next_char:
                viable_transitions.append(transition)
        
        if len(viable_transitions) == 0:
            self.reject_machine()
            return None
        machines = []

        for transition in viable_transitions:
            modified_machine = self.save_copy()
            #look for the new state in the states, then set the current state to the new state
            for state in modified_machine.states:
                if state.name == transition.target:
                    modified_machine.set_current_state(state)
                    break
            modified_machine.string_pointer+=1
            machines.append(modified_machine)
        self.load_copy(machines[0])
        machines.pop(0)
        return machines
        


    def step_SCAN_LEFT(self, state):
        transitions = state.transitions
        viable_transitions = []
        if self.string_pointer-1<0:
            prev_char='#'
        else:
            prev_char=self.input_string[self.string_pointer-1]

        for transition in transitions:
            if transition.symbol==prev_char:
                viable_transitions.append(transition)
        
        if len(viable_transitions) == 0:
            self.reject_machine()
            return None
        machines = []

        for transition in viable_transitions:
            modified_machine = self.save_copy()
            #look for the new state in the states, then set the current state to the new state
            for state in modified_machine.states:
                if state.name == transition.target:
                    modified_machine.set_current_state(state)
                    break
            modified_machine.string_pointer-=1
            machines.append(modified_machine)
        self.load_copy(machines[0])
        machines.pop(0)
        return machines
    

    def step_PRINT(self, state):
        transitions=state.transitions
        machines=[]
        for transition in transitions:
            modified_machine=self.save_copy()
            #look for the new state in the states, then set the current state to the new state
            for state in modified_machine.states:
                if state.name==transition.target:
                    modified_machine.set_current_state(state)
                    break
            modified_machine.output_string+=transition.symbol
            machines.append(modified_machine)
        self.load_copy(machines[0])
        machines.pop(0)
        return machines
    #TODO: number one check if doing mem_object_tape=tape actually gets the reference and can edit it freely
    #TODO: number two check if the memory object is actually being passed correctly
    #TODO: number three be wary of the fact that the tapes list will contain both 2d and 1d tapes
    #move/check right and left should have been implemented in an abstract way that accepts the same parameters.
    #make sure to not step up or down on 1d tape machines.
    def step_LEFT(self, state):
        transitions=state.transitions
        machines=[]
        viable_transitions=[]
        mem_object_tape=None
        for tape in self.tapes:
            if transitions[0].memory_object==tape.name:
                mem_object_tape=tape
                break

        for transition in transitions:
            if mem_object_tape.check_left(transition.symbol):
                viable_transitions.append(transition)
        
        if len(viable_transitions)==0:
            self.reject_machine()
            return None
        
        for transition in viable_transitions:
            modified_machine=self.save_copy()
            #look for the new state in the states, then set the current state to the new state
            for state in modified_machine.states:
                if state.name==transition.target:
                    modified_machine.set_current_state(state)
                    break
            for tape in modified_machine.tapes:
                if tape.name==transition.memory_object:
                    mem_object_tape=tape
                    break
            #look for the memory object in the stacks, queues, then add the symbol to the memory object
            mem_object_tape.move_left(transition.symbol)
            machines.append(modified_machine)
        self.load_copy(machines[0])
        machines.pop(0)
        return machines

        
    def step_RIGHT(self, state):
        transitions=state.transitions
        machines=[]
        viable_transitions=[]
        mem_object_tape=None
        for tape in self.tapes:
            if transitions[0].memory_object==tape.name:
                mem_object_tape=tape
                break
        
        for transition in transitions:
            if mem_object_tape.check_right(transition.symbol):
                viable_transitions.append(transition)

        if len(viable_transitions)==0:
            self.reject_machine()
            return None
        
        for transition in viable_transitions:
            modified_machine=self.save_copy()
            #look for the new state in the states, then set the current state to the new state
            for state in modified_machine.states:
                if state.name==transition.target:
                    modified_machine.set_current_state(state)
                    break
            for tape in modified_machine.tapes:
                if tape.name==transition.memory_object:
                    mem_object_tape=tape
                    break
            #look for the memory object in the stacks, queues, then add the symbol to the memory object
            mem_object_tape.move_right(transition.symbol)
            machines.append(modified_machine)
        self.load_copy(machines[0])
        machines.pop(0)
        return machines
        
    def step_UP(self, state):
        transitions=state.transitions
        machines=[]
        viable_transitions=[]
        mem_object_tape=None
        for tape in self.tapes:
            if transitions[0].memory_object==tape.name:
                mem_object_tape=tape
                break

        for transition in transitions:
            if mem_object_tape.check_up(transition.symbol):
                viable_transitions.append(transition)

        if len(viable_transitions)==0:
            self.reject_machine()
            return None
        
        for transition in viable_transitions:
            modified_machine=self.save_copy()
            #look for the new state in the states, then set the current state to the new state
            for state in modified_machine.states:
                if state.name==transition.target:
                    modified_machine.set_current_state(state)
                    break
            for tape in modified_machine.tapes:
                if tape.name==transition.memory_object:
                    mem_object_tape=tape
                    break
            #look for the memory object in the stacks, queues, then add the symbol to the memory object
            mem_object_tape.move_up(transition.symbol)
            machines.append(modified_machine)
        self.load_copy(machines[0])
        machines.pop(0)
        return machines
        

    def step_DOWN(self, state):
        transitions=state.transitions
        machines=[]
        viable_transitions=[]
        mem_object_tape=None
        for tape in self.tapes:
            if transitions[0].memory_object==tape.name:
                mem_object_tape=tape
                break

        for transition in transitions:
            if mem_object_tape.check_down(transition.symbol):
                viable_transitions.append(transition)

        if len(viable_transitions)==0:
            self.reject_machine()
            return None
        
        for transition in viable_transitions:
            modified_machine=self.save_copy()
            #look for the new state in the states, then set the current state to the new state
            for state in modified_machine.states:
                if state.name==transition.target:
                    modified_machine.set_current_state(state)
                    break
            for tape in modified_machine.tapes:
                if tape.name==transition.memory_object:
                    mem_object_tape=tape
                    break
            #look for the memory object in the stacks, queues, then add the symbol to the memory object
            mem_object_tape.move_down(transition.symbol)
            machines.append(modified_machine)
        self.load_copy(machines[0])
        machines.pop(0)
        return machines


    def step(self):
        if self.status == Status.RUNNING:
            # Get the current state
            current_state = self.get_current_state()            
            #before doing anything, check if the current state is accept or reject state
            if current_state.state_type==State_Types.ACCEPT:
                self.status=Status.ACCEPTED
                return None
            elif current_state.state_type==State_Types.REJECT:
                self.status=Status.REJECTED
                return None
            if(current_state.state_type==State_Types.SCAN_RIGHT):
                return self.step_SCAN_RIGHT(current_state)
            
            elif(current_state.state_type==State_Types.SCAN_LEFT):
                return self.step_SCAN_LEFT(current_state)
            
            elif(current_state.state_type==State_Types.SCAN):
                return self.step_SCAN_RIGHT(current_state)
            
            elif(current_state.state_type==State_Types.PRINT):
                return self.step_PRINT(current_state)
            
            elif(current_state.state_type==State_Types.READ):
                return self.step_READ(current_state)
            
            elif(current_state.state_type==State_Types.WRITE):
                return self.step_WRITE(current_state)
            
            elif(current_state.state_type==State_Types.RIGHT):
                return self.step_RIGHT(current_state)
            
            elif(current_state.state_type==State_Types.LEFT):
                return self.step_LEFT(current_state)
            
            elif(current_state.state_type==State_Types.UP):
                return self.step_UP(current_state)
            
            elif(current_state.state_type==State_Types.DOWN):
                return self.step_DOWN(current_state)
            
    def __str__(self):
        return self.current_state.name + " Status " + str(self.status) +" State Type: " + str(self.current_state.state_type)
            
            
    