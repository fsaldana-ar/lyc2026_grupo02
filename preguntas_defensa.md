# Cuestionario Incisivo de Defensa del Proyecto: Compilador en PLY

Este cuestionario de 30 preguntas y respuestas críticas analiza en profundidad los detalles de implementación, las vulnerabilidades latentes, las inconsistencias de diseño y las decisiones arquitectónicas tomadas en el compilador.

---

## Bloque 1: Analizador Léxico y Tabla de Símbolos (`lexer.py`, `i_token.py`)

### 1. ¿Por qué el lexer valida que los enteros estén en el rango de 16 bits con signo ($-32768$ a $32767$) si luego en el ensamblador los declaras como `dd` (32 bits)?
> **Respuesta:** Existe una discrepancia de diseño. El lexer restringe los enteros a 16 bits para cumplir con las especificaciones académicas típicas de los sistemas de modo real. Sin embargo, el generador de código ensamblador los declara como `dd` (32 bits) para homogeneizar la lógica del compilador y permitir el uso directo de registros de 32 bits (`EAX`, `EBX`, etc.) sin tener que lidiar con la complejidad de combinar registros de 16 bits (como `DX:AX`) en operaciones aritméticas avanzadas.

### 2. ¿Cómo evita el compilador una colisión en la Tabla de Símbolos si el usuario define una variable llamada `_10` y luego utiliza la constante entera `10`?
> **Respuesta:** Por definición léxica, los identificadores de las variables obligatoriamente deben comenzar con una letra (`r'[a-zA-Z](\w|_)*'`). Dado que el compilador antepone automáticamente un guion bajo únicamente a los nombres de las constantes en la tabla de símbolos (ej: la constante `10` se guarda como el token `_10`), es imposible que el usuario declare una variable con ese nombre exacto.

### 3. ¿Por qué las constantes de cadena se limitan estrictamente a 50 caracteres?
> **Respuesta:** Es una medida preventiva para evitar desbordamientos de búfer (*buffer overflow*). Al limitar la longitud léxica de las constantes string a 50 caracteres, garantizamos que el buffer estático reservado en el archivo ensamblador (`db 51 dup(?), "$"`) tenga espacio suficiente para almacenar el contenido del texto más el terminador de fin de cadena de DOS (`$`).

### 4. ¿Qué sucede si un comentario multilinea `#+ ... +#` no se cierra? ¿Cómo reacciona el lexer?
> **Respuesta:** Dado que la regla del comentario (`t_ignore_comentario`) requiere el patrón de cierre `+\#` para hacer match, si este no se encuentra, la expresión regular fallará. El lexer continuará escaneando secuencialmente y, al encontrarse con caracteres que no encajan en ningún otro token válido, lanzará una excepción genérica en `t_error` reportando un carácter inválido, en lugar de emitir un diagnóstico limpio de "Comentario sin cerrar".

### 5. ¿Cómo evita la tabla de símbolos la declaración duplicada de una misma constante que aparece múltiples veces en el código?
> **Respuesta:** La clase `Itoken` utiliza un diccionario de Python (`self.tokens`) donde la clave es el lexema sanitizado (ej: `_3_14` para la constante `3.14`). Al escanear una constante repetida, se invoca `crear_token` con la misma clave. Al ser un diccionario, la clave existente simplemente se sobrescribe en memoria en lugar de crear una nueva entrada, resultando en una única declaración en la sección `.DATA`.

### 6. ¿Por qué los operadores como `div` o `mod` se buscan en minúsculas en la regla `t_VARIABLE`?
> **Respuesta:** En la regla `t_VARIABLE`, si un lexema no coincide exactamente con una palabra reservada sensible a mayúsculas/minúsculas (como `if` o `while`), se ejecuta `reserved.get(t.value.lower(), 'VARIABLE')` específicamente para evaluar `div` y `mod`. Esto flexibiliza el uso de estos operadores matemáticos permitiendo escribirlos indistintamente en mayúsculas o minúsculas, mientras que las estructuras de control permanecen estrictamente en minúsculas.

---

## Bloque 2: Analizador Sintáctico y Semántico (`parser.py`)

