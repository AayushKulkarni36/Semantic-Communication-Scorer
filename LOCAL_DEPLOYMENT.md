# Deployment Guide

## Live Demo

Deployed Application: https://huggingface.co/spaces/aayushhhh/communication-scorer

The application is publicly accessible with full functionality including rule-based scoring, NLP semantic analysis, grammar checking, sentiment analysis, and vocabulary assessment.

## Local Deployment

### Prerequisites

List required software with minimum versions:

- Python 3.8 or higher
- Java JRE 8 or higher (required for LanguageTool grammar checking)
- pip (Python package manager)
- Git

### Installation Steps

#### 1. Clone Repository

```bash
git clone https://github.com/AayushKulkarni36/Semantic-Communication-Scorer.git
cd Semantic-Communication-Scorer
```

#### 2. Create Virtual Environment

**Windows PowerShell:**
```powershell
python -m venv venv
```

**Windows CMD:**
```cmd
python -m venv venv
```

**macOS/Linux:**
```bash
python3 -m venv venv
```

#### 3. Activate Virtual Environment

**Windows PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

#### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

#### 5. Verify Java Installation

```bash
java -version
```

If Java is not installed, download and install from [Oracle Java](https://www.oracle.com/java/technologies/downloads/) or [OpenJDK](https://openjdk.org/).

#### 6. Run Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Troubleshooting

**Port 5000 already in use:**

If port 5000 is occupied, modify `app.py` to use a different port:

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
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

### Testing the Application

Use the following sample transcript to test the application:

```
Hello everyone, myself Muskan, studying in class 8th B section from Christ Public School. I am 13 years old. I live with my family. There are 3 people in my family, me, my mother and my father. One special thing about my family is that they are very kind hearted to everyone and soft spoken. One thing I really enjoy is play, playing cricket and taking wickets. A fun fact about me is that I see in mirror and talk by myself. One thing people don't know about me is that I once stole a toy from one of my cousin. My favorite subject is science because it is very interesting. Through science I can explore the whole world and make the discoveries and improve the lives of others. Thank you for listening.
```

**Expected Score:** 86/100

**Breakdown:**
- Content & Structure: 34/40
- Speech Rate: 10/10
- Language & Grammar: 12/20
- Clarity: 15/15
- Engagement: 15/15

### Performance Notes

**First request delay:**

The first API request may take 10-30 seconds as ML models (sentence transformers, spaCy, LanguageTool) are loaded into memory. Subsequent requests will be significantly faster.

**Performance expectations:**

- First request: 10-30 seconds (model loading)
- Subsequent requests: 2-5 seconds
- Memory usage: 2-4 GB RAM recommended

**Model caching:**

ML models are cached in memory after the first load. Restart the application to clear the cache.

## Cloud Deployment (Hugging Face Spaces)

### Live Application

URL: https://huggingface.co/spaces/aayushhhh/communication-scorer

### Deployment Configuration

The Hugging Face Spaces deployment requires the following key files:

**requirements.txt:**
```
Flask==3.0.0
Flask-CORS==4.0.0
sentence-transformers==2.7.0
language-tool-python==2.8.1
vaderSentiment==3.3.2
spacy==3.7.4
gradio==4.44.0
torch>=2.2.0
numpy==1.26.4
```

**packages.txt:**
```
openjdk-8-jdk
```

**README.md with YAML frontmatter:**
```yaml
---
title: Communication Scorer
emoji: 🎯
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app_hf.py
pinned: false
---
```

### Deployment Steps

1. **Create Hugging Face account**

   Visit [Hugging Face](https://huggingface.co/) and create a free account.

2. **Create new Space**

   - Navigate to your profile and click "New Space"
   - Choose a Space name (e.g., `communication-scorer`)
   - Select SDK: Gradio
   - Select visibility: Public
   - Click "Create Space"

3. **Configure Space settings**

   - Upload `app_hf.py` as the main application file
   - Upload `requirements.txt` with exact package versions
   - Create `packages.txt` with system dependencies (Java)
   - Update `README.md` with YAML frontmatter

4. **Push code to HF using git**

   ```bash
   git clone https://huggingface.co/spaces/aayushhhh/communication-scorer
   cd communication-scorer
   git lfs install
   git add app_hf.py requirements.txt packages.txt README.md scorer.py config.py
   git commit -m "Initial deployment"
   git push
   ```

   The Space will automatically build and deploy. Monitor the build logs in the Space interface.

### Features on HF Deployment

**Advantages of Hugging Face Spaces deployment:**

- No cold starts: Models are pre-loaded and ready
- Public URL: Instantly shareable with anyone
- Gradio UI: User-friendly interface with no frontend development required
- Auto-deployment: Automatic rebuilds on git push
- Free hosting: No cost for public Spaces
- Full ML functionality: All NLP models work seamlessly
- Persistent storage: Models cached between requests
- Community features: Easy sharing and collaboration

### Comparison Table

| Feature | Local Deployment | Hugging Face Spaces |
|---------|-----------------|---------------------|
| Setup Time | 10-15 minutes | 5-10 minutes |
| Accessibility | Localhost only | Public URL, accessible worldwide |
| Dependencies | Manual installation required | Automatic via requirements.txt |
| Availability | Requires local machine running | 24/7 availability |
| Sharing | Requires port forwarding/VPN | Direct URL sharing |
| Cost | Free (local resources) | Free for public Spaces |
| Model Loading | First request delay | Pre-loaded, instant responses |
| Updates | Manual restart required | Automatic on git push |
| UI | Flask web interface | Gradio interface |

## Repository Structure

```
Semantic-Communication-Scorer/
├── app.py                 # Flask application (local deployment)
├── app_hf.py             # Gradio application (Hugging Face Spaces)
├── scorer.py             # Core scoring logic and NLP analysis
├── config.py             # Configuration constants and keyword mappings
├── requirements.txt      # Python dependencies
├── packages.txt          # System dependencies (for HF Spaces)
├── README.md             # Project documentation with HF frontmatter
├── LOCAL_DEPLOYMENT.md   # This deployment guide
├── templates/
│   └── index.html        # Flask web interface template
├── static/               # Static assets (CSS, JS)
└── data/                 # Data files (if any)
```

## Technology Stack

**Web Frameworks:**
- Flask 3.0.0: RESTful API and web server
- Gradio 4.44.0: Interactive ML interface for Hugging Face Spaces

**NLP & ML Libraries:**
- spaCy 3.7.4: Natural language processing and tokenization
- sentence-transformers 2.7.0: Semantic similarity analysis
- LanguageTool 2.8.1: Grammar and language checking
- VADER Sentiment 3.3.2: Sentiment analysis
- PyTorch >=2.2.0: Deep learning framework (dependency for sentence-transformers)

**Supporting Libraries:**
- NumPy 1.26.4: Numerical computations
- Flask-CORS 4.0.0: Cross-origin resource sharing

**Deployment Platforms:**
- Hugging Face Spaces: Cloud hosting with Gradio
- Local: Flask development server

**System Dependencies:**
- Java JRE 8+: Required for LanguageTool grammar checking
- Python 3.8+: Runtime environment

## Support

**GitHub Repository:**
https://github.com/AayushKulkarni36/Semantic-Communication-Scorer

**Hugging Face Space:**
https://huggingface.co/spaces/aayushhhh/communication-scorer

For issues, feature requests, or contributions, please use the GitHub repository's issue tracker.
