
import os
import subprocess
from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]

ALLOWED = {
    "date": ["date"],
    "uptime": ["uptime"]
}


@app.after_request
def security_headers(resp):
    resp.headers["Content-Security-Policy"] = "default-src 'self'"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp


@app.route('/')
def index():
    return """
    <h1>Welcome to our Flask App!</h1>
    <ul>
        <li><a href="/hello?name=World">Hello Page</a></li>
        <li><a href="/execute?cmd=date">Execute Command Page</a></li>
    </ul>
    """


@app.route('/hello')
def hello():
    name = request.args.get('name', 'Guest')
    return f"<h1>Hello Page</h1><p>Hello, {escape(name)}!</p>"


@app.route('/execute')
def execute():
    key = request.args.get('cmd', 'date')

    if key not in ALLOWED:
        return "Commande non autorisée", 400

    result = subprocess.run(
        ALLOWED[key],
        capture_output=True,
        text=True
    )

    return (
        f"<h1>Execute Command Page</h1>"
        f"<pre>{escape(result.stdout)}</pre>"
        f"<pre>{escape(result.stderr)}</pre>"
    )


if __name__ == '__main__':
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(debug=debug, host='0.0.0.0')

