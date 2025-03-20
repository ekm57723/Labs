import os  # Import os to create directories
from flask import Flask, render_template, request
import segno

app = Flask(__name__)

# Ensure 'static/qr_codes/' exists (this should be outside the POST request handling)
os.makedirs("static/qr_codes", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_path = None
    message = None

    if request.method == "POST":
        message = request.form["data"].strip()  # Remove leading/trailing spaces
        if message:  # Only process if there's input
            filename = message.replace(" ", "_") + ".png"  # Safe filename
            qr_path = f"static/qr_codes/{filename}"

            # Generate the QR code
            qr = segno.make(message)

            # Debug: Check if QR code is being created
            print(f"QR code generated with message: {message}")

            # Save the QR code to the specified path
            qr.save(qr_path, scale=8)

            # Debug: Check if QR code file is saved
            if os.path.exists(qr_path):
                print(f"QR code saved to: {qr_path}")
            else:
                print(f"Failed to save QR code to: {qr_path}")

    return render_template("index.html", qr_path=qr_path, message=message)

if __name__ == "__main__":
    app.run(debug=True)