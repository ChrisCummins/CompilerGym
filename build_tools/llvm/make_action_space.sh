#!/usr/bin/env bash
#
# Usage: run.sh <llvm-src-root> <outdir>
#
CWD=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
set -euo pipefail

main() {
    llvm_root="$1"
    outdir="$2"

    set -x
    mkdir -p "$outdir"
    python "$CWD/extract_passes_from_sources.py" \
        --llvm_root="$llvm_root" \
        > "$outdir/passes.json"
    python "$CWD/make_action_space_sources.py" \
        --outdir="$outdir" \
        < "$outdir/passpasses.json"
}
main $@
