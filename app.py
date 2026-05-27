from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# ---------- MENU DATA ----------
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

# ---------- DSA FEATURES ----------
# 1. Binary search helper
def binary_search_menu(query, items_list):
    """Binary search on sorted list of menu items by name."""
    low, high = 0, len(items_list) - 1
    while low <= high:
        mid = (low + high) // 2
        if items_list[mid]['name'].lower() == query.lower():
            return items_list[mid]
        elif items_list[mid]['name'].lower() < query.lower():
            low = mid + 1
        else:
            high = mid - 1
    return None

# 2. Quicksort by price
def quicksort_price(items):
    if len(items) <= 1:
        return items
    pivot = items[len(items) // 2]['price']
    left = [item for item in items if item['price'] < pivot]
    middle = [item for item in items if item['price'] == pivot]
    right = [item for item in items if item['price'] > pivot]
    return quicksort_price(left) + middle + quicksort_price(right)

# 3. FIFO queue for orders
order_queue = []
    order_queue.append(order)
    return render_template('kitchen_queue.html', orders=order_queue)

# 4. Recursive total calculator
def recursive_sum(items, index=0):
    if index >= len(items):
        return 0
    return items[index]['price'] * items[index]['quantity'] + recursive_sum(items, index + 1)

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
    sort_by = request.args.get('sort')
    if sort_by == 'price':
        all_items = []
        for cat_items in menu.values():
            all_items.extend(cat_items)
        sorted_items = quicksort_price(all_items)
        sorted_menu = {"Sorted by Price": sorted_items}
        return render_template('home.html', user=session['user'], menu=sorted_menu, best_sellers=best_sellers)
    else:
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

@app.route('/search')
def search():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    query = request.args.get('q', '')
    all_items = []
    for cat_items in menu.values():
        all_items.extend(cat_items)
    sorted_items = sorted(all_items, key=lambda x: x['name'].lower())
    result = binary_search_menu(query, sorted_items) if query else None
    return render_template('search_results.html', user=session['user'], query=query, result=result)

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
    recursive_total = recursive_sum(cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total, recursive_total=recursive_total)

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

@app.route('/place_order')
def place_order():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('view_cart'))
    all_items = [item for cat in menu.values() for item in cat]
    items_ordered = []
    total = 0
    for item_id, qty in cart.items():
        item = next((i for i in all_items if i['id'] == int(item_id)), None)
        if item:
            subtotal = item['price'] * qty
            total += subtotal
            items_ordered.append({'name': item['name'], 'qty': qty, 'price': item['price']})
    order = {
        'order_id': len(order_queue) + 1,
        'user': session['user'],
        'items': items_ordered,
        'total': total,
        'status': 'pending'
    }
    order_queue.append(order)   # enqueue
    session.pop('cart', None)
    return redirect(url_for('kitchen_queue'))

@app.route('/kitchen_queue')
def kitchen_queue():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    return render_template('kitchen_queue.html', user=session['user'], orders=order_queue)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
