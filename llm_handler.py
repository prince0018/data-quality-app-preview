import json
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables for API keys
load_dotenv()

# Initialize model
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Function to call the LLM and get confidence scores
def get_confidence_scores(data_description, csv_content):
    messages = [
        SystemMessage(
        content='''You are a part of an application you have to perform some tasks.

Context: It is an application which gives the quality score for tabular data on the basis of issues listed down.

issues = { 
    
    "column-issues": {
       column1Name:{
        "Duplicated Values": "confidence here",
        "Outliers": "confidence here",
        }
       column2Name:..........So On.
    },
    "cell-issues": {
        column1Name:{
        "Missing Values": "confidence here"
        "Inconsistency": "confidence here"
        }
       column2Name:..........So On.
    }
}

Confidence: It is basically the value between 0 to 1. And it states that how important the issue is with respect to a dataset. Means If confidence is close to 1 then issue is very important to user, and he don't want to ignore this issue. Means the weightage of issue will be more.

Description of issues:

Column-Level Issues:
1) Duplicated Values: Columns expected to have unique values (e.g., identifiers) but contain duplicates.
2) Outliers: Extreme values that are statistically distant from most of the values in the column.

Cell-Level Issues:
1) Missing Values: Null or empty values where data is expected (e.g., in non-nullable columns).
2) Inconsistency: Values that don't conform to expected formats, patterns, or domain constraints. For example, a date column containing a non-date value or a numerical column containing text.

Now these issues will have the different confidence score with respect to different columns of different dataset.

Task: You have to analyze the given dataset description and the dataset and its columns/features, understand the importance of issues for the given dataset and fill the below format with the confidence score keeping in mind the below given rules for each issues. 
Rules:
    Rules for Duplicate value issue:
    Below given features and similar to those will have duplicate value confidence 1
        -IDs, Primary Keys, Unique Keys, Identifiers.
        -Examples : user_id, order_id, transaction_id, email, but not limited to this.
        -These features are crucial for maintaining the uniqueness of records in a dataset.
    Below given features and similar to those will have duplicate value confidence 0
        -Categorical Features with No Uniqueness Requirement
        -Examples : gender, status, education_level, region, but not limited to this.
        -These features are used for classification and do not require unique values.
    For other features, assign confidence between 0 and 1 based on the importance of Duplicate value issue for that feature. So don't assign 0 and 1 only.

    Rules for Missing value issue:
    Below given features and similar to those will have missing value confidence 1:
        - Features that cannot have null values due to their critical nature in the dataset.
        - Examples: IDs, Primary Keys, mandatory fields like created_at, order_id, transaction_id, but not limited to this.
        - These are essential features where missing values would affect data integrity.
    Below given features and similar to those will have missing value confidence 0:
        - Features where missing data is acceptable or does not heavily impact analysis.
        - Examples: comments, feedback, review_text, secondary_contact_number, but not limited to this.
        - These are optional or free-text fields where null values are expected or permissible.
    For other features, assign confidence between 0 and 1 based on the importance of missing values for that feature. So don't assign 0 and 1 only.

    Rules for Outlier issue:
    Below given features and similar to those will have outlier confidence 1:
        - Numeric Features with Defined Ranges, Sensitive Data.
        - Examples: salary, age, percentage, transaction_amount, but not limited to this.
        - These features must remain within specific thresholds, and outliers could distort analysis or represent errors.
    Below given features and similar to those will have outlier confidence 0:
        - Features where outliers are either expected or do not significantly impact analysis.
        - Examples: gender, education_level, region, feedback, comments, but not limited to this.
        - Categorical or free-text fields where there is no concept of outliers.
    For other features, assign confidence between 0 and 1 based on the importance of outlier for that feature. So don't assign 0 and 1 only.

    Rules for Inconsistency Issue:
    Below given features and similar to those will have inconsistency issue confidence 1.
        - Features where data must adhere strictly to specific datatype, formats, patterns, or domains.
        - Examples: IDs, Primary Keys, Unique Keys, Identifiers, date_of_birth (must follow date format), email (must follow a valid email pattern), phone_number (must follow a valid number pattern), but not limited to this.
        - These features have strict requirements for data integrity, and inconsistent values could represent significant errors.
    Below given features and similar to those will have inconsistency issue confidence 0.
        - Features where there is no strict requirement for format or pattern adherence.
        - Examples: comments, feedback, review_text.
        - These are free-text or optional fields where data variation is expected, and inconsistency does not significantly affect the analysis.
    For other features, assign confidence between 0 and 1 based on the importance of data consistency for that feature. So don't assign 0 and 1 only.

Output Format:

issues-confidence = { 
    
    "column-issues": {
       column1Name:{ 
        "Duplicated Values": "confidence here",
        "Outliers": "confidence here",
        }
       column2Name:..........So On.
    },
    "cell-issues": {
        column1Name:{ 
        "Missing Values": "confidence here"
        "Inconsistency": "confidence here"
        }
       column2Name:..........So On.
    }
}

Output: 
Fill the format given above and return it in json. Don't write anything else.

'''
    ),
    HumanMessage(
        content=f"""
        Data Description: {data_description}
        Data: {csv_content}
        """
    )
        
    ]

    # Invoke the model four times for redundancy
    result1 = model.invoke(messages)
    result2 = model.invoke(messages)
    result3 = model.invoke(messages)
    result4 = model.invoke(messages)

    # Helper function to clean and convert LLM response to JSON
    def LLM_result_to_JSON(result):
        cleaned_content = result.content.replace('```json', '').replace('```', '').strip()
        return json.loads(cleaned_content)

    responses = [
        LLM_result_to_JSON(result1),
        LLM_result_to_JSON(result2),
        LLM_result_to_JSON(result3),
        LLM_result_to_JSON(result4),
    ]

    # Average the results
    return average_responses(responses)

# Function to average the confidence scores from multiple responses
def average_responses(responses):
    result = {}
    num_responses = len(responses)

    for response in responses:
        for issue_type, columns in response.items():
            if issue_type not in result:
                result[issue_type] = {}
            for column, metrics in columns.items():
                if column not in result[issue_type]:
                    result[issue_type][column] = {}
                for metric, value in metrics.items():
                    if metric not in result[issue_type][column]:
                        result[issue_type][column][metric] = 0
                    result[issue_type][column][metric] += float(value)

    for issue_type, columns in result.items():
        for column, metrics in columns.items():
            for metric in metrics:
                result[issue_type][column][metric] /= num_responses

    return result
