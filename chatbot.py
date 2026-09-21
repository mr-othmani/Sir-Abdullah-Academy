import json
from models import load_json

def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def get_bot_response(user_input: str) -> str:
    faqs = load_json('faq.json', [])
    query = user_input.lower().strip()
    
    best_match = None
    highest_score = 0
    
    for faq in faqs:
        for pattern in faq.get('patterns', []):
            pattern_clean = pattern.lower().strip()
            score = 0
            if pattern_clean in query:
                score += 10
            
            words = query.split()
            for word in words:
                if len(word) > 3 and levenshtein_distance(word, pattern_clean) <= 2:
                    score += 5
            
            if score > highest_score:
                highest_score = score
                best_match = faq.get('response')
                
    if best_match and highest_score >= 5:
        return best_match
        
    return "I'm sorry, I couldn't quite understand that. Please select options from the menu or contact us on WhatsApp (+92 332 1234567)."
