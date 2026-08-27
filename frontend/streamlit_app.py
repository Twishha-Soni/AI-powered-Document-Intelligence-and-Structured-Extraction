import streamlit as st
import requests

from render_utils import render_extracted_fields

API_URL = 'http://localhost:8000'

st.set_page_config(
    page_title="AI-Powered DocIQ",
    page_icon="📄",
    layout="wide"
)

# ---------------- Session State Init ----------------
if 'page' not in st.session_state:
    st.session_state.page = 'login'      # which auth screen to show
if 'token' not in st.session_state:
    st.session_state.token = None        # None = not logged in
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'login_error' not in st.session_state:
    st.session_state.login_error = None
if 'register_error' not in st.session_state:
    st.session_state.register_error = None
if 'register_success' not in st.session_state:
    st.session_state.register_success = None
if 'uploader_version' not in st.session_state:
    st.session_state.uploader_version = 0
if 'upload_success' not in st.session_state:
    st.session_state.upload_success = None
if 'upload_error' not in st.session_state:
    st.session_state.upload_error = None
if 'selected_doc_id' not in st.session_state:
    st.session_state.selected_doc_id = None
if 'history_error' not in st.session_state:
    st.session_state.history_error = None
if 'detail_error' not in st.session_state:
    st.session_state.detail_error = None
if 'analyze_error' not in st.session_state:
    st.session_state.analyze_error = None

# ---------------- Auth Header ----------------
def auth_headers() -> dict:
    return {
        'Authorization': f'Bearer {st.session_state.token}'
    }

def go_to(page: str) -> None:
    st.session_state.page = page

# ---------------- Login Callback ----------------
def do_login():
    username = st.session_state.login_username
    password = st.session_state.login_password

    resp = requests.post(
        f"{API_URL}/login",
        data={'username': username, 'password': password}
    )

    if resp.ok:
        data = resp.json()
        st.session_state.token = data['access_token']
        st.session_state.username = username
        st.session_state.login_error = None
        st.session_state.page = 'main'
    else:
        st.session_state.login_error = 'Invalid username or password'

# ---------------- Register Callback ----------------
def do_register():
    username = st.session_state.reg_username
    password = st.session_state.reg_password

    resp = requests.post(
        f"{API_URL}/register",
        json={"username": username, "password": password}
    )

    if resp.ok:
        st.session_state.register_error = None
        st.session_state.register_success = f"Account created for '{username}'. Please log in."
        st.session_state.page = "login"
    else:
        st.session_state.register_error = resp.json().get("detail", "Registration failed.")
        st.session_state.register_success = None

# ---------------- upload callback ----------------
def do_upload():
    uploader_key = f'file_uploader_{st.session_state.uploader_version}'
    uploaded_file = st.session_state.get(uploader_key)

    if uploaded_file is None:
        st.session_state.upload_error = "Please choose a file first."
        st.session_state.upload_success = None
        return

    resp = requests.post(
        f"{API_URL}/uploads",
        headers=auth_headers(),
        files={"file": (uploaded_file.name, uploaded_file.getvalue())}
    )

    if resp.ok:
        data = resp.json()
        st.session_state.upload_success = f"Uploaded '{uploaded_file.name}'."
        st.session_state.upload_error = None
        st.session_state.uploader_version += 1  # forces a fresh, empty uploader
    else:
        detail = resp.json().get("detail", "Upload failed.")
        st.session_state.upload_error = detail
        st.session_state.upload_success = None

# ---------------- history callback ----------------
def fetch_history() -> list[dict]:
    resp = requests.get(f"{API_URL}/history" , headers=auth_headers())

    if resp.ok:
        return resp.json()
    else:
        st.session_state.history_error = resp.json().get("detail", "Could not load history.")
        return []

# ---------------- select doc callback ----------------
def select_document(document_id: int) -> None:
    st.session_state.selected_doc_id = document_id

