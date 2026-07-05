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
    _100 dd 100
    _20 dd 20
    _0 dd 0
    _4 dd 4
    _1 dd 1
    _30 dd 30
    _200 dd 200
    @aux1 dd ?
    @aux2 dd ?
    @aux3 dd ?
    STR_0 db "1. Inicializando variables...", 13, 10,"$"
    STR_1 db "Hola","$"
    STR_2 db "Mundo","$"
    STR_3 db "a inicial: ","$"
    STR_4 db 13, 10,"$"
    STR_5 db "b inicial: ","$"
    STR_6 db "c inicial: ","$"
    STR_7 db "d inicial: ","$"
    STR_8 db 13, 10, "Probando asignaciones de tipos distintos...", 13, 10,"$"
    STR_9 db "Asignacion Int := Float (a := e):", 13, 10,"$"
    STR_10 db "Valor en a: ","$"
    STR_11 db "Asignacion Int := Float literal (a := 1.5):", 13, 10,"$"
    STR_12 db "Asignacion Float := Int literal (e := 100):", 13, 10,"$"
    STR_13 db "Presione Enter para continuar...", 13, 10,"$"
    STR_14 db 13, 10, "2. Probando operaciones aritmeticas...", 13, 10,"$"
    STR_15 db "Variables a usar -> b: ","$"
    STR_16 db ", c: ","$"
    STR_17 db "Suma (b + c): ","$"
    STR_18 db "Resta (b - c): ","$"
    STR_19 db "Multiplicacion (b * c): ","$"
    STR_20 db "Division entera (b div c): ","$"
    STR_21 db "Modulo entero (b mod c): ","$"
    STR_22 db 13, 10, "3. Probando condicionales (If/Else, AND/OR)...", 13, 10,"$"
    STR_23 db "Variables a usar -> a: ","$"
    STR_24 db ", b: ","$"
    STR_25 db "a es menor que b (Correcto)", 13, 10,"$"
    STR_26 db "a no es menor que b (Incorrecto)", 13, 10,"$"
    STR_27 db "Comparacion Int > Float: a es mayor que e", 13, 10,"$"
    STR_28 db "Comparacion Int > Float: a no es mayor que e", 13, 10,"$"
    STR_29 db "AND funciona: ambos son mayores a 0 (Correcto)", 13, 10,"$"
    STR_30 db "OR funciona: al menos uno mayor a 0 (Correcto)", 13, 10,"$"
    STR_31 db 13, 10, "4. Probando IFs anidados...", 13, 10,"$"
    STR_32 db "Ambos a y b son mayores a 0 (Correcto)", 13, 10,"$"
    STR_33 db "a es mayor a 0, pero b no (Incorrecto)", 13, 10,"$"
    STR_34 db "a no es mayor a 0 (Incorrecto)", 13, 10,"$"
    STR_35 db 13, 10, "5. Probando IF dentro de WHILE...", 13, 10,"$"
    STR_36 db "Variable a usar -> a: ","$"
    STR_37 db "Iteracion a: ","$"
    STR_38 db "a es par (Correcto)", 13, 10,"$"
    STR_39 db "a es impar (Correcto)", 13, 10,"$"
    STR_40 db 13, 10, "6. Probando bucles while anidados...", 13, 10,"$"
    STR_41 db "Anidado a: ","$"
    STR_42 db 13, 10, "7. Probando ciclos especiales...", 13, 10,"$"
    STR_43 db "Lista a usar: [10, 20, 30]", 13, 10,"$"
    STR_44 db "Ciclo especial a: ","$"
    STR_45 db 13, 10, "8. Probando ciclos especiales anidados...", 13, 10,"$"
    STR_46 db "Listas: a in [1, 2], b in [100, 200]", 13, 10,"$"
    STR_47 db "Especial anidado a: ","$"
    STR_48 db 13, 10, "9. Probando lecturas de teclado...", 13, 10,"$"
    STR_49 db "Ingrese un numero entero para la variable a: ","$"
    STR_50 db "El numero ingresado es: ","$"
    STR_51 db 13, 10, 13, 10,"$"
    STR_52 db "Pruebas completadas de manera exitosa!", 13, 10,"$"
    tmp79 dd ?
    tmp87 dd ?
    tmp95 dd ?
    tmp103 dd ?
    tmp111 dd ?
    tmp208 dd ?
    tmp218 dd ?
    tmp248 dd ?
    tmp254 dd ?
    tmp295 dd ?
    tmp332 dd ?
    tmp361 dd ?

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
    DisplayInteger a

