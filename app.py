import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, redirect, url_for, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    food = list(db.food.find({}))
    return render_template('dashboard.html',food=food)

@app.route('/food',methods=['GET','POST'])
def food():
    food = list(db.food.find({}))
    return render_template('food.html',food=food)

@app.route('/addFood',methods=['GET','POST'])
def addFood():
    if request.method == 'POST':
        # mengambil data dari client
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']

        nama_gambar = request.files['gambar']

        if nama_gambar:
            nama_file_asli = nama_gambar.filename
            print(nama_file_asli)
            nama_file_gambar = nama_file_asli.split('/')[-1]
            file_path = f'static/assets/imgFruit/{nama_file_gambar}'
            nama_gambar.save(file_path)
        else:
            nama_gambar = None

        doc = {
            'nama': nama,
            'harga': harga,
            'gambar': nama_file_gambar,
            'deskripsi': deskripsi
        }
        db.food.insert_one(doc)
        return redirect(url_for('food'))
    return render_template('addFood.html')

@app.route('/editFood/<_id>',methods=['GET','POST'])
def editFood(_id):
    if request.method == 'POST':
        id = request.form['_id']
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        nama_gambar = request.files['gambar']

        doc = {
            'nama': nama,
            'harga': harga,
            'deskripsi': deskripsi
        }
        if nama_gambar:
            nama_file_asli = nama_gambar.filename
            print(nama_file_asli)
            nama_file_gambar = nama_file_asli.split('/')[-1]
            file_path = f'static/assets/imgFruit/{nama_file_gambar}'
            nama_gambar.save(file_path)
            doc['gambar'] = nama_file_gambar
        db.food.update_one({"_id":ObjectId(id)},{'$set':doc})
        return redirect(url_for('food'))

    id = ObjectId(_id)
    data = list(db.food.find({'_id':id}))
    return render_template('EditFood.html',data=data)

@app.route('/deleteFood/<_id>',methods=['GET','POST'])
def deleteFood(_id):
    db.food.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('food'))

if __name__ == '__main__':
    app.run(port=5000,debug=True)