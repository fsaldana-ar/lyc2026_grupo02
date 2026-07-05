import argparse
from pathlib import Path
from parser import ejecutar_parser
from lexer import ejecutar_lexer
from asm_generator import generate_asm, read_symbol_table, read_tercetos


def main():
    parser = argparse.ArgumentParser(description='Compilador LYC que genera asm desde un archivo de entrada.')
    parser.add_argument('input_file', nargs='?', default='resources/test.txt',
                        help='Archivo de entrada a compilar (por defecto resources/test.txt)')
    args = parser.parse_args()

    root = Path(__file__).parent
    input_path = Path(args.input_file)
    if not input_path.is_absolute():
        input_path = root / input_path
    if not input_path.exists():
        raise FileNotFoundError(f'No se encontró el archivo de entrada: {input_path}')

    ejecutar_lexer(input_path)
    ejecutar_parser(input_path)

    root = Path(__file__).parent
    symbols = read_symbol_table(root / 'symbol-table.txt')
    tercetos = read_tercetos(root / 'intermediate-code.txt')
    generate_asm(tercetos, symbols, root / 'assembler_final' / 'final.asm')


if __name__ == '__main__':
    main()
