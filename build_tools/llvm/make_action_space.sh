#!/usr/bin/env bash
#
# Usage: run.sh <config-py> <llvm-src-root> <outdir>
#
CWD=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
set -euo pipefail

main() {
    config_py="$1"
    llvm_root="$2"
    outdir="$3"

    set -x
    mkdir -p "$outdir"
    python "$CWD/extract_passes_from_sources.py" --llvm_root "$llvm_root" > "$outdir/passes.json"
    python "$CWD/make_action_space_sources.py" \
        --outdir "$outdir" \
        < "$outdir/filtered_passes.json"
}
main $@
