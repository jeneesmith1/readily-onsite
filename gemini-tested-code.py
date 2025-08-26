# CODE FROM PROMPT 4

# import pandas as pd
# import io

# # When running locally, use the actual path to your file.
# # The `content_fetcher` tool is not a standard library.
# # We'll use a placeholder for the local file path.
# file_path = "source.csv"

# try:
#     # Use the local file path to read the CSV.
#     # We set the 'header' parameter to a list of row indices.
#     # The snippet shows the top-level header is on row 8 (index 7)
#     # and the sub-header is on row 9 (index 8).
#     df = pd.read_csv(file_path, header=[7, 8])

#     def get_columns_under_header(df: pd.DataFrame, top_level_header: str) -> list:
#         """
#         Groups all columns that fall under a specific top-level header.

#         Args:
#             df: The pandas DataFrame with a multi-index header.
#             top_level_header: The string of the top-level header to find.

#         Returns:
#             A list of tuples representing the full column names under the
#             specified top-level header.
#         """
#         # The column names are tuples. We can filter them based on the first
#         # element of the tuple, which corresponds to the top-level header.
#         # We also want to exclude the unnamed columns from the grouping.
#         grouped_columns = [
#             col for col in df.columns
#             if isinstance(col, tuple) and col[0] == top_level_header
#         ]
#         return grouped_columns

#     # First, let's find all unique top-level headers in the DataFrame.
#     # We can get the first level of the column index and get its unique values.
#     # We filter out any 'Unnamed' columns which don't belong to a group.
#     unique_top_level_headers = [
#         col for col in df.columns.get_level_values(0).unique()
#         if not col.startswith('Unnamed:')
#     ]

#     print("Found the following top-level headers:")
#     for header in unique_top_level_headers:
#         print(f"- {header}")

#     # Now, we can use our new function to dynamically group columns for each header.
#     print("\n-----------------------------------------------------")
#     for header in unique_top_level_headers:
#         # Get the columns under the current top-level header.
#         columns_to_group = get_columns_under_header(df, header)
        
#         if columns_to_group:
#             print(f"\nColumns grouped under '{header}':")
#             # We can now select and display data for these dynamically grouped columns.
#             # Here, we'll print the column names for verification.
#             print(columns_to_group)
            
#             # Example of how to access the data. We'll show the first 5 rows.
#             print(f"\nFirst 5 rows for the columns under '{header}':")
#             print(df[columns_to_group].head())
#         else:
#                 print(f"\nNo columns found under the top-level header '{header}'.")

# except Exception as e:
#     print(f"An error occurred: {e}")

# CODE FROM PROMPT 5

# import pandas as pd
# import io

# # This script is designed to handle a CSV with multiple, repeating header sections.
# # Instead of using a fixed header row, we will parse the file line-by-line
# # to identify and group each 'Element' section (e.g., Element A, Element B, etc.).

# def parse_multi_section_csv(file_content: str) -> dict:
#     """
#     Parses a CSV file with repeating header sections and returns a dictionary
#     where each key is a top-level header (e.g., 'Element A') and the value
#     is a DataFrame containing the data for that section.

#     Args:
#         file_content: The content of the CSV file as a string.

#     Returns:
#         A dictionary of pandas DataFrames, one for each section.
#     """
#     # Read the entire CSV into a list of lists, without headers.
#     print("START OF PARSE")
#     data_lines = [line.strip().split(',') for line in file_content.splitlines()]
#     print("DATA LINES", data_lines)

#     sections = {}
#     current_section_name = None
#     section_data_start = None

#     for i, row in enumerate(data_lines):
#         # A simple way to detect the start of a new section is to look for a
#         # cell that starts with "Element ". This assumes the top-level
#         # header is always in the first column.
#         if row and row[0].strip().startswith('Element '):
#             # This is a new section header.
#             if current_section_name and section_data_start:
#                 # We've finished collecting data for the previous section.
#                 # Now we need to process it. The sub-headers are on the
#                 # row immediately after the blank row following the section header.
#                 header_row_index = section_data_start + 1
#                 data_rows = data_lines[header_row_index + 1 : i]
#                 sub_headers = data_lines[header_row_index]

#                 # Create a DataFrame for this section using the sub_headers.
#                 section_df = pd.DataFrame(data_rows, columns=sub_headers)
                
#                 # Clean up the DataFrame by dropping rows that are all NaN/empty.
#                 section_df.dropna(how='all', inplace=True)
                
#                 sections[current_section_name] = section_df

#             # Start of a new section.
#             current_section_name = row[0].strip()
#             print("CURRENT SECTION NAME: ", current_section_name)
#             section_data_start = i
            
#     # Process the final section after the loop.
#     if current_section_name and section_data_start:
#         header_row_index = section_data_start + 1
#         data_rows = data_lines[header_row_index + 1:]
#         sub_headers = data_lines[header_row_index]

