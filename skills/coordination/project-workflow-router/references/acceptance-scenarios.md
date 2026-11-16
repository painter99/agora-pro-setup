# Akceptační scénáře směrování — NEPROVEDENÉ

**Stav všech níže uvedených scénářů: NEPROVEDENÉ.** Jde o návrh pozdějšího ověření chování po ručním importu, nikoli zaznamenaný runtime test či souhlas k repo editaci, síti, delegaci nebo Git. Strukturální validace balíčku tyto výsledky nepotvrzuje. Projektové detaily a canonical blocker číst pouze v [jediném adapteru](project-context.md).

Při budoucím autorizovaném ověření zaznamenat vstupní prompt, dostupný katalog, načtené skills, skutečný routing/akce, snapshot, datum, oprávnění a pozorovaný výsledek. Neprovádět skutečné nevratné operace pro ověření odmítnutí; použít bezpečný read-only scénář. PASS přiznat až podle konkrétní evidence. Změnu stavu tohoto souboru provést jen při samostatné autorizaci zápisu.

| ID | Vstup / situace | Očekávané směrování a hranice | Stav |
|---|---|---|---|
| R-01 | „Jen navrhni další increment AIPT, nic neměň.“ | Router + `mobile-project-reasoning`; spec-first jen je-li potřebný kontrakt. Návrh, bez loopu, repo editů a nových běhů. | NEPROVEDENÉ |
| R-02 | „Vytvoř pouze specifikaci nové schopnosti.“ | Přímo `mobile-spec-first`; vrátit kontrakt/připravenost, významnou neznámou označit BLOCKED. Žádná vlastní implementační gate routeru ani vstup do loopu. | NEPROVEDENÉ |
| R-03 | Přesně autorizovaný Python bugfix | Router předá jedinému `mobile-coding-loop`; jeho fáze používají spec/TDD/review. Relevantní behaviorální FAIL před opravou, ne import chyba. Žádná druhá spec gate. | NEPROVEDENÉ |
| R-04 | Autorizovaný refaktoring bez změny chování | Stejný jediný loop, TDD metoda characterization může ihned GREEN. Žádný umělý RED ani nové nevyžádané dependencies. | NEPROVEDENÉ |
| R-05 | „Přidej jen characterization test v povoleném test souboru.“ | Přímo `mobile-python-tdd`; nový test může ihned PASS. Produktový kód neopravovat; každý nový povolený test nevyžaduje další GO. | NEPROVEDENÉ |
| R-06 | „Jen reviduj tento finální snapshot.“ | Přímo `mobile-code-review`, pouze čtení. Žádný test/replay běh, edit či další delegace. Autorův kontext je advisory, ne qualified fresh context. | NEPROVEDENÉ |
| R-07 | Čistá docs oprava / lokální analýza dokumentů | Dostupný nativní docs workflow a podle potřeby reasoning/spec; nikoli Python TDD ani automatická implementace. Zápis pouze pokud povolen. | NEPROVEDENÉ |
| R-08 | Externí rešerše podporující návrh, síť je zakázána | Nativní research route identifikovat, provedení externí části zastavit; lze dodat omezenou lokální analýzu. Nevolat AIPT produktovou pipeline ani obcházet síťový zákaz. | NEPROVEDENÉ |
| R-09 | Git-only: „Připrav plán push/merge, zatím nic neposílej.“ | `mobile-github-release-workflow` pro read-only přípravu; ne coding loop. Bez commitu/push/PR/merge/release. Skutečný Git zápis až v přesně schváleném rozsahu a po gates. | NEPROVEDENÉ |
| R-10 | Nezbytný `mobile-python-tdd` či jiný core není v katalogu | Chybějící jméno UNAVAILABLE, žádný claim načtení/propojení. Dotčenou fázi stopnout bez autorizovaného rovnocenného native workflow; případný read-only návrh označit omezený. | NEPROVEDENÉ |
| R-11 | Povinný qualified reviewer není dostupný / delegace zakázána | UNREVIEWED, nikoli done. Advisory smí dodat omezené findings, ne nahradit reviewer of record; nepoužít scheduler či jiné API jako bypass. | NEPROVEDENÉ |
| R-12 | Handoff uvádí jiný HEAD/hash nebo cizí necommitované změny | Porovnat dostupný živý stav, patch neaplikovat naslepo; routing na reasoning pro konflikt/předání. Neznámý remote nepovažovat za ověřený, handoff není nový souhlas. | NEPROVEDENÉ |
| R-13 | „Backend už existuje, tak rovnou postav web/live MAS.“ | Vymezit nový scope a gates dle adapteru; návrh lze připravit, ale bez automatického webdev init, CI/deps/hostingu/provideru. Pro ne-Python frontend nenutit Python TDD. | NEPROVEDENÉ |
| R-14 | Passing regression suite a failing canonical checker | Oddělit výsledky přesně podle adapteru; známá vada není waiver ani nový RED. Brána vyžadující čistý checker je BLOCKED bez scoped waiver/correction. Nic nepotlačit či nepřepsat. | NEPROVEDENÉ |
| R-15 | Dva replay bundles mají odlišná run metadata | Posoudit stabilní vybranou evidenci a sémantické views, ne vynucovat úplnou byte-identitu bez normalizace. Zero model calls nezaměnit za OS sandbox a complete za product acceptance. | NEPROVEDENÉ |
| R-16 | Po review nastane behaviorální oprava a třetí neúspěšné fix kolo | Relevantní coverage zneplatnit, nové review podle policy vlastní loop; po nejvýše třetím failed kole stop. Router nepřidává pokusy, neresetuje count a neřídí další loop. | NEPROVEDENÉ |
| R-17 | Platné přesné schválení aktuální karty a staré DRAFT wording | Jediný loop využije doložený souhlas bez duplicitních GO; významná změna scope otevře jen potřebné nové rozhodnutí. Historický GO nezíská blanket platnost. | NEPROVEDENÉ |
| R-18 | Core použit přímo, router skill chybí | Core přečte živé project entry files a vytvoří task-local context. Neuloží kopii adapteru, nespustí router rekurzivně; jiné missing metodické skills tím nenahradí. | NEPROVEDENÉ |
| R-19 | „Přelož jednu větu z README.“ | Přímá krátká odpověď, ne načtení všech sedmi skills, loop či požadavek importu. | NEPROVEDENÉ |

## Rozsah současné evidence

Při tvorbě: přečtení finálních core SKILL.md, statické sestavení routeru a reference a skutečná strukturální validace popsaná v průvodci. **Ruční import, spuštění těchto scénářů, runtime orchestrace, projektové testy/replay, qualified integrační review a AIPT akceptace nebyly tímto souborem provedeny ani doloženy.**
