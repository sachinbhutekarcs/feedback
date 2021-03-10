from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod' #global variable

if ENV == 'dev': #if ENV = dev (during developement)
    app.debug = True #debugging on
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:HareKrsna@localhost/tata' #our postgres developement data base with username:password
else: #after developement is over i.e when ENV = prod
    app.debug = False #debugging off
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lmmzugswssgmwy:94734e80041c7c10e7f86e096e172ba8865efcf17b75781589db182bb437b3a8@ec2-3-211-245-154.compute-1.amazonaws.com:5432/d54uoogu7kss60' #post developement database

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #dont know

db = SQLAlchemy(app) #passing our app to SQLAlchemy to create database object

class Feedback(db.Model): #model of database (class)
    __tablename__ = 'feedback' #creating table feedback
    id = db.Column(db.Integer, primary_key=True) #columns
    customer = db.Column(db.String(200), unique=True) #unique customer name
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments): #class constructor
        #store variable values in table feedback inside database
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments

@app.route('/') #homepage route
def index(): #whenever on homepage, call index function
    return render_template('index.html') #exexute index.html


@app.route('/submit', methods=['POST']) #handles form data from front end
def submit():
    if request.method == 'POST': #on receving POST request
        customer = request.form['customer'] #data from customer input will be stored in this variable
        dealer = request.form['dealer'] #data from dealer input will be stored in this variable
        rating = request.form['rating'] #data from rating input will be stored in this variable
        comments = request.form['comments'] #data from comment box will be stored in this variable
        # print(customer, dealer, rating, comments)
        if customer == '' or dealer == '': #if no input at customer or dealer
            return render_template('index.html', message='Please enter required fields') #redirect to index.html with message

        #making query in feedback table in database filtered by field customer, count the customer entries 
        #and if that count = 0, then that means that customer is unique and does not exist in database and we need to add him in database
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0: #if true
            data = Feedback(customer, dealer, rating, comments) #variable identical to database model
            db.session.add(data) #add that data in database
            db.session.commit() #commit to add data
            send_mail(customer, dealer, rating, comments) #call to send_mail() function
            return render_template('success.html') #if data added successfully then redirect to success.html
        return render_template('index.html', message='You have already submitted feedback') # if count != 0 then redirect to homepage with message



if __name__ == '__main__':
    app.run()