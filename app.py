from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the MySQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/chrisBase'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)


# Define a function to create the database tables
def create_tables():
    with app.app_context():
        db.create_all()

# Route to create the tables (you can call this route to create the tables)
@app.route('/create_tables', methods=['GET'])
def create_database_tables():
    create_tables()
    return 'Database tables created successfully!'

@app.route('/')
def hello_world():
    return 'Hello, World!'


# Route to create a new product
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(name=data['name'], quantity=data['quantity'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

# Route to retrieve all products
@app.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    product_list = [{'id': product.id, 'name': product.name, 'quantity': product.quantity, 'price': product.price} for product in products]
    return jsonify(product_list)


if __name__ == '__main__':
    app.run(debug=True)