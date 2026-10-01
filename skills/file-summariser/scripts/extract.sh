#!/usr/bin/env bash

set -euo pipefail

readonly SCRIPT_NAME="$(basename "$0")"

print_usage() {
    cat >&2 <<EOF
Usage: ${SCRIPT_NAME} <file> <symbol-or-pattern>

Print a one-line file outline followed by the first matching declaration or block.
The pattern is interpreted as an extended regular expression.
EOF
}

fail() {
    echo "[ERROR] $*" >&2
    exit 1
}

if [[ "$#" -ne 2 ]]; then
    print_usage
    exit 2
fi

readonly FILE_PATH="$1"
readonly PATTERN="$2"

[[ -n "${PATTERN}" ]] || fail 'The symbol or pattern must not be empty.'
[[ -f "${FILE_PATH}" ]] || fail "File not found: ${FILE_PATH}"
[[ -r "${FILE_PATH}" ]] || fail "File is not readable: ${FILE_PATH}"

readonly LINE_COUNT="$(wc -l < "${FILE_PATH}")"
readonly BYTE_COUNT="$(wc -c < "${FILE_PATH}")"
printf 'File: %s | lines: %s | bytes: %s\n' "${FILE_PATH}" "${LINE_COUNT}" "${BYTE_COUNT}"

if ! grep -q -E -- "${PATTERN}" "${FILE_PATH}"; then
    fail "Pattern not found: ${PATTERN}"
fi

awk -v pattern="${PATTERN}" '
    function indentation(line) {
        match(line, /^[[:space:]]*/)
        return RLENGTH
    }

    function brace_delta(line,    opening, closing) {
        opening = gsub(/\{/, "", line)
        closing = gsub(/\}/, "", line)
        return opening - closing
    }

    BEGIN {
        matched = 0
        in_block = 0
        brace_depth = 0
        base_indent = -1
    }

    {
        if (!matched) {
            if ($0 ~ pattern) {
                matched = 1
                start_line = NR
                base_indent = indentation($0)
                brace_depth = brace_delta($0)
                in_block = (brace_depth > 0)
                print $0

                if (!in_block) {
                    next
                }
            }
            next
        }

        current_indent = indentation($0)

        if (in_block) {
            print $0
            brace_depth += brace_delta($0)
            if (brace_depth <= 0) {
                exit
            }
            next
        }

        if ($0 ~ /^[[:space:]]*$/) {
            print $0
            next
        }

        if (current_indent > base_indent) {
            print $0
            next
        }

        exit
    }

    END {
        if (!matched) {
            exit 1
        }
    }
' "${FILE_PATH}"
