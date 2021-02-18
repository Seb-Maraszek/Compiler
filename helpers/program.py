from enum import Enum
from typing import Any, List
from helpers.generator import *
from dataclasses import dataclass, field

memoryCount = 1
programVariables = {}


class ArithmeticTypes(Enum):
    PLUS = "PLUS"
    MINUS = "MINUS"
    DIV = "DIV"
    MULT = "MULT"
    MOD = "MOD"


class ValueTypes(Enum):
    ID = "PIDENTIFIER"
    NUMBER = "NUMBER"
    ARRAY = "ARRAY"


class ConditionTypes(Enum):
    EQ = "EQ"
    NEQ = "NEQ"
    GEQ = "GEQ"
    LEQ = "LEQ"
    LT = "LT"
    GT = "GT"


class ConditionCommandTypes(Enum):
    IF = "IF"
    IF_ELSE = "IF_ELSE"
    WHILE = "WHILE"
    REPEAT = "REPEAT"


@dataclass
class Error:
    message: str = ""
    lineno: str = ""
    name: str = ""


@dataclass
class Variable:
    name: str
    address: int
    initialized: bool = False
    isIterator: bool = False


@dataclass
class Array:
    address: int
    name: str
    start: str
    stop: str
    initialized: bool = False


@dataclass
class Identifier:
    type: ValueTypes
    name: str
    data: Any = None


@dataclass
class ForCommands:
    start: Any
    stop: Any
    iterator: Any
    tempForStop: Any
    size: int = 0
    isDownTo: bool = False
    data: List[Any] = field(default_factory=list)
    inner: List[Any] = field(default_factory=list)
    markers: List[Any] = field(default_factory=list)
    externalCommands: str = ""
    code: str = ""

    def __post_init__(self):
        self.tempForStop.loadingRegister = "f"
        self.stop.loadingRegister = "f"

        self.iterator.loadingRegister = "e"
        self.start.loadingRegister = "e"

        if self.isDownTo:
            self.manageDownTo()
        else:
            self.manageFor()
        self.addressJumps()
        self.code = self.stringCommands(13)

    def manageFor(self):
        self.addCommand(self.stop.load())
        self.addCommand(loadValueAddress(self.tempForStop))
        self.addCommand(
            storeValueFromRegisterToMemory(self.tempForStop.loadingRegister, self.tempForStop.addressRegister))

        self.addCommand(self.start.load())
        self.addCommand(loadValueAddress(self.iterator))
        self.addCommand(storeValueFromRegisterToMemory(self.start.loadingRegister, self.start.addressRegister))

        self.addMarkerCommand("#2")
        self.addCommand(self.tempForStop.load())
        self.addCommand(self.iterator.load())
        self.addCommand(resetRegister("d"))
        self.addCommand(addValuesFromRegisters("d", self.iterator.loadingRegister))
        self.addCommand(subValuesFromRegisters("d", self.tempForStop.loadingRegister))
        self.addCommand(jumpIfZero("d", "2"))
        self.addCommand(jumpLines("#1"))
        self.addInnerCommands(self.externalCommands)
        self.addCommand(self.iterator.load())
        self.addCommand(incrementValueInRegister(self.iterator.loadingRegister))
        self.addCommand(loadValueAddress(self.iterator))
        self.addCommand(storeValueFromRegisterToMemory("e", "a"))
        self.addCommand(jumpLines("#2"))
        self.addMarkerCommand("#1")

    def manageDownTo(self):
        self.addCommand(self.stop.load())
        self.addCommand(loadValueAddress(self.tempForStop))
        self.addCommand(
            storeValueFromRegisterToMemory(self.tempForStop.loadingRegister, self.tempForStop.addressRegister))

        self.addCommand(self.start.load())
        self.addCommand(loadValueAddress(self.iterator))
        self.addCommand(storeValueFromRegisterToMemory(self.start.loadingRegister, self.start.addressRegister))

        self.addMarkerCommand("#2")
        self.addCommand(self.tempForStop.load())
        self.addCommand(self.iterator.load())
        self.addCommand(resetRegister("d"))
        self.addCommand(addValuesFromRegisters("d", self.tempForStop.loadingRegister))
        self.addCommand(subValuesFromRegisters("d", self.iterator.loadingRegister))
        self.addCommand(jumpIfZero("d", "2"))
        self.addCommand(jumpLines("#1"))
        self.addInnerCommands(self.externalCommands)
        self.addCommand(self.iterator.load())
        self.addCommand(jumpIfZero("e", "#3"))
        self.addCommand(decrementValueInRegister(self.iterator.loadingRegister))
        self.addCommand(loadValueAddress(self.iterator))
        self.addCommand(storeValueFromRegisterToMemory(self.iterator.loadingRegister, "a"))
        self.addCommand(jumpLines("#2"))
        self.addMarkerCommand("#1")
        self.addMarkerCommand("#3")

    def addCommand(self, command):
        self.size += len(command.split("\n")) - 1
        self.data.append((command, self.size))

    def addInnerCommands(self, commands):
        self.size += len(commands.split("\n")) - 1
        self.inner.append((commands, self.size))

    def addMarkerCommand(self, command):
        self.markers.append((command, self.size))

    def addressJumps(self):
        list = []
        for marker in self.markers:
            for i in self.data:
                if marker[0] in i[0]:
                    item = (i[0][:-3] + str(marker[1] - i[1] + 1) + str("\n"),)
                    list.append((item, self.data.index(i)))

        for item in list:
            self.data[item[1]] = item[0]

    def stringCommands(self, innerCommandsSize):
        self.data.insert(innerCommandsSize, self.inner[0])
        finalString = ""
        for i in self.data:
            finalString += i[0]
        return finalString


