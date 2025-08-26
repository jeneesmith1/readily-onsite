import pandas as pd

# begin with our file - read the first two columns, start at Element A
source_csv = pd.read_csv("source.csv", skiprows=6, usecols=[1,2])
#print("SOURCE CSV", source_csv)

# task one - need to transform table into data object in such a way that citations and requirements are grouped by element and then individual splitting can occur
# observation that there are multiple tables within file - contracted/regulatory requirements and audit elements and the element name and these reoccur within the file

# gets index of row for every table which contains "Element in column 1"
def split_source_csv_by_table_headers(source_csv):
    df = source_csv.iloc[:, 0]
    table_header = "Element"
    is_row_table_header_df = df.loc[df.fillna('').str.startswith(table_header)].copy()
    header_row_table = pd.DataFrame({
        'HeaderIndices': is_row_table_header_df.index,
        'HeaderName': is_row_table_header_df.values
    })
    # print("TABLE HEADERS", is_row_table_header_df)
    # print("TABLE HEADERS 2", is_row_table_header_df_2)
    # tested that header table worked
    #print("TABLE INDICE", header_row_table.HeaderIndices)
    # print("TABLE NAME", is_row_table_header_df_2.HeaderName[1])
    # returns index for table start column
    return header_row_table


# helpers to split data into set of indices based on index of header row
def helper_create_pairs(data):
    return [[data[i], data[i+1]] for i in range(len(data) - 1)]

# helper to split element index and element
def get_element_and_index(policy_row, split_element):
    element_index, element = policy_row.split(split_element)
    return [element_index, element.lstrip()]

# task two - create separate tables based on header index
def create_tables(source_csv, header_row_table):
    # count number of tables from header_table
    number_tables = len(header_row_table)
    # get indices pairs to start creating table
    indices_array = helper_create_pairs(header_row_table.HeaderIndices)
    #print(indices_array)
        # function for header element_index and element to append
    for start, end in indices_array:
        policy_table = source_csv.iloc[start:end].dropna(how='all').copy()
        print(policy_table)
        # need to keep track of header row to append
        # separate for array with citation, requirement_index, requirement
        # function that takes indices_array and returns citation, requirement_index, requirement
        citations_requirements = get_citations_and_requirement_elements(policy_table)
        #print(citations_requirements)
        # get it all together

    

    return 

def get_citations_and_requirement_elements(policy_table):
        # get index array without the header rows
        index_array_no_header_rows = policy_table.iloc[2:]
        citations = index_array_no_header_rows.iloc[:, 0]
        # requirement_items = get_requirement_elements(index_array_no_header_rows.iloc[:, 1])

        #print("REMOVED HEADER ROWS", index_array_no_header_rows)
        # for start, end in index_array_no_header_rows:
        #     policy_table = source_csv.iloc[start:end].dropna(how='all').copy()
        #     print(policy_table)
            # inside each table - I want to extract the data to get it into my structured table
        return

# def get_requirement_elements(requirement_data):
#      print("Requirement Data")
#      #for row in requirement_data:
#         #print(get_element_and_index(requirement_data.iloc[row], "."))
#      return []
     
# def 


# testing function with print statements
# print(split_source_csv_by_table_headers(source_csv=source_csv))
header_row_table = split_source_csv_by_table_headers(source_csv=source_csv)
print(create_tables(source_csv=source_csv, header_row_table=header_row_table))
#print(get_element_and_index("Element A: processing"))
# print(get_element_and_index("1. Policy outlining the requirement", "."))



# final structure desired: [element_index, element, requirement_index, requirement, citations]

# element_index - must be split from element with delimiter :
# 

