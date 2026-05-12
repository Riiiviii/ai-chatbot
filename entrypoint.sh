#!/bin/bash

# Start the first process
uv run mcp_server.py &
sleep 2

# Start the second process
uv run fastapi run &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?