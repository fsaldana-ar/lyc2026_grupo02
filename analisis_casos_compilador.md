# Análisis Detallado de Flujo del Compilador: 60 Casos Prácticos Paso a Paso

---

## Tabla de Tokens y Palabras Reservadas

El analizador léxico (`lexer.py`) reconoce los siguientes tokens y palabras clave para estructurar el código fuente:

| Nombre del Token | Patrón / Expresión Regular / Valor | Tipo de Token | Explicación / Propósito en el Lenguaje |
| :--- | :--- | :--- | :--- |
| **`INIT`** | `init` | Reservada | Define la sección de inicio del bloque de declaraciones de variables. |
| **`READ`** | `read` | Reservada | Instrucción de lectura de datos por consola (entrada estándar). |
| **`WRITE`** | `write` | Reservada | Instrucción de escritura/impresión de datos en consola (salida estándar). |
| **`IF`** | `if` | Reservada | Palabra clave para la estructura condicional de selección simple/doble. |
| **`ELSE`** | `else` | Reservada | Rama alternativa ejecutada si la condición del `if` es falsa. |
| **`OR`** | `or` | Reservada | Operador lógico de disyunción (O lógico) con evaluación por cortocircuito. |
| **`NOT`** | `not` | Reservada | Operador lógico de negación (NO lógico) que invierte la condición. |
| **`AND`** | `and` | Reservada | Operador lógico de conjunción (Y lógico) con evaluación por cortocircuito. |
| **`MOD`** | `mod` (insensible a mayúsculas) | Reservada | Operador aritmético que calcula el residuo de la división entera. |
| **`DIV`** | `div` (insensible a mayúsculas) | Reservada | Operador aritmético que realiza la división entera (truncada). |
| **`WHILE`** | `while` | Reservada | Palabra clave para iniciar bucles iterativos controlados por condición. |
| **`IN`** | `in` | Reservada | Conector del ciclo iterativo especial para recorrer una lista de expresiones. |
| **`DO`** | `do` | Reservada | Palabra clave que introduce el cuerpo de sentencias del ciclo especial. |
| **`ENDWHILE`** | `endwhile` | Reservada | Palabra clave que indica la finalización del ciclo especial. |
| **`INT`** | `Int` | Reservada | Especificador del tipo de dato entero con signo de 16 bits. |
| **`FLOAT`** | `Float` | Reservada | Especificador del tipo de dato punto flotante con signo de 32 bits. |
| **`STRING`** | `String` | Reservada | Especificador del tipo de dato para cadenas de texto de hasta 50 caracteres. |
| **`COMA`** | `,` | Símbolo | Separador de variables en declaraciones y de expresiones en listas. |
| **`DOSPUNTOS`** | `:` | Símbolo | Delimitador que separa la lista de variables de su tipo de dato. |
| **`ASIGNACION`** | `:=` | Símbolo | Operador utilizado para asignar el valor de una expresión a una variable. |
| **`MAS`** | `+` | Símbolo | Operador de suma aritmética. |
| **`MENOS`** | `-` | Símbolo | Operador de resta aritmética o signo negativo. |
| **`DIVISION`** | `/` | Símbolo | Operador de división real (de punto flotante). |
| **`MULTIPLICACION`** | `*` | Símbolo | Operador de multiplicación aritmética. |
| **`COMP_IGUAL`** | `==` | Comparador | Operador de comparación lógico de igualdad. |
| **`COMP_DISTINTO`** | `<>` | Comparador | Operador de comparación lógico de desigualdad (distinto). |
| **`COMP_MAYOR`** | `>` | Comparador | Operador de comparación lógico mayor que. |
| **`COMP_MENOR`** | `<` | Comparador | Operador de comparación lógico menor que. |
| **`COMP_MAYOR_IGUAL`** | `>=` | Comparador | Operador de comparación lógico mayor o igual que. |
| **`COMP_MENOR_IGUAL`** | `<=` | Comparador | Operador de comparación lógico menor o igual que. |
| **`A_LLAVE`** | `{` | Símbolo | Apertura de bloque ejecutable de sentencias o bloque de declaraciones. |
| **`C_LLAVE`** | `}` | Símbolo | Cierre de bloque ejecutable de sentencias o bloque de declaraciones. |
| **`A_CORCHETE`** | `[` | Símbolo | Apertura de delimitador para listas (usado en el ciclo especial). |
| **`C_CORCHETE`** | `]` | Símbolo | Cierre de delimitador para listas (usado en el ciclo especial). |
| **`A_PARENTESIS`** | `(` | Símbolo | Apertura de paréntesis para agrupar expresiones y rodear condiciones. |
| **`C_PARENTESIS`** | `)` | Símbolo | Cierre de paréntesis para agrupar expresiones y rodear condiciones. |
| **`VARIABLE`** | `[a-zA-Z](\w\|_)*` | Identificador | Nombre de variables definidas por el usuario (máx. 20 caracteres). |
| **`N_ENTERO`** | `0\|-?[1-9]\d*` | Literal | Valor constante de tipo entero de 16 bits firmado ($[-32768, 32767]$). |
| **`N_FLOTANTE`** | `-?\d+[.]\d*\|-?[.]\d+` | Literal | Valor constante de tipo punto flotante de 32 bits firmado ($[-3.4e38, 3.4e38]$). |
| **`CTE_STRING`** | `\"[^"]*\"` | Literal | Cadena constante encerrada en comillas dobles (máx. 50 caracteres). |

---

## Estructura General del Flujo
Cada caso describe el recorrido a través de los siguientes archivos del proyecto:
1. **`lexer.py`:** Entrada de caracteres $\rightarrow$ Reconocimiento de expresiones regulares $\rightarrow$ Llamadas a `itoken.py` $\rightarrow$ Salida de tokens.
2. **`parser.py`:** Consumo de tokens $\rightarrow$ Reglas de gramática $p\_...$ $\rightarrow$ Validaciones de tipo $\rightarrow$ Creación de tercetos vía `terceto.py`.
3. **`terceto.py`:** Almacenamiento indexado y modificación diferida (*backfilling*).
4. **`i_token.py`:** Gestión de la tabla de símbolos (`symbol-table.txt`).
5. **`asm_generator.py`:** Mapeo de tercetos y tabla de símbolos $\rightarrow$ Escritura de instrucciones y variables en sintaxis TASM de 16/32 bits.

---

## 60 Casos de Estudio Detallados

---

