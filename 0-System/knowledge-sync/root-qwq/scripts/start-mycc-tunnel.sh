#!/bin/bash
# Start MyCC Cloudflared Tunnel

CONFIG="/root/.mycc/current.json"
LOGFILE="/tmp/cloudflared-mycc.log"
PIDFILE="/tmp/cloudflared-mycc.pid"

if [[ ! -f "$CONFIG" ]]; then
    echo "Error: $CONFIG not found"
    exit 1
fi

TOKEN=$(jq -r '.routeToken' "$CONFIG")
echo "Starting cloudflared tunnel with token: $TOKEN"

# Kill old process
if [[ -f "$PIDFILE" ]]; then
    kill $(cat "$PIDFILE") 2>/dev/null
    rm -f "$PIDFILE"
fi

# Start tunnel
nohup cloudflared tunnel --url http://localhost:18080 --token "$TOKEN" > "$LOGFILE" 2>&1 &
PID=$!
echo $PID > "$PIDFILE"
echo "Started cloudflared (PID: $PID)"

sleep 3
if kill -0 $PID 2>/dev/null; then
    echo "Tunnel running. Log tail:"
    tail -5 "$LOGFILE"
else
    echo "Failed to start. Log:"
    cat "$LOGFILE"
fi