### 7. Usas variables globales en `parser.py` para arrastrar estados de saltos y banderas (ej: `flag_ciclo_seleccion`). ¿Qué pasa si el parser encuentra un error de sintaxis y aborta?
> **Respuesta:** El compilador no limpia estas variables si se interrumpe la ejecución por una excepción. Dado que el compilador está diseñado para ejecutarse como un proceso único por archivo de entrada (se levanta, compila o falla, y finaliza), no es un problema inmediato. No obstante, si se usara el compilador dentro de un servidor persistente o un entorno interactivo de compilación continua, provocaría fugas de estado y fallos catastróficos.

### 8. ¿Por qué el compilador prohíbe explícitamente comparar un `Int` con un `Float` en las expresiones condicionales?
> **Respuesta:** Para simplificar la generación de código. Realizar comparaciones mixtas requeriría que el compilador detecte el operando de tipo entero, genere código ensamblador para cargarlo en el coprocesador con `fild` para promoverlo a flotante, y luego ejecute la comparación. Prohibirlo en la etapa semántica traslada la responsabilidad de la conversión explícita al programador y evita imprecisiones accidentales.

### 9. ¿Es posible asignar una constante entera `5` a una variable declarada como `Float`?
> **Respuesta:** No. El análisis semántico en `p_asignacion` realiza una comprobación estricta de tipos. La constante `5` se parsea como `cte_int` (normalizado a `Int`). Si la variable destino es `Float`, el compilador lanza un error semántico de tipos incompatibles. Para lograrlo, el usuario debe escribir explícitamente `5.0`.

### 10. ¿Por qué la división real `/` siempre produce un `Float`, incluso si ambos operandos son variables enteras?
> **Respuesta:** Porque en la semántica del lenguaje, `/` representa la división matemática real. Para obtener división entera (con truncamiento y retorno entero), se provee explícitamente el operador `DIV`. Así se separa claramente el tipo de cómputo aritmético deseado desde la sintaxis.

### 11. ¿Cómo se evita que una variable sea declarada dos veces en el bloque `init`?
> **Respuesta:** En la regla `p_declaracion`, al iterar las variables declaradas, se consulta la tabla de símbolos. Si el tipo de datos asignado previamente a la variable es diferente al valor inicial `'-'`, el compilador detecta que ya pasó por una regla de declaración previa y lanza una excepción indicando que la variable ya está declarada.

### 12. ¿Qué sucede si se usa una variable en el cuerpo del programa que no fue declarada en el bloque `init`?
> **Respuesta:** Durante el análisis sintáctico, todas las operaciones que involucran variables invocan a `verificar_variable_declarada`. Esta función consulta la tabla de símbolos y, si encuentra que el tipo es `'-'` (valor por defecto creado durante la fase de análisis léxico), significa que nunca fue procesada por la regla del bloque `init` y se arroja un error semántico de "Variable no declarada".

### 13. ¿Por qué los operadores `DIV` y `MOD` exigen operandos de tipo entero?
> **Respuesta:** Por definición matemática, la división entera y el residuo solo aplican sobre números enteros. Permitir operandos de tipo real (`Float`) generaría incoherencias lógicas o requeriría un procesamiento de truncamiento complejo en ensamblador. El compilador lo previene mediante chequeo semántico usando la función helper `es_tipo_numerico` y verificando que el tipo no sea `Float`.

### 14. ¿Sostiene el parser la asignación encadenada del tipo `a := b := 5`?
> **Respuesta:** No. La regla `p_asignacion` define que el lado izquierdo debe ser una variable de asignación y el lado derecho una `expresion` o `CTE_STRING`. Dado que la regla `p_asignacion` en sí no devuelve un valor (no asigna nada a `p[0]` para ser consumido en una expresión), una asignación no puede formar parte de otra asignación.

---

## Bloque 3: Representación Intermedia y Control de Flujo (`parser.py`, `terceto.py`)

### 15. ¿Cómo se manejan los bloques `if` anidados sin que se mezclen sus índices de salto en los tercetos?
> **Respuesta:** Se manejan mediante una pila (estructura LIFO) implementada en listas globales (ej. `indice_comienzo_seleccion`). Al abrir un `if`, se apila el índice del salto incompleto. Si hay un `if` anidado, su índice de salto se apila encima del anterior. Al encontrarse con los cierres de bloque (`C_LLAVE`), se desapila el último índice (el del `if` más interno) garantizando que los saltos se resuelvan en el orden inverso al que se abrieron.

