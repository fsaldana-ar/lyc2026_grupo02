include macros2.asm
include number.asm

.MODEL  SMALL
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
    _0 dd 0
    _1 dd 1
    _-1 dd -1
    _-150 dd -150
    _19.1 dd 19.1
    _18. dd 18.
    _.17 dd .17
    _-19.1 dd -19.1
    _-18. dd -18.
    _-.17 dd -.17
    _99999.99 dd 99999.99
    _99. dd 99.
    _.9999 dd .9999
    _27 dd 27
    _500 dd 500
    _34 dd 34
    _3 dd 3
    _21 dd 21
    _4 dd 4
    _-21 dd -21
    _2 dd 2
    _.27 dd .27
    _50.0 dd 50.0
    _3.4 dd 3.4
    _3. dd 3.
    _.21 dd .21
    _2.1 dd 2.1
    _10 dd 10
    _35 dd 35
    _100 dd 100
    _5 dd 5
    _6 dd 6
    _9 dd 9
    _55 dd 55
    _7 dd 7
    @aux1 dd ?
    @aux2 dd ?
    @aux3 dd ?
    @aux4 dd ?
    @aux5 dd ?
    @aux6 dd ?
    STR_0 db "a es mas grande que b","$"
    STR_1 db "a es mas chico o igual a b","$"
    STR_2 db "ewr","$"
    STR_3 db "a es mas grande que b y c es mas grande que b","$"
    STR_4 db "a es mas grande que b o c es mas grande que b","$"
    STR_5 db "a no es mas grande que b","$"
    STR_6 db "Par","$"
    STR_7 db "HolaMundo","$"
    STR_8 db "Test","$"
    tmp66 dd ?
    tmp71 dd ?
    tmp76 dd ?
    tmp81 dd ?
    tmp87 dd ?
    tmp88 dd ?
    tmp90 dd ?
    tmp96 dd ?
    tmp97 dd ?
    tmp99 dd ?
    tmp105 dd ?
    tmp106 dd ?
    tmp108 dd ?
    tmp113 dd ?
    tmp118 dd ?
    tmp123 dd ?
    tmp128 dd ?
    tmp134 dd ?
    tmp135 dd ?
    tmp137 dd ?
    tmp143 dd ?
    tmp144 dd ?
    tmp146 dd ?
    tmp164 dd ?
    tmp177 dd ?
    tmp190 dd ?
    tmp222 dd ?
    tmp233 dd ?
    tmp425 dd ?
    tmp431 dd ?
    tmp649 dd ?
    tmp669 dd ?
    tmp670 dd ?
    tmp697 dd ?
    tmp715 dd ?
    tmp716 dd ?
    tmp721 dd ?
    tmp723 dd ?
    tmp726 dd ?
    tmp728 dd ?
    tmp747 dd ?
    tmp748 dd ?
    tmp753 dd ?
    tmp755 dd ?
    tmp758 dd ?
    tmp760 dd ?
    tmp797 dd ?
    tmp804 dd ?
    tmp807 dd ?
    tmp842 dd ?
    tmp848 dd ?
    tmp894 dd ?
    tmp910 dd ?
    tmp913 dd ?
    tmp954 dd ?
    tmp1002 dd ?
    tmp1007 dd ?
    tmp1033 dd ?

.CODE

START:
    mov ax,@DATA
    mov ds,ax
    mov es,ax

L0:

L1:

L2:
    mov eax, 0
    mov a, eax

L3:

L4:

L5:
    mov eax, 1
    mov a, eax

L6:

L7:

L8:
    mov eax, -1
    mov a, eax

L9:

L10:

L11:
    mov eax, -150
    mov a, eax

L12:

L13:

L14:
    mov eax, 19.1
    mov e, eax

L15:

L16:

L17:
    mov eax, 18.0
    mov e, eax

L18:

L19:

L20:
    mov eax, 0.17
    mov e, eax

L21:

L22:

L23:
    mov eax, -19.1
    mov e, eax

L24:

L25:

