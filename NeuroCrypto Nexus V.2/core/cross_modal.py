import torch
import torch.nn as nn
from transformers import BertModel


class CrossModalFusion(nn.Module):
    """Кросс-модальное слияние финансовых и текстовых данных"""

    def __init__(self, num_features=64, text_model_name='bert-base-uncased'):
        super().__init__()
        self.text_encoder = BertModel.from_pretrained(text_model_name)
        self.financial_encoder = nn.Sequential(
            nn.Linear(10, 32),
            nn.ReLU(),
            nn.Linear(32, 64)
        )
        self.fusion_layer = nn.TransformerEncoderLayer(
            d_model=128,
            nhead=8,
            dim_feedforward=256
        )

    def fuse(self, financial_data, text_data):
        """Слияние финансовых данных и текста"""
        # Кодирование финансовых данных
        financial_emb = self.financial_encoder(financial_data)

        # Кодирование текста
        text_emb = self.text_encoder(**text_data).last_hidden_state.mean(dim=1)

        # Конкатенация
        combined = torch.cat([financial_emb, text_emb], dim=1)

        # Трансформер для слияния
        fused = self.fusion_layer(combined.unsqueeze(0))
        return fused.squeeze(0)