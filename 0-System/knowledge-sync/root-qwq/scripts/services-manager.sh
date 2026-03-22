#!/bin/bash
# AI Team Services Manager

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

show_status() {
    echo ""
    echo "╔════════════════════════════════════════════════╗"
    echo "║        AI Team Services Status                 ║"
    echo "╚════════════════════════════════════════════════╝"
    echo ""
    
    if curl -s --socks5-hostname localhost:7890 --connect-timeout 2 https://api.ip.sb/ip >/dev/null 2>&1; then
        IP=$(curl -s --socks5-hostname localhost:7890 --connect-timeout 2 https://api.ip.sb/ip)
        echo "  cc-clash-tunnel:  🟢 Running (Exit IP: $IP)"
    else
        echo "  cc-clash-tunnel:  🔴 Stopped"
    fi
    
    if pgrep -f "cc-clash-watchdog.sh" >/dev/null 2>&1; then
        echo "  cc-clash-watchdog: 🟢 Running"
    else
        echo "  cc-clash-watchdog: 🔴 Stopped"
    fi
    
    if pm2 list 2>/dev/null | grep -q "free-claude-code.*online"; then
        echo "  free-claude-code: 🟢 Running (PM2)"
    else
        echo "  free-claude-code: 🔴 Stopped"
    fi
    
    if curl -s http://localhost:8769 >/dev/null 2>&1; then
        echo "  mobile-web:       🟢 Running (8769)"
    else
        echo "  mobile-web:       🔴 Stopped"
    fi
    
    if curl -s http://localhost:18080 >/dev/null 2>&1; then
        echo "  mycc:             🟢 Running (18080)"
    else
        echo "  mycc:             🔴 Stopped"
    fi
    echo ""
}

start_all() {
    echo -e "${GREEN}Starting all services...${NC}"
    
    pkill -f "ssh -N -D 7890" 2>/dev/null || true
    pkill -f "cc-clash-watchdog" 2>/dev/null || true
    rm -f /tmp/cc-clash-tunnel.pid
    sleep 2
    
    /root/cc-clash-tunnel.sh start &
    sleep 5
    
    nohup /root/cc-clash-watchdog.sh >/dev/null 2>&1 &
    
    show_status
}

stop_all() {
    echo -e "${GREEN}Stopping all services...${NC}"
    pkill -f "cc-clash-watchdog" 2>/dev/null || true
    pkill -f "ssh -N -D 7890" 2>/dev/null || true
    rm -f /tmp/cc-clash-tunnel.pid
    sleep 2
    echo -e "${GREEN}All services stopped${NC}"
    show_status
}

case "${1:-status}" in
    start) start_all ;;
    stop) stop_all ;;
    restart) stop_all; sleep 2; start_all ;;
    status) show_status ;;
    *) echo "Usage: $0 {start|stop|restart|status}" ;;
esac
