include macros2.asm
include number.asm

.MODEL  LARGE
.386
.STACK 200h
.DATA
    a dd ?
    b dd ?
    c dd ?
    d dd ?
    e dd ?
    f dd ?
    g dd ?
    h dd ?
    i db 51 dup(?), "$"
    j db 51 dup(?), "$"
    k db 51 dup(?), "$"
    nombre db 51 dup(?), "$"
    _10 dd 10
    _3 dd 3
    _2 dd 2
    _5 dd 5
    _10_5 dd 10.5
    _3_2 dd 3.2
    _1_5 dd 1.5
    _2_0 dd 2.0
    _20 dd 20
    _0 dd 0
    _1 dd 1
    _30 dd 30
    _100 dd 100
    _200 dd 200
    @aux1 dd ?
    @aux2 dd ?
    @aux3 dd ?
    STR_0 db "1. Inicializando variables...", 13, 10,"$"
    STR_1 db "Hola","$"
    STR_2 db "Mundo","$"
    STR_3 db "2. Probando operaciones aritmeticas...", 13, 10,"$"
    STR_4 db "Suma (3 + 2): ","$"
    STR_5 db 13, 10,"$"
    STR_6 db "Resta (3 - 2): ","$"
    STR_7 db "Multiplicacion (3 * 2): ","$"
    STR_8 db "Division entera (3 div 2): ","$"
    STR_9 db "Modulo entero (3 mod 2): ","$"
    STR_10 db 13, 10, "3. Probando condicionales (If / Else)...", 13, 10,"$"
    STR_11 db "a es menor que b (Correcto)", 13, 10,"$"
    STR_12 db "a no es menor que b (Incorrecto)", 13, 10,"$"
    STR_13 db "a es mayor que b (Incorrecto)", 13, 10,"$"
    STR_14 db "a no es mayor que b (Correcto)", 13, 10,"$"
    STR_15 db 13, 10, "4. Probando bucles while simples...", 13, 10,"$"
    STR_16 db "Iteracion simple a: ","$"
    STR_17 db 13, 10, "5. Probando bucles while anidados...", 13, 10,"$"
    STR_18 db "Anidado a y b: ","$"
    STR_19 db " ","$"
    STR_20 db 13, 10, "6. Probando ciclos especiales...", 13, 10,"$"
    STR_21 db "Ciclo especial a: ","$"
    STR_22 db 13, 10, "7. Probando ciclos especiales anidados...", 13, 10,"$"
    STR_23 db "Especial anidado a y b: ","$"
    STR_24 db 13, 10, "8. Probando lecturas de teclado...", 13, 10,"$"
    STR_25 db "Ingrese un numero entero para la variable a: ","$"
    STR_26 db "El numero ingresado es: ","$"
    STR_27 db 13, 10, 13, 10,"$"
    STR_28 db "Pruebas completadas de manera exitosa!", 13, 10,"$"
    tmp35 dd ?
    tmp43 dd ?
    tmp51 dd ?
    tmp59 dd ?
    tmp67 dd ?
    tmp108 dd ?
    tmp136 dd ?
    tmp142 dd ?
    tmp180 dd ?
    tmp214 dd ?
    tmp243 dd ?

.CODE

START:
    mov ax,@DATA
    mov ds,ax
    mov es,ax

L0:
    mov dx, OFFSET STR_0
    mov ah, 9
    int 21h

L1:

L2:

L3:
    mov eax, _10
    mov a, eax

L4:

L5:

L6:
    mov eax, _3
    mov b, eax

L7:

L8:

L9:
    mov eax, _2
    mov c, eax

L10:

L11:

L12:
    mov eax, _5
    mov d, eax

L13:

L14:

L15:
    mov eax, _10_5
    mov e, eax

L16:

L17:

L18:
    mov eax, _3_2
    mov f, eax

L19:

L20:

L21:
    mov eax, _1_5
    mov g, eax

L22:

L23:

L24:
    mov eax, _2_0
    mov h, eax

L25:

L26:

L27:
    mov si, OFFSET STR_1
    mov di, OFFSET i
    cld
copy_string_27:
    lodsb
    stosb
    cmp al, '$'
    jne copy_string_27

L28:

L29:

L30:
    mov si, OFFSET STR_2
    mov di, OFFSET j
    cld
