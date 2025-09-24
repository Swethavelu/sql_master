import os
import pandas as pd
import streamlit as st
from analysis import analyse_fields
from col_rename import replace_columns
from git_commands import git_checkout, git_push

st.set_page_config(page_title="Sql Master", layout="centered")
st.title("Rebase Agent")

# --- Inputs ---
repo_path = st.text_input("Enter repository folder path")
excel_path = st.text_input("Enter the input Excel path")

valid_input = True

# --- Basic validation ---
if repo_path and not os.path.isdir(repo_path):
    st.error("❌ Repository path does not exist or is not a directory")
    valid_input = False

if excel_path:
    if not os.path.exists(excel_path):
        st.error("❌ Excel file path does not exist")
        valid_input = False
    elif not excel_path.lower().endswith((".xls", ".xlsx")):
        st.error("❌ File is not an Excel file (.xls or .xlsx)")
        valid_input = False

# --- Proceed only if inputs are valid ---
if valid_input and repo_path and excel_path:
    try:
        xl = pd.ExcelFile(excel_path)
        selected_sheets = st.multiselect("Select one or more sheets", xl.sheet_names)

        if selected_sheets:
            st.success(f"✅ Selected Sheets: {', '.join(selected_sheets)}")

        action = st.radio("Choose Action", ["Run Analysis", "Replace Files"])

        # --- Only show push options if Replace Files is selected ---
        push_to_repo = False
        default_branch = branch_name = commit_message = None

        if action == "Replace Files":
            push_to_repo = st.checkbox("Do you want to push these changes to the repository?")
            if push_to_repo:
                default_branch = st.text_input(
                    "Enter your default branch",
                    placeholder="e.g. main or master"
                )
                branch_name = st.text_input(
                    "Enter Branch Name to push changes",
                    placeholder="e.g. feature/update-column-names"
                )
                commit_message = st.text_input(
                    "Enter commit message",
                    placeholder="e.g. Rename columns and update Excel files"
                )

        # --- Action Button ---
        if st.button("Run Action"):
            if action == "Run Analysis":
                res = analyse_fields(selected_sheets, excel_path, repo_path)
                if res is True:
                    st.success(f"✅ Results successfully updated in 'result' sheet of {excel_path}")
                else:
                    st.error(f"❌ Error during analysis: {res}")

            elif action == "Replace Files":
                if push_to_repo:
                    # Ensure all git inputs are filled
                    if default_branch and branch_name and commit_message:
                        git_checkout(repo_path, default_branch, branch_name, commit_message)

                        res = replace_columns(selected_sheets, excel_path)
                        if res is True:
                            st.success("✅ Files successfully updated with new column names")
                            git_push(branch_name)
                            st.success(f"🚀 Changes pushed to branch '{branch_name}'")
                        else:
                            st.error("❌ Error renaming columns...")
                    else:
                        st.warning("⚠️ Please complete all git fields before proceeding.")
                else:
                    res = replace_columns(selected_sheets, excel_path)
                    if res is True:
                        st.success("✅ Files successfully updated with new column names")
                    else:
                        st.error("❌ Error renaming columns...")

    except Exception as e:
        st.error(f"❌ Error reading Excel: {e}")
