#!/bin/bash
# CC Clash Tunnel - PM2 Compatible Version

PIDFILE="/tmp/cc-clash-tunnel.pid"
LOGFILE="/tmp/cc-clash-tunnel.log"

# Clear old log on start
> "$LOGFILE"

log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOGFILE"; }

stop_tunnel() {
    if [ -f "$PIDFILE" ]; then
        PID=$(cat "$PIDFILE")
        kill "$PID" 2>/dev/null
        rm -f "$PIDFILE"
        log "Stopped old tunnel (PID: $PID)"
    fi
    pkill -f "ssh -N -D 7890.*CC" 2>/dev/null
    sleep 1
}

start_tunnel() {
    # Check if already running and healthy
    if [ -f "$PIDFILE" ]; then
        PID=$(cat "$PIDFILE")
        if kill -0 "$PID" 2>/dev/null; then
            if curl -s --socks5-hostname localhost:7890 --connect-timeout 2 https://api.ip.sb/ip >/dev/null 2>&1; then
                log "Tunnel already running and healthy"
                # For PM2: keep running in foreground
                wait "$PID"
                return 0
            fi
        fi
    fi

    stop_tunnel

    log "Starting SSH tunnel to CC..."

    # PM2 compatible: start ssh in background, save PID, then wait
    ssh -N \
        -D 7890 \
        -o ServerAliveInterval=15 \
        -o ServerAliveCountMax=2 \
        -o ExitOnForwardFailure=yes \
        CC >> "$LOGFILE" 2>&1 &
    PID=$!
    echo $PID > "$PIDFILE"
    log "Tunnel started (PID: $PID)"

    # Wait for the SSH process (keeps PM2 happy)
    wait $PID
    EXIT_CODE=$?
    log "Tunnel exited with code: $EXIT_CODE"
    rm -f "$PIDFILE"
    exit $EXIT_CODE
}

case "${1:-start}" in
    start) start_tunnel ;;
    stop) stop_tunnel; log "Tunnel stopped" ;;
    restart) stop_tunnel; sleep 1; start_tunnel ;;
    status)
        if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
            if curl -s --socks5-hostname localhost:7890 --connect-timeout 2 https://api.ip.sb/ip 2>/dev/null; then
                log "✅ Healthy"
                exit 0
            else
                log "⚠️ Running but not working"
                exit 1
            fi
        else
            log "❌ Not running"
            exit 1
        fi
        ;;
    *) echo "Usage: $0 {start|stop|restart|status}"; exit 1 ;;
esac
