import torch
import torch.nn as nn
from transformers import BertModel, BertTokenizer


class CrossModalFusion(nn.Module):
    """Слияние числовых финансовых данных и текстовой информации"""

    def __init__(self, num_features=64, text_model_name='bert-base-uncased'):
        super().__init__()
        self.text_encoder = BertModel.from_pretrained(text_model_name)
        self.tokenizer = BertTokenizer.from_pretrained(text_model_name)
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

    def encode_text(self, text):
        """Кодирование текста в векторные представления"""
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        return self.text_encoder(**inputs).last_hidden_state.mean(dim=1)

    def forward(self, financial_data, text_data):
        """Слияние финансовых данных и текста"""
        financial_emb = self.financial_encoder(financial_data)
        text_emb = self.encode_text(text_data)
        combined = torch.cat([financial_emb, text_emb], dim=1)
        fused = self.fusion_layer(combined.unsqueeze(0))
        return fused.squeeze(0)