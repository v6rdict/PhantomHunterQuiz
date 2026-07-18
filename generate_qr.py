"""
Generate a QR code that points at your deployed quiz.

Usage:
    python generate_qr.py https://your-quiz-url.onrender.com
    python generate_qr.py http://192.168.1.23:5000   # for local phone testing
    python generate_qr.py https://your-quiz-url.com my_code.png   # custom filename
    python generate_qr.py https://your-quiz-url.com my_code.png /path/to/folder

By default the image is saved to an "output" folder created right next to
this script, regardless of which directory you run the command from.
"""
import sys
import os
import qrcode

# Folder the QR code gets saved into. Change this if you want a different
# default location (e.g. a shared "assets" folder in your project).
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_qr.py <url> [filename] [output_dir]")
        sys.exit(1)

    url = sys.argv[1]
    filename = sys.argv[2] if len(sys.argv) > 2 else "quiz_qr_code.png"
    output_dir = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_OUTPUT_DIR

    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    img = qrcode.make(url)
    img.save(filepath)
    print(f"Saved {filepath} -> points to {url}")


if __name__ == "__main__":
    main()