@dataclass
class ConditionCommands:
    conditionCommandType: ConditionCommandTypes
    conditionCode: str = ""
    commandsCode: str = ""
    commandsCodeTwo: str = ""
    code: str = ""

    def __post_init__(self):
        if self.conditionCommandType is ConditionCommandTypes.IF:
            self.code = self.conditionCode + self.calculateFailJump() + self.commandsCode
        elif self.conditionCommandType is ConditionCommandTypes.IF_ELSE:
            self.code = self.conditionCode + self.calculateFailJump()[0] + self.commandsCode + \
                        self.calculateFailJump()[1] + self.commandsCodeTwo
        elif self.conditionCommandType is ConditionCommandTypes.WHILE:
            self.code = self.conditionCode + self.calculateFailJump()[0] + self.commandsCode + self.calculateFailJump()[
                1]
        elif self.conditionCommandType is ConditionCommandTypes.REPEAT:
            self.code = self.commandsCode + self.conditionCode + self.calculateFailJump()

    def calculateFailJump(self):
        if self.conditionCommandType is ConditionCommandTypes.IF:
            return jumpLines(len(self.commandsCode.split("\n")))
        elif self.conditionCommandType is ConditionCommandTypes.IF_ELSE:
            return jumpLines(len(self.commandsCode.split("\n")) + 1), jumpLines(len(self.commandsCodeTwo.split("\n")))
        elif self.conditionCommandType is ConditionCommandTypes.WHILE:
            return jumpLines((len(self.commandsCode.split("\n")) + 1)), jumpLines(
                -(len(self.commandsCode.split("\n")) + len(self.conditionCode.split("\n"))) + 1)
        elif self.conditionCommandType is ConditionCommandTypes.REPEAT:
            return jumpLines(-(len(self.commandsCode.split("\n")) + len(self.conditionCode.split("\n"))))


@dataclass
class Value:
    type: ValueTypes = None
    data: Any = None
    name: Any = None
    address: Any = None
    addressRegister: str = "a"
    loadingRegister: str = "b"

    @classmethod
    def fromIdentifier(cls, identifier):
        return cls(identifier.type, identifier.data, identifier.name)

    @classmethod
    def fromVariable(cls, variable):
        return cls(type=ValueTypes.ID, name=variable.name, address=variable.address)

    def load(self):
        if self.type == ValueTypes.NUMBER:
            return generateNumber(int(self.data), self.loadingRegister)
        elif self.type == ValueTypes.ID:
            ErrorsManager.verifyVariableInitialization(self.name, self.address)
            return loadValueAddress(self) + loadValueFromMemoryToRegister(self.loadingRegister, self.addressRegister)
        elif self.type == ValueTypes.ARRAY:
            return loadValueAddress(self) + loadValueFromMemoryToRegister(self.loadingRegister, self.addressRegister)


def loadValue(value, register):
    if value.type == ValueTypes.NUMBER:
        return generateNumber(int(value.data), register)
    if value.type == ValueTypes.ID:
        ErrorsManager.verifyVariableInitialization(value.name, value.address)
    return loadValueAddress(value) + loadValueFromMemoryToRegister(register, value.addressRegister)


