# parser.out -> se genera solo

from lexer import tokens, tabla_simbolos
import ply.yacc as yacc  # analizador sintactico
from pathlib import Path

tercetos = []
label_count = 0
EMPTY_OPERAND = '_'  # Constante para operandos vacíos en tercetos

precedence = (
    ('right', 'ASIGNACION'),
    ('right', 'MENOS', 'MAS'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
    ('left', 'A_PARENTESIS', 'C_PARENTESIS'),
)


def new_terceto(op, arg1, arg2):
    index = len(tercetos) + 1
    tercetos.append((op, arg1, arg2))
    return index


def new_label():
    global label_count
    label_count += 1
    return f'L{label_count}'


def format_operand(value):
    if isinstance(value, int):
        return f'[{value}]'
    if isinstance(value, list):
        return '[' + ', '.join(format_operand(v) for v in value) + ']'
    return str(value)


def emit(op, arg1, arg2):
    """Emit a terceto and return its index."""
    return new_terceto(op, arg1, arg2)


def backpatch(idx, target):
    """Backpatch the jump at terceto index `idx` to point to `target`.

    Assumes the jump instruction stores its destination in arg1.
    """
    op, a1, a2 = tercetos[idx - 1]
    tercetos[idx - 1] = (op, target, a2)


def write_intermediate_code(filename='intermediate-code.txt'):
    with open(filename, 'wt', encoding='utf-8') as f:
        for idx, terceto in enumerate(tercetos, start=1):
            op, arg1, arg2 = terceto
            f.write(f'[{idx}] ({op},{format_operand(arg1)},{format_operand(arg2)})\n')


# transform_labels_to_jumps removed: backpatch-based emission used instead


def _jump_for_op(op):
    return {'<': 'BGE', '>': 'BLE', '==': 'BNE', '<>': 'BEQ', '<=': 'BGT', '>=': 'BLT'}.get(op, 'BEQ')


def write_symbol_table(filename='symbol-table.txt'):
    with open(filename, 'wt', encoding='utf-8') as f:
        nombre = 'Nombre'
        tipo = 'TipoDato'
        valor = 'Valor'
        longitud = 'Longitud'
        max_len_nombre = 30
        max_len_tipo = 10
        max_len_valor = 30
        f.write(f'{nombre: <{max_len_nombre}}{tipo: <{max_len_tipo}}{valor: <{max_len_valor}}{longitud}\n')
        for (k, v) in sorted(tabla_simbolos.items()):
            longitud_str = v.longitud if k.startswith('_') else '-'
            f.write(f'{k: <{max_len_nombre}}{v.tipo: <{max_len_tipo}}{str(v.valor): <{max_len_valor}}{longitud_str}\n')


def check_variable_declarada(nombre, lineno=None):
    simbolo = tabla_simbolos.get(nombre)
    if not simbolo or simbolo.tipo == '-' or simbolo.tipo == '':
        linea = f' linea {lineno}' if lineno else ''
        raise Exception(f'ERROR SEMÁNTICO: variable "{nombre}" no declarada.{linea}')
    return simbolo.tipo


def is_numeric(tipo):
    return tipo in ('Int', 'Float')


def compatibilidad_numerica(tipo1, tipo2):
    if not is_numeric(tipo1) or not is_numeric(tipo2):
        return False
    return True



def obtener_tipo_aritmetico(tipo1, tipo2):
    if 'Float' in (tipo1, tipo2):
        return 'Float'
    return 'Int'


def condicion_to_ref(cond):
    """Convierte una condicion_simple (con 'op') a un índice de terceto."""
    if 'ref' in cond:
        return cond['ref']
    return new_terceto('CMP', cond['left'], cond['right'])

def p_start(p):
    '''start : bloque_init programa
             | programa
    '''
    if len(p) == 3:
        print('bloque_init programa -> start')
    else:
        print('programa -> start')


def p_bloque_init(p):
    '''bloque_init : INIT A_LLAVE lista_declaraciones C_LLAVE
                   | INIT A_LLAVE C_LLAVE
    '''
    if len(p) == 4:
        print('init { } -> init')
    else:
        print('init { lista_declaraciones } -> init')


def p_lista_declaraciones(p):
    '''lista_declaraciones : lista_declaraciones declaracion
                           | declaracion
    '''
    if len(p) == 3:
        print('lista_declaraciones declaracion -> lista_declaraciones')
    else:
        print('declaracion -> lista_declaraciones')


def p_declaracion(p):
    'declaracion : lista_variables DOSPUNTOS tipo'
    print('lista_variables DOSPUNTOS tipo -> declaracion')
    tipo = p[3]['tipo']
    for var in p[1]:
        simbolo = tabla_simbolos.get(var)
        if simbolo is None:
            raise Exception(f'ERROR SEMÁNTICO: variable "{var}" no declarada en la sección de declaración')
        if simbolo.tipo != '-':
            raise Exception(f'ERROR SEMÁNTICO: variable "{var}" ya declarada')
        simbolo.tipo = tipo


def p_lista_variables(p):
    '''lista_variables : lista_variables COMA VARIABLE
                       | VARIABLE
    '''
    if len(p) == 4:
        print('lista_variables COMA VARIABLE -> lista_variables')
        p[0] = p[1] + [p[3]]
    else:
        print('VARIABLE -> lista_variables')
        p[0] = [p[1]]


def p_programa(p):
    '''programa : programa sentencia
                | sentencia
    '''
    if len(p) == 3:
        print('programa sentencia -> programa')
        p[0] = p[1]
        if p[2] is not None:
            p[0].append(p[2])
    else:
        print('sentencia -> programa')
        p[0] = [p[1]] if p[1] is not None else []


def p_sentencia(p):
    '''sentencia : asignacion
                 | seleccion
                 | ciclo_while
                 | ciclo_especial
                 | salida
                 | entrada
    '''
    print(f'{p.slice[1].type} -> sentencia')
    p[0] = p[1]


def p_salida(p):
    '''salida : WRITE A_PARENTESIS VARIABLE C_PARENTESIS
              | WRITE A_PARENTESIS CTE_STRING C_PARENTESIS'''
    print(f'write( {p.slice[3].type} ) -> salida')
    if p.slice[3].type == 'VARIABLE':
        tipo = check_variable_declarada(p[3], p.lineno(3))
        arg = p[3]
    else:
        arg = f'"{p[3]}"'
        tipo = 'String'
    p[0] = new_terceto('WRITE', arg, EMPTY_OPERAND)


def p_entrada(p):
    'entrada : READ A_PARENTESIS VARIABLE C_PARENTESIS'
    print('read ( variable ) -> read')
    check_variable_declarada(p[3], p.lineno(3))
    p[0] = new_terceto('READ', p[3], EMPTY_OPERAND)


def p_asignacion(p):
    '''asignacion : VARIABLE ASIGNACION expresion
                  | VARIABLE ASIGNACION CTE_STRING
    '''
    print(f'VARIABLE ASIGNACION {p.slice[3].type} -> asignacion')
    left = p[1]
    left_tipo = check_variable_declarada(left, p.lineno(1))
    if p.slice[3].type == 'CTE_STRING':
        right = {'ref': f'"{p[3]}"', 'tipo': 'String'}
    else:
        right = p[3]
    if left_tipo != right['tipo']:
        raise Exception(f'ERROR SEMÁNTICO: asignación incompatible para "{left}". Esperado {left_tipo} pero se obtuvo {right["tipo"]}. Línea {p.lineno(1)}')
    p[0] = new_terceto(':=', left, right['ref'])


def p_seleccion(p):
    '''seleccion : IF A_PARENTESIS condicion_simple C_PARENTESIS A_LLAVE programa C_LLAVE
                 | IF A_PARENTESIS condicion_simple C_PARENTESIS A_LLAVE programa C_LLAVE ELSE A_LLAVE programa C_LLAVE
                 | IF A_PARENTESIS condicion_multiple C_PARENTESIS A_LLAVE programa C_LLAVE
                 | IF A_PARENTESIS condicion_multiple C_PARENTESIS A_LLAVE programa C_LLAVE ELSE A_LLAVE programa C_LLAVE
    '''
    # Generación con backpatching: emitir CMP y salto condicional que se parchea
    def _jump_for_op(op):
        return {'<': 'BGE', '>': 'BLE', '==': 'BNE', '<>': 'BEQ', '<=': 'BGT', '>=': 'BLT'}.get(op, 'BEQ')

    if len(p) == 8:
        print(f'if ( {p.slice[3].type} ) {{ {p.slice[6].type} }} -> seleccion')
        cond = p[3]
        if isinstance(cond, dict) and 'op' in cond:
            cmp_idx = emit('CMP', cond['left'], cond['right'])
            b_idx = emit(_jump_for_op(cond['op']), 0, EMPTY_OPERAND)
        else:
            cmp_idx = emit('CMP', cond['ref'], 0)
            b_idx = emit('BEQ', 0, EMPTY_OPERAND)

        # cuerpo verdadero (ya genera sus tercetos)
        if p[6] is not None:
            pass

        # parchear salto al final del if
        end_pos = len(tercetos) + 1
        backpatch(b_idx, end_pos)
    else:
        print(f'if ( {p.slice[3].type} ) {{ {p.slice[6].type} }} else {{ {p.slice[10].type} }} -> seleccion')
        cond = p[3]
        if isinstance(cond, dict) and 'op' in cond:
            cmp_idx = emit('CMP', cond['left'], cond['right'])
            b_else = emit(_jump_for_op(cond['op']), 0, EMPTY_OPERAND)
        else:
            cmp_idx = emit('CMP', cond['ref'], 0)
            b_else = emit('BEQ', 0, EMPTY_OPERAND)

        # cuerpo then
        if p[6] is not None:
            pass

        # salto incondicional al final
        bi_idx = emit('BI', 0, EMPTY_OPERAND)

        # parchear b_else al inicio del else
        else_pos = len(tercetos) + 1
        backpatch(b_else, else_pos)

        # cuerpo else
        if p[10] is not None:
            pass

        # parchear BI al final
        end_pos = len(tercetos) + 1
        backpatch(bi_idx, end_pos)
    p[0] = None


def p_ciclo_while(p):
    '''ciclo_while : WHILE A_PARENTESIS condicion_simple C_PARENTESIS A_LLAVE programa C_LLAVE
                   | WHILE A_PARENTESIS condicion_multiple C_PARENTESIS A_LLAVE programa C_LLAVE
    '''
    print(f'while ( {p.slice[3]} ) {{ {p.slice[6]} }} -> ciclo_while')
    # punto de inicio de la evaluación
    start_pos = len(tercetos) + 1
    cond = p[3]
    if isinstance(cond, dict) and 'op' in cond:
        cmp_idx = emit('CMP', cond['left'], cond['right'])
        b_idx = emit(_jump_for_op(cond['op']), 0, EMPTY_OPERAND)
    else:
        cmp_idx = emit('CMP', cond['ref'], 0)
        b_idx = emit('BEQ', 0, EMPTY_OPERAND)

    # cuerpo
    if p[6] is not None:
        pass

    # salto incondicional al inicio de la evaluación
    emit('BI', start_pos, EMPTY_OPERAND)

    # parchear salto condicional al final
    end_pos = len(tercetos) + 1
    backpatch(b_idx, end_pos)
    p[0] = None


def p_condicion_simple(p):
    'condicion_simple : expresion comparador expresion'
    print('expresion comparador expresion -> condicion_simple')
    left = p[1]
    right = p[3]
    if left['tipo'] != right['tipo'] and not (is_numeric(left['tipo']) and is_numeric(right['tipo'])):
        raise Exception(f'ERROR SEMÁNTICO: comparador incompatible entre {left["tipo"]} y {right["tipo"]}. Línea {p.lineno(2)}')
    # No emitimos aquí un terceto del comparador: devolvemos la estructura para que
    # las reglas que generan saltos (if/while) emitan un CMP y el branch correspondiente.
    p[0] = {'tipo': 'Bool', 'left': left['ref'], 'right': right['ref'], 'op': p[2]}


def p_condicion_multiple(p):
    '''condicion_multiple : NOT condicion_simple
                          | condicion_simple OR condicion_simple
                          | condicion_simple AND condicion_simple
    '''
    if len(p) == 4:
        print(f'condicion_simple {p.slice[2].type} condicion_simple -> condicion_multiple')
        left = p[1]
        right = p[3]
        op = p[2].upper()
        left_ref  = condicion_to_ref(left)
        right_ref = condicion_to_ref(right)
        p[0] = {'ref': new_terceto(op, left_ref, right_ref), 'tipo': 'Bool'}
    else:
        print('NOT condicion_simple -> condicion_multiple')
        cond_ref = condicion_to_ref(p[2])
        p[0] = {'ref': new_terceto('NOT', cond_ref, EMPTY_OPERAND), 'tipo': 'Bool'}


# Temas especiales
def p_modulo(p):
    'modulo : expresion MOD expresion'
    print('expresion MOD expresion -> modulo')
    left = p[1]
    right = p[3]
    if not compatibilidad_numerica(left['tipo'], right['tipo']):
        raise Exception(f'ERROR SEMÁNTICO: modulo incompatible entre {left["tipo"]} y {right["tipo"]}. Línea {p.lineno(2)}')
    resultado = obtener_tipo_aritmetico(left['tipo'], right['tipo'])
    p[0] = {'ref': new_terceto('MOD', left['ref'], right['ref']), 'tipo': resultado}


def p_division(p):
    'division : expresion DIV expresion'
    print('expresion DIV expresion -> division')
    left = p[1]
    right = p[3]
    if not compatibilidad_numerica(left['tipo'], right['tipo']):
        raise Exception(f'ERROR SEMÁNTICO: div incompatible entre {left["tipo"]} y {right["tipo"]}. Línea {p.lineno(2)}')
    resultado = obtener_tipo_aritmetico(left['tipo'], right['tipo'])
    p[0] = {'ref': new_terceto('DIV', left['ref'], right['ref']), 'tipo': resultado}


def p_ciclo_especial(p):
    'ciclo_especial : WHILE VARIABLE IN A_CORCHETE lista_expresiones C_CORCHETE DO programa ENDWHILE'
    print('while VARIABLE in [ lista_expresiones ] do programa endwhile -> ciclo_especial')
    check_variable_declarada(p[2], p.lineno(2))

    # Helper: normaliza cada elemento de la lista a un operando válido de terceto
    def make_operand(ref):
        # si ya es un índice de terceto entero, retornarlo
        try:
            if isinstance(ref, int):
                return ref
            s = str(ref)
            # si es un entero literal representado como string -> crear CONST
            try:
                v = int(s)
                return new_terceto('CONST', v, EMPTY_OPERAND)
            except Exception:
                pass
            # si es float literal
            try:
                v = float(s)
                return new_terceto('CONST', v, EMPTY_OPERAND)
            except Exception:
                pass
            # si es una constante string ya con comillas (p_elemento produce '"text"')
            if s.startswith('"') and s.endswith('"'):
                return new_terceto('CONST', s, EMPTY_OPERAND)
            # en cualquier otro caso (nombre de variable o referencia a terceto) devolver tal cual
            return ref
        except Exception:
            return ref

    elems = p[5]['refs']
    # construir la estructura de lista encadenando con operador '-' (formato intermedio elegido)
    if len(elems) == 0:
        list_root = EMPTY_OPERAND
    elif len(elems) == 1:
        list_root = make_operand(elems[0])
    else:
        left = make_operand(elems[0])
        right = make_operand(elems[1])
        t = new_terceto('-', left, right)
        for e in elems[2:]:
            t = new_terceto('-', t, make_operand(e))
        list_root = t

    # Asignaciones e inicializaciones temporales
    emit(':=', '@list', list_root)
    emit(':=', '@idx', 0)
    emit('LENGTH', '@len', '@list')

    # Control del bucle: CMP @idx,@len  ; BGE fin (backpatch)
    cmp_idx = emit('CMP', '@idx', '@len')
    bge_idx = emit('BGE', 0, EMPTY_OPERAND)

    # cuerpo del bucle
    if p[7] is not None:
        pass

    # incremento y salto al inicio de la comparación
    emit('INC', '@idx', 1)
    emit('BI', cmp_idx, EMPTY_OPERAND)

    # parchear BGE al final
    end_pos = len(tercetos) + 1
    backpatch(bge_idx, end_pos)
    p[0] = None


def p_lista_expresiones(p):
    '''lista_expresiones : lista_expresiones COMA expresion
                         | expresion
    '''
    if len(p) == 4:
        print('lista_expresiones COMA expresion -> lista_expresiones')
        p[0] = {'refs': p[1]['refs'] + [p[3]['ref']]}
    else:
        print('expresion -> lista_expresiones')
        p[0] = {'refs': [p[1]['ref']]}


def p_expresion_menos(p):
    'expresion : expresion MENOS termino'
    print('expresion - termino -> expresion')
    left = p[1]
    right = p[3]
    if not compatibilidad_numerica(left['tipo'], right['tipo']):
        raise Exception(f'ERROR SEMÁNTICO: operación '-' incompatible entre {left["tipo"]} y {right["tipo"]}. Línea {p.lineno(2)}')
    p[0] = {'ref': new_terceto('-', left['ref'], right['ref']), 'tipo': obtener_tipo_aritmetico(left['tipo'], right['tipo'])}


def p_expresion_mas(p):
    'expresion : expresion MAS termino'
    print('expresion + termino -> expresion')
    left = p[1]
    right = p[3]
    if not compatibilidad_numerica(left['tipo'], right['tipo']):
        raise Exception(f"ERROR SEMÁNTICO: operación '+' incompatible entre {left['tipo']} y {right['tipo']}. Línea {p.lineno(2)}")
    p[0] = {'ref': new_terceto('+', left['ref'], right['ref']), 'tipo': obtener_tipo_aritmetico(left['tipo'], right['tipo'])}


def p_expresion_termino(p):
    'expresion : termino'
    print('termino -> expresion')
    p[0] = p[1]


def p_termino_multiplicacion(p):
    'termino : termino MULTIPLICACION elemento'
    print('termino * elemento -> termino')
    left = p[1]
    right = p[3]
    if not compatibilidad_numerica(left['tipo'], right['tipo']):
        raise Exception(f'ERROR SEMÁNTICO: operación '*' incompatible entre {left["tipo"]} y {right["tipo"]}. Línea {p.lineno(2)}')
    p[0] = {'ref': new_terceto('*', left['ref'], right['ref']), 'tipo': obtener_tipo_aritmetico(left['tipo'], right['tipo'])}


def p_termino_division(p):
    'termino : termino DIVISION elemento'
    print('termino / elemento -> termino')
    left = p[1]
    right = p[3]
    if not compatibilidad_numerica(left['tipo'], right['tipo']):
        raise Exception(f"ERROR SEMÁNTICO: operación '/' incompatible entre {left['tipo']} y {right['tipo']}. Línea {p.lineno(2)}")
    p[0] = {'ref': new_terceto('/', left['ref'], right['ref']), 'tipo': obtener_tipo_aritmetico(left['tipo'], right['tipo'])}


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
                | CTE_STRING
                | VARIABLE
    '''
    print(f'{p.slice[1].type} -> elemento')
    token_type = p.slice[1].type
    if token_type == 'VARIABLE':
        tipo = check_variable_declarada(p[1], p.lineno(1))
        p[0] = {'ref': p[1], 'tipo': tipo}
    elif token_type == 'N_FLOTANTE':
        p[0] = {'ref': str(p[1]), 'tipo': 'Float'}
    elif token_type == 'N_ENTERO':
        p[0] = {'ref': str(p[1]), 'tipo': 'Int'}
    elif token_type == 'CTE_STRING':
        p[0] = {'ref': f'"{p[1]}"', 'tipo': 'String'}
    else:
        p[0] = {'ref': str(p[1]), 'tipo': '-'}


def p_tipo(p):
    '''tipo : INT
            | FLOAT
            | STRING
    '''
    print(f'{p.slice[1].type} -> tipo')
    p[0] = {'tipo': p[1]}


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


# Error rule for syntax errors
def p_error(p):
    raise Exception(f"Error en la linea {p.lineno or ''} at {p.value or ''}")


def ejecutar_parser():
    parser = yacc.yacc()
    path_parser = Path('./resources/test.txt')
    code = path_parser.read_text()
    parser.parse(code)
    # transformar labels/gotos a CMP + saltos numéricos antes de escribir
    try:
        transform_labels_to_jumps()
    except Exception:
        pass
    write_symbol_table('symbol-table.txt')
    write_intermediate_code('intermediate-code.txt')

