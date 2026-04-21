from parser import ejecutar_parser
from lexer import ejecutar_lexer

try:
    # ejecutar_lexer()
    ejecutar_parser()
    print("Compilación exitosa. Tabla de símbolos generada en symbol-table.txt")
except Exception as e:
    print(f"Error durante la compilación: {e}")
