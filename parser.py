# parser.out -> se genera solo

# Se importan los tokens generado previamente en el lexer
from lexer import tokens
import ply.yacc as yacc  # analizador sintactico
from pathlib import Path

symbol_table = {}

numeric_types = {'int', 'float'}

def check_declared_variable(name):
    if name not in symbol_table:
        raise Exception(f"Variable '{name}' no declarada")
    return symbol_table[name]['type']


def are_comparable_types(left_type, right_type):
    return left_type == right_type or ({left_type, right_type} <= numeric_types)


def arithmetic_result_type(left_type, right_type):
    if left_type == right_type:
        return left_type
    if {left_type, right_type} <= numeric_types:
        return 'float'
    raise Exception(f"Tipos incompatibles en operación aritmética: {left_type} vs {right_type}")


def assignment_compatible(var_type, expr_type):
    return var_type == expr_type or (var_type == 'float' and expr_type == 'int')


def check_compatible_types(left_type, right_type, context):
    if not are_comparable_types(left_type, right_type):
        raise Exception(f"Tipo incompatible en {context}: {left_type} vs {right_type}")


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


def p_start(p):
    '''start : bloque_init programa
             | programa
    '''
    if len(p) == 3:
        print(f'bloque_init programa -> start')
    else:
        print('programa -> start')


def p_bloque_init(p):
    '''bloque_init : INIT A_LLAVE lista_declaraciones C_LLAVE
                   | INIT A_LLAVE C_LLAVE
    '''
    if len(p) == 4:
        print(f'init {{ }} -> init')
    else:
        print(f'init {{ lista_declaraciones }} -> init')


def p_lista_declaraciones(p):
    '''lista_declaraciones : lista_declaraciones declaracion
                           | declaracion
    '''
    if len(p) == 3:
        print(f'lista_declaraciones declaracion -> lista_declaraciones')
    else:
        print(f'declaracion -> lista_declaraciones')


def p_declaracion(p):
    'declaracion : lista_variables DOSPUNTOS tipo'
    for var in p[1]:
        if var in symbol_table and symbol_table[var]['kind'] == 'variable':
            raise Exception(f"Variable '{var}' ya declarada")
        symbol_table[var] = {'type': p[3], 'kind': 'variable'}