### Caso 1: Declaración de una variable entera (`x : Int`)
* **Léxico (`lexer.py`):**
  * `x` es procesado por `t_VARIABLE(t)`. Verifica que no esté en `reserved`. Llama a `itoken.crear_token("x", "-")` (agrega `"x"` con tipo `'-'` a la tabla de símbolos) y retorna el token `VARIABLE`.
  * `:` se reconoce como `t_DOSPUNTOS` y retorna `DOSPUNTOS`.
  * `Int` se reconoce como la reservada `INT` y retorna `INT`.
* **Sintáctico/Semántico (`parser.py`):**
  * Se activa `p_lista_variables` que retorna `["x"]`.
  * Se activa `p_tipo` que retorna `"Int"`.
  * Se dispara `p_declaracion` (`declaracion : lista_variables DOSPUNTOS tipo`). Valida que `x` exista en `itoken` y su tipo sea `'-'`. Ejecuta `itoken.set_tipo("x", "Int")`.
* **Código Intermedio (`terceto.py`):** No se generan tercetos para la fase declarativa.
* **Código Objeto (`asm_generator.py`):**
  * `build_data_section` itera sobre la tabla de símbolos. Al encontrar `"x"` con tipo `"Int"`, escribe en la sección `.DATA`:
    ```assembly
    x dd ?
    ```

---

### Caso 2: Declaración múltiple de variables flotantes (`a, b : Float`)
* **Léxico (`lexer.py`):**
  * `a` $\rightarrow$ `t_VARIABLE` $\rightarrow$ llama a `itoken.crear_token("a", "-")`.
  * `,` $\rightarrow$ `t_COMA` $\rightarrow$ retorna `COMA`.
  * `b` $\rightarrow$ `t_VARIABLE` $\rightarrow$ llama a `itoken.crear_token("b", "-")`.
  * `:` $\rightarrow$ `t_DOSPUNTOS`.
  * `Float` $\rightarrow$ reservada `FLOAT`.
* **Sintáctico/Semántico (`parser.py`):**
  * `p_lista_variables` se dispara recursivamente acumulando `["a", "b"]`.
  * `p_declaracion` itera la lista. Verifica que ambas tengan tipo `'-'` y aplica `itoken.set_tipo("a", "Float")` y `itoken.set_tipo("b", "Float")`.
* **Código Intermedio:** No se generan tercetos.
* **Código Objeto (`asm_generator.py`):**
  * Escribe en la sección `.DATA`:
    ```assembly
    a dd ?
    b dd ?
    ```

---

### Caso 3: Asignación de constante entera (`x := 10`)
* **Léxico (`lexer.py`):**
  * `x` $\rightarrow$ `t_VARIABLE` (ya declarada).
  * `:=` $\rightarrow$ `t_ASIGNACION`.
  * `10` $\rightarrow$ `t_N_ENTERO`. Llama a `itoken.crear_token("_10", "10", "cte_int")` y retorna `N_ENTERO`.
* **Sintáctico/Semántico (`parser.py`):**
  * Se ejecuta `p_variable_asignacion` para `x` y crea el terceto `[0] - (x, _, _)`. Retorna `{"variable": "x", "indice": 0}`.
  * Se ejecuta `p_elemento` para el entero `10`. Crea el terceto `[1] - (10, _, _)` y almacena su índice en `indice_terceto_expresion = [1]`.
  * Se ejecuta `p_asignacion`. Comprueba que el tipo de `x` (`Int`) coincida con el de `10` (`Int`). Crea el terceto de asignación:
    ```python
    terceto.crear_terceto(':=', '[0]', '[1]')
    ```
* **Código Intermedio (`terceto.py`):**
  * Genera en `intermediate-code.txt`:
    ```text
    [0] - (x,_,_)
    [1] - (10,_,_)
    [2] - (:=,[0],[1])
    ```
* **Código Objeto (`asm_generator.py`):**
  * `build_data_section` escribe `_10 dd 10`.
  * `generate_asm` procesa el terceto `[2]`: resuelve operandos (`x` y `_10`) y genera:
    ```assembly
    mov eax, _10
    mov x, eax
    ```

---

### Caso 4: Asignación de constante flotante (`y := 3.14`)
* **Léxico (`lexer.py`):**
  * `3.14` activa `t_N_FLOTANTE`. Llama a `itoken.crear_token("_3.14", "3.14", "cte_float")`. Retorna el valor `3.14` y el token `N_FLOTANTE`.
* **Sintáctico/Semántico (`parser.py`):**
  * `p_variable_asignacion` crea terceto `[0]` para `y`.
  * `p_elemento` crea terceto `[1]` para `3.14`.
  * `p_asignacion` valida compatibilidad `Float` con `Float`. Genera el terceto `[2] - (:=, [0], [1])`.
* **Código Intermedio:**
  ```text
  [0] - (y,_,_)
  [1] - (3.14,_,_)
  [2] - (:=,[0],[1])
  ```
* **Código Objeto (`asm_generator.py`):**
  * `build_data_section` sanitiza `_3.14` reemplazando el punto por un guion bajo: `_3_14 dd 3.14`.
  * `generate_asm` procesa `:=` y genera:
    ```assembly
    mov eax, _3_14
    mov y, eax
    ```

---

### Caso 5: Asignación de constante string (`s := "hola"`)
* **Léxico (`lexer.py`):**
  * `"hola"` activa `t_CTE_STRING`. Extrae el contenido `hola`. Llama a `itoken.crear_token("_hola", "hola", "cte_str", 4)`. Retorna `CTE_STRING`.
* **Sintáctico/Semántico (`parser.py`):**
  * `p_variable_asignacion` crea terceto `[0]` para `s`.
  * `p_asignacion` valida compatibilidad `String` con `cte_string`.
  * Genera un terceto intermedio con la constante: `[1] - ("hola", _, _)`.
  * Genera el terceto de asignación: `[2] - (:=, [0], [1])`.
* **Código Intermedio:**
  ```text
  [0] - (s,_,_)
  [1] - ("hola",_,_)
  [2] - (:=,[0],[1])
  ```
* **Código Objeto (`asm_generator.py`):**
  * `build_data_section` asocia la constante con una etiqueta única, ej: `STR_0 db "hola","$"`.
  * `generate_asm` detecta operandos string y genera el lazo de copia a nivel de bytes:
    ```assembly
    mov si, OFFSET STR_0
    mov di, OFFSET s
    cld
    copy_string_2:
    lodsb
    stosb
    cmp al, '$'
    jne copy_string_2
    ```

---

### Caso 6: Suma de enteros (`x + y`)
* **Léxico (`lexer.py`):**
  * `+` activa `t_MAS` y retorna `MAS`.
