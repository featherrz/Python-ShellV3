#!/bin/bash

# 1. Environment Detection (Termux vs Standard Linux)
if [ -d "$PREFIX/bin" ]; then
    echo "Detected Termux environment..."
    BIN_DIR="$PREFIX/bin"
    DATA_DIR="$HOME/soft/shell"
    SUDO="" 
else
    echo "Detected Standard Linux environment..."
    BIN_DIR="/usr/local/bin"
    DATA_DIR="/usr/local/soft/shell"
    SUDO="sudo"
fi

# 2. Create Project Folders
echo "Creating directory at $DATA_DIR..."
$SUDO mkdir -p $DATA_DIR
$SUDO chown $USER:$USER $DATA_DIR 2>/dev/null || true

# 3. Download the Python Script
echo "Fetching shell.py from GitHub..."
curl -sL https://raw.githubusercontent.com/featherrz/Python-ShellV3/main/shell.py -o $DATA_DIR/shell.py

# 4. Create the Execution Command
# This creates a small script so you can just type 'shell'
echo "Creating system command..."
echo "#!/bin/bash
python3 $DATA_DIR/shell.py" > shell_cmd

# 5. Install the Command
$SUDO mv shell_cmd $BIN_DIR/shell
$SUDO chmod +x $BIN_DIR/shell
$SUDO chmod +x $DATA_DIR/shell.py

echo "-----------------------------------------------"
echo "Done! SoftShell v3 is installed."
echo "You can now run 'shell' from anywhere."
echo "Data folder: $DATA_DIR"
echo "-----------------------------------------------"

