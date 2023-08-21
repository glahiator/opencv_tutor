from flask import Flask, render_template, session, redirect, url_for, make_response
from flask import flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

class NameForm(FlaskForm):
    name = StringField("Whats your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

app = Flask(__name__)
app.config['SECRET_KEY'] = "12345678"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return f"<Role {self.name}>"

    users = db.relationship("User", backref='role', lazy="dynamic")

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return f"<User {self.username}>"
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False))

@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)

@app.route("/resp")
def response():
    response = make_response("<h1>Make response</h1>")
    response.status_code = 222
    response.set_cookie("answer", "42")
    return response

#@app.errorhandler(404)
#def page_not_found():
#    return render_template('404.html'), 404

#@app.errorhandler(500)
#def page_not_found():
#    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
