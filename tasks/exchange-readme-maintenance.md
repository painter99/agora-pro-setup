# Task: exchange README maintenance

> Card of a live scheduled task — **not the verbatim prompt**. Operator-specific
> details are genericized into fill-in placeholders; see the
> [task cards README](README.md).

## Purpose

Keep the README of a shared file-exchange directory (the operator's only window
into the machine) in sync with its actual state: directory structure, pending
items, project directories, total size. Most runs correctly end with
"no change".

## Schedule

Daily, night (NN:NN).

## Reads

- the exchange directory tree (listing with types, timestamps, sizes)
- the exchange README itself

## Workflow

1. Clean stale README backups older than 7 days — via one fixed command, and
   nothing else.
2. Map the actual state (tree, total size).
3. Read the README.
4. Compare: directory structure vs the documented paths; pending inbox items vs
   the current-state section; project directories in the outbox; total size.
5. Nothing changed → end with "no change", write nothing.
6. Something changed → back up the README first, then edit it with exact
   in-place string replacements (never a full rewrite): refresh the
   current-state section, adjust the paths section only if a branch appeared or
   disappeared, append one history line.

## Hard rules

- The only permitted change in the exchange is editing the README.
- Never move, rename, or delete anything in the exchange; never create files
  there (backups live in a separate drafts directory).
- Backup deletion is limited to the one fixed command from step 1.
- Never write secrets, tokens, or file contents into the README — names, sizes,
  dates only.
- Unsure what a file is → describe it neutrally (name, size, date); never
  guess.
- Control/metadata directories of the exchange are off-limits.

## Delivery and notifications

- None by design: the README itself is the artifact; the operator reads it
  directly.

## Failure behavior

Report the failure factually and write nothing; never silent-fail.

## Verification

Re-read the README after the edit: the change is in place, language and
structure intact.