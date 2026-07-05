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
    pausa dd ?
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
    _n2 dd -2
    _5 dd 5
    _10_5 dd 10.5
    _3_2 dd 3.2
    _1_5 dd 1.5
    _2_0 dd 2.0
    _2 dd 2
    _20 dd 20
    _0 dd 0
    _100 dd 100
    _0_0 dd 0.0
    _4 dd 4
    _1 dd 1
    _8_0 dd 8.0
    _9_0 dd 9.0
    _1_0 dd 1.0
    _7_0 dd 7.0
    _5_0 dd 5.0
    _30 dd 30
    _20_5 dd 20.5
    _30_5 dd 30.5
    _200 dd 200
    _2_5 dd 2.5
    _100_5 dd 100.5
    _200_5 dd 200.5
    @aux1 dd ?
    @aux2 dd ?
    @aux3 dd ?
    @aux4 dd ?
    @aux5 dd ?
    @aux6 dd ?
    STR_0 db "1. Inicializando variables...", 13, 10,"$"
    STR_1 db "Hola","$"
    STR_2 db "Mundo","$"
    STR_3 db "a inicial: ","$"
    STR_4 db 13, 10,"$"
    STR_5 db "b inicial: ","$"
    STR_6 db "c inicial: ","$"
    STR_7 db "d inicial: ","$"
    STR_8 db "e inicial: ","$"
    STR_9 db "f inicial: ","$"
    STR_10 db 13, 10, "Probando asignaciones de tipos distintos...", 13, 10,"$"
    STR_11 db "Presione Enter para continuar...", 13, 10,"$"
    STR_12 db 13, 10, "2. Probando operaciones aritmeticas...", 13, 10,"$"
    STR_13 db "Variables a usar -> b: ","$"
    STR_14 db ", c: ","$"
    STR_15 db ", d: ","$"
    STR_16 db "b * c + d (deberia ser -1): ","$"
    STR_17 db "b * (c + d) (deberia ser 9): ","$"
    STR_18 db "(b + c) * d - a (deberia ser -4): ","$"
    STR_19 db "(d * (b + c)) div 2 (deberia ser 2): ","$"
    STR_20 db "b mod c (deberia ser 1): ","$"
    STR_21 db "Variables a usar -> e: ","$"
    STR_22 db ", f: ","$"
    STR_23 db ", g: ","$"
    STR_24 db "e + f * g (deberia ser 15.30): ","$"
    STR_25 db 13, 10, "3. Probando condicionales (If/Else, AND/OR)...", 13, 10,"$"
    STR_26 db "Variables a usar -> a: ","$"
    STR_27 db ", b: ","$"
    STR_28 db "a es menor que b (Correcto)", 13, 10,"$"
    STR_29 db "a no es menor que b (Incorrecto)", 13, 10,"$"
    STR_30 db "Float e es mayor que f (Correcto)", 13, 10,"$"
    STR_31 db "Float e no es mayor que f (Incorrecto)", 13, 10,"$"
    STR_32 db "AND funciona: ambos son mayores a 0 (Correcto)", 13, 10,"$"
    STR_33 db "OR funciona: al menos uno mayor a 0 (Correcto)", 13, 10,"$"
    STR_34 db 13, 10, "4. Probando IFs anidados...", 13, 10,"$"
    STR_35 db "Ambos a y b son mayores a 0 (Correcto)", 13, 10,"$"
    STR_36 db "a es mayor a 0, pero b no (Incorrecto)", 13, 10,"$"
    STR_37 db "a no es mayor a 0 (Incorrecto)", 13, 10,"$"
    STR_38 db "Floats e y f mayores a 0.0 (Correcto)", 13, 10,"$"
    STR_39 db 13, 10, "5. Probando IF dentro de WHILE...", 13, 10,"$"
    STR_40 db "Variable a usar -> a: ","$"
    STR_41 db "Iteracion a: ","$"
    STR_42 db "a es par (Correcto)", 13, 10,"$"
    STR_43 db "a es impar (Correcto)", 13, 10,"$"
    STR_44 db "Ejecutando bucle while con float...", 13, 10,"$"
    STR_45 db "e actual: ","$"
    STR_46 db "e es mayor que 9.0 (Correcto)", 13, 10,"$"
    STR_47 db 13, 10, "6. Probando bucles while anidados...", 13, 10,"$"
    STR_48 db "Anidado a: ","$"
    STR_49 db "Bucles anidados con float...", 13, 10,"$"
    STR_50 db "Float anidado e: ","$"
    STR_51 db 13, 10, "7. Probando ciclos especiales...", 13, 10,"$"
    STR_52 db "Lista a usar: [10, 20, 30]", 13, 10,"$"
    STR_53 db "Ciclo especial a: ","$"
    STR_54 db "Ciclo especial Float in [10.5, 20.5, 30.5]:", 13, 10,"$"
    STR_55 db "Especial Float e: ","$"
    STR_56 db 13, 10, "8. Probando ciclos especiales anidados...", 13, 10,"$"
    STR_57 db "Listas: a in [1, 2], b in [100, 200]", 13, 10,"$"
    STR_58 db "Especial anidado a: ","$"
    STR_59 db "Ciclos Float especiales anidados...", 13, 10,"$"
    STR_60 db "Float especial e: ","$"
    STR_61 db 13, 10, "9. Probando lecturas de teclado...", 13, 10,"$"
    STR_62 db "Ingrese un numero entero para la variable a: ","$"
    STR_63 db "El numero ingresado es: ","$"
    STR_64 db 13, 10, 13, 10,"$"
    STR_65 db "Pruebas completadas de manera exitosa!", 13, 10,"$"
    tmp63 dd ?
    tmp65 dd ?
    tmp74 dd ?
    tmp75 dd ?
    tmp83 dd ?
    tmp85 dd ?
    tmp87 dd ?
    tmp96 dd ?
    tmp97 dd ?
    tmp99 dd ?
    tmp107 dd ?
    tmp123 dd ?
    tmp124 dd ?
    tmp230 dd ?
    tmp240 dd ?
    tmp260 dd ?
    tmp293 dd ?
    tmp299 dd ?
    tmp327 dd ?
    tmp333 dd ?
    tmp380 dd ?
    tmp422 dd ?
    tmp462 dd ?
    tmp491 dd ?
    tmp528 dd ?
    tmp557 dd ?

