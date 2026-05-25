class Itoken():
    dict_tokens = {}

    def __init__(self, nombre, valor, tipo = "-", longitud = 0):
        self.tipo = tipo
        self.valor = valor
        self.nombre = nombre
        self.longitud = longitud
    
    def set_token(token):        
        Itoken.dict_tokens[token.nombre] = token
    
    def get_token_dict():
        return Itoken.dict_tokens