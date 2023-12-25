"""
With your help, the Elves manage to find the right parts and fix all of the machines. Now, they just need to send the command to boot up the machines and get the sand flowing again.

The machines are far apart and wired together with long cables. The cables don't connect to the machines directly, but rather to communication modules attached to the machines that perform various initialization tasks and also act as communication relays.

Modules communicate using pulses. Each pulse is either a high pulse or a low pulse. When a module sends a pulse, it sends that type of pulse to each module in its list of destination modules.

There are several different types of modules:

Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives a high pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low pulse, it flips between on and off. If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.

Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules; they initially default to remembering a low pulse for each input. When a pulse is received, the conjunction module first updates its memory for that input. Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.

There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the same pulse to all of its destination modules.

Here at Desert Machine Headquarters, there is a module with a single button on it called, aptly, the button module. When you push the button, a single low pulse is sent directly to the broadcaster module.

After pushing the button, you must wait until all pulses have been delivered and fully handled before pushing it again. Never push the button if modules are still processing pulses.

Pulses are always processed in the order they are sent. So, if a pulse is sent to modules a, b, and c, and then module a processes its pulse and sends more pulses, the pulses sent to modules b and c would have to be handled first.

The module configuration (your puzzle input) lists each module. The name of the module is preceded by a symbol identifying its type, if any. The name is then followed by an arrow and a list of its destination modules. For example:

broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
In this module configuration, the broadcaster has three destination modules named a, b, and c. Each of these modules is a flip-flop module (as indicated by the % prefix). a outputs to b which outputs to c which outputs to another module named inv. inv is a conjunction module (as indicated by the & prefix) which, because it has only one input, acts like an inverter (it sends the opposite of the pulse type it receives); it outputs to a.

By pushing the button once, the following pulses are sent:

button -low-> broadcaster
broadcaster -low-> a
broadcaster -low-> b
broadcaster -low-> c
a -high-> b
b -high-> c
c -high-> inv
inv -low-> a
a -low-> b
b -low-> c
c -low-> inv
inv -high-> a
After this sequence, the flip-flop modules all end up off, so pushing the button again repeats the same sequence.

Here's a more interesting example:

broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
This module configuration includes the broadcaster, two flip-flops (named a and b), a single-input conjunction module (inv), a multi-input conjunction module (con), and an untyped module named output (for testing purposes). The multi-input conjunction module con watches the two flip-flop modules and, if they're both on, sends a low pulse to the output module.

Here's what happens if you push the button once:

button -low-> broadcaster
broadcaster -low-> a
a -high-> inv
a -high-> con
inv -low-> b
con -high-> output
b -high-> con
con -low-> output
Both flip-flops turn on and a low pulse is sent to output! However, now that both flip-flops are on and con remembers a high pulse from each of its two inputs, pushing the button a second time does something different:

button -low-> broadcaster
broadcaster -low-> a
a -low-> inv
a -low-> con
inv -high-> b
con -high-> output
Flip-flop a turns off! Now, con remembers a low pulse from module a, and so it sends only a high pulse to output.

Push the button a third time:

button -low-> broadcaster
broadcaster -low-> a
a -high-> inv
a -high-> con
inv -low-> b
con -low-> output
b -low-> con
con -high-> output
This time, flip-flop a turns on, then flip-flop b turns off. However, before b can turn off, the pulse sent to con is handled first, so it briefly remembers all high pulses for its inputs and sends a low pulse to output. After that, flip-flop b turns off, which causes con to update its state and send a high pulse to output.

Finally, with a on and b off, push the button a fourth time:

button -low-> broadcaster
broadcaster -low-> a
a -low-> inv
a -low-> con
inv -high-> b
con -high-> output
This completes the cycle: a turns off, causing con to remember only low pulses and restoring all modules to their original states.

To get the cables warmed up, the Elves have pushed the button 1000 times. How many pulses got sent as a result (including the pulses sent by the button itself)?

In the first example, the same thing happens every time the button is pushed: 8 low pulses and 4 high pulses are sent. So, after pushing the button 1000 times, 8000 low pulses and 4000 high pulses are sent. Multiplying these together gives 32000000.

In the second example, after pushing the button 1000 times, 4250 low pulses and 2750 high pulses are sent. Multiplying these together gives 11687500.

Consult your module configuration; determine the number of low pulses and high pulses that would be sent after pushing the button 1000 times, waiting for all pulses to be fully handled after each push of the button. What do you get if you multiply the total number of low pulses sent by the total number of high pulses sent?

Your puzzle answer was 919383692.

--- Part Two ---
The final machine responsible for moving the sand down to Island Island has a module attached named rx. The machine turns on when a single low pulse is sent to rx.

Reset all modules to their default states. Waiting for all pulses to be fully handled after each button press, what is the fewest number of button presses required to deliver a single low pulse to the module named rx?

Your puzzle answer was 247702167614647.
"""

from math import gcd
from functools import reduce
from collections import deque

