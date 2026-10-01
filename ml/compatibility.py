# ml/compatibility.py

TRAIT_WEIGHTS = {
    "Extraversion": 0.20,
    "Neuroticism": 0.15,
    "Agreeableness": 0.25,
    "Conscientiousness": 0.20,
    "Openness": 0.20
}


def trait_similarity(traits_a, traits_b, weights=None):
    """
    Calculates weighted personality similarity.

    Returns a score from 0 to 100.
    """

    if weights is None:
        weights = TRAIT_WEIGHTS

    total_weight = sum(weights.values())

    if total_weight == 0:
        return 0.0

    score = 0.0

    for trait, weight in weights.items():

        a = float(traits_a.get(trait, 0))
        b = float(traits_b.get(trait, 0))

        # Traits are on a 1-5 scale.
        difference = abs(a - b)

        similarity = max(0.0, 1.0 - (difference / 4.0))

        score += similarity * weight

    return (score / total_weight) * 100


def interest_similarity(interests_a, interests_b):
    """
    Jaccard similarity between two interest lists.
    """

    set_a = set(
        str(x).strip().lower()
        for x in (interests_a or [])
        if str(x).strip()
    )

    set_b = set(
        str(x).strip().lower()
        for x in (interests_b or [])
        if str(x).strip()
    )

    if not set_a and not set_b:
        return 50.0

    if not set_a or not set_b:
        return 0.0

    intersection = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))

    if union == 0:
        return 0.0

    return (intersection / union) * 100


def social_energy_compatibility(traits_a, traits_b):
    """
    Measures compatibility of social energy.

    Based mainly on Extraversion.

    Similar social energy gets a higher score.
    """

    a = float(traits_a.get("Extraversion", 3))
    b = float(traits_b.get("Extraversion", 3))

    difference = abs(a - b)

    return max(0.0, 1.0 - (difference / 4.0)) * 100


def calculate_compatibility(
    traits_a,
    traits_b,
    interests_a=None,
    interests_b=None,
    trait_weights=None,
    personality_weight=0.60,
    interests_weight=0.25,
    social_weight=0.15
):
    """
    Calculate compatibility between two people.

    Returns:
        overall
        personality
        interests
        social_energy
    """

    personality = trait_similarity(
        traits_a,
        traits_b,
        trait_weights
    )

    interests = interest_similarity(
        interests_a or [],
        interests_b or []
    )

    social_energy = social_energy_compatibility(
        traits_a,
        traits_b
    )

    overall = (
        personality * personality_weight
        + interests * interests_weight
        + social_energy * social_weight
    )

    return {
        "overall": round(overall, 1),
        "personality": round(personality, 1),
        "interests": round(interests, 1),
        "social_energy": round(social_energy, 1)
    }


# ---------------------------------------------------------
# QUERY-SPECIFIC COMPATIBILITY
# ---------------------------------------------------------

def calculate_query_compatibility(
    traits_a,
    traits_b,
    interests_a,
    interests_b,
    query_info
):
    """
    Calculates compatibility according to the user's
    natural-language request.

    Example:

    "Who is my best travel partner?"

    Ollama may return:

    Openness       0.40
    Extraversion   0.30
    Agreeableness  0.20
    etc.
    """

    trait_weights = query_info.get(
        "important_traits",
        TRAIT_WEIGHTS
    )

    # Make sure all weights are valid numbers.
    cleaned_weights = {}

    for trait in [
        "Extraversion",
        "Neuroticism",
        "Agreeableness",
        "Conscientiousness",
        "Openness"
    ]:

        try:
            value = float(trait_weights.get(trait, 0))
        except (TypeError, ValueError):
            value = 0.0

        cleaned_weights[trait] = max(0.0, min(1.0, value))

    personality = trait_similarity(
        traits_a,
        traits_b,
        cleaned_weights
    )

    interests = interest_similarity(
        interests_a,
        interests_b
    )

    social_energy = social_energy_compatibility(
        traits_a,
        traits_b
    )

    purpose = query_info.get(
        "purpose",
        "overall_match"
    )

    # Different contexts use different combinations.
    if purpose == "travel_partner":

        overall = (
            personality * 0.55
            + interests * 0.25
            + social_energy * 0.20
        )

    elif purpose == "study_buddy":

        overall = (
            personality * 0.65
            + interests * 0.15
            + social_energy * 0.20
        )

    elif purpose == "project_partner":

        overall = (
            personality * 0.65
            + interests * 0.15
            + social_energy * 0.20
        )

    elif purpose == "friendship":

        overall = (
            personality * 0.55
            + interests * 0.30
            + social_energy * 0.15
        )

    elif purpose == "intellectual_match":

        overall = (
            personality * 0.70
            + interests * 0.15
            + social_energy * 0.15
        )

    elif purpose == "adventure_partner":

        overall = (
            personality * 0.50
            + interests * 0.25
            + social_energy * 0.25
        )

    elif purpose == "team_member":

        overall = (
            personality * 0.65
            + interests * 0.15
            + social_energy * 0.20
        )

    else:

        overall = (
            personality * 0.60
            + interests * 0.25
            + social_energy * 0.15
        )

    return {
        "overall": round(overall, 1),
        "personality": round(personality, 1),
        "interests": round(interests, 1),
        "social_energy": round(social_energy, 1)
    }


# ---------------------------------------------------------
# HUMAN-READABLE EXPLANATION
# ---------------------------------------------------------

def explain_match(
    traits_a,
    traits_b,
    interests_a,
    interests_b
):
    """
    Creates simple compatibility observations.
    """

    explanations = []

    # Personality
    personality = trait_similarity(
        traits_a,
        traits_b
    )

    if personality >= 80:
        explanations.append(
            "Your personality profiles are highly similar."
        )
    elif personality >= 65:
        explanations.append(
            "You have several compatible personality characteristics."
        )
    else:
        explanations.append(
            "Your personalities have some interesting differences."
        )

    # Interests
    interest_score = interest_similarity(
        interests_a,
        interests_b
    )

    if interest_score >= 60:
        explanations.append(
            "You share several common interests."
        )
    elif interest_score >= 25:
        explanations.append(
            "You have some overlapping interests."
        )
    else:
        explanations.append(
            "Your interests are quite different, which may create opportunities to explore new things."
        )

    # Social energy
    social_score = social_energy_compatibility(
        traits_a,
        traits_b
    )

    if social_score >= 80:
        explanations.append(
            "Your social energy levels are quite similar."
        )
    elif social_score >= 60:
        explanations.append(
            "Your social energy levels are reasonably compatible."
        )
    else:
        explanations.append(
            "Your social energy levels are noticeably different."
        )

    return explanations