from flask import Flask, send_from_directory, render_template, abort
from pathlib import Path
from werkzeug.utils import safe_join

app = Flask(__name__)

# Secure base directory — using absolute path prevents path confusion
IMAGE_FOLDER = Path("cards").resolve()

# Whitelist of supported image extensions
SUPPORTED_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}

# Collect all valid image files in subfolders
def get_all_images():
    return sorted([
        f.relative_to(IMAGE_FOLDER).as_posix()
        for f in IMAGE_FOLDER.rglob("*")
        if f.suffix.lower() in SUPPORTED_EXTS and f.is_file() and not f.name.startswith('.')
    ])

@app.route('/')
def index():
    images = get_all_images()
    return render_template("index.html", images=images)

@app.route('/images/<path:filename>')
def image_file(filename):
    # Ensure the joined path is within IMAGE_FOLDER
    safe_path = safe_join(IMAGE_FOLDER, filename)
    if not safe_path:
        abort(400)  # Bad request
    safe_path = Path(safe_path).resolve()

    # Prevent access outside IMAGE_FOLDER
    if not str(safe_path).startswith(str(IMAGE_FOLDER)):
        abort(403)  # Forbidden

    # Check file exists and has valid extension
    if not safe_path.is_file() or safe_path.suffix.lower() not in SUPPORTED_EXTS:
        abort(404)

    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == '__main__':
    # DO NOT run with debug=True in production
    app.run(debug=False, port=8000)