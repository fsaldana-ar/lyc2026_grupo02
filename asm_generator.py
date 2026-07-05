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


def operand_value(tercetos, operand: str, literal_labels: dict):
    if is_reference(operand):
        idx = ref_index(operand)
        arg1, arg2, arg3 = tercetos[idx]
        if arg1 in ('+', '-', '*', '/', 'DIV', 'MOD', 'CMP', 'BGE', 'BLE', 'BGT', 'BLT', 'BEQ', 'BNE', 'BI', 'WHILE'):
            return f'tmp{idx}'
        return arg1
    if is_string_literal(operand):
        return literal_labels.setdefault(operand, f'STR_{len(literal_labels)}')
    if is_number_literal(operand):
        return operand
    if operand == '_':
        return None
    return operand


def build_data_section(symbols, tercetos, literal_labels):
    lines = []
    lines.append('.DATA')
    for name, info in symbols.items():
        tipo = info['tipo']
        if tipo == 'Int':
            lines.append(f'    {name} dd ?')
        elif tipo == 'Float':
            lines.append(f'    {name} dd ?')
        elif tipo == 'String':
            lines.append(f'    {name} db 51 dup(?), "$"')
        elif tipo == 'cte_int':
            lines.append(f'    {name} dd {info["valor"]}')
        elif tipo == 'cte_float':
            lines.append(f'    {name} dd {info["valor"]}')
        elif tipo == 'cte_str':
            continue
        else:
            lines.append(f'    {name} dd ?')

    for label, literal in literal_labels.items():
        if is_string_literal(label):
            text = label[1:-1].replace('"', '"')
            lines.append(f'    {literal} db "{text}","$"')
        else:
            lines.append(f'    {literal} dd {label}')

    declared = set(symbols.keys())
    for idx, terceto in enumerate(tercetos):
        op = terceto[0]
        if op in ('+', '-', '*', '/', 'DIV', 'MOD'):
            lines.append(f'    tmp{idx} dd ?')
        elif op.startswith('@') and op not in declared:
            lines.append(f'    {op} dd ?')
            declared.add(op)
    return lines


def generate_expression_code(op, left, right, dest):
    if left is None or right is None:
        raise ValueError(f'Expresion incompleta: {op} {left} {right}')
    code = []
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


def generate_asm(tercetos, symbols, output_path: Path):
    literal_labels = {}
    lines = []
    lines.append('include macros2.asm')
    lines.append('include number.asm')
    lines.append('')
    lines.append('.MODEL  SMALL')
    lines.append('.386')
    lines.append('.STACK 200h')
    lines.append('')
    lines.append('.CODE')
    lines.append('')
    lines.append('START:')
    lines.append('    mov ax,@DATA')
    lines.append('    mov ds,ax')
    lines.append('    mov es,ax')
    lines.append('')

    literal_labels = {}
    jump_targets = set()
    for idx, terceto in enumerate(tercetos):
        op, arg2, arg3 = terceto
        lines.append(f'{make_label(idx)}:')

        if op == 'WHILE':
            continue
        if op == 'CMP':
            left = operand_value(tercetos, arg2, literal_labels)
            right = operand_value(tercetos, arg3, literal_labels)
            lines.append(f'    mov eax, {left}')
            lines.append(f'    cmp eax, {right}')
        elif op in COND_MAP:
            if not is_reference(arg2):
                raise ValueError(f'Destino inválido en salto condicional en terceto {idx}')
            target = ref_index(arg2)
            jump_targets.add(target)
            lines.append(f'    {COND_MAP[op]} {make_label(target)}')
        elif op == 'BI':
            target = ref_index(arg2)
            jump_targets.add(target)
            lines.append(f'    jmp {make_label(target)}')
        elif op == ':=':
            destino = operand_value(tercetos, arg2, literal_labels)
            fuente = operand_value(tercetos, arg3, literal_labels)
            if is_string_literal(arg3):
                lines.append(f'    lea esi, {fuente}')
                lines.append(f'    lea edi, {destino}')
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
            lines.extend(generate_expression_code(op, left, right, f'tmp{idx}'))
        elif op == 'WRITE':
            destino = operand_value(tercetos, arg2, literal_labels)
            if is_string_literal(arg2):
                lines.append(f'    displayString {destino}')
            else:
                lines.append(f'    DisplayInteger {destino}')
        elif op == 'READ':
            variable = arg2
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