* **Sintáctico/Semántico (`parser.py`):**
  * `p_elemento` crea terceto `[0]` para `x` e `[1]` para `y`. Apila sus índices en `indice_terceto_expresion = [0, 1]`.
  * `p_expresion_mas` desapila `t1 = 1` y `t2 = 0`. Valida que ambos sean numéricos.
  * Llama a `terceto.crear_terceto('+', '[0]', '[1]')` (índice 2). Apila `[2]` en `indice_terceto_expresion`.
* **Código Intermedio (`terceto.py`):**
  * Genera en `intermediate-code.txt`:
    ```text
    [0] - (x,_,_)
    [1] - (y,_,_)
    [2] - (+,[0],[1])
    ```
* **Código Objeto (`asm_generator.py`):**
  * Al detectar operador aritmético entero `+`, genera:
    ```assembly
    mov eax, x
    add eax, y
    mov tmp2, eax
    ```
    (Y declara `tmp2 dd ?` en `.DATA`).

---

### Caso 7: Resta de flotantes (`a - b`)
* **Léxico (`lexer.py`):**
  * `-` activa `t_MENOS` y retorna `MENOS`.
* **Sintáctico/Semántico (`parser.py`):**
  * `p_expresion_menos` saca operandos `b` (índice `1`) y `a` (índice `0`). Valida que sean numéricos.
  * Crea `terceto.crear_terceto('-', '[0]', '[1]')` (índice 2) de tipo `Float`.
* **Código Intermedio:**
  ```text
  [0] - (a,_,_)
  [1] - (b,_,_)
  [2] - (-,[0],[1])
  ```
* **Código Objeto (`asm_generator.py`):**
  * `generate_asm` determina que los tipos involucrados son `Float`.
  * Llama a `generate_expression_code` y genera instrucciones de la FPU:
    ```assembly
    fld dword ptr [a]
    fsub dword ptr [b]
    fstp dword ptr [tmp2]
    ```

---

### Caso 8: Multiplicación mixta (`x * a`) siendo `x : Int` y `a : Float`
* **Léxico (`lexer.py`):**
  * `*` activa `t_MULTIPLICACION` y retorna `MULTIPLICACION`.
* **Sintáctico/Semántico (`parser.py`):**
  * `p_termino_multiplicacion` desapila operandos. Detecta tipo de `x` (`Int`) y de `a` (`Float`).
  * `obtener_tipo_dato` promueve el resultado a `Float` (aritmética mixta).
  * Crea terceto `[2] - (*, [0], [1])`.
* **Código Intermedio:**
  ```text
  [0] - (x,_,_)
  [1] - (a,_,_)
  [2] - (*,[0],[1])
  ```
* **Código Objeto (`asm_generator.py`):**
  * `generate_asm` evalúa el tipo de `tmp2` como `Float`. Genera instrucciones FPU:
    ```assembly
    fld dword ptr [x]
    fmul dword ptr [a]
    fstp dword ptr [tmp2]
    ```

---

### Caso 9: División real (`x / y`) siendo enteros
* **Léxico (`lexer.py`):**
  * `/` activa `t_DIVISION` y retorna `DIVISION`.
* **Sintáctico/Semántico (`parser.py`):**
  * `p_termino_division` valida operandos enteros. Por diseño, la división real `/` siempre se promociona a `Float`.
  * Crea terceto `[2] - (/, [0], [1])` de tipo `Float`.
* **Código Intermedio:**
  ```text
  [0] - (x,_,_)
  [1] - (y,_,_)
  [2] - (/,[0],[1])
  ```
* **Código Objeto (`asm_generator.py`):**
  * Al ser tipo resultante `Float`, utiliza la FPU:
    ```assembly
    fld dword ptr [x]
    fdiv dword ptr [y]
    fstp dword ptr [tmp2]
    ```

---

### Caso 10: División entera (`x DIV y`)
* **Léxico (`lexer.py`):**
  * `div` es procesado por `t_VARIABLE`. Convierte a minúsculas, detecta reservada `DIV` y retorna `DIV`.
* **Sintáctico/Semántico (`parser.py`):**
  * `p_division` comprueba que ambos sean enteros. Retorna tipo `Int`.
  * Crea terceto `[2] - (DIV, [0], [1])`.
* **Código Intermedio:**
  ```text
  [0] - (x,_,_)
  [1] - (y,_,_)
  [2] - (DIV,[0],[1])
  ```
* **Código Objeto (`asm_generator.py`):**
  * Ejecuta la división entera mediante registros de 32 bits y división con signo `idiv`:
    ```assembly
    mov eax, x
    cdq                  ; Extiende signo de EAX a EDX:EAX
    mov ebx, y
    idiv ebx             ; EAX = Cociente, EDX = Resto
    mov tmp2, eax
    ```

---

### Caso 11: Operación de resto entero (`x MOD y`)
* **Léxico (`lexer.py`):**
  * `mod` activa `t_VARIABLE`, mapea a reservada `MOD` e inserta `MOD`.
* **Sintáctico/Semántico (`parser.py`):**
  * `p_modulo` comprueba tipos enteros y crea terceto `[2] - (MOD, [0], [1])`.
* **Código Intermedio:**
  ```text
  [0] - (x,_,_)
  [1] - (y,_,_)
  [2] - (MOD,[0],[1])
  ```
* **Código Objeto (`asm_generator.py`):**
  * Utiliza `idiv` y copia el residuo del registro `EDX`:
    ```assembly
    mov eax, x
    cdq
    mov ebx, y
    idiv ebx
    mov tmp2, edx        ; Guarda el residuo (MOD)
    ```

---

### Caso 12: Precedencia aritmética (`x + y * z`)
* **Léxico (`lexer.py`):** Identifica variables y operadores.
* **Sintáctico/Semántico (`parser.py`):**
  * La precedencia declarada en `precedence` le da prioridad a `MULTIPLICACION` sobre `MAS`.
  * Por ende, se reduce primero el producto `y * z` (creando terceto `[3] - (*, [1], [2])`).
  * Luego se reduce la suma `x + [3]` (creando terceto `[4] - (+, [0], [3])`).
* **Código Intermedio:**
  ```text
  [0] - (x,_,_)
  [1] - (y,_,_)
  [2] - (z,_,_)
  [3] - (*,[1],[2])
  [4] - (+,[0],[3])
  ```
* **Código Objeto (`asm_generator.py`):**
  * Resuelve de forma secuencial y lineal:
    ```assembly
    mov eax, y
    imul eax, z
    mov tmp3, eax

    mov eax, x
    add eax, tmp3
    mov tmp4, eax
    ```

---

### Caso 13: Comparación simple (`x < y`)
* **Léxico (`lexer.py`):**
  * `<` activa `t_COMP_MENOR` y retorna `COMP_MENOR`.
