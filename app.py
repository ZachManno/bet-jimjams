from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return """
    <p style="font-size:xx-large"> <b>Jimjams BET HQ</b> </p>
    """