### 16. En condiciones múltiples con `OR` (ej: `cond1 OR cond2`), ¿por qué modificas el salto de la primera condición utilizando el comparador negado (`diccionarioComparadoresNot`)?
> **Respuesta:** Para implementar cortocircuito. Si la primera condición (`cond1`) es verdadera, no se debe evaluar la segunda y se debe saltar directo al cuerpo del `if`. Normalmente, `cond1` genera un salto condicional que se activa si es falsa para ir al final. Al modificar ese salto con el comparador invertido (`Not`), logramos que el salto ocurra si la condición es **verdadera**, dirigiéndolo directamente al inicio del bloque de ejecución. Si es falsa, continúa secuencialmente evaluando `cond2`.

### 17. ¿Qué limitación severa posee la implementación de condiciones múltiples en este compilador?
> **Respuesta:** La gramática define `condicion_multiple` únicamente como `condicion_simple conector condicion_simple` o `NOT condicion_simple`. Esto limita las condiciones a un máximo de dos expresiones simples y un solo conector. No existe recursividad en la regla (ej: `condicion_multiple conector condicion_multiple`), por lo que no es posible procesar tres o más condiciones lógicas encadenadas.

### 18. En el ciclo especial `while VARIABLE in [ exp1, exp2, ... ] do`, ¿cuándo se evalúan las expresiones del corchete?
> **Respuesta:** Se evalúan dinámicamente en cada iteración del bucle. El código intermedio generado sitúa la evaluación de estas expresiones y sus respectivas comparaciones dentro de la sección condicional del ciclo. Si las expresiones del corchete contienen variables mutables, sus valores se recalcularán en cada ciclo, lo cual puede producir efectos colaterales inesperados.

### 19. ¿Qué ocurre si un programador intenta declarar una lista vacía en el ciclo especial: `while x in [] do ...`?
> **Respuesta:** Fallará en la etapa de análisis sintáctico. La regla `expresiones_ciclo_while_especial` exige la presencia de `lista_expresiones`, la cual recursivamente requiere al menos una `expresion`. Por lo tanto, `[]` generará un error de sintaxis directo provisto por PLY.

### 20. ¿Qué función cumple el terceto que contiene únicamente la palabra reservada `'WHILE'`?
> **Respuesta:** Sirve como un marcador de posición (ancla) en la lista de tercetos. Le indica al generador de ensamblador el índice exacto donde comienza la evaluación condicional del ciclo, permitiendo emitir una etiqueta de salto (ej: `L5:`) en ese punto exacto para que el salto incondicional `BI` al final del bucle sepa a dónde retornar.

### 21. ¿Es eficiente la traducción del ciclo especial `while in` en términos de saltos?
> **Respuesta:** No. Se utiliza una comparación secuencial elemento por elemento. Si la lista contiene $N$ expresiones, el compilador generará una cadena de $N$ comparaciones y saltos condicionales `BE` (Branch if Equal) por cada iteración. Esto da una complejidad de $O(N)$ en el peor de los casos para la evaluación de la condición de entrada, lo cual es ineficiente comparado con una tabla de saltos indirectos, pero simple de implementar sin soporte runtime.

### 22. ¿Cómo se previene el desbordamiento de la pila de expresiones intermedias `indice_terceto_expresion`?
> **Respuesta:** El compilador no realiza comprobaciones de desbordamiento de pila. Se confía en la correctitud sintáctica garantizada por las reglas recursivas de precedencia de PLY. Como cada operador matemático consume un número exacto de operandos de la pila y produce exactamente uno, el balance de la pila está garantizado matemáticamente a nivel de gramática.

---

## Bloque 4: Generación de Código Objeto (`asm_generator.py`)

### 23. ¿Por qué declaras variables usando `dd` (32 bits) pero configuras el modelo de memoria como `.MODEL LARGE` de 16 bits?
> **Respuesta:** Esto permite aprovechar los registros extendidos de 32 bits de la arquitectura Intel 386 (mediante la directiva `.386`) para facilitar la aritmética y el coprocesador, mientras se mantiene el binario ejecutable bajo el modelo segmentado de 16 bits nativo de DOS. El riesgo es que las operaciones de direccionamiento de memoria indirecto deben seguir respetando los segmentos de 16 bits de 64 KB de capacidad máxima.