* **Sintáctico/Semántico (`parser.py`):**
  * `p_condicion_simple_expi` almacena el índice de `x` (`indice_expresion_izquierda_seleccion = 0`).
  * `p_condicion_simple` (`condicion_simple : condicion_simple_expi comparador expresion`) valida tipos.
  * Crea terceto de comparación: `[2] - (CMP, [0], [1])`.
  * Obtiene el código condicional invertido de `diccionarioComparadores` para `<` que es `"BGE"`.
  * Crea terceto de salto condicional incompleto: `[3] - (BGE, _, _)`.
  * Almacena el índice `3` en `indice_comienzo_seleccion` (si `flag_ciclo_seleccion` es `True`).
* **Código Intermedio:**
  ```text
  [0] - (x,_,_)
  [1] - (y,_,_)
  [2] - (CMP,[0],[1])
  [3] - (BGE,_,_)
  ```

---

### Caso 14: Sentencia `if` sin `else` (`if (x < y) { write(x) }`)
* **Léxico (`lexer.py`):** Procesa palabras clave y expresiones.
* **Sintáctico/Semántico (`parser.py`):**
  * `p_comienzo_seleccion_if` (`IF`) activa `flag_ciclo_seleccion = True`.
  * Se procesa la condición simple (Caso 13), apilando el índice del salto condicional `[3]` en `indice_comienzo_seleccion`.
  * Se procesa el cuerpo (programa) generando el terceto `[4] - (WRITE, x, _)`.
  * En `p_seleccion` (`seleccion : comienzo_seleccion_if A_PARENTESIS condicion_simple ...`), se desapila el salto `3`.
  * Modifica el salto condicional incompleto `[3]` para que salte a la instrucción posterior al bloque (índice actual `5`).
* **Código Intermedio:**
  ```text
  [2] - (CMP,[0],[1])
  [3] - (BGE,[5],_)
  [4] - (WRITE,x,_)
  ```
* **Código Objeto (`asm_generator.py`):**
  ```assembly
  L2:
      mov eax, x
      cmp eax, y
  L3:
      jge L5
  L4:
      DisplayInteger x
  L5:
  ```

---

### Caso 15: Sentencia `if` con `else` (`if (x < y) { x := 1 } else { x := 2 }`)
* **Léxico (`lexer.py`):** Detecta palabra reservada `ELSE`.
* **Sintáctico/Semántico (`parser.py`):**
  * Al finalizar el cuerpo del `if`, se procesa `p_seleccion_else` (`ELSE`). Crea un salto incondicional incompleto: `[4] - (BI, _, _)`. Apila `4` en `indice_comienzo_seleccion_else`.
  * Se reduce `p_seleccion` con rama else.
  * Desapila el salto condicional de la condición (`[2]`) y lo redirecciona al inicio del bloque else (que está en `indice_else + 1` $\rightarrow$ `5`).
  * Desapila el `BI` (`[4]`) y lo redirecciona al final de toda la selección (índice actual `7`).
* **Código Intermedio:**
  ```text
  [1] - (CMP,x,y)
  [2] - (BGE,[5],_)
  [3] - (:=,x,1)
  [4] - (BI,[7],_)
  [5] - (:=,x,2)
  ```
* **Código Objeto (`asm_generator.py`):**
  ```assembly
  L1: mov eax, x
      cmp eax, y
  L2: jge L5
  L3: ; (cuerpo if)
  L4: jmp L7
  L5: ; (cuerpo else)
  L7: ; (fin de selección)
  ```

---

### Caso 16: Anidamiento de `if` (`if (c1) { if (c2) { programa } }`)
* **Sintáctico/Semántico (`parser.py`):**
  * Primer `IF` $\rightarrow$ `flag_ciclo_seleccion = True`.
  * Condición 1 crea salto condicional `[2] - (BGE, _, _)`. `indice_comienzo_seleccion = [2]`.
  * Segundo `IF` $\rightarrow$ `flag_ciclo_seleccion = True`.
  * Condición 2 crea salto condicional `[5] - (BGE, _, _)`. `indice_comienzo_seleccion = [2, 5]`.
  * Cierre del segundo `if`: desapila `5`, modifica terceto `5` para saltar a `[7]`.
  * Cierre del primer `if`: desapila `2`, modifica terceto `2` para saltar a `[7]`.
* **Código Intermedio:**
  ```text
  [2] - (BGE,[7],_)
  ...
  [5] - (BGE,[7],_)
  ...
  ```

---

### Caso 17: Bucle `while` estándar (`while (x < y) { x := x + 1 }`)
* **Sintáctico/Semántico (`parser.py`):**
  * `p_comienzo_ciclo_while` (`WHILE`): activa `flag_ciclo_while = True`. Crea terceto de etiqueta `[0] - (WHILE, _, _)`. Apila `0` en `indice_etiqueta_ciclo_while`.
  * Condición simple genera `[3] - (CMP, x, y)` y `[4] - (BGE, _, _)`. Apila `4` en `indice_comienzo_ciclo_while`.
  * Cuerpo genera tercetos de suma y asignación.
  * `p_ciclo_while` crea un salto incondicional de retorno `[7] - (BI, _, _)`.
  * Modifica `[7]` con el inicio del ciclo desapilado: `[7] - (BI, [0], _)`.
  * Modifica el salto de salida condicional `[4]` con el índice de fin de bucle (`8`).
* **Código Intermedio:**
  ```text
  [0] - (WHILE,_,_)
  [3] - (CMP,x,y)
  [4] - (BGE,[8],_)
  ... (cuerpo)
  [7] - (BI,[0],_)
  ```
* **Código Objeto (`asm_generator.py`):**
  ```assembly
  L0: ; etiqueta de retorno
  L3: mov eax, x
      cmp eax, y
  L4: jge L8
  ... ; cuerpo
  L7: jmp L0
  L8: ; salida
  ```

---

### Caso 18: Negación lógica (`NOT (x < y)`)
* **Léxico (`lexer.py`):** Detecta palabra reservada `NOT`.
* **Sintáctico/Semántico (`parser.py`):**
  * Se procesa la condición simple `x < y` que genera `[2] - (CMP, x, y)` y `[3] - (BGE, _, _)`.
  * La regla `p_condicion_multiple` (`NOT condicion_simple`) toma el operador de la condición simple (ej: `BGE`).
  * Ejecuta `terceto.modificar_terceto(3, diccionarioComparadoresNot.get(p[2]))`. Al ser el operador original `<` (que mapeó a `BGE`), busca en `diccionarioComparadoresNot` el inverso de `<` que es `BLT` (Branch if Less Than / Salta si es menor).
