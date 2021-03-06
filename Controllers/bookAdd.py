from flask import Flask,request,redirect,url_for,flash
from flask_restful import Resource,Api
from werkzeug.utils import secure_filename

from db import db
from Models.book import Book

class BookAdd(Resource):
    def post(self):
        title =  request.form.get("title")
        author =  request.form.get("author")
        type =  request.form.get('select_type')
        barcode =  request.form.get("barcode")
        pic = request.files['pic']
        existing_book = Book.find_barcode(barcode)

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype

        if not title or not author or not type or not barcode :
            flash("Tüm alanların doldurulması zorunludur!","wrong")
        elif existing_book:
            flash("Barkod numarası mevcut!","wrong")
        else:
            newBook = Book(title = title, author=author, type=type,barcode=barcode,status=True,img=pic.read(),mimetype=mimetype,imgname=filename)
            Book.save(newBook)
            flash("Kitap kaydedildi","success")
            return redirect(url_for("routes.admin_book"))

        return redirect(url_for("routes.admin_book"))
