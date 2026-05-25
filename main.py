from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'секретный_ключ_123456'  # Нужен для работы сессий

# Список цветов
flowers = [
    {"id": 1, "name": "Альстромерия", "price": 150, "color": "белые", "image_url": "/static/photo/Альстромерия.jpg"},
    {"id": 2, "name": "Верба", "price": 100, "color": "белые", "image_url": "/static/photo/Верба.jpg"},
    {"id": 3, "name": "Гвоздика", "price": 150, "color": "красные", "image_url": "/static/photo/Гвоздика.jpg"},
    {"id": 4, "name": "Георгин", "price": 180, "color": "розовый", "image_url": "/static/photo/Георгин.jpg"},
    {"id": 5, "name": "Пион", "price": 200, "color": "бежевые", "image_url": "/static/photo/Пионы.jpg"},
    {"id": 6, "name": "Хризантема", "price": 180, "color": "розовый", "image_url": "/static/photo/Хризантемы.jpg"},
]

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Каталог
@app.route('/catalog')
def catalog():
    return render_template('catalog.html', flowers=flowers)

# Добавление в корзину
@app.route('/add_to_cart/<int:flower_id>')
def add_to_cart(flower_id):
    # Получаем корзину из сессии (если нет - создаём пустую)
    cart = session.get('cart', {})
    
    # Увеличиваем количество товара в корзине
    if str(flower_id) in cart:
        cart[str(flower_id)] += 1
    else:
        cart[str(flower_id)] = 1
    
    # Сохраняем корзину обратно в сессию
    session['cart'] = cart
    
    return redirect(url_for('catalog'))

# Просмотр корзины
@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    
    for flower_id, quantity in cart.items():
        flower = next((f for f in flowers if f['id'] == int(flower_id)), None)
        if flower:
            subtotal = flower['price'] * quantity
            total += subtotal
            cart_items.append({
                'id': flower['id'],
                'name': flower['name'],
                'price': flower['price'],
                'image': flower['image'],
                'quantity': quantity,
                'subtotal': subtotal
            })
    
    return render_template('cart.html', cart_items=cart_items, total=total)

# Обновление количества в корзине
@app.route('/update_cart', methods=['POST'])
def update_cart():
    cart = session.get('cart', {})
    
    flower_id = request.form.get('flower_id')
    quantity = int(request.form.get('quantity'))
    
    if quantity <= 0:
        # Удаляем товар из корзины
        cart.pop(flower_id, None)
    else:
        cart[flower_id] = quantity
    
    session['cart'] = cart
    return redirect(url_for('cart'))

# Удаление товара из корзины
@app.route('/remove_from_cart/<int:flower_id>')
def remove_from_cart(flower_id):
    cart = session.get('cart', {})
    cart.pop(str(flower_id), None)
    session['cart'] = cart
    return redirect(url_for('cart'))

# Оформление заказа (страница с формой)
@app.route('/checkout')
def checkout():
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('catalog'))
    
    cart_items = []
    total = 0
    
    for flower_id, quantity in cart.items():
        flower = next((f for f in flowers if f['id'] == int(flower_id)), None)
        if flower:
            subtotal = flower['price'] * quantity
            total += subtotal
            cart_items.append({
                'name': flower['name'],
                'quantity': quantity,
                'price': flower['price'],
                'subtotal': subtotal
            })
    
    return render_template('checkout.html', cart_items=cart_items, total=total)

# Обработка заказа (когда нажали "Оплатить")
@app.route('/place_order', methods=['POST'])
def place_order():
    # Получаем данные из формы
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')
    
    # Здесь можно сохранить заказ в базу данных
    # Пока просто выводим подтверждение
    
    # Очищаем корзину
    session.pop('cart', None)
    
    return render_template('order_confirmation.html', name=name)

# Контакты
@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

# Очистка корзины (для тестирования)
@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('catalog'))

@app.route('/flower')
def flower():
    return render_template('flower.html', flowers=flowers)

if __name__ == '__main__':
    app.run(debug=True)