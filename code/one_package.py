"""
one_package.py — Part 1: one package description, typed in.

A Streamlit app that asks for a single package description, parses it with the
`packaging_parser` module, and shows each level of packaging plus the total number of
units inside.

This is the smallest possible Streamlit app that does real work, and it exists to
teach one thing: a Streamlit script runs **top to bottom on every interaction**.
When the page first opens, the text box is empty — and your code still runs. So
the work has to sit behind a guard: only parse when there is something to parse.

Run it:  Run and Debug -> "Streamlit Run: Current File"   (see README Reference #1)
Test it: pytest tests/test_streamlit.py -k one_package
"""

import streamlit as st

from packaging_parser import calc_total_units, get_unit, parse_packaging

st.title("Process One Package")

# st.text_input returns the box's current contents — "" on the first run.
package_data = st.text_input(
    "Enter package data:",
    key="package_data",
    placeholder="12 eggs in 1 carton / 3 cartons in 1 box",
)

# Guard: only parse once something has been typed.
if package_data:
    try:
        package = parse_packaging(package_data)
    except ValueError as err:
        st.error(f"Could not parse that package description: {err}")
    else:
        total = calc_total_units(package)
        unit = get_unit(package)

        # Each level is a one-item dictionary, {name: quantity}.
        for level in package:
            for name, quantity in level.items():
                st.info(f"{name} ➡️ {quantity}")

        st.success(f"Total 📦 Size: {total} {unit}")