L33:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L34:
    mov dx, OFFSET STR_5
    mov ah, 9
    int 21h

L35:
    DisplayInteger b

L36:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L37:
    mov dx, OFFSET STR_6
    mov ah, 9
    int 21h

L38:
    DisplayInteger c

L39:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L40:
    mov dx, OFFSET STR_7
    mov ah, 9
    int 21h

L41:
    DisplayInteger d

L42:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L43:
    mov dx, OFFSET STR_8
    mov ah, 9
    int 21h

L44:

L45:

L46:
    mov eax, e
    mov a, eax

L47:
    mov dx, OFFSET STR_9
    mov ah, 9
    int 21h

L48:
    mov dx, OFFSET STR_10
    mov ah, 9
    int 21h

L49:
    DisplayInteger a

L50:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L51:

L52:

L53:
    mov eax, _10
    mov a, eax

L54:

L55:

L56:
    mov eax, _1_5
    mov a, eax

L57:
    mov dx, OFFSET STR_11
    mov ah, 9
    int 21h

L58:
    mov dx, OFFSET STR_10
    mov ah, 9
    int 21h

L59:
    DisplayInteger a

L60:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L61:

L62:

L63:
    mov eax, _10
    mov a, eax

L64:

L65:

L66:
    mov eax, _100
    mov e, eax

L67:
    mov dx, OFFSET STR_12
    mov ah, 9
    int 21h

L68:
    mov dx, OFFSET STR_13
    mov ah, 9
    int 21h

L69:
    GetInteger d

L70:
    mov dx, OFFSET STR_14
    mov ah, 9
    int 21h

L71:
    mov dx, OFFSET STR_15
    mov ah, 9
    int 21h

L72:
    DisplayInteger b

L73:
    mov dx, OFFSET STR_16
    mov ah, 9
    int 21h

L74:
    DisplayInteger c

L75:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L76:

L77:

L78:

L79:
    mov eax, b
    add eax, c
    mov tmp79, eax

L80:
    mov eax, tmp79
    mov a, eax

L81:
    mov dx, OFFSET STR_17
    mov ah, 9
    int 21h

L82:
    DisplayInteger a

L83:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L84:

L85:

L86:

L87:
    mov eax, b
    sub eax, c
    mov tmp87, eax

L88:
    mov eax, tmp87
    mov a, eax

L89:
    mov dx, OFFSET STR_18
    mov ah, 9
    int 21h

L90:
    DisplayInteger a

L91:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L92:

L93:

L94:

L95:
    mov eax, b
    imul eax, c
    mov tmp95, eax

L96:
    mov eax, tmp95
    mov a, eax

L97:
    mov dx, OFFSET STR_19
    mov ah, 9
    int 21h

L98:
    DisplayInteger a

L99:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L100:

L101:

L102:

L103:
    mov eax, b
    cdq
    mov ebx, c
    idiv ebx
    mov tmp103, eax

L104:
    mov eax, tmp103
    mov a, eax

L105:
    mov dx, OFFSET STR_20
    mov ah, 9
    int 21h

L106:
    DisplayInteger a

L107:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L108:

L109:

L110:

L111:
    mov eax, b
    cdq
    mov ebx, c
    idiv ebx
    mov tmp111, edx

L112:
    mov eax, tmp111
    mov a, eax

L113:
    mov dx, OFFSET STR_21
    mov ah, 9
    int 21h

L114:
    DisplayInteger a

L115:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L116:
    mov dx, OFFSET STR_13
    mov ah, 9
    int 21h

L117:
    GetInteger d

L118:
    mov dx, OFFSET STR_22
    mov ah, 9
    int 21h

L119:

L120:

L121:
    mov eax, _10
    mov a, eax

L122:

L123:

L124:
    mov eax, _20
    mov b, eax

L125:
    mov dx, OFFSET STR_23
    mov ah, 9
    int 21h

L126:
    DisplayInteger a

L127:
    mov dx, OFFSET STR_24
    mov ah, 9
    int 21h

L128:
    DisplayInteger b

L129:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L130:

L131:

L132:
    mov eax, a
    cmp eax, b

L133:
    jge L136

L134:
    mov dx, OFFSET STR_25
    mov ah, 9
    int 21h

L135:
    jmp L137

L136:
    mov dx, OFFSET STR_26
    mov ah, 9
    int 21h

