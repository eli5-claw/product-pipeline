#!/bin/bash
# Coinbase Agentic Wallet helper script

# Check if awal is available
check_awal() {
  if ! command -v npx &> /dev/null; then
    echo "npm/npx not found. Install Node.js first."
    return 1
  fi
  return 0
}

# Get wallet status
get_status() {
  check_awal || return 1
  npx awal status
}

# Quick send
quick_send() {
  check_awal || return 1
  local amount=$1
  local recipient=$2
  npx awal send "$amount" "$recipient"
}

# Quick trade
quick_trade() {
  check_awal || return 1
  local amount=$1
  local from=$2
  local to=$3
  npx awal trade "$amount" "$from" "$to"
}

# Fund wallet
fund_wallet() {
  check_awal || return 1
  npx awal fund
}

# Search x402 services
search_service() {
  check_awal || return 1
  local query=$1
  npx awal search "$query"
}

# Main
case "$1" in
  status)
    get_status
    ;;
  send)
    quick_send "$2" "$3"
    ;;
  trade)
    quick_trade "$2" "$3" "$4"
    ;;
  fund)
    fund_wallet
    ;;
  search)
    search_service "$2"
    ;;
  *)
    echo "Usage: $0 {status|send <amount> <recipient>|trade <amount> <from> <to>|fund|search <query>}"
    exit 1
    ;;
esac
