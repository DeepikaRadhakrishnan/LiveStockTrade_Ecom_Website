from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask_socketio import SocketIO, emit, join_room, leave_room
from engineio.payload import Payload
Payload.max_decode_packets = 200
from werkzeug.utils import secure_filename
from flask import request as flask_request


app = Flask(__name__, static_url_path='/static')
app.secret_key = 'abcdef'


socketio = SocketIO(app)

_users_in_room = {} # stores room wise user list
_room_of_sid = {} # stores room joined by an used
_name_of_sid = {} # stores display name of users



mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    charset="utf8",
    use_pure="True",
    database="livecommerce"
)

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'abcdef'

@app.route('/', methods=['GET', 'POST'])
def index():
    
    return render_template('index.html')

@app.route('/sellerwel', methods=['GET', 'POST'])
def sellerwel():
    if 'username' not in session or session.get('user_type') != 'seller':
        flash("Please log in as a seller to access the page.", 'danger')
        return redirect(url_for('seller'))

    username=session.get('username')
    
    return render_template('sellerwel.html', username=username)

@app.route('/buyerwel', methods=['GET', 'POST'])
def buyerwel():
    if 'username' not in session or session.get('user_type') != 'buyer':
        flash("Please log in as a buyer to access the page.", 'danger')
        return redirect(url_for('buyer'))
    username=session.get('username')
    
    return render_template('buyerwel.html', username=username)

@app.route('/buyerreport', methods=['GET', 'POST'])
def buyerreport():
    if 'username' not in session or session.get('user_type') != 'buyer':
        flash("Please log in as a buyer to access the page.", 'danger')
        return redirect(url_for('buyer'))

    if request.method == 'POST':
        month = request.form.get('month')
        username = session.get('username')
        cursor = mydb.cursor()

        if month:
            # Modify the SQL query to retrieve both count and total amount for the logged-in user
            cursor.execute("SELECT DATE_FORMAT(submission_datetime, '%Y-%m') as month_year, COUNT(*) as booking_count, SUM(price) as total_amount FROM tb_booking WHERE DATE_FORMAT(submission_datetime, '%Y-%m') = %s AND username = %s GROUP BY month_year", (month, username))
            data = cursor.fetchall()

            cursor.close()

            return render_template('buyerreport.html', data=data)

    return render_template('buyerreport.html', data=None)

@app.route('/livestock', methods=['GET', 'POST'])
def livestock():
    
    livestock_category = request.args.get('category')
    cursor = mydb.cursor()
    if livestock_category:
    
        cursor.execute("SELECT * FROM products WHERE vetcategory = %s", (livestock_category,))
        data = cursor.fetchall()
    
    else:
            
        cursor.execute("SELECT * FROM products")
        data = cursor.fetchall()
        
    cursor.close()
    return render_template('livestock.html', products=data)


