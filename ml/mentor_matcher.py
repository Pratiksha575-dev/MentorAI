import numpy as np

def calculate_compatibility(mentor, group):
    raw_score = 0
    
    # Topic matching (max 20)
    topic = group.get("project_topic", "").lower()
    for domain in mentor.get("domains", []):
        if domain.lower() in topic or topic in domain.lower():
            raw_score += 20
            break
            
    # Complementary traits (max 25 + 25 = 50)
    raw_score += (5 - mentor["neuroticism"]) * group["neuroticism"]
    raw_score += mentor["conscientiousness"] * (5 - group["conscientiousness"])
    
    # Similar traits (max 15 + 15 = 30)
    raw_score += (5 - abs(mentor["openness"] - group["openness"])) * 3
    raw_score += (5 - abs(mentor["agreeableness"] - group["agreeableness"])) * 3
    
    # Total raw_score max is ~100
    return min(max(raw_score, 0), 100)

def match_mentors_and_mentees(mentors, groups, max_groups_per_mentor=4):
    assignments = {m["id"]: {"mentor": m, "mentees": []} for m in mentors}
    unassigned_groups = list(groups)
    np.random.shuffle(unassigned_groups)
    
    for group in unassigned_groups:
        best_mentor_id = None
        best_score = -1
        
        for mentor in mentors:
            if len(assignments[mentor["id"]]["mentees"]) < max_groups_per_mentor:
                score = calculate_compatibility(mentor, group)
                if score > best_score:
                    best_score = score
                    best_mentor_id = mentor["id"]
        
        if best_mentor_id:
            assignments[best_mentor_id]["mentees"].append({
                "mentee": group,
                "score": best_score
            })
            
    return assignments
