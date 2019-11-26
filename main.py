import sys
from instruction_parser import parse_instructions
import instructions

def main():
    # Checks that strategy argument is given
    if(len(sys.argv) < 2 or sys.argv[1] not in ['fifo', 'lru']):
        print('Forma de uso: %s (fifo|lru)' % sys.argv[0])
        exit()
    print('Utilizando ', sys.argv[1], ' como estrategia de remplazo')
    """ 
    Bool that sets strategy for simulation
    true - uses fifo
    false - uses lru		 
    """
    # Sets strategy on instructions
    instructions.strategy = True if sys.argv[1] == 'fifo' else False

    parsed_instructions = parse_instructions()
    for instruction in parsed_instructions:
        print(' '.join(str(x) for x in instruction))
    # Add calls to each instruction
        if instruction[0] == 'P':
            instructions.P(instruction[1], instruction[2])
        elif instruction[0] == 'A':
            instructions.A(instruction[1], instruction[2], instruction[3])
        elif instruction[0] == 'E':
            instructions.E()

main()