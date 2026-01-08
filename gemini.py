import streamlit as st
import text_res as text
import image_res as img
import audio_res as aud
import csv_result as csv
import pdf_res as pdf
# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Multi-Modal RAG Application",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Simple Styling ----------------
st.markdown("""
<style>
  
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
            .title, h1, h2, h3, h4, h5, h6 {
    color: white !important;
    text-align: center;
}

/* Subtitle class */
.subtitle {
    color: white !important;
    text-align: center;
}

/* File uploader, input boxes, and buttons */
.stFileUploader, .stTextInput, .stTextArea, .stButton {
    color: black !important; /* black input text */
}
/* st.write() outputs or answers */
.stMarkdown, .stText {
    color: white !important;
    font-weight: bold;
}

/* Buttons text color */
.stButton>button {
    color: white;
    background-color: #4CAF50; /* green button for visibility */
}
            /* Streamlit info / warning messages */
.stAlert {
    color: white !important;
    background-color: rgba(0,0,0,0.5) !important;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: white;
    margin-bottom: 6px;
}
h3 {
    color: white !important;
}
.subtitle {
    text-align: center;
    font-size: 18px;
    color: white;
    margin-bottom: 30px;
}

# .card {
#     # background-color: white;
#     padding: 24px;
#     border-radius: 14px;
#     box-shadow: 0 6px 18px rgba(0,0,0,0.2);
# }
</style>
""", unsafe_allow_html=True)

# ---------------- Title ----------------
st.markdown('<div class="title">🤖 Welcome to Multi-Modal RAG Application</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Upload files and ask questions across text, images, PDFs, audio, and more</div>',
    unsafe_allow_html=True
)

# ---------------- TWO COLUMNS ----------------
left_col, right_col = st.columns([2, 3])

# -------- LEFT COLUMN --------
with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📂 Upload Your File/Record Audio")


    uploaded_file = st.file_uploader(
        "Supported formats: PDF, Image, CSV, Audio, Text",
        type=["pdf", "png", "jpg", "jpeg", "csv", "txt", "wav", "mp3"]
    )
    
   
    # -------- RESET STATE WHEN NEW FILE IS UPLOADED --------
if "last_file" not in st.session_state:
    st.session_state.last_file = None

# if uploaded_file is not None:
#     if st.session_state.last_file != uploaded_file.name:
#         st.session_state.last_file = uploaded_file.name

#         # Clear old RAG data
#         st.session_state.text = None
#         st.session_state.vectorstore = None
if uploaded_file is not None:
    if st.session_state.get("last_file") != uploaded_file.name:
        st.session_state.last_file = uploaded_file.name
        st.session_state.vectorstore = None
        st.session_state.chunks_printed = False
        st.session_state.text = None
        st.session_state.vectorstore = None

    if uploaded_file:
        st.success(f"File uploaded: {uploaded_file.name}")

    st.markdown('</div>', unsafe_allow_html=True)


# -------- RIGHT COLUMN --------
with right_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔍 Ask Your Question")

    query = st.text_input("Type your query here")
    
    clicked = st.button("🚀 Get Answer")


def rag_app(ufile, query, type):
    st.write(f"Processing `{ufile.name}` ({type}) with query: `{query}`")
    st.write("🎤 Processing File...")

    res = None  # ✅ ALWAYS initialize

    if type == "text/plain":
        res = text.rag(ufile, query)

    elif type == "text/csv":
        res = csv.rag_csv(ufile, query)

    elif type in ["image/jpeg", "image/png", "image/jpg"]:
        res = img.rag_image(ufile, query)
    elif type == "application/pdf":
        res = pdf.rag_pdf(ufile, query)
    elif type in ["audio/wav", "audio/mpeg", "audio/mp3", "audio/m4a"]:
        res = aud.rag_audio(ufile, query)

    # ✅ SAFE DISPLAY
    if res is not None and res != "":
        st.markdown(
            f"<span style='color:white;'>🧠 {res}</span>",
            unsafe_allow_html=True
        )
    else:
        st.warning("No response generated.")

    # # st.write(f"🧠 {query} {res}\n")
    # st.markdown(f"<span style='color:white;'>🧠 {res}</span>", unsafe_allow_html=True)


# if clicked:
#     if not uploaded_file:
#         st.warning("⚠️ Please upload a file")
#     elif not query:
#         st.warning("⚠️ Please enter a query")
#     else:
#         st.info("🔎 Processing your query...")
#         st.success("✅ Answer will appear here")
if uploaded_file:
    # Call RAG handler
    if query:
        rag_app(uploaded_file, query, uploaded_file.type)
    else:
        st.info("Type a query to process the file.")
else:
    st.info("📌 Please upload a file to start.")


    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Footer ----------------
st.markdown(
    "<p style='text-align:center; color:#d1d5db; margin-top:30px;'>Built with ❤️ using Streamlit | Multi-Modal RAG Project</p>",
    unsafe_allow_html=True
)
#venv\Scripts\activate to create virtual environment