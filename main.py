import sys
from instruction_parser import parse_instructions
from instructions import E

def main():
	if(len(sys.argv) < 2 or sys.argv[1] not in ['fifo', 'lru']):
		print('Forma de uso: %s (fifo|lru)' % sys.argv[0])
		exit()
	print('script with name ', sys.argv[0])
	print('replacement strategy ', sys.argv[1])
	""" 
		Bool that sets strategy for simulation
		true - uses fifo
		false - uses lru		 
	"""
	strategy = True if sys.argv[1] == 'fifo' else False

	instructions = parse_instructions()
	for instruction in instructions:
		print(' '.join(str(x) for x in instruction))
		# Add calls to each instruction
		if(instruction[0]=='E'):
			E()
main()