@dataclass
class Condition:
    v1: Value
    v2: Value
    conditionType: ConditionTypes
    valuesAddresses: str
    code: str = None

    def __post_init__(self):
        self.v1.address = self.valuesAddresses
        self.v2.address = self.valuesAddresses

        self.v1.loadingRegister = "b"
        self.v2.loadingRegister = "c"

        if self.conditionType is ConditionTypes.EQ:
            self.code = self.v1.load() + self.v2.load() + equalGenerator()
        elif self.conditionType is ConditionTypes.NEQ:
            self.code = self.v1.load() + self.v2.load() + notEqualGenerator()
        elif self.conditionType is ConditionTypes.GEQ:
            self.code = self.v1.load() + self.v2.load() + greaterEqualGenerator()
        elif self.conditionType is ConditionTypes.GT:
            self.code = self.v1.load() + self.v2.load() + greaterThanGenerator()
        elif self.conditionType is ConditionTypes.LEQ:
            self.v2.loadingRegister = "b"
            self.v1.loadingRegister = "c"
            self.code = self.v2.load() + self.v1.load() + lessEqualGenerator()
        elif self.conditionType is ConditionTypes.LT:
            self.v2.loadingRegister = "b"
            self.v1.loadingRegister = "c"
            self.code = self.v2.load() + self.v1.load() + lessThanGenerator()


@dataclass
class Expression:
    v1: Value
    v2: Value
    valuesAddress: str
    expressionType: ArithmeticTypes
    code: str = ""

    def __post_init__(self):
        self.v1.address = self.valuesAddress
        self.v2.address = self.valuesAddress

        self.v2.loadingRegister = "c"

        if self.expressionType == ArithmeticTypes.PLUS:
            self.code = self.v1.load() + self.v2.load() + addValuesFromRegisters(self.v1.loadingRegister,
                                                                                 self.v2.loadingRegister)
        elif self.expressionType == ArithmeticTypes.MINUS:
            self.code = self.v1.load() + self.v2.load() + subValuesFromRegisters(self.v1.loadingRegister,
                                                                                 self.v2.loadingRegister)
        elif self.expressionType == ArithmeticTypes.MULT:
            self.code = self.v1.load() + self.v2.load() + optimizeMultiplying() + multiplyGenerator()
        elif self.expressionType == ArithmeticTypes.DIV:
            self.code = self.v1.load() + self.v2.load() + divideGenerator()
        elif self.expressionType == ArithmeticTypes.MOD:
            self.code = self.v1.load() + self.v2.load() + moduloGenerator()


def add(v1, v2, lineno):
    expression = Expression(v1=v1, v2=v2, valuesAddress=lineno, expressionType=ArithmeticTypes.PLUS)
    return expression.code


def sub(v1, v2, lineno):
    expression = Expression(v1=v1, v2=v2, valuesAddress=lineno, expressionType=ArithmeticTypes.MINUS)
    return expression.code


def multiply(v1, v2, lineno):
    expression = Expression(v1=v1, v2=v2, valuesAddress=lineno, expressionType=ArithmeticTypes.MULT)
    return expression.code


def divide(v1, v2, lineno):
    expression = Expression(v1=v1, v2=v2, valuesAddress=lineno, expressionType=ArithmeticTypes.DIV)
    return expression.code


def modulo(v1, v2, lineno):
    expression = Expression(v1=v1, v2=v2, valuesAddress=lineno, expressionType=ArithmeticTypes.MOD)
    return expression.code


def lessEqual(v1, v2, lineno):
    condition = Condition(v1=v1, v2=v2, valuesAddresses=lineno, conditionType=ConditionTypes.LEQ)
    return condition


def notEqual(v1, v2, lineno):
    condition = Condition(v1=v1, v2=v2, valuesAddresses=lineno, conditionType=ConditionTypes.NEQ)
    return condition


def equal(v1, v2, lineno):
    condition = Condition(v1=v1, v2=v2, valuesAddresses=lineno, conditionType=ConditionTypes.EQ)
    return condition


def greaterEqual(v1, v2, lineno):
    condition = Condition(v1=v1, v2=v2, valuesAddresses=lineno, conditionType=ConditionTypes.GEQ)
    return condition


def lessThan(v1, v2, lineno):
    condition = Condition(v1=v1, v2=v2, valuesAddresses=lineno, conditionType=ConditionTypes.LT)
    return condition


def greaterThan(v1, v2, lineno):
    condition = Condition(v1=v1, v2=v2, valuesAddresses=lineno, conditionType=ConditionTypes.GT)
    return condition


def ifCommand(condition, commands):
    outCommands = ConditionCommands(conditionCommandType=ConditionCommandTypes.IF, conditionCode=condition.code,
                                    commandsCode=commands)
    return outCommands.code