.CODE

START:
    mov ax,@DATA
    mov ds,ax
    mov es,ax
    finit

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
    mov eax, _n2
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
    DisplayFloat e, 2

L45:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L46:
    mov dx, OFFSET STR_9
    mov ah, 9
    int 21h

L47:
    DisplayFloat f, 2

L48:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L49:
    mov dx, OFFSET STR_10
    mov ah, 9
    int 21h

L50:
    mov dx, OFFSET STR_11
    mov ah, 9
    int 21h

L51:
    GetInteger pausa

L52:
    mov dx, OFFSET STR_12
    mov ah, 9
    int 21h

L53:
    mov dx, OFFSET STR_13
    mov ah, 9
    int 21h

L54:
    DisplayInteger b

L55:
    mov dx, OFFSET STR_14
    mov ah, 9
    int 21h

L56:
    DisplayInteger c

L57:
    mov dx, OFFSET STR_15
    mov ah, 9
    int 21h

L58:
    DisplayInteger d

L59:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L60:

L61:

L62:

L63:
    mov eax, b
    imul eax, c
    mov tmp63, eax

L64:

L65:
    mov eax, tmp63
    add eax, d
    mov tmp65, eax

L66:
    mov eax, tmp65
    mov a, eax

L67:
    mov dx, OFFSET STR_16
    mov ah, 9
    int 21h

L68:
    DisplayInteger a

L69:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L70:

L71:

L72:

L73:

L74:
    mov eax, c
    add eax, d
    mov tmp74, eax

L75:
    mov eax, b
    imul eax, tmp74
    mov tmp75, eax

L76:
    mov eax, tmp75
    mov a, eax

L77:
    mov dx, OFFSET STR_17
    mov ah, 9
    int 21h

L78:
    DisplayInteger a

L79:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L80:

L81:

L82:

L83:
    mov eax, b
    add eax, c
    mov tmp83, eax

L84:

L85:
    mov eax, tmp83
    imul eax, d
    mov tmp85, eax

L86:

L87:
    mov eax, tmp85
    sub eax, a
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

L96:
    mov eax, b
    add eax, c
    mov tmp96, eax

L97:
    mov eax, d
    imul eax, tmp96
    mov tmp97, eax

L98:

L99:
    mov eax, tmp97
    cdq
    mov ebx, _2
    idiv ebx
    mov tmp99, eax

L100:
    mov eax, tmp99
    mov a, eax

