"""
Flask Web UI — DOCX to Markdown Converter
------------------------------------------
Run:  python app.py
Open: http://localhost:5000
"""

import io
import os
import tempfile
from pathlib import Path

# pyrefly: ignore [missing-import]
import mammoth
# pyrefly: ignore [missing-import]
import markdownify
# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, send_file, jsonify

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB max upload


# ---------------------------------------------------------------------------
# Conversion logic (shared with convert.py)
# ---------------------------------------------------------------------------

def _ignore_images(image):
    """Drop embedded images — prevents giant base64 blobs in output."""
    return {}


def docx_to_markdown(file_obj) -> str:
    style_map = """
        p[style-name='Heading 1'] => h1:fresh
        p[style-name='Heading 2'] => h2:fresh
        p[style-name='Heading 3'] => h3:fresh
        p[style-name='Heading 4'] => h4:fresh
        p[style-name='Heading 5'] => h5:fresh
        p[style-name='Heading 6'] => h6:fresh
        p[style-name='Title']     => h1:fresh
        p[style-name='Subtitle']  => h2:fresh
        r[style-name='Strong']    => strong
        r[style-name='Emphasis']  => em
    """
    result = mammoth.convert_to_html(
        file_obj,
        style_map=style_map,
        convert_image=mammoth.images.img_element(_ignore_images),
    )
    md = markdownify.markdownify(
        result.value,
        heading_style=markdownify.ATX,
        bullets="-",
        strip=["script", "style", "img"],
    )
    return md.strip()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    if not file.filename.lower().endswith(".docx"):
        return jsonify({"error": "Only .docx files are supported"}), 400

    try:
        md_content = docx_to_markdown(file.stream)
    except Exception as e:
        return jsonify({"error": f"Conversion failed: {str(e)}"}), 500

    # Return markdown content as JSON (for preview + download)
    stem = Path(file.filename).stem
    return jsonify({
        "markdown": md_content,
        "filename": f"{stem}.md",
        "chars": len(md_content),
        "lines": md_content.count("\n") + 1,
    })


@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    if not data or "markdown" not in data or "filename" not in data:
        return jsonify({"error": "Invalid request"}), 400

    md_bytes = data["markdown"].encode("utf-8")
    return send_file(
        io.BytesIO(md_bytes),
        mimetype="text/markdown",
        as_attachment=True,
        download_name=data["filename"],
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
