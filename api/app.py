from flask import Flask, jsonify ,request
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Drink (db.Model):
    id = db.Column(db.Integer , primary_key = True )
    name = db.Column(db.String(80) , unique = True , nullable = False)
    description = db.Column(db.String(80))

    def __repr__(self) -> str:
        return f"{self.name} --- {self.description}"

@app.route('/')
def index():
    return 'hello'



@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    
    result = [{"name": drink.name, "description": drink.description} for drink in drinks]

    return {"drinks": result}

# @app.route('/drinks/<int:id>')
# def get_drinks_id(id):
#     drinks = Drink.query.get_or_404(id)
#     return jsonify({"name":drinks.name,"description":drinks.description})


# This is for Get
@app.route('/drinks/<int:id>')
def get_drink_by_string_id(id):
    try:
      drinks = Drink.query.get_or_404(id)
      return jsonify({"name":drinks.name,"description":drinks.description})
    
    except ValueError:
        return jsonify ({" Message " : "Invalid Id please provide some valid id"})
    

# This is for Post
@app.route('/drinks' , methods = ['POST'])
def add_drink():
    drink = Drink(name = request.json['name'] , description = request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id' : drink.id}

# This is for Put(Update)
@app.route('/drinks/<int:id>', methods=['PUT'])
def put_drink(id):
    drink = Drink.query.get_or_404(id)  
    data = request.get_json()

    if 'name' in data:
        drink.name = data['name']
    if 'description' in data:
        drink.description = data['description']

    db.session.commit()
    return {"Message": "Successfully Updated ✔ "}




# This is for Delete
@app.route('/drinks/<int:id>' , methods = ['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"Error ⚠ " : " Not Found " }
    db.session.delete(drink)
    db.session.commit()
    return {"Message" : "Successfully Deleted ✔ "}


if __name__ == '__main__':
    app.run(debug=True)