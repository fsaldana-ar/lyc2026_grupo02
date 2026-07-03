class Itoken():
    def __init__(self):
        self.tokens = {}

    def crear_token(self, nombre, valor, tipo = '-', longitud = 0):
        self.tokens[nombre] = { 'tipo': tipo, 'valor': valor, 'longitud': longitud }
    
    def get_tipo(self, nombre):
        return self.tokens.get(nombre)['tipo']
    
    def set_tipo(self, nombre, tipo):
        self.tokens.get(nombre)['tipo'] = tipo

    def get_token(self, nombre):
        return self.tokens.get(nombre)
    
    def get_nombre(self, valor):
        nombre = '_' + str(valor)
        nombre = nombre.replace(' ','_')
        nombre = nombre.replace('.','_')
        return nombre
    
    def cargar_tokens(self):
        with open('symbol-table.txt', 'rt') as f:
            i = True
            for line in f:
                if i:
                    i = False
                    continue
                
                line = line.split('|')
                nombre = line[0].strip()
                tipo = line[1].strip()
                valor = line[2].strip()
                longitud = line[3].strip()
                self.crear_token(nombre,valor,tipo,longitud)

    def almacenar_tokens(self):
        with open('symbol-table.txt', 'wt') as f:
            # info de la cabecera
            nombre = "Nombre"
            tipo = "TipoDato"
            valor = "Valor"
            longitud = "Longitud"
            max_len_tipo = 15
            max_len_nombre = 51
            max_len_valor = max_len_nombre
            
            # escribimos la cabecera
            f.write(f'{nombre: <{max_len_nombre}}{tipo: <{max_len_tipo}}{valor: <{max_len_valor}}{longitud}\n')
            
            # escribimos el resto de los datos
            for (k,v) in self.tokens.items():
                #f.write(f'{k: <{max_len_nombre}}{v['tipo']: <{max_len_tipo}}{v['valor']: <{max_len_valor}}{v['longitud']}\n')
                f.write(f'{k: <{max_len_nombre}}|{v['tipo']: <{max_len_tipo}}|{v['valor']: <{max_len_valor}}|{v['longitud']}\n')