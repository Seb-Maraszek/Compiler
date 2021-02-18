def saveLoadedValueToMemory(placeInMemory):
    return "GET {} \n".format(placeInMemory)


def putLoadedValue(placeInMemory):
    return "PUT {}\n".format(placeInMemory)


def loadValueFromMemoryToRegister(register, placeInMemory):
    return "LOAD {} {}\n".format(register, placeInMemory)


def storeValueFromRegisterToMemory(placeInMemory, register):
    return "STORE {} {}\n".format(placeInMemory, register)


def addValuesFromRegisters(v1, v2):
    return "ADD {} {}\n".format(v1, v2)


def subValuesFromRegisters(v1, v2):
    return "SUB {} {}\n".format(v1, v2)


def resetRegister(register):
    return "RESET {}\n".format(register)


def incrementValueInRegister(register):
    return "INC {}\n".format(register)


def decrementValueInRegister(register):
    return "DEC {}\n".format(register)


def shiftRight(register):
    return "SHR {}\n".format(register)


def shiftLeft(register):
    return "SHL {}\n".format(register)


def jumpLines(lines):
    return "JUMP {}\n".format(lines)


def jumpIfZero(register, lines):
    return "JZERO {} {}\n".format(register, lines)


def jumpIfOdd(register, lines):
    return "JODD {} {}\n".format(register, lines)


def saveValueFromRegisterToMemory(r, m):
    return "STORE {} {}\n".format(r, m)


def generateNumberInRegister(number, register):
    commands = ""

    while number != 0:
        if number % 2 == 0:
            number = number // 2
            commands = "SHL {}\n".format(register) + commands
        else:
            number = number - 1
            commands = "INC {}\n".format(register) + commands
    commands = "RESET {} \n".format(register) + commands
    return commands



def greaterEqualGenerator():
    return "RESET d\n" + \
           "ADD d c\n" + \
           "SUB d b\n" + \
           "JZERO d 2\n"


def lessEqualGenerator():
    return "RESET d\n" + \
           "ADD d c\n" + \
           "SUB d b\n" + \
           "JZERO d 2\n"


def lessThanGenerator():
    return "RESET d\n" + \
           "ADD d c\n" + \
           "INC d\n" + \
           "SUB d b\n" + \
           "JZERO d 2\n"


def greaterThanGenerator():
    return "RESET d\n" + \
           "ADD d c\n" + \
           "INC d\n" + \
           "SUB d b\n" + \
           "JZERO d 2\n"


def equalGenerator():
    return "RESET d\n" + \
           "RESET e\n" + \
           "ADD d b\n" + \
           "SUB d c\n" + \
           "JZERO d 2\n" + \
           "INC e\n" + \
           "RESET d\n" + \
           "ADD d c\n" + \
           "SUB d b\n" + \
           "JZERO e 2\n" + \
           "JUMP 2\n" + \
           "JZERO d 2\n"


def notEqualGenerator():
    return "RESET d\n" + \
           "RESET e\n" + \
           "ADD d b\n" + \
           "SUB d c\n" + \
           "JZERO d 2\n" + \
           "INC e\n" + \
           "RESET d\n" + \
           "ADD d c\n" + \
           "SUB d b\n" + \
           "JZERO e 2\n" + \
           "JUMP 2\n" + \
           "JZERO d 2\n" + \
           "JUMP 2\n"




def divideGenerator():
    return "JZERO c 25\n" + \
           "RESET d\n" + \
           "INC d\n" + \
           "RESET a\n" + \
           "ADD a b\n" + \
           "SUB a c\n" + \
           "JZERO a 4\n" + \
           "SHL c\n" + \
           "SHL d\n" + \
           "JUMP -6\n" + \
           "RESET e\n" + \
           "ADD e b\n" + \
           "RESET b\n" + \
           "RESET a\n" \
           "ADD a c\n" + \
           "SUB a e\n" + \
           "JZERO a 2\n" + \
           "JUMP 3\n" + \
           "SUB e c\n" + \
           "ADD b d\n" + \
           "SHR c\n" + \
           "SHR d\n" + \
           "JZERO d 2\n" + \
           "JUMP -10\n" + \
           "JUMP 2\n" + \
           "RESET b\n"


def moduloGenerator():
    return "JZERO c 24\n" + \
           "RESET d\n" + \
           "INC d\n" + \
           "RESET a\n" + \
           "ADD a b\n" + \
           "SUB a c\n" + \
           "JZERO a 4\n" + \
           "SHL c\n" + \
           "SHL d\n" + \
           "JUMP -6\n" + \
           "RESET e\n" + \
           "ADD e b\n" + \
           "RESET b\n" + \
           "RESET a\n" + \
           "ADD a c\n" + \
           "SUB a e\n" + \
           "JZERO a 2\n" + \
           "JUMP 3\n" + \
           "SUB e c\n" + \
           "ADD b d\n" + \
           "SHR c\n" + \
           "SHR d\n" + \
           "JZERO d 4\n" + \
           "JUMP -10\n" + \
           "RESET b\n" + \
           "JUMP 4\n" + \
           "RESET b\n" + \
           "ADD b e\n"


def optimizeMultiplying():
    return "RESET d\n" +\
           "ADD d b\n" +\
           "SUB d c\n" +\
           "JZERO d 7\n"+\
           "RESET e\n"+\
           "ADD e c\n"+\
           "RESET c\n"+\
           "ADD c b\n"+\
           "RESET b\n"+\
           "ADD b e\n"

def multiplyGenerator():
    return "RESET d\n" + \
           "RESET e\n" + \
           "JODD b 2\n" + \
           "INC e\n" + \
           "JZERO b 11\n"+ \
           "JZERO e 2\n" + \
           "JUMP 2\n" + \
           "ADD d c\n" + \
           "SHL c\n" + \
           "SHR b\n" + \
           "JODD b 3\n" + \
           "INC e\n" + \
           "JUMP 2\n" + \
           "RESET e\n" + \
           "JUMP -10\n" + \
           "RESET b\n" + \
           "ADD b d\n"
