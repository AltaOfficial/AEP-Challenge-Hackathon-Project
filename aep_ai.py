import pandas as pd
import PyPDF2
from sklearn.model_selection import train_test_split

def load_csv_data(file_path):
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} records from {file_path}")
    return df

def extract_pdf_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def prepare_data_for_finetuning(df, safety_info, guidelines):
    fine_tuning_data = []
    for _, row in df.iterrows():
        input_text = f"Safety Info: {safety_info}\nGuidelines: {guidelines}\nComment: {row['PNT_ATRISKNOTES_TX']}"
        output_text = "Classify this comment as high-value or low-value based on its potential to prevent serious hazards."
        fine_tuning_data.append({"input": input_text, "output": output_text})
    return fine_tuning_data

def prepare_data():
    df = load_csv_data("data/comments.csv")
    safety_info = extract_pdf_text("data/cases.pdf")
    guidelines = extract_pdf_text("data/eeiSCLmodel.pdf")
    fine_tuning_data = prepare_data_for_finetuning(df, safety_info, guidelines)
    train_data, val_data = train_test_split(fine_tuning_data, test_size=0.2, random_state=42)
    return train_data, val_data, df


if __name__ == "__main__":
    train_data, val_data, df = prepare_data()
    print(f"Prepared {len(train_data)} training samples and {len(val_data)} validation samples")


#####################


# Prepare data for fine-tuning
def prepare_data_for_finetuning(comments, safety_info, guidelines):
    fine_tuning_data = []
    for _, row in comments.iterrows():
        input_text = f"Safety Info: {safety_info}\nGuidelines: {guidelines}\nComment: {row['PNT_ATRISKNOTES_TX']}"
        output_text = "Classify this comment as high-value or low-value based on its potential to prevent serious hazards."
        fine_tuning_data.append({"input": input_text, "output": output_text})
    return fine_tuning_data

# Main data preparation function
def prepare_data():
    comments = pd.read_csv("data/comments.csv")
    safety_info = PyPDF2.PdfReader("data/cases.pdf")
    guidelines = PyPDF2.PdfReader("data/eeiSCLmodel.pdf")
    fine_tuning_data = prepare_data_for_finetuning(comments=comments, safety_info=safety_info, guidelines=guidelines)
    train_data, val_data = train_test_split(fine_tuning_data, test_size=0.2, random_state=42)
    return train_data, val_data, comments

if __name__ == "__main__":
    train_data, val_data, comments = prepare_data()
    print(f"Prepared {len(train_data)} training samples and {len(val_data)} validation samples")

############
