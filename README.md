# 📦 DTDC Barcode Generator

A professional barcode generation tool built for **DTDC Courier (Agra Operations)** to generate bulk barcode labels efficiently.

---

## 🚀 Features

- Generate **Code 128 Barcodes**
- Bulk barcode generation using **Prefix + Range**
- Automatic PDF creation (print-ready)
- Each barcode includes:
  - DTDC logo (top)
  - Barcode
  - Tracking number
- Clean and compact layout for maximum utilization
- No local storage (memory optimized)
- Modern UI with branding

---

## 🖥️ Tech Stack

- Python
- Streamlit
- ReportLab
- Python-Barcode
- Pillow

---

## 📥 How to Use

1. Enter **Prefix** (e.g., D1015589)
2. Enter **Start Range**
3. Enter **End Range**
4. Click **Generate Barcodes PDF**
5. Download and print the PDF

---

## 📄 Output

- High-quality PDF file
- Optimized for A4 printing
- Multiple barcodes per page
- Logo integrated for branding

---

## ⚙️ Installation (Local Setup)

```bash
pip install -r requirements.txt
streamlit run app.py
