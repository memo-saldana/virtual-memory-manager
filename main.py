import sys
from instruction_parser import parse_instructions

""" 
	Bool that sets strategy for simulation
	true - uses fifo
	false - uses lru		 
"""
strategy

def main():
	if(len(sys.argv) < 2 or sys.argv[1] not in ['fifo', 'lru']):
		print('Forma de uso: %s (fifo|lru)' % sys.argv[0])
		exit()
	print('script with name ', sys.argv[0])
	print('replacement strategy ', sys.argv[1])
	strategy = True if argv[1] == 'fifo' else False

	instructions = parse_instructions()
	for instruction in instructions:
		print(instruction)
		# Add calls to each instruction
main()