#         section_df = pd.DataFrame(data_rows, columns=sub_headers)
#         section_df.dropna(how='all', inplace=True)
#         sections[current_section_name] = section_df
#         print("SECTIONS", sections)

#     return sections

# try:
#     # Read the file content as a string, which is what the function expects.
#     with open("source.csv", 'r') as file:
#         file_content = file.read()
    

#     # Use the new function to parse the file into a dictionary of DataFrames.
#     parsed_sections = parse_multi_section_csv(file_content)

#     print("Successfully parsed the CSV into multiple sections.: ", parsed_sections )
    
#     # Iterate through the dictionary and print the contents of each section.
#     for section_name, df in parsed_sections.items():
#         print(f"\n--- Section: {section_name} ---")
#         print("Column Headers:")
#         print(df.columns.tolist())
#         print("\nFirst 5 Rows of Data:")
#         print(df.head().to_string())
#         print("-" * 20)

# except Exception as e:
#     print(f"An error occurred: {e}")

# CODE FROM PROMPT 6

# import pandas as pd
# import io

# # # When running locally, use the actual path to your file.
# # # The `content_fetcher` tool is not a standard library.
# # # We'll use a placeholder for the local file path.
# file_path = "source.csv"

#     sections = {}
#     current_section_start = None

#     # We'll use a for loop to iterate through the lines and find the start of each section.
#     for i, line in enumerate(file_path):
#         # A new section starts when a line begins with "Element".
#         if line.strip().startswith('Element '):
#             if current_section_start is not None:
#                 # We have found a new section, so the previous one has ended.
#                 # Extract the section's lines and read them into a DataFrame.
#                 section_lines = lines[current_section_start:i]
                
#                 # The headers for the section are on the second line.
#                 section_header_line = section_lines[1]
                
#                 # The data for the section starts on the third line.
#                 section_data_lines = section_lines[2:]
                
#                 # Re-create a string for just this section to be read by pandas.
#                 section_content = section_header_line + '\n' + '\n'.join(section_data_lines)
                
#                 # Use io.StringIO to treat the string as a file.
#                 df = pd.read_csv(io.StringIO(section_content))

# 

# import pandas as pd
# import io
# import content_fetcher

# def create_pairs(data: list) -> list:
#     """
#     Takes a list of numbers and creates an array of pairs, where each pair
#     contains a start and end point from the original list.

#     Args:
#         data: A list of numbers, e.g., [0, 12, 20, 30].

#     Returns:
#         A new list containing pairs, e.g., [[0, 12], [12, 20], [20, 30]].
#     """
#     # Use a list comprehension to iterate through the list.
#     # We stop one element before the end to avoid an index out of bounds error.
#     return [[data[i], data[i+1]] for i in range(len(data) - 1)]

# def process_by_index_range(source_df: pd.DataFrame, index_pairs: list) -> dict:
#     """
#     Iterates over a DataFrame using a list of index pairs and returns a
#     dictionary of DataFrames, with each key representing a section.

#     Args:
#         source_df: The DataFrame to iterate over.
#         index_pairs: A list of lists, where each inner list contains a start and
#                      end index for a slice, e.g., [[0, 12], [12, 20]].

#     Returns:
#         A dictionary of DataFrames.
#     """
#     tables = {}
#     for i, (start, end) in enumerate(index_pairs):
#         sub_df = source_df.iloc[start:end].copy()
        
#         # Use a descriptive key for each table in the dictionary.
#         key = f"Table_{i+1}_rows_{start}_to_{end-1}"
#         tables[key] = sub_df
        
#     return tables

# # Example Usage
# if __name__ == "__main__":
#     # Assuming 'source.csv' is available in the local directory.
#     # We will read the file here to demonstrate the full workflow.
#     try:
#         source_df = pd.read_csv("source.csv")
#     except FileNotFoundError:
#         print("Error: 'source.csv' not found. Please make sure it's in the same directory.")
#         source_df = pd.DataFrame() # Create an empty DataFrame to prevent errors
    
#     # We'll create a dummy list of indices to demonstrate the slicing.
#     # In your case, this would come from your previous function.
#     # Example indices
#     indices = [12, 20, 30, 39, 48]
    
#     # Create the pairs using the new function
#     index_pairs = create_pairs(indices)
    
#     print("Created index pairs:", index_pairs)
    
#     if not source_df.empty:


# CODE FOR PROMPT 12

# import pandas as pd
# import io

# # I've commented out the file reading part since it's an external file.
# # You will need to uncomment and set the correct file path to run this locally.
# source_csv = pd.read_csv("source.csv", skiprows=6, usecols=[1,2])
# # print("SOURCE CSV", source_csv)