L26:
    mov eax, -18.0
    mov e, eax

L27:

L28:

L29:
    mov eax, -0.17
    mov e, eax

L30:

L31:

L32:
    mov eax, 99999.99
    mov e, eax

L33:

L34:

L35:
    mov eax, 99.0
    mov e, eax

L36:

L37:

L38:
    mov eax, 0.9999
    mov e, eax

L39:

L40:

L41:
    mov eax, "string"
    mov i, eax

L42:

L43:

L44:
    mov eax, "string09"
    mov i, eax

L45:

L46:

L47:
    mov eax, "string 09"
    mov i, eax

L48:

L49:

L50:
    mov eax, "Hol@, Mundo"
    mov i, eax

L51:

L52:

L53:
    mov eax, "Hola % Mundo"
    mov i, eax

L54:

L55:

L56:
    mov eax, "        s t r i n g   "
    mov i, eax

L57:

L58:

L59:
    mov eax, "@sdADaSjfla%dfg"
    mov i, eax

L60:

L61:

L62:
    mov eax, "asldk  fh sjf"
    mov i, eax

L63:

L64:

L65:

L66:
    mov eax, 27
    sub eax, c
    mov tmp66, eax

L67:
    mov eax, tmp66
    mov a, eax

L68:

L69:

L70:

L71:
    mov eax, b
    add eax, 500
    mov tmp71, eax

L72:
    mov eax, tmp71
    mov a, eax

L73:

L74:

L75:

L76:
    mov eax, 34
    imul eax, 3
    mov tmp76, eax

L77:
    mov eax, tmp76
    mov a, eax

L78:

L79:

L80:

L81:
    mov eax, c
    cdq
    mov ebx, d
    idiv ebx
    mov tmp81, eax

L82:
    mov eax, tmp81
    mov a, eax

L83:

L84:

L85:

L86:

L87:
    mov eax, b
    sub eax, 21
    mov tmp87, eax

L88:
    mov eax, d
    imul eax, tmp87
    mov tmp88, eax

L89:

L90:
    mov eax, tmp88
    cdq
    mov ebx, 4
    idiv ebx
    mov tmp90, eax

L91:
    mov eax, tmp90
    mov a, eax

L92:

L93:

L94:

L95:

L96:
    mov eax, a
    add eax, -21
    mov tmp96, eax

L97:
    mov eax, d
    imul eax, tmp96
    mov tmp97, eax

L98:

L99:
    mov eax, tmp97
    cdq
    mov ebx, 4
    idiv ebx
    mov tmp99, eax

L100:
    mov eax, tmp99
    mov a, eax

L101:

L102:

L103:

L104:

L105:
    mov eax, c
    add eax, 21
    mov tmp105, eax

L106:
    mov eax, d
    imul eax, tmp105
    mov tmp106, eax

L107:

L108:
    mov eax, tmp106
    cdq
    mov ebx, 2
    idiv ebx
    mov tmp108, eax

L109:
    mov eax, tmp108
    mov a, eax

L110:

L111:

L112:

L113:
    mov eax, 0.27
    sub eax, f
    mov tmp113, eax

L114:
    mov eax, tmp113
    mov e, eax

L115:

L116:

L117:

L118:
    mov eax, g
    add eax, 50.0
    mov tmp118, eax

L119:
    mov eax, tmp118
    mov e, eax

L120:

L121:

L122:

L123:
    mov eax, 3.4
    imul eax, 3.0
    mov tmp123, eax

L124:
    mov eax, tmp123
    mov e, eax

L125:

L126:

L127:

L128:
    mov eax, g
    cdq
    mov ebx, h
    idiv ebx
    mov tmp128, eax

L129:
    mov eax, tmp128
    mov e, eax

L130:

L131:

L132:

L133:

L134:
    mov eax, e
    sub eax, 0.21
    mov tmp134, eax

L135:
    mov eax, e
    imul eax, tmp134
    mov tmp135, eax

L136:

L137:
    mov eax, tmp135
    cdq
    mov ebx, 4
    idiv ebx
    mov tmp137, eax

