import ply.lex as lex
from pathlib import Path
import re

class Simbolo:
    def __init__(self, nombre = "", tipo = "-", valor = "-", longitud = "-"):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor
        self.longitud = longitud

tabla_simbolos = {}

reserved = {
    'init': 'INIT',
    
    'read': 'READ',
    'write': 'WRITE',
    
    'if': 'IF',
    'else': 'ELSE',
    'or': 'OR',
    'not': 'NOT',
    'and': 'AND',

    'mod': 'MOD',
    'div': 'DIV',

    'while': 'WHILE',
    'in': 'IN',
    'do': 'DO',
    'endwhile': 'ENDWHILE',
    
    'Int': 'INT',
    'Float': 'FLOAT',
    'String': 'STRING',
}

tokens = [
    'COMA',
    'DOSPUNTOS',
    'ASIGNACION',
    
    'VARIABLE',
    'N_ENTERO',
    'N_FLOTANTE',
    'CTE_STRING',
    
    'MAS',
    'MENOS',
    'DIVISION',
    'MULTIPLICACION',

    'COMP_IGUAL',
    'COMP_MAYOR',
    'COMP_MENOR',
    'COMP_DISTINTO',
    'COMP_MAYOR_IGUAL',
    'COMP_MENOR_IGUAL',

    'A_LLAVE',
    'C_LLAVE',
    'A_CORCHETE',
    'C_CORCHETE',
    'A_PARENTESIS',
    'C_PARENTESIS',
] + list(reserved.values())


# Expresiones regulares para TOKENS simples
t_COMA = r','
t_DOSPUNTOS = r':'
t_ASIGNACION = r':='

t_MAS = r'\+'
t_MENOS = r'-'
t_DIVISION = r'/'
t_MULTIPLICACION = r'\*'

t_COMP_IGUAL = r'=='
t_COMP_MAYOR = r'>'
t_COMP_MENOR = r'<'
t_COMP_DISTINTO = r'<>'
t_COMP_MAYOR_IGUAL = r'>='
t_COMP_MENOR_IGUAL = r'<='

t_A_LLAVE = r'{'
t_C_LLAVE = r'}'
t_A_CORCHETE = r'\['
t_C_CORCHETE = r'\]'
t_A_PARENTESIS = r'\('
t_C_PARENTESIS = r'\)'


def t_CTE_STRING(t):
    r'\"[^"]*\"' # Captura desde la primera " hasta la segunda " y permite cualquier caracter ej: "hol@"
    
    # Extraemos el contenido sin las comillas
    contenido = t.value[1:-1]

    # Validamos el largo hasta 50 caracteres(Cota de 50)
    if len(contenido) > 50:
        raise Exception(f"ERROR LÉXICO: String de {len(contenido)} caracteres supera el máximo de 50. Línea {t.lexer.lineno}")

    # Si llega acá, está todo bien. Guardamos el valor limpio.
    t.value = contenido

    # creo el simbolo
    simbolo = Simbolo()
    simbolo.nombre = "_" + t.value
    simbolo.tipo = 'String'
    simbolo.valor = t.value
    simbolo.longitud = len(t.value)

    tabla_simbolos[simbolo.nombre] = simbolo
    return t


def t_N_FLOTANTE(t):
    r'-?[.]\d+|-?[1-9]+\d*[.]\d*'
    
    valor = float(t.value)
    
    # Validamos la cota de flotantes 32 bits
    if valor < -3.4e38 or valor > 3.4e38:
        raise Exception(f"ERROR: El número {valor} esta fuera de rango para un Float de 32 bits")
    
    # creo el simbolo
    simbolo = Simbolo()
    simbolo.nombre = "_" + t.value
    simbolo.tipo = 'Float'
    simbolo.valor = t.value

    tabla_simbolos[simbolo.nombre] = simbolo
    t.value = valor
    return t


def t_N_ENTERO(t):
    r'0|-?[1-9]\d*'

    valor = int(t.value)

    # Validamos la cota de enteros 16 bits
    if valor < -32768 or valor > 32767:
        raise Exception(f"ERROR: El número {valor} esta fuera de rango para un Int de 16 bits")

    # creo el simbolo
    simbolo = Simbolo()
    simbolo.nombre = "_" + t.value
    simbolo.tipo = 'Int'
    simbolo.valor = t.value
    
    tabla_simbolos[simbolo.nombre] = simbolo
    t.value = valor
    return t


def t_VARIABLE(t):
    r'[a-zA-Z](\w|_)*'
    
    t.type = reserved.get(t.value, 'VARIABLE')

    # verifico que es una variable
    if t.type == "VARIABLE":
        # verifico la longitud
        if len(t.value) > 20:
            raise Exception(f"ERROR: La variable \"{t.value}\" esta fuera de rango para nombres de variables. Línea {t.lexer.lineno}")

        # sólo creo el símbolo si no existe aún
        if t.value not in tabla_simbolos:
            simbolo = Simbolo()
            simbolo.nombre = t.value
            simbolo.tipo = '-'
            simbolo.valor = '-'
            simbolo.longitud = len(t.value)
            tabla_simbolos[simbolo.nombre] = simbolo
    
    return t


# Regla que cuenta la cantidad de lineas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Ignorar tabulaciones y espacios
t_ignore = ' \t'


# Ignorar comentarios
t_ignore_comentario = r'\#\+(?:(?!\#\+).)*?\+\#'


# Manejo de errores
def t_error(t):
    raise Exception(f"Caracter invalido '{t.value[0]}' en la linea: {t.lexer.lineno}")


# Build the lexer
lexer = lex.lex(reflags=re.DOTALL)


def ejecutar_lexer():
    path_lexter = Path('./resources/test.txt')
    data = path_lexter.read_text()
    lexer.input(data)
    while True:
        token = lexer.token()
        if not token:
            break
        print(f'TOKEN: {token.type} LEXEMA: {token.value}')