copy_string_30:
    lodsb
    stosb
    cmp al, '$'
    jne copy_string_30

L31:
    mov dx, OFFSET STR_3
    mov ah, 9
    int 21h

L32:

L33:

L34:

L35:
    mov eax, b
    add eax, c
    mov tmp35, eax

L36:
    mov eax, tmp35
    mov a, eax

L37:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L38:
    DisplayInteger a

L39:
    mov dx, OFFSET STR_5
    mov ah, 9
    int 21h

L40:

L41:

L42:

L43:
    mov eax, b
    sub eax, c
    mov tmp43, eax

L44:
    mov eax, tmp43
    mov a, eax

L45:
    mov dx, OFFSET STR_6
    mov ah, 9
    int 21h

L46:
    DisplayInteger a

L47:
    mov dx, OFFSET STR_5
    mov ah, 9
    int 21h

L48:

L49:

L50:

L51:
    mov eax, b
    imul eax, c
    mov tmp51, eax

L52:
    mov eax, tmp51
    mov a, eax

L53:
    mov dx, OFFSET STR_7
    mov ah, 9
    int 21h

L54:
    DisplayInteger a

L55:
    mov dx, OFFSET STR_5
    mov ah, 9
    int 21h

L56:

L57:

L58:

L59:
    mov eax, b
    cdq
    mov ebx, c
    idiv ebx
    mov tmp59, eax

L60:
    mov eax, tmp59
    mov a, eax

L61:
    mov dx, OFFSET STR_8
    mov ah, 9
    int 21h

L62:
    DisplayInteger a

L63:
    mov dx, OFFSET STR_5
    mov ah, 9
    int 21h

L64:

L65:

L66:

L67:
    mov eax, b
    cdq
    mov ebx, c
    idiv ebx
    mov tmp67, edx

L68:
    mov eax, tmp67
    mov a, eax

L69:
    mov dx, OFFSET STR_9
    mov ah, 9
    int 21h

L70:
    DisplayInteger a

L71:
    mov dx, OFFSET STR_5
    mov ah, 9
    int 21h

L72:
    mov dx, OFFSET STR_10
    mov ah, 9
    int 21h

L73:

L74:

L75:
    mov eax, _10
    mov a, eax

L76:

L77:

L78:
    mov eax, _20
    mov b, eax

L79:

L80:

L81:
    mov eax, a
    cmp eax, b

L82:
    jge L85

L83:
    mov dx, OFFSET STR_11
    mov ah, 9
    int 21h

L84:
    jmp L86

L85:
    mov dx, OFFSET STR_12
    mov ah, 9
    int 21h

L86:

L87:

L88:
    mov eax, a
    cmp eax, b

L89:
    jle L92

L90:
    mov dx, OFFSET STR_13
    mov ah, 9
    int 21h

L91:
    jmp L93

L92:
    mov dx, OFFSET STR_14
    mov ah, 9
    int 21h

L93:
    mov dx, OFFSET STR_15
    mov ah, 9
    int 21h

L94:

L95:

L96:
    mov eax, _3
    mov a, eax

L97:
L98:

L99:

L100:
    mov eax, a
    cmp eax, _0

L101:
    jle L111

L102:
    mov dx, OFFSET STR_16
    mov ah, 9
    int 21h

L103:
    DisplayInteger a

L104:
    mov dx, OFFSET STR_5
    mov ah, 9
    int 21h

L105:

L106:

L107:

L108:
    mov eax, a
    sub eax, _1
    mov tmp108, eax

L109:
    mov eax, tmp108
    mov a, eax

L110:
    jmp L97

L111:
    mov dx, OFFSET STR_17
    mov ah, 9
    int 21h

L112:

L113:

L114:
    mov eax, _2
    mov a, eax

L115:
L116:

L117:

L118:
    mov eax, a
    cmp eax, _0

L119:
    jle L145

L120:

L121:

L122:
    mov eax, _2
    mov b, eax

L123:
L124:

L125:

L126:
    mov eax, b
    cmp eax, _0

L127:
    jle L139

L128:
    mov dx, OFFSET STR_18
    mov ah, 9
    int 21h

L129:
    DisplayInteger a

L130:
    mov dx, OFFSET STR_19
    mov ah, 9
    int 21h

L131:
    DisplayInteger b

