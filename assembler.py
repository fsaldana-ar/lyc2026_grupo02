from i_token import Itoken

class Assembler:
    itoken = Itoken()

    def _escribir_cabecera(self,f):
        data = ['.MODEL  LARGE','.386','.STACK 200h']
        
        for i in data:
            f.write(i + '\n')
        
        f.write('\n\n')
    
    def _escribir_data(self,f):
        f.write('.DATA\n\n')
    
    def _escribir_code(self,f):
        data = ['.CODE','main:','mov ax,@DATA','mov ds,ax','mov es,ax']

        for i in data:
            f.write(i + '\n')
        
        f.write('\n\n')
    
    def _escribir_end(self,f):
        data = ['mov ax,4C00h','int 21h','END main']

        for i in data:
            f.write(i + '\n')

    def _escribir_tabla_de_simbolos(self,f):
        self.itoken.cargar_tokens()

        for t in self.itoken.tokens:
            token = self.itoken.get_token(t)
            
            if token['tipo'] == 'String':
                linea = f'{t} db '
            else:
                linea = f'{t} dd '
            
            if t.startswith('_'):
                if token['tipo'] == 'cte_int':
                    linea += f'{token['valor']}.0'
                elif token['tipo'] == 'cte_float':
                    linea += f'{token['valor']}'
                elif token['tipo'] == 'cte_str':
                    linea += f'"{token['valor']}",$'
            else:
                linea += '?'
            
            f.write(linea + '\n')
        
        f.write('\n\n')
    
    def generar_assembler(self):
        with open('assembler_final/final.asm', 'w') as f:
            self._escribir_cabecera(f)
            self._escribir_data(f)
            self._escribir_tabla_de_simbolos(f)
            self._escribir_code(f)
            self._escribir_end(f)