# def split_source_csv_by_table_headers(source_csv):
#     """
#     Finds and returns a DataFrame of header indices and names from the source CSV.
#     """
#     # Use .iloc to get the first column as a Series.
#     df = source_csv.iloc[:, 0]
#     table_header = "Element"

#     # Use .fillna('') to safely handle NaNs before checking for the string.
#     is_row_table_header_df = df.loc[df.fillna('').str.startswith(table_header)].copy()

#     header_row_table = pd.DataFrame({
#         'HeaderIndices': is_row_table_header_df.index,
#         'HeaderName': is_row_table_header_df.values
#     })
#     return header_row_table

# def helper_create_pairs(data):
#     """
#     Creates pairs of start and end indices for slicing.
#     """
#     return [[data[i], data[i+1]] for i in range(len(data) - 1)]

# def get_element_and_index(policy_row, split_element):
#     """
#     Splits a string by a delimiter and returns a cleaned list.
#     """
#     # The split() method breaks the string into a list of substrings
#     # based on the delimiter.
#     parts = policy_row.split(split_element)

#     # We expect exactly two parts after the split. If not, the input
#     # format is incorrect, so we'll return a default.
#     if len(parts) >= 2:
#         # Use .strip() to remove any leading or trailing whitespace.
#         element_index = parts[0].strip()
#         # Join the rest of the parts in case the delimiter appears multiple times.
#         element = split_element.join(parts[1:]).strip()
#         return [element_index, element]
#     else:
#         # Return a list with the original string if no delimiter is found.
#         return [None, policy_row.strip()]

# def get_requirement_elements(requirement_data):
#     """
#     Processes a Series of requirement strings to extract index and element.
#     """
#     print("Requirement Data")
#     # Iterate over the values of the Series, not the indices.
#     # The get_element_and_index function will handle the parsing.
#     parsed_elements = [get_element_and_index(item, ".") for item in requirement_data if pd.notna(item)]
    
#     # Optional: return a DataFrame for better structure
#     df_requirements = pd.DataFrame(parsed_elements, columns=['RequirementIndex', 'Requirement'])
#     print(df_requirements)
#     return df_requirements

# def get_citations_and_requirement_elements(policy_table):
#     """
#     Extracts citations and requirement elements from a policy table DataFrame.
#     """
#     # Remove the first two rows (the headers).
#     index_array_no_header_rows = policy_table.iloc[2:].copy()
    
#     # Get the citations from the first column.
#     citations = index_array_no_header_rows.iloc[:, 0]
    
#     # Get the requirement items from the second column.
#     requirement_items = get_requirement_elements(index_array_no_header_rows.iloc[:, 1])

#     # Combine citations and requirement items into a single DataFrame.
#     result_df = pd.DataFrame()
#     # Ensure both have the same index for correct joining.
#     if not citations.empty and not requirement_items.empty:
#       result_df['Citations'] = citations.values
#       result_df['RequirementIndex'] = requirement_items['RequirementIndex'].values
#       result_df['Requirement'] = requirement_items['Requirement'].values

#     return result_df

# def create_tables(source_csv, header_row_table):
#     """
#     Creates and processes tables based on the header indices.
#     """
#     all_tables = pd.DataFrame() # An empty DataFrame to store all results.
    
#     # Add a final index to the header table to process the last table.
#     final_index = pd.DataFrame({
#       'HeaderIndices': [len(source_csv)],
#       'HeaderName': ['EndOfFile']
#     })
#     header_row_table = pd.concat([header_row_table, final_index], ignore_index=True)
    
#     # Get indices pairs to start creating table.
#     indices_array = helper_create_pairs(header_row_table.HeaderIndices)
    
#     for start, end in indices_array:
#         policy_table = source_csv.iloc[start:end].dropna(how='all').copy()
        
#         # Check if the policy table is not empty before processing.
#         if not policy_table.empty:
#             citations_requirements = get_citations_and_requirement_elements(policy_table)
            
#             # Add the current table's data to the overall DataFrame.
#             all_tables = pd.concat([all_tables, citations_requirements], ignore_index=True)

#     return all_tables

# # --- Main Execution ---
# # Assumes 'source.csv' exists in the same directory.
# try:
#     source_csv = pd.read_csv("source.csv", skiprows=6, usecols=[1, 2], header=None)
#     header_row_table = split_source_csv_by_table_headers(source_csv)
#     final_structured_df = create_tables(source_csv=source_csv, header_row_table=header_row_table)
#     print("\n--- Final Structured DataFrame ---")
#     print(final_structured_df.to_string())

# except FileNotFoundError:
#     print("Error: 'source.csv' not found. Please ensure it is in the same directory as the script.")
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")


# CODE FOR PROMPT 13

import pandas as pd
import io
import os

