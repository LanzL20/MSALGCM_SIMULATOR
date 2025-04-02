import re
from machine import Machine
from state import State
from state import State_Types
from transition import Transition
import tkinter as tk
from simulation import Simulation
#parse the input file
def parse_input_file(string_input, initial_machine):
    #iterate through the lines
    print("Parsing the input file...")
    split_input = string_input.split(".LOGIC")
    data_input = split_input[0]
    logic_input = split_input[1]

    is_initial = True

    data_input = data_input.split("\n")
    logic_input = logic_input.split("\n")
    logic_input.pop(0)
    #getting all the data structures from the file
    for line in data_input:
        structure=line.split(" ")
        if(structure[0]=="STACK"):
            initial_machine.create_stack(structure[1])
        elif(structure[0]=="QUEUE"):
            initial_machine.create_queue(structure[1])
        elif(structure[0]=="TAPE"):
            initial_machine.create_tape(structure[1])
        elif(structure[0]=="2D_TAPE"):
            initial_machine.create_tape_2D(structure[1])
    #getting all the state names and transitions from the file
    for line in logic_input:
        #name getting
        try:
            name, action = line.split("] ")
        except ValueError:
            continue
        type_index=action.find("(")
        state_type=action[:type_index].strip()
        state=State(name, is_initial, False, state_type)
        
        if(is_initial):
            is_initial=False
        #transition getting
        action=action[type_index:]

        mem_object=re.match(r"\([a-zA-Z0-9]+\)", action)
        mem_object_name=None
        if mem_object:
            mem_object_name=action[mem_object.start()+1:mem_object.end()-1]
            action=action[mem_object.end():].strip()
        actions=action.split(", ")
        for action in actions:
            action=action[1:len(action)-1]
            action=action.split(",")
            if(mem_object_name==None):
                transition=Transition(state.name, action[1], action[0], None, None, mem_object_name, state.state_type)
            elif(mem_object_name!=None and action[0].find("/")!=-1):
                transition=Transition(state.name, action[1], action[0], None, None, mem_object_name, state.state_type)
            else:
                transition=Transition(state.name, action[1], None, None, action[0], mem_object_name, state.state_type)
            state.add_transition(transition)

        initial_machine.add_state(state)

def combined_function(initial_machine, text_input, text_input2, root):
    parse_input_file(text_input, initial_machine)
    initial_machine.set_input_string(text_input2)
    root.destroy()
    simulation_window(initial_machine, text_input, text_input2)
    print(text_input2)

def on_frame_configure(canvas, scrollable_frame):
    canvas.configure(scrollregion=canvas.bbox("all"))

def change_timeline(simulate_machine, state_labels, stack_labels, queue_labels, tape_labels, input_string_label, output_string_label, timeline_label, timeline_entry_label):
    simulate_machine.displayed_machine=int(timeline_entry_label.get())-1
    if(simulate_machine.displayed_machine>=len(simulate_machine.machines) or simulate_machine.displayed_machine<0):
        simulate_machine.displayed_machine=0
        new_window = tk.Toplevel()
        new_window.title("Error")
        new_window.geometry("400x200")
        error_label = tk.Label(new_window, text="Invalid timeline number changing back to 1", font=("Arial", 16))
        error_label.pack(pady=(20,0))
    update_display(simulate_machine.get_displayed_machine(), state_labels, stack_labels, queue_labels, tape_labels, input_string_label, output_string_label, timeline_label, len(simulate_machine.machines))


def simulation_window(initial_machine, text_input, text_input2):
    #initial_display
    root = tk.Tk()
    root.title("Machine Simulation")
    root.geometry("1500x800")

    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollable_frame.bind("<Configure>", lambda e: on_frame_configure(canvas, scrollable_frame))

    simulate_machine=Simulation(initial_machine)

    timeine_label=tk.Label(scrollable_frame, text=f"Timelines: 1-{len(simulate_machine.machines)}", font=("Arial", 16), anchor="w")
    timeine_label.pack(pady=(20,0),side="left", padx=(30,0), anchor="n")

    timeline_entry_label = tk.Entry(scrollable_frame, width=10)
    #put text in the entry box
    timeline_entry_label.insert(0, f"{simulate_machine.displayed_machine+1}")
    timeline_entry_label.pack(pady=(20,0), padx=(30,0), anchor="n", side="left")

    timeline_button = tk.Button(scrollable_frame, text="Select Timeline", command=lambda: change_timeline(simulate_machine, state_labels, stack_labels, queue_labels, tape_labels, input_string_label, output_string_label,timeine_label, timeline_entry_label))
    timeline_button.pack(pady=(20,0), padx=(30,0), anchor="n", side="left")
    step_button = tk.Button(scrollable_frame, text="Step", command=lambda: processing_step(simulate_machine, state_labels, stack_labels, queue_labels, tape_labels, input_string_label, output_string_label,timeine_label))
    step_button.pack(pady=(20,0), anchor="n", side="left")

    state_labels, stack_labels, queue_labels, tape_labels, input_string_label, output_string_label = processing_window(simulate_machine.get_displayed_machine(), text_input, text_input2, scrollable_frame)
    root.mainloop()

