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
    # Main title with custom styling
    st.markdown('<h1 class="main-title">AI Resume Screening System</h1>', unsafe_allow_html=True)

    # Instructions section
    with st.container():
        st.markdown('<div class="instructions-card">', unsafe_allow_html=True)
        st.markdown("### How to Use This Tool")
        st.markdown("""
        <div class="fade-in">
        <p><span class="step-number">1</span> Enter the job description or use the sample job description button.</p>
        <p><span class="step-number">2</span> Upload one or more resumes (Supported formats: PDF, DOC, DOCX).</p>
        <p><span class="step-number">3</span> Click the "Process Resumes" button to start the analysis.</p>
        <p><span class="step-number">4</span> Review the detailed analysis results including:</p>
        <ul>
            <li>Overall match score</li>
            <li>Skills analysis</li>
            <li>Education and experience evaluation</li>
            <li>Document statistics</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Initialize components
    doc_processor = DocumentProcessor()
    nlp_analyzer = NLPAnalyzer()
    ml_scorer = MLScorer()

    # Job Description Input
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

    # Resume Upload Section
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.header("Resume Upload")
    uploaded_files = st.file_uploader(
        "Upload resumes (PDF, DOC, or DOCX format)",
        type=['pdf', 'doc', 'docx'],
        accept_multiple_files=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Store uploaded files in session state
    if uploaded_files:
        st.session_state['uploaded_files'] = uploaded_files

    # Process button
    if uploaded_files and job_description and st.button("Process Resumes"):
        with st.spinner('Processing resumes...'):
            try:
                results = []
                progress_bar = st.progress(0)

                for idx, file in enumerate(uploaded_files):
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

                    # Update progress
                    progress = int((idx + 1) / len(uploaded_files) * 100)
                    progress_bar.progress(progress)

                # Sort results by overall score
                results.sort(key=lambda x: x['scores']['overall_score'], reverse=True)

                # Display Results
                st.markdown('<div class="results-section fade-in">', unsafe_allow_html=True)
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
                            st.markdown("##### Matched Skills")
                            matched_skills = result['scores']['matched_skills']
                            if matched_skills:
                                st.markdown('<div class="skills-container">' + 
                                    ''.join([f'<span class="skills-tag matched-skill">{skill}</span>' for skill in matched_skills]) +
                                    '</div>', unsafe_allow_html=True)
                            else:
                                st.write("None found")

                        with col2:
                            st.markdown("##### Missing Skills")
                            missing_skills = result['scores']['missing_skills']
                            if missing_skills:
                                st.markdown('<div class="skills-container">' + 
                                    ''.join([f'<span class="skills-tag missing-skill">{skill}</span>' for skill in missing_skills]) +
                                    '</div>', unsafe_allow_html=True)
                            else:
                                st.write("None found")

                        # Document Statistics
                        st.subheader("Document Statistics")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Word Count", result['stats']['word_count'])
                        with col2:
                            st.metric("Sentence Count", result['stats']['sentence_count'])
                        with col3:
                            st.metric("Avg Word Length", f"{result['stats']['avg_word_length']:.1f}")

                        # Named Entities
                        st.subheader("Named Entities")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("##### Organizations")
                            orgs = result['entities']['ORGANIZATION']
                            if orgs:
                                st.markdown('<div class="skills-container">' + 
                                    ''.join([f'<span class="skills-tag">{org}</span>' for org in orgs]) +
                                    '</div>', unsafe_allow_html=True)
                            else:
                                st.write("None found")

                        with col2:
                            st.markdown("##### People")
                            people = result['entities']['PERSON']
                            if people:
                                st.markdown('<div class="skills-container">' + 
                                    ''.join([f'<span class="skills-tag">{person}</span>' for person in people]) +
                                    '</div>', unsafe_allow_html=True)
                            else:
                                st.write("None found")

                        with col3:
                            st.markdown("##### Locations")
                            locations = result['entities']['GPE']
                            if locations:
                                st.markdown('<div class="skills-container">' + 
                                    ''.join([f'<span class="skills-tag">{loc}</span>' for loc in locations]) +
                                    '</div>', unsafe_allow_html=True)
                            else:
                                st.write("None found")

                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()