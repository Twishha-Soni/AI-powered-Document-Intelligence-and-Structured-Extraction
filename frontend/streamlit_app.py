import streamlit as st
import requests
from render_utils import render_extracted_fields

API_URL = 'http://localhost:8000'

# ---------------- Page Config ----------------
st.set_page_config(
    page_title='AI-powered Document Intelligence',
    layout='wide'
)

# ---------------- Session State ----------------
if 'uploaded_doc' not in st.session_state:
    st.session_state['uploaded_doc'] = False

# ---------------- Title ----------------
st.title('AI-powered Document Intelligence')
st.markdown("---")

# ---------------- Upload Section ----------------
doc = st.file_uploader(
    'Upload your document (.pdf, .docx)',
    type=['pdf', 'docx']
)

if st.button(
    '📥 Upload',
    disabled=doc is None
):
    with st.spinner('Uploading doc...'):
        resp = requests.post(
            f"{API_URL}/uploads",
            files={
                'file': (
                    doc.name,
                    doc.getvalue()
                )
            }
        )

        if not resp.ok:
            st.error(f'Server down: {resp.text}')
        else:
            result = resp.json()

            if result.get('text'):
                st.success('Uploaded on Server.')

            if result.get('waring'):
                st.warning(result['warning'])

            if st.button(
                'Extract',
                disabled=result.get('text') is None
            ):
                payload={'string1': result.get('text'), 'string2': result.get('warning')}

                with st.spinner('Extracting fields...'):
                    resp = requests.post(
                        f"{API_URL}/extract",
                        json=payload
                    )

                    if not resp.ok:
                        st.error('LLM response error.')

                    else:
                        if result.get('error'):
                            st.error(result['error'])

                        classification = result.get('classification')
                        if classification:
                            st.info(
                                f"Detected type: **{classification['doc_type']}"
                                f"(confidence: {classification['confidence']:.0%})"
                            )

                        extracted = result.get('extracted')
                        if extracted:
                            st.markdown("### Extracted Fields")
                            render_extracted_fields(extracted)