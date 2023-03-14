from flask import Flask


app = Flask(__name__, template_folder='templates')
app.app_context().push()


@app.route('/')
def index():
    return 'Hello World'


if __name__ == '__main__':
    app.debug = True
    
    app.run(host='0.0.0.0', port=5000)
