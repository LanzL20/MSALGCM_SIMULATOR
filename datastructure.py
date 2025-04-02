class datastructure:
    name = None

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name
    
#TODO: FIX THE STRUCTURES
class Stack(datastructure):
    def __init__(self, name):
        super().__init__(name)
        self.stack = []

    def push(self, symbol):
        self.stack.append(symbol)

    def peek(self):
        return self.stack[-1]

    #only pop if the given symbol is on top of the stack
    def pop(self, symbol):
        if self.peek() == symbol:
            return self.stack.pop()
        else:
            return None        
    
    def is_empty(self):
        return len(self.stack) == 0

    def get_stack(self):
        return self.stack
    
    def __str__(self):
        return self.name
    
class Queue(datastructure):
    def __init__(self, name):
        super().__init__(name)
        self.queue = []

    def enqueue(self, symbol):
        self.queue.append(symbol)

    def peek(self):
        return self.queue[0]
    
    def dequeue(self, symbol):
        if self.peek() == symbol:
            return self.queue.pop(0)
        else:
            return None

    def is_empty(self):
        return len(self.queue) == 0

    def get_queue(self):
        return self.queue
    
    def __str__(self):
        return self.name

#fix the    
class Tape(datastructure):
    def __init__(self, name):
        super().__init__(name)
        self.tape = "###"
        self.pointer_x = 1
        #should never be used but is here for abstraction between 1D and 2D tapes
        self.pointer_y = 1
        self.type="1D"

    def put_input_string(self, input_string):
        self.tape = "##" + input_string + "#"
        self.pointer = 1

    def read(self):
        return self.tape.pop(0)

    def check_left(self, symbol):
        read, replacement=symbol.split("/")
        if(self.tape[self.pointer_x-1]==read):
            return True
        else:
            return False

    def check_right(self, symbol):
        read, replacement=symbol.split("/")
        if(self.tape[self.pointer_x+1]==read):
            return True
        else:
            return False

    def move_left(self, symbol):
        read, replacement=symbol.split("/")
        self.pointer_x-=1
        if self.pointer_x<=0:
            self.pointer_x=1
            self.tape="#"+self.tape
        self.tape = self.tape[:self.pointer_x] + replacement + self.tape[self.pointer_x+1:]
        char=self.tape[self.pointer_x]
        return char

    def move_right(self, symbol):
        print("symbol: ", symbol)
        read, replacement=symbol.split("/")
        self.pointer_x+=1
        if self.pointer_x>=len(self.tape)-1:
            self.tape=self.tape+"#"
        self.tape = self.tape[:self.pointer_x] + replacement + self.tape[self.pointer_x+1:]
        print("tape: ", self.tape)
        char=self.tape[self.pointer_x]
        return char

    def get_tape(self):
        return self.tape
    #return string
    def print_tape(self):
        return_string=""
        return_string+=self.tape
        return return_string
    
    def __str__(self):
        return self.name
    
    
class Tape_2D(datastructure):
    def __init__(self, name):
        super().__init__(name)
        self.tape = ["###","###","###"]
        self.pointer_x = 1
        self.pointer_y = 1
        self.type="2D"
    #TODO: FIX THE PUT INPUT STRING FOR 2D TAPES
    def put_input_string(self, input_string):
        starting_tape_line="##"+input_string+"#"
        temp_string=""
        for i in range(len(starting_tape_line)):
            temp_string+="#"
        self.tape[0]=temp_string
        self.tape[1]=starting_tape_line
        self.tape[2]=temp_string
        self.pointer_x = 1
        self.pointer_y = 1

    def write(self, symbol):
        self.tape.append(symbol)

    def read(self):
        return self.tape.pop(0)

    def check_left(self, symbol):
        read, replacement=symbol.split("/")
        if(self.tape[self.pointer_y][self.pointer_x-1]==read):
            return True
        else:
            return False

    def check_right(self, symbol):
        read, replacement=symbol.split("/")
        if(self.tape[self.pointer_y][self.pointer_x+1]==read):
            return True
        else:
            return False
    #TODO:DOUBLE CHECK THE UP AND DOWN MOVES FOR 2D TAPES
    def check_up(self, symbol):
        read, replacement=symbol.split("/")
        if(self.tape[self.pointer_y-1][self.pointer_x]==read):
            return True
        else:
            return False
    #TODO:DOUBLE CHECK THE UP AND DOWN MOVES FOR 2D TAPES
    def check_down(self, symbol):
        read, replacement=symbol.split("/")
        if(self.tape[self.pointer_y+1][self.pointer_x]==read):
            return True
        else:
            return False
        
    def move_left(self, symbol):
        read, replacement=symbol.split("/")
        #move the pointer to the left
        self.pointer_x-=1
        #check if the pointer will go to the first character, if so add a new column to the tape
        if self.pointer_x<=0:
            self.pointer_x=1
            print("Adding new column to the left")
            for i in range(len(self.tape)):
                self.tape[i]="#"+self.tape[i]

        #replace the character at the pointer with the replacement character
        tape_line=self.tape[self.pointer_y]
        self.tape[self.pointer_y]=tape_line[:self.pointer_x] + replacement + tape_line[self.pointer_x+1:]
        #return the character at the pointer
        char=self.tape[self.pointer_y][self.pointer_x]
        return char
    
    def move_right(self, symbol):
        read, replacement=symbol.split("/")
        #move the pointer to the right
        self.pointer_x+=1
        #check if the pointer will go to the last character, if so add a new column to the tape
        if self.pointer_x>=len(self.tape[0])-1:
            for i in range(len(self.tape)):
                self.tape[i]=self.tape[i]+"#"
        #replace the character at the pointer with the replacement character
        tape_line=self.tape[self.pointer_y]
        self.tape[self.pointer_y]=tape_line[:self.pointer_x] + replacement + tape_line[self.pointer_x+1:]
        #return the character at the pointer
        char=self.tape[self.pointer_y][self.pointer_x]
        return char
    
    def move_up(self, symbol):
        read, replacement=symbol.split("/")
        self.pointer_y-=1
        if self.pointer_y<=0:
            self.pointer_y=1
            #add a new row to the tape at the top
            temp_string=""
            for i in range(len(self.tape[0])):
                temp_string+="#"
            self.tape.insert(0,temp_string)
        #replace the character at the pointer with the replacement character
        tape_line=self.tape[self.pointer_y]
        self.tape[self.pointer_y]=tape_line[:self.pointer_x] + replacement + tape_line[self.pointer_x+1:]
        #return the character at the pointer
        char=self.tape[self.pointer_y][self.pointer_x]
        return char
            

    def move_down(self, symbol):
        read, replacement=symbol.split("/")
        self.pointer_y+=1
        if self.pointer_y>=len(self.tape)-1:
            #add a new row to the tape at the bottom
            temp_string=""
            for i in range(len(self.tape[0])):
                temp_string+="#"
            self.tape.append(temp_string)
        #replace the character at the pointer with the replacement character
        tape_line=self.tape[self.pointer_y]
        self.tape[self.pointer_y]=tape_line[:self.pointer_x] + replacement + tape_line[self.pointer_x+1:]
        #return the character at the pointer
        char=self.tape[self.pointer_y][self.pointer_x]
        return char

    def get_tape(self):
        return self.tape
    
    def print_tape(self):
        return_string=""
        for i in range(len(self.tape)):
            return_string+=self.tape[i]+"\n"
        return return_string
    
    def __str__(self):
        return self.name