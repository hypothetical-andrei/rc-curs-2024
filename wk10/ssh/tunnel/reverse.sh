#!/bin/bash

# --- Configuration ---
LOCAL_PORT=8000           # Port where netcat is running on your local machine
REMOTE_PORT=9000          # Port on remote server users will connect to
SSH_USER=root
SSH_HOST=xp.nextlab.tech

# --- Setup ---
echo "[*] Starting SSH reverse tunnel: $SSH_HOST:$REMOTE_PORT → localhost:$LOCAL_PORT"
echo "[*] SSHing into $SSH_USER@$SSH_HOST"

# Start netcat listener locally
echo "[*] Starting local netcat server on port $LOCAL_PORT..."
nc -l -p $LOCAL_PORT &
NC_PID=$!

# Create reverse SSH tunnel
ssh -N -R ${REMOTE_PORT}:localhost:${LOCAL_PORT} ${SSH_USER}@${SSH_HOST} &
TUNNEL_PID=$!

sleep 2

echo "[*] Tunnel is active. On $SSH_HOST, run: echo 'hi' | nc localhost $REMOTE_PORT"
echo "[*] Press Ctrl+C to stop everything."

# Handle Ctrl+C
trap "echo; echo '[*] Cleaning up...'; kill $TUNNEL_PID $NC_PID" SIGINT
wait $TUNNEL_PID
