# DOCX → Markdown Converter

A lightweight local web app that converts Microsoft Word `.docx` files to clean Markdown `.md` files — with drag-and-drop upload and one-click download.

---

## Project Structure

```
docx to MD/
├── app.py               # Flask backend (upload, convert, download routes)
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # Web UI (drag & drop, preview, download)
└── venv/                # Virtual environment
```

---

## Setup

### 1 · Create & activate a virtual environment (recommended)

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2 · Install dependencies

```powershell
pip install -r requirements.txt
```

### 3 · Run the app

```powershell
python app.py
```

### 4 · Open in browser

```
http://localhost:5000
```

---

## How to Use

1. **Drop** a `.docx` file onto the upload zone — or click to browse
2. Click **Convert to Markdown**
3. Preview the result in the output panel
4. Click **Download .md file** to save it

---

## How It Works

| Step | Library | Role |
|------|---------|------|
| 1 | **mammoth** | Reads the `.docx` and converts it to HTML, mapping Word styles (headings, bold, italic, lists, tables, links) |
| 2 | **markdownify** | Converts the HTML to clean ATX-style Markdown |
| 3 | **Flask** | Serves the UI and handles upload / download |

> **Note:** Embedded images are automatically stripped from the output to keep the Markdown clean and readable.

---

## Supported DOCX Features

| Feature | Supported |
|---------|-----------|
| Headings (H1–H6), Title, Subtitle | ✅ |
| Bold, Italic | ✅ |
| Ordered & unordered lists | ✅ |
| Tables | ✅ |
| Hyperlinks | ✅ |
| Embedded images | ⚠️ Stripped (intentional) |
| Complex layouts (text boxes, columns) | ⚠️ Partial |

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `flask` | Web framework |
| `mammoth` | DOCX → HTML conversion |
| `markdownify` | HTML → Markdown conversion |
