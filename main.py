import sys
from instruction_parser import parse_instructions


def main():
	if(len(sys.argv) < 2 or sys.argv[1] not in ['fifo', 'lru']):
		print('Forma de uso: %s (fifo|lru)' % sys.argv[0])
		exit()
	print('script with name ', sys.argv[0])
	print('replacement strategy ', sys.argv[1])
	instructions = parse_instructions()
	for instruction in instructions:
		print(instruction)
main()