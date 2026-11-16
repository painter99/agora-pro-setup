# Provenience a rozsah adaptace

Vytvořeno 2026-11-14 jako český Manus derivát `mobile-code-review`.

## Licencovaný výchozí zdroj

- Repozitář: `painter99/agora-pro-setup`.
- Zdroj: `skills/android-development/android-code-review/SKILL.md`.
- Revize uvedená v build-contract: `552034846217c035ce802aad276fb826d0aaedf4`.
- Přečten lokální zdroj; revize nebyla znovu ověřována sítí ani Git operací.
- Zachovat upstream MIT notice `Copyright (c) 2026 Pavel Mareš`; celé znění licence je beze změny v [LICENSE.txt](../LICENSE.txt).
- Upstream skill sám uvádí adaptaci z `addyosmani/agent-skills/skills/code-review-and-quality` (v1.0, nikoli verbatim copy). Jde o převzatou informaci o původu; tento další zdroj nebyl samostatně načten ani ověřen.

## Projektové a metodické podklady

Přečteny `skill-build-contract.md`, `aipt-tdd-coding-loop-navrh.md`, `skill-creator/SKILL.md` a jeho workflow/output patterns. Konkrétní příklady review a hranice jsou dány těmito podklady; nevytvářet novou projektovou policy.

AIPT podklady přečtené 2026-11-14: `AGENTS.md`, `README.md`, `docs/principles.md`, `docs/project-status.md`, `docs/decisions/effective-index.md`, `docs/milestone-3-spec.md`, `contracts/offline-replay-v1.md`, `TODO.md`. Návrh/build-contract uvádějí revizi `04772f3cdee2a0fe8e6560e8ee1799fed8ac44cb`; tento build ji nezávisle znovu neověřoval. Živý stav musí ověřit každé budoucí použití.

AIPT slouží jen jako projektový kontext, nikoli licence pro copied code. Nekopírovat jeho kód, data, historii ani úplný adapter; AIPT chybějící licenci tímto derivátem neměnit. Jediný uložený projektový adapter má patřit `aipt-project-workflow/references/project-context.md`, mimo tento balíček.

## Hlavní změny proti originálu

Zachovat pět os, standard zlepšení code health, posouzení velikosti a konkrétní strukturální remedy. Odstranit Android/Kotlin/Compose specifika, pevné dependencies a automatickou merge gate. Zavést read-only review finálního snapshotu bez editů, testových side effects, delegace a získávání permissions; ponechat jedinou spec gate v coding loopu.

Rozlišit qualified fresh-context reviewer, advisory checker a `UNREVIEWED`; navázat závěr na úplný touched file set, diff, test evidence a snapshot identity. Nepovažovat chybějící pokrytí za „clean“. Pro AIPT přidat evidence fidelity, reproducibility a privacy, čtyři odlišné evidence/acceptance hranice a přesnou determinističnost sémantického obsahu bez falešné byte-identity celého bundle.

Použít jednosměrnou kompozici podle přesných katalogových jmen, bez rekurzivního spuštění routeru, hardcoded model routes či instalací podmíněných cest. Netvrdit import, runtime ověření, produktovou akceptaci ani nová oprávnění. Licence se vztahuje k tomuto derivátu; jeho notice zachovat při dalším šíření.
