from time import gmtime, strftime
from termcolor import colored, cprint

class Opcode:
	def __init__(self, name, code = '', numOperands = 0):
		self.name = name
		self.code = code
		self.numOperands = numOperands

	def __eq__(self, o):
		return self.name == o.name



class Token:
	def __init__(self, name = '', address = ''):
		self.name = name
		self.address = address

	def __str__(self):
		return 'Name: ' + self.name +  ' | Address: ' + str(self.address)

	def __eq__(self, o):
		return o.name == self.name


class Label(Token):
	pass

class Symbol(Token):
	def __init__(self, name = '', address = '', value = 0):
		super().__init__(name, address);
		self.value = value
	def __str__(self):
		return 'Name: ' + self.name +  ' | Address: ' + str(self.address) + ' | Value: ' + str(self.value)


class Literal(Token):
	def __init__(self, name = '', address = '', value = 0):
		super().__init__(name, address);
		self.value = value
	def __str__(self):
		return 'Name: ' + self.name +  ' | Address: ' + str(self.address) + ' | Value: ' + str(self.value)


class Instruction:
	def __init__(self, address, opcode, operand = None):
		self.address = address
		self.opcode = opcode
		self.operand = operand

	def __str__(self):
		if self.opcode.numOperands == 0:
			return str(self.address) + ' : ' + self.opcode.name
		else:
			return str(self.address) + ' : ' + self.opcode.name + ' ' + self.operand.name + ' ( ' + str(self.operand.address) + ' )'




labels = []
symbols = []
literals = []
instructions = []

opcodes = [
	Opcode('CLA', '0000', 0),
	Opcode('LAC', '0001', 1),
	Opcode('SAC', '0010', 1),
	Opcode('ADD', '0011', 1),
	Opcode('SUB', '0100', 1),
	Opcode('BRZ', '0101', 1),
	Opcode('BRN', '0110', 1),
	Opcode('BRP', '0111', 1),
	Opcode('INP', '1000', 1),
	Opcode('DSP', '1001', 1),
	Opcode('MUL', '1010', 1),
	Opcode('DIV', '1011', 1),
	Opcode('STP', '1100', 0),
]


def binLen(n, length):
	s = bin(n)[2:]
	s =  ((length - len(s)) * '0') + s
	return s	

def reportError(msg, eType = 1):
	t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	err = ''

	if eType == 1:
		err += '[ERROR]\n' + msg  + '\n'
	elif eType == 0:
		err += '[WARNING]\n' + msg + '\n'

	if eType == 1:
		cprint('\n'+err, 'white', 'on_red', attrs=['bold'])
	elif eType == 0:
		cprint('\n'+err, 'grey', 'on_yellow', attrs=['bold'])

	err = '\n\n'+ '['+ t +']\n' + err
	errFile = open('./messages.log', 'a')
	errFile.writelines(err)
	errFile.close()
	if eType == 1:
		exit()


def setup(line):	
	if not line:
		reportError('Can not assemble an empty file')		

	elems = line.split(' ')
	if elems[0].upper() == 'START':
		if len(elems) < 2:
			reportError('Start address not provided. Staring at 0', 0)
			return [0, True]
		else:
			if elems[1].isnumeric() and int(elems[1]) < 255 and int(elems[1]) >= 0:
				return [int(elems[1]), True]
			else:
				reportError('Invalid start address provided')
	else:
		reportError('Start statement missing. Staring at 0', 0)
		return [0, False]


def cleanUp(line):
	line = line.strip()
	line = line.split(' ')
	while '' in line:
		line.remove('')
	
	line = ' '.join(line)
	return line


def findOpcode(txt):
	o = Opcode(txt)
	
	try:
		opcode = opcodes[opcodes.index(o)]
		return opcode
	except:
		return None

def findLiteral(txt):
	l = Literal(txt)
	
	try:
		literal = literals[literals.index(l)]
		return literal
	
	except:
		return None

def findSymbol(txt):
	s = Symbol(txt)
	
	try:
		symbol = symbols[symbols.index(s)]
		return symbol
	
	except:
		return None


def findLabel(txt):
	l = Label(txt)
	
	try:
		label = labels[labels.index(l)]
		return label
	
	except:
		return None



def isValidToken(token):
	if not token[0].isalpha():
		return [False, 'Invalid token name ' + token]
	
	for c in token:
		if (not c.isalnum()) and  c != '_':
			return [False, 'Invalid literal name ' + token]

	if findLabel(token) is None and findLiteral(token) is None and findSymbol(token) is None:
		if findOpcode(token.upper()) is None:
			return [True]
		else:
			return [False, 'Token name ' + token + ' is an Opcode']		
	else:
		return [False, 'Token name ' + token + ' is already defined']		


def getUndefinedTokens():
	res = []
	for ins in instructions:
		if ins.opcode.numOperands == 0:
			continue

		token = ins.operand.name
		if ins.opcode.name[:2] == 'BR':
			lab = findLabel(token)
			if lab is None:
				if token not in res:
					res.append(token)
			else:
				ins.operand = lab	
		
		else:
			lit = findLiteral(token)
			symb = findSymbol(token)

			if symb is None and lit is None:
				if token not in res:
					res.append(token)
			else:
				if symb is None:
					ins.operand = lit
				else:
					ins.operand = symb

	return res