* **Código Intermedio:**
  ```text
  [2] - (CMP,x,y)
  [3] - (BLT,_,_)
  ```

---

### Caso 19: Conector lógico `AND` (`if (x < y AND a > b)`)
* **Sintáctico/Semántico (`parser.py`):**
  * Primera condición crea `[2] - (CMP, x, y)` y `[3] - (BGE, _, _)`. `indice_comienzo_seleccion = [3]`.
  * Al ver `AND`, se reactiva `flag_ciclo_seleccion = True` para la segunda condición.
  * Segunda condición crea `[6] - (CMP, a, b)` y `[7] - (BLE, _, _)`. `indice_comienzo_seleccion = [3, 7]`.
  * En `p_seleccion` (siendo conector `and`):
    * Desapila el segundo salto (`7`) y lo direcciona al final del bloque.
    * Desapila el primer salto (`3`) y lo direcciona al mismo final del bloque. (Si cualquiera falla, salta fuera).
* **Código Intermedio:**
  ```text
  [3] - (BGE,[9],_)
  [7] - (BLE,[9],_)
  ```

---

### Caso 20: Conector lógico `OR` (`if (x < y OR a > b)`)
* **Sintáctico/Semántico (`parser.py`):**
  * Primera condición crea `[3] - (BGE, _, _)`. `indice_comienzo_seleccion = [3]`.
  * Segunda condición crea `[7] - (BLE, _, _)`. `indice_comienzo_seleccion = [3, 7]`.
  * En `p_seleccion` (siendo conector `or`):
    * Desapila el segundo salto `7` y lo redirecciona al final del bloque (`[9]`).
    * Desapila el primer salto `3`, modifica su código de instrucción usando `diccionarioComparadoresNot` para que salte si es **verdadero** (se convierte en `BLT`), y lo redirecciona para que salte al inicio del cuerpo del `if` (justo después de la segunda condición $\rightarrow$ `[8]`).
* **Código Intermedio:**
  ```text
  [3] - (BLT,[8],_)  ; Salta al cuerpo si cond1 es verdadera
  [7] - (BLE,[9],_)  ; Salta al final si cond2 es falsa
  ```

---

### Caso 21: Bucle especial (`while x in [10, 20] do x := x + 1 endwhile`)
* **Sintáctico/Semántico (`parser.py`):**
  * `p_variable_ciclo_while_especial` guarda los datos de la variable de control `x` (`tipo: Int`).
  * `p_lista_expresiones` apila los índices de los tercetos de `10` y `20` en `indice_expresion_ciclo_while_especial`.
  * En `p_expresiones_ciclo_while_especial` (dentro del corchete):
    1. Llama a `crear_variable_auxiliar()` para obtener `@aux1`.
    2. Crea tercetos para inicializarla en 0:
       `[4] - (@aux1, _, _)`, `[5] - (0, _, _)`, `[6] - (:=, [4], [5])`.
    3. Define etiqueta de ciclo `[7] - (WHILE, _, _)`.
    4. Compara `@aux1` con la longitud de la lista (2): si es mayor o igual, sale:
       `[10] - (CMP, @aux1, 2)`, `[11] - (BGE, _, _)`.
    5. Para cada elemento, comprueba el índice de iteración `@aux1`:
       Si `@aux1 == 0`, asigna `x := 10`.
       Si `@aux1 == 1`, asigna `x := 20`.
    6. Al final de la iteración, incrementa la variable auxiliar:
       `@aux1 := @aux1 + 1`.
  * Al cerrar el bloque en `p_ciclo_especial`: se genera el salto de retorno `BI` a la etiqueta `[7]`, y se resuelven las salidas del bucle.
* **Código Intermedio:** Genera una estructura secuencial detallada con saltos y asignaciones.

---

### Caso 22: Asignación entre variables de texto (copia de strings)
* **Sintáctico/Semántico (`parser.py`):**
  * Valida que ambas variables tengan tipo `"String"`. Genera terceto `:=`.
* **Código Objeto (`asm_generator.py`):**
  * `generate_asm` analiza los operandos. Al detectar variables declaradas como `String` en la tabla de símbolos, genera una copia por lazo:
    ```assembly
    mov si, OFFSET variable_fuente
    mov di, OFFSET variable_destino
    cld
    copy_string_X:
    lodsb
    stosb
    cmp al, '$'
    jne copy_string_X
    ```

---

### Caso 23: Lectura por teclado (`read(x)`)
* **Léxico (`lexer.py`):** `read` se reconoce como reservada `READ`.
* **Sintáctico/Semántico (`parser.py`):**
  * `p_entrada` valida que la variable esté declarada y genera el terceto: `[0] - (READ, x, _)`.
* **Código Objeto (`asm_generator.py`):**
  * En `generate_asm`, mapea el operador `READ` al tipo de la variable en la tabla de símbolos.
  * Si `x` es `Int`, escribe:
    ```assembly
    GetInteger x
    ```
  * Si fuera `Float`, escribiría:
    ```assembly
    GetFloat x
    ```

---

### Caso 24: Escritura de cadena constante (`write("hola")`)
* **Léxico (`lexer.py`):** `"hola"` activa `t_CTE_STRING`, se agrega a tabla de símbolos.
* **Sintáctico/Semántico (`parser.py`):**
  * `p_salida` detecta constante string. Crea terceto: `[0] - (WRITE, "hola", _)`.
* **Código Objeto (`asm_generator.py`):**
  * `build_data_section` asigna etiqueta, ej: `STR_1 db "hola","$"`.
  * `generate_asm` traduce `WRITE` de string constante usando la interrupción nativa de DOS (Servicio 9):
    ```assembly
    mov dx, OFFSET STR_1
    mov ah, 9
    int 21h
    ```

---

### Caso 25: Escritura de variable numérica (`write(x)`)
* **Sintáctico/Semántico (`parser.py`):**
  * `p_salida` valida que la variable esté declarada. Crea terceto: `[0] - (WRITE, x, _)`.
* **Código Objeto (`asm_generator.py`):**
  * Si `x` es `Int`, invoca la macro correspondiente en ensamblador:
    ```assembly
    DisplayInteger x
    ```
  * Si `x` es `Float`, invoca la macro con parámetros de formato:
    ```assembly
    DisplayFloat x, 2
    ```

---

### Caso 26: Error Semántico: Variable no declarada en el bloque `init`
* **Léxico (`lexer.py`):** Inserta la variable no declarada en el diccionario de tokens con tipo por defecto `'-'`.
* **Sintáctico/Semántico (`parser.py`):**
  * El usuario escribe una expresión, por ejemplo `a := 1`.
  * `p_variable_asignacion` llama a `verificar_variable_declarada(p, "a")`.
  * La función lee que el tipo registrado en `itoken` para `"a"` es `'-'`.
  * Lanza la excepción semántica:
    ```python
    raise Exception('Error: Variable "a" no declarada. Linea: X')
    ```
  * La compilación aborta de forma inmediata.

