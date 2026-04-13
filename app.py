import streamlit as st
import base64
import barcode
from barcode.writer import ImageWriter
from reportlab.platypus import SimpleDocTemplate, Image, Table, PageBreak, Paragraph, Spacer, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
from io import BytesIO
import os

st.set_page_config(page_title="DTDC Barcode Generator", layout="wide")

# =========================
# 🔥 BACKGROUND + CSS
# =========================
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    css = """
    <style>

    .stApp {
        background-image: url("data:image/png;base64,DATA_HERE");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        backdrop-filter: blur(8px);
        background: rgba(0,0,0,0.5);
        z-index: -1;
    }

    /* 🔥 DEV TAG */
    .dev-tag {
    position: fixed;
    top: 60px;     /* 👈 adjust kiya */
    right: 25px;
    color: black;
    font-size: 13px;
    font-weight: 600;
    # background: rgba(0,0,0,0.6);
    padding: 6px 14px;
    # border-radius: 20px;
    z-index: 999999;
    # box-shadow: 0 0 10px rgba(0,0,0,0.5);
}

    /* 🔥 HEADER */
    h1 {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #ffffff;
        text-shadow: 0 0 10px rgba(0,0,0,0.7),
                     0 0 20px rgba(0,0,0,0.5);
        letter-spacing: 1px;
    }

    /* 🔥 LABELS */
    label {
        color: #ffffff;
        font-size: 20px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-shadow: 0 0 5px rgba(0,0,0,0.6);
    }

    /* 🔥 INPUT */
    .stTextInput input, .stNumberInput input {
        background-color: rgba(255,255,255,0.95);
        color: black;
        border-radius: 10px;
        padding: 10px;
        font-size: 15px;
    }

    /* 🔥 BUTTON */
    .stButton>button {
        background: linear-gradient(135deg, #E30613, #b00510);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
    }

    </style>
    """

    css = css.replace("DATA_HERE", encoded)
    st.markdown(css, unsafe_allow_html=True)


# =========================
# APPLY BG + DEV TAG
# =========================
set_bg(r"bg.png")

st.markdown(
    '<div class="dev-tag">⚡ Developed by Akash Sharma</div>',
    unsafe_allow_html=True
)

# =========================
# TITLE
# =========================
st.markdown("<h1>📦 DTDC Barcode Generator</h1>", unsafe_allow_html=True)

# =========================
# INPUT
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    prefix = st.text_input("Prefix", "D1015589")

with col2:
    start = st.number_input("Start Range", min_value=0, step=1)

with col3:
    end = st.number_input("End Range", min_value=0, step=1)

# =========================
# GENERATE PDF
# =========================
if st.button("🚀 Generate Barcodes PDF"):

    if start > end:
        st.error("Start should be less than End")

    else:
        numbers = [f"{prefix}{i}" for i in range(int(start), int(end)+1)]

        pdf_buffer = BytesIO()

        pdf = SimpleDocTemplate(
            pdf_buffer,
            pagesize=A4,
            topMargin=10,
            bottomMargin=10,
            leftMargin=20,
            rightMargin=20
        )

        styles = getSampleStyleSheet()
        elements = []

        # Header
        title_style = ParagraphStyle(
            'title',
            fontSize=16,
            leading=18,
            spaceAfter=4
        )

        elements.append(Paragraph("<b>DTDC Courier - Barcode Labels</b>", title_style))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%d-%m-%Y')}", styles['Normal']))
        elements.append(Spacer(1, 8))

        cols = 3
        per_page = 27

        table_data = []
        row = []
        count = 0

        for i, num in enumerate(numbers):

            buffer = BytesIO()
            code128 = barcode.get('code128', num, writer=ImageWriter())
            code128.write(buffer)
            buffer.seek(0)

            logo = Image(r"dtdc_logo.png", width=50, height=25)
            img = Image(buffer, width=140, height=50)

            cell = [logo, img]

            row.append(cell)
            count += 1

            if (i + 1) % cols == 0:
                table_data.append(row)
                row = []

            if count == per_page:
                if row:
                    table_data.append(row)

                table = Table(table_data)
                table.setStyle(TableStyle([
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('TOPPADDING', (0,0), (-1,-1), 2),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ]))

                elements.append(table)
                elements.append(PageBreak())

                table_data = []
                row = []
                count = 0

        if row:
            table_data.append(row)

        if table_data:
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ]))
            elements.append(table)

        pdf.build(elements)

        pdf_buffer.seek(0)

        st.download_button(
            label="📥 Download PDF",
            data=pdf_buffer,
            file_name="DTDC_Barcodes.pdf",
            mime="application/pdf"
        )

        st.success("✅ PDF Ready!")
