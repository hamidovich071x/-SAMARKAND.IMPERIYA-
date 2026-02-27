from flask import Flask, request, redirect, session
import requests
import json
import os
from datetime import datetime

ORDERS_FILE = "orders.json"
FOODS_FILE = "foods.json"

def load_json(file):
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

orders = load_json(ORDERS_FILE)
foods = load_json(FOODS_FILE)
app = Flask(__name__)
app.secret_key = "taylaqfood"

TELEGRAM_TOKEN = "8532829799:AAHp4rZ43UUGjuvrDBPFA5LFKW_OENnP9ds"
CHAT_ID = "8435898042"

def send_to_telegram(text):
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=5)
    except:
        pass

ADMIN_PASSWORD = "1234"

# ===== Global Data =====
orders = []
# ===== MENU =====
menu = {
    "Osh": {"price": 25000, "img": "https://images.unsplash.com/photo-1604908177522-0409cfe7c36d", "reviews":[]},
    "Lag‘mon": {"price": 30000, "img": "https://images.unsplash.com/photo-1625944525533-473f1a3f87b5", "reviews":[]},
    "Manti": {"price": 28000, "img": "https://images.unsplash.com/photo-1626078292169-35d6a8b5f9e4", "reviews":[]},
    "Shashlik": {"price": 32000, "img": "https://images.unsplash.com/photo-1594007650254-586b20b86909", "reviews":[]},
    "Chuchvara": {"price": 27000, "img": "https://images.unsplash.com/photo-1603077912333-4c0d176c8ff1", "reviews":[]},
    "Somsa": {"price": 15000, "img": "https://images.unsplash.com/photo-1617196036473-1479b6b80b4d", "reviews":[]},
    "Qovurma": {"price": 29000, "img": "https://images.unsplash.com/photo-1617195875918-08beef688c85", "reviews":[]},
    "Beshbarmak": {"price": 31000, "img": "https://images.unsplash.com/photo-1617196031123-9ff5e4d6f92f", "reviews":[]},
    "Qazi": {"price": 35000, "img": "https://images.unsplash.com/photo-1603077912332-4c0d176c8ff2", "reviews":[]},
    "Chuchvara Sho‘rva": {"price": 26000, "img": "https://images.unsplash.com/photo-1603077912334-4c0d176c8ff3", "reviews":[]},
    "Osh Qo‘zi": {"price": 33000, "img": "https://images.unsplash.com/photo-1604908177523-0409cfe7c36e", "reviews":[]},
    "Tandir Kabob": {"price": 36000, "img": "https://images.unsplash.com/photo-1603077912335-4c0d176c8ff4", "reviews":[]},
    "Piyozli Kabob": {"price": 28000, "img": "https://images.unsplash.com/photo-1603077912336-4c0d176c8ff5", "reviews":[]},
    "Baliq Qovurish": {"price": 34000, "img": "https://images.unsplash.com/photo-1603077912337-4c0d176c8ff6", "reviews":[]},
    "Tovuq Sho‘rva": {"price": 22000, "img": "https://images.unsplash.com/photo-1603077912338-4c0d176c8ff7", "reviews":[]},
    "Sabzavotli Plov": {"price": 24000, "img": "https://images.unsplash.com/photo-1603077912339-4c0d176c8ff8", "reviews":[]},
    "Achchiq Osh": {"price": 25000, "img": "https://images.unsplash.com/photo-1603077912340-4c0d176c8ff9", "reviews":[]},
    "Goshtli Lag‘mon": {"price": 31000, "img": "https://images.unsplash.com/photo-1603077912341-4c0d176c8ffa", "reviews":[]},
    "Tandir Somsa": {"price": 16000, "img": "https://images.unsplash.com/photo-1603077912342-4c0d176c8ffb", "reviews":[]},
}

