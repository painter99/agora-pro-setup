# Původ routeru a licence

## Agora glue derivát

Nový český projektový rozcestník pro Manus vytvořit jako glue adaptaci metod z `painter99/agora-pro-setup`, zejména `skills/coding/coding-loop/SKILL.md`, upstream revize **`552034846217c035ce802aad276fb826d0aaedf4`** dle build-contractu. Původní lokální skill a upstream `LICENSE` byly přečteny 2026-11-14; uvedená upstream revize nebyla při této tvorbě nově síťově ověřena. Zachovat úplný původní MIT notice `Copyright (c) 2026 Pavel Mareš`; přiložený `LICENSE.txt` je nezměněná bajtová kopie upstream `LICENSE`.

Oproti původnímu coding loopu **neimplementovat další loop ani spec gate**: pouze klasifikovat zadání, načíst datovanou projektovou referenci a předat odpovědnost jedinému `mobile-coding-loop`, přímé spec/test/review metodě či odpovídajícímu nativnímu workflow. Rozlišit development coding loop a produktový `ResearchLoop`; nahradit instalační/Agora kernel předpoklady aktuálním katalogem a platform permissions. Neimportovat dependencies, nekopírovat soukromé instance/model policy a nevynucovat Android stack.

## Přečtená kompozice a projektové podklady

Při sestavení byly celé přečteny finální `mobile-spec-first`, `mobile-python-tdd`, `mobile-code-review`, `mobile-coding-loop` a existující `mobile-project-reasoning`, `mobile-github-release-workflow` (jejich SKILL.md, 2026-11-14). Jejich obsah nebyl upraven. Zápis na disku a přečtení není import, instalace ani automatická dostupnost v jiné relaci.

Pracovní `skill-build-contract.md` a `aipt-tdd-coding-loop-navrh.md` jsou brief/návrh adaptace, nikoli nové permissions. Navigační projektové podklady a jejich úroveň evidence jsou uvedeny pouze v [project-context.md](project-context.md); revize AIPT je převzata z briefu/návrhu, ne z nového Git či remote ověření tohoto autora.

AIPT použít jako projektový kontext, **nikoli licenční zdroj pro copied code/data**. Nepřevzít jeho kód, ledger, historické provozní záznamy ani private data. MIT routeru nelicencuje AIPT; jeho chybějící projektovou licenci neřešit a repo docs nepřepisovat. Adapter ukládat pouze zde, ne do core skills nebo průvodce.

## Rozsah ověření

Skill byl inicializován předepsaným `init_skill.py`; generovaná šablona byla celá přečtena před nahrazením a nepoužité examples byly odstraněny. Výsledek skutečné strukturální validace a doplňkových statických kontrol uvést odděleně v průvodci/delivery. Strukturální PASS neprokazuje chování po importu.

Akceptační scénáře v [acceptance-scenarios.md](acceptance-scenarios.md), ruční import, runtime použití sady, review dispatch a projektové testy/akceptace: **NEPROVEDENÉ** v této tvorbě. Bez sítě, další delegace, Git zápisů a změn AIPT nebo Agora zdrojů. Provenance ani licence nepřidělují práva.