def p_lista_variables(p):
    '''lista_variables : lista_variables COMA VARIABLE
                       | VARIABLE
    '''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_tipo(p):
    '''tipo : INT
            | FLOAT
            | STRING
    '''
    p[0] = p.slice[1].type.lower()


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
                 | read
                 | print
    '''# agregamos salida a sentencia para poder procesar las sentencias de escritura
    print(f'{p.slice[1].type} -> sentencia')


def p_salida(p):
    'salida : WRITE A_PARENTESIS contenido_write C_PARENTESIS'
    print(f'write( contenido ) -> salida')


def p_contenido_write(p):
    '''contenido_write : CTE_STRING
                       | VARIABLE'''
    if p.slice[1].type == 'CTE_STRING':
        symbol_table[p[1]] = {'type': 'string', 'kind': 'constant', 'value': p[1]}
        p[0] = 'string'
    else:
        p[0] = check_declared_variable(p[1])
    print(f'{p.slice[1].type} -> contenido_write')
    # p[0] es el valor que sube, puede ser el texto o el resultado de una cuenta
    # p[0] = p[1]


def p_asignacion(p):
    '''asignacion : VARIABLE ASIGNACION expresion
    '''
    var_type = check_declared_variable(p[1])
    expr_type = p[3]
    if not assignment_compatible(var_type, expr_type):
        raise Exception(f"Tipo incompatible en asignación: {var_type} vs {expr_type}")
    print(f'VARIABLE ASIGNACION expresion -> asignacion')


def p_seleccion(p):
    '''seleccion : IF A_PARENTESIS condicion_simple C_PARENTESIS A_LLAVE programa C_LLAVE
                 | IF A_PARENTESIS condicion_simple C_PARENTESIS A_LLAVE programa C_LLAVE ELSE A_LLAVE programa C_LLAVE
                 | IF A_PARENTESIS condicion_multiple C_PARENTESIS A_LLAVE programa C_LLAVE
                 | IF A_PARENTESIS condicion_multiple C_PARENTESIS A_LLAVE programa C_LLAVE ELSE A_LLAVE programa C_LLAVE
    '''
    if len(p) == 8:
        print(f'if ( {p.slice[3].type} ) {{ {p.slice[6].type} }} -> seleccion')
    else:
        print(f'if ( {p.slice[3].type} ) {{ {p.slice[6].type} }} else {{ {p.slice[10].type} }} -> seleccion')


def p_ciclo_while(p):
    '''ciclo_while : WHILE A_PARENTESIS condicion_simple C_PARENTESIS A_LLAVE programa C_LLAVE
                   | WHILE A_PARENTESIS condicion_multiple C_PARENTESIS A_LLAVE programa C_LLAVE
    '''
    print(f'while ( {p.slice[3]} ) {{ {p.slice[6]} }} -> ciclo_while')


def p_condicion_simple(p):
    'condicion_simple : VARIABLE comparador VARIABLE'
    left_type = check_declared_variable(p[1])
    right_type = check_declared_variable(p[3])
    check_compatible_types(left_type, right_type, 'condición')
    p[0] = 'bool'
    print(f'VARIABLE comparador VARIABLE -> condicion_simple')


def p_condicion_multiple(p):
    '''condicion_multiple : NOT condicion_simple
                          | condicion_simple OR condicion_simple
                          | condicion_simple AND condicion_simple
    '''
    if len(p) == 4:
        p[0] = 'bool'
        print(f'condicion_simple {p.slice[2].type} condicion_simple -> condicion_multiple')
    else:
        p[0] = 'bool'
        print(f'NOT condicion_simple -> condicion_multiple')


def p_expresion_menos(p):
    'expresion : expresion MENOS termino'
    p[0] = arithmetic_result_type(p[1], p[3])
    print('expresion - termino -> expresion')


def p_expresion_mas(p):
    'expresion : expresion MAS termino'
    p[0] = arithmetic_result_type(p[1], p[3])
    print('expresion + termino -> expresion')


def p_expresion_termino(p):
    'expresion : termino'
    p[0] = p[1]
    print('termino -> expresion')


def p_termino_multiplicacion(p):
    'termino : termino MULTIPLICACION elemento'
    p[0] = arithmetic_result_type(p[1], p[3])
    print('termino * elemento -> termino')


def p_termino_division(p):
    'termino : termino DIVISION elemento'
    p[0] = arithmetic_result_type(p[1], p[3])
    print('termino / elemento -> termino')


def p_termino_elemento(p):
    'termino : elemento'
    p[0] = p[1]
    print('elemento -> termino')


def p_elemento_expresion(p):
    'elemento : A_PARENTESIS expresion C_PARENTESIS'
    p[0] = p[2]
    print('( expresion ) -> elemento')


def p_elemento(p):
    '''elemento : N_ENTERO
                | N_FLOTANTE
                | VARIABLE
    '''
    if p.slice[1].type in ['N_ENTERO', 'N_FLOTANTE']:
        tipo = 'int' if p.slice[1].type == 'N_ENTERO' else 'float'
        symbol_table[p[1]] = {'type': tipo, 'kind': 'constant', 'value': p[1]}
        p[0] = tipo
    else:  # VARIABLE
        if p[1] not in symbol_table:
            raise Exception(f"Variable '{p[1]}' no declarada")
        p[0] = symbol_table[p[1]]['type']
    print(f'{p.slice[1].type} -> elemento')
    # p[0] = p[1]


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
    path_parser = Path("./resources/test.txt")
    code = path_parser.read_text()
    parser.parse(code)
    # Write symbol table
    with open('symbol-table.txt', 'w') as f:
        for name, attrs in symbol_table.items():
            value_str = f" = {attrs['value']}" if 'value' in attrs else ""
            f.write(f"{name}: {attrs['type']} ({attrs['kind']}){value_str}\n")

def p_read(p):
    '''read : READ A_PARENTESIS VARIABLE C_PARENTESIS'''
    check_declared_variable(p[3])
    p[0] = symbol_table[p[3]]['type']
    print(f'READ ( {p[3]} ) -> read')

def p_print(p):
    '''print : PRINT A_PARENTESIS contenido_write C_PARENTESIS'''
    print(f'PRINT ( {p.slice[3].type} ) -> print')

def p_list_expressions_single(p):
    '''list_expressions : expresion'''
    p[0] = [p[1]]

def p_list_expressions_multiple(p):
    '''list_expressions : list_expressions COMA expresion'''
    p[0] = p[1] + [p[3]]

def p_ciclo_while_in(p):
    '''ciclo_while : WHILE VARIABLE IN CORCHETE_ABIERTO list_expressions CORCHETE_CERRADO DO programa ENDWHILE'''