L138:
    mov eax, tmp137
    mov e, eax

L139:

L140:

L141:

L142:

L143:
    mov eax, g
    add eax, 2.1
    mov tmp143, eax

L144:
    mov eax, f
    imul eax, tmp143
    mov tmp144, eax

L145:

L146:
    mov eax, tmp144
    cdq
    mov ebx, 2
    idiv ebx
    mov tmp146, eax

L147:
    mov eax, tmp146
    mov e, eax

L148:

L149:

L150:
    mov eax, a
    cmp eax, b

L151:
    jle L154

L152:
    displayString STR_0

L153:
    jmp L155

L154:
    displayString STR_1

L155:

L156:

L157:
    mov eax, a
    cmp eax, b

L158:
    jle L162

L159:

L160:

L161:
    mov eax, b
    mov a, eax

L162:

L163:

L164:
    mov eax, a
    imul eax, b
    mov tmp164, eax

L165:

L166:
    mov eax, tmp164
    cmp eax, c

L167:
    jge L174

L168:

L169:

L170:
    mov eax, a
    mov a, eax

L171:

L172:

L173:
    mov eax, b
    mov b, eax

L174:

L175:

L176:

L177:
    mov eax, b
    add eax, 2
    mov tmp177, eax

L178:
    mov eax, a
    cmp eax, tmp177

L179:
    jle L184

L180:

L181:

L182:
    mov eax, b
    mov a, eax

L183:
    jmp L187

L184:

L185:

L186:
    mov eax, a
    mov a, eax

L187:

L188:

L189:

L190:
    mov eax, b
    imul eax, 0
    mov tmp190, eax

L191:
    mov eax, a
    cmp eax, tmp190

L192:
    jge L197

L193:

L194:

L195:
    mov eax, b
    mov a, eax

L196:
    jmp L203

L197:

L198:

L199:
    mov eax, a
    mov a, eax

L200:

L201:

L202:
    mov eax, b
    mov b, eax

L203:

L204:

L205:
    mov eax, a
    cmp eax, 0

L206:
    jle L219

L207:

L208:

L209:
    mov eax, b
    cmp eax, 0

L210:
    jle L215

L211:

L212:

L213:
    mov eax, 1
    mov c, eax

L214:
    jmp L218

L215:

L216:

L217:
    mov eax, 0
    mov c, eax

L218:
    jmp L224

L219:

L220:

L221:

L222:
    mov eax, a
    add eax, b
    mov tmp222, eax

L223:
    mov eax, tmp222
    mov c, eax

L224:
L225:

L226:

L227:
    mov eax, a
    cmp eax, b

L228:
    jle L236

L229:
    displayString STR_0

L230:

L231:

L232:

L233:
    mov eax, a
    add eax, 1
    mov tmp233, eax

L234:
    mov eax, tmp233
    mov a, eax

L235:
    jmp L224

L236:
L237:

L238:

L239:
    mov eax, a
    cmp eax, b

L240:
    jg L245

L241:

L242:

L243:
    mov eax, b
    mov a, eax

L244:
    jmp L236

L245:
L246:

L247:

L248:
    mov eax, a
    cmp eax, b

L249:
    jl L257

L250:

L251:

L252:
    mov eax, a
    mov a, eax

L253:

L254:

L255:
    mov eax, b
    mov b, eax

L256:
    jmp L245

L257:
L258:

L259:

L260:
    mov eax, a
    cmp eax, b

L261:
    jge L266

L262:

L263:

L264:
    mov eax, b
    mov a, eax

L265:
    jmp L257

L266:
L267:

L268:

L269:
    mov eax, a
    cmp eax, b

L270:
    jle L278

L271:

L272:

L273:
    mov eax, a
    mov a, eax

L274:

L275:

L276:
    mov eax, b
    mov b, eax

L277:
    jmp L266

L278:
L279:

L280:

L281:
    mov eax, a
    cmp eax, b

L282:
    jne L287

L283:

L284:

L285:
    mov eax, b
    mov a, eax

