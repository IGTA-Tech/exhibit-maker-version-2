# 🖥️ TERMINAL GUIDE - Visa Exhibit Maker Project
## Complete Breakdown for Working in Terminal

**Last Updated**: December 3, 2025

---

## 📍 PART 1: NAVIGATING TO THE PROJECT

### **Step 1: Open Terminal**

**Linux/Mac:**
- Press `Ctrl + Alt + T` (Linux)
- Press `Cmd + Space`, type "Terminal" (Mac)

**Windows:**
- Use WSL (Windows Subsystem for Linux)
- Or Git Bash

---

### **Step 2: Navigate to Project Directory**

```bash
# Go to the project
cd "/home/innovativeautomations/Visa Exhibit Maker"

# OR if you're starting from home directory
cd ~
cd "Visa Exhibit Maker"

# Verify you're in the right place
pwd
# Should show: /home/innovativeautomations/Visa Exhibit Maker
```

---

### **Step 3: Check Project Status**

```bash
# See what's in this directory
ls -la

# You should see:
# - streamlit-exhibit-generator/
# - google-apps-script-exhibit-generator/
# - GOOGLE_CLOUD_RUN_ENV_VARS.md
# - ENV_QUICK_REFERENCE.txt
# - README files, etc.
```

---

## 📂 PART 2: EXPLORING THE PROJECT STRUCTURE

### **View Complete Directory Structure**

```bash
# Show tree structure (if tree is installed)
tree -L 2

# OR use ls to see directories
ls -d */

# Output:
# Examples of Single PDFs/
# google-apps-script-exhibit-generator/
# streamlit-exhibit-generator/
```

---

### **Navigate to Streamlit App**

```bash
# Go to Streamlit directory
cd streamlit-exhibit-generator

# See what's inside
ls -la

# You'll see:
# - app.py (main application)
# - pdf_handler.py
# - google_drive.py
# - compress_handler.py
# - requirements.txt
# - README.md
```

---

### **View File Contents**

```bash
# View a file with cat
cat requirements.txt

# View with less (scrollable)
less README.md
# Press 'q' to quit

# View first 20 lines
head -n 20 app.py

# View last 20 lines
tail -n 20 app.py

# Search for specific text
grep -n "COMPRESSION" app.py
```

---

### **Go Back to Project Root**

```bash
# Go up one directory
cd ..

# OR go directly to project root
cd "/home/innovativeautomations/Visa Exhibit Maker"

# Check where you are
pwd
```

---

## 🔍 PART 3: GIT OPERATIONS

### **Check Git Status**

```bash
# See current branch and changes
git status

# See commit history
git log --oneline -10

# See what branch you're on
git branch

# See remote repository
git remote -v
# Output: https://github.com/IGTA-Tech/visa-exhibit-maker.git
```

---

### **Pull Latest Changes from GitHub**

```bash
# Make sure you're in the project root
cd "/home/innovativeautomations/Visa Exhibit Maker"

# Pull latest changes
git pull origin master

# If there are conflicts, you'll see them
# If clean, you'll see: Already up to date.
```

---

### **View Differences**

```bash
# See what changed in recent commits
git diff HEAD~1

# See changes in specific file
git diff app.py

# See changes between branches
git diff master origin/master
```

---

### **Clone Project (If Starting Fresh)**

```bash
# Clone the repository to a new location
git clone https://github.com/IGTA-Tech/visa-exhibit-maker.git

# Navigate into it
cd visa-exhibit-maker

# You're ready to work!
```

---

## 🐍 PART 4: PYTHON & DEPENDENCIES

### **Check Python Version**

```bash
# Check Python 3 version
python3 --version

# Should be Python 3.8 or higher
```

---

### **Create Virtual Environment (Recommended)**

```bash
# Navigate to streamlit directory
cd "/home/innovativeautomations/Visa Exhibit Maker/streamlit-exhibit-generator"

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You'll see (venv) in your prompt
# (venv) user@machine:~/Visa Exhibit Maker/streamlit-exhibit-generator$
```

---

### **Install Dependencies**

```bash
# Make sure you're in streamlit-exhibit-generator directory
cd "/home/innovativeautomations/Visa Exhibit Maker/streamlit-exhibit-generator"

# Install all requirements
pip install -r requirements.txt

# You'll see packages installing:
# - streamlit
# - PyPDF2
# - google-api-python-client
# - etc.

# Verify installations
pip list | grep streamlit
pip list | grep PyPDF2
```

