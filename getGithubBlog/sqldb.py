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
	com=get_db()
	for key in globalName:
#		executeString="insert into  blog_entries(href,title,text) values (\'%s\',\'%s\',\'%s\')" % (globalName[key]['href'],globalName[key]['title'],globalName[key]['content'].replace("'","\'"))
		executeTemplate="insert into  blog_entries(href,title,text,oriId,des) values (%s,%s,%s,%s,%s)" 
		cur = com.cursor()
		cur.execute(executeTemplate,(globalName[key]['href'],globalName[key]['title'],globalName[key]['content'].encode("utf-8"),globalName[key]['id'],globalName[key]['des']))
#		cur.execute(executeTemplate,("ggg","k","ggg","UUU原价","GGGGG"))
		com.commit()

def get_db():
#		com=sqlite3.connect("getGithubBlog.db")
		com=db.connect("localhost","root","","blog",charset='utf8')
		return com


###
def before_request():
	g.db = get_db()


## 
def close_db_connection(exception):
	if hasattr(g, 'db'):
		g.db.close()


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


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

