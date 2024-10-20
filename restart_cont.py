import restart
import ollama
import pandas as pd
from tqdm import tqdm

def load_model():
    """Load the LLaMA model using Ollama."""
    return ollama.Client()


def train_model(client, training_data):
    """Train the LLaMA model on the safety guidelines."""
    print("Training the model...")
    for item in tqdm(training_data):
        client.chat(model='llama3.2', messages=[
            {'role': 'user', 'content': item['input']},
            {'role': 'assistant', 'content': item['output']}
        ])
    print("Training complete.")


def analyze_comment(client, comment, safety_info, guidelines, vocab, precursor):
    """Analyze a single comment using the trained LLaMA model."""
    prompt = f"""
    Safety Info: {safety_info}
    Guidelines: {guidelines}
    Comment: {comment}

    Based on the safety information, guidelines, cases, and FAQs provided, is this comment a high-value hazard observation? 
    If yes, explain why it's one of the most hazardous and from which high energy category it falls into.

    Analysis:
    """

    response = client.chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
    result = response['message']['content']

    if "yes" in result.lower():
        hazardous = "high-value"
        explanation = result.split("yes,", 1)[-1].strip()
    else:
        hazardous = "low-value"
        explanation = result.split("no,", 1)[-1].strip()

    return hazardous, explanation


def analyze_comments(df, client, safety_info, guidelines, vocab, precursor):
    """Analyze comments using the trained LLaMA model."""
    results = []
    for _, row in tqdm(df.iterrows(), total=len(df)):
        hazardous, explanation = analyze_comment(client, row['PNT_ATRISKNOTES_TX'], safety_info, guidelines, vocab, precursor)
        results.append((hazardous, explanation))

    df['hazardous'] = [r[0] for r in results]
    df['explanation'] = [r[1] for r in results]
    return df


def get_top_comments(df, n=30):
    """Get the top n high-value comments."""
    high_value_comments = df[df['hazardous'] == 'high-value'].sort_values('Obs Number', ascending=False)
    return high_value_comments.head(n)


if __name__ == "__main__":
    client = load_model()

    # Load safety info and guidelines
    safety_info = restart.extract_pdf_text("data/cases.pdf")
    guidelines = restart.extract_pdf_text("data/eeiSCLModel.pdf")
    vocab = restart.extract_pdf_text("data/vocab_and_faq.pdf")
    precursor = restart.extract_pdf_text("data/precursor.pdf")

    # Create training data
    training_data = restart.create_training_examples(safety_info, guidelines, vocab, precursor)

    # Train the model
    train_model(client, restart.training_data)

    # Analyze comments
    df = pd.read_csv("data/comments.csv")
    analyzed_df = analyze_comments(df, client, safety_info, guidelines, vocab, precursor)
    top_comments = get_top_comments(analyzed_df)

    print(f"Top {len(top_comments)} high-value comments:")
    for _, row in top_comments.iterrows():
        print(f"Obs Number: {row['OBSRVTN_NB']}, Type: {row['PNT_NM']}")
        print(f"Comment: {row['PNT_ATRISKNOTES_TX']}")
        print(f"Explanation: {row['explanation']}")
        print("-" * 50)