# agents/relationship_agent.py

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RelationshipAgent:
    def __init__(self, vc_embeddings: dict):
        self.embeddings = vc_embeddings

    def run(self):
        vc_names = list(self.embeddings.keys())
        matrix = cosine_similarity(list(self.embeddings.values()))
        relationships = []

        for i, name_a in enumerate(vc_names):
            for j, name_b in enumerate(vc_names):
                if i >= j:
                    continue
                sim_score = matrix[i][j]
                label = (
                    "Collaborative" if sim_score > 0.85
                    else "Competitive" if sim_score > 0.6
                    else "Independent"
                )
                relationships.append({
                    "vc_a": name_a,
                    "vc_b": name_b,
                    "score": float(sim_score),
                    "relationship": label
                })

        return relationships
