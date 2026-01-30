from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer
import torch


def load_universal_model(model_name: str = "google/flan-t5-base"):
    """
    Load a Seq2Seq LLM (default: flan-t5-base) with safe settings
    Works on CPU and GPU (Colab-friendly)
    """

    print(f"Loading model: {model_name}")

    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        padding_side="left",
        truncation_side="left"
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,   # safest for CPU
        device_map="auto" if torch.cuda.is_available() else None
    )

    model.eval()

    print("✓ Model loaded and ready")
    return tokenizer, model

def load_embedder(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """
    Load a sentence-transformers embedding model.
    Returns the embedder object.
    """
    embedder = SentenceTransformer(model_name)
    return embedder