class Module:
    def __init__(self, name):
        self.name = name
        self.destinations = []

    def add_destination(self, module):
        self.destinations.append(module)

    def receive_pulse(self, pulse, pulse_counts, source=None):
        pass

    def get_state(self):
        pass

    def get_name(self):
        return self.name

    def __repr__(self):
        return f"Module({self.name})"

class Output(Module):
    def receive_pulse(self, pulse, pulse_counts, source=None):
        # Output modules receive pulses but do not send them further
        # They act as endpoints in the pulse network
        pass

    def get_state(self):
        # Output modules have no state
        return

    def __repr__(self):
        return f"Output({self.name})"

# Adjusting the other modules to pass the source of the pulse
class Broadcaster(Module):
    def receive_pulse(self, pulse, pulse_counts, source=None):
        for module in self.destinations:
            yield (module.get_name(), pulse, self.name)
        pulse_counts[pulse] += len(self.destinations)

    def get_state(self):
        # Broadcaster doesn't have a state like FlipFlop or Conjunction, so we return None
        return None

    def __repr__(self):
        return f"Broadcaster({self.name})"


class FlipFlop(Module):
    def __init__(self, name):
        super().__init__(name)
        self.state = False  # Initially off

    def receive_pulse(self, pulse, pulse_counts, source=None):
        if pulse == "low":
            self.state = not self.state
            pulse_to_send = "high" if self.state else "low"
            for module in self.destinations:
                yield (module.get_name(), pulse_to_send, self.name)
            pulse_counts[pulse_to_send] += len(self.destinations)

    def get_state(self):
        return self.state

    def __repr__(self):
        return f"FlipFlop({self.name}, state={self.state})"

    def reset(self):
        self.state = False

class Conjunction(Module):
    def __init__(self, name):
        super().__init__(name)
        self.input_states = {}  # Tracks the most recent pulse from each input module by name

    def add_input(self, module):
        # Initializes the state of each input to low
        self.input_states[module.get_name()] = "low"

    def receive_pulse(self, pulse, pulse_counts, source=None):
        # Updates the state of the specific input that sent the pulse
        if source in self.input_states:
            self.input_states[source] = pulse

        # Checks if all inputs are high
        if all(state == "high" for state in self.input_states.values()):
            pulse_to_send = "low"
        else:
            pulse_to_send = "high"
        for module in self.destinations:
            yield (module.get_name(), pulse_to_send, self.name)

        pulse_counts[pulse_to_send] += max(1, len(self.destinations))


    def get_state(self):
        return tuple(self.input_states.items())

    def __repr__(self):
        return f"Conjunction({self.name}, input_states={self.input_states})"

    def reset(self):
        for key in self.input_states:
            self.input_states[key] = "low"

def lcm(a, b):
    return a * b // gcd(a, b)

# Ensure the add_input method of Conjunction class is correctly linking inputs
def create_module_network(config_lines):
    """
    This function constructs a network of interconnected modules based on the provided configuration.
    The configuration specifies different types of modules (like Flip-Flop, Conjunction, Broadcaster, etc.)
    and how they are connected. The function parses each line of the configuration, creating appropriate
    module objects and establishing links between them. These links determine how pulses are passed through
    the network. Special attention is given to the types of modules, as each behaves differently when
    receiving pulses. The resulting network is a representation of the entire system described in the puzzle.

    Notes:
    - I wanted to solve at least 1 problem in an OOP style, but I'm not sure if this is the best way to do it for this problem.
    - Also maybe i could have parsed the configuration in a more elegant and efficient way, but I'm too tired to think about it now.
    """

    modules = {}
    destinations_list = []
    inputs_list = []

    # Parse each line and create module objects
    for line in config_lines:
        parts = line.strip().split(" -> ")
        module_name = parts[0].strip()
        module_type = module_name[0] if module_name[0] in ['%', '&'] else ''

        # Correcting the module name if it has a type prefix
        if module_type:
            module_name = module_name[1:].strip()

        # Determine the type of the module and create it
        if module_type == "%":
            module = FlipFlop(module_name)
        elif module_type == "&":
            module = Conjunction(module_name)
        elif module_name == "broadcaster":
            module = Broadcaster(module_name)

        modules[module_name] = module

        # Prepare to add destinations and inputs
        if len(parts) > 1:
            destinations = parts[1].split(", ")
            destinations_list.append((module_name, destinations))

    # Create an Output module for each destination if it doesn't exist
    for module_name, destinations in destinations_list:
        for dest in destinations:
            if dest not in modules:
                modules[dest] = Output(dest)

    # For each Conjunction module, add its inputs
    for module_name, destinations in destinations_list:
        for dest in destinations:
            if dest in modules and isinstance(modules[dest], Conjunction):
                inputs_list.append((dest, [module_name]))

    # Add destinations to each module
    for module_name, destinations in destinations_list:
        for dest in destinations:
            if dest in modules:
                modules[module_name].add_destination(modules[dest])

    # Link inputs for Conjunction modules
    for module_name, inputs in inputs_list:
        for input_module in inputs:
            if input_module in modules:
                modules[module_name].add_input(modules[input_module])

    return modules

