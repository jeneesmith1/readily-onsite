import unittest
import pandas as pd
import io
import os

# For this example, we'll put the functions directly in this script.

def split_source_csv_by_table_headers(source_csv):
    """
    Finds and returns a DataFrame of header indices and names from the source CSV.
    """
    df = source_csv.iloc[:, 0]
    table_header = "Element"
    is_row_table_header_df = df.loc[df.fillna('').str.startswith(table_header)].copy()
    header_row_table = pd.DataFrame({
        'HeaderIndices': is_row_table_header_df.index,
        'HeaderName': is_row_table_header_df.values
    })
    return header_row_table

def helper_create_pairs(data):
    """
    Creates pairs of start and end indices for slicing.
    """
    return [[data[i], data[i+1]] for i in range(len(data) - 1)]

def get_element_and_index(policy_row, split_element):
    """
    Splits a string by a delimiter and returns a cleaned list.
    """
    parts = policy_row.split(split_element)
    if len(parts) >= 2:
        element_index = parts[0].strip()
        element = split_element.join(parts[1:]).strip()
        return [element_index, element]
    else:
        return [None, policy_row.strip()]

class TestIngestionFunctions(unittest.TestCase):
    """
    Test suite for the data ingestion functions.
    """

    def setUp(self):
        """
        Set up a mock CSV file and DataFrame for testing.
        This runs before each test method.
        """
        self.mock_csv_content = """
        ,<<YYYY> Annual Oversight CLAIMS and PDRs Audit ,,,,,,,,
        ,<<ENTER DELEGATE>>,,,,,,,,
        ,Audit Period: <<enter audit period>>,,,,,,,,
        ,Audit Scope: <<enter LIMITED or FULL>>,,,,,,,,
        ,,,,,,,,,,
        ,Claims and PDRs Policy and Procedure Review,,,,,,,,
        ,,,,,,,,,,
        ,"Element A: Claims Processing",Audit Elements,,,,,
        ,"28 CCR 1300.71 (a)(2) (a)-(f)",1. Policy and procedure(s) outlining the organization's mail room process,,,,,,
        ,"28 CCR 1300.71(b)(1)-(3)",2. Policy or procedure(s) identifying the organization shall not impose a deadline,,,,,
        ,"Element B: Interest & Penalties",,,,,,,,
        ,"28 CCR 1300.71.38 (a)",3. Policies and procedure(s) establishing the organization's process for paying interest,,,,,,
        """
        # Read the mock content into a DataFrame, skipping initial rows
        self.mock_df = pd.read_csv(io.StringIO(self.mock_csv_content), skiprows=6, usecols=[1, 2], header=None)

    def test_split_source_csv_by_table_headers(self):
        """
        Test that split_source_csv_by_table_headers correctly identifies headers.
        """
        expected_indices = [2, 5]
        expected_names = ["Element A: Claims Processing", "Element B: Interest & Penalties"]
        
        result_df = split_source_csv_by_table_headers(self.mock_df)
        
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertListEqual(result_df['HeaderIndices'].tolist(), expected_indices)
        self.assertListEqual(result_df['HeaderName'].tolist(), expected_names)

    def test_helper_create_pairs(self):
        """
        Test that helper_create_pairs correctly creates index pairs.
        """
        data = [12, 20, 30, 39, 48]
        expected_pairs = [[12, 20], [20, 30], [30, 39], [39, 48]]
        
        result_pairs = helper_create_pairs(data)
        
        self.assertIsInstance(result_pairs, list)
        self.assertListEqual(result_pairs, expected_pairs)

    def test_get_element_and_index(self):
        """
        Test that get_element_and_index correctly splits strings.
        """
        # Test a standard case with a colon delimiter
        standard_string = "Element A: claims processing"
        expected_standard = ["Element A", "claims processing"]
        self.assertListEqual(get_element_and_index(standard_string, ":"), expected_standard)
        
        # Test a case with an irregular delimiter (period)
        period_string = "1. Policy and procedure(s)"
        expected_period = ["1", "Policy and procedure(s)"]
        self.assertListEqual(get_element_and_index(period_string, "."), expected_period)
        
        # Test a case with no delimiter
        no_delimiter_string = "No delimiter here"
        expected_no_delimiter = [None, "No delimiter here"]
        self.assertListEqual(get_element_and_index(no_delimiter_string, ":"), expected_no_delimiter)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)