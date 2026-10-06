import streamlit as st
import PyPDF2
from gtts import gTTS
import tempfile

st.set_page_config(
    page_title="PDF to Voice Converter",
    page_icon="🔊"
)

st.title("📄 PDF to Voice Converter")
st.write("Upload a PDF file and convert its text into voice.")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file is not None:
    st.success("PDF uploaded successfully!")

    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    if text.strip():
        st.subheader("📖 Extracted Text")
        st.text_area("Text from PDF", text, height=300)

        language = st.selectbox(
            "Select Voice Language",
            [
                ("English", "en"),
                ("Tamil", "ta"),
                ("Hindi", "hi")
            ]
        )

        if st.button("🔊 Convert to Voice"):
            with st.spinner("Converting..."):
                selected_language = language[1]

                tts = gTTS(
                    text=text,
                    lang=selected_language,
                    slow=False
                )

                audio_file = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".mp3"
                )

                tts.save(audio_file.name)

                st.success("Voice conversion completed!")

                st.audio(
                    audio_file.name,
                    format="audio/mp3"
                )

                with open(audio_file.name, "rb") as file:
                    st.download_button(
                        "⬇️ Download Voice",
                        data=file,
                        file_name="pdf_voice.mp3",
                        mime="audio/mp3"
                    )
    else:
        st.error("No readable text found in this PDF.")