---

### **Install System Dependencies**

```bash
# Install Ghostscript (for PDF compression)
sudo apt-get update
sudo apt-get install ghostscript

# Verify installation
gs --version
# Should show: GPL Ghostscript 9.50 (or higher)

# Check if gs is in PATH
which gs
# Output: /usr/bin/gs
```

---

## 🚀 PART 5: RUNNING THE APPLICATION

### **Option 1: Run Streamlit App Locally**

```bash
# Navigate to streamlit directory
cd "/home/innovativeautomations/Visa Exhibit Maker/streamlit-exhibit-generator"

# Run the app
streamlit run app.py

# You'll see output:
# You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
# Network URL: http://192.168.x.x:8501

# Open browser and go to: http://localhost:8501
```

---

### **Stop the Application**

```bash
# Press Ctrl + C in terminal

# You'll see:
# Stopping...
# ^C
```

---

### **Run with Specific Port**

```bash
# Run on custom port
streamlit run app.py --server.port 8080

# Run on specific address
streamlit run app.py --server.address 0.0.0.0 --server.port 8080
```

---

### **Run in Background**

```bash
# Run in background with nohup
nohup streamlit run app.py &

# View output
tail -f nohup.out

# Stop background process
ps aux | grep streamlit
kill <process_id>
```

---

## 📝 PART 6: WORKING WITH FILES

### **Create New Files**

```bash
# Create a new file
touch new-file.py

# Create with content
cat > test.txt << EOF
This is test content
Line 2
EOF

# Open in nano editor
nano new-file.py
# Press Ctrl+X to exit, Y to save
```

---

### **Edit Files**

```bash
# Edit with nano (simple)
nano app.py

# Edit with vim (advanced)
vim app.py
# Press 'i' to insert, 'ESC' then ':wq' to save and quit

# Edit with VS Code (if installed)
code app.py
```

---

### **Copy and Move Files**

```bash
# Copy file
cp app.py app-backup.py

# Copy directory
cp -r streamlit-exhibit-generator/ backup/

# Move/rename file
mv old-name.py new-name.py

# Remove file
rm test-file.py

# Remove directory
rm -rf test-directory/
```

---

## 🔧 PART 7: ENVIRONMENT VARIABLES

### **View Current Environment Variables**

```bash
# View all environment variables
env

# View specific variable
echo $PORT
echo $APP_ENV

# Check if variable is set
[ -z "$PORT" ] && echo "PORT not set" || echo "PORT is $PORT"
```

---

### **Set Environment Variables (Temporary)**

```bash
# Set for current session
export APP_ENV=production
export PORT=8080
export COMPRESSION_ENABLED=true

# Verify
echo $APP_ENV
# Output: production
```

---

### **Set Environment Variables (Permanent)**

```bash
# Edit bash profile
nano ~/.bashrc

# Add at the end:
export APP_ENV=production
export PORT=8080

# Save and reload
source ~/.bashrc

# Verify
echo $APP_ENV
```

---

### **Using .env File**

```bash
# Create .env file
cd "/home/innovativeautomations/Visa Exhibit Maker/streamlit-exhibit-generator"

# Create file
cat > .env << EOF
APP_ENV=production
PORT=8080
COMPRESSION_ENABLED=true
SMALLPDF_API_KEY=your-key-here
EOF

# View contents
cat .env

# Load environment variables
export $(cat .env | xargs)

# Verify
echo $APP_ENV
```

---

## 📊 PART 8: TESTING & DEBUGGING

### **Run Python Scripts Directly**

```bash
# Navigate to directory
cd "/home/innovativeautomations/Visa Exhibit Maker/streamlit-exhibit-generator"

# Run Python script
python3 compress_handler.py

# Run with verbose output
python3 -v app.py
```

---

### **Test Individual Components**

```bash
# Test compression
python3 << EOF
from compress_handler import USCISPDFCompressor
compressor = USCISPDFCompressor(quality_preset='high')
print("✓ Compression handler loaded")
EOF

# Test Google Drive
python3 << EOF
from google_drive import GoogleDriveHandler
print("✓ Google Drive handler imported")
EOF
```

---

### **Check Logs**

```bash
# View Streamlit logs
ls ~/.streamlit/logs/

# View latest log
tail -f ~/.streamlit/logs/streamlit.log

# Search logs for errors
grep -i "error" ~/.streamlit/logs/streamlit.log
```

