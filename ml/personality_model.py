# ml/personality_model.py

def analyze_traits(answers, questions_bank):
    """
    Calculates Big Five traits directly from a 20-question test.
    answers: List of integer scores (1-5).
    questions_bank: MENTOR_QUESTIONS or STUDENT_QUESTIONS list.
    """
    if len(answers) != len(questions_bank):
        raise ValueError(f"Expected {len(questions_bank)} answers.")
        
    traits = {
        "Extraversion": [],
        "Neuroticism": [],
        "Agreeableness": [],
        "Conscientiousness": [],
        "Openness": []
    }
    
    # Mapping abbreviated keys to full trait names
    key_map = {
        "EXT": "Extraversion",
        "EST": "Neuroticism",
        "AGR": "Agreeableness",
        "CSN": "Conscientiousness",
        "OPN": "Openness"
    }
    
    for i, answer in enumerate(answers):
        trait_key = questions_bank[i][0]
        full_trait = key_map[trait_key]
        
        # Simple scoring logic for the 4 questions per trait:
        # 1st and 3rd are positively correlated.
        # 2nd and 4th are negatively correlated.
        if i % 4 == 0 or i % 4 == 2:
            score = answer
        else:
            score = 6 - answer # Reverse scoring
            
        traits[full_trait].append(score)
        
    # Calculate average out of 5
    final_traits = {}
    for trait, scores in traits.items():
        final_traits[trait] = sum(scores) / len(scores)
        
    return final_traits