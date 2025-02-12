import pandas as pd
import streamlit as st
from tabula import read_pdf
import os

def process_pdf(file):
    try:
        # Save uploaded file temporarily
        temp_file_path = "temp_uploaded_file.pdf"
        with open(temp_file_path, "wb") as f:
            f.write(file.getbuffer())

        # Extract all tables from the PDF into a list of DataFrames
        tables = read_pdf(temp_file_path, pages="all", multiple_tables=True)

        # Remove temporary file
        os.remove(temp_file_path)

        if len(tables) > 2:  # Ensure there are at least three tables
            table_three = tables[2]
            st.write("Processing Table 3...")

            # Ensure Table 3 is not empty and has enough columns
            if not table_three.empty and len(table_three.columns) > 4:
                column_part_number = table_three.iloc[:, 0]  # First column: Part Number
                column_quantity = table_three.iloc[:, 4]  # Fifth column: Quantity

                # Find all-caps words with numbers in "Part Number" column
                all_caps_with_numbers = []
                for cell in column_part_number.dropna():
                    words = str(cell).split()
                    matching_words = [word for word in words if word.isupper() and any(char.isdigit() for char in word)]
                    all_caps_with_numbers.extend(matching_words)

                # Combine "Part Number" and "Quantity" into a DataFrame
                filtered_table = pd.DataFrame({
                    "Part Number": all_caps_with_numbers,
                    "Quantity": column_quantity.dropna().reset_index(drop=True)
                })

                # Display results
                st.write("### Filtered Table 3 with Quantity")
                st.dataframe(filtered_table)
                
                # Provide download button
                csv = filtered_table.to_csv(index=False).encode('utf-8')
                st.download_button("Download CSV", csv, "filtered_table_three_with_quantity.csv", "text/csv")
            else:
                st.error("Table 3 is empty or does not have enough columns.")
        else:
            st.error("The PDF does not contain at least three tables.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Streamlit UI Setup
st.title("Everextension")
st.write("Upload an Invoice")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
if uploaded_file is not None:
    process_pdf(uploaded_file)
