# Default Detective

In an increasingly complex financial landscape, the ability to accurately predict loan default risk has become paramount for financial institutions, lenders, and investors. This project aims to develop a robust and data-driven solution for loan default prediction, leveraging data preprocessing and feature engineering techniques, extensive data analysis and state-of-the-art machine learning algorithms. 

## Dataset
The Dataset used for the project is historical loan data from Small Business Administration (SBA) of the United States. The dataset contains 899,164 records and 27 features. The dataset is highly imbalanced with only 17.5% of the loans being defaulted. 

## Requirements

- Python
- Scikit-learn
- Pandas
- Streamlit
- FastAPI

## Installation

1. Install the dependencies.

    ```sh
        pip install -r requirements.txt 
    ```

## Usage

- Change the directory to the src folder and run the FastAPI server.
    
     ```sh
        uvicorn server:app --reload 
     ```

- Run the Streamlit app from root directory.

     ```sh
        streamlit run app.py 
     ```

## References

Min Li, Amy Mickel & Stanley Taylor (2018) “Should This Loan be Approved or Denied?”: A Large Dataset with Class Assignment Guidelines, Journal of Statistics Education, 26:1, 55-66, DOI: 10.1080/10691898.2018.1434342