L132:
    mov dx, OFFSET STR_5
    mov ah, 9
    int 21h

L133:

L134:

L135:

L136:
    mov eax, b
    sub eax, _1
    mov tmp136, eax

L137:
    mov eax, tmp136
    mov b, eax

L138:
    jmp L123

L139:

L140:

L141:

L142:
    mov eax, a
    sub eax, _1
    mov tmp142, eax

L143:
    mov eax, tmp142
    mov a, eax

L144:
    jmp L115

L145:
    mov dx, OFFSET STR_20
    mov ah, 9
    int 21h

L146:

L147:

L148:

L149:

L150:

L151:
    mov eax, _0
    mov @aux1, eax

L152:
L153:

L154:

L155:
    mov eax, @aux1
    cmp eax, _3

L156:
    jge L187

L157:

L158:

L159:
    mov eax, _0
    cmp eax, @aux1

L160:

L161:

L162:

L163:
    mov eax, _1
    cmp eax, @aux1

L164:

L165:

L166:

L167:
    mov eax, _2
    cmp eax, @aux1

L168:

L169:

L170:
    mov eax, _10
    mov a, eax

L171:
    jmp L178

L172:

L173:
    mov eax, _20
    mov a, eax

L174:
    jmp L178

L175:

L176:
    mov eax, _30
    mov a, eax

L177:
    jmp L178

L178:

L179:

L180:
    mov eax, @aux1
    add eax, _1
    mov tmp180, eax

L181:

L182:
    mov eax, tmp180
    mov @aux1, eax

L183:
    mov dx, OFFSET STR_21
    mov ah, 9
    int 21h

L184:
    DisplayInteger a

L185:
    mov dx, OFFSET STR_5
    mov ah, 9
    int 21h

L186:
    jmp L152

L187:
    mov dx, OFFSET STR_22
    mov ah, 9
    int 21h

L188:

L189:

L190:

L191:

L192:
    mov eax, _0
    mov @aux2, eax

L193:
L194:

L195:

L196:
    mov eax, @aux2
    cmp eax, _2

L197:
    jge L253

L198:

L199:

L200:
    mov eax, _0
    cmp eax, @aux2

L201:

L202:

L203:

L204:
    mov eax, _1
    cmp eax, @aux2

L205:

L206:

L207:
    mov eax, _1
    mov a, eax

L208:
    jmp L212

L209:

L210:
    mov eax, _2
    mov a, eax

L211:
    jmp L212

L212:

L213:

L214:
    mov eax, @aux2
    add eax, _1
    mov tmp214, eax

L215:

L216:
    mov eax, tmp214
    mov @aux2, eax

L217:

L218:

L219:

L220:

L221:
    mov eax, _0
    mov @aux3, eax

L222:
L223:

L224:

L225:
    mov eax, @aux3
    cmp eax, _2

L226:
    jge L252

L227:

L228:

L229:
    mov eax, _0
    cmp eax, @aux3

L230:

L231:

L232:

L233:
    mov eax, _1
    cmp eax, @aux3

L234:

L235:

L236:
    mov eax, _100
    mov b, eax

L237:
    jmp L241

L238:

L239:
    mov eax, _200
    mov b, eax

L240:
    jmp L241

L241:

L242:

L243:
    mov eax, @aux3
    add eax, _1
    mov tmp243, eax

L244:

L245:
    mov eax, tmp243
    mov @aux3, eax

L246:
    mov dx, OFFSET STR_23
    mov ah, 9
    int 21h

L247:
    DisplayInteger a

L248:
    mov dx, OFFSET STR_19
    mov ah, 9
    int 21h

L249:
    DisplayInteger b

L250:
    mov dx, OFFSET STR_5
    mov ah, 9
    int 21h

L251:
    jmp L222

L252:
    jmp L193

L253:
    mov dx, OFFSET STR_24
    mov ah, 9
    int 21h

L254:
    mov dx, OFFSET STR_25
    mov ah, 9
    int 21h

L255:
    GetInteger a

L256:
    mov dx, OFFSET STR_26
    mov ah, 9
    int 21h

L257:
    DisplayInteger a

L258:
    mov dx, OFFSET STR_27
    mov ah, 9
    int 21h

L259:
    mov dx, OFFSET STR_28
    mov ah, 9
    int 21h

    mov ah, 4Ch
    int 21h
END START