# ---------------- fetch doc callback ----------------
def fetch_document_detail(document_id: int) -> dict | None:
    resp = requests.get(
        f"{API_URL}/document/{document_id}",
        headers=auth_headers()
    )

    if resp.ok:
        return resp.json()
    else:
        st.session_state.detail_error = resp.json().get("detail", "Could not load document.")
        return None

# ---------------- analyze callback ----------------
def do_analyze(document_id: int):
    resp = requests.post(
        f"{API_URL}/extract/{document_id}",
        headers=auth_headers()
    )

    if resp.ok:
        st.session_state.analyze_error = None
    else:
        st.session_state.analyze_error = resp.json().get("detail", "Extraction failed.")

# ---------------- Register Page ----------------
def register_page():
    with st.container(border=True):
        st.subheader("Register")
        st.text_input("Username", key="reg_username")
        st.text_input("Password", type="password", key="reg_password")
        st.button("Create account", key="reg_submit", on_click=do_register)

        if st.session_state.register_error:
            st.error(st.session_state.register_error)

    st.markdown("Already a user?")
    st.button("Login", key="to_login", on_click=go_to, args=("login",))


# ---------------- Login Page ----------------
def login_page():
    if st.session_state.register_success:
        st.success(st.session_state.register_success)
        st.session_state.register_success = None
        
    with st.container(border=True):
        st.subheader("Login")
        st.text_input("Username", key="login_username")
        st.text_input("Password", type="password", key="login_password")
        st.button("Login", key="login_submit", on_click=do_login)

        if st.session_state.login_error:
            st.error(st.session_state.login_error)

    st.markdown("Not a user?")
    st.button("Register", key="to_register", on_click=go_to, args=("register",))


# ---------------- Main App (logged in) ----------------
def main_page():
    with st.sidebar:
        st.text_input("Username", value=st.session_state.get('username', ''), disabled=True)
        st.markdown("---")

        uploader_key = f"file_uploader_{st.session_state.uploader_version}"
        st.file_uploader(
            "Upload a document",
            type=["pdf", "docx", '.png', '.jpeg', '.jpg', '.webp'],
            key=uploader_key
        )

        if st.session_state.upload_success:
            st.success(st.session_state.upload_success)
        if st.session_state.upload_error:
            st.error(st.session_state.upload_error)

        st.button("📤 Upload", key="upload_button", on_click=do_upload)

        st.markdown("---")
        st.markdown("**History:**")

        st.session_state.history_error = None
        history = fetch_history()

        if st.session_state.history_error:
            st.error(st.session_state.history_error)

        if not history:
            st.caption("No documents yet.")
        else:
            for doc in history:
                label = f"{doc['filename']} ({doc['status']})"
                st.button(
                    label,
                    key=f"doc_{doc['document_id']}",
                    on_click=select_document,
                    args=(doc['document_id'],)
                )


    render_main_pane()

# ---------------- Render main pane ----------------
def render_main_pane():
    if st.session_state.selected_doc_id is None:
        st.title("WELCOME TO AI-Powered DocIQ")
        st.markdown("*select your document from the uploaded history to analyze it deeply*")
        return

    st.session_state.detail_error = None
    doc = fetch_document_detail(st.session_state.selected_doc_id)

    if st.session_state.detail_error:
        st.error(st.session_state.detail_error)
        return

    st.subheader(doc["filename"])

    if doc["status"] == "uploaded":
        st.text_area("Extracted text", value=doc["extracted_text"] or "", height=300, disabled=True)
        st.button(
            "🔍 Analyze",
            key="analyze_button",
            on_click=do_analyze,
            args=(doc["id"],)
        )
        if st.session_state.analyze_error:
            st.error(st.session_state.analyze_error)


    elif doc["status"] == "extracted":
        st.info(f"Detected type: **{doc['doc_type']}** (confidence: {doc['confidence']*100:.1f}%)")
        st.markdown("### Extracted Fields")
        render_extracted_fields(doc["extracted_data"])


# ---------------- Router ----------------
if st.session_state.token is None:
    if st.session_state.page == 'register':
        register_page()
    else:
        login_page()
else:
    main_page()
