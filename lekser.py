import ply.lex as lex

program = ('DECLARE', 'BEGIN', 'END', 'SEMICOLON', 'COMMA',)
expression_operators = ('PLUS', 'MINUS', 'MULT', 'DIV', 'MOD')
number_relations = ('EQ', 'NEQ', 'LEQ', 'GEQ', 'LT', 'GT')
arrays = ('LEFT', 'RIGHT', 'COLON')
commands = ('ASSIGN', 'IF', 'THEN', 'ELSE', 'ENDIF',
            'FOR', 'FROM', 'TO', 'DOWNTO', 'ENDFOR', 'DO',
            'WHILE', 'ENDWHILE', 'REPEAT', 'UNTIL',
            'READ', 'WRITE')
values = ('NUMBER', 'ID')

tokens = program + expression_operators + number_relations + arrays + commands + values

t_ignore_COM = r'\[[^\]]*\]'
t_DECLARE = r'DECLARE'
t_COMMA = r','
t_BEGIN = r'BEGIN'
t_END = r'END'
t_SEMICOLON = r';'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_DIV = r'\/'
t_MOD = r'\%'

t_EQ = r'='
t_NEQ = r'!='
t_LEQ = r'<='
t_GEQ = r'>='
t_LT = r'<'
t_GT = r'>'

t_ASSIGN = r':='

t_LEFT = r'\('
t_RIGHT = r'\)'
t_COLON = r':'

t_IF = r'IF'
t_THEN = r'THEN'
t_ELSE = r'ELSE'
t_ENDIF = r'ENDIF'

t_DO = r'DO'
t_FOR = r'FOR'
t_FROM = r'FROM'
t_TO = r'TO'
t_DOWNTO = r'DOWNTO'
t_ENDFOR = r'ENDFOR'
t_WHILE = r'WHILE'
t_ENDWHILE = r'ENDWHILE'
t_REPEAT = r'REPEAT'
t_UNTIL = r'UNTIL'

t_READ = r'READ'
t_WRITE = r'WRITE'

t_ID = r'[_a-z]+'


def t_newline(t):
    r'\r?\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print("Nielegalny znak '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
