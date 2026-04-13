import streamlit as st
import base64
import barcode
from barcode.writer import ImageWriter
from reportlab.platypus import SimpleDocTemplate, Image, Table, PageBreak, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os

st.set_page_config(page_title="DTDC Barcode Generator", layout="wide")

# =========================
# 🔥 BACKGROUND IMAGE SET
# =========================
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Overlay effect */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.6);
        z-index: -1;
    }}

    /* Text color */
    h1, h2, h3, h4, h5, h6, label, p {{
        color: white !important;
    }}

    /* Buttons */
    .stButton>button {{
        background-color: #E30613;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }}

    .stButton>button:hover {{
        background-color: #b00510;
    }}

    /* Input fields */
    .stTextInput input, .stNumberInput input {{
        background-color: rgba(255,255,255,0.9);
        border-radius: 6px;
    }}

    </style>
    """, unsafe_allow_html=True)

# 🔹 Set your image path
set_bg("bg.png")   # 👈 yaha apni image ka naam daal

# =========================
# TITLE
# =========================
st.markdown("<h1 style='text-align: center;'>📦 DTDC Barcode Generator</h1>", unsafe_allow_html=True)

st.write("")

# =========================
# INPUT UI
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    prefix = st.text_input("Prefix", "D1015589")

with col2:
    start = st.number_input("Start Range", min_value=0, step=1)

with col3:
    end = st.number_input("End Range", min_value=0, step=1)

st.write("")

# =========================
# GENERATE BUTTON
# =========================
if st.button("🚀 Generate Barcodes PDF"):

    if start > end:
        st.error("Start should be less than End")
    else:
        if not os.path.exists("barcodes"):
            os.makedirs("barcodes")

        numbers = [f"{prefix}{i}" for i in range(int(start), int(end)+1)]

        barcode_images = []

        for num in numbers:
            code128 = barcode.get('code128', num, writer=ImageWriter())
            filename = f"barcodes/{num}"
            code128.save(filename)
            barcode_images.append(f"{filename}.png")

        pdf_path = "DTDC_Barcodes.pdf"
        pdf = SimpleDocTemplate(pdf_path, pagesize=A4)

        styles = getSampleStyleSheet()
        elements = []

        # Logo (optional)
        if os.path.exists("dtdc_logo.png"):
            logo = Image("dtdc_logo.png", width=120, height=60)
            elements.append(logo)

        title = Paragraph("<b>DTDC Courier - Barcode Labels</b>", styles['Title'])
        elements.append(title)

        date = Paragraph(f"Generated on: {datetime.now().strftime('%d-%m-%Y')}", styles['Normal'])
        elements.append(date)

        elements.append(Spacer(1, 20))

        cols = 3
        per_page = 24

        table_data = []
        row = []
        count = 0

        for i, img_path in enumerate(barcode_images):
            img = Image(img_path, width=150, height=60)
            cell = [img, Paragraph(numbers[i], styles['Normal'])]
            row.append(cell)
            count += 1

            if (i + 1) % cols == 0:
                table_data.append(row)
                row = []

            if count == per_page:
                if row:
                    table_data.append(row)

                elements.append(Table(table_data))
                elements.append(PageBreak())

                table_data = []
                row = []
                count = 0

        if row:
            table_data.append(row)

        if table_data:
            elements.append(Table(table_data))

        pdf.build(elements)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Download PDF",
                data=f,
                file_name="DTDC_Barcodes.pdf",
                mime="application/pdf"
            )

        st.success("✅ PDF Generated Successfully!")
