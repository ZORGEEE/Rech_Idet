from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("main.html")

@app.route("/instruction")
def instruction():
    return render_template("instruction.html")

@app.route("/for_tutors")
def for_tutors():
    return render_template("for_tutors.html")

@app.route("/find")
def find():
    return render_template("find.html")

@app.route("/search_result", methods=['GET', 'POST'])
def search_result():
    if request.method == 'POST':
        # Get form data
        construction = request.form.get('construction', '')
        place = request.form.get('place', '')
        intention = request.form.get('intention', '')
        emotion = request.form.get('emotion', '')
        
        # Build the query dynamically based on provided filters
        query = 'SELECT * FROM search_results WHERE 1=1'
        params = []
        
        if construction:
            query += ' AND construction = ?'
            params.append(construction)
        if place:
            query += ' AND place = ?'
            params.append(place)
        if intention:
            query += ' AND intention = ?'
            params.append(intention)
        if emotion:
            query += ' AND emotion = ?'
            params.append(emotion)
        
        # Execute query
        conn = get_db_connection()
        results = conn.execute(query, params).fetchall()
        conn.close()
        
        print(f"Query: {query}")  # Debug print
        print(f"Params: {params}")  # Debug print
        print(f"Results: {results}")  # Debug print
        
        return render_template("search_result.html", results=results, request=request)
    
    return render_template("search_result.html", results=[], request=request)

@app.route("/contacts")
def contacts():
    return render_template("contacts.html")

if __name__ == "__main__":
    app.run(debug=True)