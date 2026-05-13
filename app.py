from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# ---------- MENU DATA (to be filled by Hulyu) ----------
menu = {
    "Appetizers": [
        {"id": 1, "name": "Lumpiang Shanghai", "price": 149, "desc": "Crispy spring rolls", "image": "lumpia.jpg"},
        {"id": 2, "name": "Calamares", "price": 189, "desc": "Fried squid rings", "image": "calamares.jpg"},
    ],
    "Royal Specials": [
        {"id": 3, "name": "Royal Burger", "price": 180, "desc": "Double patty", "image": "royal_burger.jpg"},
        {"id": 4, "name": "Cheesecake", "price": 150, "desc": "New York style", "image": "cheesecake.jpg"},
    ],
    "Main Course": [
        {"id": 5, "name": "Lechon Kawali", "price": 259, "desc": "Crispy pork belly", "image": "lechon.jpg"},
        {"id": 6, "name": "Chicken Inasal", "price": 229, "desc": "Grilled chicken", "image": "inasal.jpg"},
        {"id": 7, "name": "Beef Bulalo", "price": 299, "desc": "Beef soup", "image": "bulalo.jpg"},
        {"id": 8, "name": "Roasted Chicken", "price": 350, "desc": "Herb roasted", "image": "roasted_chicken.jpg"},
        {"id": 9, "name": "Pizza", "price": 299, "desc": "Cheesy", "image": "pizza.jpg"},
        {"id": 10, "name": "Carbonara", "price": 220, "desc": "Creamy", "image": "carbonara.jpg"},
    ],
    "Desserts": [
        {"id": 11, "name": "Halo-Halo", "price": 149, "desc": "Shaved ice", "image": "halohalo.jpg"},
        {"id": 12, "name": "Leche Flan", "price": 89, "desc": "Caramel custard", "image": "lecheflan.jpg"},
    ],
    "Drinks": [
        {"id": 13, "name": "Iced Tea", "price": 69, "desc": "House blend", "image": "icedtea.jpg"},
        {"id": 14, "name": "Calamansi Juice", "price": 79, "desc": "Fresh", "image": "calamansi.jpg"},
    ]
}

best_sellers = [
    {"id": 3, "name": "Royal Burger", "price": 180, "desc": "Double patty", "image": "royal_burger.jpg"},
    {"id": 5, "name": "Lechon Kawali", "price": 259, "desc": "Crispy pork belly", "image": "lechon.jpg"},
    {"id": 7, "name": "Beef Bulalo", "price": 299, "desc": "Beef soup", "image": "bulalo.jpg"},
]

# ---------- ROUTES ----------
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    if username:
        session['user'] = username
        return redirect(url_for('home'))
    return redirect(url_for('login_page'))

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    return render_template('home.html', user=session['user'], menu=menu, best_sellers=best_sellers)

@app.route('/about')
def about():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    return render_template('about.html', user=session['user'])

@app.route('/service')
def service():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    return render_template('service.html', user=session['user'])

@app.route('/contact')
def contact():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    return render_template('contact.html', user=session['user'])

@app.route('/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    cart = session.get('cart', {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    session['cart'] = cart
    return redirect(request.referrer or url_for('home'))

@app.route('/cart')
def view_cart():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    cart = session.get('cart', {})
    all_items = [item for cat in menu.values() for item in cat]
    cart_items = []
    total = 0
    for item_id, qty in cart.items():
        item = next((i for i in all_items if i['id'] == int(item_id)), None)
        if item:
            subtotal = item['price'] * qty
            total += subtotal
            cart_items.append({
                'id': item['id'],
                'name': item['name'],
                'price': item['price'],
                'quantity': qty,
                'subtotal': subtotal
            })
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update_cart', methods=['POST'])
def update_cart():
    cart = session.get('cart', {})
    for key in list(cart.keys()):
        new_qty = request.form.get(f'qty_{key}')
        if new_qty and new_qty.isdigit() and int(new_qty) > 0:
            cart[key] = int(new_qty)
        else:
            cart.pop(key, None)
    session['cart'] = cart
    return redirect(url_for('view_cart'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)