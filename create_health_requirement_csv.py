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
