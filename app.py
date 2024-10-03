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


    # Display dropdown for each column with dropdown menus for attributes inside
    st.subheader("Set Quality Scores for Each Column")

    for column in columns:
        with st.expander(f"### Column: {column}"):
            if column in issue_confidence["column-issues"]:
                col1, col2, col3, col4 = st.columns(4)  # Create four columns for horizontal layout

                with col1:
                    issue = "Duplicated Values"
                    short_issue_name = "Duplicate"
                    confidence = issue_confidence["column-issues"][column].get(issue, 0)
                    select_value = int(round(confidence * 4 + 1))
                    st.selectbox(f"{short_issue_name}", options=[1, 2, 3, 4, 5], index=select_value-1, key=f"{column}_{issue}")

                with col2:
                    issue = "Outliers"
                    short_issue_name = "Outliers"
                    confidence = issue_confidence["column-issues"][column].get(issue, 0)
                    select_value = int(round(confidence * 4 + 1))
                    st.selectbox(f"{short_issue_name}", options=[1, 2, 3, 4, 5], index=select_value-1, key=f"{column}_{issue}")

                with col3:
                    issue = "Missing Values"
                    short_issue_name = "Missing"
                    confidence = issue_confidence["cell-issues"][column].get(issue, 0)
                    select_value = int(round(confidence * 4 + 1))
                    st.selectbox(f"{short_issue_name}", options=[1, 2, 3, 4, 5], index=select_value-1, key=f"{column}_{issue}")

                with col4:
                    issue = "Inconsistency"
                    short_issue_name = "Inconsistency"
                    confidence = issue_confidence["cell-issues"][column].get(issue, 0)
                    select_value = int(round(confidence * 4 + 1))
                    st.selectbox(f"{short_issue_name}", options=[1, 2, 3, 4, 5], index=select_value-1, key=f"{column}_{issue}")
