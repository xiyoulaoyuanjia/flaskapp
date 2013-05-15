# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
from flask import Flask, render_template, jsonify,request,url_for,g
from werkzeug import secure_filename

from vdisksdk import * 
UPLOAD_FOLDER = 'uploadDir/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


import MySQLdb as db
#from getGithubBlog import sqldb
from getGithubBlog import getGithubBlog



app = Flask(__name__)      
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/favicon.ico")
def addFavicon():
    return app.send_static_file("favicon.ico")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route("/update")
def update():
	getGithubBlog.updatemain()
    return "ok"
	

### for db 
@app.before_request
def before_request():
	### sae has the APP_NAME but local does not
	### APP_NAME：应用名
	### APP_VERSION: 当前应用使用的版本号
	### SERVER_SOFTWARE: 当前server的版本
	from os import environ
	if environ.get("SERVER_SOFTWARE", ""):
		g.db = get_db_sae()
	else :
		g.db = get_db()

def get_db_sae():
	import sae.const
#	sae.const.MYSQL_DB      # 数据库名
#	sae.const.MYSQL_USER    # 用户名
#	sae.const.MYSQL_PASS    # 密码
#	sae.const.MYSQL_HOST    # 主库域名（可读写）
#	sae.const.MYSQL_PORT    # 端口，类型为，请根据框架要求自行转换为int
#	sae.const.MYSQL_HOST_S  # 从库域名（只读）
	### stupid the port
	com=db.connect(sae.const.MYSQL_HOST,sae.const.MYSQL_USER,sae.const.MYSQL_PASS,sae.const.MYSQL_DB,charset='utf8',port=int(sae.const.MYSQL_PORT))
	return com.cursor()

def get_db():
	com=db.connect("localhost","root","","blog",charset='utf8',port=3306)
	return com.cursor()
#	import sqlite3
#	com=sqlite3.connect("getGithubBlog/getGithubBlog.db")
#	return com

def query_db(query, args=(), one=False):
    cur = g.db.execute(query,args)
	
#for sqllite3
#    rv = [dict((cur.description[idx][0], value)
#               for idx, value in enumerate(row)) for row in cur.fetchall()]
# for mysql
    rv = [dict((g.db.description[idx][0], value)
               for idx, value in enumerate(row)) for row in g.db.fetchall()]
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_db_connection(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def home():
	import base64
	blog_entries=query_db("select * from blog_entries")
	blog=[]
	blog=[{'des':base64.decodestring(blog_entry['des']),'id':blog_entry['id'] } for blog_entry in blog_entries]
	print type(base64.decodestring(blog_entry['des'])).__name__
#	return "ok"
	return render_template('getGithubBlog/home.html',blog=blog)


## about blog
@app.route('/blog/<blogId>')
def blog(blogId):
	import base64
#for sqllite3
#	blog_entries=query_db("select * from blog_entries where id=?",[blogId],one=True)
	blog_entries=query_db("select * from blog_entries where id=%s",[blogId],one=True)
	return render_template('blog.html',blog=base64.decodestring(blog_entries['text']))

@app.route('/about',methods=['post','get'])
def about():
    return render_template('about.html')



from flask.ext.mail import Message, Mail
import config
mail=Mail()
## config for mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = getattr(config,'mailName','')
app.config["MAIL_PASSWORD"] = getattr(config,'mailpasswd','')

from forms import ContactForm
app.secret_key = 'xiyoulaoyuanjia'

mail.init_app(app)


@app.route("/contact",methods=['post','get'])
def contact():
	form = ContactForm()
	if request.method == "POST":
		if form.validate() == False:
			return render_template("contact.html",form=form)
		else:
			msg = Message(form.subject.data, sender='contact@example.com', recipients=['xiyoulaoyuanjia@gmail.com'])
			msg.body = """
			      From: %s <%s>
			      %s
			      """ % (form.name.data.encode("utf-8"), form.email.data.encode("utf-8"), form.message.data.encode("utf-8"))
			mail.send(msg)
		return render_template("contact.html",success=True)
#		return "ok"
	elif request.method == "GET":
		return render_template("contact.html",form=form)


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
  return jsonify(token=client.access_token)
				
@app.route('/markdownEditor')
def markdownEditor():
  return render_template('markdownEditor/markdownEditor.html')


if __name__ == '__main__':
  app.run(debug=True)