def update_display(machine, state_labels, stack_labels, queue_labels, tape_labels, input_string_label, output_string_label, timeline_label, number_of_machines):
    input_string_label.delete("1.0", tk.END)  # Clear text
    input_string_label.insert("1.0", "#"+machine.input_string+"#")
    input_string_label.tag_configure("highlight", foreground="red", font=("Arial", 10, "bold"))
    input_string_label.tag_add("highlight", f"1.{machine.string_pointer+1}", f"1.{machine.string_pointer+2}")

    output_string_label.config(text=machine.output_string)
    print("Number of machines: ", number_of_machines)
    timeline_label.config(text=f"Timelines: 1-{number_of_machines}")

    #update the state labels
    for state_label, state_name in state_labels:
        if(state_name==machine.current_state.name):
            state_label.config(bg="lightgreen")
        else:
            state_label.config(bg="white")     

    #update the stack labels
    for stack_label, stack_name in stack_labels:
        for stack in machine.stacks:
            if(stack.name==stack_name):
                stack_label.config(text=f"Contents: {''.join(stack.stack)}")
                break


    #update the queue labels
    for queue_label, queue_name in queue_labels:
        for queue in machine.queues:
            if(queue.name==queue_name):
                queue_label.config(text=f"Contents: {''.join(queue.queue)}")
                break

    #update the tape labels
    for tape_label, tape_name in tape_labels:
        for tape in machine.tapes:
            if(tape.name==tape_name):
                tape_label.delete("1.0", tk.END)  # Clear text
                tape_label.insert("1.0", tape.print_tape())
                tape_label.tag_configure("highlight", foreground="red", font=("Arial", 10, "bold"))
                #DOES NOT TAKE INTO ACCOUNT 2D TAPES
                if(tape.type=="1D"):
                    tape_label.tag_add("highlight", f"1.{tape.pointer_x}", f"1.{tape.pointer_x+1}")
                elif(tape.type=="2D"):
                    tape_label.tag_add("highlight", f"{tape.pointer_y+1}.{tape.pointer_x}", f"{tape.pointer_y+1}.{tape.pointer_x+1}")
                break


