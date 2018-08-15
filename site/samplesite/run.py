from flask import Flask, render_template
import os
app = Flask(__name__, static_url_path='')

@app.route("/")
def index():
   return render_template("index.html")
   # return app.send_static_file('index.html')

port = int(os.getenv('PORT', 5000))
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=port, debug=True)