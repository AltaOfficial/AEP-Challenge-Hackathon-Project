import PyPDF2
import random


def extract_pdf_text(pdf_path):
    """Extract text content from a PDF file."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text


def create_training_examples(safety_info, guidelines, vocab, precursor):
    """Create training examples based on the content of the PDFs."""
    combined_text = safety_info + " " + guidelines + " " + vocab + " " + precursor
    sentences = combined_text.split('.')

    training_examples = []

    # Create positive examples
    for _ in range(50):  # Adjust the number of examples as needed
        sample = '. '.join(random.sample(sentences, 3))  # Combine 3 random sentences
        training_examples.append({
            "input": f"Hazard Observations: {sample}\n\nIs the above text a high-value hazard observation?",
            "output": "Yes, this is a high-value hazard observation because it directly relates to hazardous conditions based on guidelines and procedures, and is part of the Temperature: Fire with Sustained Fuel Source high energy category"
        })

    # Create negative examples
    negative_sentences = [
        "The weather was nice today.",
        "I had a sandwich for lunch.",
        "The traffic was heavy this morning.",
        "Remember to water the plants.",
        "The movie last night was entertaining."
    ]

    for _ in range(50):  # Adjust the number of examples as needed
        sample = '. '.join(random.sample(negative_sentences, 3))
        training_examples.append({
            "input": f"Safety guidelines: {sample}\n\nIs the above text a high-value safety observation?",
            "output": "No, this is not a high-value safety observation because it does not relate to any specific safety guidelines or procedures."
        })

    return training_examples


# Usage
safety_info = extract_pdf_text("data/cases.pdf")
guidelines = extract_pdf_text("data/eeiSCLModel.pdf")
vocab = extract_pdf_text("data/vocab_and_faq.pdf")
precursor = extract_pdf_text("data/precursor.pdf")
training_data = create_training_examples(safety_info, guidelines, vocab, precursor)