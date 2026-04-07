import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Define directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))

app = Flask(__name__)
# Enable CORS to allow requests from your frontend
CORS(app)

TARGET_EMAIL = 'benven1510@gmail.com'

# --- SERVING FRONTEND ---
@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    # Only allow safe file extensions
    allowed_exts = ('.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp', '.woff', '.woff2', '.ttf')
    if filename.endswith(allowed_exts) and '..' not in filename and not filename.startswith('backend/'):
        return send_from_directory(FRONTEND_DIR, filename)
    return "File Not Found", 404
# -------------------------

@app.route('/api/book', methods=['POST'])
def book_session():
    # Reload .env dynamically so user doesn't need to restart backend
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(BASE_DIR, '.env'), override=True)
    
    SENDER_EMAIL = os.environ.get('GMAIL_ADDRESS', TARGET_EMAIL)
    SENDER_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Extract data from the request
        name = data.get('name', 'Unknown')
        phone = data.get('phone', 'Unknown')
        email = data.get('email', 'Unknown')
        occasion = data.get('occasion', 'Unknown')
        city = data.get('city', 'Unknown')
        date = data.get('date', 'Unknown')
        package = data.get('package', 'None Selected')

        if not SENDER_PASSWORD:
            return jsonify({
                "error": "Server misconfiguration",
                "message": "GMAIL_APP_PASSWORD is not set in the .env file."
            }), 500

        # Construct the email content
        subject = f"New Booking Enquiry from {name} - FLASHOOT!"
        body = f"""
        New Booking Request Received!
        -----------------------------
        Name: {name}
        Email: {email}
        Phone: {phone}
        Occasion: {occasion}
        City: {city}
        Date: {date}
        Package Selected: {package}
        """

        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = TARGET_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email using Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return jsonify({"success": True, "message": "Enquiry submitted successfully!"}), 200

    except smtplib.SMTPAuthenticationError:
        return jsonify({
            "error": "Authentication Failed", 
            "message": "Failed to log in to Gmail. Please check your App Password in the .env file."
        }), 401
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


if __name__ == '__main__':
    print("Starting Flashoot Email Backend on http://localhost:5000 ...")
    
    import webbrowser
    from threading import Timer
    import os
    
    def open_browser():
        file_url = "http://localhost:5000/"
        
        # Try specific Chrome path, otherwise fallback to the system default browser
        try:
            chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
            webbrowser.get(chrome_path).open(file_url)
        except webbrowser.Error:
            try:
                chrome_path_x86 = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
                webbrowser.get(chrome_path_x86).open(file_url)
            except webbrowser.Error:
                webbrowser.open(file_url)

    # Only open browser once (prevents double tabs when Flask reloads in debug mode)
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        Timer(1.5, open_browser).start()

    app.run(debug=True, port=5000)
