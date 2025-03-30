from flask import Flask, request, jsonify, session
from flask_session import Session
from models import db, bcrypt, User, Product
from config import Config

app = Flask(__name__)  # Initialize Flask app
app.config.from_object(Config)  # Load config
db.init_app(app)  # Initialize database
bcrypt.init_app(app)  # Initialize Bcrypt
Session(app)  # Initialize session

# Create database tables
with app.app_context():
    db.create_all()

### AUTH ROUTES ###

@app.route("/register", methods=["POST"])
def register():
    data = request.json  # Get request data
    if User.query.filter_by(username=data["username"]).first():  # Check if user exists
        return jsonify({"message": "User already exists"}), 400
    
    user = User(username=data["username"])  # Create new user
    user.set_password(data["password"])  # Hash password
    db.session.add(user)  # Add user to DB
    db.session.commit()  # Save changes
    return jsonify({"message": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json  # Get request data
    user = User.query.filter_by(username=data["username"]).first()  # Find user
    if user and user.check_password(data["password"]):  # Check password
        session["user_id"] = user.id  # Store user ID in session
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)  # Remove user from session
    return jsonify({"message": "Logout successful"}), 200

### PRODUCT ROUTES ###

@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()  # Get all products
    return jsonify([{
        "id": p.id, "name": p.name, "description": p.description,
        "price": p.price, "stock": p.stock
    } for p in products]), 200

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get(product_id)  # Find product by ID
    if not product:  # Check if product exists
        return jsonify({"message": "Product not found"}), 404
    return jsonify({
        "id": product.id, "name": product.name,
        "description": product.description, "price": product.price,
        "stock": product.stock
    }), 200

@app.route("/products", methods=["POST"])
def add_product():
    if "user_id" not in session:  # Require login
        return jsonify({"message": "Unauthorized"}), 403
    
    data = request.json  # Get request data
    product = Product(
        name=data["name"], description=data["description"],
        price=data["price"], stock=data["stock"]
    )  # Create product
    db.session.add(product)  # Add to DB
    db.session.commit()  # Save changes
    return jsonify({"message": "Product added"}), 201

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    if "user_id" not in session:  # Require login
        return jsonify({"message": "Unauthorized"}), 403

    product = Product.query.get(product_id)  # Find product
    if not product:  # Check if product exists
        return jsonify({"message": "Product not found"}), 404
    
    data = request.json  # Get request data
    product.name = data.get("name", product.name)  # Update name if provided
    product.description = data.get("description", product.description)  # Update description if provided
    product.price = data.get("price", product.price)  # Update price if provided
    product.stock = data.get("stock", product.stock)  # Update stock if provided
    db.session.commit()  # Save changes
    return jsonify({"message": "Product updated"}), 200

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    if "user_id" not in session:  # Require login
        return jsonify({"message": "Unauthorized"}), 403
    
    product = Product.query.get(product_id)  # Find product
    if not product:  # Check if product exists
        return jsonify({"message": "Product not found"}), 404

    db.session.delete(product)  # Delete product
    db.session.commit()  # Save changes
    return jsonify({"message": "Product deleted"}), 200

### PRODUCT QUERY API ###

@app.route("/products/search", methods=["GET"])
def search_products():
    query = request.args.get("q", "")  # Get search query
    products = Product.query.filter(Product.name.ilike(f"%{query}%")).all()  # Search products
    return jsonify([{
        "id": p.id, "name": p.name, "description": p.description,
        "price": p.price, "stock": p.stock
    } for p in products]), 200

if __name__ == "__main__":
    app.run(debug=True)  # Run Flask app