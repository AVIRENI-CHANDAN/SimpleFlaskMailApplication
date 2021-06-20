from flask import Flask,render_template,request
from flask_mail import Mail, Message
import os
from mail_details import users

template_dir = os.path.relpath('../Frontend')
print("Template folder is:",template_dir)
app = Flask(__name__,template_folder=template_dir)
mail= Mail(app)

# Please add your mail credentials creating a file name mail_details.py
# Enabling the access to less secure apps in your google account.
# https://myaccount.google.com/lesssecureapps?rapt=AEjHL4PPGYf6rAt0RtxQr5ybr_N6KcHvN3aQYvsV-PAO6kSQpiT7d_k0ycME4Tnyzkq_c7CF6BzNG5rtuXDBMrNoqDzlL7N43g

# mail_details.py
# --------------------------------------------------------------------------------------

# users = {"mail_address":"example1@gmail.com","mail_password":"Password"}

# --------------------------------------------------------------------------------------

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = users['mail_address']
app.config['MAIL_PASSWORD'] = users['mail_password']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.config['FLASK_MAIL_SENDER'] = app.config['MAIL_USERNAME']
mail = Mail(app)

@app.route("/",methods=['GET','POST'])
def index():
    if request.method=="GET":
        return render_template("mail.html",messages={})
    if request.method=="POST":
        tomailaddress = request.form['tomailaddress'].split(";")
        emailsubject = request.form['emailsubject']
        emailmessage = request.form['emailmessage']
        emailsListStr = ''
        for i in tomailaddress:
            emailsListStr += i
        print("Reciepients are: ",tomailaddress)
        msg = Message(subject=emailsubject,sender = app.config['FLASK_MAIL_SENDER'], recipients = tomailaddress)
        msg.body = emailmessage
        try:
            mail.send(msg)
        except:
            error_msg = 'https://myaccount.google.com/lesssecureapps?rapt=AEjHL4PPGYf6rAt0RtxQr5ybr_N6KcHvN3aQYvsV-PAO6kSQpiT7d_k0ycME4Tnyzkq_c7CF6BzNG5rtuXDBMrNoqDzlL7N43g'
            return render_template("mail.html",messages=f"{error_msg}")
        return render_template("mail.html",messages=["Mailed",f"To:{tomailaddress}"])

if __name__ == '__main__':
   app.run(debug = True)