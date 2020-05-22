import sys


class CPU:
    def __init__(self):
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.flag = 0

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def load(self, path):
        address = 0
        p = []

        try:
            with open(path) as f:
                for line in f:
                    instruction = line.split('#', 1)[0].strip()
                    if len(instruction):
                        p.append(int(instruction, 2))
        except FileNotFoundError:
            print("Error: file not found")
            sys.exit(2)

        for instruction in p:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        if op == "CMP":
            # if reg_a and reg_b are equal, set the flag to one
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 1

        else:
            raise Exception("Invalid code")

    def run(self):
        self.running = True

        def stop():
            self.running = False

        def load_immediate():
            self.reg[op_a] = op_b

        def print_numeric():
            print(self.reg[op_a])

        def compare():
            self.alu("CMP", op_a, op_b)

        def jump():
            self.pc = self.reg[op_a]

        def jump_eq():
            # if the equal flag is true
            equal = (self.flag & 1)
            # jump to the address stored in the register
            if equal:
                self.pc = self.reg[op_a]
            # increment counter
            else:
                self.pc += 2

        def jump_ne():
            # if the equal flag is false jump to address in the given register
            equal = (self.flag & 1)
            if not equal:
                self.pc = self.reg[op_a]
            else:
                self.pc += 2

        bt = {
            0b00000001: stop,
            0b10000010: load_immediate,
            0b01000111: print_numeric,
            0b10100111: compare,
            0b01010100: jump,
            0b01010101: jump_eq,
            0b01010110: jump_ne,
        }

        while self.running:
            instruction = self.ram[self.pc]
            op_count = (instruction & 0b11000000) >> 6
            sets_pc = (instruction & 0b00010000) >> 4

            op_a = None
            op_b = None
            if op_count > 0:
                op_a = self.ram[self.pc + 1]
            if op_count > 1:
                op_b = self.ram[self.pc + 2]

            command = bt.get(instruction)

            if not command:
                print(f'Unknown instruction')
                sys.exit(1)
            command()
            if not sets_pc:
                self.pc += (op_count + 1)