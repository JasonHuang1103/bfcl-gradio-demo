import pandas as pd

def get_result(result_path):
    """
    Read CSV file and return DataFrame with relevant columns
    """
    df = pd.read_csv(result_path)
    return df[['entry_id', 'error_reason_type', 'error_reason_description', 'error_turn_id']]