L137:

L138:

L139:
    mov eax, a
    cmp eax, e

L140:
    jle L143

L141:
    mov dx, OFFSET STR_27
    mov ah, 9
    int 21h

L142:
    jmp L144

L143:
    mov dx, OFFSET STR_28
    mov ah, 9
    int 21h

L144:

L145:

L146:
    mov eax, a
    cmp eax, _0

L147:
    jle L153

L148:

L149:

L150:
    mov eax, b
    cmp eax, _0

L151:
    jle L153

L152:
    mov dx, OFFSET STR_29
    mov ah, 9
    int 21h

L153:

L154:

L155:
    mov eax, a
    cmp eax, _100

L156:
    jg L161

L157:

L158:

L159:
    mov eax, b
    cmp eax, _0

L160:
    jle L162

L161:
    mov dx, OFFSET STR_30
    mov ah, 9
    int 21h

L162:
    mov dx, OFFSET STR_13
    mov ah, 9
    int 21h

L163:
    GetInteger d

L164:
    mov dx, OFFSET STR_31
    mov ah, 9
    int 21h

L165:

L166:

L167:
    mov eax, _5
    mov a, eax

L168:

L169:

L170:
    mov eax, _3
    mov b, eax

L171:
    mov dx, OFFSET STR_23
    mov ah, 9
    int 21h

L172:
    DisplayInteger a

L173:
    mov dx, OFFSET STR_24
    mov ah, 9
    int 21h

L174:
    DisplayInteger b

L175:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L176:

L177:

L178:
    mov eax, a
    cmp eax, _0

L179:
    jle L188

L180:

L181:

L182:
    mov eax, b
    cmp eax, _0

L183:
    jle L186

L184:
    mov dx, OFFSET STR_32
    mov ah, 9
    int 21h

L185:
    jmp L187

L186:
    mov dx, OFFSET STR_33
    mov ah, 9
    int 21h

L187:
    jmp L189

L188:
    mov dx, OFFSET STR_34
    mov ah, 9
    int 21h

L189:
    mov dx, OFFSET STR_13
    mov ah, 9
    int 21h

L190:
    GetInteger d

L191:
    mov dx, OFFSET STR_35
    mov ah, 9
    int 21h

L192:

L193:

L194:
    mov eax, _4
    mov a, eax

L195:
    mov dx, OFFSET STR_36
    mov ah, 9
    int 21h

L196:
    DisplayInteger a

L197:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L198:
L199:

L200:

L201:
    mov eax, a
    cmp eax, _0

L202:
    jle L221

L203:
    mov dx, OFFSET STR_37
    mov ah, 9
    int 21h

L204:
    DisplayInteger a

L205:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L206:

L207:

L208:
    mov eax, a
    cdq
    mov ebx, _2
    idiv ebx
    mov tmp208, edx

L209:

L210:
    mov eax, tmp208
    cmp eax, _0

L211:
    jne L214

L212:
    mov dx, OFFSET STR_38
    mov ah, 9
    int 21h

L213:
    jmp L215

L214:
    mov dx, OFFSET STR_39
    mov ah, 9
    int 21h

L215:

L216:

L217:

L218:
    mov eax, a
    sub eax, _1
    mov tmp218, eax

L219:
    mov eax, tmp218
    mov a, eax

L220:
    jmp L198

L221:
    mov dx, OFFSET STR_13
    mov ah, 9
    int 21h

L222:
    GetInteger d

L223:
    mov dx, OFFSET STR_40
    mov ah, 9
    int 21h

L224:

L225:

L226:
    mov eax, _2
    mov a, eax

L227:
L228:

L229:

L230:
    mov eax, a
    cmp eax, _0

L231:
    jle L257

L232:

L233:

L234:
    mov eax, _2
    mov b, eax

L235:
L236:

L237:

L238:
    mov eax, b
    cmp eax, _0

L239:
    jle L251

L240:
    mov dx, OFFSET STR_41
    mov ah, 9
    int 21h

L241:
    DisplayInteger a

L242:
    mov dx, OFFSET STR_24
    mov ah, 9
    int 21h

L243:
    DisplayInteger b

L244:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L245:

L246:

L247:

L248:
    mov eax, b
    sub eax, _1
    mov tmp248, eax

L249:
    mov eax, tmp248
    mov b, eax

L250:
    jmp L235

L251:

L252:

L253:

L254:
    mov eax, a
    sub eax, _1
    mov tmp254, eax

