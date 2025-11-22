import re
import spacy
import language_tool_python
from sentence_transformers import SentenceTransformer, util
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from config import (
    SalutationKeywords, MustHaveKeywords, GoodToHaveKeywords,
    FillerWords, WPMRanges, GrammarScoreMap, TTRScoreMap,
    FillerRateMap, SentimentScoreMap
)

nlp = spacy.load('en_core_web_sm')
grammar_tool = language_tool_python.LanguageTool('en-US')
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

sentiment_analyzer = SentimentIntensityAnalyzer()


def analyze_salutation(transcript):
    text_lower = transcript.lower()
    
    for level, data in SalutationKeywords.items():
        for keyword in data['keywords']:
            if keyword in text_lower:
                return {
                    'score': data['score'],
                    'level': level,
                    'found': keyword
                }
    
    return {'score': 0, 'level': 'none', 'found': None}


def analyze_keywords(transcript):
    text_lower = transcript.lower()
    must_have_found = []
    good_to_have_found = []
    
    for category, keywords in MustHaveKeywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                must_have_found.append(category)
                break
    
    for category, keywords in GoodToHaveKeywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                good_to_have_found.append(category)
                break
    
    must_have_score = len(must_have_found) * 2.5
    good_to_have_score = len(good_to_have_found) * 5
    
    return {
        'must_have_score': min(must_have_score, 20),
        'good_to_have_score': min(good_to_have_score, 10),
        'must_have_found': must_have_found,
        'good_to_have_found': good_to_have_found,
        'must_have_count': len(must_have_found),
        'good_to_have_count': len(good_to_have_found)
    }


def analyze_flow(transcript):
    text_lower = transcript.lower()
    
    salutation_found = False
    for level_data in SalutationKeywords.values():
        if any(kw in text_lower[:100] for kw in level_data['keywords']):
            salutation_found = True
            break
    
    closing_keywords = ['thank you', 'thanks for listening', 'thank you for your time', 'thanks']
    closing_found = any(kw in text_lower[-100:] for kw in closing_keywords)
    
    if salutation_found and closing_found:
        return {'score': 5, 'order_followed': True}
    else:
        return {'score': 0, 'order_followed': False}


def calculate_speech_rate(transcript, duration_seconds=None):
    words = transcript.split()
    word_count = len(words)
    
    if duration_seconds is None:
        assumed_wpm = 120
        duration_seconds = (word_count / assumed_wpm) * 60
    
    wpm = word_count / (duration_seconds / 60) if duration_seconds > 0 else 120
    
    for category, ranges in WPMRanges.items():
        if ranges['min'] <= wpm <= ranges['max']:
            return {
                'score': ranges['score'],
                'wpm': round(wpm, 2),
                'category': category,
                'word_count': word_count
            }
    
    return {'score': 2, 'wpm': round(wpm, 2), 'category': 'unknown', 'word_count': word_count}


def check_grammar(transcript):
    matches = grammar_tool.check(transcript)
    word_count = len(transcript.split())
    
    errors_per_100_words = (len(matches) / word_count) * 100 if word_count > 0 else 0
    grammar_score = 1 - min(errors_per_100_words / 10, 1)
    grammar_score = max(0, grammar_score)
    
    for threshold, score in GrammarScoreMap:
        if grammar_score >= threshold:
            return {
                'score': score,
                'grammar_quality': round(grammar_score, 2),
                'errors': len(matches),
                'errors_per_100': round(errors_per_100_words, 2)
            }
    
    return {
        'score': 2,
        'grammar_quality': round(grammar_score, 2),
        'errors': len(matches),
        'errors_per_100': round(errors_per_100_words, 2)
    }


def calculate_vocabulary_richness(transcript):
    doc = nlp(transcript.lower())
    words = [token.text for token in doc if token.is_alpha]
    
    if len(words) == 0:
        return {'score': 0, 'ttr': 0, 'unique_words': 0, 'total_words': 0}
    
    unique_words = len(set(words))
    ttr = unique_words / len(words)
    
    for threshold, score in TTRScoreMap:
        if ttr >= threshold:
            return {
                'score': score,
                'ttr': round(ttr, 2),
                'unique_words': unique_words,
                'total_words': len(words)
            }
    
    return {
        'score': 2,
        'ttr': round(ttr, 2),
        'unique_words': unique_words,
        'total_words': len(words)
    }


def calculate_filler_rate(transcript):
    text_lower = transcript.lower()
    words = transcript.split()
    total_words = len(words)
    
    filler_count = sum(text_lower.count(' ' + filler + ' ') for filler in FillerWords)
    filler_count += sum(1 for filler in FillerWords if text_lower.startswith(filler + ' '))
    filler_count += sum(1 for filler in FillerWords if text_lower.endswith(' ' + filler))
    
    filler_rate = (filler_count / total_words) * 100 if total_words > 0 else 0
    
    for threshold, score in FillerRateMap:
        if filler_count >= threshold:
            return {
                'score': score,
                'filler_count': filler_count,
                'filler_rate': round(filler_rate, 2)
            }
    
    return {
        'score': 15,
        'filler_count': filler_count,
        'filler_rate': round(filler_rate, 2)
    }


