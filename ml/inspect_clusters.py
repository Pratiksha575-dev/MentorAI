import joblib
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "kmeans.pkl"
)

kmeans = joblib.load(MODEL_PATH)

traits = [
    "Extraversion",
    "Neuroticism",
    "Agreeableness",
    "Conscientiousness",
    "Openness"
]

print("\n========================================")
print("       CONNECTAI CLUSTER PROFILES")
print("========================================\n")

centers = kmeans.cluster_centers_

for cluster_number, center in enumerate(centers):

    print(f"Cluster {cluster_number}")

    for trait, value in zip(traits, center):
        print(f"  {trait:20}: {value:.3f}")

    print()