def ifElseCommand(condition, commandsIf, commandsElse):
    outCommands = ConditionCommands(conditionCommandType=ConditionCommandTypes.IF_ELSE, conditionCode=condition.code,
                                    commandsCode=commandsIf, commandsCodeTwo=commandsElse)
    return outCommands.code


def whileCommand(condition, commands):
    outCommands = ConditionCommands(conditionCommandType=ConditionCommandTypes.WHILE, conditionCode=condition.code,
                                    commandsCode=commands)
    return outCommands.code


def repeatUntilCommand(condition, commands):
    outCommands = ConditionCommands(conditionCommandType=ConditionCommandTypes.REPEAT, conditionCode=condition.code,
                                    commandsCode=commands)
    return outCommands.code


def valueNumber(data):
    return Value(type=ValueTypes.NUMBER, data=data)


def identifierID(name):
    return Identifier(type=ValueTypes.ID, name=name)


def identifierArrayId(name, id):
    return Identifier(type=ValueTypes.ARRAY, name=name, data=(ValueTypes.ID, id))


def identifierArrayNum(name, num):
    return Identifier(type=ValueTypes.ARRAY, name=name, data=(ValueTypes.NUMBER, num))


def forToCommand(iterator, start, stop, commands, lineno):
    tempForStop = addTempVariable()
    iterator = Value(type=ValueTypes.ID, name=iterator, address=lineno)
    start.address = lineno
    stop.address = lineno
    ErrorsManager.verifyLoop(iterator, start, stop, lineno)
    outputCommands = ForCommands(start=start, stop=stop, iterator=iterator, tempForStop=tempForStop,
                                 externalCommands=commands)
    deleteVariable(iterator.name)
    return outputCommands.code


def forDownToCommand(iterator, start, stop, commands, lineno):
    tempForStop = addTempVariable()
    iterator = Value(type=ValueTypes.ID, name=iterator, address=lineno)
    start.address = lineno
    stop.address = lineno
    ErrorsManager.verifyLoop(iterator, start, stop, lineno)
    outputCommands = ForCommands(start=start, stop=stop, iterator=iterator, tempForStop=tempForStop,
                                 externalCommands=commands, isDownTo=True)
    deleteVariable(iterator.name)
    return outputCommands.code


def generateNumber(num, register):
    return generateNumberInRegister(num, register)


def valueIdentifier(identifier):
    return Value.fromIdentifier(identifier)


def loadValueAndPut(value, register):
    if value.type == ValueTypes.NUMBER:
        tempValue = addTempVariable()
        return loadValueAddress(tempValue) + \
               generateNumber(int(value.data), "b") + \
               saveValueFromRegisterToMemory("b", register) + \
               putLoadedValue(register)

    if value.type == ValueTypes.ID:
        ErrorsManager.verifyVariableInitialization(value.name, value.address)
    return loadValueAddress(value) + putLoadedValue(register)


def getNextMemoryCell():
    global memoryCount
    memoryCount += 1
    return memoryCount


def addArrayToCount(stop, start):
    global memoryCount
    memoryCount += (stop - start + 1)


def addVariable(id, lineno):
    ErrorsManager.checkIfFirstDeclaration(id, lineno)
    newVariable = Variable(name=id, address=getNextMemoryCell(), initialized=False)
    programVariables[newVariable.name] = newVariable


def addArray(id, start, stop, lineno):
    ErrorsManager.checkArrayRange(start=start, stop=stop, identifier=id, lineno=lineno)
    newArray = Array(name=id, address=getNextMemoryCell(), start=start, stop=stop, initialized=False)
    addArrayToCount(stop, start)
    programVariables[newArray.name] = newArray


def iteratorId(id, lineno):
    addVariable(id, lineno)
    programVariables[id].initialized = True
    programVariables[id].isIterator = True
    return id


def outputCommand(value, lineno):
    value.address = lineno
    return loadValueAndPut(value, value.addressRegister)


def assignCommand(identifier, expression, lineno):
    ErrorsManager.verifyIdentifier(identifier, lineno)
    programVariables[identifier.name].initialized = True
    value = Value.fromIdentifier(identifier)
    value.address = lineno
    return expression + loadValueAddress(value) + saveValueFromRegisterToMemory(value.loadingRegister,
                                                                                value.addressRegister)


def readCommand(identifier, lineno):
    ErrorsManager.verifyIdentifier(identifier, lineno)
    programVariables[identifier.name].initialized = True
    value = Value.fromIdentifier(identifier)
    value.address = lineno
    return loadValueAddress(value) + saveLoadedValueToMemory(value.addressRegister)


