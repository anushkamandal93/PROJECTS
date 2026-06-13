import streamlit as st
from pathlib import Path
import os

st.set_page_config(page_title="File Manager", page_icon="🗂️", layout="centered")

st.markdown("""
    <style>
        .main { background-color: #0f1117; }
        h1 { color: #00d4ff; font-family: 'Courier New', monospace; }
        .stButton>button {
            width: 100%;
            background-color: #1e2a3a;
            color: #00d4ff;
            border: 1px solid #00d4ff;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            transition: 0.2s;
        }
        .stButton>button:hover {
            background-color: #00d4ff;
            color: #0f1117;
        }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #1e2a3a;
            color: #e0e0e0;
            border: 1px solid #00d4ff44;
            font-family: 'Courier New', monospace;
        }
        .stSelectbox>div>div {
            background-color: #1e2a3a;
            color: #e0e0e0;
        }
        .file-list {
            background-color: #1e2a3a;
            border: 1px solid #00d4ff33;
            border-radius: 8px;
            padding: 12px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            color: #a0c4d8;
            max-height: 200px;
            overflow-y: auto;
        }
        .success-msg { color: #00ff88; font-weight: bold; }
        .error-msg { color: #ff4444; font-weight: bold; }
        .info-msg { color: #00d4ff; }
    </style>
""", unsafe_allow_html=True)


# ── helpers ──────────────────────────────────────────────────────────────────

def list_items():
    p = Path('')
    return list(p.rglob('*'))


def show_file_list():
    items = list_items()
    if items:
        lines = "\n".join(f"{i+1}. {f}" for i, f in enumerate(items))
        st.markdown(f'<div class="file-list">{lines}</div>', unsafe_allow_html=True)
    else:
        st.info("No files or folders found in the current directory.")


# ── UI ────────────────────────────────────────────────────────────────────────

st.title("🗂️ File Manager")
st.caption("CRUD Operations · Files & Folders")

st.divider()

operation = st.selectbox(
    "Select Operation",
    [
        "📄 Create File",
        "📖 Read File",
        "✏️ Update File",
        "🗑️ Delete File",
        "🔄 Rename File",
        "📁 Create Folder",
        "🗑️ Delete Folder",
    ]
)

st.divider()

# ── current directory listing ─────────────────────────────────────────────────
with st.expander("📂 Current Directory Contents", expanded=False):
    show_file_list()

st.divider()

# ── operations ────────────────────────────────────────────────────────────────

if operation == "📄 Create File":
    st.subheader("Create File")
    file_name = st.text_input("File name (e.g. notes.txt)")
    content = st.text_area("File content")
    if st.button("Create File"):
        if not file_name:
            st.markdown('<p class="error-msg">⚠ Please enter a file name.</p>', unsafe_allow_html=True)
        else:
            p = Path(file_name)
            if p.exists():
                st.markdown('<p class="error-msg">⚠ File already exists!</p>', unsafe_allow_html=True)
            else:
                try:
                    p.write_text(content)
                    st.markdown('<p class="success-msg">✅ File created successfully!</p>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<p class="error-msg">❌ Error: {e}</p>', unsafe_allow_html=True)


elif operation == "📖 Read File":
    st.subheader("Read File")
    file_name = st.text_input("File name to read")
    if st.button("Read File"):
        if not file_name:
            st.markdown('<p class="error-msg">⚠ Please enter a file name.</p>', unsafe_allow_html=True)
        else:
            p = Path(file_name)
            if p.exists():
                try:
                    st.text_area("File Contents", p.read_text(), height=200)
                except Exception as e:
                    st.markdown(f'<p class="error-msg">❌ Error: {e}</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="error-msg">⚠ File not found!</p>', unsafe_allow_html=True)


elif operation == "✏️ Update File":
    st.subheader("Update File")
    file_name = st.text_input("File name to update")
    mode = st.radio("Update mode", ["Overwrite", "Append"])
    new_content = st.text_area("New content")
    if st.button("Update File"):
        if not file_name:
            st.markdown('<p class="error-msg">⚠ Please enter a file name.</p>', unsafe_allow_html=True)
        else:
            p = Path(file_name)
            if p.exists():
                try:
                    flag = 'w' if mode == "Overwrite" else 'a'
                    with open(file_name, flag) as f:
                        f.write(new_content)
                    st.markdown('<p class="success-msg">✅ File updated successfully!</p>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<p class="error-msg">❌ Error: {e}</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="error-msg">⚠ File does not exist!</p>', unsafe_allow_html=True)


elif operation == "🗑️ Delete File":
    st.subheader("Delete File")
    file_name = st.text_input("File name to delete")
    if st.button("Delete File", type="primary"):
        if not file_name:
            st.markdown('<p class="error-msg">⚠ Please enter a file name.</p>', unsafe_allow_html=True)
        else:
            p = Path(file_name)
            if p.exists():
                try:
                    os.remove(p)
                    st.markdown('<p class="success-msg">✅ File deleted successfully!</p>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<p class="error-msg">❌ Error: {e}</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="error-msg">⚠ File does not exist!</p>', unsafe_allow_html=True)


elif operation == "🔄 Rename File":
    st.subheader("Rename File")
    file_name = st.text_input("Current file name")
    new_name = st.text_input("New file name")
    if st.button("Rename File"):
        if not file_name or not new_name:
            st.markdown('<p class="error-msg">⚠ Please fill in both fields.</p>', unsafe_allow_html=True)
        else:
            p = Path(file_name)
            if p.exists():
                try:
                    p.rename(new_name)
                    st.markdown('<p class="success-msg">✅ File renamed successfully!</p>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<p class="error-msg">❌ Error: {e}</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="error-msg">⚠ File not found!</p>', unsafe_allow_html=True)


elif operation == "📁 Create Folder":
    st.subheader("Create Folder")
    folder_name = st.text_input("Folder name")
    if st.button("Create Folder"):
        if not folder_name:
            st.markdown('<p class="error-msg">⚠ Please enter a folder name.</p>', unsafe_allow_html=True)
        else:
            p = Path(folder_name)
            if p.exists():
                st.markdown('<p class="error-msg">⚠ Folder already exists!</p>', unsafe_allow_html=True)
            else:
                try:
                    p.mkdir(parents=True)
                    st.markdown('<p class="success-msg">✅ Folder created successfully!</p>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<p class="error-msg">❌ Error: {e}</p>', unsafe_allow_html=True)


elif operation == "🗑️ Delete Folder":
    st.subheader("Delete Folder")
    folder_name = st.text_input("Folder name to delete")
    if st.button("Delete Folder", type="primary"):
        if not folder_name:
            st.markdown('<p class="error-msg">⚠ Please enter a folder name.</p>', unsafe_allow_html=True)
        else:
            p = Path(folder_name)
            if p.exists():
                try:
                    p.rmdir()
                    st.markdown('<p class="success-msg">✅ Folder deleted successfully!</p>', unsafe_allow_html=True)
                except OSError:
                    st.markdown('<p class="error-msg">⚠ Folder is not empty! Remove contents first.</p>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<p class="error-msg">❌ Error: {e}</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="error-msg">⚠ Folder does not exist!</p>', unsafe_allow_html=True)


st.divider()
st.caption("Run with:  `streamlit run crud_streamlit.py`")