L101:
    mov dx, OFFSET STR_19
    mov ah, 9
    int 21h

L102:
    DisplayInteger a

L103:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L104:

L105:

L106:

L107:
    mov eax, b
    cdq
    mov ebx, c
    idiv ebx
    mov tmp107, edx

L108:
    mov eax, tmp107
    mov a, eax

L109:
    mov dx, OFFSET STR_20
    mov ah, 9
    int 21h

L110:
    DisplayInteger a

L111:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L112:
    mov dx, OFFSET STR_21
    mov ah, 9
    int 21h

L113:
    DisplayFloat e, 2

L114:
    mov dx, OFFSET STR_22
    mov ah, 9
    int 21h

L115:
    DisplayFloat f, 2

L116:
    mov dx, OFFSET STR_23
    mov ah, 9
    int 21h

L117:
    DisplayFloat g, 2

L118:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L119:

L120:

L121:

L122:

L123:
    fld dword ptr [f]
    fmul dword ptr [g]
    fstp dword ptr [tmp123]

L124:
    fld dword ptr [e]
    fadd dword ptr [tmp123]
    fstp dword ptr [tmp124]

L125:
    mov eax, tmp124
    mov h, eax

L126:
    mov dx, OFFSET STR_24
    mov ah, 9
    int 21h

L127:
    DisplayFloat h, 2

L128:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L129:
    mov dx, OFFSET STR_11
    mov ah, 9
    int 21h

L130:
    GetInteger pausa

L131:
    mov dx, OFFSET STR_25
    mov ah, 9
    int 21h

L132:

L133:

L134:
    mov eax, _10
    mov a, eax

L135:

L136:

L137:
    mov eax, _20
    mov b, eax

L138:
    mov dx, OFFSET STR_26
    mov ah, 9
    int 21h

L139:
    DisplayInteger a

L140:
    mov dx, OFFSET STR_27
    mov ah, 9
    int 21h

L141:
    DisplayInteger b

L142:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L143:

L144:

L145:
    mov eax, a
    cmp eax, b

L146:
    jge L149

L147:
    mov dx, OFFSET STR_28
    mov ah, 9
    int 21h

L148:
    jmp L150

L149:
    mov dx, OFFSET STR_29
    mov ah, 9
    int 21h

L150:

L151:

L152:
    fld dword ptr [e]
    fcomp dword ptr [f]
    fstsw ax
    sahf

L153:
    jbe L156

L154:
    mov dx, OFFSET STR_30
    mov ah, 9
    int 21h

L155:
    jmp L157

L156:
    mov dx, OFFSET STR_31
    mov ah, 9
    int 21h

L157:

L158:

L159:
    mov eax, a
    cmp eax, _0

L160:
    jle L166

L161:

L162:

L163:
    mov eax, b
    cmp eax, _0

L164:
    jle L166

L165:
    mov dx, OFFSET STR_32
    mov ah, 9
    int 21h

L166:

L167:

L168:
    mov eax, a
    cmp eax, _100

L169:
    jg L174

L170:

L171:

L172:
    mov eax, b
    cmp eax, _0

L173:
    jle L175

L174:
    mov dx, OFFSET STR_33
    mov ah, 9
    int 21h

L175:
    mov dx, OFFSET STR_11
    mov ah, 9
    int 21h

L176:
    GetInteger pausa

L177:
    mov dx, OFFSET STR_34
    mov ah, 9
    int 21h

L178:

L179:

L180:
    mov eax, _5
    mov a, eax

L181:

L182:

L183:
    mov eax, _3
    mov b, eax

L184:
    mov dx, OFFSET STR_26
    mov ah, 9
    int 21h

L185:
    DisplayInteger a

L186:
    mov dx, OFFSET STR_27
    mov ah, 9
    int 21h

L187:
    DisplayInteger b

L188:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L189:

L190:

L191:
    mov eax, a
    cmp eax, _0

L192:
    jle L201

L193:

L194:

L195:
    mov eax, b
    cmp eax, _0

L196:
    jle L199

L197:
    mov dx, OFFSET STR_35
    mov ah, 9
    int 21h

L198:
    jmp L200

L199:
    mov dx, OFFSET STR_36
    mov ah, 9
    int 21h

L200:
    jmp L202

L201:
    mov dx, OFFSET STR_37
    mov ah, 9
    int 21h

L202:

L203:

L204:
    fld dword ptr [e]
    fcomp dword ptr [_0_0]
    fstsw ax
    sahf

