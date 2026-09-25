"""
process_files.py — Part 3: many files, one after another, with a running total.

The same job as process_file.py, but the app now remembers what it has already
done: how many files have been processed, how many packages that came to, and a
one-line summary of each file — and it keeps remembering across uploads.

That is the hard part, and it is hard for a specific reason: every interaction
reruns this whole script from the top, so an ordinary variable like
`files_processed = 0` is reset to zero on every rerun. Anything that has to
survive a rerun lives in `st.session_state` instead, and is initialised only
once — the first time the script runs.

The other trap is the uploader itself. Once a file has been chosen it stays
chosen on every rerun, so an app that processes "whenever there is a file" would
count the same file again on every interaction. Processing happens on a button
click instead: `st.button` is True only on the one rerun the click caused.

Run it:  Run and Debug -> "Streamlit Run: Current File"   (see README Reference #1)
Test it: pytest tests/test_streamlit.py -k process_files
"""

import json

import streamlit as st

from packaging_parser import parse_packaging


def process_upload(uploaded_file) -> tuple[int, str]:
    """Parse every non-blank line of an uploaded file and write the packages to JSON.

    Returns the number of packages written and the name of the JSON file.
    """
    text = uploaded_file.getvalue().decode("utf-8")
    packages = [parse_packaging(line.strip()) for line in text.splitlines() if line.strip()]

    json_filename = "data/" + uploaded_file.name.replace(".txt", ".json")
    with open(json_filename, "w") as json_file:
        json.dump(packages, json_file, indent=4)

    return len(packages), json_filename


# 1. Initialise once — these keys only get created on the very first run.
if "files_processed" not in st.session_state:
    st.session_state.files_processed = 0
    st.session_state.packages_processed = 0
    st.session_state.history = []

st.title("Process Package Files")

uploaded_file = st.file_uploader("Upload package file:", key="package_file")
clicked = st.button("Process file", key="process")

# 2. Update on the click. The button is True only on the rerun the click caused,
#    so a file left in the uploader is never counted twice.
if clicked and uploaded_file:
    package_count, json_filename = process_upload(uploaded_file)
    st.session_state.files_processed += 1
    st.session_state.packages_processed += package_count
    st.session_state.history.append(f"{package_count} packages written to {json_filename}")

# 3. Display from state, on every run.
files_col, packages_col = st.columns(2)
files_col.metric("Files processed", st.session_state.files_processed)
packages_col.metric("Packages processed", st.session_state.packages_processed)

for summary in st.session_state.history:
    st.info(summary)
