import streamlit as st
import requests

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
    'Upload your document (.pdf, .docx, .txt)',
    type=['pdf', 'docx', 'txt']
)

if st.button(
    '📥 Extract',
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

        if resp.ok:
            st.session_state['uploaded_doc'] = True
            st.success('✅ Uploaded on server.')
            st.download_button(
                "⬇️ Download Brief PDF",
                data=resp.content,
                file_name=f"extracted_text_doc.pdf",
                mime="application/pdf",
            )
        else:
            st.error('Server down')