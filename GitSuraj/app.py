from email import message
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///contact.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


# from flask_admin.contrib.sqla import ModelView
# from flask_admin import Admin
# from flask_login import UserMixin, LoginManager
# admin = Admin(app)
# login = LoginManager(app)


class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(400), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name} - {self.message}"

# admin.add_view(ModelView(Contact, db.session ))
@app.before_first_request
def create_tables():
    db.create_all()
@app.route('/', methods=["GET","POST"])
def get_contact():
    if request.method == 'POST':
        name =  request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        contact = Contact(name=name, email=email ,message=message)
        db.session.add(contact)
        db.session.commit()
        print("The data are saved !")
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=8000)