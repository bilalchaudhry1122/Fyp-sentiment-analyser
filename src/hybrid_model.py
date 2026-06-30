import torch
import torch.nn as nn
from typing import Dict, Any, Tuple

class HybridSentimentClassifier(nn.Module):
    def __init__(self, roberta_dim: int, lexicon_dim: int, num_labels: int = 3):
        super(HybridSentimentClassifier, self).__init__()
        self.roberta_dim = roberta_dim
        self.lexicon_dim = lexicon_dim
        
        # Dense layer for combining embeddings + lexicon features
        self.classifier = nn.Sequential(
            nn.Linear(roberta_dim + lexicon_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, num_labels)
        )
        
    def forward(self, roberta_embeddings: torch.Tensor, lexicon_features: torch.Tensor) -> torch.Tensor:
        """Forward pass combining both features."""
        combined = torch.cat((roberta_embeddings, lexicon_features), dim=-1)
        return self.classifier(combined)