def split_source_csv_by_table_headers(source_csv):
    """
    Finds and returns a DataFrame of header indices and names from the source CSV.
    """
    # Use .iloc to get the first column as a Series.
    df = source_csv.iloc[:, 0]
    table_header = "Element"

    # Use .fillna('') to safely handle NaNs before checking for the string.
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
    # The split() method breaks the string into a list of substrings
    # based on the delimiter.
    parts = policy_row.split(split_element)

    # We expect at least two parts after the split. If not, the input
    # format is incorrect, so we'll return a default.
    if len(parts) >= 2:
        # Use .strip() to remove any leading or trailing whitespace.
        element_index = parts[0].strip()
        # Join the rest of the parts in case the delimiter appears multiple times.
        element = split_element.join(parts[1:]).strip()
        return [element_index, element]
    else:
        # Return a list with the original string if no delimiter is found.
        return [None, policy_row.strip()]

def get_requirement_elements(requirement_data):
    """
    Processes a Series of requirement strings to extract index and element.
    """
    # Iterate over the values of the Series, not the indices.
    # The get_element_and_index function will handle the parsing.
    parsed_elements = [get_element_and_index(item, ".") for item in requirement_data if pd.notna(item)]
    
    # Return a DataFrame for better structure.
    df_requirements = pd.DataFrame(parsed_elements, columns=['RequirementIndex', 'Requirement'])
    return df_requirements

def get_citations_and_requirement_elements(policy_table, header_name):
    """
    Extracts citations and requirement elements from a policy table DataFrame.
    """
    # Remove the first two rows (the headers).
    index_array_no_header_rows = policy_table.iloc[2:].copy()
    
    # Get the citations from the first column.
    citations = index_array_no_header_rows.iloc[:, 0].reset_index(drop=True)
    
    # Get the requirement items from the second column.
    requirement_items = get_requirement_elements(index_array_no_header_rows.iloc[:, 1].reset_index(drop=True))

    # Combine citations and requirement items into a single DataFrame.
    if not citations.empty and not requirement_items.empty:
      result_df = pd.DataFrame()
      result_df['Citations'] = citations.values
      result_df['RequirementIndex'] = requirement_items['RequirementIndex'].values
      result_df['Requirement'] = requirement_items['Requirement'].values
      return result_df
    
    return pd.DataFrame()

def create_tables(source_csv, header_row_table):
    """
    Creates and processes tables based on the header indices.
    """
    all_tables = pd.DataFrame() # An empty DataFrame to store all results.
    
    # Add a final index to the header table to process the last table.
    final_index = pd.DataFrame({
      'HeaderIndices': [len(source_csv)],
      'HeaderName': ['EndOfFile']
    })
    header_row_table = pd.concat([header_row_table, final_index], ignore_index=True)
    
    # Get indices pairs to start creating table.
    indices_array = helper_create_pairs(header_row_table.HeaderIndices)
    
    for i, (start, end) in enumerate(indices_array):
        policy_table = source_csv.iloc[start:end].dropna(how='all').copy()
        
        # Check if the policy table is not empty before processing.
        if not policy_table.empty:
            # Get the top-level header information for the current table.
            top_level_header = header_row_table.iloc[i]['HeaderName']
            element_index, element = get_element_and_index(top_level_header, ":")
            
            # Extract citations and requirements for the current table.
            citations_requirements = get_citations_and_requirement_elements(policy_table, top_level_header)
            
            # Add the top-level header info to the new DataFrame.
            if not citations_requirements.empty:
                citations_requirements.insert(0, 'Element', element)
                citations_requirements.insert(0, 'ElementIndex', element_index)

            # Add the current table's data to the overall DataFrame.
            all_tables = pd.concat([all_tables, citations_requirements], ignore_index=True)

    return all_tables

def run_ingestion_and_save(source_file_path, destination_file_path):
    """
    Runs the full ingestion process and saves the final DataFrame.
    """
    try:
        source_csv = pd.read_csv(source_file_path, skiprows=6, usecols=[1, 2], header=None)
        header_row_table = split_source_csv_by_table_headers(source_csv)
        final_structured_df = create_tables(source_csv=source_csv, header_row_table=header_row_table)
        
        # Rename columns to match the requested output headers
        final_structured_df.rename(columns={
            'ElementIndex': 'element_index',
            'Element': 'element',
            'RequirementIndex': 'requirement_index',
            'Requirement': 'requirement',
            'Citations': 'citations'
        }, inplace=True)

        # Save the final DataFrame to the new CSV file.
        final_structured_df.to_csv(destination_file_path, index=False)
        print(f"\n--- Final Structured DataFrame ---")
        print(final_structured_df.to_string())
        print(f"\nSuccessfully saved the final DataFrame to '{destination_file_path}'.")

    except FileNotFoundError:
        print(f"Error: The file '{source_file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    source_file = "source.csv"
    destination_file = "destination.csv"
    run_ingestion_and_save(source_file, destination_file)
