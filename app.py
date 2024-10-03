import streamlit as st
from llm_handler import get_confidence_scores
import pandas as  pd
st.title("Data Quality Score App")

# File upload option
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    data =pd.read_csv(uploaded_file)
    csv_content = uploaded_file.getvalue().decode("utf-8")
    st.write("Uploaded CSV:")
    st.dataframe(data)





    # Extract column names
    columns = csv_content.splitlines()[0].split(',')
    st.write("Detected columns:", columns)

    # Get confidence scores from the LLM
    data_description = "Your data description goes here"
    issue_confidence = get_confidence_scores(data_description, csv_content)


    # Display dropdown for each column with sliders inside
    st.subheader("Set Quality Scores for Each Column")

    for column in columns:
        with st.expander(f"### Column: {column}"):
            if column in issue_confidence["column-issues"]:
                for issue, confidence in issue_confidence["column-issues"][column].items():
                    slider_value = int(round(confidence * 4 + 1))  # Scale confidence from 0-1 to 1-5
                    st.slider(f"{issue} for {column}", 1, 5, slider_value)

            if column in issue_confidence["cell-issues"]:
                for issue, confidence in issue_confidence["cell-issues"][column].items():
                    slider_value = int(round(confidence * 4 + 1))  # Scale confidence from 0-1 to 1-5
                    st.slider(f"{issue} for {column}", 1, 5, slider_value)



