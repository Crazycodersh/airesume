# Resume Screening App - File Structure and Contents

1. Create the following directory structure:
```
resume-screening-app/
├── .streamlit/
│   └── config.toml
├── utils/
│   ├── pdf_processor.py
│   ├── nlp_analyzer.py
│   └── resume_ranker.py
├── styles/
│   └── main.css
└── main.py
```

2. Place each file in its corresponding directory with the contents provided below.

## File Contents:

### main.py (place in root directory)
```python
import streamlit as st
import time
from utils.pdf_processor import PDFProcessor
from utils.nlp_analyzer import NLPAnalyzer
from utils.resume_ranker import ResumeRanker
import base64

# Load custom CSS
with open('styles/main.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.title("AI Resume Screening System")
    st.markdown("Upload resumes and job description to get AI-powered analysis and ranking")

    # Initialize components
    pdf_processor = PDFProcessor()
    nlp_analyzer = NLPAnalyzer()
    resume_ranker = ResumeRanker()

    # Job Description Input
    st.header("Job Description")
    job_description = st.text_area(
        "Enter the job description",
        height=200,
        placeholder="Paste the job description here..."
    )

    # Sample job description loader
    if st.button("Load Sample Job Description"):
        job_description = """
        Senior Software Engineer
        Requirements:
        - 5+ years of experience in Python development
        - Strong knowledge of web frameworks (Django, Flask)
        - Experience with cloud platforms (AWS, GCP)
        - Background in machine learning and data analysis
        - Excellent communication and team collaboration skills
        """
        st.session_state['job_description'] = job_description
        st.rerun()

    # Resume Upload Section
    st.header("Resume Upload")
    uploaded_files = st.file_uploader(
        "Upload resumes (PDF format)",
        type=['pdf'],
        accept_multiple_files=True
    )

    if uploaded_files and job_description:
        with st.spinner('Processing resumes...'):
            try:
                results = []
                for file in uploaded_files:
                    # Extract text from PDF
                    resume_text = pdf_processor.extract_text(file)

                    # Get document statistics
                    doc_stats = pdf_processor.get_document_stats(resume_text)

                    # Extract entities
                    entities = nlp_analyzer.extract_entities(resume_text)

                    # Calculate scores
                    scores = resume_ranker.calculate_score_breakdown(job_description, resume_text)

                    results.append({
                        'filename': file.name,
                        'text': resume_text,
                        'stats': doc_stats,
                        'entities': entities,
                        'scores': scores
                    })

                # Sort results by overall score
                results.sort(key=lambda x: x['scores']['overall_score'], reverse=True)

                # Display Results
                st.header("Analysis Results")

                for idx, result in enumerate(results, 1):
                    with st.expander(f"#{idx} - {result['filename']} (Score: {result['scores']['overall_score']}%)"):
                        # Score Breakdown
                        st.subheader("Score Breakdown")
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric("Content Match", f"{result['scores']['content_similarity']}%")
                        with col2:
                            st.metric("Keyword Match", f"{result['scores']['keyword_match']}%")
                        with col3:
                            st.metric("Length Score", f"{result['scores']['length_score']}%")

                        # Document Statistics
                        st.subheader("Document Statistics")
                        st.write(f"Word Count: {result['stats']['word_count']}")
                        st.write(f"Sentence Count: {result['stats']['sentence_count']}")
                        st.write(f"Average Word Length: {result['stats']['avg_word_length']:.2f}")

                        # Named Entities
                        st.subheader("Named Entities")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write("Organizations")
                            st.write(", ".join(result['entities']['ORGANIZATION']) if result['entities']['ORGANIZATION'] else "None found")
                        with col2:
                            st.write("People")
                            st.write(", ".join(result['entities']['PERSON']) if result['entities']['PERSON'] else "None found")
                        with col3:
                            st.write("Locations")
                            st.write(", ".join(result['entities']['GPE']) if result['entities']['GPE'] else "None found")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
```

Would you like me to provide the contents of the other files as well?
