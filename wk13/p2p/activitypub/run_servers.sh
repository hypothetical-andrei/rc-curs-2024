#!/bin/bash
# Start server A on port 9001
BASE_URL=http://localhost:9001 python3 -c "import server; server.start_server('http://localhost:9001', 9001)" &
# Start server B on port 9002
BASE_URL=http://localhost:9002 python3 -c "import server; server.start_server('http://localhost:9002', 9002)" &