L286:
    jmp L278

L287:
L288:

L289:

L290:
    mov eax, a
    cmp eax, b

L291:
    je L296

L292:

L293:

L294:
    mov eax, b
    mov a, eax

L295:
    jmp L287

L296:
L297:

L298:

L299:
    mov eax, a
    cmp eax, b

L300:
    jle L309

L301:

L302:

L303:
    mov eax, b
    cmp eax, a

L304:
    jge L309

L305:

L306:

L307:
    mov eax, b
    mov a, eax

L308:
    jmp L296

L309:
L310:

L311:

L312:
    mov eax, a
    cmp eax, b

L313:
    jge L325

L314:

L315:

L316:
    mov eax, b
    cmp eax, a

L317:
    jle L325

L318:

L319:

L320:
    mov eax, a
    mov a, eax

L321:

L322:

L323:
    mov eax, b
    mov b, eax

L324:
    jmp L309

L325:
L326:

L327:

L328:
    mov eax, a
    cmp eax, b

L329:
    jg L338

L330:

L331:

L332:
    mov eax, b
    cmp eax, a

L333:
    jl L338

L334:

L335:

L336:
    mov eax, b
    mov a, eax

L337:
    jmp L325

L338:
L339:

L340:

L341:
    mov eax, a
    cmp eax, b

L342:
    jne L354

L343:

L344:

L345:
    mov eax, b
    cmp eax, a

L346:
    je L354

L347:

L348:

L349:
    mov eax, a
    mov a, eax

L350:

L351:

L352:
    mov eax, b
    mov b, eax

L353:
    jmp L338

L354:
L355:

L356:

L357:
    mov eax, a
    cmp eax, b

L358:
    jg L363

L359:

L360:

L361:
    mov eax, b
    cmp eax, a

L362:
    jge L367

L363:

L364:

L365:
    mov eax, b
    mov a, eax

L366:
    jmp L354

L367:
L368:

L369:

L370:
    mov eax, a
    cmp eax, b

L371:
    jl L376

L372:

L373:

L374:
    mov eax, b
    cmp eax, a

L375:
    jle L380

L376:

L377:

L378:
    mov eax, b
    mov a, eax

L379:
    jmp L367

L380:
L381:

L382:

L383:
    mov eax, a
    cmp eax, b

L384:
    jle L389

L385:

L386:

L387:
    mov eax, b
    cmp eax, a

L388:
    jl L396

L389:

L390:

L391:
    mov eax, a
    mov a, eax

L392:

L393:

L394:
    mov eax, b
    mov b, eax

L395:
    jmp L380

L396:
L397:

L398:

L399:
    mov eax, a
    cmp eax, b

L400:
    je L405

L401:

L402:

L403:
    mov eax, b
    cmp eax, a

L404:
    je L409

L405:

L406:

L407:
    mov eax, b
    mov a, eax

L408:
    jmp L396

L409:
L410:

L411:

L412:
    mov eax, a
    cmp eax, 0

L413:
    jle L434

L414:

L415:

L416:
    mov eax, 1
    mov b, eax

L417:
L418:

L419:

L420:
    mov eax, b
    cmp eax, 10

L421:
    jge L428

L422:

L423:

L424:

L425:
    mov eax, b
    add eax, 1
    mov tmp425, eax

L426:
    mov eax, tmp425
    mov b, eax

L427:
    jmp L417

L428:

L429:

L430:

L431:
    mov eax, a
    sub eax, 1
    mov tmp431, eax

L432:
    mov eax, tmp431
    mov a, eax

L433:
    jmp L409

L434:
    GetInteger nombre

L435:
    displayString STR_2

L436:
    DisplayInteger nombre

L437:

L438:

L439:
    mov eax, a
    cmp eax, b

L440:
    jle L446

L441:

L442:

L443:
    mov eax, c
    cmp eax, b

L444:
    jle L446

L445:
    displayString STR_3

L446:

L447:

L448:
    mov eax, a
    cmp eax, b

L449:
    jle L460

