from flask import Flask , redirect , render_template , url_for , request , session
from flask_pymongo import PyMongo
import stripe


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/shop-data"

stripe.api_key = "sk_test_51OzmpvSCSZLUuBuFtzYikQSG65DPkeZC9anPZpd1bdJiIzy4BhCd2r2UdzIYYKhbtK0CCaYWpw5zbvsFfZCRWguD00Lm7UTFti"

my_domain = "http://localhost:5500"


mongo = PyMongo(app)

app.secret_key="hello"

@app.route('/add' , methods=["POST" , "GET"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        model = request.form["model"]
        price = request.form["price"]
        link = request.form["link"]
        code = request.form["code"]
        pay = request.form["pid"]
        mongo.db.user.insert_one({"Name":name, "Model": model , "Price":price , "link":link , "code":code , "pid":pay})
        mongo.db.user.delete_one({"code" : "FFG45"})
        
    return render_template("add.html")


@app.route('/', methods=["POST","GET"])
def check():
    if request.method == "POST":
        cd = request.form["code"]
        session['ppid']=cd
        users=list(mongo.db.user.find({"code":cd}))
        for i in users:
            print(type(i['Price']))
            op = int(i['Price'])
          
        op = (op*18)/100;       
        print(op)     
        return render_template("checkout.html", details = users , price = op)
     
        
    ll = list(mongo.db.user.find({}))

    return render_template('checking.html', cc=ll)


@app.route('/checkout' , methods=["POST"])
def checkout():
    if request.method == "POST":
    #   cd = request.form["pid"]
      cd=session['ppid']
      users=list(mongo.db.user.find({"code":cd}))
      print(cd)
      pid=""
      for i in users:
         pid=i['pid']

      print("hello",pid)
      try:
         checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': pid,
                    'quantity': 1,
                },
            ],
            mode="subscription",
            success_url=my_domain + '/success.html',
            cancel_url=my_domain + '/cancel.html',
        )

         return redirect(checkout_session.url, code=303)

      except Exception as e:
        return str(e)



if __name__ == "__main__":
   app.run(debug=True)