import streamlit as st
import requests
from render_utils import render_extracted_fields

API_URL = 'http://backend:8000'

# ---------------- Page Config ----------------
st.set_page_config(
    page_title='AI-powered Document Intelligence',
    layout='wide'
)

# ---------------- Session State ----------------
if 'uploaded_doc' not in st.session_state:
    st.session_state['uploaded_doc'] = False
    st.session_state['result'] = {}


# ---------------- Title ----------------
st.title('AI-powered Document Intelligence')
st.markdown("---")

# ---------------- Upload Section ----------------
doc = st.file_uploader(
    'Upload your document',
    type=['pdf', 'docx', 'png', 'jpg', 'jpeg', 'webp']
)

if st.button(
    '📋 Extract Text',
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
            st.session_state['result'] = resp.json()

            if st.session_state['result'].get('text'):
                st.success('Uploaded on Server.')
                st.success(st.session_state['result'].get('text'))

            if st.session_state['result'].get('waring'):
                st.warning(st.session_state['result'].get('warning'))

            st.session_state['uploaded_doc'] = True

if st.button(
    '📥 Extract Fields',
    disabled=st.session_state['result'].get('text') is None
):
    payload={'string1': st.session_state['result'].get('text'), 'string2': st.session_state['result'].get('warning')}

    with st.spinner('Extracting fields...'):
        resp = requests.post(
            f"{API_URL}/extract",
            json=payload
        )

        if not resp.ok:
            st.error('LLM response error.')

        else:
            resp = resp.json()

            if resp.get('error'):
                st.error(resp['error'])

            classification = resp.get('classification')
            if classification:
                st.info(
                    f"Detected type: **{classification['doc_type']}"
                    f"(confidence: {classification['confidence']:.0%})"
                )

            extracted = resp.get('extracted')
            if extracted:
                st.markdown("### Extracted Fields")
                render_extracted_fields(extracted)