L450:

L451:

L452:
    mov eax, b
    cmp eax, a

L453:
    jge L460

L454:

L455:

L456:
    mov eax, a
    mov a, eax

L457:

L458:

L459:
    mov eax, b
    mov b, eax

L460:

L461:

L462:
    mov eax, a
    cmp eax, b

L463:
    jge L472

L464:

L465:

L466:
    mov eax, b
    cmp eax, a

L467:
    jle L472

L468:

L469:

L470:
    mov eax, b
    mov a, eax

L471:
    jmp L478

L472:

L473:

L474:
    mov eax, a
    mov a, eax

L475:

L476:

L477:
    mov eax, b
    mov b, eax

L478:

L479:

L480:
    mov eax, a
    cmp eax, b

L481:
    jg L489

L482:

L483:

L484:
    mov eax, b
    cmp eax, a

L485:
    jl L489

L486:

L487:

L488:
    mov eax, b
    mov a, eax

L489:

L490:

L491:
    mov eax, a
    cmp eax, b

L492:
    jne L500

L493:

L494:

L495:
    mov eax, b
    cmp eax, a

L496:
    je L500

L497:

L498:

L499:
    mov eax, b
    mov a, eax

L500:

L501:

L502:
    mov eax, a
    cmp eax, b

L503:
    jg L507

L504:

L505:

L506:
    mov eax, b
    mov a, eax

L507:

L508:

L509:
    mov eax, a
    cmp eax, b

L510:
    jl L517

L511:

L512:

L513:
    mov eax, a
    mov a, eax

L514:

L515:

L516:
    mov eax, b
    mov b, eax

L517:

L518:

L519:
    mov eax, a
    cmp eax, b

L520:
    jge L525

L521:

L522:

L523:
    mov eax, b
    mov a, eax

L524:
    jmp L528

L525:

L526:

L527:
    mov eax, a
    mov a, eax

L528:

L529:

L530:
    mov eax, a
    cmp eax, b

L531:
    jle L535

L532:

L533:

L534:
    mov eax, b
    mov a, eax

L535:

L536:

L537:
    mov eax, a
    cmp eax, b

L538:
    jne L542

L539:

L540:

L541:
    mov eax, b
    mov a, eax

L542:

L543:

L544:
    mov eax, a
    cmp eax, b

L545:
    je L550

L546:

L547:

L548:
    mov eax, b
    mov a, eax

L549:
    jmp L556

L550:

L551:

L552:
    mov eax, a
    mov a, eax

L553:

L554:

L555:
    mov eax, b
    mov b, eax

L556:

L557:

L558:
    mov eax, a
    cmp eax, b

L559:
    jg L566

L560:

L561:

L562:
    mov eax, b
    cmp eax, a

L563:
    jge L567

L564:

L565:

L566:
    mov eax, b
    mov a, eax

L567:

L568:

L569:
    mov eax, a
    cmp eax, b

L570:
    jl L575

L571:

L572:

L573:
    mov eax, b
    cmp eax, a

L574:
    jle L579

L575:

L576:

L577:
    mov eax, b
    mov a, eax

L578:
    jmp L585

L579:

L580:

L581:
    mov eax, a
    mov a, eax

L582:

L583:

L584:
    mov eax, b
    mov b, eax

L585:

L586:

L587:
    mov eax, a
    cmp eax, b

L588:
    jle L598

L589:

L590:

L591:
    mov eax, b
    cmp eax, a

L592:
    jl L599

L593:

L594:

L595:
    mov eax, a
    mov a, eax

L596:

L597:

L598:
    mov eax, b
    mov b, eax

L599:

L600:

L601:
    mov eax, a
    cmp eax, b

L602:
    je L607

L603:

L604:

L605:
    mov eax, b
    cmp eax, a

L606:
    je L611

L607:

L608:

L609:
    mov eax, b
    mov a, eax

L610:
    jmp L614

L611:

L612:

L613:
    mov eax, a
    mov a, eax

L614:

L615:

