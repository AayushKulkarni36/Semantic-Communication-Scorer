# Semantic Communication Scorer

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

An intelligent NLP-powered system for evaluating communication quality from transcript text. The system analyzes five key dimensions to provide comprehensive scoring with detailed feedback.

##  Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Example](#-example)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [Scoring Methodology](#-scoring-methodology)
- [Design Decisions](#-design-decisions)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)
- [Acknowledgments](#-acknowledgments)

##  Features

The system evaluates communication across **5 dimensions** with a total score of **100 points**:

| Dimension | Max Points | Components |
|-----------|------------|------------|
| **Content Structure** | 40 | Salutation (5), Must-have keywords (20), Good-to-have keywords (10), Flow (5) |
| **Speech Rate** | 10 | Words per minute (WPM) analysis |
| **Language & Grammar** | 20 | Grammar correctness (10), Vocabulary richness (10) |
| **Clarity** | 15 | Filler word usage analysis |
| **Engagement** | 15 | Sentiment analysis |

### Key Capabilities

-  **Semantic Analysis**: Uses sentence transformers to evaluate content relevance
-  **Multi-dimensional Scoring**: Comprehensive evaluation across 5 criteria
-  **Grammar Checking**: Real-time grammar error detection
-  **Sentiment Analysis**: Emotional engagement assessment
-  **Vocabulary Richness**: Type-Token Ratio (TTR) calculation
-  **Real-time Processing**: Fast API response times

##  Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 2GB+ RAM (4GB recommended for ML models)

### Quick Setup

```bash
# Clone the repository
git clone <repository-url>
cd NirmaanAi

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm

# Run the application
python app.py
```

The application will be available at `http://localhost:5000`

##  Usage

### Web Interface

Navigate to `http://localhost:5000` in your browser to access the interactive web interface.

### API Endpoint

**POST** `/score`

**Request:**
```json
{
  "transcript": "Good morning everyone. My name is John and I am 15 years old...",
  "duration": 120
}
```

**Response:**
```json
{
  "overall_score": 86.0,
  "max_score": 100,
  "transcript_length": 150,
  "breakdown": {
    "content_structure": {
      "score": 35.0,
      "max": 40,
      "salutation": {...},
      "keywords": {...},
      "flow": {...},
      "semantic_analysis": {...}
    },
    "speech_rate": {
      "score": 10,
      "max": 10,
      "details": {...}
    },
    "language_grammar": {
      "score": 18.0,
      "max": 20,
      "grammar": {...},
      "vocabulary": {...}
    },
    "clarity": {
      "score": 12,
      "max": 15,
      "details": {...}
    },
    "engagement": {
      "score": 11,
      "max": 15,
      "details": {...}
    }
  }
}
```

**Health Check:**
```bash
GET /health
```

## Example

### Input Transcript

```
Good morning everyone. I'm excited to introduce myself. My name is Sarah and I am 14 years old. I study at Riverside High School in grade 9. I live with my wonderful family including my parents and my younger sister. 

In my free time, I enjoy reading books and playing basketball. These hobbies keep me active and help me learn new things. My family is special because we always support each other in everything we do.

My goal is to become a scientist in the future. I want to explore new discoveries and make a positive impact on the world. Thank you for listening.
```

### Output Score: **86/100**

**Breakdown:**

| Dimension | Score | Details |
|-----------|-------|---------|
| Content Structure | 35/40 | Excellent salutation (5), 7/8 must-have keywords (17.5), 1/2 good-to-have (5), proper flow (5), semantic similarity: 0.52 |
| Speech Rate | 10/10 | 125 WPM (ideal range: 111-140) |
| Language & Grammar | 18/20 | Grammar quality: 0.95 (10), TTR: 0.72 (8) |
| Clarity | 12/15 | 3 filler words detected |
| Engagement | 11/15 | Positive sentiment: 0.68 |

##  Project Structure

```
NirmaanAi/
├── app.py                 # Flask application and API routes
├── scorer.py              # Core scoring algorithms
├── config.py              # Configuration and scoring parameters
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
├── DEPLOYMENT.md         # Deployment instructions
├── templates/
│   └── index.html        # Web interface
├── static/               # Frontend assets
└── data/                 # Data files
```

##  Technology Stack

### Core Framework
- **Flask 3.0.0** - Web framework
- **Flask-CORS 4.0.0** - Cross-origin resource sharing

### NLP & ML Libraries
- **spaCy 3.7.2** - Natural language processing
- **sentence-transformers 2.7.0** - Semantic similarity
- **language-tool-python 2.8.1** - Grammar checking
- **vaderSentiment 3.3.2** - Sentiment analysis

### Data Processing
- **pandas 2.1.4** - Data manipulation
- **numpy 1.26.4** - Numerical computing
- **scikit-learn 1.3.0** - Machine learning utilities

### Production
- **gunicorn 21.2.0** - WSGI HTTP server

##  Scoring Methodology

### 1. Content Structure (40 points)

**Salutation (5 points):**
```python
# Excellent: "excited to introduce", "thrilled to" → 5 points
# Good: "good morning", "hello everyone" → 4 points
# Normal: "hi", "hello" → 2 points
```

**Must-have Keywords (20 points):**
- 8 categories: name, age, school, family, hobbies, about_family, origin, ambition
- 2.5 points per category found (max 20)

**Good-to-have Keywords (10 points):**
- 2 categories: unique, strengths
- 5 points per category found (max 10)

**Flow (5 points):**
- Checks for salutation at start and closing at end
- Both present → 5 points

**Semantic Similarity:**
- Compares transcript against 6 ideal communication patterns
- Uses cosine similarity with sentence transformers
- Quality thresholds: High (≥0.5), Medium (≥0.35), Low (<0.35)

### 2. Speech Rate (10 points)

```python
WPM = (word_count / duration_seconds) * 60

# Ideal: 111-140 WPM → 10 points
# Fast: 141-160 WPM → 6 points
# Too Fast: >160 WPM → 2 points
# Slow: 81-110 WPM → 6 points
# Too Slow: <80 WPM → 2 points
```

### 3. Language & Grammar (20 points)

**Grammar (10 points):**
```python
errors_per_100_words = (grammar_errors / word_count) * 100
grammar_quality = 1 - min(errors_per_100_words / 10, 1)

# Quality ≥0.9 → 10 points
# Quality ≥0.7 → 8 points
# Quality ≥0.5 → 6 points
# Quality ≥0.3 → 4 points
# Quality <0.3 → 2 points
```

**Vocabulary Richness (10 points):**
```python
TTR = unique_words / total_words

# TTR ≥0.9 → 10 points
# TTR ≥0.7 → 8 points
# TTR ≥0.5 → 6 points
# TTR ≥0.3 → 4 points
# TTR <0.3 → 2 points
```

### 4. Clarity (15 points)

```python
filler_rate = (filler_count / total_words) * 100

# 0 fillers → 15 points
# 1-3 fillers → 12 points
# 4-6 fillers → 9 points
# 7-9 fillers → 6 points
# 10+ fillers → 3 points
```

### 5. Engagement (15 points)

```python
compound_normalized = (sentiment_compound + 1) / 2

# Normalized ≥0.9 → 15 points
# Normalized ≥0.7 → 12 points
# Normalized ≥0.5 → 9 points
# Normalized ≥0.3 → 6 points
# Normalized <0.3 → 3 points
```

##  Design Decisions

### Architecture Choices

1. **Modular Design**: Separated scoring logic (`scorer.py`) from API layer (`app.py`) for maintainability
2. **Configuration-driven**: All scoring parameters in `config.py` for easy tuning
3. **Lightweight Models**: Used `all-MiniLM-L6-v2` for fast semantic analysis without sacrificing accuracy
4. **Rule-based + ML Hybrid**: Combined keyword matching with semantic similarity for robust evaluation

### Trade-offs

- **Speed vs. Accuracy**: Chose faster models (MiniLM) over larger ones (BERT) for real-time API responses
- **Simplicity vs. Complexity**: Used rule-based keyword matching alongside ML for interpretable results
- **Memory vs. Performance**: Single model loading per worker balances memory usage and response time

### Performance Optimizations

- Lazy loading of ML models on first request
- Efficient sentence-level semantic comparison
- Caching of spaCy document processing


##  Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to new functions
- Include tests for new features
- Update documentation as needed

##  License

This project is licensed under the MIT License - see the LICENSE file for details.

##  Author
 Aayush Kulkarni

## Acknowledgments

- **spaCy** - For excellent NLP capabilities
- **Hugging Face** - For sentence transformer models
- **LanguageTool** - For grammar checking functionality
- **VADER Sentiment** - For sentiment analysis
- **Flask Community** - For the robust web framework
- **Open Source Community** - For continuous inspiration and support

---


