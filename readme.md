# About this Project

This was a part of a case study for the Readily team. 

<mark> The goal is to map the data from a CSV that health auditors might use into a structured CSV for the Readily product. </mark>

I created this script using a combination of documentation, my own abilities, and Gemini to assist in this project. 

I have included my self-written code inside of self-written.py, the list of Gemini prompts I used to inform my development, and the Gemini-tested code I used. The final product was written by Gemini.

I enjoyed the process of completing the mapping. I spent the majority of my self-written work splitting the tables.


# Files in this Project
 | Files | 
 | --------------------------------------------------- |
 | 1. create_health_requirement_csv.py   |
 | 2. Convert CSV Interview - pseudocode | 
 | 3. self_written.py - code I wrote myself |
 | 4. gemini-tested-code.py gemini produced code that I tested in developing this work |
 | 5. Gemini-prompts.txt - prompts that I asked Gemini in developing this. I did not use Cursor as I did not have any Cursor credits left for the day. |
 | 6. source.csv |
 | 7. Test file - gemini created |

 # How to run this work:
 ```
 python create-health_requirement_csv.py
 ```

Self-written code:
```
python self_written.py
```

# Future Directions
For future considerations, I would make this more reusable. For instance, I hardcoded the number of rows to skip at the top of the file. This would make it hard to reuse this code unless every auditing spreadsheet is formatted the same. 

I would also add the ability to add a source file as an input argument into the file as part of the CLI.

I would also add more robust testing. To make this document reusable, would need more robust checking and tools to clean data. For example, checking that number of rows in destination csv match the number of rows in the document would be helpful. It isn't as simple as getting a count because there are rows in the document that contain text that are unrelated to the number of rows in the final CSV

# How this was tested
I used console printing and manual checks to test this code worked against the document given.
6. <img width="1390" height="974" alt="Screenshot 2025-08-26 at 3 21 20 PM" src="https://github.com/user-attachments/assets/927dd5f3-6b4b-4117-af6d-b9f5c0d7e0aa" />



# Resources Used:
1. [Pandas Documentation](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)

2. [Read CSV File Containing Multiple Tables](https://stackoverflow.com/questions/34184841/python-pandas-read-csv-file-containing-multiple-tables)

3. Gemini Prompts and Code Assists Located in Gemini Prompts and Tested Code

4. [Select rows in series matching value](https://stackoverflow.com/questions/62397170/python-pandas-how-to-select-rows-where-objects-start-with-letters-pl)

5. [Adding Column Headers to new pandas dataframe](https://stackoverflow.com/questions/37038733/adding-column-headers-to-new-pandas-dataframe)