L616:
    mov eax, a
    cmp eax, b

L617:
    jg L622

L618:

L619:

L620:
    mov eax, c
    cmp eax, b

L621:
    jle L623

L622:
    displayString STR_4

L623:

L624:

L625:
    mov eax, a
    cmp eax, b

L626:
    jg L628

L627:
    displayString STR_5

L628:
L629:

L630:

L631:
    mov eax, a
    cmp eax, b

L632:
    je L683

L633:

L634:

L635:
    mov eax, c
    cmp eax, d

L636:
    jne L683

L637:

L638:

L639:
    mov eax, e
    cmp eax, f

L640:
    jl L643

L641:
    GetInteger a

L642:
    jmp L656

L643:

L644:

L645:
    mov eax, g
    cmp eax, h

L646:
    jg L655

L647:

L648:

L649:
    mov eax, 1
    add eax, 1
    mov tmp649, eax

L650:

L651:
    mov eax, tmp649
    cmp eax, 0

L652:
    jne L656

L653:

L654:

L655:
    mov eax, a
    mov a, eax

L656:
    DisplayInteger nombre

L657:
L658:

L659:

L660:
    mov eax, f
    cmp eax, 0

L661:
    je L666

L662:

L663:

L664:
    mov eax, g
    cmp eax, 0

L665:
    je L682

L666:

L667:

L668:

L669:
    mov eax, b
    imul eax, c
    mov tmp669, eax

L670:
    mov eax, a
    add eax, tmp669
    mov tmp670, eax

L671:

L672:
    mov eax, tmp670
    cmp eax, 3

L673:
    jge L681

L674:

L675:

L676:

L677:

L678:
    mov eax, DIV
    cmp eax, 1

L679:
    jne L681

L680:
    DisplayInteger nombre

L681:
    jmp L657

L682:
    jmp L628

L683:

L684:

L685:

L686:

L687:
    mov eax, MOD
    cmp eax, 0

L688:
    jne L690

L689:
    displayString STR_6

L690:

L691:

L692:

L693:

L694:

L695:

L696:

L697:
    mov eax, DIV
    add eax, MOD
    mov tmp697, eax

L698:
    mov eax, tmp697
    mov e, eax

L699:

L700:

L701:

L702:

L703:
    mov eax, MOD
    mov a, eax

L704:

L705:

L706:

L707:

L708:
    mov eax, MOD
    mov a, eax

L709:

L710:

L711:

L712:

L713:

L714:

L715:
    mov eax, MOD
    imul eax, 100
    mov tmp715, eax

L716:
    mov eax, 35
    add eax, tmp715
    mov tmp716, eax

L717:
    mov eax, tmp716
    mov a, eax

L718:

L719:

L720:

L721:
    mov eax, 1
    add eax, 2
    mov tmp721, eax

L722:

L723:
    mov eax, tmp721
    add eax, 3
    mov tmp723, eax

L724:

L725:

L726:
    mov eax, 4
    add eax, 5
    mov tmp726, eax

L727:

L728:
    mov eax, tmp726
    add eax, 6
    mov tmp728, eax

L729:

L730:
    mov eax, MOD
    mov a, eax

L731:

L732:

L733:

L734:

L735:
    mov eax, DIV
    mov e, eax

L736:

L737:

L738:

L739:

L740:
    mov eax, DIV
    mov e, eax

L741:

L742:

L743:

L744:

L745:

L746:

L747:
    mov eax, DIV
    imul eax, 100
    mov tmp747, eax

L748:
    mov eax, 35
    add eax, tmp747
    mov tmp748, eax

L749:
    mov eax, tmp748
    mov e, eax

L750:

L751:

L752:

L753:
    mov eax, 1
    add eax, 2
    mov tmp753, eax

L754:

L755:
    mov eax, tmp753
    add eax, 3
    mov tmp755, eax

L756:

L757:

L758:
    mov eax, 4
    add eax, 5
    mov tmp758, eax

L759:

L760:
    mov eax, tmp758
    add eax, 6
    mov tmp760, eax

