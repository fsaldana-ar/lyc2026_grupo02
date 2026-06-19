# parser.out -> se genera solo

# Se importan los tokens generado previamente en el lexer
from lexer import tokens
import ply.yacc as yacc  # analizador sintactico
from pathlib import Path
from i_token import Itoken
from terceto import Terceto

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

itoken = Itoken()

# Variables para la creacion de codigo intermedio
terceto = Terceto()

# para indices de tercetos con expresiones
indice_terceto_expresion = []

# para indices de selecciones if
flag_ciclo_seleccion = False
indice_comienzo_seleccion = []
indice_comienzo_seleccion_else = []
indice_expresion_izquierda_seleccion = None

# para indices de ciclo while
flag_ciclo_while = False
indice_etiqueta_ciclo_while = []
indice_comienzo_ciclo_while = []

# para indicar ultimo flag utilizado ( flag_ciclo_seleccion, flag_ciclo_while ) para condiciones multiples
ultimo_flag = None

# para generar variables auxiliares con nombres unicos
indice_variable_auxiliar = 0

# para almacenar variables auxiliares utilizadas en ciclo while especial
indice_etiqueta_ciclo_while_especial = []
indice_comienzo_ciclo_while_especial = []
variables_auxiliares_ciclo_while_especial = []

# para indices de las expresiones del ciclo while especial
indice_expresion_ciclo_while_especial = []


def crear_variable_auxiliar():
    global indice_variable_auxiliar
    indice_variable_auxiliar += 1
    variables_auxiliares_ciclo_while_especial.append('@aux' + str(indice_variable_auxiliar))
    return variables_auxiliares_ciclo_while_especial[-1]


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
    print(f'lista_variables DOSPUNTOS tipo -> declaracion')

    for v in p[1]:
        token = itoken.get_token(v)

        if token == None:
            raise Exception(f'Erro: Variable "{v}" no declarada en la sección de declaración')
        if itoken.get_tipo(v) != '-':
            raise Exception(f'Error: Variable "{v}" ya declarada')
        
        itoken.set_tipo(v,p[3])


