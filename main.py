from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'секретный_ключ_123456'

# Отдельные цветы (для конструктора)
individual_flowers = [
    {"id": 1, "name": "Альстромерия", "price": 150, "color": "белые", 
     "description": "Нежные цветы с экзотической красотой", 
     "image_url": "/static/photo/Альстромерия.jpg", "is_bouquet": False},
    
    {"id": 2, "name": "Верба", "price": 100, "color": "белые", 
     "description": "Пушистые весенние веточки", 
     "image_url": "/static/photo/Верба.jpg", "is_bouquet": False},
    
    {"id": 3, "name": "Гвоздика", "price": 150, "color": "красные", 
     "description": "Яркие и ароматные цветы", 
     "image_url": "/static/photo/Гвоздика.jpg", "is_bouquet": False},
    
    {"id": 4, "name": "Георгин", "price": 180, "color": "розовый", 
     "description": "Пышные махровые цветы", 
     "image_url": "/static/photo/Георгин.jpg", "is_bouquet": False},
    
    {"id": 5, "name": "Пион", "price": 200, "color": "бежевые", 
     "description": "Королевские цветы с нежным ароматом", 
     "image_url": "/static/photo/Пионы.jpg", "is_bouquet": False},
    
    {"id": 6, "name": "Хризантема", "price": 180, "color": "розовый", 
     "description": "Осенние цветы для настроения", 
     "image_url": "/static/photo/Хризантемы.jpg", "is_bouquet": False},
    
    {"id": 7, "name": "Роза красная", "price": 250, "color": "красные", 
     "description": "Королева цветов! Символ любви и страсти.", 
     "image_url": "/static/photo/красная_роза.jpg", "is_bouquet": False},
    
    {"id": 8, "name": "Роза белая", "price": 250, "color": "белые", 
     "description": "Символ чистоты и невинности.", 
     "image_url": "/static/photo/белая_роза.jpg", "is_bouquet": False},
    
    {"id": 9, "name": "Тюльпан желтый", "price": 120, "color": "желтые", 
     "description": "Весенние цветы, дарящие радость.", 
     "image_url": "/static/photo/желтый_тюльпан.jpg", "is_bouquet": False},
    
    {"id": 10, "name": "Тюльпан розовый", "price": 120, "color": "розовый", 
     "description": "Нежные весенние цветы.", 
     "image_url": "/static/photo/розовый_тюльпан.jpg", "is_bouquet": False},
    
    {"id": 11, "name": "Лилия белая", "price": 300, "color": "белые", 
     "description": "Изысканные цветы с божественным ароматом.", 
     "image_url": "/static/photo/белая_лилия.jpg", "is_bouquet": False},
    
    {"id": 12, "name": "Орхидея", "price": 450, "color": "фиолетовые", 
     "description": "Экзотическая красота!", 
     "image_url": "/static/photo/белая_орхидея.jpg", "is_bouquet": False},
]

