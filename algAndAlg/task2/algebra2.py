import numpy as np


def add_command(buffer: str, command: str):
    buffer += command + '\n'
    return buffer


def get_command(output_gate, operation, input_1, input_2=None):
    command = "GATE {} {} {} {}"
    return command.format(output_gate, operation, input_1, "" if input_2 is None else input_2).strip()


def output_command(number, gate):
    return "OUTPUT {} {}".format(number, gate)


def make_xor(input_1, input_2, buffer, next_v):
    cm1 = get_command(next_v, "AND", input_1, input_2)
    cm2 = get_command(next_v + 1, "OR", input_1, input_2)
    cm3 = get_command(next_v + 2, "NOT", next_v)
    cm4 = get_command(next_v + 3, "AND", next_v + 2, next_v + 1)

    buffer = add_command(buffer, cm1)
    buffer = add_command(buffer, cm2)
    buffer = add_command(buffer, cm3)
    buffer = add_command(buffer, cm4)

    return next_v + 4, next_v, buffer


if __name__ == '__main__':
    n = int(input())
    vertixes = np.arange(3 * n)

    next_v = 3 * n

    buffer = ""
    output_buffer = ""
    cur_number_output = 0

    output_gates_x = []
    output_gates_y = []

    for i in range(n):
        a_i, b_i, c_i = vertixes[i::n]
        next_v, desyatki_a_b, buffer = make_xor(a_i, b_i, buffer, next_v)
        next_v, desyatki_a_b_c, buffer = make_xor(next_v - 1, c_i, buffer, next_v)
        output_gates_x.append(str(next_v - 1))
        buffer += get_command(next_v, "OR", desyatki_a_b, desyatki_a_b_c) + '\n'
        output_gates_y.append(str(next_v))
        next_v += 1

        if len(output_gates_y) == n:
            buffer += get_command(next_v, "NOT", 0) + '\n'
            next_v += 1
            buffer += get_command(next_v, "AND", next_v - 1, 0) + '\n'
            output_gates_y.insert(0, str(next_v))
            next_v += 1

        if len(output_gates_x) == n:
            output_gates_x.append(str(next_v - 1))


    output_buffer = ""
    for idx, value in enumerate(output_gates_x + output_gates_y):
        output_buffer += "OUTPUT {} {}".format(idx, value) + '\n'

    print(buffer + output_buffer.rstrip('\n'))

