from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars_1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db object
db = SQLAlchemy(app)

class Cars(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key = True)
    make = db.Column(db.String)
    model = db.Column(db.String)
    color = db.Column(db.String)
    year = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __init__(self, make, model, color, year, price):
        self.make = make
        self.model = model
        self.color = color
        self.year = year
        self.price = price

    def __str__(self):
        return f"{self.make} {self.model} {self.color} {self.year} {self.price}"

@app.route('/')
def home():
    search_text = request.args.get('paieskoslaukelis')
    if search_text:
        all_rows = Cars.query.filter(Cars.make.ilike(search_text + '%')).all()
    else:
        all_rows = Cars.query.all()
    return render_template('index.html', all_rows=all_rows)

@app.route('/masinos/<int:cars_id>', methods=['POST'])
def one_car(cars_id):
    one_row = Cars.query.get(cars_id)
    return render_template('one_car.html', one_row=one_row)

#Create
@app.route('/masinos/naujas', methods=['GET', 'POST'])
def new_car():
    if request.method == 'GET':
        return render_template('new_car.html')
    elif request.method == 'POST':
        make = request.form.get('makelaukas')
        model = request.form.get('modellaukas')
        color = request.form.get('colorlaukas')
        year = request.form.get('yearlaukas')
        price = request.form.get('pricelaukas')
        if make and model and price:
            try:
                year_int = int(year) if year else None
                price_int = int(price)
            except ValueError:
                return "Metai ir kaina turi buti skaiciai"
            new_row = Cars(make,
                                  model,
                                  color,
                                  year_int,
                                  price_int)
            db.session.add(new_row)
            db.session.commit()
    return redirect(url_for('home'))

#Delete
@app.route('/masinos/trinti/<int:cars_id>', methods=['POST'])
def delete_car(cars_id):
    row = Cars.query.get(cars_id)
    db.session.delete(row)
    db.session.commit()
    return redirect(url_for('home'))

#Update
@app.route('/masinos/redaguoti/<int:cars_id>', methods=['POST', 'GET'])
def update_car(cars_id):
    row = db.session.get(Cars, cars_id)

    if not row:
        return "Nuoroda neegzistuoja"

    if request.method == 'GET':
        return render_template('update_car.html', row=row)

    elif request.method == 'POST':
        make = request.form.get('makelaukas')
        model = request.form.get('modellaukas')
        color = request.form.get('colorlaukas')
        year = request.form.get('yearlaukas')
        price = request.form.get('pricelaukas')

        if make and model and price:
            row.make = make
            row.model = model
            row.color = color
            row.year = int(year)
            row.price = int(price)

            db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)