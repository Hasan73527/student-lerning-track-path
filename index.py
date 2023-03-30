from flask import Flask 
from flask import render_template
from flask import request
from flask import session
from flask import redirect, url_for
import datetime
from flask import *  
from flask_mail import * 
from flask_pymongo import PyMongo

app = Flask(__name__) 
#Flask mail configuration  
app.config['MAIL_SERVER']='smtp.gmail.com'  
app.config['MAIL_PORT']=465  
app.config['MAIL_USERNAME'] = 'hasan735278@gmail.com'  
app.config['MAIL_PASSWORD'] = 'Hasan@123'  
app.config['MAIL_USE_TLS'] = False 
app.config['MAIL_USE_SSL'] = True  
  
#instantiate the Mail class  
mail = Mail(app)  

app.secret_key = "hasan" #For Create Session 

mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/GMIT_Flask_Mongo")
db = mongodb_client.db
 
@app.route('/')  
def indexPage():  
    return render_template('index.html')

@app.route('/userreg', methods=["GET", "POST"])  
def userregpage():
    if request.method == 'GET':
        return render_template('userreg.html')
    else:
        x = datetime.datetime.now() 
        x = ''+str(x)

        uname = request.form['fullname']
        #upass = request.form['pass']
        db.usercollection.insert_one(
        {'username': uname,
        'useremail': request.form['email'],
        'usermobile': request.form['mobile'],
        'usercountry': request.form['country'],
        'usergender': request.form['gender'],
        'userdob': request.form['dob'],
        'userpass': request.form['password'],
        'useraddress': request.form['address'],
        'regdate':x
    
        })
        msg = Message('subject', sender = 'hasan735278@gmail.com', recipients=['hasan73527@gmail.com'])  
        msg.body = 'hi, this is the mail sent by using the flask web application'  
        mail.send(msg)
        return "Mail Sent, Please check the mail id"  

        return render_template('userreg.html',msg = "REGISTRATION SUCCESSFUL")

@app.route('/userreg1', methods=["GET", "POST"])  
def userreg1page():
    if request.method == 'GET':
        return render_template('userreg1.html')
    else:
        uname = request.form['fullname']
        #upass = request.form['pass']
        db.admincollection.insert_one(
        {'username': uname,
        'useremail': request.form['email'],
        'usermobile': request.form['mobile'],
        'usercountry': request.form['country'],
        'usergender': request.form['gender'],
        'userdob': request.form['dob'],
        'userpass': request.form['password'],
        'useraddress': request.form['address'],
        })
        return render_template('userreg1.html',msg = "REGISTRATION SUCCESSFUL")


@app.route('/userlogin', methods=["GET", "POST"])  
def userloginpage(): 
    if request.method == 'GET': 
        return render_template('userlogin.html')
    else:
        user = db.usercollection.find_one(
        {'useremail': request.form['email'],
         'userpass': request.form['pass']
        })
        print(user)
        
        if user:
            #print(user['username'])
            session['uemail']= user['useremail']
            session['uname'] = user['username']
            session['usertype']= 'USER'
            return render_template('userafterlogin.html', uname = user['username'])
        else:
            return render_template('userlogin.html', errormsg = "INVALID UID OR PASSWORD")
        

@app.route('/about')  
def aboutpage():  
      return render_template('about.html') 

@app.route('/contact')  
def contact():  
      return render_template('contact.html') 

@app.route('/logout')  
def logout():  
    if 'usertype' in session:
        utype = session['usertype']
        if utype == 'ADMIN':
            session.pop('usertype',None)
        else: 
            session.pop('usertype',None)
            session.pop('uemail',None)
            session.pop('uname',None)
        return redirect(url_for('indexPage'));    
    else:  
        return '<p>user already logged out</p>' 

@app.route('/adminlogin', methods=['GET','POST'])  
def adminloginpage(): 
    if request.method == 'GET':
        return render_template('adminlogin.html')
    else:      
        adminuid = request.form['adminuserid']
        adminpass = request.form['adminpassword']

        if(adminuid == 'admin' and adminpass == 'admin'):
            session['usertype']= 'ADMIN'
            return render_template('adminafterlogin.html', utype = 'ADMIN')
        else:
            return render_template('adminlogin.html', msg = 'INVALID UID OR PASS')

@app.route('/adminhome')  
def adminafterlogin(): 
    return render_template('adminafterlogin.html')

@app.route('/viewall')  
def viewall(): 
    userobj = db.usercollection.find({})
    print(userobj)
    return render_template('viewalluser.html', userdata = userobj)


@app.route('/searchuser', methods=['GET','POST'])  
def searchUser(): 
    if request.method == 'GET':
        return render_template('searchuser.html')
    else:      
        userobj = db.usercollection.find_one(
        {'useremail': request.form['email']})
        print(userobj)
        
        if userobj:
            #print(userobj['username'])
            return render_template('searchuser.html', userdata = userobj,show_results=1)
        else:
            return render_template('searchuser.html', errormsg = "INVALID EMAIL ID")


@app.route('/delete', methods=['GET','POST'])  
def deleteUser(): 
    if request.method == 'GET':
        return render_template('deleteuser.html')
    else:      
        responsefrommongodb = db.usercollection.find_one_and_delete(
        {'useremail': request.form['email']})
        print(responsefrommongodb)
        if responsefrommongodb is not None:
            return render_template('deleteuser.html', msg = "SUCCESSFULLY DETELED")
        return render_template('deleteuser.html', msg = "INVALID EMAIL ID")

@app.route('/delete1', methods=['POST'])  
def deleteUser1():
    print(request.form['email']) 
    responsefrommongodb = db.usercollection.find_one_and_delete({'useremail': request.form['email']})
    print(responsefrommongodb)
    return redirect(url_for('viewall'))

@app.route('/delete2', methods=['POST'])  
def deleteUser2():
    print(request.form['email']) 
    responsefrommongodb = db.usercollection.find_one_and_delete({'useremail': request.form['email']})
    print(responsefrommongodb)
    return redirect(url_for('searchUser'))

@app.route('/userhome')  
def userafterlogin(): 
    return render_template('userafterlogin.html')

@app.route('/viewuserprofile')  
def viewUserProfile(): 
    uemail = session['uemail']      
    userobj = db.usercollection.find_one({'useremail': uemail})
    print(userobj)
    return render_template('viewuserprofile.html', userdata = userobj)
    
@app.route('/updateuserprofile', methods=["GET", "POST"])  
def updateUserProfile():
    if request.method == 'GET':
        uemail = session['uemail']      
        userobj = db.usercollection.find_one({'useremail': uemail})
        return render_template('updateuserprofile.html',userdata = userobj)
    else:
        db.usercollection.update_one( {'useremail': session['uemail'] },
        { "$set": { 'usermobile': request.form['mobile'],
                    'userpass': request.form['pass'],
                    'useraddress': request.form['address'] 
                  } 
        })
        return redirect(url_for('viewUserProfile'))

if __name__ == '__main__':  
   app.run(debug = True)  