---

### Caso 27: Error Semántico: Redeclaración de una variable en bloque `init`
* **Sintáctico/Semántico (`parser.py`):**
  * El programador escribe en la cabecera:
    ```text
    init {
        x: Int
        x: Float
    }
    ```
  * Para la primera línea, `p_declaracion` cambia el tipo de `x` a `"Int"`.
  * Para la segunda línea, `p_declaracion` evalúa `itoken.get_tipo("x")`. Como su tipo actual ya no es `'-'` sino `"Int"`, detecta la redeclaración y lanza:
    ```python
    raise Exception('Error: Variable "x" ya declarada')
    ```

---

### Caso 28: Error Semántico: Asignación de tipos incompatibles (`x := s` siendo `Int` y `String`)
* **Sintáctico/Semántico (`parser.py`):**
  * `p_asignacion` obtiene el tipo de la variable destino (`Int`) y el tipo de la expresión derecha (`String`).
  * Al evaluar `tipo_a != tipo_b_normalized`, detecta la discrepancia.
  * Lanza la excepción semántica:
    ```python
    raise Exception('Error semántico: Asignación incompatible para "x". Esperado Int pero se obtuvo String.')
    ```

---

### Caso 29: Sanitización de constante numérica negativa (`-5` o `_-5`)
* **Léxico (`lexer.py`):** `t_N_ENTERO` captura el lexema `-5`. Crea el token `_-5` en la tabla de símbolos.
* **Código Objeto (`asm_generator.py`):**
  * En `build_data_section`, las constantes que comienzan con `_-` no son identificadores válidos en ensamblador.
  * El compilador limpia el nombre mediante una regla de reemplazo:
    ```python
    if name.startswith('_-'):
        safe_name = '_n' + name[2:].replace('.', '_')
    ```
  * En el código `.asm` generado, se escribe en `.DATA`:
    ```assembly
    _n5 dd -5
    ```
  * Toda referencia a la constante en el código objeto reemplaza `_-5` por la variable sanitizada `_n5`.

---

### Caso 30: Finalización segura del programa en Ensamblador
* **Código Objeto (`asm_generator.py`):**
  * Al terminar de recorrer y traducir todos los tercetos en `generate_asm`, el generador inserta la rutina de finalización limpia para el sistema operativo DOS:
    ```assembly
    mov ah, 4Ch
    int 21h
    END START
    ```
  * Esto asegura que el binario devuelva el control al sistema operativo una vez concluida su ejecución, previniendo cuelgues o bucles infinitos en el emulador (ej: DOSBox).

---

### Caso 31: Inicialización del Coprocesador Matemático (FPU x87)
* **Código Objeto (`asm_generator.py`):**
  * Al inicializarse el segmento `.CODE` de ensamblador en `generate_asm`, se genera la directiva de inicialización de la FPU:
    ```assembly
    finit
    ```
  * Esto limpia los registros del coprocesador (`ST(0)` a `ST(7)`) y configura los registros de estado por defecto para evitar arrastrar errores lógicos de redondeo de cómputos anteriores.

---

### Caso 32: Comparación de igualdad de flotantes (`a == b`)
* **Sintáctico/Semántico (`parser.py`):**
  * Detecta operador `COMP_IGUAL`. En `p_condicion_simple`, busca en `diccionarioComparadores` para `==` y recupera el código condicional invertido `"BNE"`.
  * Genera el terceto de comparación `[2] - (CMP, a, b)` y el salto condicional `[3] - (BNE, _, _)`.
* **Código Objeto (`asm_generator.py`):**
  * En `generate_asm`, al ver que `a` y `b` son `Float`, realiza la carga, comparación, y descarga de banderas usando `sahf`.
  * Mapea `"BNE"` a salto condicional sin signo usando la tabla `unsigned_map` donde `jne` (jump if not equal) se mantiene como `jne`:
    ```assembly
    fld dword ptr [a]
    fcomp dword ptr [b]
    fstsw ax
    sahf
    jne L_destino
    ```

---

### Caso 33: Comparación de desigualdad de flotantes (`a <> b`)
* **Sintáctico/Semántico (`parser.py`):**
  * Detecta `COMP_DISTINTO`. Mapea el código invertido en `diccionarioComparadores` para `<>` que es `"BEQ"`.
  * Genera el terceto `[3] - (BEQ, _, _)`.
* **Código Objeto (`asm_generator.py`):**
  * Evalúa el salto para flotantes:
    ```assembly
    fld dword ptr [a]
    fcomp dword ptr [b]
    fstsw ax
    sahf
    je L_destino         ; Salta si son iguales (BEQ)
    ```

---

### Caso 34: Doble negación lógica (`NOT NOT (x < y)`)
* **Sintáctico/Semántico (`parser.py`):**
  * La condición `x < y` produce `[2] - (CMP, x, y)` y `[3] - (BGE, _, _)`.
  * La primera reducción de `p_condicion_multiple` (`NOT condicion_simple`) invierte el salto en el índice `3` usando `diccionarioComparadoresNot` convirtiéndolo en `BLT`.
  * La segunda reducción de `NOT condicion_multiple` vuelve a evaluar el salto condicional en el índice `3` y aplica de nuevo el re-mapeo del comparador negado, convirtiéndolo nuevamente en `BGE`.
* **Código Intermedio:**
  ```text
  [2] - (CMP,x,y)
  [3] - (BGE,_,_)
  ```
  *(La doble negación se anula matemáticamente a nivel de saltos en el código intermedio).*

---

### Caso 35: Expresiones con paréntesis anidados (`(x + (y - z))`)
* **Sintáctico/Semántico (`parser.py`):**
  * La regla `p_elemento_expresion` (`elemento : A_PARENTESIS expresion C_PARENTESIS`) permite anidar expresiones libremente sin romper la gramática.
  * Reduce recursivamente la expresión interna `(y - z)` creando el terceto `[2] - (-, y, z)`.
  * Luego reduce la expresión externa `x + [2]` creando el terceto `[3] - (+, x, [2])`.
* **Código Intermedio:**
  ```text
  [0] - (y,_,_)
  [1] - (z,_,_)
  [2] - (-,[0],[1])
  [3] - (+,x,[2])
  ```

---