#display machine information
def processing_window(initial_machine, text_input, text_input2, root):
    input_string_title_label = tk.Label(root, text="Input String:", font=("Arial", 16))
    input_string_title_label.pack(pady=(20,0), padx=(30,0), anchor="w")

    input_string_label = tk.Text(root, height=1, width=110, font=("Arial", 10))
    input_string_label.insert("1.0", "#"+initial_machine.input_string+"#")
    input_string_label.tag_configure("highlight", foreground="red", font=("Arial", 10, "bold"))
    input_string_label.tag_add("highlight", f"1.{initial_machine.string_pointer+1}", f"1.{initial_machine.string_pointer+2}")
    input_string_label.pack(pady=(5,0), padx=(30,0), anchor="w")

    output_string_title_label = tk.Label(root, text="Output String:", font=("Arial", 16))
    output_string_title_label.pack(pady=(20,0), padx=(30,0), anchor="w")
    output_string_label=tk.Label(root, text=initial_machine.output_string, font=("Arial", 10))
    output_string_label.pack(pady=(5,0), padx=(30,0), anchor="w")

    machine_label = tk.Label(root, text="Machine States:", font=("Arial", 16))
    machine_label.pack(pady=(20,0), padx=(30,0),anchor="w")
    
    data_structures_label = tk.Label(root, text="Data Structures:", font=("Arial", 16))
    data_structures_label.pack(pady=(20,0), padx=(30,0), anchor="w")
    stack_labels=[]
    for stack in initial_machine.stacks:
        stack_label = tk.Label(root, text=f"Stack: {stack.name}", font=("Arial", 12), justify="left")
        stack_label.pack(pady=(5,0), padx=(30,0), anchor="w")
        stack_content=tk.Frame(root, borderwidth=1, relief="solid")
        stack_content.pack(pady=(5,0), padx=(30,0), anchor="w")
        stack_content_label = tk.Label(stack_content, text=f"Contents: {"".join(stack.stack)}", font=("Arial", 10), justify="left")
        stack_content_label.pack(pady=5, padx=5, anchor="w")
        stack_labels.append([stack_content_label, stack.name])

    queue_labels=[]
    for queue in initial_machine.queues:
        queue_label = tk.Label(root, text=f"Queue: {queue.name}", font=("Arial", 12), justify="left")
        queue_label.pack(pady=(5,0), padx=(30,0), anchor="w")
        queue_content=tk.Frame(root, borderwidth=1, relief="solid")
        queue_content.pack(pady=(5,0), padx=(30,0), anchor="w")
        queue_content_label = tk.Label(queue_content, text=f"Contents: {"".join(queue.queue)}", font=("Arial", 10), justify="left")
        queue_content_label.pack(pady=5, padx=5, anchor="w")
        queue_labels.append([queue_content_label, queue.name])
    tape_labels=[]
    for tape in initial_machine.tapes:
        tape_label = tk.Label(root, text=f"Tape: {tape.name}", font=("Arial", 12), justify="left")
        tape_label.pack(pady=(5,0), padx=(30,0), anchor="w")
        tape_content=tk.Frame(root, borderwidth=1, relief="solid")
        tape_content.pack(pady=(5,0), padx=(30,0), anchor="w")
        tape_content_label = tk.Text(tape_content, font=("Arial", 10), height=5, width=110)
        tape_content_label.insert("1.0", tape.print_tape())
        tape_content_label.tag_configure("highlight", foreground="red", font=("Arial", 10, "bold"))
        if(tape.type=="1D"):
            tape_content_label.tag_add("highlight", f"1.{tape.pointer_x}", f"1.{tape.pointer_x+1}")
        elif(tape.type=="2D"):
            tape_content_label.tag_add("highlight", f"{tape.pointer_y+1}.{tape.pointer_x}", f"{tape.pointer_y+1}.{tape.pointer_x+1}")
        tape_content_label.pack(pady=5, padx=5, anchor="w")
        tape_labels.append([tape_content_label, tape.name])

    state_labels = []
    for state in initial_machine.states:
        if(state.is_initial):
            state_label = tk.Label(root, text="-> "+str(state.name), font=("Arial", 12), justify="left")
        else:
            state_label = tk.Label(root, text=str(state.name), font=("Arial", 12), justify="left")
        if(state.name==initial_machine.current_state.name):
            state_label.config(bg="lightgreen")
        else:
            state_label.config(bg="white")     
        state_labels.append([state_label,state.name])
        state_label.pack(pady=(5,0), padx=(30,0), anchor="w")
        for transition in state.transitions:
            transition_label = tk.Label(root, text=f"  {transition}", font=("Arial", 10), justify="left")
            transition_label.pack(pady=(5,0), padx=(30,0), anchor="w")

    return state_labels, stack_labels, queue_labels, tape_labels, input_string_label, output_string_label
    
    
#TODO: still needs to be implemented
def processing_step(simulate_machine, state_labels, stack_labels, queue_labels, tape_labels, input_string_label, output_string_label, timeine_label):
    print("Processing step")
    result=simulate_machine.simulate_step()
    displayed_machine=simulate_machine.get_displayed_machine()
    print("Displayed machine: ", displayed_machine)
    if(displayed_machine!="REJECTED" and displayed_machine!="ACCEPTED"):
        update_display(displayed_machine, state_labels, stack_labels, queue_labels, tape_labels, input_string_label, output_string_label, timeine_label, len(simulate_machine.machines))
    if(displayed_machine=="ACCEPTED" or displayed_machine=="REJECTED"):
        print("Simulation finished")
        #create a new window to show the result
        result_window = tk.Toplevel()
        result_window.title("Result")
        result_window.geometry("400x200")
        if(displayed_machine=="ACCEPTED"):
            result_label = tk.Label(result_window, text="Accepted", font=("Arial", 16))
            result_label.pack(pady=(20,0))
        else:
            result_label = tk.Label(result_window, text="Rejected", font=("Arial", 16))
            result_label.pack(pady=(20,0))
        
            
def initial_input():
    root = tk.Tk()
    initial_machine=Machine()
    root.title("Machine Simulation")
    root.geometry("1000x800")

    label = tk.Label(root, text="Enter the machine description:", font=("Arial", 14))
    label.pack(pady=(20,0))

    text_input = tk.Text(root, height=20, width=80)
    text_input.pack(pady=20)

    label2=tk.Label(root, text="Enter the input string:", font=("Arial", 14))
    label2.pack(pady=(30,0))

    text_input2 = tk.Entry(root, width=80)
    text_input2.pack(pady=(20,0))

    button = tk.Button(root, text="Parse", command=lambda: combined_function(initial_machine, text_input.get("1.0", tk.END), text_input2.get(), root))
    button.pack(pady=(20,0))

    root.mainloop()    


if __name__ == "__main__":
    initial_input()