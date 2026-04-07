# FLASHOOT! - Photoshoot Website

A beautiful single-page website for a photography business, built with HTML, CSS, JavaScript, and a Flask backend to handle booking enquiries via email.

## Features
- **Responsive Design**: Looks great on desktop and mobile.
- **Booking Form**: Allows users to select packages, enter their details, and submit an enquiry.
- **Flask Email Backend**: Submissions are automatically emailed to the owner using Gmail SMTP.

## Project Structure
- `index.html`: The main website structure.
- `style.css`: Custom styling and responsive design rules.
- `script.js`: Interactive elements, smooth scrolling, and form submission logic.
- `backend/app.py`: The local Flask server that receives bookings and sends emails.
- `api/index.py`: The Vercel serverless function entrypoint.
- `vercel.json`: Vercel routing configuration for simple serverless deployment.

## Running Locally

1. Create a Python virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Windows
   # source .venv/bin/activate    # Mac/Linux
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup environment variables:
   Create a `.env` file in the `backend/` directory from `.env.example`:
   ```env
   GMAIL_ADDRESS=yourmail@gmail.com
   GMAIL_APP_PASSWORD=your_16_char_google_app_password
   ```

4. Start the development server:
   ```bash
   python backend/app.py
   ```
   The backend will start on http://localhost:5000 and automatically open your browser.

## Deploying to Vercel

This repository is pre-configured to be deployed natively on [Vercel](https://vercel.com).
1. Push this code to GitHub.
2. Link your repository in Vercel as a new Project.
3. In Vercel's environment variables dashboard, set `GMAIL_ADDRESS` and `GMAIL_APP_PASSWORD`.
4. Deploy! The frontend will be served as static files on the edge, and the `/api/book` endpoint will seamlessly route to the Python serverless function.