# ГОТОВЫЕ БУКЕТЫ (отображаются в каталоге, НЕ отображаются в конструкторе)
bouquets = [
    {"id": 101, "name": "Свадебный букет", "price": 3500, "color": "белые, розовые", 
     "description": "Роскошный букет для самого важного дня в жизни. Состав: 25 роз, 7 пионов, эустома, кружево и жемчуг. Ручная работа.", 
     "image_url": "/static/photo/свадебный_букет.jpg", "is_bouquet": True},
    
    {"id": 102, "name": "Романтический букет", "price": 2800, "color": "красные, белые", 
     "description": "Букет для любимой. 25 красных роз в форме сердца и белые лилии по краям. Нежные чувства в каждом цветке.", 
     "image_url": "/static/photo/романтический_букет.jpg", "is_bouquet": True},
    
    {"id": 103, "name": "Весеннее настроение", "price": 1900, "color": "желтые, розовые", 
     "description": "Яркий букет из 15 тюльпанов, 7 нарциссов и 5 гиацинтов. Поднимет настроение и подарит весну в душе!", 
     "image_url": "/static/photo/весенний_букет.jpg", "is_bouquet": True},
    
    {"id": 104, "name": "Королевская лилия", "price": 4200, "color": "белые, золотые", 
     "description": "Эксклюзивный букет из 15 белых лилий с золотым декором и стразами. Для особенных моментов.", 
     "image_url": "/static/photo/лилейный_букет.jpg", "is_bouquet": True},
    
    {"id": 105, "name": "Детская радость", "price": 1500, "color": "разноцветные", 
     "description": "Мини-букет из 21 ромашки, васильков и маленьких хризантем. Идеален для учителей и коллег.", 
     "image_url": "/static/photo/детский_букет.jpg", "is_bouquet": True},
    
    {"id": 106, "name": "Мужской букет", "price": 2200, "color": "синие, белые", 
     "description": "Сдержанный и стильный букет из 11 ирисов, 7 эустомы и декоративной зелени. Для настоящих мужчин.", 
     "image_url": "/static/photo/мужской_букет.jpg", "is_bouquet": True},
    
    {"id": 107, "name": "День рождения", "price": 3000, "color": "ассорти", 
     "description": "Праздничный букет из 35 разных цветов: розы, хризантемы, герберы, альстромерии. Ярко, красочно, празднично!", 
     "image_url": "/static/photo/празднечный_букет.jpg", "is_bouquet": True},
    
    {"id": 109, "name": "Осенний вальс", "price": 2300, "color": "оранжевые, желтые", 
     "description": "Уютный осенний букет из хризантем, георгинов и декоративных тыквочек. Теплые оттенки осени.", 
     "image_url": "/static/photo/осенний_букет.jpg", "is_bouquet": True},
    
    {"id": 110, "name": "Нежность", "price": 2600, "color": "розовые, белые", 
     "description": "Нежный букет из 25 пионов и розовых роз. Идеальный подарок для мамы или сестры.", 
     "image_url": "/static/photo/нежный_букет.jpg", "is_bouquet": True},
    
    {"id": 111, "name": "Премиум-класс", "price": 8000, "color": "красные, золотые", 
     "description": "VIP-букет из 51 красной розы с золотым напылением. Для самых важных людей в жизни.", 
     "image_url": "/static/photo/премиум_букет.jpg", "is_bouquet": True},
]

# Объединенный список для каталога (цветы + букеты)
all_items = individual_flowers + bouquets

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Каталог (показывает все: и цветы, и букеты)
@app.route('/catalog')
def catalog():
    return render_template('catalog.html', flowers=all_items)

# Конструктор букетов (показывает только отдельные цветы)
@app.route('/flower')
def flower():
    return render_template('flower.html', flowers=individual_flowers)

# Добавление в корзину
@app.route('/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    cart = session.get('cart', {})
    
    if str(item_id) in cart:
        cart[str(item_id)] += 1
    else:
        cart[str(item_id)] = 1
    
    session['cart'] = cart
    return redirect(url_for('catalog'))

# Просмотр корзины
@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    
    for item_id, quantity in cart.items():
        item = next((i for i in all_items if i['id'] == int(item_id)), None)
        if item:
            subtotal = item['price'] * quantity
            total += subtotal
            cart_items.append({
                'id': item['id'],
                'name': item['name'],
                'price': item['price'],
                'image': item['image_url'],
                'quantity': quantity,
                'subtotal': subtotal,
                'is_bouquet': item.get('is_bouquet', False)
            })
    
    return render_template('cart.html', cart_items=cart_items, total=total)

# Обновление количества в корзине
@app.route('/update_cart', methods=['POST'])
def update_cart():
    cart = session.get('cart', {})
    
    item_id = request.form.get('flower_id')
    quantity = int(request.form.get('quantity'))
    
    if quantity <= 0:
        cart.pop(item_id, None)
    else:
        cart[item_id] = quantity
    
    session['cart'] = cart
    return redirect(url_for('cart'))

# Удаление товара из корзины
@app.route('/remove_from_cart/<int:item_id>')
def remove_from_cart(item_id):
    cart = session.get('cart', {})
    cart.pop(str(item_id), None)
    session['cart'] = cart
    return redirect(url_for('cart'))

# Оформление заказа
@app.route('/checkout')
def checkout():
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('catalog'))
    
    cart_items = []
    total = 0
    
    for item_id, quantity in cart.items():
        item = next((i for i in all_items if i['id'] == int(item_id)), None)
        if item:
            subtotal = item['price'] * quantity
            total += subtotal
            cart_items.append({
                'name': item['name'],
                'quantity': quantity,
                'price': item['price'],
                'subtotal': subtotal
            })
    
    return render_template('checkout.html', cart_items=cart_items, total=total)

# Обработка заказа
@app.route('/place_order', methods=['POST'])
def place_order():
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')
    
    session.pop('cart', None)
    
    return render_template('order_confirmation.html', name=name)

# Контакты
@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

# Поиск
@app.route('/search')
def search():
    return render_template('search.html', flowers=all_items)

# Очистка корзины
@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('catalog'))

if __name__ == '__main__':
    app.run(debug=True)