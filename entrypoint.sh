#!/bin/bash

# Trap signals and forward to child processes
trap 'kill -TERM $MCP_PID $API_PID 2>/dev/null; wait $MCP_PID $API_PID' SIGTERM SIGINT

# Start the first process
uv run mcp_server.py &
MCP_PID=$!
i=1
max_attempts=30
ready=false

while [ "$i" -le "$max_attempts" ]; do
    if timeout 1 bash -c "echo > /dev/tcp/127.0.0.1/8001" 2>/dev/null; then
        ready=true
        break
    fi

    i=$((i + 1))
    sleep 1
done

if [ "$ready" = false ]; then
    echo "Error: localhost:8001 did not become ready"
    exit 1
fi

# Start the second process
uv run fastapi run &
API_PID=$!

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?