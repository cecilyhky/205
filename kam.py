from flask import *
from collections import *
from pymysql import *
from pymysql.cursors import *


class OD_Cursor(DictCursorMixin,Cursor):
    dict_type = OrderedDict

def db():
    return connect(cursorclass=OD_Cursor,host="localhost",user="root",password="kam21008",db="cafe")

def query(sql):
    c=db()
    cur=c.cursor()
    cur.execute(sql)
    r=cur.fetchall()
    cur.close()
    return r

def insert(sql):
    c=db()
    cur=c.cursor()
    r=cur.execute(sql)
    cur.commit()
    cur.close()
    return r

app = Flask(__name__)
app.debug = True
app.secret_key = "abc"

def cookie(msgs,pagecontent):
    r=make_response(pagecontent)
    for x in msgs:
        r.set_cookie(x, msgs[x])
    print (r)
    return r

@app.route("/", defaults={'filename': 'home.html'})
@app.route("/<path:filename>", methods=['POST', 'GET'])
def getfile(filename):
    try:
        return render_template(filename)
    except Exception:
        return app.send_static_file(filename)

@app.route("/login",methods=['POST','GET'])
def login():
    print (request)
    print (request.form)
    print (request.method)
    if request.method=='POST':
        r=query("SELECT * FROM user WHERE user='"+request.form['user']+"' AND pass='"+request.form['pass']+"'")
        print (r)
        print ("len(r): ", len(r))
        if len(r) == 1:
            session['username'] = request.form['user']
            return redirect("/")
        msgs={"error": "login error"}
        return cookie(msgs,render_template("/login.html"))
    return render_template("/login.html")


@app.route("/Signup",methods=['POST','GET'])
def Signup():
    print (request)
    print (request.form)
    if request.method=='POST':
        r=insert("insert into user (user,pass,first,last,gender,phone,email) value ('" + request.form['user'] + "','" + request.form['pass'] + "','" +request.form['first']+ "', '" +request['last'] + "', '" +  request.form['gender'] +"', '" + request.form['phone'] + "', '"+request.form['email'] +   "'")
        if r > 0:
            session['user'] = request.form['user']
            return redirect("/")
        msgs={"error": "Signup error"}
        return cookie(msgs,render_template("/Signup.html"))
    return render_template("/Signup.html")

if __name__=='__main__':
    app.run('0.0.0.0',port=8080)