def expressionValue(value, lineno):
    value.address = lineno
    return value.load()


def deleteVariable(id):
    programVariables.pop(id)


def createTempVar():
    global memoryCount
    return "#TEMPVAR_" + str(memoryCount)


def addTempVariable():
    tempVarName = createTempVar()
    addVariable(tempVarName, None)
    programVariables[tempVarName].initialized = True
    tempValue = Value.fromVariable(programVariables[tempVarName])
    return tempValue


def getArrayCell(value):
    if value.data[0] == ValueTypes.NUMBER:
        return Value(type=value.data[0], data=value.data[1])
    else:
        return Value(type=value.data[0], name=value.data[1])


def loadValueAddress(value):
    if value.type == ValueTypes.ID:
        ErrorsManager.verifyVariableAddress(value.name, value.address)
        return generateNumber(programVariables[value.name].address, "a")
    elif value.type == ValueTypes.ARRAY:
        ErrorsManager.verifyArrayAddress(value.name, value.address)
        array = programVariables[value.name]
        cell = getArrayCell(value)
        if cell.name is not None:
            ErrorsManager.verifyVariableInitialization(cell.name, value.address)
            ErrorsManager.verifyVariableAddress(cell.name, value.address)
        cell.loadingRegister = "a"
        return cell.load() + \
               generateNumber(array.start, "c") + \
               subValuesFromRegisters(cell.loadingRegister, "c") + \
               generateNumber(array.address, "c") + \
               addValuesFromRegisters(cell.loadingRegister, "c")


class ErrorsManager:
    @staticmethod
    def checkArrayRange(start, stop, identifier, lineno):
        if start > stop:
            ErrorsManager.throwError(
                Error(message="Błąd w linii: {} zły zakres tablicy: '{}'", lineno=lineno, name=identifier))

    @staticmethod
    def checkIfFirstDeclaration(identifier, lineno):
        if identifier in programVariables:
            ErrorsManager.throwError(
                Error(message="Błąd w linii: {} druga deklaracja: '{}'", lineno=lineno, name=identifier))

    @staticmethod
    def verifyIdentifier(identifier, lineno):
        if identifier.name not in programVariables:
            ErrorsManager.throwError(
                Error(message="Błąd w linii: {} niezadeklarowana zmienna: '{}'", lineno=lineno,
                      name=str(identifier.name)))
        if type(programVariables[identifier.name]) == Variable:
            if programVariables[identifier.name].isIterator:
                ErrorsManager.throwError(
                    Error(message="Błąd w linii: {} iterator: '{}' zmieniony w pętli", lineno=lineno,
                          name=str(identifier.name)))

    @staticmethod
    def verifyArrayAddress(identifier, lineno):
        if identifier in programVariables:
            if type(programVariables[identifier]) == Variable:
                ErrorsManager.throwError(
                    Error(message="Błąd w linii: {} niewłaściwe użycie zmiennej: '{}'", lineno=lineno, name=identifier))
        else:
            raise ErrorsManager.throwError(
                Error(message="Błąd w linii: {} niewłaściwe użycie zmiennej: '{}'", lineno=lineno, name=identifier))

    @staticmethod
    def verifyVariableAddress(identifier, lineno):
        if identifier in programVariables:
            if type(programVariables[identifier]) == Array:
                ErrorsManager.throwError(
                    Error(message="Błąd w linii: {} niewłaściwe użycie zmiennej tablicowej: '{}'", lineno=lineno,
                          name=identifier))
        else:
            ErrorsManager.throwError(Error(message="Błąd w linii: {} niewłaściwe użycie zmiennej: '{}'"))

    @staticmethod
    def verifyLoop(iterator, start, stop, lineno):
        if start.name == iterator.name or stop.name == iterator.name:
            ErrorsManager.throwError(
                Error(message="Błąd w linii: {} iterator w zakresie pętli: '{}'", lineno=lineno, name=iterator.name))

    @staticmethod
    def verifyVariableInitialization(identifier, lineno):
        if identifier not in programVariables:
            ErrorsManager.throwError(
                Error(message="Błąd w linii: {} taka zmienna nie istnieje: '{}'", lineno=lineno, name=identifier))
        if not programVariables[identifier].initialized:
            ErrorsManager.throwError(
                Error(message="Błąd w linii: {} zmienna nie była zainicjowana '{}'", lineno=lineno, name=identifier))

    @staticmethod
    def throwError(error):
        raise Exception(error.message.format(error.lineno, error.name))
