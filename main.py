from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,FloatField
from wtforms.validators import DataRequired
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

url="https://api.themoviedb.org/3/search/movie"
api_key=os.getenv("api_key")

# CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"

class Base(DeclarativeBase):
    pass

db=SQLAlchemy(model_class=Base)
db.init_app(app)

class Movie(db.Model):
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    title:Mapped[str]=mapped_column(String,unique=True,nullable=False)
    year:Mapped[str]=mapped_column(String,nullable=False)
    description:Mapped[str]=mapped_column(String,nullable=False)
    rating:Mapped[float]=mapped_column(Float,nullable=True)
    ranking:Mapped[int]=mapped_column(Integer,nullable=True)
    review:Mapped[str]=mapped_column(String,nullable=True)
    img_url:Mapped[str]=mapped_column(String,nullable=False)
    
with app.app_context():
    db.create_all()

    
# CREATE TABLE

class edituser(FlaskForm):
    userreview=StringField("Review",validators=[DataRequired()])
    userrating=FloatField("Rating",validators=[DataRequired()])
    usersubmit=SubmitField("save")
    
class adduser(FlaskForm):
    title=StringField("Movie Title",validators=[DataRequired()])
    submit=SubmitField("save")

@app.route("/")
def home():
    with app.app_context():
        foren=db.session.execute(db.select(Movie).order_by(Movie.rating))
        all_cards=foren.scalars().all()
        
        for a in range(len(all_cards)):
            all_cards[a].ranking= len(all_cards)-a
        db.session.commit()
        
        all_cards.reverse()
        
        return render_template("index.html",send=all_cards)
    

@app.route("/update/<int:id>", methods=["GET","POST"])
def update(id):
    c_edit=edituser()
    if request.method == "POST":
        user_review=c_edit.userreview.data
        user_rating=c_edit.userrating.data
        
        with app.app_context():
            data=db.session.execute(db.select(Movie).where(Movie.id == id))
            edit_data=data.scalar()
            edit_data.review=user_review
            edit_data.rating=user_rating
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html',form=c_edit)

supers=[]

@app.route("/add", methods=["GET","POST"])
def add():
    global supers
    c_add=adduser()
    if request.method == "POST":
        Movie_name=c_add.title.data
        for i in range(10):
            print(i)
            try:
                api_data=requests.get(url,params={"api_key":api_key,"query":Movie_name})
                supers=api_data.json()["results"]
                
                return render_template('select.html',data_user=supers)
            except requests.exceptions.RequestException:
                pass

    return render_template('add.html',form=c_add)

@app.route('/select/<int:id>')
def select(id):
    for user in supers:
        if user['id'] == id:
            with app.app_context():
                new_movie = Movie(
                    title=user['original_title'],
                    year=user['release_date'],
                    description=user['overview'],
                    img_url=f"https://image.tmdb.org/t/p/w500{user['poster_path']}"
                    )
                db.session.add(new_movie)
                db.session.commit()
                return redirect(url_for('update',id=new_movie.id))
            break
    return f"not find"

    

@app.route("/delete/<int:id>")
def dele(id):
    with app.app_context():
        data=db.session.execute(db.select(Movie).where(Movie.id == id))
        d_data=data.scalar()
        db.session.delete(d_data)
        db.session.commit()
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
