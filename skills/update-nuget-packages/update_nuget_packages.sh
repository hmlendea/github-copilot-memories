#!/usr/bin/env bash
# update-nuget-packages: update every PackageReference in a .NET solution or
# project to the latest version, with optional test baselines and validation.
#
# Usage:
#   update_nuget_packages.sh <target> [--skip-baseline] [--skip-tests] [--dry-run]
#
# Arguments:
#   <target>          Path to a .sln, .slnx, or .csproj file. Required.
#
# Options:
#   --skip-baseline   Skip the pre-update test baseline.
#   --skip-tests      Skip all test runs (baseline and final validation).
#   --dry-run         List packages that would be updated without changing files.
#
# Exit codes:
#   0  success
#   1  usage error
#   2  baseline failed (no changes made)
#   3  a package update failed and could not be resolved safely
#   4  final validation failed

set -euo pipefail

usage() {
  printf '%s\n' \
    "Usage: $0 <target.sln|target.slnx|target.csproj> [options]" \
    "" \
    "Options:" \
    "  --skip-baseline   Skip the pre-update test baseline." \
    "  --skip-tests      Skip all test runs (baseline and final validation)." \
    "  --dry-run         List packages that would be updated without changing files." \
    "  -h, --help        Show this help."
  exit 1
}

die() {
  printf 'ERROR: %s\n' "$1" >&2
  exit "${2:-1}"
}

log() { printf '%s\n' "$*"; }

TARGET=""
SKIP_BASELINE=0
SKIP_TESTS=0
DRY_RUN=0

while [ $# -gt 0 ]; do
  case "$1" in
    --skip-baseline) SKIP_BASELINE=1 ;;
    --skip-tests) SKIP_TESTS=1 ;;
    --dry-run) DRY_RUN=1 ;;
    -h|--help) usage ;;
    -*) die "unknown option: $1" 1 ;;
    *) [ -z "$TARGET" ] || die "multiple targets given" 1; TARGET=$1 ;;
  esac
  shift
done

[ -n "$TARGET" ] || usage
[ -f "$TARGET" ] || die "target not found: $TARGET"

if ! command -v dotnet >/dev/null 2>&1; then
  die "dotnet CLI not found" 1
fi

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$REPO_ROOT"

case "$TARGET" in
  *.sln|*.slnx) MODE=solution ;;
  *.csproj) MODE=project ;;
  *) die "unsupported target type: $TARGET (expected .sln, .slnx, or .csproj)" 1 ;;
esac

# --- enumerate projects ------------------------------------------------------
if [ "$MODE" = solution ]; then
  mapfile -t PROJECTS < <(dotnet sln "$TARGET" list | grep -E '\.csproj$')
  [ ${#PROJECTS[@]} -gt 0 ] || die "solution contains no projects: $TARGET"
else
  PROJECTS=("$TARGET")
fi

# --- detect test projects --------------------------------------------------
is_test_project() {
  local proj=$1
  local dir
  grep -Eqi 'Microsoft\.(NET\.Test\.Sdk|NETTestSdk)|xunit|nunit|NUnit3TestAdapter|MSTest|MSTest\.TestFramework|coverlet' "$proj" && return 0
  dir=$(dirname "$proj")
  find "$dir" -maxdepth 3 -type f \( -name '*Tests.cs' -o -name '*Test.cs' \) \
    -not -path '*/bin/*' -not -path '*/obj/*' 2>/dev/null | grep -q . && return 0
  return 1
}

TEST_PROJECTS=()
for p in "${PROJECTS[@]}"; do
  is_test_project "$p" && TEST_PROJECTS+=("$p")
done

HAS_TEST_PROJECTS=0
[ ${#TEST_PROJECTS[@]} -gt 0 ] && HAS_TEST_PROJECTS=1

# --- test baseline -------------------------------------------------------------
BASELINE_STATUS="skipped (no test projects)"
if [ "$SKIP_TESTS" -eq 1 ]; then
  BASELINE_STATUS="skipped (--skip-tests)"
  log "SKIPPED: tests skipped by flag"
elif [ "$SKIP_BASELINE" -eq 1 ]; then
  BASELINE_STATUS="skipped (--skip-baseline)"
  log "SKIPPED: baseline skipped by flag"
elif [ "$HAS_TEST_PROJECTS" -eq 1 ]; then
  log "BASELINE: dotnet test $TARGET"
  if ! dotnet test "$TARGET"; then
    die "test baseline failed; aborting without changes" 2
  fi
  BASELINE_STATUS="passed"
else
  log "SKIPPED: no test projects detected; baseline skipped"
fi

# --- update every project ----------------------------------------------------
total_updated=0
declare -a REPORT=()

for PROJ in "${PROJECTS[@]}"; do
  log "--- $PROJ ---"
  mapfile -t PACKAGES < <(
    grep -oP '<PackageReference\s+Include="\K[^"]+' "$PROJ" | sort -u
  )

  if [ ${#PACKAGES[@]} -eq 0 ]; then
    log "no explicit PackageReference entries"
    continue
  fi

  for PKG in "${PACKAGES[@]}"; do
    if [ "$DRY_RUN" -eq 1 ]; then
      log "WOULD UPDATE: $PKG in $PROJ"
      REPORT+=("WOULD UPDATE: $PROJ: $PKG")
      continue
    fi

    log "UPDATE: $PKG in $PROJ"
    if ! dotnet add "$PROJ" package "$PKG"; then
      log "FAILED: $PKG in $PROJ"
      exit 3
    fi
    total_updated=$((total_updated + 1))
    REPORT+=("UPDATED: $PROJ: $PKG")
  done
done

if [ "$DRY_RUN" -eq 1 ]; then
  log ""
  log "==== SUMMARY (DRY RUN; no changes written) ===="
  log "Target:            $TARGET"
  log "Projects:          ${#PROJECTS[@]}"
  if [ ${#REPORT[@]} -gt 0 ]; then
    for line in "${REPORT[@]}"; do
      log "  - $line"
    done
  fi
  exit 0
fi

# --- validate ----------------------------------------------------------------
log "RESTORE: dotnet restore $TARGET"
if ! dotnet restore "$TARGET"; then
  die "restore failed after updates" 4
fi

FINAL_STATUS="skipped"
if [ "$SKIP_TESTS" -eq 1 ]; then
  log "SKIPPED: tests skipped by flag"
elif [ "$HAS_TEST_PROJECTS" -eq 0 ]; then
  log "SKIPPED: no test projects detected; final validation skipped"
else
  log "FINAL: dotnet test $TARGET"
  if ! dotnet test "$TARGET"; then
    log "FINAL TESTS FAILED; classify each failure and repair production code or tests as appropriate"
    exit 4
  fi
  FINAL_STATUS="passed"
fi

# --- report ------------------------------------------------------------------
log ""
log "==== SUMMARY ===="
log "Target:            $TARGET"
log "Projects:          ${#PROJECTS[@]}"
log "Packages updated:  $total_updated"
log "Test baseline:     $BASELINE_STATUS"
log "Final test run:    $FINAL_STATUS"
if [ ${#REPORT[@]} -gt 0 ]; then
  for line in "${REPORT[@]}"; do
    log "  - $line"
  done
fi
log ""
log "Next: review 'git diff' for unintended changes, downgrades, duplicate references, leaked credentials, or generated artifacts."
