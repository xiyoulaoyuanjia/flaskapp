import os
import sqlite3
from flask import Flask, render_template, jsonify,request,url_for,g
from werkzeug import secure_filename

from vdisksdk import * 
UPLOAD_FOLDER = 'uploadDir/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#from getGithubBlog import sqldb

app = Flask(__name__)      
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/favicon.ico")
def addFavicon():
    return app.send_static_file("favicon.ico")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



### for db 
@app.before_request
def before_request():
	g.db = get_db()

def get_db():
        com=sqlite3.connect("getGithubBlog/getGithubBlog.db")
        return com

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_db_connection(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def home():
	blog_entries=query_db("select * from blog_entries")
	blog=[]
	blog=[{'des':blog_entry['des'],'id':blog_entry['id'] } for blog_entry in blog_entries]
	return render_template('getGithubBlog/home.html',blog=blog)


## about blog
@app.route('/blog/<blogId>')
def blog(blogId):
	blog_entries=query_db("select * from blog_entries where id=?",[blogId],one=True)
	return render_template('blog.html',blog=blog_entries['text'])


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
