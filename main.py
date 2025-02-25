import streamlit as st
import time
from utils.document_processor import DocumentProcessor
from utils.nlp_analyzer import NLPAnalyzer
from utils.ml_scorer import MLScorer
import base64

# Load custom CSS
with open('styles/main.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.title("AI Resume Screening System")
    st.markdown("Upload resumes and job description to get AI-powered analysis and ranking")

    # Initialize components
    doc_processor = DocumentProcessor()
    nlp_analyzer = NLPAnalyzer()
    ml_scorer = MLScorer()

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
        Bachelor's degree in Computer Science or related field required
        """
        st.session_state['job_description'] = job_description
        st.rerun()

    # Resume Upload Section
    st.header("Resume Upload")
    uploaded_files = st.file_uploader(
        "Upload resumes (PDF, DOC, or DOCX format)",
        type=['pdf', 'doc', 'docx'],
        accept_multiple_files=True
    )

    if uploaded_files and job_description:
        with st.spinner('Processing resumes...'):
            try:
                results = []
                for file in uploaded_files:
                    # Extract text from document
                    resume_text = doc_processor.extract_text(file)

                    # Get document statistics
                    doc_stats = doc_processor.get_document_stats(resume_text)

                    # Extract entities
                    entities = nlp_analyzer.extract_entities(resume_text)

                    # Calculate advanced scores
                    scores = ml_scorer.calculate_advanced_scores(job_description, resume_text)

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
                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            st.metric("Content Match", f"{result['scores']['content_similarity']}%")
                        with col2:
                            st.metric("Skills Match", f"{result['scores']['skills_match']}%")
                        with col3:
                            st.metric("Education", f"{result['scores']['education_level']}%")
                        with col4:
                            st.metric("Experience", f"{result['scores']['experience_level']}%")

                        # Skills Analysis
                        st.subheader("Skills Analysis")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("Matched Skills")
                            st.write(", ".join(result['scores']['matched_skills']) if result['scores']['matched_skills'] else "None found")
                        with col2:
                            st.write("Missing Skills")
                            st.write(", ".join(result['scores']['missing_skills']) if result['scores']['missing_skills'] else "None found")

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