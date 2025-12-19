from flask import Flask, render_template, request # type: ignore

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html') 

@app.route('/login',methods =['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print (f"Username: {username}, Password: {password}")
    return render_template('login.html') 

if __name__ == '__main__':
    app.run(debug=True)








    