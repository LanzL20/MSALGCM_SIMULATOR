from machine import Machine, Status
class Simulation:
    machines = []
    displayed_machine=0
    rejected_machines=[]
    accepted_machines=[]
    number_of_steps=0
    status=None

    def __init__(self, machine):
        #multiple start states stuff later na.
        print("HI")
        machine.start()
        self.machines.append(machine)

    def simulate_step(self):
        if self.number_of_steps==5000:
            print("Maximum number of steps reached")
            return
        new_machines=[]
        for machine in self.machines:
            machines_generated=[]
            machines_generated = machine.step()
            if(machines_generated!= None):
                new_machines.extend(machines_generated)
        self.machines.extend(new_machines)
        #TODO: add a check if the machine is finished/rejected or still running
        for machine in self.machines:
            if machine.status==Status.REJECTED:
                self.rejected_machines.append(machine)
                self.machines.remove(machine)
            elif machine.status==Status.ACCEPTED:
                self.accepted_machines.append(machine)
                self.machines.remove(machine)
        self.number_of_steps+=1
        if(len(self.accepted_machines)>0):
            print("Accepted")
            self.status=Status.ACCEPTED
            for i in range(len(self.machines)):
                self.machines.pop(i)

        return 1
        
        

    def get_displayed_machine(self):
        if(self.displayed_machine>=len(self.machines)):
            self.displayed_machine=0
        if len(self.machines)>0:
            return self.machines[self.displayed_machine]
        if(len(self.machines)==0 and len(self.accepted_machines)==0):
            print("All machines rejected")
            return "REJECTED"
        if(len(self.machines)==0 and len(self.accepted_machines)>0):
            print("Accepted")
            return "ACCEPTED"
        

                
        #idk if need but can be useful for removing redundant machines
        #self.machines = list(set(self.machines))
