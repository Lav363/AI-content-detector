import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import numpy as np
import nltk

# This is the corrected, more robust way to handle the download
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("NLTK 'punkt' tokenizer not found. Downloading...")
    nltk.download('punkt')

# Load a pre-trained model and tokenizer for perplexity calculation
# (The rest of your code stays the same)
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def calculate_perplexity(text):
    """Calculates the perplexity of a given text using GPT-2."""
    if not text.strip():
        return 0.0
        
    encodings = tokenizer(text, return_tensors="pt")
    max_length = model.config.n_positions
    stride = 512
    seq_len = encodings.input_ids.size(1)

    nlls = []
    prev_end_loc = 0
    for begin_loc in range(0, seq_len, stride):
        end_loc = min(begin_loc + max_length, seq_len)
        trg_len = end_loc - prev_end_loc
        input_ids = encodings.input_ids[:, begin_loc:end_loc]
        target_ids = input_ids.clone()
        target_ids[:, :-trg_len] = -100

        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)
            neg_log_likelihood = outputs.loss

        nlls.append(neg_log_likelihood)
        prev_end_loc = end_loc
        if end_loc == seq_len:
            break

    ppl = torch.exp(torch.stack(nlls).mean())
    return ppl.item()

def calculate_burstiness(text):
    """Calculates the burstiness of a text (std deviation of sentence lengths)."""
    if not text.strip():
        return 0.0
        
    sentences = nltk.sent_tokenize(text)
    sentence_lengths = [len(nltk.word_tokenize(s)) for s in sentences]
    
    if len(sentence_lengths) < 2:
        return 0.0 # Not enough sentences to calculate variance
        
    std_dev = np.std(sentence_lengths)
    return std_dev

# --- Example Usage ---
if __name__ == "__main__":
    ai_text = "The study of artificial intelligence is a cornerstone of modern computer science. The implications of this research are far-reaching and have the potential to revolutionize many industries. The development of advanced algorithms is crucial for progress in this field."
    human_text = "So, AI... it's everywhere now, right? It's weird. One minute you're just using it to find cat pictures, the next it's driving cars and writing articles. I wonder what's next. Honestly, it's a bit scary but also pretty cool."

    print("--- Statistical Analysis ---")
    
    # Analyze AI text
    ai_ppl = calculate_perplexity(ai_text)
    ai_burst = calculate_burstiness(ai_text)
    print(f"AI Text Perplexity: {ai_ppl:.2f} (Lower is more predictable)")
    print(f"AI Text Burstiness: {ai_burst:.2f} (Lower is more uniform)")

    print("-" * 20)

    # Analyze Human text
    human_ppl = calculate_perplexity(human_text)
    human_burst = calculate_burstiness(human_text)
    print(f"Human Text Perplexity: {human_ppl:.2f}")
    print(f"Human Text Burstiness: {human_burst:.2f}")