def analyze_sentiment(transcript):
    sentiment_scores = sentiment_analyzer.polarity_scores(transcript)
    
    compound_score = sentiment_scores['compound']
    compound_normalized = (compound_score + 1) / 2
    
    for threshold, score in SentimentScoreMap:
        if compound_normalized >= threshold:
            return {
                'score': score,
                'compound_normalized': round(compound_normalized, 2),
                'compound': round(sentiment_scores['compound'], 2),
                'pos': round(sentiment_scores['pos'], 2),
                'neu': round(sentiment_scores['neu'], 2),
                'neg': round(sentiment_scores['neg'], 2)
            }
    
    return {
        'score': 3,
        'compound_normalized': round(compound_normalized, 2),
        'compound': round(sentiment_scores['compound'], 2),
        'pos': round(sentiment_scores['pos'], 2),
        'neu': round(sentiment_scores['neu'], 2),
        'neg': round(sentiment_scores['neg'], 2)
    }

def calculate_semantic_similarity(transcript):
    ideal_patterns = [
        "My name is [name] and I am [age] years old",
        "I study at [school name] in class [grade]",
        "I live with my family including my parents and siblings",
        "My hobbies include [activities] and I enjoy [interests]",
        "I want to achieve my goal of [ambition] in the future",
        "My family is special because [unique trait]"
    ]
    
    # Split transcript into sentences using spaCy
    doc = nlp(transcript)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    
    if not sentences:
        sentences = [transcript]
    
    # Encode each sentence separately
    sentence_embeddings = semantic_model.encode(sentences, convert_to_tensor=True)
    pattern_embeddings = semantic_model.encode(ideal_patterns, convert_to_tensor=True)
    
    # Create similarity matrix comparing all sentences to all patterns
    similarity_matrix = util.cos_sim(sentence_embeddings, pattern_embeddings)
    
    # For each pattern, find the best matching sentence
    best_matches = []
    for pattern_idx in range(len(ideal_patterns)):
        best_sentence_similarity = float(similarity_matrix[:, pattern_idx].max())
        best_matches.append(best_sentence_similarity)
    
    # Average the best matches to get final similarity score
    avg_similarity = sum(best_matches) / len(best_matches) if best_matches else 0.0
    
    # Adjust quality thresholds: High ≥0.5, Medium ≥0.35, Low <0.35
    if avg_similarity >= 0.5:
        semantic_quality = 'High'
    elif avg_similarity >= 0.35:
        semantic_quality = 'Medium'
    else:
        semantic_quality = 'Low'
    
    return {
        'avg_similarity': round(avg_similarity, 3),
        'semantic_quality': semantic_quality
    }


def calculate_overall_score(transcript, duration_seconds=None):
    salutation = analyze_salutation(transcript)
    keywords = analyze_keywords(transcript)
    flow = analyze_flow(transcript)
    speech_rate = calculate_speech_rate(transcript, duration_seconds)
    grammar = check_grammar(transcript)
    vocabulary = calculate_vocabulary_richness(transcript)
    clarity = calculate_filler_rate(transcript)
    engagement = analyze_sentiment(transcript)
    semantic = calculate_semantic_similarity(transcript)  
    
    content_structure_score = (
        salutation['score'] + 
        keywords['must_have_score'] + 
        keywords['good_to_have_score'] + 
        flow['score']
    )
    
    language_grammar_score = grammar['score'] + vocabulary['score']
    
    overall_score = (
        content_structure_score + 
        speech_rate['score'] + 
        language_grammar_score + 
        clarity['score'] + 
        engagement['score']
    )
    
    return {
        'overall_score': round(overall_score, 2),
        'max_score': 100,
        'transcript_length': len(transcript.split()),  
        'breakdown': {
            'content_structure': {
                'score': round(content_structure_score, 2),
                'max': 40,
                'salutation': salutation,
                'keywords': keywords,
                'flow': flow,
                'semantic_analysis': semantic 
            },
            'speech_rate': {
                'score': speech_rate['score'],
                'max': 10,
                'details': speech_rate
            },
            'language_grammar': {
                'score': round(language_grammar_score, 2),
                'max': 20,
                'grammar': grammar,
                'vocabulary': vocabulary
            },
            'clarity': {
                'score': clarity['score'],
                'max': 15,
                'details': clarity
            },
            'engagement': {
                'score': engagement['score'],
                'max': 15,
                'details': engagement
            }
        }
    }
