import streamlit as st
from typing import Any

def render_extracted_fields(data: dict) -> None:
    """Recursively render extracted fields with clear key/value distinction."""
    for field_name, value in data.items():
        label = _prettify_field_name(field_name)

        # Skip empty / None values
        if value is None or value == "" or value == []:
            continue

        # ---------- List of dictionaries ----------
        if isinstance(value, list) and value and isinstance(value[0], dict):
            st.markdown(f"##### {label}")

            # Check if any nested dict/list exists inside the rows
            has_nested = any(
                any(isinstance(v, (dict, list)) for v in row.values())
                for row in value
            )

            if has_nested:
                # Complex case → render each item as an expander
                for idx, item in enumerate(value, start=1):
                    with st.expander(f"{label} #{idx}", expanded=True):
                        render_extracted_fields(item)
            else:
                # Simple case → clean dataframe
                st.dataframe(value, use_container_width=True, hide_index=True)

            st.markdown("---")

        # ---------- Nested dictionary ----------
        elif isinstance(value, dict):
            with st.expander(f"**{label}**", expanded=True):
                render_extracted_fields(value)

        # ---------- List of simple values ----------
        elif isinstance(value, list):
            st.markdown(f"**{label}**")
            for item in value:
                st.markdown(f"- {item}")
            st.markdown("---")

        # ---------- Simple key-value ----------
        else:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"**{label}**")
            with col2:
                st.markdown(
                    f"<span style='color:#4CAF50; font-weight:500'>{value}</span>",
                    unsafe_allow_html=True
                )


def _prettify_field_name(field_name: str) -> str:
    return " ".join(word.capitalize() for word in field_name.split("_"))