L205:
    jbe L211

L206:

L207:

L208:
    fld dword ptr [f]
    fcomp dword ptr [_0_0]
    fstsw ax
    sahf

L209:
    jbe L211

L210:
    mov dx, OFFSET STR_38
    mov ah, 9
    int 21h

L211:
    mov dx, OFFSET STR_11
    mov ah, 9
    int 21h

L212:
    GetInteger pausa

L213:
    mov dx, OFFSET STR_39
    mov ah, 9
    int 21h

L214:

L215:

L216:
    mov eax, _4
    mov a, eax

L217:
    mov dx, OFFSET STR_40
    mov ah, 9
    int 21h

L218:
    DisplayInteger a

L219:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L220:
L221:

L222:

L223:
    mov eax, a
    cmp eax, _0

L224:
    jle L243

L225:
    mov dx, OFFSET STR_41
    mov ah, 9
    int 21h

L226:
    DisplayInteger a

L227:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L228:

L229:

L230:
    mov eax, a
    cdq
    mov ebx, _2
    idiv ebx
    mov tmp230, edx

L231:

L232:
    mov eax, tmp230
    cmp eax, _0

L233:
    jne L236

L234:
    mov dx, OFFSET STR_42
    mov ah, 9
    int 21h

L235:
    jmp L237

L236:
    mov dx, OFFSET STR_43
    mov ah, 9
    int 21h

L237:

L238:

L239:

L240:
    mov eax, a
    sub eax, _1
    mov tmp240, eax

L241:
    mov eax, tmp240
    mov a, eax

L242:
    jmp L220

L243:
    mov dx, OFFSET STR_44
    mov ah, 9
    int 21h

L244:
L245:

L246:

L247:
    fld dword ptr [e]
    fcomp dword ptr [_8_0]
    fstsw ax
    sahf

L248:
    jbe L263

L249:
    mov dx, OFFSET STR_45
    mov ah, 9
    int 21h

L250:
    DisplayFloat e, 2

L251:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L252:

L253:

L254:
    fld dword ptr [e]
    fcomp dword ptr [_9_0]
    fstsw ax
    sahf

L255:
    jbe L257

L256:
    mov dx, OFFSET STR_46
    mov ah, 9
    int 21h

L257:

L258:

L259:

L260:
    fld dword ptr [e]
    fsub dword ptr [_1_0]
    fstp dword ptr [tmp260]

L261:
    mov eax, tmp260
    mov e, eax

L262:
    jmp L244

L263:

L264:

L265:
    mov eax, _10_5
    mov e, eax

L266:
    mov dx, OFFSET STR_11
    mov ah, 9
    int 21h

L267:
    GetInteger pausa

L268:
    mov dx, OFFSET STR_47
    mov ah, 9
    int 21h

L269:

L270:

L271:
    mov eax, _2
    mov a, eax

L272:
L273:

L274:

L275:
    mov eax, a
    cmp eax, _0

L276:
    jle L302

L277:

L278:

L279:
    mov eax, _2
    mov b, eax

L280:
L281:

L282:

L283:
    mov eax, b
    cmp eax, _0

L284:
    jle L296

L285:
    mov dx, OFFSET STR_48
    mov ah, 9
    int 21h

L286:
    DisplayInteger a

L287:
    mov dx, OFFSET STR_27
    mov ah, 9
    int 21h

L288:
    DisplayInteger b

L289:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L290:

L291:

L292:

L293:
    mov eax, b
    sub eax, _1
    mov tmp293, eax

L294:
    mov eax, tmp293
    mov b, eax

L295:
    jmp L280

L296:

L297:

L298:

L299:
    mov eax, a
    sub eax, _1
    mov tmp299, eax

L300:
    mov eax, tmp299
    mov a, eax

L301:
    jmp L272

L302:
    mov dx, OFFSET STR_49
    mov ah, 9
    int 21h

L303:

L304:

L305:
    mov eax, _7_0
    mov e, eax

L306:
L307:

L308:

L309:
    fld dword ptr [e]
    fcomp dword ptr [_5_0]
    fstsw ax
    sahf

L310:
    jbe L336

L311:

L312:

L313:
    mov eax, _2_0
    mov f, eax

L314:
L315:

L316:

L317:
    fld dword ptr [f]
    fcomp dword ptr [_0_0]
    fstsw ax
    sahf

L318:
    jbe L330

