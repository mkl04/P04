from flask import Flask, render_template, request, jsonify
from flask import request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pickle

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/p04' #p04
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

dict_label = {0: 'Setosa', 
              1: 'Versicolor',
              2: 'Virginica'}

model = pickle.load(open('res/model.pkl', 'rb'))

class Replier(db.Model):
    __tablename__ = 'register' #register
    id = db.Column(db.Integer, primary_key=True)
    petal_length = db.Column(db.Float)
    petal_width = db.Column(db.Float)
    pred = db.Column(db.Integer)

    def __init__(self, petal_length, petal_width, pred):
        self.petal_length = petal_length
        self.petal_width = petal_width
        self.pred = pred

    def __repr__(self):
        return '<Prediction %r>' % self.pred

db.create_all()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/inference')
def infere():
    all_data = Replier.query.all()
    return render_template('inference.html', employees = all_data, dict_aux = dict_label)

@app.route('/insert', methods=['POST'])
def insert():

    if request.method == 'POST':
        
        pl = request.form['petal_length']
        pw = request.form['petal_width']

        m = np.array([[pl,pw]])
        inf = model.predict(m)[0]

        replier = Replier(pl, pw, int(inf))
        db.session.add(replier)
        try:
            db.session.commit()
        except:
            print("error for insert db")
        
        return redirect(url_for('infere'))


@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Replier.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('infere'))

@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        my_data = Replier.query.get(request.form.get('id'))
 
        my_data.petal_length = request.form['petal_length']
        my_data.petal_width = request.form['petal_width']
        my_data.pred  = int(model.predict(np.array([[request.form['petal_length'],request.form['petal_width']]]))[0])
 
        db.session.commit()
 
        return redirect(url_for('infere'))

# Keep running
if __name__ == '__main__':
    app.run(port=3000, debug=True)
