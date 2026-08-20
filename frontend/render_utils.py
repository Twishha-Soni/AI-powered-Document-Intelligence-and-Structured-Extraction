import streamlit as st

def render_extracted_fields(data: dict) -> None:
    for field_name, value in data.items():
        label = _prettify_field_name(field_name)

        if isinstance(value, list) and value and isinstance(value[0], dict):
            st.markdown(f"**{label}**")
            st.table(value)

        elif isinstance(value, dict):
            st.markdown(f"**{label}**")
            render_extracted_fields(value)

        elif value is None:
            continue

        else:
            st.write(f"**{label}:** {value}")

def _prettify_field_name(field_name: str) -> str:
    return " ".join(word.capitalize() for word in field_name.split('_'))