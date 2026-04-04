# parser.out -> se genera solo

# Se importan los tokens generado previamente en el lexer
from lexer import tokens
import ply.yacc as yacc  # analizador sintactico
from pathlib import Path

diccionarioComparadores = {
    ">=":   "BLT",
    ">":   "BLE",
    "<=":   "BGT",
    "<":   "BGE",
    "<>":   "BEQ",
    "==":   "BNE"
}

diccionarioComparadoresNot = {
    ">=":   "BGE",
    ">":   "BGT",
    "<=":   "BLE",
    "<":   "BLT",
    "<>":   "BNE",
    "==":   "BEQ"
}


precedence = (
    ('right', 'ASIGNACION'),
    ('right', 'MENOS','MAS'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
    ('left', 'A_PARENTESIS', 'C_PARENTESIS'),
)


# def p_start(p):
#     '''start : programa'''
#     print('FIN')

# El bloque init es opcional, por eso se agregan dos reglas EN START: una con init y otra sin init

def p_start(p):
    '''start : bloque_init programa
             | programa'''
    print('ANÁLISIS FINALIZADO: Programa válido (con o sin INIT).')

def p_bloque_init(p):
    '''bloque_init : INIT A_LLAVE lista_declaraciones C_LLAVE
                   | INIT A_LLAVE C_LLAVE'''
    print('INFO: Bloque INIT procesado.')


def p_lista_declaraciones(p):
    '''lista_declaraciones : lista_declaraciones declaracion
                           | declaracion
    '''
    if len(p) == 3:
        print(f'lista_declaraciones declaracion -> lista_declaraciones')
    else:
        print(f'declaracion -> lista_declaraciones')


def p_declaracion(p):
    '''declaracion : lista_variables DOSPUNTOS tipo
    '''
    print(f'lista_variables DOSPUNTOS tipo -> declaracion')


def p_lista_variables(p):
    '''lista_variables : lista_variables COMA VARIABLE
                       | VARIABLE
    '''
    if len(p) == 4:
        print(f'lista_variables COMA VARIABLE -> lista_variables')
    else:
        print(f'VARIABLE -> lista_variables')


def p_tipo(p):
    '''tipo : INT
            | FLOAT
            | STRING
    '''
    print(f'{p.slice[1].type} -> tipo')


def p_programa(p):
    '''programa : programa sentencia
                | sentencia
    '''
    if len(p) == 3:
        print(f'programa sentencia -> programa')
    else:
        print(f'sentencia -> programa')


def p_sentencia(p):
    '''sentencia : asignacion
                 | seleccion
                 | ciclo_while
                 | salida
    '''# agregamos salida a sentencia para poder procesar las sentencias de escritura
    print(f'{p.slice[1].type} -> sentencia')

#REGLA DEL WRITE
def p_salida(p):
    '''salida : WRITE A_PARENTESIS contenido_write C_PARENTESIS'''
    print("REGLA: WRITE reconocido")

def p_contenido_write(p):
    '''contenido_write : CTE_STRING
                       | expresion'''
    # p[0] es el valor que sube, puede ser el texto o el resultado de una cuenta
    p[0] = p[1]

def p_asignacion(p):
    '''asignacion : VARIABLE ASIGNACION expresion
    '''
    print(f'VARIABLE ASIGNACION {p.slice[3].type} -> asignacion')


def p_seleccion(p):
    '''seleccion : IF A_PARENTESIS condicion_simple C_PARENTESIS A_LLAVE sentencia C_LLAVE
                 | IF A_PARENTESIS condicion_simple C_PARENTESIS A_LLAVE sentencia C_LLAVE ELSE A_LLAVE sentencia C_LLAVE
                 | IF A_PARENTESIS condicion_multiple C_PARENTESIS A_LLAVE sentencia C_LLAVE
                 | IF A_PARENTESIS condicion_multiple C_PARENTESIS A_LLAVE sentencia C_LLAVE ELSE A_LLAVE sentencia C_LLAVE
    '''
    if len(p) == 8:
        print(f'if ( {p.slice[3].type} ) {{ {p.slice[6].type} }} -> seleccion')
    else:
        print(f'if ( {p.slice[3].type} ) {{ {p.slice[6].type} }} else {{ {p.slice[10].type} }} -> seleccion')


def p_ciclo_while(p):
    '''ciclo_while : WHILE A_PARENTESIS condicion_simple C_PARENTESIS A_LLAVE sentencia C_LLAVE
                   | WHILE A_PARENTESIS condicion_multiple C_PARENTESIS A_LLAVE sentencia C_LLAVE
    '''
    print(f'while ( {p.slice[3]} ) {{ {p.slice[6]} }} -> ciclo_while')


def p_condicion_simple(p):
    'condicion_simple : VARIABLE comparador VARIABLE'
    print(f'VARIABLE comparador VARIABLE -> condicion_simple')


def p_condicion_multiple(p):
    '''condicion_multiple : NOT condicion_simple
                          | condicion_simple OR condicion_simple
                          | condicion_simple AND condicion_simple
    '''
    if len(p) == 4:
        print(f'condicion_simple {p.slice[2].type} condicion_simple -> condicion_multiple')
    else:
        print(f'NOT condicion_simple -> condicion_multiple')


def p_expresion_menos(p):
    'expresion : expresion MENOS termino'
    print('expresion - termino -> expresion')

def p_expresion_mas(p):
    'expresion : expresion MAS termino'
    print('expresion + termino -> expresion')


def p_expresion_termino(p):
    'expresion : termino'
    print('termino -> expresion')


def p_termino_multiplicacion(p):
    'termino : termino MULTIPLICACION elemento'
    print('termino * elemento -> termino')


def p_termino_division(p):
    'termino : termino DIVISION elemento'
    print('termino / elemento -> termino')


def p_termino_elemento(p):
    'termino : elemento'
    print('elemento -> termino')


def p_elemento_expresion(p):
    'elemento : A_PARENTESIS expresion C_PARENTESIS'
    print('( expresion ) -> elemento')


def p_elemento(p):
    '''elemento : N_ENTERO
                | VARIABLE
    '''
    print(f'{p.slice[1].type} -> elemento')
    p[0] = p[1]


def p_comparador(p):
    '''comparador : COMP_IGUAL
                  | COMP_MAYOR
                  | COMP_MENOR
                  | COMP_DISTINTO
                  | COMP_MAYOR_IGUAL
                  | COMP_MENOR_IGUAL
    '''
    print(f'{p.slice[1].type} -> comparador')
    #print(f'{p.slice[1].value} -> comparador')


# Error rule for syntax errors
def p_error(p):
    raise Exception(f"Error en la linea {p.lineno or ''} at {p.value or ''}")


def ejecutar_parser():
    # Build the parser
    parser = yacc.yacc()
    path_parser = Path("./resources/parser_test.txt")
    code = path_parser.read_text()
    parser.parse(code)

