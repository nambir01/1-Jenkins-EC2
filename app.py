from flask import Flask, render_template
import boto3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image')
def get_image():
    s3 = boto3.client('s3')
    bucket_name = 'your_s3_bucket_name'
    s3_key = 'your_s3_key'
    url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': s3_key})
    return url

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
