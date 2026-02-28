#!/bin/bash
# Bankr CLI helper script

# Check if bankr is installed
check_bankr() {
  if ! command -v bankr &> /dev/null; then
    echo "Bankr CLI not found. Install with:"
    echo "  bun install -g @bankr/cli"
    echo "  or"
    echo "  npm install -g @bankr/cli"
    return 1
  fi
  return 0
}

# Get balance summary
get_balance() {
  check_bankr || return 1
  bankr prompt "Show my portfolio balance summary" --json
}

# Quick trade
quick_trade() {
  check_bankr || return 1
  local amount=$1
  local from=$2
  local to=$3
  bankr prompt "Swap $amount $from for $to" --json
}

# Check if logged in
check_auth() {
  check_bankr || return 1
  bankr whoami
}

# Main
case "$1" in
  balance)
    get_balance
    ;;
  trade)
    quick_trade "$2" "$3" "$4"
    ;;
  check)
    check_auth
    ;;
  *)
    echo "Usage: $0 {balance|trade <amount> <from> <to>|check}"
    exit 1
    ;;
esac