L761:

L762:
    mov eax, DIV
    mov e, eax

L763:

L764:

L765:

L766:

L767:

L768:
    mov eax, 0
    mov @aux1, eax

L769:
L770:

L771:

L772:
    mov eax, @aux1
    cmp eax, 3

L773:
    jge L802

L774:

L775:

L776:
    mov eax, 0
    cmp eax, @aux1

L777:

L778:

L779:

L780:
    mov eax, 1
    cmp eax, @aux1

L781:

L782:

L783:

L784:
    mov eax, 2
    cmp eax, @aux1

L785:

L786:

L787:
    mov eax, 1
    mov a, eax

L788:
    jmp L795

L789:

L790:
    mov eax, 2
    mov a, eax

L791:
    jmp L795

L792:

L793:
    mov eax, 3
    mov a, eax

L794:
    jmp L795

L795:

L796:

L797:
    mov eax, @aux1
    add eax, 1
    mov tmp797, eax

L798:

L799:
    mov eax, tmp797
    mov @aux1, eax

L800:
    DisplayInteger a

L801:
    jmp L769

L802:

L803:

L804:
    mov eax, 1
    add eax, 1
    mov tmp804, eax

L805:

L806:

L807:
    mov eax, 2
    imul eax, 2
    mov tmp807, eax

L808:

L809:

L810:

L811:

L812:

L813:
    mov eax, 0
    mov @aux2, eax

L814:
L815:

L816:

L817:
    mov eax, @aux2
    cmp eax, 3

L818:
    jge L852

L819:

L820:

L821:
    mov eax, 0
    cmp eax, @aux2

L822:

L823:

L824:

L825:
    mov eax, 1
    cmp eax, @aux2

L826:

L827:

L828:

L829:
    mov eax, 2
    cmp eax, @aux2

L830:

L831:

L832:
    mov eax, tmp804
    mov b, eax

L833:
    jmp L840

L834:

L835:
    mov eax, tmp807
    mov b, eax

L836:
    jmp L840

L837:

L838:
    mov eax, DIV
    mov b, eax

L839:
    jmp L840

L840:

L841:

L842:
    mov eax, @aux2
    add eax, 1
    mov tmp842, eax

L843:

L844:
    mov eax, tmp842
    mov @aux2, eax

L845:

L846:

L847:

L848:
    mov eax, b
    imul eax, 2
    mov tmp848, eax

L849:
    mov eax, tmp848
    mov d, eax

L850:
    DisplayInteger d

L851:
    jmp L814

L852:

L853:

L854:

L855:

L856:

L857:

L858:
    mov eax, 0
    mov @aux3, eax

L859:
L860:

L861:

L862:
    mov eax, @aux3
    cmp eax, 4

L863:
    jge L908

L864:

L865:

L866:
    mov eax, 0
    cmp eax, @aux3

L867:

L868:

L869:

L870:
    mov eax, 1
    cmp eax, @aux3

L871:

L872:

L873:

L874:
    mov eax, 2
    cmp eax, @aux3

L875:

L876:

L877:

L878:
    mov eax, 3
    cmp eax, @aux3

L879:

L880:

L881:
    mov eax, 1
    mov c, eax

L882:
    jmp L892

L883:

L884:
    mov eax, 2
    mov c, eax

L885:
    jmp L892

L886:

L887:
    mov eax, 3
    mov c, eax

L888:
    jmp L892

L889:

L890:
    mov eax, 4
    mov c, eax

L891:
    jmp L892

L892:

L893:

L894:
    mov eax, @aux3
    add eax, 1
    mov tmp894, eax

L895:

L896:
    mov eax, tmp894
    mov @aux3, eax

L897:

L898:

L899:

L900:

L901:
    mov eax, MOD
    cmp eax, 0

L902:
    jne L907

L903:
    displayString STR_7

L904:

L905:

L906:
    mov eax, "ResultadoPar"
    mov nombre, eax

L907:
    jmp L859

L908:

L909:

L910:
    mov eax, 1
    imul eax, 0
    mov tmp910, eax

