import os

def parse_instructions():
    instructions = []
    # Input instruction file
    user_input = input('Ingresa el nombre (PATH) del archivo de instrucciones: ')
    file_path = user_input.rstrip('\r')

    # Check that instruction file exists before parsing
    if not os.path.isfile(file_path):
        print('El archivo no existe. Revisa el nombre ingresado.')
        print('Terminando ejecución por error de input.')

        exit()
    
    with open(file_path.rstrip('\r')) as file:
        # Read all lines, and split them into an array, with ith line at lines[i]
        lines = file.read().splitlines()
        """
            Possible options
            A - 3 args, all numbers
            P - 2 args, all numbers
            L - 1 arg, number
            F - 0 args
            E - 0 args
            C - all comments
        """
        for i, line in enumerate(lines):
            words = ' '.join(line.split()).split(' ')
            # Manage all valid cases
            if words[0] == 'A':
                # Checks instruction arguments
                if(len(words) < 4):
                    print('Cantidad inválida de argumentos en línea ', i+1, '.', sep="")
                    print('Instrucción \'A\' espera 3 argumentos, recibió ', len(words)-1,'.', sep="")
                    print('No se ejecutará esta instrucción.')
                else:
                    instruction = [words[0]]
                    # Tries to convert to number and adds to parsed instruction
                    try:
                        instruction.append(int(words[1]))
                        instruction.append(int(words[2]))
                        instruction.append(int(words[3]))
                        if instruction[3] not in [0,1]:
                            print("El argumento 3 es inválido, esperando (0|1), se recibió ", instruction[3])
                        else:
                            instructions.append(instruction)
                    except ValueError:
                        print("Uno de los argumentos en la línea", i+1, "no es válido.", sep="")
                        print('No se ejecutará esta instrucción.')
                        exit()

            elif words[0] == 'P':
                # Checks instruction arguments
                if(len(words) < 3):
                    print('Cantidad inválida de argumentos en línea ', i+1, '.', sep="")
                    print('Instrucción \'P\' espera 3 argumentos, recibió ', len(words)-1,'.', sep="")
                    print('No se ejecutará esta instrucción.')
                else:                
                    instruction = [words[0]]
                    # Tries to convert to number and adds to parsed instruction
                    try:
                        instruction.append(int(words[1]))
                        instruction.append(int(words[2]))
                        instructions.append(instruction)
                    except ValueError:
                        print("Uno de los argumentos en la línea", i+1, "no es válido.")
                        print('No se ejecutará esta instrucción.')
            elif words[0] == 'L':
                # Checks instruction arguments
                if(len(words) < 2):
                    print('Cantidad inválida de argumentos en línea ', i+1, '.', sep="")
                    print('Instrucción \'L\' espera 3 argumentos, recibió ', len(words)-1,'.', sep="")
                    print('No se ejecutará esta instrucción.')
                else:
                    instruction = [words[0]]
                    # Tries to convert to number and adds to parsed instruction
                    try:
                        instruction.append(int(words[1]))
                        instructions.append(instruction)
                    except ValueError:
                        print("Uno de los argumentos en la línea", i+1, "no es válido.")
                        print('No se ejecutará esta instrucción.')
            elif words[0] == 'C':
                instruction = [words[0]]
                # Joins comment that will be printed out and adds it to the instruction
                instruction.append(' '.join(words[1::]))
                instructions.append(instruction)
            elif words[0]== 'E':
                instruction = [words[0]]
                instructions.append(instruction)
            elif words[0] == 'F':
                instruction = [words[0]]
                instructions.append(instruction)
            else: 
                # Manage invalid instruction
                print("Instrucción inválida en la línea ", i+1, ".", sep="")
                print('No se ejecutará esta instrucción.')
        return instructions