from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Sample cart data for demonstration
carts = {}

# Product Service URL
product_service_url = "http://localhost:5000"

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart = carts.get(user_id, {})
    return jsonify(cart)

@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    quantity = int(request.args.get('quantity', 1))

    # Get product details from the Product Service
    response = requests.get(f"{product_service_url}/products/{product_id}")
    if response.status_code != 200:
        return jsonify({"message": "Product not found"}), 404
    product = response.json()

    # Update the user's cart
    if user_id in carts:
        if product_id in carts[user_id]:
            carts[user_id][product_id]["quantity"] += quantity
        else:
            carts[user_id][product_id] = {
                "name": product["name"],
                "quantity": quantity,
                "price": product["price"] * quantity,
            }
    else:
        carts[user_id] = {product_id: {
            "name": product["name"],
            "quantity": quantity,
            "price": product["price"] * quantity,
        }}

    return jsonify({"message": "Product added to cart"}), 201

@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    quantity = int(request.args.get('quantity', 1))

    if user_id in carts and product_id in carts[user_id]:
        if quantity >= carts[user_id][product_id]["quantity"]:
            del carts[user_id][product_id]
        else:
            carts[user_id][product_id]["quantity"] -= quantity
            carts[user_id][product_id]["price"] -= quantity * \
                carts[user_id][product_id]["price"]
        return jsonify({"message": "Product removed from cart"}), 200
    else:
        return jsonify({"message": "Product not found in cart"}), 404

if __name__ == '__main__':
    app.run(debug=True)
