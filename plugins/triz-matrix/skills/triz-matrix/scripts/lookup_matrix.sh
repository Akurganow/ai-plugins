#!/bin/sh
# TRIZ Matrix Skill — Contradiction Matrix Lookup
# Looks up recommended inventive principles for a given parameter pair
#
# Usage:
#   ./lookup_matrix.sh --improve 9 --worsen 27
#   ./lookup_matrix.sh --improve 9 --worsen 27 --json

set -e

if ! command -v jq >/dev/null 2>&1; then
  echo "Error: jq is required. Install: brew install jq (macOS) or apt-get install jq (Linux)"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REF_DIR="$SCRIPT_DIR/../references"
MATRIX_FILE="$REF_DIR/matrix_data.json"

usage() {
  echo "Usage: $0 --improve <N> --worsen <N> [--json]"
  echo ""
  echo "Options:"
  echo "  --improve <N>  Parameter number (1-39) being improved"
  echo "  --worsen <N>   Parameter number (1-39) being worsened"
  echo "  --json         Output as JSON"
  echo ""
  echo "Example:"
  echo "  $0 --improve 9 --worsen 27"
  echo "  → Looks up: improving Speed worsens Reliability"
  exit 1
}

IMPROVE=""
WORSEN=""
JSON_OUT=false

while [ $# -gt 0 ]; do
  case "$1" in
    --improve) IMPROVE="$2"; shift 2 ;;
    --worsen)  WORSEN="$2"; shift 2 ;;
    --json)    JSON_OUT=true; shift ;;
    --help|-h) usage ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

[ -z "$IMPROVE" ] || [ -z "$WORSEN" ] && usage

# Validate numeric input
case "$IMPROVE" in
  ''|*[!0-9]*) echo "Error: --improve must be a number (1-39), got: '$IMPROVE'"; exit 1 ;;
esac
case "$WORSEN" in
  ''|*[!0-9]*) echo "Error: --worsen must be a number (1-39), got: '$WORSEN'"; exit 1 ;;
esac

# Validate range
if [ "$IMPROVE" -lt 1 ] || [ "$IMPROVE" -gt 39 ] || [ "$WORSEN" -lt 1 ] || [ "$WORSEN" -gt 39 ]; then
  echo "Error: Parameter numbers must be between 1 and 39"
  exit 1
fi

if [ "$IMPROVE" = "$WORSEN" ]; then
  echo "Error: Improving and worsening parameters must be different"
  exit 1
fi

# Look up the matrix cell
RESULT=$(jq --arg imp "$IMPROVE" --arg wor "$WORSEN" '
  .matrix[$imp][$wor] // empty
' "$MATRIX_FILE" 2>/dev/null)

# Get parameter names
IMP_NAME=$(jq -r --arg n "$IMPROVE" '.parameter_map[$n] // "Unknown"' "$MATRIX_FILE")
WOR_NAME=$(jq -r --arg n "$WORSEN" '.parameter_map[$n] // "Unknown"' "$MATRIX_FILE")

if [ "$JSON_OUT" = true ]; then
  if [ -z "$RESULT" ]; then
    jq -n --arg imp "$IMPROVE" --arg wor "$WORSEN" \
          --arg imp_name "$IMP_NAME" --arg wor_name "$WOR_NAME" \
      '{
        improving: {number: ($imp|tonumber), name: $imp_name},
        worsening: {number: ($wor|tonumber), name: $wor_name},
        principles: [],
        note: "No principles recommended for this pair — the matrix cell is empty"
      }'
  else
    jq -n --arg imp "$IMPROVE" --arg wor "$WORSEN" \
          --arg imp_name "$IMP_NAME" --arg wor_name "$WOR_NAME" \
          --argjson principles "$RESULT" \
      '{
        improving: {number: ($imp|tonumber), name: $imp_name},
        worsening: {number: ($wor|tonumber), name: $wor_name},
        principles: $principles
      }'
  fi
else
  echo "=== Contradiction Matrix Lookup ==="
  echo ""
  echo "  Improving: #$IMPROVE $IMP_NAME"
  echo "  Worsening: #$WORSEN $WOR_NAME"
  echo ""

  if [ -z "$RESULT" ]; then
    echo "  No principles recommended for this parameter pair."
    echo "  The matrix cell is empty — try reformulating the contradiction"
    echo "  or use physical contradiction analysis instead."
  else
    echo "  Recommended principles: $(echo "$RESULT" | jq -r 'join(", ")')"
    echo ""
    echo "  Look up these principles in the 40 Principles list in SKILL.md"
  fi
fi
