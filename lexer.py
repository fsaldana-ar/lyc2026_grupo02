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
    'NOT': 'NOT',
    'AND': 'AND',
    'OR': 'OR',
    'init': 'INIT', 
    'read': 'READ',
    'write': 'WRITE',
    'String': 'STRING',
    'Int': 'INT',
    'Float': 'FLOAT',
    'in': 'IN',
    'do': 'DO',
    'endwhile': 'ENDWHILE',
    'print': 'PRINT'
}

tokens = [
    'COMA',
    'DOSPUNTOS',
    'ASIGNACION',
    'DOSPUNTOS',
    'COMA',
    'CTE_STRING',
    
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
    'CORCHETE_ABIERTO',
    'CORCHETE_CERRADO',

    'A_LLAVE',
    'C_LLAVE',
    'A_CORCHETE',
    'C_CORCHETE',
    'A_PARENTESIS',
    'C_PARENTESIS',
] + list(reserved.values())

states = (('COMMENT', 'exclusive'),)


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
t_CORCHETE_ABIERTO = r'\['
t_CORCHETE_CERRADO = r'\]'
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
    simbolo.valor = t.value
    
    tabla_simbolos[simbolo.nombre] = simbolo
    t.value = valor
    return t


def t_VARIABLE(t):
    r'[a-zA-Z](\w|_)*'
    if len(t.value) > 25:
        raise Exception(f"ERROR LÉXICO: Identificador '{t.value}' de {len(t.value)} caracteres supera el máximo de 25. Línea {t.lexer.lineno}")
    t.type = reserved.get(t.value, 'VARIABLE')

    # verifico que es una variable
    if t.type == "VARIABLE":
        # verifico la longitud
        if len(t.value) > 20:
            raise Exception(f"ERROR: La variable \"{t.value}\" esta fuera de rango para nombres de variables. Línea {t.lexer.lineno}")

        # creo el simbolo
        simbolo = Simbolo()
        simbolo.nombre = t.value
        tabla_simbolos[simbolo.nombre] = simbolo
    
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
    path_lexter = Path('./resources/test.txt')
    data = path_lexter.read_text()
    lexer.input(data)
    while True:
        token = lexer.token()
        if not token:
            break
        print(f'TOKEN: {token.type} LEXEMA: {token.value}')
    
    # guardamos la tabla de simbolos
    with open('tabla_simbolos.txt', 'wt') as f:
        # info de la cabecera
        nombre = "Nombre"
        tipo = "TipoDato"
        valor = "Valor"
        longitud = "Longitud"
        max_len_nombre = 51
        max_len_tipo = 10
        max_len_valor = max_len_nombre
        
        # escribimos la cabecera
        f.write(f'{nombre: <{max_len_nombre}}{tipo: <{max_len_tipo}}{valor: <{max_len_valor}}{longitud}\n')

        # escribimos el resto de los datos
        for (k,v) in tabla_simbolos.items():
            f.write(f'{k: <{max_len_nombre}}{v.tipo: <{max_len_tipo}}{v.valor: <{max_len_valor}}{v.longitud}\n')