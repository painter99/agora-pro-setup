# Provenance — mobile-spec-first

## Původ a licence

Český metodický derivát Agora skillu `android-spec-first`. Přečtený původní zdroj: `skills/android-development/android-spec-first/SKILL.md` v repozitáři `agora-pro-setup`, revize dle build-contract `552034846217c035ce802aad276fb826d0aaedf4`; datum čtení 2026-11-14. Zachovat původní MIT notice `Copyright (c) 2026 Pavel Mareš`; soubor [LICENSE.txt](../LICENSE.txt) je nezměněná kopie licence Agora repozitáře.

Původní skill uvádí v1.0 a metodickou adaptaci z `addyosmani/agent-skills/skills/spec-driven-development`. Jde o převzatý údaj z jeho sekce Sources, nikoli zde provedené externí ověření či přímé kopírování dalšího upstream zdroje.

## Rozdíly adaptace

Zachovat assumptions-first, šest oblastí specifikace, pozorovatelná acceptance kritéria a ochranu non-goals. Nahradit Android/Kotlin/Gradle specifika obecnou metodou odvozenou od aktuálního projektu. Přidat krátkou kartu pro jednoznačné změny, přímou spec-only cestu, rozlišení připravenosti a autorizace a task-local načtení živých podkladů bez rekurzivního routeru.

Odstranit vlastní fáze IMPLEMENT a čtyři schvalovací gate, automatické směrování do Android TDD/review a implicitní souhlas mlčením. Jedinou spec gate ponechat `mobile-coding-loop`; tento skill dodává tvar kontraktu a nepřebírá řízení, implementaci ani oprávnění. Rozlišovat software evidence, sémantickou podporu a přijetí operátorem.

## Projektový podklad a omezení

Přečíst lokální návrh `aipt-tdd-coding-loop-navrh.md` a celý `skill-build-contract.md` ze složky `agora-manus-adaptation`, dále živé AIPT `AGENTS.md`, `README.md`, `docs/principles.md`, `docs/project-status.md`, `docs/decisions/effective-index.md`, `docs/milestone-3-spec.md`, `contracts/offline-replay-v1.md` a `TODO.md`; čtení 2026-11-14. Kontextový návrh a build-contract uvádějí AIPT revizi `04772f3cdee2a0fe8e6560e8ee1799fed8ac44cb`; nejde o zde nově ověřený remote stav.

AIPT slouží pouze jako projektový podklad pro požadavky a příklad acceptance kritéria. Nekopírovat jeho kód ani data; MIT tohoto derivátu neposkytuje licenci pro AIPT a nemění jeho chybějící licenci. Neuchovávat zde projektový snapshot: jediný uložený adapter patří do `aipt-project-workflow/references/project-context.md`, při použití vždy ověřit relevantní živé zdroje.

Použít `skill-creator` a jeho vzory workflows/output-patterns pro inicializaci, strukturu a výstup. Strukturální kontrolu oddělit od použití skillu; návrhové scénáře v SKILL.md zůstávají **NEPROVEDENÉ**. Netvrdit import, instalaci, runtime správnost ani provedenou AIPT implementaci.
