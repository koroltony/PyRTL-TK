import pyrtl

def barrel_shifter(inp, a, b, c, l1, l2, l3):
    with pyrtl.conditional_assignment:
        with inp == 0b00:
            b.next |= a
            c.next |= b
            a.next |= c
        with inp == 0b01:
            b.next |= l2
            c.next |= l3
            a.next |= l1
        with inp == 0b10:
            b.next |= c
            c.next |= a
            a.next |= b
        with inp == 0b11:
            a.next |= 0
            b.next |= 0
            c.next |= 0

# inputs
inp = pyrtl.Input(2, 'inp')
l1 = pyrtl.Input(1, 'l1')
l2 = pyrtl.Input(1, 'l2')
l3 = pyrtl.Input(1, 'l3')

# outputs
a = pyrtl.Register(1, 'a')
b = pyrtl.Register(1, 'b')
c = pyrtl.Register(1, 'c')

# Define barrel shifter module
barrel_shifter(inp, a, b, c, l1, l2, l3)

# variables for selector inputs
shift_left = 0b10
load_data = 0b01
shift_right = 0b00
clear_data = 0b11

# How many test cycles?
num_steps = 5

# How many operations per cycle?
num_ops = 6

# Define the data inputs for multiple simulations
data_inputs = [
    {'l1': 1, 'l2': 0, 'l3': 1},
    {'l1': 0, 'l2': 1, 'l3': 0},
    {'l1': 1, 'l2': 0, 'l3': 1},
    {'l1': 0, 'l2': 0, 'l3': 0},
    {'l1': 1, 'l2': 1, 'l3': 1},
]

# Create a sim trace
sim_trace = pyrtl.SimulationTrace()

# Run the simulation
for step in range(num_steps):
    sim = pyrtl.Simulation(tracer=sim_trace)

    # Simulate load operation
    sim.step({inp: load_data, l1: data_inputs[step]['l1'], l2: data_inputs[step]['l2'], l3: data_inputs[step]['l3']})

    # Simulate shift left operation
    sim.step({inp: shift_left, l1: data_inputs[step]['l1'], l2: data_inputs[step]['l2'], l3: data_inputs[step]['l3']})

    # Simulate shift right operation
    sim.step({inp: shift_right, l1: data_inputs[step]['l1'], l2: data_inputs[step]['l2'], l3: data_inputs[step]['l3']})

    # Simulate shift right operation again
    sim.step({inp: shift_right, l1: data_inputs[step]['l1'], l2: data_inputs[step]['l2'], l3: data_inputs[step]['l3']})

    # Simulate clear operation
    sim.step({inp: clear_data, l1: data_inputs[step]['l1'], l2: data_inputs[step]['l2'], l3: data_inputs[step]['l3']})

# Define correct outputs for first data_input dictionary
expected_outputs = [
    {'a': 0, 'b': 0, 'c': 0},
    {'a': 1, 'b': 0, 'c': 1},
    {'a': 0, 'b': 1, 'c': 1},
    {'a': 1, 'b': 0, 'c': 1},
    {'a': 1, 'b': 1, 'c': 0},
    {'a': 0, 'b': 0, 'c': 0},
]

#optional embedded waveform generator of PyRTL (looks bad)
sim_trace.render_trace()

# Assertions for the correct output
for i in range(num_ops):
    assert sim_trace.trace['a'][i] == expected_outputs[i]['a'], f"Test {i + 1}: Expected a={expected_outputs[i]['a']}, but got a={sim_trace.trace['a'][i]}"
    assert sim_trace.trace['b'][i] == expected_outputs[i]['b'], f"Test {i + 1}: Expected b={expected_outputs[i]['b']}, but got b={sim_trace.trace['b'][i]}"
    assert sim_trace.trace['c'][i] == expected_outputs[i]['c'], f"Test {i + 1}: Expected c={expected_outputs[i]['c']}, but got c={sim_trace.trace['c'][i]}"

# If all the tests pass
print("All test cases passed successfully.")
