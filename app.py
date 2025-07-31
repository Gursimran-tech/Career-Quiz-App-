from flask import Flask, render_template, request, redirect,session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Guri@12345",
    database="career_db"
)
cursor = db.cursor(buffered=True)

# Home route redirects to login
@app.route('/')
def home():
    return redirect('/login')

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (name, email, password))
        db.commit()
        return redirect('/login')
    return render_template('signup.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT id, username FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', user_name=session['user_name'])
    else:
        return redirect('/login')

# Show the quiz form (GET only)
@app.route('/career_form', methods=['GET'])
def show_career_form():
    if 'user_id' in session:
        return render_template('career_form.html')
    else:
        return redirect('/login')

# Process form and show career result (POST only)
@app.route('/career_result', methods=['GET', 'POST'])
def career():
    if request.method == 'GET':
        return render_template('career_form.html')  # Show the form if user visits directly

    # Get form data
    answers = {
        'q1': request.form.get('q1'),
        'q2': request.form.get('q2'),
        'q3': request.form.get('q3'),
        'q4': request.form.get('q4'),
        'q5': request.form.get('q5'),
        'q6': request.form.get('q6'),
    }

    # Logic for recommendation
    if answers['q3'] == 'Politics' or answers['q6'] == 'History':
        career = "Civil Services (UPSC, PCS)"
        reason = "You enjoy discussing politics, history, and civics, making Civil Services a great fit."
    elif answers['q3'] == 'Tech' and answers['q6'] == 'Math':
        career = "Software Engineer / AI Engineer"
        reason = "Your interest in tech, logic, and learning on the go aligns well with Software/AI roles."
    elif answers['q3'] == 'Ideas' and answers['q4'] == 'Explore':
        career = "Startup Founder / Entrepreneur"
        reason = "You enjoy innovation, solving problems creatively, and thinking independently."
    elif answers['q3'] == 'Art' or answers['q6'] == 'Design':
        career = "UX/UI Designer or Creative Director"
        reason = "You're drawn to creative expression, design, and user experience."
    elif answers['q6'] == 'Science':
        career = "Biotech or Healthcare Professional"
        reason = "Your love for biology and scientific approach suits healthcare or research domains."
    elif answers['q5'] == 'Money':
        career = "Finance / Investment Banker / MBA"
        reason = "You’re driven by high-earning careers with growth opportunities."
    else:
        career = "Multidisciplinary Explorer"
        reason = "You have diverse interests — explore internships in tech, design, or content to decide!"

    return render_template('career_result.html', career=career, reason=reason)
# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