### Caso 36: Error Semántico: Módulo sobre números de punto flotante (`a MOD b` con reales)
* **Sintáctico/Semántico (`parser.py`):**
  * En la regla `p_modulo`, evalúa `es_tipo_numerico(p[1])` y `es_tipo_numerico(p[3])`. Ambos son flotantes (`Float`), por lo que pasa la validación numérica general.
  * Sin embargo, para `MOD` se exige que el tipo no sea `Float`. Al detectar que al menos uno es `Float`, se dispara la excepción semántica:
    ```python
    raise Exception('Error: Operación "MOD" incompatible entre Float y Float.')
    ```

---

### Caso 37: Error Semántico: División entera sobre números de punto flotante (`a DIV b` con reales)
* **Sintáctico/Semántico (`parser.py`):**
  * `p_division` comprueba los tipos de `a` y `b`.
  * Al detectar que el tipo de datos involucra `Float` (en lugar de ser estrictamente `Int`), lanza:
    ```python
    raise Exception('Error: Operación "DIV" incompatible entre Float y Float.')
    ```

---

### Caso 38: Backfilling diferido en bucles `while`
* **Sintáctico/Semántico (`parser.py`):**
  * En `p_ciclo_while`, tras compilar el cuerpo del ciclo, se genera un salto incondicional `BI` a la etiqueta inicial.
  * Luego, se recupera el índice de salida guardado en la pila (`indice_comienzo_ciclo_while.pop()`).
  * Mediante `terceto.modificar_terceto`, se sobrescribe el destino del salto condicional de salida de la condición para que apunte exactamente al índice del primer terceto que está **fuera** del ciclo.
* **Código Intermedio:**
  ```text
  [4] - (BGE,[10],_)  ; Salto modificado tras backfilling
  ...
  [9] - (BI,[0],_)    ; Salto incondicional de retorno
  ```

---

### Caso 39: Configuración y directivas de cabecera TASM
* **Código Objeto (`asm_generator.py`):**
  * Al iniciar la generación del archivo `.asm`, `generate_asm` escribe de manera fija las directivas de la arquitectura del procesador:
    ```assembly
    include macros2.asm
    include number.asm
    .MODEL LARGE
    .386
    .STACK 200h
    ```
  * Esto habilita las macros de entrada/salida y define un tamaño de pila estático de 512 bytes (`200h`).

---

### Caso 40: Inclusión de librerías de macros en ensamblador
* **Código Objeto (`asm_generator.py`):**
  * Las directivas `include macros2.asm` e `include number.asm` permiten que el compilador use macros predefinidas para visualización de registros y captura de datos (ej. `GetInteger`, `DisplayFloat`) sin tener que implementar rutinas complejas de parseo de E/S de caracteres en ensamblador puro.

---

### Caso 41: Lectura por teclado de variables de punto flotante (`read(a)` siendo `Float`)
* **Sintáctico/Semántico (`parser.py`):**
  * `p_entrada` genera el terceto de lectura `[0] - (READ, a, _)`.
* **Código Objeto (`asm_generator.py`):**
  * `generate_asm` detecta que el operando `a` está registrado como `Float` en la tabla de símbolos.
  * Genera el llamado a la macro de flotantes de la librería:
    ```assembly
    GetFloat a
    ```

---

### Caso 42: Escritura de variables de punto flotante (`write(a)` siendo `Float`)
* **Sintáctico/Semántico (`parser.py`):**
  * `p_salida` genera el terceto `[0] - (WRITE, a, _)`.
* **Código Objeto (`asm_generator.py`):**
  * `generate_asm` lee que `a` es `Float` en `symbols`.
  * Genera la macro indicando la cantidad de decimales a formatear (2):
    ```assembly
    DisplayFloat a, 2
    ```

---

### Caso 43: Copia de cadenas constantes a variables string (`s := "mensaje"`)
* **Sintáctico/Semántico (`parser.py`):**
  * `p_asignacion` crea el terceto `[1] - ("mensaje", _, _)` y el terceto de asignación `[2] - (:=, s, [1])`.
* **Código Objeto (`asm_generator.py`):**
  * Detecta que la fuente es un literal string constante (etiqueta `STR_0` que vale `"mensaje"`).
  * Realiza la copia por bucle carácter a carácter:
    ```assembly
    mov si, OFFSET STR_0
    mov di, OFFSET s
    cld
    copy_string_2:
    lodsb
    stosb
    cmp al, '$'
    jne copy_string_2
    ```

---

### Caso 44: Validación de longitud de nombres de variables en el lexer (> 20 caracteres)
* **Léxico (`lexer.py`):**
  * Al escanear un identificador con `t_VARIABLE`, se ejecuta la validación:
    ```python
    if len(t.value) > 20:
        raise Exception(f'ERROR: La variable "{t.value}" esta fuera de rango...')
    ```
  * Si la variable mide 21 o más caracteres, detiene inmediatamente el lexer lanzando una excepción.

---

### Caso 45: Validación de longitud de strings constantes en el lexer (> 50 caracteres)
* **Léxico (`lexer.py`):**
  * Al detectar una constante de texto mediante `t_CTE_STRING`, se verifica el largo del contenido sin las comillas:
    ```python
    if len(contenido) > 50:
        raise Exception(f'ERROR LÉXICO: String de {len(contenido)} caracteres supera...')
    ```
  * Si excede los 50 caracteres, la fase léxica aborta con un error específico.

---

### Caso 46: Validación de desbordamiento de constantes Float en el lexer
* **Léxico (`lexer.py`):**
  * En `t_N_FLOTANTE`, convierte el lexema a float de Python y valida los límites de simple precisión (32 bits):
    ```python
    if valor < -3.4e38 or valor > 3.4e38:
        raise Exception(f'ERROR: El número {valor} esta fuera de rango para un Float de 32 bits')
    ```
  * Detiene la compilación si la constante matemática excede estos límites físicos.

---

### Caso 47: Validación de desbordamiento de constantes enteros en el lexer
* **Léxico (`lexer.py`):**
  * En `t_N_ENTERO`, convierte a entero y valida el rango firmado de 16 bits:
    ```python
    if valor < -32768 or valor > 32767:
        raise Exception(f'ERROR: El número {valor} esta fuera de rango para un Int de 16 bits')
    ```
  * Previene la generación de números enteros fuera del rango estándar del lenguaje en tiempo de análisis léxico.

---

### Caso 48: Traducción en ensamblador de la división entera (`DIV`)
* **Código Objeto (`asm_generator.py`):**
  * Cuando se procesa el terceto de división entera (`DIV`), `generate_expression_code` escribe la lógica de registros:
    ```assembly
    mov eax, operando_izq
    cdq
    mov ebx, operando_der
    idiv ebx
    mov temporal_destino, eax
    ```
  * El cociente se recupera del registro acumulador `EAX`.

