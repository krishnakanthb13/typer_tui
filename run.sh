#!/bin/bash

# Typer TUI Launcher for Unix/macOS

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}========================================================${NC}"
echo -e "${YELLOW}  Typer TUI Launcher${NC}"
echo -e "${YELLOW}========================================================${NC}"

# 1. Check for Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python 3 is not installed or not in PATH.${NC}"
    exit 1
fi

# 2. Priority Check: Global Dependencies
if python3 -c "import textual" &> /dev/null; then
    echo -e "${GREEN}[INFO] Dependencies found globally. Skipping virtual environment.${NC}"
else
    # 3. Fallback to Virtual Environment
    if [ -d "venv" ]; then
        echo -e "${GREEN}[INFO] Dependencies missing globally. Activating venv...${NC}"
        source venv/bin/activate
    else
        echo -e "${YELLOW}[INFO] No 'venv' found and global deps missing.${NC}"
    fi
fi

# 4. Final Dependency Check & Install
if ! python3 -c "import textual" &> /dev/null; then
    echo -e "${YELLOW}[WARNING] Dependency 'textual' not found.${NC}"
    if [ -f "requirements.txt" ]; then
        echo -e "${GREEN}[INFO] Installing dependencies from requirements.txt...${NC}"
        python3 -m pip install -r requirements.txt
        if [ $? -ne 0 ]; then
             echo -e "${RED}[ERROR] Failed to install dependencies.${NC}"
             exit 1
        fi
    else
        echo -e "${RED}[ERROR] requirements.txt missing.${NC}"
        exit 1
    fi
fi

# 5. Launch Application
echo -e "${GREEN}[INFO] Starting application...${NC}"
echo "--------------------------------------------------------"

trap "echo; echo 'Interrupted'; exit" SIGINT

python3 main.py
EXIT_CODE=$?

echo "--------------------------------------------------------"
if [ $EXIT_CODE -ne 0 ]; then
    echo -e "${RED}[ERROR] Application exited with code $EXIT_CODE${NC}"
    read -p "Press Enter to exit..."
else
    echo -e "${GREEN}[SUCCESS] Application exited gracefully.${NC}"
fi
