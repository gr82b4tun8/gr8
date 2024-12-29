import pandas as pd
from tabula import read_pdf

# Path to your PDF file
pdf_path = "SAMPLE TEST.pdf"  # Replace with your PDF file path



# Extract all tables from the PDF into a list of DataFrames
try:
    tables = read_pdf(pdf_path, pages="all", multiple_tables=True)

    # Select Table 3 (index 2, as Python uses zero-based indexing)
    if len(tables) > 2:  # Ensure there are at least three tables
        table_three = tables[2]
        print("Processing Table 3...")

        # Ensure Table 3 is not empty
        if not table_three.empty and len(table_three.columns) > 4:  # Check column count
            # Extract the first column for Part Numbers
            column_part_number = table_three.iloc[:, 0]  # Assuming "Part Number" is in the first column
            print(f"First few rows of column 'Part Number':\n{column_part_number.head()}")

            # Extract the 5th column for Quantity
            column_quantity = table_three.iloc[:, 4]  # Assuming "Quantity" is the 5th column
            print(f"First few rows of column 'Quantity':\n{column_quantity.head()}")

            # Find all-caps words in "Part Number" column
            all_caps_with_numbers = []
            for cell in column_part_number.dropna():  # Ignore NaN values
                words = cell.split()
                matching_words = [word for word in words if word.isupper() and any(char.isdigit() for char in word)]
                all_caps_with_numbers.extend(matching_words)

            # Combine "Part Number" and "Quantity" columns into a DataFrame
            filtered_table = pd.DataFrame({
                "Part Number": all_caps_with_numbers,
                "Quantity": column_quantity.dropna().reset_index(drop=True)
            })

            # Save the results to a CSV
            output_file = "filtered_table_three_with_quantity.csv"
            filtered_table.to_csv(output_file, index=False)
            print(f"Filtered Table 3 with Quantity saved to {output_file}")
        else:
            print("Table 3 is empty, has no columns, or fewer than expected columns.")
    else:
        print("The PDF does not contain at least three tables.")

except Exception as e:
    print(f"An error occurred: {e}")
