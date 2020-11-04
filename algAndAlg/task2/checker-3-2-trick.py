from collections import namedtuple
from collections import defaultdict
from enum import Enum
from random import randrange

Circuit = namedtuple('Circuit', ['gates', 'inputs', 'outputs'])
Gate = namedtuple('Gate', ['opcode', 'inputs'])

class CircuitRequirements(Enum):
    STANDARD_BASIS = 0
    NO_UNREACHABLE_GATES = 1
    
    
def read_circuit(s, options={CircuitRequirements.STANDARD_BASIS, CircuitRequirements.NO_UNREACHABLE_GATES}):
    gates = dict()
    outputs = dict()

    for line in s.splitlines():
        line = line.strip()
        if len(line) == 0:
            continue
        tokens = line.split()
        type_ = tokens[0]
        if type_ == 'GATE':
            gate = Gate(opcode=tokens[2], inputs=list(map(int, tokens[3:])))
            node_number = int(tokens[1])
            if node_number in gates:
                print('Gate at node #{node_number} specified twice')
                return None
            gates[node_number] = gate
            if CircuitRequirements.STANDARD_BASIS in options:
                basis = {'AND': 2, 'OR': 2, 'NOT': 1}
                if gate.opcode not in basis:
                    print(f'Wrong gate opcode: {gate.opcode}')
                    return None
                if len(gate.inputs) != basis[gate.opcode]:
                    print(f'Wrong number of inputs for gate #{node_number}')
                    return None
        elif type_ == 'OUTPUT':
            if len(tokens) > 3:
                print('Wrong output specification')
                return None
            k = int(tokens[1])
            if k in outputs:
                print('Same output #{k} specified twice')
                return None
            outputs[k] = int(tokens[2])
        else:
            print('Wrong file format')
            return None
        

    if sorted(gates) != list(range(min(gates), max(gates) + 1)):
        print('Gate numbers do not form a continuous interval')
        return None
    
    for k in outputs:
        if k > max(gates):
            print(f'Output #{k} is neither a gate nor an input')

    for gate in gates:
        for k in gates[gate].inputs:
            if k > max(gates):
                print(f'Input #{k} of gate #{gate} is invalid')
                return None
    
    if CircuitRequirements.NO_UNREACHABLE_GATES in options:
        reachable_vertices = set()
        def set_as_reachable(node):
            reachable_vertices.add(node)
            if node in gates:
                for k in gates[node].inputs:
                    if k not in reachable_vertices:
                        set_as_reachable(k)
        for output in outputs.values():
            set_as_reachable(output)
        if not set(gates) <= reachable_vertices:
            print('Some gates are not reachable from the output nodes. These should be eliminated from the circuit.')
            return None
            
    def has_reachable_cycles(node):
        dfs_stack = [node]
        dfs_stack_set = {node}
        visited_nodes = set()
        while dfs_stack != []:
            node = dfs_stack[-1]
            visited_nodes.add(node)
            if node in gates:
                for k in gates[node].inputs:
                    if k in dfs_stack_set:
                        return True
                    if k not in visited_nodes:
                        dfs_stack.append(k)
                        dfs_stack_set.add(k)
                        break
                else:
                    dfs_stack_set.remove(dfs_stack.pop())
            else:
                dfs_stack_set.remove(dfs_stack.pop())
        return False
            
    if any(map(has_reachable_cycles, outputs.values())):
        print('A cycle found that is reachable from a circuit output. Cannot evaluate such circuit.')
        return None
    
    inputs = sorted(range(0, min(gates)))
    return Circuit(gates=gates, outputs=outputs, inputs=inputs)


def get_depth(circuit):
    depths = dict()
    def get_depth_at_node(node):
        if node in depths:
            return depths[node]
        if node not in circuit.gates:
            return 0
        depths[node] = 1 + max(map(get_depth_at_node, circuit.gates[node].inputs))
        return depths[node]
    return max(map(get_depth_at_node, circuit.outputs.values()))


def get_size(c):
    return len(c.gates)

def evaluate_circuit(circuit, input_values, is_vectorized=False):
    evaluations = dict()
    for i, v in enumerate(input_values):
        evaluations[i] = v
    
    if is_vectorized:
        operations = {
            'AND': (lambda x,y: x & y), 
            'OR': (lambda x,y: x | y), 
            'NOT': (lambda x: 0xFFFF ^ x)
        }
    else:
        operations = {
            'AND': min, 
            'OR': max, 
            'NOT': (lambda x: 1-x)
        }
    
    def evaluate_at_node(node):
        if node in evaluations:
            return evaluations[node]
        gate = circuit.gates[node]
        evaluations[node] = operations[gate.opcode](*map(evaluate_at_node, gate.inputs))
        return evaluations[node]

    for node in circuit.outputs.values():
        evaluate_at_node(node)
    return evaluations


def randbinary(n, force_leading_one=False):
    r = randrange(0, 2**n) | (2**n)
    r = list(map(int, bin(r)[3:]))
    if force_leading_one:
        r[-1] = 1
    return r

def list_to_number(t):
    return int(''.join(map(str, reversed(t))), base=2)
    
def addbinary(a, b, c=[0]):
    t = list_to_number(a) + list_to_number(b)
    t += list_to_number(c)
    return t

def check_3_2_trick(circuit, n):
    a = randbinary(n)
    b = randbinary(n)
    c = randbinary(n)
    evals = evaluate_circuit(circuit, a + b + c)
    x = [evals[circuit.outputs[k]] for k in range(0, n+1)]
    y = [evals[circuit.outputs[k]] for k in range(n+1, 2*n+2)]
    return addbinary(a,b,c) == addbinary(x,y)

def check(reply, n):
    c = read_circuit(reply)
    return all(check_3_2_trick(c, n) for _ in range(n)) and get_depth(c) <= 5 and get_size(c) <= 12*n + 1