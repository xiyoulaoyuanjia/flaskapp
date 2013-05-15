# -*- coding: utf-8 -*-

import MySQLdb as db


#cur=com.cursor

## 插入全局对象globalName
## 表名称 blog_entries 对应的属性分别为
## oriId
## href
## text
## title

## 初始插入 默认此时数据库为空 
def initInsertGlobal(globalName):
	import base64
	cur=get_db()
	for key in globalName:
#		executeString="insert into  blog_entries(href,title,text) values (\'%s\',\'%s\',\'%s\')" % (globalName[key]['href'],globalName[key]['title'],globalName[key]['content'].replace("'","\'"))
		executeTemplate="insert into  blog_entries(href,title,text,oriId,des,datetime) values (%s,%s,%s,%s,%s,%s)" 
		cur.execute(executeTemplate,(globalName[key]['href'],globalName[key]['title'],base64.encodestring(globalName[key]['content'].encode("utf-8")),globalName[key]['id'].split("-")[0],base64.encodestring(globalName[key]['des'].encode("utf-8")),globalName[key]['datetime']))
#		cur.execute(executeTemplate,("ggg","k","ggg","UUU原价","GGGGG"))


## 更新数据库操作
def upGlobal(globalName):
	import base64
	cur=get_db()
	for key in globalName:
		executeTemplate="update  blog_entries set href=\"%s\" , title=\"%s\" ,text=\"%s\",oriId=\"%s\",des=\"%s\",datetime=\"%s\" where oriId=\"%s\"" 
		cur.execute(executeTemplate % (globalName[key]['href'].encode("utf-8"),globalName[key]['title'].encode("utf-8"),base64.encodestring(globalName[key]['content'].encode("utf-8")),globalName[key]['id'].split("-")[0].encode("utf-8"),base64.encodestring(globalName[key]['des'].encode("utf-8")),globalName[key]['datetime'].encode("utf-8"),globalName[key]['id'].split("-")[0].encode("utf-8")))
#		cur.execute(executeTemplate,("ggg","k","ggg","UUU原价","GGGGG"))
	

def get_db():
	from os import environ
	if environ.get("SERVER_SOFTWARE", ""):
    		return get_db_sae()
	else :
    		return  get_db_local()



def get_db_local():
#		com=sqlite3.connect("getGithubBlog.db")
	com=db.connect("localhost","root","","blog",charset='utf8')
	return com.cursor()


def get_db_sae():
 
    import sae.const
#    com=""
#   sae.const.MYSQL_DB      # 数据库名
#   sae.const.MYSQL_USER    # 用户名
#   sae.const.MYSQL_PASS    # 密码
#   sae.const.MYSQL_HOST    # 主库域名（可读写）
#   sae.const.MYSQL_PORT    # 端口，类型为，请根据框架要求自行转换为int
#   sae.const.MYSQL_HOST_S  # 从库域名（只读）
    ### stupid the port
    com=db.connect(sae.const.MYSQL_HOST,sae.const.MYSQL_USER,sae.const.MYSQL_PASS,sae.const.MYSQL_DB,charset='utf8',port=int(sae.const.MYSQL_PORT))
    return com.cursor()




###
def before_request():
	g.db = get_db()


## 
def close_db_connection(exception):
	if hasattr(g, 'db'):
		g.db.close()


## 返回数据库中所有blog的 orid 与 datetime
def update_db(con):
	return __query_db(con,"select oriId,datetime from blog_entries")
		

### 使用方法
## for user in query_db('select * from users'):
##    print user['username'], 'has the id', user['user_id']
###
##    user = query_db('select * from users where username = ?',
#                [the_username], one=True)
#if user is None:
#    print 'No such user'
#else:
#   print the_username, 'has the id', user['user_id']


def __query_db(con,query, args=(), one=False):
    cur = con.execute(query, args)
    rv = [dict((con.description[idx][0], value)
               for idx, value in enumerate(row)) for row in con.fetchall()]
    return (rv[0] if rv else None) if one else rv


if __name__ == "__main__":
	db=get_db()
	print update_db(db)
