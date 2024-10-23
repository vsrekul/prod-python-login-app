from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Ensure that the environment variables (POSTGRES_HOST, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD) are set in your container, whether through Kubernetes secrets.
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'),
        database=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD')
    )
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            flash('Login successful!', 'success')
            return redirect(url_for('welcome'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    return 'Welcome to the application!'

if __name__ == '__main__':
    app.run(debug=True)