fast_food = {
    "Burger": {"price": 30000, "img": "https://images.unsplash.com/photo-1550547660-d9450f859349", "reviews":[]},
    "Pizza": {"price": 45000, "img": "https://images.unsplash.com/photo-1548365328-8b849e6e3b45", "reviews":[]},
    "Hot Dog": {"price": 20000, "img": "https://images.unsplash.com/photo-1606755962772-043896a72f0c", "reviews":[]},
    "Fries": {"price": 10000, "img": "https://images.unsplash.com/photo-1559628235-fbd3d6c7b4b7", "reviews":[]},
    "Cheeseburger": {"price": 35000, "img": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd", "reviews":[]},
    "Chicken Nuggets": {"price": 25000, "img": "https://images.unsplash.com/photo-1604917864687-5b8f246a1b2d", "reviews":[]},
    "Veggie Burger": {"price": 30000, "img": "https://images.unsplash.com/photo-1598514983614-1a5b9b48e5b1", "reviews":[]},
    "BBQ Burger": {"price": 38000, "img": "https://images.unsplash.com/photo-1603077912343-4c0d176c8ffc", "reviews":[]},
    "Double Burger": {"price": 42000, "img": "https://images.unsplash.com/photo-1603077912344-4c0d176c8ffd", "reviews":[]},
    "Pepperoni Pizza": {"price": 47000, "img": "https://images.unsplash.com/photo-1603077912345-4c0d176c8ffe", "reviews":[]},
    "Margarita Pizza": {"price": 43000, "img": "https://images.unsplash.com/photo-1603077912346-4c0d176c8fff", "reviews":[]},
    "Hawaiian Pizza": {"price": 45000, "img": "https://images.unsplash.com/photo-1603077912347-4c0d176c8ff0", "reviews":[]},
    "Meat Pizza": {"price": 48000, "img": "https://images.unsplash.com/photo-1603077912348-4c0d176c8ff1", "reviews":[]},
    "Cheese Pizza": {"price": 44000, "img": "https://images.unsplash.com/photo-1603077912349-4c0d176c8ff2", "reviews":[]},
    "Chicken Pizza": {"price": 46000, "img": "https://images.unsplash.com/photo-1603077912350-4c0d176c8ff3", "reviews":[]},
    "Fries Large": {"price": 12000, "img": "https://images.unsplash.com/photo-1603077912351-4c0d176c8ff4", "reviews":[]},
    "Onion Rings": {"price": 15000, "img": "https://images.unsplash.com/photo-1603077912352-4c0d176c8ff5", "reviews":[]},
    "Taco": {"price": 22000, "img": "https://images.unsplash.com/photo-1603077912353-4c0d176c8ff6", "reviews":[]},
    "Wrap": {"price": 25000, "img": "https://images.unsplash.com/photo-1603077912354-4c0d176c8ff7", "reviews":[]},
}

drinks = {
    "Cola": {"price": 10000, "img": "https://images.unsplash.com/photo-1629203851122-3726ecdf080e", "reviews":[]},
    "Choy": {"price": 5000, "img": "https://images.unsplash.com/photo-1544787219-7f47ccb76574", "reviews":[]},
    "Coffee": {"price": 12000, "img": "https://images.unsplash.com/photo-1603077912355-4c0d176c8ff8", "reviews":[]},
    "Tea Latte": {"price": 14000, "img": "https://images.unsplash.com/photo-1603077912356-4c0d176c8ff9", "reviews":[]},
    "Orange Juice": {"price": 15000, "img": "https://images.unsplash.com/photo-1603077912357-4c0d176c8ffa", "reviews":[]},
    "Lemonade": {"price": 12000, "img": "https://images.unsplash.com/photo-1603077912358-4c0d176c8ffb", "reviews":[]},
    "Milkshake": {"price": 20000, "img": "https://images.unsplash.com/photo-1603077912359-4c0d176c8ffc", "reviews":[]},
    "Green Tea": {"price": 10000, "img": "https://images.unsplash.com/photo-1603077912360-4c0d176c8ffd", "reviews":[]},
    "Cappuccino": {"price": 18000, "img": "https://images.unsplash.com/photo-1603077912361-4c0d176c8ffe", "reviews":[]},
    "Espresso": {"price": 16000, "img": "https://images.unsplash.com/photo-1603077912362-4c0d176c8fff", "reviews":[]},
    "Iced Coffee": {"price": 18000, "img": "https://images.unsplash.com/photo-1603077912363-4c0d176c8ff0", "reviews":[]},
    "Hot Chocolate": {"price": 15000, "img": "https://images.unsplash.com/photo-1603077912364-4c0d176c8ff1", "reviews":[]},
    "Soda": {"price": 12000, "img": "https://images.unsplash.com/photo-1603077912365-4c0d176c8ff2", "reviews":[]},
    "Energy Drink": {"price": 20000, "img": "https://images.unsplash.com/photo-1603077912366-4c0d176c8ff3", "reviews":[]},
    "Water": {"price": 5000, "img": "https://images.unsplash.com/photo-1603077912367-4c0d176c8ff4", "reviews":[]},
    "Herbal Tea": {"price": 12000, "img": "https://images.unsplash.com/photo-1603077912368-4c0d176c8ff5", "reviews":[]},
    "Fruit Juice": {"price": 15000, "img": "https://images.unsplash.com/photo-1603077912369-4c0d176c8ff6", "reviews":[]},
    "Smoothie": {"price": 18000, "img": "https://images.unsplash.com/photo-1603077912370-4c0d176c8ff7", "reviews":[]},
    "Iced Tea": {"price": 14000, "img": "https://images.unsplash.com/photo-1603077912371-4c0d176c8ff8", "reviews":[]},
}
5
# ===== HELPER FUNCTIONS =====
def page(title, body, extra_head=""):
    return f"""
<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Poppins:wght@300;400;500&display=swap" rel="stylesheet">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{font-family:'Segoe UI',sans-serif;color:#333;background:#fefefe;}}
header {{position:fixed;width:100%;top:0;background:#222;padding:20px 40px;display:flex;justify-content:space-between;align-items:center;z-index:1000;}}
header h1 {{color:#d4af37;font-family:'Playfair Display',serif;}}
nav a {{color:#aaa;margin-left:20px;text-decoration:none;transition:0.3s;}}
nav a:hover {{color:#d4af37;}}
.hero {{height:80vh;background:url("https://images.unsplash.com/photo-1414235077428-338989a2e8c0") center/cover no-repeat;display:flex;align-items:center;justify-content:center;text-align:center;position:relative;}}
.hero::after {{content:"";position:absolute;inset:0;background:linear-gradient(to bottom,rgba(0,0,0,0.5),rgba(0,0,0,0.7));}}
.hero-content {{position:relative;z-index:2;color:#fff;max-width:800px;padding:20px;}}
.hero h2 {{font-family:'Playfair Display',serif;font-size:clamp(32px,5vw,72px);letter-spacing:2px;margin-bottom:20px;}}
.hero p {{font-family:'Poppins',sans-serif;font-size:20px;font-weight:300;margin-bottom:30px;opacity:0.9;}}
.btn {{font-family:'Poppins',sans-serif;background:#d4af37;color:#000;padding:14px 32px;border-radius:50px;text-decoration:none;font-weight:500;transition:0.3s;}}
.btn:hover {{background:#fff;transform:translateY(-3px);}}
.section {{padding:140px 40px 80px;text-align:center;}}
.container {{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:30px;margin-top:40px;}}
.card {{background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 8px 25px rgba(0,0,0,0.1);transition:0.3s ease;cursor:pointer;}}
.card img {{width:100%;height:220px;object-fit:cover;display:block;transition:0.3s ease;}}
.card:hover {{transform:scale(1.05);box-shadow:0 12px 30px rgba(0,0,0,0.2);}}
.card h3 {{margin:15px 0 8px;font-family:'Playfair Display',serif;}}
.card p {{margin-bottom:15px;color:#555;}}
.box {{max-width:600px;margin:40px auto;}}
input,textarea,select {{width:100%;padding:12px;margin-bottom:15px;border:1px solid #ccc;border-radius:8px;}}
footer {{background:#222;color:#fff;text-align:center;padding:25px;margin-top:80px;}}
.review {{margin:10px 0;padding:10px;background:#f0f0f0;border-radius:8px;text-align:left;}}
.slider {{display:flex;overflow-x:auto;gap:20px;scroll-behavior:smooth;padding-bottom:20px;}}
.slider::-webkit-scrollbar {{display:none;}}
.card-detail img {{width:100%;max-height:400px;object-fit:cover;}}
{extra_head}

</style>
</head>
<body>
<header>
<h1>TAYLAQ</h1>
<nav>
<a href="/">Bosh sahifa</a>
<a href="/fast">Fast Food</a>
<a href="/drinks">Ichimliklar</a>
<a href="/cart">Savat</a>
<a href="/contact">Aloqa</a>
<a href="/admin">Admin</a> 
</nav>

</header>
{f'''
<div class="hero">
  <div class="hero-content">
    <h2>Taylaq Food</h2>
    <p>Taomlar — lazzat bilan</p>
    <a href="#menu" class="btn">Menyu</a>
  </div>
</div>
''' if title=="Bosh sahifa" else ''}
<div class="section" id="menu">{body}</div>
<footer>© 2026 Taylaq Food</footer>
</body>
</html>
"""

# ===== CARDS WITH REVIEWS =====
def cards(data):
    html="<div class='slider'>"
    for n,i in data.items():
        review_html = "".join(f"<div class='review'>⭐ {r[0]} — {r[1]}: {r[2]}</div>" for r in i.get("reviews",[]))
        html+=f"""
        <div class="card" onclick="location.href='/detail/{n}'">
        <img src="{i['img']}" alt="{n}">
        <h3>{n}</h3>
        <p>{i['price']} so'm</p>
        {review_html}
        </div>"""
    return html+"</div>"

# ===== DETAIL PAGE =====
def detail_card(name, info):
    review_html = "".join(f"<div class='review'>⭐ {r[0]} — {r[1]}: {r[2]}</div>" for r in info.get("reviews",[]))
    return f"""
    <div class="box card-detail">
        <img src="{info['img']}">
        <h2>{name}</h2>
        <p>Narx: {info['price']} so'm</p>
        <a class="btn" href="/add/{name}">Savatga qo‘shish</a>
        <h3>Izohlar</h3>
        {review_html}
        <form method="post" action="/review/{name}">
            <input name="name" placeholder="Ismingiz" required>
            <input name="rating" type="number" min="1" max="5" placeholder="Ball 1-5" required>
            <textarea name="text" placeholder="Izoh" required></textarea>
            <button class="btn" type="submit">Yuborish</button>
        </form>
    </div>
    """

def price_of(n):
    for c in (menu, fast_food, drinks):
        if n in c:
            return c[n]["price"]
    return 0

def get_item(n):
    for c in (menu, fast_food, drinks):
        if n in c:
            return c[n]
    return None

# ===== ROUTES =====
@app.route("/")
def home():
    return page("Bosh sahifa", cards(menu))

@app.route("/fast")
def fast():
    return page("Fast Food", cards(fast_food))

@app.route("/drinks")
def drink():
    return page("Ichimliklar", cards(drinks))

@app.route("/detail/<n>")
def detail(n):
    info = get_item(n)
    if not info:
        return redirect("/")
    return page(n, detail_card(n, info))

@app.route("/review/<item>", methods=["POST"])
def review(item):
    name=request.form.get("name","Anonim")
    rating=request.form.get("rating","5")
    text=request.form.get("text","")
    info = get_item(item)
    if info:
        info["reviews"].append((rating,name,text))
    return redirect(request.referrer or "/")

# ===== SEARCH / FILTER =====
@app.route("/search")
def search():
    query = request.args.get("q","").lower()
    min_price = request.args.get("min","")
    max_price = request.args.get("max","")
    result={}
    for category in (menu, fast_food, drinks):
        for name, info in category.items():
            if query in name.lower():
                ok=True
                if min_price.isdigit() and info['price']<int(min_price):
                    ok=False
                if max_price.isdigit() and info['price']>int(max_price):
                    ok=False
                if ok:
                    result[name]=info
    return page("Qidiruv natijalari", cards(result) or "<p>Hech nima topilmadi</p>")

# ===== CART & PAYMENT =====
@app.route("/add/<n>")
def add(n):
    if 'cart' not in session:
        session['cart']=[]
    if price_of(n)>0:
        session['cart'].append(n)
    session.modified=True
    return redirect(request.referrer or "/")

@app.route("/cart")
def cart_page():
    cart_items = session.get('cart',[])
    total=sum(price_of(i) for i in cart_items)
    items="".join(f"<p>• {i} — {price_of(i)} so'm</p>" for i in cart_items) or "<p>Savat bo‘sh</p>"
    return page("Savat", f"""
    <div class="box">
    {items}<hr>
    <input placeholder="Manzil (+uy raqami, ko‘cha)" id="address">
    <h3>Jami: {total} so'm</h3>
    <a class="btn" href="/payment">To‘lov</a>
    </div>""")

@app.route("/payment", methods=["GET","POST"])
def payment():
    if request.method=="POST":
        cart_items = session.get('cart',[])
        if cart_items:
            total=sum(price_of(i) for i in cart_items)
            text="🍽 YANGI BUYURTMA\n\n"
            for i in cart_items:
                text+=f"• {i} — {price_of(i)} so'm\n"
            text+=f"\n💰 Jami: {total} so'm"
            send_to_telegram(text)
            orders.append({"items": cart_items.copy(), "total": total, "status":"Qabul qilindi"})
            session['cart']=[]
            session.modified=True
            return page("OK","<div class='box'><h2>Buyurtma yuborildi</h2></div>")
    return page("To‘lov","""<div class="box">
    <form method="post">
    <input placeholder="Karta (TEST)">
    <input placeholder="CVV">
    <button type="submit" class="btn">To‘lash</button>
    </form></div>""")

# ===== CONTACT =====
@app.route("/contact", methods=["GET","POST"])
def contact():
    msg=""
    if request.method=="POST":
        name=request.form.get("name","")
        phone=request.form.get("phone","")
        email=request.form.get("email","")
        text=request.form.get("text","")
        if len(name)<3 or "@" not in email or not phone.startswith("+998"):
            msg="<p style='color:red'>Ma'lumotlar noto‘g‘ri</p>"
        else:
            send_to_telegram(f"📩 XABAR\n{name}\n{phone}\n{text}")
            msg="<p style='color:lightgreen'>Xabar yuborildi</p>"
    return page("Aloqa",f"""
    <div class="box">
    {msg}
    <form method="post">
    <input name="name" placeholder="Ism">
    <input name="phone" placeholder="+998...">
    <input name="email" placeholder="Email">
    <textarea name="text" placeholder="Xabar"></textarea>
    <button type="submit" class="btn">Yuborish</button>
    </form></div>""")
@app.route("/admin_login", methods=["GET","POST"])
def admin_login():
    msg=""
    if request.method=="POST":
        if request.form.get("password")==ADMIN_PASSWORD:
            session["admin"]=True
            return redirect("/admin")
        else:
            msg="❌ Parol xato"
    return page("Admin Login",f"""
    <div class='box'>
    <h2>Admin Login</h2>
    <form method='post'>
    <input type='password' name='password' placeholder='Parol'>
    <button class='btn'>Kirish</button>
    </form>
    <p style='color:red'>{msg}</p>
    </div>
    """)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/admin", methods=["GET","POST"])
def admin():
    if not session.get("admin"):
        return redirect("/admin_login")

    global orders, foods
    msg = ""

    if request.method == "POST":
        # ====== ORDER DELETE ======
        if "delete_order" in request.form:
            idx = int(request.form.get("delete_order"))
            if 0 <= idx < len(orders):
                orders.pop(idx)
                save_json(ORDERS_FILE, orders)
                msg = "✅ Buyurtma o‘chirildi"

        # ====== STATUS UPDATE ======
        elif "update_status" in request.form:
            idx = int(request.form.get("index"))
            new_status = request.form.get("status")
            if 0 <= idx < len(orders):
                orders[idx]["status"] = new_status
                save_json(ORDERS_FILE, orders)
                text = "🔄 BUYURTMA STATUS YANGILANDI\n\n"
                text += ", ".join(orders[idx]["items"])
                text += f"\nYangi holat: {new_status}"
                send_to_telegram(text)
                msg = "✅ Status yangilandi"

        # ====== FOOD ADD ======
        elif "add_food" in request.form:
            name = request.form.get("food_name", "").strip()
            price_str = request.form.get("food_price", "").strip()
            if not name or not price_str:
                msg = "❌ Iltimos, nom va narxni kiriting"
            else:
                try:
                    price = int(price_str)
                    foods.append({"name": name, "price": price})
                    save_json(FOODS_FILE, foods)
                    msg = "✅ Ovqat qo‘shildi"
                except ValueError:
                    msg = "❌ Narxni to‘g‘ri kiriting"

        # ====== FOOD DELETE ======
        elif "delete_food" in request.form:
            delete_idx = request.form.get("delete_food")
            if delete_idx and delete_idx.isdigit():
                idx = int(delete_idx)
                if 0 <= idx < len(foods):
                    foods.pop(idx)
                    save_json(FOODS_FILE, foods)
                    msg = "✅ Ovqat o‘chirildi"

        # ====== FOOD EDIT ======
        elif "edit_food" in request.form:
            idx_str = request.form.get("food_index", "").strip()
            name = request.form.get("food_name", "").strip()
            price_str = request.form.get("food_price", "").strip()

            if not idx_str.isdigit():
                msg = "❌ Xato index"
            elif not name or not price_str:
                msg = "❌ Nomi va narxni to‘ldiring"
            else:
                try:
                    idx = int(idx_str)
                    price = int(price_str)
                    if 0 <= idx < len(foods):
                        foods[idx]["name"] = name
                        foods[idx]["price"] = price
                        save_json(FOODS_FILE, foods)
                        msg = "✅ Ovqat tahrirlandi"
                except ValueError:
                    msg = "❌ Narxni to‘g‘ri kiriting"

    # ===== STATISTIKA =====
    total_orders = len(orders)
    total_income = sum(o["total"] for o in orders)
    delivered = len([o for o in orders if o["status"] == "Yetkazildi"])
    cooking = len([o for o in orders if o["status"] == "Tayyorlanmoqda"])

    # ===== ORDER TABLE =====
    order_rows = ""
    for i, o in enumerate(orders):
        items = ", ".join(o['items'])
        order_rows += f"""
        <tr>
        <td>{o.get('date','')}</td>
        <td>{items}</td>
        <td>{o['total']} so'm</td>
        <td>{o['status']}</td>
        <td>
        <form method='post'>
        <input type='hidden' name='index' value='{i}'>
        <select name='status'>
            <option>Qabul qilindi</option>
            <option>Tayyorlanmoqda</option>
            <option>Yetkazildi</option>
        </select>
        <button name='update_status'>OK</button>
        <button name='delete_order' value='{i}' style='background:red;color:white'>O‘chirish</button>
        </form>
        </td>
        </tr>
        """

    # ===== FOOD TABLE =====
    food_rows = ""
    for i, f in enumerate(foods):
        food_rows += f"""
        <tr>
        <td>{f['name']}</td>
        <td>{f['price']} so'm</td>
        <td>
        <form method='post'>
        <input type='hidden' name='food_index' value='{i}'>
        <input type='text' name='food_name' value='{f['name']}'>
        <input type='number' name='food_price' value='{f['price']}'>
        <button name='edit_food'>Saqlash</button>
        <button name='delete_food' value='{i}' style='background:red;color:white'>O‘chirish</button>
        </form>
        </td>
        </tr>
        """

    return page("Admin Panel", f"""
    <div class='box'>
        <div style='display:flex;justify-content:space-between'>
            <h2>Admin Panel</h2>
            <a href='/logout' class='btn'>Logout</a>
        </div>

        <h3>📊 Dashboard</h3>
        <div style='display:flex;gap:20px;flex-wrap:wrap'>
            <div class='card'>📦 {total_orders}</div>
            <div class='card'>💰 {total_income} so'm</div>
            <div class='card'>🚚 {delivered}</div>
            <div class='card'>🍳 {cooking}</div>
        </div>

        <hr>

        <h3>🧾 Buyurtmalar</h3>
        <table border='1' width='100%'>
            <tr>
                <th>Sana</th>
                <th>Mahsulotlar</th>
                <th>Summa</th>
                <th>Status</th>
                <th>Amal</th>
            </tr>
            {order_rows}
        </table>

        <hr>

        <h3>🍔 Ovqat qo‘shish</h3>
        <form method='post'>
            <input type='text' name='food_name' placeholder='Nomi'>
            <input type='number' name='food_price' placeholder='Narxi'>
            <button name='add_food'>Qo‘shish</button>
        </form>

        <h3>📋 Ovqatlar ro‘yxati</h3>
        <table border='1' width='100%'>
            <tr>
                <th>Nomi</th>
                <th>Narxi</th>
                <th>Amal</th>
            </tr>
            {food_rows}
        </table>

        <p>{msg}</p>
    </div>
    """)
# ===== RUN =====
if __name__ == "__main__":
    app.run()