L255:
    mov eax, tmp254
    mov a, eax

L256:
    jmp L227

L257:
    mov dx, OFFSET STR_13
    mov ah, 9
    int 21h

L258:
    GetInteger d

L259:
    mov dx, OFFSET STR_42
    mov ah, 9
    int 21h

L260:
    mov dx, OFFSET STR_43
    mov ah, 9
    int 21h

L261:

L262:

L263:

L264:

L265:

L266:
    mov eax, _0
    mov @aux1, eax

L267:
L268:

L269:

L270:
    mov eax, @aux1
    cmp eax, _3

L271:
    jge L302

L272:

L273:

L274:
    mov eax, _0
    cmp eax, @aux1

L275:
    je L284

L276:

L277:

L278:
    mov eax, _1
    cmp eax, @aux1

L279:
    je L287

L280:

L281:

L282:
    mov eax, _2
    cmp eax, @aux1

L283:
    je L290

L284:

L285:
    mov eax, _10
    mov a, eax

L286:
    jmp L293

L287:

L288:
    mov eax, _20
    mov a, eax

L289:
    jmp L293

L290:

L291:
    mov eax, _30
    mov a, eax

L292:
    jmp L293

L293:

L294:

L295:
    mov eax, @aux1
    add eax, _1
    mov tmp295, eax

L296:

L297:
    mov eax, tmp295
    mov @aux1, eax

L298:
    mov dx, OFFSET STR_44
    mov ah, 9
    int 21h

L299:
    DisplayInteger a

L300:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L301:
    jmp L267

L302:
    mov dx, OFFSET STR_13
    mov ah, 9
    int 21h

L303:
    GetInteger d

L304:
    mov dx, OFFSET STR_45
    mov ah, 9
    int 21h

L305:
    mov dx, OFFSET STR_46
    mov ah, 9
    int 21h

L306:

L307:

L308:

L309:

L310:
    mov eax, _0
    mov @aux2, eax

L311:
L312:

L313:

L314:
    mov eax, @aux2
    cmp eax, _2

L315:
    jge L371

L316:

L317:

L318:
    mov eax, _0
    cmp eax, @aux2

L319:
    je L324

L320:

L321:

L322:
    mov eax, _1
    cmp eax, @aux2

L323:
    je L327

L324:

L325:
    mov eax, _1
    mov a, eax

L326:
    jmp L330

L327:

L328:
    mov eax, _2
    mov a, eax

L329:
    jmp L330

L330:

L331:

L332:
    mov eax, @aux2
    add eax, _1
    mov tmp332, eax

L333:

L334:
    mov eax, tmp332
    mov @aux2, eax

L335:

L336:

L337:

L338:

L339:
    mov eax, _0
    mov @aux3, eax

L340:
L341:

L342:

L343:
    mov eax, @aux3
    cmp eax, _2

L344:
    jge L370

L345:

L346:

L347:
    mov eax, _0
    cmp eax, @aux3

L348:
    je L353

L349:

L350:

L351:
    mov eax, _1
    cmp eax, @aux3

L352:
    je L356

L353:

L354:
    mov eax, _100
    mov b, eax

L355:
    jmp L359

L356:

L357:
    mov eax, _200
    mov b, eax

L358:
    jmp L359

L359:

L360:

L361:
    mov eax, @aux3
    add eax, _1
    mov tmp361, eax

L362:

L363:
    mov eax, tmp361
    mov @aux3, eax

L364:
    mov dx, OFFSET STR_47
    mov ah, 9
    int 21h

L365:
    DisplayInteger a

L366:
    mov dx, OFFSET STR_24
    mov ah, 9
    int 21h

L367:
    DisplayInteger b

L368:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L369:
    jmp L340

L370:
    jmp L311

L371:
    mov dx, OFFSET STR_13
    mov ah, 9
    int 21h

L372:
    GetInteger d

L373:
    mov dx, OFFSET STR_48
    mov ah, 9
    int 21h

L374:
    mov dx, OFFSET STR_49
    mov ah, 9
    int 21h

L375:
    GetInteger a

L376:
    mov dx, OFFSET STR_50
    mov ah, 9
    int 21h

L377:
    DisplayInteger a

L378:
    mov dx, OFFSET STR_51
    mov ah, 9
    int 21h

L379:
    mov dx, OFFSET STR_52
    mov ah, 9
    int 21h

    mov ah, 4Ch
    int 21h
END START