def p_lista_variables(p):
    '''lista_variables : lista_variables COMA VARIABLE
                       | VARIABLE
    '''
    if len(p) == 4:
        print(f'lista_variables COMA VARIABLE -> lista_variables')
        p[0] = p[1] + [p[3]]
    else:
        print(f'VARIABLE -> lista_variables')
        p[0] = [p[1]]


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
                 | ciclo_especial
                 | salida
                 | entrada
    '''
    print(f'{p.slice[1].type} -> sentencia')


def p_salida(p):
    '''salida : WRITE A_PARENTESIS VARIABLE C_PARENTESIS
              | WRITE A_PARENTESIS CTE_STRING C_PARENTESIS'''
    print(f'write( {p.slice[3].type} ) -> salida')

    if p.slice[3].type == "CTE_STRING":
        terceto.crear_terceto('WRITE',f'"{p[3]}"')
    else:
        verificar_variable_declarada(p,p[3])
        terceto.crear_terceto('WRITE',p[3])


def p_entrada(p):
    'entrada : READ A_PARENTESIS VARIABLE C_PARENTESIS'
    print(f'read ( variable ) -> read')
    
    verificar_variable_declarada(p,p[3])
    terceto.crear_terceto('READ',p[3])


def p_variable_asignacion(p):
    'variable_asignacion : VARIABLE'
    terceto.crear_terceto(p[1])

    p[0] = {'variable': p[1], 'indice': terceto.get_indice() - 1}


def p_asignacion(p):
    '''asignacion : variable_asignacion ASIGNACION expresion
                  | variable_asignacion ASIGNACION CTE_STRING
    '''
    print(f'VARIABLE ASIGNACION {p.slice[3].type} -> asignacion')
    verificar_variable_declarada(p,p[1]['variable'])

    tipo_a = itoken.get_tipo(p[1]['variable'])

    if p.slice[3].type == 'CTE_STRING':
        tipo_b = 'cte_string'
    else:
        tipo_b = p[3]['tipo']

    if tipo_a != tipo_b:
        if tipo_a == 'String' and tipo_b != 'cte_string':
            raise Exception(f'Error: Asignación incompatible para "{p[1]['variable']}". Esperado {tipo_a} pero se obtuvo {tipo_b}. Línea {p.lineno(1)}')
    
    if tipo_b == 'cte_string':
        terceto.crear_terceto(f'"{p[3]}"')
    
    terceto.crear_terceto(':=',f'[{p[1]['indice']}]',f'[{terceto.get_indice() - 1}]')


def p_comienzo_seleccion_if(p):
    'comienzo_seleccion_if : IF'
    global flag_ciclo_seleccion
    flag_ciclo_seleccion = True


def p_seleccion_else(p):
    'seleccion_else : ELSE'
    indice = terceto.crear_terceto('BI')
    indice_comienzo_seleccion_else.append(indice)
    """
    print('#'*50)
    print(f'p_seleccion_else - indice_bi: {indice} - icse: {indice_comienzo_seleccion_else}')
    print('#'*50)
    """


def p_seleccion(p):
    '''seleccion : comienzo_seleccion_if A_PARENTESIS condicion_simple C_PARENTESIS A_LLAVE programa C_LLAVE
                 | comienzo_seleccion_if A_PARENTESIS condicion_simple C_PARENTESIS A_LLAVE programa C_LLAVE seleccion_else A_LLAVE programa C_LLAVE
                 | comienzo_seleccion_if A_PARENTESIS condicion_multiple C_PARENTESIS A_LLAVE programa C_LLAVE
                 | comienzo_seleccion_if A_PARENTESIS condicion_multiple C_PARENTESIS A_LLAVE programa C_LLAVE seleccion_else A_LLAVE programa C_LLAVE
    '''
    # if's sin else
    if len(p) == 8:
        print(f'if ( {p.slice[3].type} ) {{ {p.slice[6].type} }} -> seleccion')
        indice = terceto.get_indice()
        if p.slice[3].type == 'condicion_simple':
            terceto.modificar_terceto(indice_comienzo_seleccion.pop(),None,f'[{indice}]')
        elif p.slice[3].type == 'condicion_multiple':
            terceto.modificar_terceto(indice_comienzo_seleccion.pop(),None,f'[{indice}]')
            
            if p[3]['conector'] == 'or':
                terceto.modificar_terceto(indice_comienzo_seleccion.pop(),diccionarioComparadoresNot.get(p[3]['comparador']),f'[{indice - 1}]')
            elif p[3]['conector'] == 'and':
                terceto.modificar_terceto(indice_comienzo_seleccion.pop(),None,f'[{indice}]')
    else:
        print(f'if ( {p.slice[3].type} ) {{ {p.slice[6].type} }} else {{ {p.slice[10].type} }} -> seleccion')
        indice = terceto.get_indice()
        """
        print('#'*50)
        print(f'p_seleccion - indice: {indice} - icse: {indice_comienzo_seleccion_else}')
        print('#'*50)
        """
        indice_else = indice_comienzo_seleccion_else.pop()
        
        if p.slice[3].type == 'condicion_simple':
            terceto.modificar_terceto(indice_comienzo_seleccion.pop(),None,f'[{indice_else + 1}]')
            terceto.modificar_terceto(indice_else,None,f'[{indice}]')
        elif p.slice[3].type == 'condicion_multiple':
            indice_tmp = indice_comienzo_seleccion.pop()
            terceto.modificar_terceto(indice_tmp,None,f'[{indice_else + 1}]')

            if p[3]['conector'] == 'or':
                terceto.modificar_terceto(indice_comienzo_seleccion.pop(),diccionarioComparadoresNot.get(p[3]['comparador']),f'[{indice_tmp + 1}]')
                terceto.modificar_terceto(indice_else,None,f'[{indice}]')
            elif p[3]['conector'] == 'and':
                terceto.modificar_terceto(indice_comienzo_seleccion.pop(),None,f'[{indice_else + 1}]')
                terceto.modificar_terceto(indice_else,None,f'[{indice}]')
            elif p[3]['conector'] == None:
                terceto.modificar_terceto(indice_else,None,f'[{indice}]')


def p_comienzo_ciclo_while(p):
    'comienzo_ciclo_while : WHILE'
    global flag_ciclo_while
    flag_ciclo_while = True
    indice = terceto.crear_terceto('WHILE')
    indice_etiqueta_ciclo_while.append(indice)


def p_ciclo_while(p):
    '''ciclo_while : comienzo_ciclo_while A_PARENTESIS condicion_simple C_PARENTESIS A_LLAVE programa C_LLAVE
                   | comienzo_ciclo_while A_PARENTESIS condicion_multiple C_PARENTESIS A_LLAVE programa C_LLAVE
    '''
    print(f'while ( {p.slice[3]} ) {{ {p.slice[6]} }} -> ciclo_while')

    indice = terceto.crear_terceto('BI')
    """
    print('#'*50)
    print(f'p_ciclo_while - indice_bi: {indice} - iecw: {indice_etiqueta_ciclo_while}')
    print('#'*50)
    """
    terceto.modificar_terceto(indice,None,f'[{indice_etiqueta_ciclo_while.pop()}]')

    if p.slice[3].type == 'condicion_simple':
        indice = terceto.get_indice()
        terceto.modificar_terceto(indice_comienzo_ciclo_while.pop(),None,f'[{indice}]')
    elif p.slice[3].type == 'condicion_multiple':
        indice = terceto.get_indice()
        """
        print('#'*50)
        print(f'while_mult - indice: {indice} - iccw: {indice_comienzo_ciclo_while}')
        print('#'*50)
        """

        indice_tmp = indice_comienzo_ciclo_while.pop()
        terceto.modificar_terceto(indice_tmp,None,f'[{indice}]')
        
        if p[3]['conector'] == 'or':
            terceto.modificar_terceto(indice_comienzo_ciclo_while.pop(),diccionarioComparadoresNot.get(p[3]['comparador']),f'[{indice_tmp + 1}]')
        elif p[3]['conector'] == 'and':
            terceto.modificar_terceto(indice_comienzo_ciclo_while.pop(),None,f'[{indice}]')


def p_condicion_simple_expi(p):
    'condicion_simple_expi : expresion'
    # Expresion izquierda de la condicion simple
    global indice_expresion_izquierda_seleccion
    indice_expresion_izquierda_seleccion = terceto.get_indice() - 1


def p_condicion_simple(p):
    'condicion_simple : condicion_simple_expi comparador expresion'
    print(f'expresion comparador expresion -> condicion_simple')

    # Indice de la primera expresion
    global indice_expresion_izquierda_seleccion

    terceto.crear_terceto('CMP',f'[{indice_expresion_izquierda_seleccion}]',f'[{terceto.get_indice() - 1}]')
    indice = terceto.crear_terceto(diccionarioComparadores.get(p[2]))

    global flag_ciclo_seleccion
    global flag_ciclo_while
    global ultimo_flag

    ultimo_flag = None
    """
    print('#'*50)
    print(f'p_condicion_simple flag_if: {flag_ciclo_seleccion} - flag_while: {flag_ciclo_while} - ultimo: {ultimo_flag}')
    print('#'*50)
    """

    if flag_ciclo_seleccion:
        ultimo_flag = 'if'
        flag_ciclo_seleccion = False
        indice_comienzo_seleccion.append(indice)
    if flag_ciclo_while:
        ultimo_flag = 'while'
        flag_ciclo_while = False
        indice_comienzo_ciclo_while.append(indice)
    p[0] = p[2]


def p_contector_condicion_multiple(p):
    '''contector_condicion_multiple : OR
                                    | AND
    '''
    global flag_ciclo_seleccion
    global flag_ciclo_while
    """
    print('#'*50)
    print(f'p_contector_condicion_multiple flag_if: {flag_ciclo_seleccion} - flag_while: {flag_ciclo_while} - ultimo: {ultimo_flag}')
    print('#'*50)
    """
    
    if ultimo_flag == 'if':
        flag_ciclo_seleccion = True
    elif ultimo_flag == 'while':
        flag_ciclo_while = True
    
    p[0] = p[1]


def p_condicion_multiple(p):
    '''condicion_multiple : NOT condicion_simple
                          | condicion_simple contector_condicion_multiple condicion_simple
    '''
    if len(p) == 4:
        print(f'condicion_simple {p.slice[2].type} condicion_simple -> condicion_multiple')
        p[0] = {'comparador': p[1], 'conector': p[2]}
    else:
        print(f'NOT condicion_simple -> condicion_multiple')
        indice = terceto.get_indice()
        """
        print('#'*50)
        print(f'p_condicion_multiple - indice {indice}')
        print('#'*50)
        """
        terceto.modificar_terceto(indice - 1,diccionarioComparadoresNot.get(p[2]))
        p[0] = {'comparador': 'not', 'conector': None}


# Temas especiales
def p_modulo(p):
    'modulo : expresion MOD expresion'
    print(f'expresion MOD expresion -> modulo')

    if not es_tipo_numerico(p[1]) or not es_tipo_numerico(p[3]):
        raise Exception(f'Error: Operación "{p[2]}" incompatible entre {p[1]['tipo']} y {p[3]['tipo']}. Línea {p.lineno(2)}')
    
    tipo_dato = obtener_tipo_dato(p[1],p[3])
    p[0] = {'tipo': tipo_dato}

    t1 = indice_terceto_expresion.pop()
    t2 = indice_terceto_expresion.pop()
    indice_terceto_expresion.append(terceto.crear_terceto('MOD',f'[{t2}]',f'[{t1}]'))


def p_division(p):
    'division : expresion DIV expresion'
    print(f'expresion DIV expresion -> division')

    if not es_tipo_numerico(p[1]) or not es_tipo_numerico(p[3]):
        raise Exception(f'Error: Operación "{p[2]}" incompatible entre {p[1]['tipo']} y {p[3]['tipo']}. Línea {p.lineno(2)}')
    
    tipo_dato = obtener_tipo_dato(p[1],p[3])
    p[0] = {'tipo': tipo_dato}

    t1 = indice_terceto_expresion.pop()
    t2 = indice_terceto_expresion.pop()
    indice_terceto_expresion.append(terceto.crear_terceto('DIV',f'[{t2}]',f'[{t1}]'))


def p_variable_ciclo_while_especial(p):
    'variable_ciclo_while_especial : VARIABLE'
    global variable_ciclo_while_especial
    variable_ciclo_while_especial = p[1]


def p_expresiones_ciclo_while_especial(p):
    'expresiones_ciclo_while_especial : A_CORCHETE lista_expresiones C_CORCHETE'
    var_aux = crear_variable_auxiliar()
    indices_saltos_expresiones = []
    indices_saltos_incodicionales = []

    terceto.crear_terceto(var_aux)
    terceto.crear_terceto(0)
    # TODO: Mirar como hacer para usar el valor del token para la asignacion
    terceto.crear_terceto(':=',f'[{terceto.get_indice() - 2}]',f'[{terceto.get_indice() - 1}]')
    
    indice = terceto.crear_terceto('WHILE')
    indice_etiqueta_ciclo_while_especial.append(indice)
    terceto.crear_terceto(f'{var_aux}')
    terceto.crear_terceto(len(indice_expresion_ciclo_while_especial))
    terceto.crear_terceto('CMP',f'[{terceto.get_indice() - 2}]',f'[{terceto.get_indice() - 1}]')
    terceto.crear_terceto('BGE')
    indice_comienzo_ciclo_while_especial.append(terceto.get_indice() - 1)

    for (i,item) in enumerate(indice_expresion_ciclo_while_especial):
        terceto.crear_terceto(i)
        terceto.crear_terceto(var_aux)
        terceto.crear_terceto('CMP',f'[{terceto.get_indice() - 2}]',f'[{terceto.get_indice() - 1}]')
        terceto.crear_terceto('BE')
        indices_saltos_expresiones.append(terceto.get_indice() - 1)

    for item in indice_expresion_ciclo_while_especial:
        terceto.modificar_terceto(indices_saltos_expresiones.pop(0),None,f'[{terceto.get_indice()}]')
        terceto.crear_terceto(variable_ciclo_while_especial)
        terceto.crear_terceto(':=',f'[{terceto.get_indice() - 1}]',f'[{item}]')
        terceto.crear_terceto('BI')
        indices_saltos_incodicionales.append(terceto.get_indice() - 1)
    
    indice = terceto.get_indice()
    terceto.crear_terceto(var_aux)
    terceto.crear_terceto(1)
    # TODO: Mirar como hacer para usar el valor del token para la suma
    terceto.crear_terceto('+',f'[{terceto.get_indice() - 2}]',f'[{terceto.get_indice() - 1}]')
    # TODO: Mirar como hacer para usar el valor del token para la asignacion
    terceto.crear_terceto(var_aux)
    terceto.crear_terceto(':=',f'[{terceto.get_indice() - 1}]',f'[{terceto.get_indice() - 2}]')

    for item in indices_saltos_incodicionales:
        terceto.modificar_terceto(item,None,f'[{indice}]')
    
    indice_expresion_ciclo_while_especial.clear()


def p_ciclo_especial(p):
    'ciclo_especial : WHILE variable_ciclo_while_especial IN expresiones_ciclo_while_especial DO programa ENDWHILE'
    print(f'while VARIABLE in [ lista_expresiones ] do programa endwhile -> ciclo_especial')
    terceto.crear_terceto('BI',f'[{indice_etiqueta_ciclo_while_especial.pop()}]')
    terceto.modificar_terceto(indice_comienzo_ciclo_while_especial.pop(),None,f'[{terceto.get_indice()}]')


def p_segunda_expresion(p):
    'segunda_expresion : expresion'
    indice_expresion_ciclo_while_especial.append(terceto.get_indice() - 1)


def p_lista_expresiones(p):
    '''lista_expresiones : lista_expresiones COMA segunda_expresion
                         | expresion
    '''
    if len(p) == 4:
        print(f'lista_expresiones COMA expresion -> lista_expresiones')
    else:
        print(f'expresion -> lista_expresiones')
        indice_expresion_ciclo_while_especial.append(terceto.get_indice() - 1)


def p_expresion_menos(p):
    'expresion : expresion MENOS termino'
    print('expresion - termino -> expresion')

    if not es_tipo_numerico(p[1]) or not es_tipo_numerico(p[3]):
        raise Exception(f'Error: Operación "{p[2]}" incompatible entre {p[1]['tipo']} y {p[3]['tipo']}. Línea {p.lineno(2)}')
    
    tipo_dato = obtener_tipo_dato(p[1],p[3])
    p[0] = {'tipo': tipo_dato}

    t1 = indice_terceto_expresion.pop()
    t2 = indice_terceto_expresion.pop()
    indice_terceto_expresion.append(terceto.crear_terceto('-',f'[{t2}]',f'[{t1}]'))


def p_expresion_mas(p):
    'expresion : expresion MAS termino'
    print('expresion + termino -> expresion')
    
    if not es_tipo_numerico(p[1]) or not es_tipo_numerico(p[3]):
        raise Exception(f'Error: Operación "{p[2]}" incompatible entre {p[1]['tipo']} y {p[3]['tipo']}. Línea {p.lineno(2)}')
    
    tipo_dato = obtener_tipo_dato(p[1],p[3])
    p[0] = {'tipo': tipo_dato}

    t1 = indice_terceto_expresion.pop()
    t2 = indice_terceto_expresion.pop()
    indice_terceto_expresion.append(terceto.crear_terceto('+',f'[{t2}]',f'[{t1}]'))


def p_expresion_termino(p):
    'expresion : termino'
    print('termino -> expresion')
    p[0] = p[1]


def p_termino_multiplicacion(p):
    'termino : termino MULTIPLICACION elemento'
    print('termino * elemento -> termino')

    if not es_tipo_numerico(p[1]) or not es_tipo_numerico(p[3]):
        raise Exception(f'Error: Operación "{p[2]}" incompatible entre {p[1]['tipo']} y {p[3]['tipo']}. Línea {p.lineno(2)}')
    
    tipo_dato = obtener_tipo_dato(p[1],p[3])
    p[0] = {'tipo': tipo_dato}

    t1 = indice_terceto_expresion.pop()
    t2 = indice_terceto_expresion.pop()
    indice_terceto_expresion.append(terceto.crear_terceto('*',f'[{t2}]',f'[{t1}]'))


def p_termino_division(p):
    'termino : termino DIVISION elemento'
    print('termino / elemento -> termino')

    if not es_tipo_numerico(p[1]) or not es_tipo_numerico(p[3]):
        raise Exception(f'Error: Operación "{p[2]}" incompatible entre {p[1]['tipo']} y {p[3]['tipo']}. Línea {p.lineno(2)}')
    
    tipo_dato = obtener_tipo_dato(p[1],p[3])
    p[0] = {'tipo': tipo_dato}
    
    t1 = indice_terceto_expresion.pop()
    t2 = indice_terceto_expresion.pop()
    indice_terceto_expresion.append(terceto.crear_terceto('/',f'[{t2}]',f'[{t1}]'))


def p_termino_elemento(p):
    'termino : elemento'
    print('elemento -> termino')
    p[0] = p[1]


def p_elemento_expresion(p):
    'elemento : A_PARENTESIS expresion C_PARENTESIS'
    print('( expresion ) -> elemento')
    p[0] = p[2]


def p_elemento_modulo(p):
    '''elemento : modulo
                | A_PARENTESIS modulo C_PARENTESIS
    '''
    if len(p) == 2:
        print('modulo -> elemento')
        p[0] = p[1]
    else:
        print('( modulo ) -> elemento')
        p[0] = p[2]


def p_elemento_division(p):
    '''elemento : division
                | A_PARENTESIS division C_PARENTESIS
    '''
    if len(p) == 2:
        print('division -> elemento')
        p[0] = p[1]
    else:
        print('( division ) -> elemento')
        p[0] = p[2]


def p_elemento(p):
    '''elemento : N_FLOTANTE
                | N_ENTERO
                | VARIABLE
    '''
    print(f'{p.slice[1].type} -> elemento')
    
    if p.slice[1].type == 'VARIABLE':
        verificar_variable_declarada(p,p[1])
        tipo_dato = itoken.get_tipo(p[1])
    elif p.slice[1].type == 'N_FLOTANTE':
        tipo_dato = 'Float'
    elif p.slice[1].type == 'N_ENTERO':
        tipo_dato = 'Int'
    
    indice_terceto_expresion.append(terceto.crear_terceto(p[1]))
    p[0] = {'tipo': tipo_dato}


def p_tipo(p):
    '''tipo : INT
            | FLOAT
            | STRING
    '''
    print(f'{p.slice[1].type} -> tipo')
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
    p[0] = p[1]


def es_tipo_numerico(var):
    return var['tipo'] in ('Int','Float')


def obtener_tipo_dato(var1, var2):
    if 'Float' in (var1['tipo'],var2['tipo']):
        return 'Float'
    return 'Int'


def verificar_variable_declarada(p,var):
    token = itoken.get_token(var)

    if token == None or itoken.get_tipo(var) == "-":
        raise Exception(f'Error: Variable "{var}" no declarada. Linea: {p.lineno(1)}')


# Error rule for syntax errors
def p_error(p):
    raise Exception(f"Error en la linea {p.lineno or ''} at {p.value or ''}")


def ejecutar_parser():
    # Build the parser
    itoken.cargar_tokens()
    parser = yacc.yacc()
    path_parser = Path("./resources/test.txt")
    code = path_parser.read_text()
    parser.parse(code)

    # Almacenamos las variables internas en la tabla de simbolos
    for item in variables_auxiliares_ciclo_while_especial:
        itoken.crear_token(item,'-')
    
    itoken.almacenar_tokens()
    terceto.almacenar_tercetos()