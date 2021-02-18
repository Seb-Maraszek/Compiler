import sys
import ply.yacc as yacc
from lekser import tokens
from helpers.program import *


def p_program(p):
    '''program : DECLARE declarations BEGIN commands END'''
    p[0] = p[4] + "HALT"


def p_program_NO_DECLARATIONS(p):
    '''program : BEGIN commands END'''
    p[0] = p[2] + "HALT"


def p_declarations_VARIABLE(p):
    '''declarations	: declarations COMMA ID'''
    addVariable(id=p[3], lineno=str(p.lineno(3)))


def p_declarations_ARRAY(p):
    '''declarations	: declarations COMMA ID LEFT NUMBER COLON NUMBER RIGHT'''
    addArray(id=p[3], start=p[5], stop=p[7], lineno=str(p.lineno(3)))


def p_declarations_SINGLE_VARIABLE(p):
    '''declarations	: ID '''
    addVariable(id=p[1], lineno=str(p.lineno(1)))


def p_declarations_SINGLE_ARRAY(p):
    '''declarations : ID LEFT NUMBER COLON NUMBER RIGHT '''
    addArray(id=p[1], start=p[3], stop=p[5], lineno=str(p.lineno(1)))


def p_commands_MANY_COMMANDS(p):
    '''commands	: commands command '''
    p[0] = p[1] + p[2]


def p_commands_ONE_COMMAND(p):
    '''commands	: command'''
    p[0] = p[1]

def p_command_ASSIGN(p):
    '''command	: identifier ASSIGN expression SEMICOLON '''
    p[0] = assignCommand(identifier=p[1], expression=p[3], lineno=(str(p.lineno(1))))


def p_command_IF(p):
    '''command	: IF condition THEN commands ENDIF'''
    p[0] = ifCommand(condition=p[2], commands=p[4])


def p_command_IF_ELSE(p):
    '''command	: IF condition THEN commands ELSE commands ENDIF'''
    p[0] = ifElseCommand(condition=p[2], commandsIf=p[4], commandsElse=p[6])


def p_command_WHILE(p):
    '''command	: WHILE condition DO commands ENDWHILE'''
    p[0] = whileCommand(condition=p[2], commands=p[4])


def p_command_REPEAT_UNTIL(p):
    '''command : REPEAT commands UNTIL condition SEMICOLON'''
    p[0] = repeatUntilCommand(commands=p[2], condition=p[4])


def p_iterator_ID(p):
    '''iterator	: ID '''
    p[0] = iteratorId(id=p[1], lineno=str(p.lineno(1)))


def p_command_FOR_TO(p):
    '''command	: FOR iterator FROM value TO value DO commands ENDFOR '''
    p[0] = forToCommand(iterator=p[2], start=p[4], stop=p[6], commands=p[8], lineno=str(p.lineno(1)))


def p_command_FOR_DOWNTO(p):
    '''command	: FOR iterator FROM value DOWNTO value DO commands ENDFOR '''
    p[0] = forDownToCommand(iterator=p[2], start=p[4], stop=p[6], commands=p[8], lineno=str(p.lineno(1)))


def p_command_READ(p):
    '''command	: READ identifier SEMICOLON '''
    p[0] = readCommand(identifier=p[2], lineno=str(p.lineno(1)))


def p_command_WRITE(p):
    '''command	: WRITE value SEMICOLON '''
    p[0] = outputCommand(value=p[2], lineno=str(p.lineno(1)))


def p_expression_VALUE(p):
    '''expression : value'''
    p[0] = expressionValue(value=p[1], lineno=str(p.lineno(1)))


def p_expression_PLUS(p):
    '''expression : value PLUS value'''
    p[0] = add(v1=p[1], v2=p[3], lineno=str(p.lineno(1)))


def p_expression_MINUS(p):
    '''expression : value MINUS value'''
    p[0] = sub(v1=p[1], v2=p[3], lineno=str(p.lineno(1)))


def p_expression_MULT(p):
    '''expression : value MULT value'''
    p[0] = multiply(v1=p[1], v2=p[3], lineno=str(p.lineno(1)))


def p_expression_DIV(p):
    '''expression : value DIV value'''
    p[0] = divide(v1=p[1], v2=p[3], lineno=str(p.lineno(1)))


def p_expression_MOD(p):
    '''expression : value MOD value'''
    p[0] = modulo(v1=p[1], v2=p[3], lineno=str(p.lineno(1)))


def p_condition_EQ(p):
    '''condition : value EQ value'''
    p[0] = equal(v1=p[1], v2=p[3], lineno=str(p.lineno(1)))


def p_condition_NEQ(p):
    '''condition	: value NEQ value'''
    p[0] = notEqual(v1=p[1], v2=p[3], lineno=str(p.lineno(1)))


def p_condition_LT(p):
    '''condition	: value LT value'''
    p[0] = lessThan(v1=p[1], v2=p[3], lineno=str(p.lineno(1)))


def p_condition_GT(p):
    '''condition	: value GT value'''
    p[0] = greaterThan(v1=p[1], v2=p[3], lineno=str(p.lineno(1)))


def p_condition_LEQ(p):
    '''condition : value LEQ value'''
    p[0] = lessEqual(v1=p[1], v2=p[3], lineno=str(p.lineno(1)))


def p_condition_GEQ(p):
    '''condition	: value GEQ value '''
    p[0] = greaterEqual(v1=p[1], v2=p[3], lineno=str(p.lineno(1)))


def p_value_NUMBER(p):
    '''value : NUMBER '''
    p[0] = valueNumber(data=p[1])


def p_value_IDENTIFIER(p):
    '''value : identifier '''
    p[0] = valueIdentifier(identifier=p[1])


def p_identifier_ID(p):
    '''identifier : ID '''
    p[0] = identifierID(name=p[1])


def p_identifier_TAB_ID(p):
    '''identifier : ID LEFT ID RIGHT '''
    p[0] = identifierArrayId(name=p[1], id=p[3])


def p_identifier(p):
    '''identifier	: ID LEFT NUMBER RIGHT '''
    p[0] = identifierArrayNum(name=p[1], num=p[3])


def p_error(p):
    raise Exception("Błąd w linii " + str(p.lineno) + ': nierozpoznany napis ' + str(p.value))



parser = yacc.yacc()
f = open(sys.argv[1], "r")
try:
    parsed = parser.parse(f.read(), tracking=True)
except Exception as e:
    print(e)
    exit()

fw = open(sys.argv[2], "w")
fw.write(parsed)