L911:

L912:

L913:
    mov eax, 2
    cdq
    mov ebx, 1
    idiv ebx
    mov tmp913, eax

L914:

L915:

L916:

L917:

L918:
    mov eax, 0
    mov @aux4, eax

L919:
L920:

L921:

L922:
    mov eax, @aux4
    cmp eax, 4

L923:
    jge L968

L924:

L925:

L926:
    mov eax, 0
    cmp eax, @aux4

L927:

L928:

L929:

L930:
    mov eax, 1
    cmp eax, @aux4

L931:

L932:

L933:

L934:
    mov eax, 2
    cmp eax, @aux4

L935:

L936:

L937:

L938:
    mov eax, 3
    cmp eax, @aux4

L939:

L940:

L941:
    mov eax, tmp910
    mov a, eax

L942:
    jmp L952

L943:

L944:
    mov eax, tmp913
    mov a, eax

L945:
    jmp L952

L946:

L947:
    mov eax, 3
    mov a, eax

L948:
    jmp L952

L949:

L950:
    mov eax, 9
    mov a, eax

L951:
    jmp L952

L952:

L953:

L954:
    mov eax, @aux4
    add eax, 1
    mov tmp954, eax

L955:

L956:
    mov eax, tmp954
    mov @aux4, eax

L957:

L958:

L959:
    mov eax, 55
    mov b, eax

L960:

L961:

L962:
    mov eax, b
    cmp eax, a

L963:
    jge L966

L964:
    DisplayInteger b

L965:
    jmp L967

L966:
    displayString STR_8

L967:
    jmp L919

L968:

L969:

L970:

L971:

L972:

L973:
    mov eax, 0
    mov @aux5, eax

L974:
L975:

L976:

L977:
    mov eax, @aux5
    cmp eax, 3

L978:
    jge L1049

L979:

L980:

L981:
    mov eax, 0
    cmp eax, @aux5

L982:

L983:

L984:

L985:
    mov eax, 1
    cmp eax, @aux5

L986:

L987:

L988:

L989:
    mov eax, 2
    cmp eax, @aux5

L990:

L991:

L992:
    mov eax, 1
    mov a, eax

L993:
    jmp L1000

L994:

L995:
    mov eax, 2
    mov a, eax

L996:
    jmp L1000

L997:

L998:
    mov eax, 3
    mov a, eax

L999:
    jmp L1000

L1000:

L1001:

L1002:
    mov eax, @aux5
    add eax, 1
    mov tmp1002, eax

L1003:

L1004:
    mov eax, tmp1002
    mov @aux5, eax

L1005:

L1006:

L1007:
    mov eax, 5
    imul eax, 0
    mov tmp1007, eax

L1008:

L1009:

L1010:

L1011:
    mov eax, 0
    mov @aux6, eax

L1012:
L1013:

L1014:

L1015:
    mov eax, @aux6
    cmp eax, 2

L1016:
    jge L1047

L1017:

L1018:

L1019:
    mov eax, 0
    cmp eax, @aux6

L1020:

L1021:

L1022:

L1023:
    mov eax, 1
    cmp eax, @aux6

L1024:

L1025:

L1026:
    mov eax, tmp1007
    mov c, eax

L1027:
    jmp L1031

L1028:

L1029:
    mov eax, 7
    mov c, eax

L1030:
    jmp L1031

L1031:

L1032:

L1033:
    mov eax, @aux6
    add eax, 1
    mov tmp1033, eax

L1034:

L1035:
    mov eax, tmp1033
    mov @aux6, eax

L1036:

L1037:

L1038:

L1039:

L1040:
    mov eax, MOD
    cmp eax, 0

L1041:
    jne L1046

L1042:
    displayString STR_7

L1043:

L1044:

L1045:
    mov eax, "ResultadoPar"
    mov nombre, eax

L1046:
    jmp L1012

L1047:
    DisplayInteger a

L1048:
    jmp L974

L1049:

    mov ah, 4Ch
    int 21h
END START