import streamlit as st
import os
import tempfile
import pandas as pd
import plotly.express as px

# Import all our backend functions
from src.figure_extractor import extract_figures
from src.visual_analyzer import categorize_figure, extract_keywords, estimate_complexity, parse_table
from src.image_authenticity import check_image_authenticity

# Use Streamlit's caching to avoid re-running the full analysis on every interaction
@st.cache_data
def run_full_analysis(pdf_path):
    """
    Runs the entire backend pipeline from PDF to structured metadata.
    """
    # Phase 1: Extract figures, captions, and OCR text
    figure_data = extract_figures(pdf_path)

    # Phases 2 & 3: Analyze each figure
    for data in figure_data:
        image_path = data["image_path"]
        ocr_text = data["ocr_text"]
        caption = data["caption"]

        # Run metadata enrichment and complexity scoring
        data["category"] = categorize_figure(image_path, ocr_text)
        data["keywords"] = extract_keywords(caption)
        data["complexity_score"] = estimate_complexity(image_path, ocr_text)

        # Run authenticity check
        auth_label, auth_score = check_image_authenticity(image_path)
        data["authenticity_label"] = auth_label
        data["authenticity_score"] = auth_score

        # If it's a table, try to parse it
        if data["category"] == "table":
            data["table_data"] = parse_table(image_path)
        else:
            data["table_data"] = None
            
    return figure_data

def main():
    # --- PAGE CONFIGURATION ---
    st.set_page_config(
        page_title="Scientific PDF Visuals Unlocker",
        page_icon="🔬",
        layout="wide"
    )

    # --- HEADER ---
    st.title("🔬 Scientific PDF Visuals Unlocker")
    st.write("Upload a scientific PDF to extract figures, analyze content, and check for AI-generated assets.")

    # --- FILE UPLOADER ---
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Upload a scientific article in PDF format to begin analysis."
    )

    # --- ANALYSIS WORKFLOW ---
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_pdf_path = tmp_file.name

        st.success(f"File '{uploaded_file.name}' uploaded successfully.")
        
        if st.button("Analyze PDF"):
            with st.spinner("Running full analysis pipeline... This may take a few minutes."):
                analysis_results = run_full_analysis(tmp_pdf_path)
            
            st.success("Full analysis complete!")
            
            # --- DISPLAY SUMMARY VISUALIZATION ---
            st.header("Overall Authenticity Summary")
            
            if not analysis_results:
                st.warning("No figures were found in this PDF.")
            else:
                # Aggregate the results for the pie chart
                labels = [res['authenticity_label'] for res in analysis_results]
                human_count = labels.count('Human-created')
                ai_count = labels.count('AI-generated image')

                if human_count + ai_count > 0:
                    pie_data = pd.DataFrame({
                        'Category': ['Human-created', 'AI-generated'],
                        'Count': [human_count, ai_count]
                    })
                    fig = px.pie(pie_data, values='Count', names='Category',
                                 title='Ratio of Human vs. AI-Generated Figures',
                                 color_discrete_map={'Human-created':'green', 'AI-generated':'red'})
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Could not determine authenticity for any figures.")

            # --- DISPLAY DETAILED RESULTS ---
            st.header("Detailed Figure-by-Figure Analysis")
            
            if analysis_results:
                st.info(f"Found {len(analysis_results)} figures. See details below:")
                for i, data in enumerate(analysis_results):
                    st.subheader(f"Figure {i + 1}")
                    col1, col2 = st.columns([1, 1.5])
                    with col1:
                        st.image(data["image_path"])
                    with col2:
                        st.metric(label="Complexity Score", value=f"{data['complexity_score']}/10")
                        auth_label = data['authenticity_label']
                        auth_score = data['authenticity_score']
                        if "AI-generated" in auth_label:
                            st.error(f"Authenticity: {auth_label} (Confidence: {auth_score:.2f})")
                        else:
                            st.success(f"Authenticity: {auth_label} (Confidence: {auth_score:.2f})")
                        st.info(f"Detected Category: **{data['category'].upper()}**")
                        if data["caption"]:
                            st.caption(f"Detected Caption: {data['caption']}")
                            if data["keywords"]:
                                st.write("**Keywords:**")
                                st.write(", ".join(data["keywords"]))
                        else:
                            st.caption("No caption found for this figure.")
                    with st.expander("Show Text Extracted from Figure (OCR)"):
                        st.text(data["ocr_text"] if data["ocr_text"] else "No text found in this figure.")
                    if data["table_data"]:
                        with st.expander("Show Parsed Table Data (CSV)"):
                            df = pd.DataFrame(data["table_data"])
                            st.dataframe(df)
        
        if os.path.exists(tmp_pdf_path):
             os.remove(tmp_pdf_path)

if __name__ == "__main__":
    main()