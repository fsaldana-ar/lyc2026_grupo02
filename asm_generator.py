import re
from pathlib import Path

COND_MAP = {
    'BGE': 'jge',
    'BLE': 'jle',
    'BGT': 'jg',
    'BLT': 'jl',
    'BEQ': 'je',
    'BNE': 'jne',
    'BI': 'jmp',
    'BE': 'je',
}


def read_symbol_table(path: Path):
    symbols = {}
    with path.open('rt', encoding='utf-8') as f:
        next(f)  # header
        for line in f:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 4 or not parts[0]:
                continue
            symbols[parts[0]] = {'tipo': parts[1], 'valor': parts[2], 'longitud': parts[3]}
    return symbols


def read_tercetos(path: Path):
    tercetos = []
    line_pattern = re.compile(r'^\[(\d+)\]\s*-\s*\((.*)\)$')

    def split_terceto_fields(content: str):
        fields = []
        current = ''
        in_string = False
        for ch in content:
            if ch == '"':
                in_string = not in_string
                current += ch
            elif ch == ',' and not in_string:
                fields.append(current.strip())
                current = ''
            else:
                current += ch
        fields.append(current.strip())
        return fields

    with path.open('rt', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = line_pattern.match(line)
            if not match:
                raise ValueError(f'No se pudo parsear el terceto: {line}')
            content = match.group(2).strip()
            parts = split_terceto_fields(content)
            if len(parts) != 3:
                raise ValueError(f'No se pudo parsear el terceto: {line}')
            tercetos.append((parts[0], parts[1], parts[2]))
    return tercetos


def make_label(idx: int) -> str:
    return f'L{idx}'


def is_reference(value: str) -> bool:
    return value.startswith('[') and value.endswith(']')


def ref_index(value: str) -> int:
    return int(value[1:-1])


def is_number_literal(value: str) -> bool:
    s = value.strip()
    if s.startswith('-'):
        s = s[1:]
    if s.count('.') == 1:
        left, right = s.split('.', 1)
        return (left.isdigit() or left == '') and right.isdigit()
    return s.isdigit()


def is_string_literal(value: str) -> bool:
    return value.startswith('"') and value.endswith('"')


def is_literal_or_symbol(value: str) -> bool:
    if value in ('_', ''):
        return True
    if is_string_literal(value) or is_number_literal(value):
        return True
    if value.startswith('@') and value[1:].isidentifier():
        return True
    return value.isidentifier()


def sanitize_literal_name(literal: str) -> str:
    """Convert number literal to valid TASM identifier by replacing special chars"""
    # Handle negative numbers by replacing leading minus with 'n'
    if literal.startswith('-'):
        # Replace leading minus with 'n' prefix
        sanitized = 'n' + literal[1:].replace('.', '_')
    else:
        # Replace all dots with underscores
        sanitized = literal.replace('.', '_')
    return f'_{sanitized}'

def operand_value(tercetos, operand: str, literal_labels: dict):
    if is_reference(operand):
        idx = ref_index(operand)
        arg1, arg2, arg3 = tercetos[idx]
        if arg1 in ('+', '-', '*', '/', 'DIV', 'MOD', 'CMP', 'BGE', 'BLE', 'BGT', 'BLT', 'BEQ', 'BNE', 'BI', 'WHILE'):
            return f'tmp{idx}'
        # Check if arg1 is a string literal - if so, return the STR label
        if is_string_literal(arg1):
            return literal_labels.setdefault(arg1, f'STR_{len([v for v in literal_labels.values() if v.startswith("STR_")])}')
        # Check if arg1 is a number literal - if so, return the sanitized underscore-prefixed name
        if is_number_literal(arg1):
            return literal_labels.setdefault(arg1, sanitize_literal_name(arg1))
        return arg1
    if is_string_literal(operand):
        return literal_labels.setdefault(operand, f'STR_{len([v for v in literal_labels.values() if v.startswith("STR_")])}')
    if is_number_literal(operand):
        # Store in literal_labels and return the sanitized variable name
        return literal_labels.setdefault(operand, sanitize_literal_name(operand))
    if not operand or operand == '_':
        return None
    return operand


def build_data_section(symbols, tercetos, literal_labels):
    lines = []
    lines.append('.DATA')
    declared = set()  # Track what we've already declared
    
    for name, info in symbols.items():
        tipo = info['tipo']
        # Sanitize the name - handle negative signs and dots
        if name.startswith('_-'):
            # For names like _-21, convert to _n21
            safe_name = '_n' + name[2:].replace('.', '_')
        elif name.startswith('-'):
            # For names like -21, convert to n21
            safe_name = 'n' + name[1:].replace('.', '_')
        else:
            # Replace dots with underscores
            safe_name = name.replace('.', '_')
        
        declared.add(safe_name)  # Mark as declared
        
        if tipo == 'Int':
            lines.append(f'    {safe_name} dd ?')
        elif tipo == 'Float':
            lines.append(f'    {safe_name} dd ?')
        elif tipo == 'String':
            lines.append(f'    {safe_name} db 51 dup(?), "$"')
        elif tipo == 'cte_int':
            lines.append(f'    {safe_name} dd {info["valor"]}')
        elif tipo == 'cte_float':
            lines.append(f'    {safe_name} dd {info["valor"]}')
        elif tipo == 'cte_str':
            continue
        else:
            lines.append(f'    {safe_name} dd ?')

    for literal, label in literal_labels.items():
        # Skip if already declared from symbols
        if label in declared:
            continue
        declared.add(label)
        
        if is_string_literal(literal):
            text = literal[1:-1]  # Remove quotes
            if '\\n' in text:
                parts = text.split('\\n')
                asm_segments = []
                for i, p in enumerate(parts):
                    if p:
                        asm_segments.append(f'"{p}"')
                    if i < len(parts) - 1:
                        asm_segments.append("13, 10")
                lines.append(f'    {label} db ' + ', '.join(asm_segments) + ',"$"')
            else:
                lines.append(f'    {label} db "{text}","$"')
        else:
            # It's a number literal - declare it as dd with the value
            lines.append(f'    {label} dd {literal}')
    
    # Track which symbols we've already processed
    declared_from_symbols = set(
        ('_n' + name[2:].replace('.', '_')) if name.startswith('_-') else
        ('n' + name[1:].replace('.', '_')) if name.startswith('-') else
        name.replace('.', '_') 
        for name in symbols.keys()
    )
    
    for idx, terceto in enumerate(tercetos):
        op = terceto[0]
        if op in ('+', '-', '*', '/', 'DIV', 'MOD'):
            if f'tmp{idx}' not in declared:
                lines.append(f'    tmp{idx} dd ?')
                declared.add(f'tmp{idx}')
        elif op.startswith('@') and op not in declared:
            lines.append(f'    {op} dd ?')
            declared.add(op)
    return lines


def generate_expression_code(op, left, right, dest, dest_type):
    if left is None or right is None:
        raise ValueError(f'Expresion incompleta: {op} {left} {right}')
    code = []
    if dest_type == 'Float':
        code.append(f'    fld dword ptr [{left}]')
        if op == '+':
            code.append(f'    fadd dword ptr [{right}]')
        elif op == '-':
            code.append(f'    fsub dword ptr [{right}]')
        elif op == '*':
            code.append(f'    fmul dword ptr [{right}]')
        elif op == '/':
            code.append(f'    fdiv dword ptr [{right}]')
        else:
            raise ValueError(f'Operador Float no soportado: {op}')
        code.append(f'    fstp dword ptr [{dest}]')
    else:
        code.append(f'    mov eax, {left}')
        if op == '+':
            code.append(f'    add eax, {right}')
            code.append(f'    mov {dest}, eax')
        elif op == '-':
            code.append(f'    sub eax, {right}')
            code.append(f'    mov {dest}, eax')
        elif op == '*':
            code.append(f'    imul eax, {right}')
            code.append(f'    mov {dest}, eax')
        elif op in ('/', 'DIV', 'MOD'):
            code.append('    cdq')
            code.append(f'    mov ebx, {right}')
            code.append('    idiv ebx')
            if op == 'MOD':
                code.append(f'    mov {dest}, edx')
            else:
                code.append(f'    mov {dest}, eax')
        else:
            raise ValueError(f'Operador no soportado: {op}')
    return code


def get_operand_type(operand, symbols, tmp_types, literal_labels):
    if not operand:
        return 'Int'
    if operand in tmp_types:
        return tmp_types[operand]
    # Check variables
    if operand in symbols:
        return symbols[operand]['tipo']
    # Check literals
    for lit, lbl in literal_labels.items():
        if lbl == operand:
            if '.' in lit:
                return 'Float'
            return 'Int'
    if operand.startswith('tmp'):
        return tmp_types.get(operand, 'Int')
    return 'Int'


def generate_asm(tercetos, symbols, output_path: Path):
    literal_labels = {}
    lines = []
    lines.append('include macros2.asm')
    lines.append('include number.asm')
    lines.append('')
    lines.append('.MODEL  LARGE')
    lines.append('.386')
    lines.append('.STACK 200h')
    lines.append('')
    lines.append('.CODE')
    lines.append('')
    lines.append('START:')
    lines.append('    mov ax,@DATA')
    lines.append('    mov ds,ax')
    lines.append('    mov es,ax')
    lines.append('    finit')
    lines.append('')

    literal_labels = {}
    jump_targets = set()
    tmp_types = {}
    last_cmp_was_float = False

    for idx, terceto in enumerate(tercetos):
        op, arg2, arg3 = terceto
        lines.append(f'{make_label(idx)}:')

        if op == 'WHILE':
            continue
        if op == 'CMP':
            left = operand_value(tercetos, arg2, literal_labels)
            right = operand_value(tercetos, arg3, literal_labels)
            type_left = get_operand_type(left, symbols, tmp_types, literal_labels)
            type_right = get_operand_type(right, symbols, tmp_types, literal_labels)
            
            if type_left == 'Float' or type_right == 'Float':
                last_cmp_was_float = True
                lines.append(f'    fld dword ptr [{left}]')
                lines.append(f'    fcomp dword ptr [{right}]')
                lines.append('    fstsw ax')
                lines.append('    sahf')
            else:
                last_cmp_was_float = False
                lines.append(f'    mov eax, {left}')
                lines.append(f'    cmp eax, {right}')
        elif op in COND_MAP:
            if not is_reference(arg2):
                raise ValueError(f'Destino inválido en salto condicional en terceto {idx}')
            target = ref_index(arg2)
            jump_targets.add(target)
            
            jump_instruction = COND_MAP[op]
            if last_cmp_was_float:
                unsigned_map = {
                    'jle': 'jbe',
                    'jge': 'jae',
                    'jl': 'jb',
                    'jg': 'ja',
                    'je': 'je',
                    'jne': 'jne'
                }
                jump_instruction = unsigned_map.get(jump_instruction, jump_instruction)
            lines.append(f'    {jump_instruction} {make_label(target)}')
        elif op == 'BI':
            target = ref_index(arg2)
            jump_targets.add(target)
            lines.append(f'    jmp {make_label(target)}')
        elif op == ':=':
            destino = operand_value(tercetos, arg2, literal_labels)
            fuente = operand_value(tercetos, arg3, literal_labels)
            if fuente and (fuente.startswith('STR_') or is_string_literal(arg3)):
                lines.append(f'    mov si, OFFSET {fuente}')
                lines.append(f'    mov di, OFFSET {destino}')
                lines.append('    cld')
                lines.append(f'copy_string_{idx}:')
                lines.append('    lodsb')
                lines.append('    stosb')
                lines.append("    cmp al, '$'")
                lines.append(f'    jne copy_string_{idx}')
            else:
                lines.append(f'    mov eax, {fuente}')
                lines.append(f'    mov {destino}, eax')
        elif op in ('+', '-', '*', '/', 'DIV', 'MOD'):
            left = operand_value(tercetos, arg2, literal_labels)
            right = operand_value(tercetos, arg3, literal_labels)
            
            type_left = get_operand_type(left, symbols, tmp_types, literal_labels)
            type_right = get_operand_type(right, symbols, tmp_types, literal_labels)
            
            if op == '/':
                dest_type = 'Float'
            elif op in ('DIV', 'MOD'):
                dest_type = 'Int'
            else:
                dest_type = 'Float' if (type_left == 'Float' or type_right == 'Float') else 'Int'
                
            tmp_types[f'tmp{idx}'] = dest_type
            lines.extend(generate_expression_code(op, left, right, f'tmp{idx}', dest_type))
        elif op == 'WRITE':
            destino = operand_value(tercetos, arg2, literal_labels)
            if is_string_literal(arg2):
                lines.append(f'    mov dx, OFFSET {destino}')
                lines.append(f'    mov ah, 9')
                lines.append(f'    int 21h')
            else:
                is_float = False
                if arg2 in symbols and symbols[arg2]['tipo'] == 'Float':
                    is_float = True
                elif destino in symbols and symbols[destino]['tipo'] == 'Float':
                    is_float = True
                else:
                    for lit, lbl in literal_labels.items():
                        if lbl == destino and '.' in lit:
                            is_float = True
                            break
                
                if is_float:
                    lines.append(f'    DisplayFloat {destino}, 2')
                else:
                    lines.append(f'    DisplayInteger {destino}')
        elif op == 'READ':
            variable = arg2
            if variable in symbols and symbols[variable]['tipo'] == 'Float':
                lines.append(f'    GetFloat {variable}')
            else:
                lines.append(f'    GetInteger {variable}')
        elif is_literal_or_symbol(op):
            pass
        else:
            raise ValueError(f'Operador no soportado en terceto {idx}: {op}')
        lines.append('')

    lines = lines[:6] + build_data_section(symbols, tercetos, literal_labels) + lines[6:]

    missing_labels = sorted(jump_targets - set(range(len(tercetos))))
    for target in missing_labels:
        lines.append(f'{make_label(target)}:')
        lines.append('')

    lines.append('    mov ah, 4Ch')
    lines.append('    int 21h')
    lines.append('END START')

    output_path.write_text('\n'.join(lines), encoding='utf-8')


def main():
    root = Path(__file__).parent
    symbols = read_symbol_table(root / 'symbol-table.txt')
    tercetos = read_tercetos(root / 'intermediate-code.txt')
    generate_asm(tercetos, symbols, root / 'assembler_final' / 'final.asm')


if __name__ == '__main__':
    main()