L319:
    mov dx, OFFSET STR_50
    mov ah, 9
    int 21h

L320:
    DisplayFloat e, 2

L321:
    mov dx, OFFSET STR_22
    mov ah, 9
    int 21h

L322:
    DisplayFloat f, 2

L323:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L324:

L325:

L326:

L327:
    fld dword ptr [f]
    fsub dword ptr [_1_0]
    fstp dword ptr [tmp327]

L328:
    mov eax, tmp327
    mov f, eax

L329:
    jmp L314

L330:

L331:

L332:

L333:
    fld dword ptr [e]
    fsub dword ptr [_1_0]
    fstp dword ptr [tmp333]

L334:
    mov eax, tmp333
    mov e, eax

L335:
    jmp L306

L336:

L337:

L338:
    mov eax, _10_5
    mov e, eax

L339:

L340:

L341:
    mov eax, _3_2
    mov f, eax

L342:
    mov dx, OFFSET STR_11
    mov ah, 9
    int 21h

L343:
    GetInteger pausa

L344:
    mov dx, OFFSET STR_51
    mov ah, 9
    int 21h

L345:
    mov dx, OFFSET STR_52
    mov ah, 9
    int 21h

L346:

L347:

L348:

L349:

L350:

L351:
    mov eax, _0
    mov @aux1, eax

L352:
L353:

L354:

L355:
    mov eax, @aux1
    cmp eax, _3

L356:
    jge L387

L357:

L358:

L359:
    mov eax, _0
    cmp eax, @aux1

L360:
    je L369

L361:

L362:

L363:
    mov eax, _1
    cmp eax, @aux1

L364:
    je L372

L365:

L366:

L367:
    mov eax, _2
    cmp eax, @aux1

L368:
    je L375

L369:

L370:
    mov eax, _10
    mov a, eax

L371:
    jmp L378

L372:

L373:
    mov eax, _20
    mov a, eax

L374:
    jmp L378

L375:

L376:
    mov eax, _30
    mov a, eax

L377:
    jmp L378

L378:

L379:

L380:
    mov eax, @aux1
    add eax, _1
    mov tmp380, eax

L381:

L382:
    mov eax, tmp380
    mov @aux1, eax

L383:
    mov dx, OFFSET STR_53
    mov ah, 9
    int 21h

L384:
    DisplayInteger a

L385:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L386:
    jmp L352

L387:
    mov dx, OFFSET STR_54
    mov ah, 9
    int 21h

L388:

L389:

L390:

L391:

L392:

L393:
    mov eax, _0
    mov @aux2, eax

L394:
L395:

L396:

L397:
    mov eax, @aux2
    cmp eax, _3

L398:
    jge L429

L399:

L400:

L401:
    mov eax, _0
    cmp eax, @aux2

L402:
    je L411

L403:

L404:

L405:
    mov eax, _1
    cmp eax, @aux2

L406:
    je L414

L407:

L408:

L409:
    mov eax, _2
    cmp eax, @aux2

L410:
    je L417

L411:

L412:
    mov eax, _10_5
    mov e, eax

L413:
    jmp L420

L414:

L415:
    mov eax, _20_5
    mov e, eax

L416:
    jmp L420

L417:

L418:
    mov eax, _30_5
    mov e, eax

L419:
    jmp L420

L420:

L421:

L422:
    mov eax, @aux2
    add eax, _1
    mov tmp422, eax

L423:

L424:
    mov eax, tmp422
    mov @aux2, eax

L425:
    mov dx, OFFSET STR_55
    mov ah, 9
    int 21h

L426:
    DisplayFloat e, 2

L427:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L428:
    jmp L394

L429:

L430:

L431:
    mov eax, _10_5
    mov e, eax

L432:
    mov dx, OFFSET STR_11
    mov ah, 9
    int 21h

L433:
    GetInteger pausa

L434:
    mov dx, OFFSET STR_56
    mov ah, 9
    int 21h

L435:
    mov dx, OFFSET STR_57
    mov ah, 9
    int 21h

L436:

L437:

L438:

L439:

L440:
    mov eax, _0
    mov @aux3, eax

L441:
L442:

L443:

L444:
    mov eax, @aux3
    cmp eax, _2

L445:
    jge L501

L446:

L447:

L448:
    mov eax, _0
    cmp eax, @aux3

L449:
    je L454

L450:

L451:

L452:
    mov eax, _1
    cmp eax, @aux3

L453:
    je L457

