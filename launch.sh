#!/bin/bash

# Start the Flask server in the background
python server.py &
SERVER_PID=$!  # Save the process ID

# Give the server a moment to start up (adjust time if needed)
sleep 3

# Open webpage based on OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open http://localhost:15733
elif [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:15733
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    start http://localhost:15733
fi

# Optional: Wait for the server process to keep script alive
# (Remove this line if you want the script to exit immediately after opening the browser)
wait $SERVER_PID