---

### Caso 49: Traducción en ensamblador del resto entero (`MOD`)
* **Código Objeto (`asm_generator.py`):**
  * Al traducir el operador de residuo `MOD`, genera las instrucciones de división, pero mueve el resultado del registro de residuo `EDX`:
    ```assembly
    mov eax, operando_izq
    cdq
    mov ebx, operando_der
    idiv ebx
    mov temporal_destino, edx
    ```

---

### Caso 50: Generación de saltos incondicionales `BI` en ensamblador
* **Código Objeto (`asm_generator.py`):**
  * Al encontrar el operador `BI` en la lista de tercetos, el generador toma la referencia del destino (ej: `[5]`), calcula la etiqueta `L5` y escribe:
    ```assembly
    jmp L5
    ```

---

### Caso 51: Limpieza e inicialización de variables auxiliares en el compilador
* **Sintáctico/Semántico (`parser.py`):**
  * Al finalizar la ejecución de `ejecutar_parser(path)`, el parser procesa la inserción en la tabla de símbolos de todas las variables auxiliares temporales creadas en bucles especiales (ej: `@aux1`, `@aux2`), asegurando que estén debidamente declaradas antes de persistir la tabla de símbolos final en `symbol-table.txt`.

---

### Caso 52: Variables que inician con guion bajo en el código fuente
* **Léxico (`lexer.py`):**
  * La expresión regular de variable `t_VARIABLE` es `r'[a-zA-Z](\w\|_)*'`. Exige obligatoriamente que comience con una letra.
  * Si el programador intenta declarar una variable como `_x`, el lexer no la emparejará como `VARIABLE` y fallará (o la detectará como un error de carácter no reconocido en `t_error`), ya que el guion bajo al inicio está reservado para la nomenclatura de constantes en la tabla de símbolos.

---

### Caso 53: Precedencia y asociatividad izquierda en multiplicación y división (`x * y / z`)
* **Sintáctico/Semántico (`parser.py`):**
  * Los operadores `MULTIPLICACION` y `DIVISION` comparten la misma precedencia y se declaran con asociatividad izquierda: `('left', 'MULTIPLICACION', 'DIVISION')`.
  * Ante la cadena `x * y / z`, se agrupa y reduce primero de izquierda a derecha: `(x * y)` genera `[2] - (*, x, y)`.
  * Luego se divide por `z`: `[3] - (/, [2], z)`.
* **Código Intermedio:**
  ```text
  [2] - (*,x,y)
  [3] - (/,[2],z)
  ```

---

### Caso 54: Error Semántico: Tipo incompatible en lista de expresiones de `while in`
* **Sintáctico/Semántico (`parser.py`):**
  * En la regla `p_expresiones_ciclo_while_especial`, el compilador itera sobre todos los tipos de datos registrados en la lista de expresiones (`tipos_expresiones_ciclo_while_especial`).
  * Si la variable de control es de tipo `Int`, pero la lista contiene una expresión evaluada como `Float`, la validación falla y arroja:
    ```python
    raise Exception('Error: Tipos de datos incompatibles "Int" - Float.')
    ```

---

### Caso 55: Error Semántico: Comparación simple incompatible (`x == s` con `Int` y `String`)
* **Sintáctico/Semántico (`parser.py`):**
  * En `p_condicion_simple`, evalúa los tipos del lado izquierdo (`Int`) y derecho (`String`).
  * Al no ser iguales, interrumpe el análisis semántico y lanza:
    ```python
    raise Exception('Error semántico: Comparación de distintos tipos de datos (Int y String) no permitida.')
    ```

---

### Caso 56: Asignación de literales numéricos negativos (`x := -15`)
* **Léxico (`lexer.py`):**
  * El lexer captura `-15` a través de la regla `t_N_ENTERO` (que permite opcionalmente un signo menos inicial en su expresión regular: `r'0|-?[1-9]\d*'`).
  * Registra el token constante como `_-15` en `itoken`.
* **Sintáctico/Semántico (`parser.py`):**
  * Crea los tercetos correspondientes mapeando la constante.
* **Código Objeto (`asm_generator.py`):**
  * Declara en `.DATA`: `_n15 dd -15`.
  * Escribe en `.CODE`:
    ```assembly
    mov eax, _n15
    mov x, eax
    ```

---

### Caso 57: Generación de múltiples variables temporales `tmp` consecutivas
* **Código Objeto (`asm_generator.py`):**
  * Al procesar expresiones aritméticas largas, cada operador intermedio crea un temporal basado en el índice de su terceto en `build_data_section`.
  * Para `a + b + c + d`, si las sumas se realizan en los tercetos `4` y `5`, el generador declara y escribe en `.DATA`:
    ```assembly
    tmp4 dd ?
    tmp5 dd ?
    ```
  * Esto asegura que no ocurran colisiones de memoria en los cálculos paralelos de sub-expresiones.

---

### Caso 58: Sincronización de banderas FPU en comparaciones condicionales
* **Código Objeto (`asm_generator.py`):**
  * La instrucción de ensamblador `sahf` es fundamental para el compilador. Sincroniza el registro de estado del procesador con el resultado de la FPU x87.
  * Sin ella, las instrucciones de salto condicional del CPU (como `jb`, `ja`) no sabrían qué valores flotantes se compararon y evaluarían condiciones con banderas obsoletas o incorrectas.

---

### Caso 59: Generación automática de etiquetas faltantes en ensamblador
* **Código Objeto (`asm_generator.py`):**
  * En `generate_asm`, recopila todos los destinos de salto de los tercetos (`jump_targets`).
  * Si un salto apunta a un índice fuera del rango de los tercetos definidos en el código intermedio (por ejemplo, el final lógico del programa), escribe dinámicamente estas etiquetas al final de la sección `.CODE` para evitar errores de referencia indefinida en TASM:
    ```assembly
    L25:
        mov ah, 4Ch
        int 21h
    ```

---

### Caso 60: Punto de entrada del programa en ensamblador y direccionamiento de segmentos
* **Código Objeto (`asm_generator.py`):**
  * El compilador inicializa los registros de segmento en el punto de entrada `START:` para asegurar que el sistema operativo apunte correctamente a los buffers de datos:
    ```assembly
    START:
        mov ax,@DATA
        mov ds,ax            ; Inicializa segmento de datos principal
        mov es,ax            ; Inicializa segmento extra (requerido para lodsb/stosb)
    ```
  * Esto garantiza que tanto la manipulación de variables como la copia y procesamiento de strings apunten al mismo segmento físico de memoria `@DATA`.
