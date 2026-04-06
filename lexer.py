import ply.lex as lex
from pathlib import Path
import re

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'NOT': 'NOT',
    'AND': 'AND',
    'OR': 'OR',
    'init': 'INIT', #---> Para indicar el inicio del programa
    'read': 'READ',#---> Para indicar que se va a leer una variable
    'write': 'WRITE',#---> Para indicar que se va a escribir una variable
    'String': 'STRING',#---> una variable de tipo string en la Declaracion de variables
    'Int': 'INT',#---> una variable de tipo entero en la Declaracion de variables
    'Float': 'FLOAT',#---> una variable de tipo flotante en la Declar
}

tokens = [
    'A_PARENTESIS',
    'C_PARENTESIS',
    'ASIGNACION',
    'DOSPUNTOS',  #DOS PUNTOS PARA LA LISTA DE VARIABLES
    'COMA',         # COMA PARA SEPARAR VARIABLES EN LA LISTA DE VARIABLES
    'CTE_STRING',
    'N_ENTERO',
    'N_FLOTANTE',
    'VARIABLE',
    'MAS',
    'MENOS',
    'DIVISION',
    'MULTIPLICACION',
    'A_LLAVE',
    'C_LLAVE',
    'COMP_IGUAL',
    'COMP_MAYOR',
    'COMP_MENOR',
    'COMP_DISTINTO',
    'COMP_MAYOR_IGUAL',
    'COMP_MENOR_IGUAL'
] + list(reserved.values())

states = (('COMMENT', 'exclusive'),)


# Expresiones regulares para TOKENS simples
t_MAS = r'\+'
t_MENOS = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_A_PARENTESIS = r'\('
t_C_PARENTESIS = r'\)'
t_ASIGNACION = r':='
t_DOSPUNTOS = r':'
t_COMA = r','
t_COMP_IGUAL = r'=='
t_COMP_MAYOR = r'>'
t_COMP_MENOR = r'<'
t_COMP_DISTINTO = r'<>'
t_COMP_MAYOR_IGUAL = r'>='
t_COMP_MENOR_IGUAL = r'<='
t_A_LLAVE = r'{'
t_C_LLAVE = r'}'


# TODO: En estas funciones hay que verificar las cotas
def t_CTE_STRING(t):
    r'\"[^"]*\"' # Captura desde la primera " hasta la segunda " y permite cualquier caracter ej: "hol@"
    # Extraemos el contenido sin las comillas
    contenido = t.value[1:-1]

    # Validamos el largo hasta 50 caracteres(Cota de 50)
    if len(contenido) > 50:
        raise Exception(f"ERROR LÉXICO: String de {len(contenido)} caracteres supera el máximo de 50. Línea {t.lexer.lineno}")

    # Si llega acá, está todo bien. Guardamos el valor limpio.
    t.value = contenido
    return t


def t_N_FLOTANTE(t):
    r'\d+[.]\d*|[.]\d+'
    valor = float(t.value)
    # Validamos la cota de flotantes 32 bits
    if valor < -3.4e38 or valor > 3.4e38:
        raise Exception(f"ERROR El número {valor} fuera de rango para un Float de 32 bits") 
    t.value=valor
    return t


def t_N_ENTERO(t):
    r'\d+'
    valor = int(t.value)
    # Validamos la cota de enteros 16 bits    
    if valor < -32768 or valor > 32767:
        raise Exception(f"ERROR El número {valor} fuera de rango para un Int de 16 bits")
    t.value = valor
    return t


def t_VARIABLE(t):
    r'[a-zA-Z](\w|_)*'
    if len(t.value) > 25:
        raise Exception(f"ERROR LÉXICO: Identificador '{t.value}' de {len(t.value)} caracteres supera el máximo de 25. Línea {t.lexer.lineno}")
    t.type = reserved.get(t.value, 'VARIABLE')
    return t


# Regla que cuenta la cantidad de lineas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Ignorar tabulaciones y espacios
t_ignore = ' \t'

# Comentarios con estados para permitir anidamiento de un nivel
def t_COMMENT(t):
    r'\#\+'
    t.lexer.comment_level = 1
    t.lexer.begin('COMMENT')

def t_COMMENT_content(t):
    r'[^\+\#]+'

def t_COMMENT_nested(t):
    r'\#\+'
    t.lexer.comment_level += 1

def t_COMMENT_end(t):
    r'\+\#'
    t.lexer.comment_level -= 1
    if t.lexer.comment_level == 0:
        t.lexer.begin('INITIAL')

t_COMMENT_ignore = ' \t\n'

def t_COMMENT_error(t):
    pass


# Manejo de errores
def t_error(t):
    raise Exception(f"Caracter invalido '{t.value[0]}' en la linea: {t.lexer.lineno}")


# Build the lexer
lexer = lex.lex(reflags=re.DOTALL)


def ejecutar_lexer():
    path_lexter = Path('./resources/lexer_test.txt')
    data = path_lexter.read_text()
    lexer.input(data)
    while True:
        token = lexer.token()
        if not token:
            break
        print(f'TOKEN: {token.type} LEXEMA: {token.value}')