@app.route('/myrequests1', methods=['GET', 'POST'])
def myrequests1():
    if 'username' not in session or session.get('user_type') != 'buyer':
        flash("Please log in as a buyer to access the page.", 'danger')
        return redirect(url_for('buyer'))

    username = session.get('username')
    vetcategory1 = request.args.get('vetcategory')  # Assuming this is product ID

    cursor = mydb.cursor()

    # Fetch product details
    cursor.execute("SELECT * FROM products WHERE id = %s", (vetcategory1,))
    data = cursor.fetchone()
    if not data:
        flash("Product not found!", 'danger')
        return redirect(url_for('buyer_dashboard'))

    post_id = data[0]
    cate = data[1]
    price = data[4]
    image = data[7]
    post_username = data[8]

    # Fetch buyer details
    cursor.execute("SELECT * FROM tb_buyer WHERE username = %s", (username,))
    data3 = cursor.fetchone()
    if not data3:
        flash("Buyer details not found!", 'danger')
        return redirect(url_for('buyer_dashboard'))

    user_id = data3[0]
    name = data3[1]
    buy_username = data3[2]
    mobile = data3[4]


    cursor = mydb.cursor()
        

        
    cursor.execute("SELECT max(id)+1 FROM requests1")
    maxid = cursor.fetchone()[0]
    if maxid is None:
        maxid = 1

    

    # Insert request details into the request table
    cursor.execute("""
        INSERT INTO requests1 (id, buyer_id, buyer_name, buyer_username, buyer_mobile, product_id, category, price, image, seller_username)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (maxid, user_id, name, buy_username, mobile, post_id, cate, price, image, post_username))

    mydb.commit()  # Save changes to the database

    flash("Request placed successfully!", 'success')
    return redirect(url_for('myrequests'))  # Redirect after storing the request


@app.route('/myrequests', methods=['GET'])
def myrequests():
    if 'username' not in session or session.get('user_type') != 'buyer':
        flash("Please log in as a buyer to access the page.", 'danger')
        return redirect(url_for('buyer'))

    username = session.get('username')
    cursor = mydb.cursor(dictionary=True)  # Dictionary cursor for easy access

    # Fetch all requests made by the logged-in buyer
    cursor.execute("SELECT * FROM requests1 WHERE buyer_username = %s", (username,))
    requests = cursor.fetchall()  # Get all results

    return render_template('myrequests.html', requests=requests)


@app.route('/seller_requests', methods=['GET'])
def seller_requests():
    if 'username' not in session or session.get('user_type') != 'seller':
        flash("Please log in as a seller to access this page.", 'danger')
        return redirect(url_for('seller'))

    seller_username = session.get('username')

    cursor = mydb.cursor(dictionary=True)
    
    # Fetch all requests where the seller is the logged-in user
    cursor.execute("""
        SELECT * FROM requests1 WHERE seller_username = %s
    """, (seller_username,))
    
    requests_data = cursor.fetchall()  # Get all requests related to this seller

    return render_template('seller_requests.html', requests=requests_data)

@app.route('/update_review_link', methods=['POST'])
def update_review_link():
    review_id = request.form['review_id']
    link = request.form['link']
    cursor = mydb.cursor()
    cursor.execute("UPDATE requests1 SET link=%s WHERE id=%s", (link, review_id))
    mydb.commit()
    cursor.close()
    print(f"Updated link for review {review_id}: {link}")
    return redirect(url_for('seller_requests'))



@app.route('/update_meeting', methods=['POST'])
def update_meeting():
    if 'username' not in session or session.get('user_type') != 'seller':
        flash("Unauthorized access", "danger")
        return redirect(url_for('seller'))

    request_id = request.form['request_id']
    meeting_date = request.form['meeting_date']
    meeting_time = request.form['meeting_time']

    cursor = mydb.cursor()
    zoom_link = f"https://yoom-zoom-clone.vercel.app/?room={request_id}"
    cursor.execute("""
        UPDATE requests1
        SET meeting_date = %s, meeting_time = %s, link = %s
        WHERE id = %s
    """, (meeting_date, meeting_time, zoom_link, request_id))
    mydb.commit()
    cursor.close()

    flash("Meeting details updated successfully!", "success")
    return redirect(url_for('seller_requests'))




@app.route('/details', methods=['GET', 'POST'])
def details():
    if 'username' not in session or session.get('user_type') != 'buyer':
        flash("Please log in as a buyer to access the page.", 'danger')
        return redirect(url_for('buyer'))

    vetcategory=''
      
    vetcategory1 = request.args.get('vetcategory')
    cursor = mydb.cursor()   
    cursor.execute("SELECT * FROM products WHERE id = %s", (vetcategory1,))
    data = cursor.fetchone()
    total = 0
    if request.method == 'POST':
        username=request.form.get('username')
        vetcategory=request.form.get('vetcategory')
        quantities = request.form.getlist('quantity')
        prices = request.form.getlist('price')

        cursor.execute("SELECT max(id)+1 FROM tb_total")
        maxid = cursor.fetchone()[0]
        if maxid is None:
            maxid=1
    
        
        for qty, price in zip(quantities, prices):
            # Check if qty and price are not empty before inserting into the database
            if qty and price:
                query = "INSERT INTO tb_total (id, username, vetcategory, quantity, price) VALUES (%s, %s, %s, %s, %s)"
                values = (maxid, username, vetcategory, qty, price)
                cursor.execute(query, values)
        session['quantities'] = quantities
        mydb.commit()
        cursor.close()
        
        # Calculate total based on the inserted quantities and prices
        total = sum(float(qty) * float(price) for qty, price in zip(quantities, prices) if qty and price)
        session['total'] = total
        return redirect(url_for('cart', vetcategory=vetcategory1))


    return render_template('details.html', vetcategory=vetcategory, data=data, total=total)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    

    quantities = session.get('quantities', [])
    vetcategory = request.args.get('vetcategory')
    cursor = mydb.cursor(buffered=True)   
    cursor.execute("SELECT * FROM products WHERE id = %s", (vetcategory,))
    data = cursor.fetchone()
    cursor.execute("SELECT * FROM tb_total WHERE id = %s", (vetcategory,))
    dataa = cursor.fetchone()
    
    cursor.execute("SELECT * FROM products")
    datta = cursor.fetchall()
        
    #cursor.close()

    
        
    return render_template('cart.html', vetcategory=vetcategory, data=data, dataa=dataa, products=datta, quantities=quantities)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'username' not in session or session.get('user_type') != 'buyer':
        flash("Please log in as a buyer to access the page.", 'danger')
        return redirect(url_for('buyer'))

    

    vetcategory = request.args.get('vetcategory')
    cursor = mydb.cursor()   
    cursor.execute("SELECT username FROM products WHERE id = %s", (vetcategory,))
    product_owner = cursor.fetchone()

    if product_owner:
        username = product_owner[0]

    
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM products WHERE id = %s", (vetcategory,))
    product_data = cursor.fetchone()

    username = session.get('username')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM tb_buyer WHERE username = %s", (username,))
    ownerdata = cursor.fetchone()

    quantities = session.get('quantities', [])

    if request.method == 'POST':

        # Additional fields
        uname = product_owner[0]  # Use the username fetched from the products table
        vetcategory = request.form.get('vetcategory')
        price = request.form.get('price')
        total = session.get('total', 0)


        # Retrieve form data
        name = request.form.get('name', '')
        mobileno = request.form.get('mobileno', '')
        address = request.form.get('address', '')
        payment_method = request.form.get('payment_method', '')

        # Get the current date and time
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        

        cursor = mydb.cursor()
        

        
        cursor.execute("SELECT max(id)+1 FROM tb_booking")
        maxid = cursor.fetchone()[0]
        if maxid is None:
            maxid = 1

        sql = "INSERT INTO tb_booking (id, vetcategory, uname, price, total, username, name, mobileno, address, payment_method, submission_datetime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid, vetcategory, uname, product_data[4], product_data[4], username, name, mobileno, address, payment_method, current_datetime)
        cursor.execute(sql, val)
        mydb.commit()

        return redirect(url_for('ordercomplete'))

    cursor.close()
    return render_template('checkout.html', vetcategory=vetcategory, data=product_data, ownerdata=ownerdata, quantities=quantities)

@app.route('/ordercomplete', methods=['GET', 'POST'])
def ordercomplete():
    if 'username' not in session or session.get('user_type') != 'buyer':
        flash("Please log in as a buyer to access the page.", 'danger')
        return redirect(url_for('buyer'))
    
    return render_template('ordercomplete.html')

@app.route('/myorders', methods=['GET', 'POST'])
def myorders():
    if 'username' not in session or session.get('user_type') != 'seller':
        flash("Please log in as a seller to access the page.", 'danger')
        return redirect(url_for('seller'))

    username = session.get('username')
    cursor = mydb.cursor()
    
    # Fetch booking details for the logged-in user
    cursor.execute("SELECT * FROM tb_booking WHERE uname = %s", (username,))
    data = cursor.fetchall()
    
    cursor.close()

    if request.method == 'POST':
        
        aid = request.form.get('aid')
        orderstatus = request.form.get('orderstatus')

        cursor = mydb.cursor()
        cursor.execute("UPDATE tb_booking SET orderstatus = %s WHERE id = %s", (orderstatus, aid))
        mydb.commit()
        cursor.close()

        flash("Order status updated successfully.", 'success')
        return redirect(url_for('myorders'))
    
    return render_template('myorders.html', tb_booking=data)

@app.route('/bookings', methods=['GET', 'POST'])
def bookings():
    if 'username' not in session or session.get('user_type') != 'buyer':
        flash("Please log in as a buyer to access the page.", 'danger')
        return redirect(url_for('buyer'))

    username = session.get('username')
    cursor = mydb.cursor()
    
    # Fetch booking details for the logged-in user
    cursor.execute("SELECT * FROM tb_booking WHERE username = %s", (username,))
    data = cursor.fetchall()
    
    cursor.close()

    return render_template('bookings.html', tb_booking=data)
    
@app.route('/seller', methods=['GET', 'POST'])
def seller():

    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM tb_seller WHERE username = %s AND password = %s AND action=1', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['username'] = username
            session['user_type'] = 'seller'
            flash("Logged in successfully")
            return redirect(url_for('sellerwel'))
        else:
            flash("Incorrect username/password! or your account will be pending for approval!")    
    
    return render_template('seller.html')

@app.route('/sellerreg', methods=['GET', 'POST'])
def sellerreg():

    if request.method=='POST':
        name=request.form['name']
        username=request.form['username']
        address=request.form['address']
        mobileno=request.form['mobileno']
        email=request.form['email']
        password=request.form['password']

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM tb_seller WHERE username = %s", (username,))
        existing_user = mycursor.fetchone()
        mycursor.close()

        
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('sellerreg'))

        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM tb_seller where name=%s",(name,))
        data = mycursor.fetchone()[0]
        
        if data==0:
            mycursor.execute("SELECT max(id)+1 FROM tb_seller")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1

            sql = "INSERT INTO tb_seller(id, name, username, address, mobileno, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (maxid, name, username, address, mobileno, email, password)
            mycursor.execute(sql, val)
            mydb.commit()            
            flash("Registration successfull")
            return redirect(url_for('seller'))
        else:
            flash("Registration unsuccessfull!")
    
    return render_template('sellerreg.html')


@app.route('/buyer', methods=['GET', 'POST'])
def buyer():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM tb_buyer WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
       

        if account:
            session['username'] = username
            session['user_type'] = 'buyer'
            
            flash("Logged in successfully")
            return redirect(url_for('buyerwel'))
        else:
            flash("Incorrect username/password!")

    return render_template('buyer.html')



@app.route('/buyerreg', methods=['GET', 'POST'])
def buyerreg():

    if request.method=='POST':
        name=request.form['name']
        username=request.form['username']
        address=request.form['address']
        mobileno=request.form['mobileno']
        email=request.form['email']
        password=request.form['password']

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM tb_buyer WHERE username = %s", (username,))
        existing_user = mycursor.fetchone()
        mycursor.close()

        
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('buyerreg'))

        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM tb_buyer where name=%s",(name,))
        data = mycursor.fetchone()[0]
        
        if data==0:
            mycursor.execute("SELECT max(id)+1 FROM tb_buyer")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1

            sql = "INSERT INTO tb_buyer(id, name, username, address, mobileno, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (maxid, name, username, address, mobileno, email, password)
            mycursor.execute(sql, val)
            mydb.commit()            
            flash("Registration successfull")
            return redirect(url_for('buyer'))
        else:
            flash("Registration unsuccessfull!")
    mycursor.close()
    return render_template('buyerreg.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM tb_admin WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['username'] = username
            session['user_type'] = 'admin'
            flash("Logged in successfully", 'success')
            return redirect(url_for('sellertab'))
            
        else:
            flash("Incorrect username/password!", 'danger')
            return redirect(url_for('admin'))
    
    return render_template('admin.html')

@app.route('/sellertab', methods=['GET', 'POST'])
def sellertab():
    if 'username' not in session or session.get('user_type') != 'admin':
        flash("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('admin'))
    
    act=request.args.get("act")
    cursor = mydb.cursor()
    cursor.execute("select * from tb_seller")
    data = cursor.fetchall()
    cursor.close()
    
    if act=="ok":
        aid=request.args.get("aid")
        cursor = mydb.cursor()
        cursor.execute("update tb_seller set action=1 where id=%s",(aid,))
        mydb.commit()
        print("successfully accepted")
        
    if act=="no":
        aid=request.args.get("aid")
        cursor = mydb.cursor()
        cursor.execute("update tb_seller set action=2 where id=%s",(aid,))
        mydb.commit()
        print("your account will be rejected")
    
    return render_template('sellertab.html', tb_seller=data)

@app.route('/buyertab', methods=['GET', 'POST'])
def buyertab():
    if 'username' not in session or session.get('user_type') != 'admin':
        flash("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('admin'))
    
    
    cursor = mydb.cursor()
    cursor.execute("select * from tb_buyer")
    data = cursor.fetchall()
    cursor.close()
    
    return render_template('buyertab.html', tb_buyer=data)


@app.route('/report', methods=['GET', 'POST'])
def report():
    if 'username' not in session or session.get('user_type') != 'admin':
        flash("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('admin'))
    
    return render_template('report.html')

@app.route('/reporttab', methods=['GET', 'POST'])
def reporttab():
    
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        orderstatus = request.form.get('orderstatus')
        cursor = mydb.cursor()

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            cursor.execute("SELECT * FROM tb_booking WHERE submission_datetime BETWEEN %s AND %s", (start_date, end_date))
        else:
            
        
            cursor.execute("SELECT * FROM tb_booking WHERE orderstatus LIKE %s", ('%' + orderstatus + '%',))

        data = cursor.fetchall()
    

    cursor.close()
    return render_template('reporttab.html', tb_booking=data)

@app.route('/sellerreport', methods=['GET', 'POST'])
def sellerreport():
    if 'username' not in session or session.get('user_type') != 'seller':
        flash("Please log in as a seller to access the page.", 'danger')
        return redirect(url_for('seller'))
    
    if request.method == 'POST':
        month = request.form.get('month')
        username = session.get('username')
        cursor = mydb.cursor()

        if month:
            # Modify the SQL query to retrieve both count and total amount for the logged-in user
            cursor.execute("SELECT DATE_FORMAT(submission_datetime, '%Y-%m') as month_year, COUNT(*) as booking_count, SUM(price) as total_amount FROM tb_booking WHERE DATE_FORMAT(submission_datetime, '%Y-%m') = %s AND uname = %s GROUP BY month_year", (month, username))
            data = cursor.fetchall()

            cursor.close()


            return render_template('sellerreport.html', data=data)

    return render_template('sellerreport.html', data=None)

from flask import Flask, request, session, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
import os

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'username' not in session or session.get('user_type') != 'seller':
        flash("Please log in as a seller to access the page.", 'danger')
        return redirect(url_for('seller'))

    if request.method == 'POST':
        vetcategory = request.form['vetcategory']
        breed = request.form['breed']  # Updated field name
        price = request.form['price']
        quantity = request.form['quantity']
        description = request.form['description']
        username = session['username']

        # Handle uploaded images
        images = request.files.getlist('images[]')
        image_paths = []

        for image in images:
            if image and image.filename:
                filename = secure_filename(image.filename)
                image_path = os.path.join('static/uploads', filename)
                image.save(image_path)
                image_paths.append(filename)

        # Insert into database
        mycursor = mydb.cursor()

        mycursor.execute("SELECT MAX(id) FROM products")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid = 1
        else:
            maxid += 1

        sql = """INSERT INTO products 
                 (id, vetcategory, name, price, quantity, description, images, username) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        val = (maxid, vetcategory, breed, price, quantity, description, ','.join(image_paths), username)

        mycursor.execute(sql, val)
        mydb.commit()

        flash("Livestock registered successfully!", 'success')
        return redirect(url_for('sellerwel'))

    return render_template('add.html')



###################################################################################################################




@app.route("/call", methods=["GET", "POST"])
def call():

    aid=request.args.get("aid")
    if request.method == "POST":
        room_id = request.form['room_id']
        cursor = mydb.cursor()
        cursor.execute("update requests1 set link=%s where id=%s",(room_id, aid))
        mydb.commit()
        
        return redirect(url_for("entry_checkpoint", room_id=room_id, aid=aid))

    return render_template("call.html")

@app.route("/room/<string:room_id>/")
def enter_room(room_id):
    act=request.args.get("act")
    
    
    if room_id not in session:
        return redirect(url_for("entry_checkpoint", room_id=room_id))
    
    return render_template("chatroom.html", room_id=room_id, display_name=session[room_id]["name"], mute_audio=session[room_id]["mute_audio"], mute_video=session[room_id]["mute_video"])

@app.route("/room/<string:room_id>/checkpoint/", methods=["GET", "POST"])
def entry_checkpoint(room_id):
    

    username=""
    
    if request.method == "POST":
        mute_audio = request.form['mute_audio']
        mute_video = request.form['mute_video']
        session[room_id] = {"name": username, "mute_audio":mute_audio, "mute_video":mute_video}
        return redirect(url_for("enter_room", room_id=room_id))

    return render_template("chatroom_checkpoint.html", room_id=room_id)

@socketio.on("connect")
def on_connect():
    sid = request.sid
    print("New socket connected ", sid)
    

@socketio.on("join-room")
def on_join_room(data):
    sid = request.sid
    room_id = data["room_id"]
    display_name = session[room_id]["name"]
    
    # register sid to the room
    join_room(room_id)
    _room_of_sid[sid] = room_id
    _name_of_sid[sid] = display_name
    
    # broadcast to others in the room
    print("[{}] New member joined: {}<{}>".format(room_id, display_name, sid))
    emit("user-connect", {"sid": sid, "name": display_name}, broadcast=True, include_self=False, room=room_id)
    
    # add to user list maintained on server
    if room_id not in _users_in_room:
        _users_in_room[room_id] = [sid]
        emit("user-list", {"my_id": sid}) # send own id only
    else:
        usrlist = {u_id:_name_of_sid[u_id] for u_id in _users_in_room[room_id]}
        emit("user-list", {"list": usrlist, "my_id": sid}) # send list of existing users to the new member
        _users_in_room[room_id].append(sid) # add new member to user list maintained on server

    print("\nusers: ", _users_in_room, "\n")


@socketio.on("disconnect")
def on_disconnect():
    sid = request.sid
    room_id = _room_of_sid[sid]
    display_name = _name_of_sid[sid]

    print("[{}] Member left: {}<{}>".format(room_id, display_name, sid))
    emit("user-disconnect", {"sid": sid}, broadcast=True, include_self=False, room=room_id)

    _users_in_room[room_id].remove(sid)
    if len(_users_in_room[room_id]) == 0:
        _users_in_room.pop(room_id)

    _room_of_sid.pop(sid)
    _name_of_sid.pop(sid)

    print("\nusers: ", _users_in_room, "\n")


@socketio.on("data")
def on_data(data):
    sender_sid = data['sender_id']
    target_sid = data['target_id']
    if sender_sid != request.sid:
        print("[Not supposed to happen!] request.sid and sender_id don't match!!!")

    if data["type"] != "new-ice-candidate":
        print('{} message from {} to {}'.format(data["type"], sender_sid, target_sid))
    socketio.emit('data', data, room=target_sid)


@app.route('/logout')
def logout():
    
    session.clear()
    flash("Logged out successfully", 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

