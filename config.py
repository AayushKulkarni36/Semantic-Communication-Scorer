SalutationKeywords = {
    'excellent': {
        'keywords': ['excited to introduce', 'feeling great', 'thrilled to', 'delighted to'],
        'score': 5
    },
    'good': {
        'keywords': ['good morning', 'good afternoon', 'good evening', 'good day', 'hello everyone'],
        'score': 4
    },
    'normal': {
        'keywords': ['hi', 'hello', 'hey'],
        'score': 2
    }
}

MustHaveKeywords = {
    'name': ['name', 'myself', 'i am', "i'm", 'call me'],
    'age': ['years old', 'age', 'born in'],
    'school': ['school', 'class', 'grade', 'studying', 'student at'],
    'family': ['family', 'parents', 'mother', 'father', 'siblings', 'brother', 'sister'],
    'hobbies': ['hobby', 'hobbies', 'enjoy', 'like to', 'love to', 'interest', 'free time', 'spare time'],
    'about_family': ['about my family', 'family is', 'special thing'],
    'origin': ['from', 'live in', 'belong to', 'location', 'hometown'],
    'ambition': ['ambition', 'goal', 'dream', 'want to', 'aspire', 'future', 'improve', 'explore', 'make discoveries']
}

GoodToHaveKeywords = {
    'unique': ['fun fact', 'interesting thing', 'unique about', 'special about me', "don't know"],
    'strengths': ['strength', 'achievement', 'good at', 'proud of', 'accomplishment']
}

FillerWords = [
    'um', 'uh', 'like', 'you know', 'so', 'actually', 'basically',
    'right', 'i mean', 'well', 'kinda', 'sort of', 'okay', 'hmm', 'ah'
]

WPMRanges = {
    'ideal': {'min': 111, 'max': 140, 'score': 10},
    'fast': {'min': 141, 'max': 160, 'score': 6},
    'too_fast': {'min': 161, 'max': 999, 'score': 2},
    'slow': {'min': 81, 'max': 110, 'score': 6},
    'too_slow': {'min': 0, 'max': 80, 'score': 2}
}

GrammarScoreMap = [
    (0.9, 10), (0.7, 8), (0.5, 6), (0.3, 4), (0.0, 2)
]

TTRScoreMap = [
    (0.9, 10), (0.7, 8), (0.5, 6), (0.3, 4), (0.0, 2)
]

FillerRateMap = [
    (0, 15), (4, 12), (7, 9), (10, 6), (13, 3)
]

SentimentScoreMap = [
    (0.9, 15), (0.7, 12), (0.5, 9), (0.3, 6), (0.0, 3)
]
