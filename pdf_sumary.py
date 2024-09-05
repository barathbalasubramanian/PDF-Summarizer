import streamlit as st
from PyPDF2 import PdfReader
from transformers import pipeline

# Initialize summarization pipeline
summarizer = pipeline("summarization")

def extract_text_from_pdf(pdf):
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def summarize_text(text):
    try:
        summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error: Unable to generate summary. Details: {str(e)}"

def summarizer(pdf):
    text = extract_text_from_pdf(pdf)
    if len(text) > 0:
        summary = summarize_text(text)
        return summary
    else:
        return "No text found in the PDF."

def main():
    st.set_page_config(page_title="PDF Summarizer")
    st.title("PDF Summarizing App with Transformers")
    st.write("Summarize your PDF files in a few seconds.")

    # File uploader for PDF
    pdf = st.file_uploader("Upload your PDF Document", type="pdf")
    submit = st.button("Generate Summary")

    # Generate and display the summary
    if submit and pdf is not None:
        response = summarizer(pdf)
        if response:
            st.subheader("Summary of file:")
            st.write(response)
        else:
            st.error("Could not generate summary. Please check the uploaded file.")
    elif submit:
        st.error("Please upload a PDF file.")

if __name__ == "__main__":
    main()
