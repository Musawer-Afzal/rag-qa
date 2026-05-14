# core/generation.py
import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# ===================================================================
# Universal QA System
# ===================================================================
class UniversalQASystem:
    """
    Handles prompt construction and answer generation ONLY
    """

    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model
        self.model.eval()

        print(f"QA system ready on {next(self.model.parameters()).device}")

    def answer(self, context: str, question: str, verbose: bool = False) -> str:
        """Generate answer from retrieved context"""

        # Clean inputs
        clean_context = re.sub(r'\s+', ' ', context).strip()
        clean_question = re.sub(r'\s+', ' ', question).strip()

        if verbose:
            print("\n" + "=" * 60)
            print(f"QUESTION: {clean_question}")
            print(f"Context length: {len(clean_context)} chars")
            print("-" * 60)

        # Prompt
        prompt = f"""Answer the question briefly (2 to 3 sentences max) using only the context.

CONTEXT:
{clean_context[:500]}

QUESTION: {clean_question}

ANSWER:"""

        try:
            # Tokenize
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=1024,
                padding=True
            ).to(self.model.device)

            # Generate output
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=80,
                    num_beams=4,
                    temperature=0.3,
                    do_sample=False,
                    repetition_penalty=1.5,
                    length_penalty=0.8,
                    no_repeat_ngram_size=3,
                    early_stopping=True
                )

            # Decode
            answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Extract answer only
            if "ANSWER:" in answer:
                answer = answer.split("ANSWER:")[-1].strip()

            # Clean up whitespace
            answer = re.sub(r'\s+', ' ', answer).strip()

            if verbose:
                print("ANSWER:")
                print("-" * 40)
                print(answer)
                print("-" * 40)

            return answer

        except Exception as e:
            return f"Error: {str(e)}"

# ===================================================================
# Helper function for fast imports in API
# ===================================================================
_qa_instance = None  # singleton

def generate_answer(context: str, question: str, model_name: str = "google/flan-t5-base", verbose: bool = False) -> str:
    """
    Simple wrapper to generate answers using a singleton QA system.
    This allows endpoints to just call generate_answer() without managing models.
    """
    global _qa_instance

    if _qa_instance is None:
        print(f"Loading QA system with model '{model_name}'...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,  # CPU safe
            device_map="auto" if torch.cuda.is_available() else None
        )
        _qa_instance = UniversalQASystem(tokenizer, model)

    return _qa_instance.answer(context, question, verbose=verbose)