def simulate_button_pushes(modules, num_pushes):
    """
    This function simulates the operation of the module network when the button is pressed a specified
    number of times. Each button press initiates a sequence of pulses throughout the network. The function
    keeps track of the pulses sent (both low and high) and the state of each module after each pulse.
    It handles the complex interactions and dependencies between different modules, ensuring that pulses
    are processed in the correct order. This simulation is key to understanding the behavior of the
    system as a whole and leads to the solution for the first part of the puzzle.
    Notes:
    - I implemented a simple cycle detection algorithm to speed up the simulation, but it was not necessary
    - For my input the cycle, if it exists, is very long (more than 1000 iterations), so that piece of code was not used
    """
    pulse_counts = {"low": 0, "high": 0}
    system_states = set()
    last_pulse_counts = None

    for _ in range(num_pushes):
        pulse_queue = deque()
        pulse_queue.append(('broadcaster', 'low', None))  # Initial pulse from the button to the broadcaster
        pulse_counts['low'] += 1  # Counting the initial pulse

        while pulse_queue:
            current_module_name, pulse, source = pulse_queue.popleft()
            current_module = modules[current_module_name]

            if isinstance(current_module, Output):
                continue

            # Process the pulse and add new pulses to the queue
            for dest_module_name, pulse_to_send, source in current_module.receive_pulse(pulse, pulse_counts, source):
                pulse_queue.append((dest_module_name, pulse_to_send, source))

        # Calculate and check the current state of the system
        current_state = hash(tuple(module.get_state() for module in modules.values()))

        if current_state in system_states:
            # Cycle detected; calculate the remaining iterations
            cycle_length = len(system_states)
            remaining_cycles = num_pushes // cycle_length

            last_pulse_counts["low"] *= remaining_cycles
            last_pulse_counts["high"] *= remaining_cycles
            break
        system_states.add(current_state)
        last_pulse_counts = pulse_counts.copy()

    return last_pulse_counts["low"], last_pulse_counts["high"]

def reset_modules(modules):
    # Resetting all modules to their default state for the next simulation if needed
       for module in modules.values():
           if isinstance(module, FlipFlop) or isinstance(module, Conjunction):
               module.reset()

def simulate_until_high(modules, source_module_name, target_module_name):
    """
    This function performs a simulation to determine the minimum number of button presses needed to
    deliver a single low pulse to a specific module (named 'rx' in the puzzle). The simulation resets
    the network to its initial state and repeatedly simulates button presses, tracking the flow of pulses
    through the network. The key is to identify the specific conditions under which the 'rx' module
    receives the required pulse. This simulation continues until the desired outcome is achieved, and
    the count of button presses is returned. This process solves the second part of the puzzle.
    Notes:
    - I found out the rx is connected to a Conjunction module, and that is also connected to only Conjunction modules
    - I also found out that the number of button presses for one of those Conjunction modules is relativly small.
    - With this information I know that the rx module will receive a low pulse when all of the Conjunction modules send a high pulse
    - The number of button presses is the LCM of the number of button presses for each Conjunction module
    - I could have factorized the code to look more clean but I already spent too much time on this problem
    """

    button_presses = 0
    output_received_low = False

    while not output_received_low:
        button_presses += 1
        pulse_queue = deque()
        pulse_queue.append(('broadcaster', 'low', None))  # Initial pulse from the button
        pulse_counts = {"low": 0, "high": 0}
        pulse_counts['low'] += 1

        while pulse_queue:
            current_module_name, pulse, source = pulse_queue.popleft()
            current_module = modules[current_module_name]

            if isinstance(current_module, Output):
                continue

            for dest_module_name, pulse_to_send, source in current_module.receive_pulse(pulse, pulse_counts, source):
                if dest_module_name == target_module_name and pulse_to_send == 'high' and source == source_module_name:
                    output_received_low = True
                pulse_queue.append((dest_module_name, pulse_to_send, source))

    return  button_presses

with open("input.txt") as f:
    module_config = f.readlines()
    # Parsing the module configuration
    modules = create_module_network(module_config)
    # # Simulating 1000 button pushes
    low_pulses, high_pulses = simulate_button_pushes(modules, 1000)
    # Calculating the final result
    final_result = low_pulses * high_pulses

    # Find the module that is connected to rx
    rx_module = modules.get('rx')
    for module in modules.values():
        if rx_module in module.destinations:
            list_of_sources = list(module.input_states.keys())
            target_module_name = module.get_name()

    number_of_presses = {}
    for source in list_of_sources:
        # Resetting all modules to their default state for the next simulation
        reset_modules(modules)
        button_presses = simulate_until_high(modules, source, target_module_name)
        number_of_presses[source] = button_presses

    # Calcumate the LCM of the number of button presses
    button_presses = reduce(lcm, number_of_presses.values())

    print("First puzzle solution:", final_result)
    print("Second puzzle solution:", button_presses)