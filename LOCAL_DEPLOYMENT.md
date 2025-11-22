# Local Deployment Guide

## Prerequisites

List required software with minimum versions:

- Python 3.8 or higher
- Java JRE 8 or higher (required for LanguageTool grammar checking)
- pip (Python package manager)
- Git

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/AayushKulkarni36/Semantic-Communication-Scorer.git
cd Semantic-Communication-Scorer
```

### 2. Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
```

**Windows (CMD):**
```cmd
python -m venv venv
```

**macOS/Linux:**
```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 5. Verify Java Installation

```bash
java -version
```

If Java is not installed, download and install from [Oracle Java](https://www.oracle.com/java/technologies/downloads/) or [OpenJDK](https://openjdk.org/).

### 6. Run Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Troubleshooting

### Common Issues

**Port 5000 already in use:**

If port 5000 is occupied, modify `app.py` to use a different port:

```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)
```

Or stop the process using port 5000:

**Windows:**
```cmd
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
lsof -ti:5000 | xargs kill -9
```

**Java not found:**

Ensure Java is installed and added to your system PATH. Verify installation:

```bash
java -version
```

If the command fails, reinstall Java and ensure the `JAVA_HOME` environment variable is set correctly.

**spaCy model not found:**

Re-download the spaCy language model:

```bash
python -m spacy download en_core_web_sm
```

If issues persist, verify spaCy installation:

```bash
python -c "import spacy; print(spacy.__version__)"
```

**Module import errors:**

Ensure the virtual environment is activated and all dependencies are installed:

```bash
pip install -r requirements.txt --upgrade
```

If specific modules fail, install them individually:

```bash
pip install <module-name>
```

**Virtual environment activation issues:**

**Windows PowerShell execution policy:**

If activation fails in PowerShell, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

**Path issues:**

Ensure you are in the project root directory and the `venv` folder exists before activation.

## Testing the Application

### Sample Transcript

Use the following transcript to test the application:

```
Good morning everyone. I'm excited to introduce myself. My name is Sarah and I am 14 years old. I study at Riverside High School in grade 9. I live with my wonderful family including my parents and my younger sister. 

In my free time, I enjoy reading books and playing basketball. These hobbies keep me active and help me learn new things. My family is special because we always support each other in everything we do.

My goal is to become a scientist in the future. I want to explore new discoveries and make a positive impact on the world. Thank you for listening.
```

**Duration:** 120 seconds

### Expected Output

**Overall Score:** 86/100

**Breakdown:**

- Content Structure: 35/40
- Speech Rate: 10/10
- Language & Grammar: 18/20
- Clarity: 12/15
- Engagement: 11/15

## Stopping the Application

Press `Ctrl+C` in the terminal where the Flask server is running to stop the application gracefully.

## Additional Notes

**First request delay:**

The first API request may take 10-30 seconds as ML models (sentence transformers, spaCy, LanguageTool) are loaded into memory. Subsequent requests will be significantly faster.

**Performance expectations:**

- First request: 10-30 seconds (model loading)
- Subsequent requests: 2-5 seconds
- Memory usage: 2-4 GB RAM recommended

**Log file location:**

Application logs are displayed in the console/terminal. For production deployment, configure logging to write to files using Python's logging module.

**Environment variables:**

No environment variables are required for local deployment. All configuration is handled in `config.py`.

**Model caching:**

ML models are cached in memory after the first load. Restart the application to clear the cache.

