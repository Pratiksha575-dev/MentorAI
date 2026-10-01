from personality_model import analyze_personality


# Test user
# 50 answers, each between 1 and 5
test_answers = [
    5, 2, 4, 2, 5, 2, 4, 1, 5, 2,   # Extraversion
    2, 4, 2, 5, 2, 4, 2, 4, 2, 3,   # Neuroticism
    5, 2, 5, 2, 5, 2, 4, 2, 5, 2,   # Agreeableness
    5, 2, 5, 2, 5, 2, 5, 2, 4, 2,   # Conscientiousness
    5, 2, 5, 2, 5, 2, 4, 2, 5, 2    # Openness
]


result = analyze_personality(test_answers)


print("\n==============================")
print("     CONNECTAI ANALYSIS")
print("==============================")

print("\nPersonality Traits:")

for trait, score in result["traits"].items():
    print(f"{trait:20}: {score:.2f} / 5")

print("\nPersonality Cluster:")
print(f"Cluster {result['cluster']}")

print("\n==============================")