---

## 🛠️ PART 9: COMMON WORKFLOWS

### **Workflow 1: Pull Latest Changes & Run**

```bash
# 1. Navigate to project
cd "/home/innovativeautomations/Visa Exhibit Maker"

# 2. Pull latest changes
git pull origin master

# 3. Navigate to Streamlit app
cd streamlit-exhibit-generator

# 4. Activate virtual environment
source venv/bin/activate

# 5. Update dependencies (if needed)
pip install -r requirements.txt

# 6. Run app
streamlit run app.py
```

---

### **Workflow 2: Make Changes & Push**

```bash
# 1. Navigate to project
cd "/home/innovativeautomations/Visa Exhibit Maker"

# 2. Check current status
git status

# 3. Make your changes (edit files)
nano streamlit-exhibit-generator/app.py

# 4. Check what changed
git diff

# 5. Stage changes
git add streamlit-exhibit-generator/app.py

# 6. Commit changes
git commit -m "Description of changes"

# 7. Push to GitHub
git push origin master
```

---

### **Workflow 3: Test Compression**

```bash
# 1. Navigate to streamlit directory
cd "/home/innovativeautomations/Visa Exhibit Maker/streamlit-exhibit-generator"

# 2. Check Ghostscript
gs --version

# 3. Test compression script
python3 << EOF
from compress_handler import USCISPDFCompressor

compressor = USCISPDFCompressor(quality_preset='high')

# Check Ghostscript
if compressor._check_ghostscript():
    print("✓ Ghostscript available")
else:
    print("✗ Ghostscript not found")
EOF
```

---

### **Workflow 4: Fresh Installation**

```bash
# 1. Clone repository
cd ~
git clone https://github.com/IGTA-Tech/visa-exhibit-maker.git
cd visa-exhibit-maker

# 2. Install system dependencies
sudo apt-get update
sudo apt-get install ghostscript python3-pip

# 3. Create virtual environment
cd streamlit-exhibit-generator
python3 -m venv venv
source venv/bin/activate

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Run application
streamlit run app.py
```

---

## 🔍 PART 10: SEARCHING & FINDING

### **Find Files**

```bash
# Find all Python files
find . -name "*.py"

# Find files containing specific text
grep -r "COMPRESSION" .

# Find files modified in last 7 days
find . -mtime -7

# Find large files (>10MB)
find . -size +10M
```

---

### **Search File Contents**

```bash
# Search for text in files
grep -n "def compress" compress_handler.py

# Search recursively in all files
grep -rn "SMALLPDF_API_KEY" .

# Search with context (3 lines before/after)
grep -C 3 "SUPABASE" app.py

# Case-insensitive search
grep -i "error" app.py
```

---

## 📦 PART 11: DOCKER (For Cloud Run)

### **Build Docker Image**

```bash
# Navigate to project root
cd "/home/innovativeautomations/Visa Exhibit Maker"

# Build image
docker build -t visa-exhibit-maker .

# Build with tag
docker build -t gcr.io/your-project/visa-exhibit-maker:latest .

# View built images
docker images | grep visa
```

---

### **Run Docker Container Locally**

```bash
# Run container
docker run -p 8080:8080 visa-exhibit-maker

# Run with environment variables
docker run -p 8080:8080 \
  -e APP_ENV=production \
  -e PORT=8080 \
  visa-exhibit-maker

# Run in detached mode
docker run -d -p 8080:8080 visa-exhibit-maker

# View running containers
docker ps

# Stop container
docker stop <container_id>
```

---

## 🎯 PART 12: QUICK REFERENCE COMMANDS

### **Navigation**

```bash
cd ~                              # Go to home directory
cd "Visa Exhibit Maker"           # Go to project
cd ..                             # Go up one directory
pwd                               # Print current directory
ls                                # List files
ls -la                            # List all files with details
```

---

### **File Operations**

```bash
cat filename                      # View file
less filename                     # Scrollable view
head -n 20 filename              # First 20 lines
tail -n 20 filename              # Last 20 lines
nano filename                     # Edit file
cp source dest                    # Copy file
mv source dest                    # Move/rename file
rm filename                       # Delete file
mkdir dirname                     # Create directory
```

---

### **Git Operations**