# Processes First pass line by line
def processLine(line, lc, endFound):
	elems = line.split(' ')
	
	# Check opcode
	opcode = findOpcode(elems[0].upper())
	
	# To ignore empty lines and comments
	if elems == [''] or elems[0][0] == ';':
		return [lc, False]

	# Check END
	elif elems[0].upper() == 'END':
		if endFound:
			reportError('Multiple END statements found. Can only have one end')
		else:
			return [lc, True]

	# Check valid Opcode
	elif opcode is not None:
		if endFound:
			reportError('Only DS and DC statements allowed after end')
		
		if (len(elems) - 1 == opcode.numOperands) or (len(elems) - 1 > opcode.numOperands and elems[opcode.numOperands+1][0] == ';'):
			if opcode.numOperands == 0:
				ins = Instruction(lc, opcode)
				lc += 4
			else:
				ins = Instruction(lc, opcode, Token(elems[1]))
				lc += 12
			instructions.append(ins)
		
		else: 
			reportError('Invalid number of operands given for the Instruction ' + opcode.name + '\n'+ str(len(elems) - 1) + ' operand(s) given but ' + str(opcode.numOperands) + ' were expected')

		

	# Symbol declaration
	elif elems[0].upper() == 'DS':
		
		if len(elems) != 2 and len(elems) != 3:
			reportError('Invalid syntax to declare symbol')
			return	
		
		valid = isValidToken(elems[1])
		if not valid[0]:
			reportError(valid[1])

		val = 0

		if len(elems) == 3:
			if elems[2].isnumeric() and int(elems[2]) <= 127 and int(elems[2]) >= -128:
				val = int(elems[2])
			else:
				reportError('Invalid value given for symbol ' + elems[1])


		symbols.append(Symbol(elems[1], lc, val))
		lc += 4

	# Literal declaration
	elif elems[0].upper() == 'DC':

		if not len(elems) == 3:
			reportError('Invalid syntax to declare literal')
		elif not (elems[2].isnumeric() and int(elems[2]) <= 127 and int(elems[2]) >= -128):
			reportError('Invalid value given for literal ' + elems[1])
		
		valid = isValidToken(elems[1])

		if not valid[0]:
			reportError(valid[1])

		literals.append(Literal(elems[1], lc, int(elems[2])))
		lc += 4
	
	# Label declaration
	elif elems[0][-1] == ':':
		
		if endFound:
			reportError('Only DS and DC statements allowed after end')
		
		valid = isValidToken(elems[0][:-1])
		if not valid[0]:
			reportError(valid[1])
		
		labels.append(Label(elems[0][:-1], lc))
		newLine = ' '.join(elems[1:])
		return processLine(newLine, lc, endFound)

	else:
		reportError('Invalid Opcode at "'+line+'"')
	return [lc, False]

def printTables():
	cprint('\nLITERALS', 'white', 'on_blue', attrs=['bold'])
	for l in literals:
		print(l)

	cprint('\nSYMBOLS', 'white', 'on_blue', attrs=['bold'])
	for l in symbols:
		print(l)

	cprint('\nLABELS', 'white', 'on_blue', attrs=['bold'])
	for l in labels:
		print(l)

	cprint('\nINSTRUCTIONS', 'white', 'on_blue', attrs=['bold'])

	for l in instructions:
		print(l)


def secondPass(fileName):
	newFile = fileName.split('.')
	if len(newFile) == 1:
		newFile = newFile[0] + '.bin'
	else:
		newFile = '.'.join(newFile[: -1]) + '.bin'

	file = open(newFile, 'w')
	for ins in instructions:
		if ins.opcode.numOperands == 1:
			s = ins.opcode.code + ' ' + binLen(ins.operand.address, 8)
		else:
			s = ins.opcode.code
		
		s += '\n'
		file.write(s)
	
	file.close()
	return newFile


try:
	fileName = input('Enter the file name of the Assembly code: ')
	inp = open(fileName, 'r')

except:
	reportError('File not found')


line = cleanUp(inp.readline())
i = 0
while not bool(line) and i < 100:	
	line = cleanUp(inp.readline())
	i += 1

line = cleanUp(line)
setupRes = setup(line)

if setupRes[1]:
	line = inp.readline()

lc = setupRes[0]
endFound = False

while bool(line):

	if lc > 255:
		reportError('Not enough memory for program. Program can not exceed 255 bits')

	line = cleanUp(line)
	lc = processLine(line, lc, endFound)
	if lc[1]:
		endFound = True
	
	lc = lc[0]
	
	line = inp.readline()

if not endFound:
	reportError('End of program not found')

err = getUndefinedTokens()
if len(err) != 0:
	reportError('Undefned tokens: ' + ', '.join(err))

printTables()

# Second Pass
newFile = secondPass(fileName)

cprint('\nSUCCESS!\nSaved machine code in '+newFile, 'grey', 'on_green', attrs=['bold'])
print()
