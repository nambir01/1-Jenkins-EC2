from flask import Flask, render_template
import boto3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image')
def get_image():
    s3 = boto3.client('s3')
    bucket_name = 'your
