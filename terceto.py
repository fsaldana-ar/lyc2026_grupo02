class Terceto:
    indice = 0
    tercetos = []

    def get_indice(self):
        return self.indice

    def crear_terceto(self, arg1, arg2 = "_", arg3 = "_"):
        self.tercetos.append((arg1,arg2,arg3))
        indice = self.indice
        self.indice += 1
        return indice
    
    def modificar_terceto(self, indice, arg1 = None, arg2 = "_", arg3 = "_"):
        terceto = self.tercetos[indice]

        if arg1 == None:
            self.tercetos[indice] = (terceto[0],arg2,arg3)
        else:
            self.tercetos[indice] = (arg1,arg2,arg3)
    
    def almacenar_tercetos(self):
        with open('intermediate-code.txt', 'wt') as f:
            indice = 0
            for item in self.tercetos:
                f.write(f'[{indice}] - ({item[0]},{item[1]},{item[2]})\n')
                indice += 1