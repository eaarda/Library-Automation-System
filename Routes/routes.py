from flask import Blueprint,Flask, render_template,request,redirect,url_for, session,flash
from flask_login import current_user
import datetime
from sqlalchemy import or_ ,update
import base64

from db import db
from Models.admin import Admin
from Models.user import User
from Models.book import Book
from Models.type import Type
from Models.borrow import Borrow

routes = Blueprint('routes',__name__)

@routes.route("/")
def index():
    return render_template("index.html")

@routes.route("/home")
def home():
    return render_template("home.html")

@routes.route("/admin",methods=['POST','GET'])
def admin():
        books = Book.query.all()
        return render_template("admin.html",books=books)

@routes.route("/panel")
def panel():
    return render_template("adminlogin.html")

@routes.route("/admin_book")
def admin_book():
    types = Type.query.all()
    return render_template("admin_book.html",types=types)

@routes.route("/admin_users")
def admin_users():
    users = User.query.all()
    return render_template("admin_users.html", users=users)


@routes.route("/user_book")
def user_book():
    orders = db.session.query(Borrow,Book).filter(Borrow.user_id == current_user.id).filter(Borrow.book_id== Book.id).all()
    print("***********orders********")
    print(orders)
    def convertdate(rdate):
        cdate=datetime.datetime.strptime(str(rdate).split(" ")[0], "%Y-%m-%d").date()
        return cdate
    time = datetime.datetime.now()
    return render_template("user_book.html",orders=orders,convertdate=convertdate,time=time)


@routes.route("/admin_book_search",methods=['POST'])
def admin_book_search():
    book_search = request.form.get('admin_book_search')
    search = "%{}%".format(book_search)

    if book_search:
        results = db.session.query(Book).filter(or_(Book.title.like(search),Book.author.like(search),Book.barcode.like(search))).all()
        print(results)
        if not results:
            flash("Kayıt bulunamadı")
        return render_template("admin.html",results = results)

    return redirect(url_for("routes.admin")) 

@routes.route("/member_search",methods=['POST'])
def member_search():
    member_search = request.form.get('member_search')
    search = "%{}%".format(member_search)

    if member_search:
        members = db.session.query(User).filter(User.username.like(search)).all()
        print(members)
        if not members:
            flash("Kayıt bulunamadı")
        return render_template("admin_users.html",members=members)

    return redirect(url_for("routes.admin_users")) 

@routes.route("/book_search",methods=['POST'])
def book_search():
    book_search = request.form.get('book_search')
    search = "%{}%".format(book_search)
    print(book_search)
    if book_search:
        books = db.session.query(Book).filter(or_(Book.title.like(search),Book.author.like(search))).all()
        print(books)
        if not books:
            flash("Kayıt bulunamadı")
            print("kayıt yok")
        return render_template("home.html",books=books)

    return redirect(url_for("routes.home"))

@routes.route("/profile")
def profile():
    user = db.session.query(User).filter(User.id == current_user.id).first()
    return render_template("profile.html",user=user)

@routes.route("/getInfo/<string:id>",methods=["GET"])
def getInfo(id):
    info = db.session.query(Book,Borrow,User).filter(id == Book.id).filter(Book.id==Borrow.book_id).filter(Borrow.user_id==User.id).all()
    print("********info*************")
    print(info)
    def convertdate(rdate):
        cdate=datetime.datetime.strptime(str(rdate).split(" ")[0], "%Y-%m-%d").date()
        return cdate
    def convertimg(rimg):
        cimg = base64.b64encode(rimg).decode('ascii')
        return cimg
    return render_template("info.html",info=info,convertdate=convertdate,convertimg=convertimg)