L454:

L455:
    mov eax, _1
    mov a, eax

L456:
    jmp L460

L457:

L458:
    mov eax, _2
    mov a, eax

L459:
    jmp L460

L460:

L461:

L462:
    mov eax, @aux3
    add eax, _1
    mov tmp462, eax

L463:

L464:
    mov eax, tmp462
    mov @aux3, eax

L465:

L466:

L467:

L468:

L469:
    mov eax, _0
    mov @aux4, eax

L470:
L471:

L472:

L473:
    mov eax, @aux4
    cmp eax, _2

L474:
    jge L500

L475:

L476:

L477:
    mov eax, _0
    cmp eax, @aux4

L478:
    je L483

L479:

L480:

L481:
    mov eax, _1
    cmp eax, @aux4

L482:
    je L486

L483:

L484:
    mov eax, _100
    mov b, eax

L485:
    jmp L489

L486:

L487:
    mov eax, _200
    mov b, eax

L488:
    jmp L489

L489:

L490:

L491:
    mov eax, @aux4
    add eax, _1
    mov tmp491, eax

L492:

L493:
    mov eax, tmp491
    mov @aux4, eax

L494:
    mov dx, OFFSET STR_58
    mov ah, 9
    int 21h

L495:
    DisplayInteger a

L496:
    mov dx, OFFSET STR_27
    mov ah, 9
    int 21h

L497:
    DisplayInteger b

L498:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L499:
    jmp L470

L500:
    jmp L441

L501:
    mov dx, OFFSET STR_59
    mov ah, 9
    int 21h

L502:

L503:

L504:

L505:

L506:
    mov eax, _0
    mov @aux5, eax

L507:
L508:

L509:

L510:
    mov eax, @aux5
    cmp eax, _2

L511:
    jge L567

L512:

L513:

L514:
    mov eax, _0
    cmp eax, @aux5

L515:
    je L520

L516:

L517:

L518:
    mov eax, _1
    cmp eax, @aux5

L519:
    je L523

L520:

L521:
    mov eax, _1_5
    mov e, eax

L522:
    jmp L526

L523:

L524:
    mov eax, _2_5
    mov e, eax

L525:
    jmp L526

L526:

L527:

L528:
    mov eax, @aux5
    add eax, _1
    mov tmp528, eax

L529:

L530:
    mov eax, tmp528
    mov @aux5, eax

L531:

L532:

L533:

L534:

L535:
    mov eax, _0
    mov @aux6, eax

L536:
L537:

L538:

L539:
    mov eax, @aux6
    cmp eax, _2

L540:
    jge L566

L541:

L542:

L543:
    mov eax, _0
    cmp eax, @aux6

L544:
    je L549

L545:

L546:

L547:
    mov eax, _1
    cmp eax, @aux6

L548:
    je L552

L549:

L550:
    mov eax, _100_5
    mov f, eax

L551:
    jmp L555

L552:

L553:
    mov eax, _200_5
    mov f, eax

L554:
    jmp L555

L555:

L556:

L557:
    mov eax, @aux6
    add eax, _1
    mov tmp557, eax

L558:

L559:
    mov eax, tmp557
    mov @aux6, eax

L560:
    mov dx, OFFSET STR_60
    mov ah, 9
    int 21h

L561:
    DisplayFloat e, 2

L562:
    mov dx, OFFSET STR_22
    mov ah, 9
    int 21h

L563:
    DisplayFloat f, 2

L564:
    mov dx, OFFSET STR_4
    mov ah, 9
    int 21h

L565:
    jmp L536

L566:
    jmp L507

L567:

L568:

L569:
    mov eax, _10_5
    mov e, eax

L570:

L571:

L572:
    mov eax, _3_2
    mov f, eax

L573:
    mov dx, OFFSET STR_11
    mov ah, 9
    int 21h

L574:
    GetInteger pausa

L575:
    mov dx, OFFSET STR_61
    mov ah, 9
    int 21h

L576:
    mov dx, OFFSET STR_62
    mov ah, 9
    int 21h

L577:
    GetInteger a

L578:
    mov dx, OFFSET STR_63
    mov ah, 9
    int 21h

L579:
    DisplayInteger a

L580:
    mov dx, OFFSET STR_64
    mov ah, 9
    int 21h

L581:
    mov dx, OFFSET STR_65
    mov ah, 9
    int 21h

    mov ah, 4Ch
    int 21h
END START