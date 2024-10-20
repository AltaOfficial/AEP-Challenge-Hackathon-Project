import restart, restart_cont
import streamlit as st
import pandas as pd

def main():
    st.title("Hazard Comment Analysis")

    # Load the LLaMA model
    client = restart_cont.load_model()

    # Load safety info and guidelines
    safety_info = restart.extract_pdf_text("data/cases.pdf")
    guidelines = restart.extract_pdf_text("data/eeiSCLModel.pdf")
    vocab =restart.extract_pdf_text("data/vocab_and_faq.pdf")
    precursor = restart.extract_pdf_text("data/precursor.pdf")

    # Create training data
    training_data = restart.create_training_examples(safety_info, guidelines, vocab, precursor)

    # Train the model
    with st.spinner("Training the model on safety guidelines..."):
        restart_cont.train_model(client, training_data)
    st.success("Model training complete!")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        st.write(f"Uploaded dataset contains {len(df)} records.")

        # Analyze comments
        if st.button("Analyze Comments"):
            with st.spinner("Analyzing comments..."):
                analyzed_df = restart_cont.analyze_comments(df, client, safety_info, guidelines, vocab, precursor)
            st.success("Analysis complete!")

            # Display top comments
            top_comments = restart_cont.get_top_comments(analyzed_df)
            st.subheader(f"Top {len(top_comments)} High-Value Comments:")
            for _, row in top_comments.iterrows():
                with st.expander(f"Obs Number: {row['OBSRVTN_NB']} - {row['PNT_NM']}"):
                    st.write(f"Comment: {row['PNT_ATRISKNOTES_TX']}")
                    st.write(f"Explanation: {row['explanation']}")

if __name__ == "__main__":
    main()