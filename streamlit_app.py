import streamlit as st
import javalang

# Store uploaded files and class/method metadata in session state
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Java to JUnit Test Generator 🚀")

st.write("Upload one or more Java files below:")

# --- 1. FILE UPLOAD ---
uploaded = st.file_uploader(
    "Choose Java file(s)", type=["java"], accept_multiple_files=True
)

if uploaded:
    for file in uploaded:
        code = file.read().decode("utf-8")
        # Parse Java file, get class names
        try:
            tree = javalang.parse.parse(code)
            class_names = [type_decl.name for type_decl in tree.types if isinstance(type_decl, javalang.tree.ClassDeclaration)]
        except Exception as e:
            class_names = []
        st.session_state.uploaded_files[file.name] = {
            "code": code,
            "classes": class_names
        }

# --- 2. SHOW FILES & CLASSES ---
if st.session_state.uploaded_files:
    st.write("### Uploaded Java Files and Detected Classes")
    all_classes = []
    for fname, meta in st.session_state.uploaded_files.items():
        st.write(f"- **{fname}**: {', '.join(meta['classes']) if meta['classes'] else 'No classes found'}")
        all_classes.extend([(fname, cname) for cname in meta["classes"]])

    # Let user pick files/classes to generate tests for
    selected = st.multiselect(
        "Select Java classes for JUnit generation:",
        options=all_classes,
        format_func=lambda tup: f"{tup[0]}: {tup[1]}"
    )

    st.session_state.selected_classes = selected

    # (For now, we just display the selections; next step will add test gen + export)
    if selected:
        st.success(f"Selected {len(selected)} class(es) for test generation!")

    # Simple session chat log (will expand this with AI response later)
    st.session_state.chat_history.append(f"User uploaded files: {list(st.session_state.uploaded_files.keys())}")
    if selected:
        st.session_state.chat_history.append(f"User selected: {selected}")

    st.write("---")
    st.write("#### Session Activity")
    for msg in st.session_state.chat_history:
        st.write(msg)

else:
    st.info("Please upload at least one Java file.")

