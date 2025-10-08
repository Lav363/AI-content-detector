import wikipediaapi
from sentence_transformers import SentenceTransformer, util
import torch
# Load a model for calculating sentence similarity
similarity_model = SentenceTransformer('all-MiniLM-L6-v2')

# Setup Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent="AIContentDetector/1.0 (lavuramya363@gmail.com)", # Replace with your email
    timeout=20
)

def extract_claim(text):
    """
    A very simple claim extractor. For this prototype, we'll just use the first sentence.
    A more advanced version would identify key statements.
    """
    first_sentence = text.strip().split('.')[0] + '.'
    return first_sentence

def retrieve_evidence(query):
    """
    Retrieves the summary of the top Wikipedia page for a given query.
    """
    page = wiki_wiki.page(query)
    if not page.exists():
        return None, "Wikipedia page not found."
    return page.summary, page.fullurl

def verify_claim(claim, evidence):
    """
    Compares the claim against the evidence using sentence similarity.
    Returns the most similar sentence from the evidence and the similarity score.
    """
    if not evidence:
        return "No evidence found.", 0.0

    # Split evidence into sentences
    evidence_sentences = evidence.split('. ')
    
    # Encode claim and evidence sentences into vectors
    claim_embedding = similarity_model.encode(claim, convert_to_tensor=True)
    evidence_embeddings = similarity_model.encode(evidence_sentences, convert_to_tensor=True)
    
    # Compute cosine similarities
    cosine_scores = util.cos_sim(claim_embedding, evidence_embeddings)
    
    # Find the sentence with the highest similarity
    best_match_index = torch.argmax(cosine_scores)
    best_score = cosine_scores[0][best_match_index].item()
    most_similar_sentence = evidence_sentences[best_match_index]
    
    return most_similar_sentence, best_score

# --- Example Usage ---
if __name__ == "__main__":
    # Example from a real paper abstract (simplified)
    sample_text = "The capital of France is Paris, a city known for its art and culture. It is the most populous city in the country. Our research focuses on its economic impact in the 21st century."
    
    print("--- Fact-Checking Prototype ---")
    
    # 1. Extract a claim
    claim = extract_claim(sample_text)
    print(f"Extracted Claim: '{claim}'")
    
    # 2. Retrieve evidence
    evidence, url = retrieve_evidence("Capital of France")
    print(f"Retrieving evidence from Wikipedia...")
    
    # 3. Verify claim against evidence
    if evidence:
        most_similar, score = verify_claim(claim, evidence)
        print(f"Similarity Score: {score:.2f}")
        print(f"Most Relevant Sentence in Evidence: '{most_similar.strip()}'")
        print(f"Source URL: {url}")
    else:
        print("Could not retrieve evidence.")