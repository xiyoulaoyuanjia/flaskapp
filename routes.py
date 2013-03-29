import os
from flask import Flask, render_template, jsonify,request
from werkzeug import secure_filename

from vdisksdk import * 
UPLOAD_FOLDER = 'uploadDir/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)      
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

 
@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/getlink')
def getlink():
  return render_template('getLink.html')

##
@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print request.files
        files = request.files.getlist("images[]")
        print files
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
   #            return jsonify(res="<h2>Successfully Uploaded Images</h2>")
        return "<h4>Successfully Uploaded Images</h4>"
#            return redirect(url_for('uploaded_file',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''





@app.route('/getlink/get_token')
def get_token():
  client = VDiskAPIClient('xiyoulaoyuanjia@gmail.com', 'yuanjia')
  client.post.auth__get_token()
#  print client.access_token
  return jsonify(token=client.access_token)
#  return jsonify(result=client.post.auth__get_token())
  

#  return jsonify(result="ggggggggggg")


				
@app.route('/markdownEditor')
def markdownEditor():
  return render_template('markdownEditor/markdownEditor.html')
				


if __name__ == '__main__':
  app.run(debug=True)
