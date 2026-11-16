# Původ a licenční hranice

## Přímý metodický zdroj

Odvodit tento český skill z `agora-pro-setup`, soubor `skills/android-development/android-dev-tdd/SKILL.md`, revize `552034846217c035ce802aad276fb826d0aaedf4`. Zdrojový soubor byl celý lokálně přečten 2026-11-14; identifikátor zdrojové revize převzít ze závazného build-contractu, nikoli vydávat za nové Git ověření.

Zachovat upstream MIT notice a celé licenční znění v `../LICENSE.txt` beze změny: Copyright (c) 2026 Pavel Mareš. Licence pokrývá tento metodický derivát, nikoli cizí projektový kód či data.

Původní skill uvádí vlastní adaptaci z `addyosmani/agent-skills/skills/test-driven-development` (RED–GREEN–REFACTOR, Prove-It, test pyramid, Beyoncé rule). Uvést tuto sekundární atribuci jako převzatý údaj upstreamu; sekundární zdroj nebyl v tomto úkolu samostatně čten ani ověřován.

## Adaptace — 2026-11-14

- Zachovat tests-first, behaviorální reprodukci bugu, minimální opravu, regresi a fixture-first přístup.
- Nahradit Android/Kotlin/Compose/Gradle konvence stdlib Python `unittest`, `unittest.mock` a dočasnými adresáři; nepřevzít nástroje ani procentní test pyramid.
- Opravit „Tests are proof“ na konkrétní software evidenci oddělenou od pravdivosti, source support a přijetí operátorem.
- Přidat ihned zelenou characterization, test-only hranici, integritu fixture kopií, přesné snapshot/FAIL/PASS záznamy, známé checker blokace a limit opravných kol.
- Zachovat jednosměrnou kompozici: testovací metoda uvnitř coding loopu, bez vlastní spec gate, zpětného volání routeru, Git zápisů nebo live akceptace.

## Projektový podklad, nikoli kopírovaný software

Lokálně přečíst návrh `agora-manus-adaptation/aipt-tdd-coding-loop-navrh.md` a jeho `skill-build-contract.md` z 2026-11-14. Jako kontext načíst živé AIPT `AGENTS.md`, `README.md`, `docs/principles.md`, `docs/project-status.md`, `docs/decisions/effective-index.md`, `docs/milestone-3-spec.md`, `contracts/offline-replay-v1.md` a `TODO.md` (přístup 2026-11-14). Build-contract a návrh uvádějí projektovou revizi `04772f3cdee2a0fe8e6560e8ee1799fed8ac44cb`; v tomto úkolu nebyla nezávisle ověřena Git příkazem.

Nekopírovat AIPT kód, fixture ani historická data; neodvozovat reuse licenci z tohoto skillu a neměnit chybějící projektovou licenci. Jediné uložené místo AIPT adapteru ponechat v `aipt-project-workflow/references/project-context.md`; zde ponechat pouze obecnou testovací metodu a pokyny k načtení živého kontextu. Dated podklad nepovažovat za trvalý runtime důkaz ani nové oprávnění.

Strukturální validaci balíčku odlišit od použití skillu, importu, testové/runtime správnosti, review a produktové akceptace. Návrhové scénáře v SKILL.md označit **NEPROVEDENÉ**; jejich uvedení není provedení ani autorizace implementace.

## Zpřesnění po uživatelském auditu — 2026-11-14

Omezit stdlib-only policy na AIPT podle jeho aktuálních pravidel; ostatní Python projekty řídit jejich existujícími konvencemi a toolingem. Zachovat metodu tohoto skillu se stdlib unittest, zákaz zavádění nových závislostí jen kvůli TDD a předání odlišné předepsané metody bez vynucené migrace. Tato změna upravuje instrukce; není runtime zkouškou, importem ani změnou projektového kódu.
