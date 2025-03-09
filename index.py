import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="💿Data Sweeper" , layout="wide")
st.title("💿Data Sweeper")
st.write("upload csv or excel file, convert formats or clean data!!")

uploded_files = st.file_uploader("Upload csv or Exell files", type=["csv", "xlsx"], accept_multiple_files=True)

if uploded_files:
    for file in uploded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"File format of {file_ext} is not supported")
            continue 

        # Display info about the file
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Type:** {file.size/1024}")

        # Show 5 rows of the data
        st.write("preview of the head of the DataFrame")
        st.write(df.head())

        # option for data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1 , col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed successfully")
            
            with col2:
                if st.button(f"Fill Missing Values in {file.name}"):
                    numaring_cols = df.select_dtypes(include=["number"]).columns
                    df[numaring_cols] = df[numaring_cols].fillna(df[numaring_cols].mean())
                    st.write("Missing values filled successfully")
                    
        # Keep or convert specific columns
        st.subheader("Select Columns to convert")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns , default=df.columns)
        df = df[columns]

        # Create visualizations
        st.subheader("💾 Data Visualizations")
        if st.checkbox(f"Show visualizations for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])


        # Convert the the file
        st.subheader("🔁Convertion Options")
        converstion_type = st.radio(f"convert {file.name} to", ["csv", "xlsx"], key=file.name)
        if st.button (f"Convert {file.name}"):
            buffer = BytesIO()
            if converstion_type == "csv":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif converstion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Download button
            st.download_button(
                label=f" Download {file_name} as {converstion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
st.success("🎉 Files processed successfully")