### 24. Explica detalladamente por qué al comparar variables de tipo `Float` en `asm_generator.py` cambias los saltos firmados a saltos sin signo (ej. `jle` a `jbe`). ¿Qué rol cumple la instrucción `sahf`?
> **Respuesta:** La FPU del x87 almacena los resultados de las comparaciones en sus propios bits de condición (`C0`, `C1`, etc.). Para utilizarlos en saltos lógicos del CPU, volcamos este registro a `AX` y luego ejecutamos `sahf` para copiar dichos bits a los flags del procesador (`CF`, `ZF`, etc.). En el procesador, estos bits se corresponden con los flags utilizados para evaluar condiciones sin signo. Por ende, los saltos con signo tradicionales darían resultados erróneos y deben mapearse a saltos sin signo (como `ja`, `jb`, `jae`, `jbe`).

### 25. En la asignación de cadenas, utilizas `lodsb` y `stosb`. ¿Por qué es obligatorio ejecutar `cld` antes de iniciar la copia?
> **Respuesta:** La instrucción `cld` limpia el Direction Flag (lo pone en 0). Esto garantiza que las instrucciones de procesamiento de strings (`lodsb` y `stosb`) incrementen automáticamente los registros de índice `SI` y `DI` en cada paso. Si el flag estuviera en 1 (debido a otra rutina que ejecutó `std`), los índices se decrementarían, copiando la cadena al revés y corrompiendo la memoria adyacente.

### 26. ¿Por qué es necesario inicializar el registro de segmento extra `ES` con el valor de `@DATA` en `START`?
> **Respuesta:** La instrucción de copiado de bytes `stosb` escribe el contenido del registro `AL` en la dirección de memoria apuntada estrictamente por el par `ES:DI`. Si no inicializamos `ES` para apuntar a nuestro segmento de datos común `@DATA` (al igual que `DS`), la copia de strings intentará escribir en un segmento de memoria incorrecto, resultando en corrupción de memoria o violación de acceso.

### 27. ¿Por qué no ocurre un desbordamiento de la pila de registros de la FPU (`ST(0)` a `ST(7)`) en expresiones matemáticas muy complejas?
> **Respuesta:** Porque el compilador lineariza las operaciones aritméticas complejas a nivel de terceto y fuerza a que el resultado de cada sub-expresión se extraiga inmediatamente de la FPU y se guarde en una variable temporal en memoria a través de la instrucción `fstp dword ptr [tmpX]`. Como la pila de la FPU se vacía en cada operación individual, la profundidad máxima de registros de la FPU utilizados simultáneamente nunca supera los 2.

### 28. ¿Cómo maneja el generador de ensamblador los caracteres especiales como el salto de línea `\n` dentro de las cadenas constantes?
> **Respuesta:** El script de generación detecta la secuencia literal `\n` y la descompone en constantes de bytes equivalentes a sus códigos ASCII correspondientes: `13` (Carriage Return) y `10` (Line Feed). La declaración final en la sección `.DATA` se escribe separada por comas (ej. `db "Mensaje", 13, 10, "$"`), evitando un salto de línea físico en el archivo `.asm` que generaría errores en TASM.

### 29. ¿Qué impacto tiene declarar los flotantes con `dd` (32 bits) si la FPU de x86 trabaja internamente con precisión de 80 bits?
> **Respuesta:** Al cargar una variable con `fld dword ptr`, la FPU promueve el valor a 80 bits internamente para minimizar la pérdida de precisión durante el cálculo. Al guardar el resultado con `fstp dword ptr`, el valor vuelve a truncarse a 32 bits. Esto causa pequeñas pérdidas por redondeo en operaciones consecutivas, pero optimiza a la mitad el consumo de memoria respecto a usar variables de doble precisión (`dq` / 64 bits) y es más que suficiente para el propósito del lenguaje.

### 30. ¿Por qué el compilador genera etiquetas `L{idx}:` para cada terceto, incluso si no son destino de ningún salto condicional o incondicional?
> **Respuesta:** Es una simplificación del diseño del generador de código objeto. En lugar de precalcular qué tercetos son destinos de saltos para colocar etiquetas únicamente en ellos, el generador estampa una etiqueta secuencial para todos los tercetos por defecto. Aunque no afecta el rendimiento ni el tamaño del archivo ejecutable binario, sí genera código fuente `.asm` redundante y menos legible para el ojo humano.
