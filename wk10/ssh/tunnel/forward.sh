#!/bin/bash

# --- Configuration ---
LOCAL_PORT=9000           # Local port to bind
REMOTE_PORT=8000          # Remote port where nc is listening
SSH_USER=root
SSH_HOST=xp.nextlab.tech

# --- Setup ---
echo "[*] Setting up SSH tunnel: localhost:$LOCAL_PORT → $SSH_HOST:$REMOTE_PORT"
echo "[*] SSHing into $SSH_USER@$SSH_HOST"

# Create SSH tunnel in background
ssh -N -L ${LOCAL_PORT}:localhost:${REMOTE_PORT} ${SSH_USER}@${SSH_HOST} &
TUNNEL_PID=$!

# Allow tunnel to establish
sleep 2

# Test the tunnel with netcat
echo "[*] Testing tunnel with: echo 'hello' | nc localhost $LOCAL_PORT"
echo "hello from tunnel" | nc localhost ${LOCAL_PORT}

# Leave the tunnel running until Ctrl+C
echo "[*] Tunnel is active. Press Ctrl+C to close it."
trap "echo; echo '[*] Killing tunnel...'; kill $TUNNEL_PID" SIGINT
wait $TUNNEL_PID