```bash
git status                        # Check status
git pull origin master           # Pull changes
git add .                        # Stage all changes
git commit -m "message"          # Commit changes
git push origin master           # Push to GitHub
git log --oneline -10            # View recent commits
git diff                         # View changes
```

---

### **Python Operations**

```bash
python3 --version                 # Check Python version
pip install -r requirements.txt   # Install dependencies
pip list                          # List installed packages
python3 script.py                 # Run Python script
streamlit run app.py             # Run Streamlit app
```

---

### **System Operations**

```bash
sudo apt-get update              # Update package list
sudo apt-get install package     # Install package
which command                    # Find command location
ps aux | grep streamlit          # Find running process
kill <pid>                       # Stop process
df -h                            # Disk space
free -h                          # Memory usage
top                              # System monitor
```

---

## 🆘 PART 13: TROUBLESHOOTING

### **Problem: Can't Find Project**

```bash
# Search for directory
find ~ -name "Visa Exhibit Maker" -type d

# OR
locate "Visa Exhibit Maker"

# OR
cd ~
ls -la | grep -i visa
```

---

### **Problem: Permission Denied**

```bash
# Check file permissions
ls -la filename

# Add execute permission
chmod +x filename

# Change ownership
sudo chown $USER:$USER filename
```

---

### **Problem: Command Not Found**

```bash
# Check if command exists
which streamlit

# If not found, install
pip install streamlit

# Add to PATH
export PATH=$PATH:/path/to/command
```

---

### **Problem: Git Conflicts**

```bash
# See conflicts
git status

# Abort merge
git merge --abort

# Force pull (WARNING: overwrites local changes)
git fetch origin
git reset --hard origin/master
```

---

### **Problem: Can't Start Streamlit**

```bash
# Check if port is in use
lsof -i :8501

# Kill process on port
kill -9 $(lsof -t -i:8501)

# Try different port
streamlit run app.py --server.port 8080
```

---

## 📚 PART 14: HELPFUL ALIASES

### **Add to ~/.bashrc**

```bash
# Edit bashrc
nano ~/.bashrc

# Add these aliases at the end:
alias visa='cd "/home/innovativeautomations/Visa Exhibit Maker"'
alias visa-run='cd "/home/innovativeautomations/Visa Exhibit Maker/streamlit-exhibit-generator" && streamlit run app.py'
alias visa-status='cd "/home/innovativeautomations/Visa Exhibit Maker" && git status'
alias visa-pull='cd "/home/innovativeautomations/Visa Exhibit Maker" && git pull origin master'

# Save and reload
source ~/.bashrc

# Now you can use:
visa          # Go to project
visa-run      # Run app
visa-status   # Check git status
visa-pull     # Pull latest changes
```

---

## 🎯 COMPLETE START-TO-FINISH EXAMPLE

```bash
# 1. Open terminal
# Press Ctrl+Alt+T (Linux) or Cmd+Space → Terminal (Mac)

# 2. Navigate to project
cd "/home/innovativeautomations/Visa Exhibit Maker"

# 3. Check git status
git status

# 4. Pull latest changes
git pull origin master

# 5. View project structure
ls -la

# 6. Navigate to Streamlit app
cd streamlit-exhibit-generator

# 7. View files
ls -la

# 8. Activate virtual environment (if you have one)
source venv/bin/activate

# 9. Check dependencies
pip list

# 10. Run the application
streamlit run app.py

# 11. Open browser to http://localhost:8501

# 12. When done, stop with Ctrl+C

# 13. Deactivate virtual environment
deactivate

# 14. Go back to root
cd ..
```

---

## 💡 PRO TIPS

1. **Use Tab Completion**: Type first few letters and press Tab
2. **Use Up Arrow**: Recall previous commands
3. **Use Ctrl+R**: Search command history
4. **Use Ctrl+C**: Stop current process
5. **Use Ctrl+Z**: Pause process (resume with `fg`)
6. **Use `!!`**: Repeat last command
7. **Use `sudo !!`**: Repeat last command with sudo

---

## 📞 QUICK HELP

```bash
# Get help for any command
man command_name        # Manual page
command_name --help     # Help flag
command_name -h         # Short help
```

---

**You're now ready to work with the Visa Exhibit Maker project in terminal!**

For more help, see:
- GOOGLE_CLOUD_RUN_ENV_VARS.md
- ENV_QUICK_REFERENCE.txt
- README.md files in each directory
