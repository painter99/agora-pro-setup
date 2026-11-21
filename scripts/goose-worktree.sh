#!/usr/bin/env bash
# goose-worktree.sh - worktree-based isolation for parallel Goose dispatches.
#
# Commands:
#   add <name> [base-ref]      Create <root>/<name> at base-ref (default HEAD)
#                              and print the worktree path on stdout. Refuses
#                              when the path already exists.
#   remove <name> [--force]    Remove <root>/<name>. Refuses when the worktree
#                              has uncommitted changes unless --force is given.
#   list                       List registered worktrees.
#
# Worktrees are created under GOOSE_WORKTREES_ROOT (default
# /home/agora/work/goose-worktrees). The repository root is the parent of this
# script's directory; every git call pins safe.directory to that root so the
# script also works under a Goose dispatch user.

set -euo pipefail

WORKTREES_ROOT="${GOOSE_WORKTREES_ROOT:-/home/agora/work/goose-worktrees}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

usage() {
    cat >&2 <<'USAGE'
Usage: goose-worktree.sh add <name> [base-ref]
       goose-worktree.sh remove <name> [--force]
       goose-worktree.sh list
USAGE
    exit 2
}

die() {
    echo "goose-worktree.sh: $*" >&2
    exit 1
}

# Names must be single, plain path components below the worktrees root.
valid_name() {
    case "$1" in
        ''|.|..|-*|*/*|*' '*) return 1 ;;
        *) return 0 ;;
    esac
}

# All git calls run against the repo root with safe.directory pinned.
git_repo() {
    git -c "safe.directory=${REPO_ROOT}" -C "${REPO_ROOT}" "$@"
}

# Git inside a worktree; pin safe.directory for the worktree path as well.
git_wt() {
    git -c "safe.directory=${REPO_ROOT}" -c "safe.directory=$1" -C "$1" "${@:2}"
}

cmd_add() {
    if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
        usage
    fi
    local name="$1"
    local base="${2:-HEAD}"
    local path="${WORKTREES_ROOT}/${name}"
    valid_name "$name" || die "invalid worktree name: '${name}'"
    if [ -e "$path" ]; then
        die "refusing: path already exists: ${path}"
    fi
    mkdir -p "${WORKTREES_ROOT}"
    # Keep stdout clean: the worktree path is the only stdout output of add.
    git_repo worktree add "$path" "$base" >&2
    echo "$path"
}

cmd_remove() {
    local force=0
    local name=""
    while [ "$#" -gt 0 ]; do
        case "$1" in
            --force) force=1 ;;
            -h|--help) usage ;;
            *)
                if [ -n "$name" ]; then
                    usage
                fi
                name="$1"
                ;;
        esac
        shift
    done
    if [ -z "$name" ]; then
        usage
    fi
    valid_name "$name" || die "invalid worktree name: '${name}'"
    local path="${WORKTREES_ROOT}/${name}"
    if [ ! -d "$path" ]; then
        die "no such worktree path: ${path}"
    fi
    if [ "$force" -eq 0 ]; then
        if [ -n "$(git_wt "$path" status --porcelain)" ]; then
            die "uncommitted changes in ${path}; pass --force to override"
        fi
    fi
    git_repo worktree remove "$path"
    echo "removed: ${path}"
}

cmd_list() {
    if [ "$#" -gt 0 ]; then
        usage
    fi
    git_repo worktree list
}

case "${1:-}" in
    add) shift; cmd_add "$@" ;;
    remove) shift; cmd_remove "$@" ;;
    list) shift; cmd_list "$@" ;;
    -h|--help|help) usage ;;
    *) usage ;;
esac
