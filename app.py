from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_filter_options():
    conn = get_db_connection()
    filters = {}
    for field in ['mwu', 'context', 'roles', 'sound']:
        rows = conn.execute(f"SELECT DISTINCT {field} FROM search_results WHERE {field} IS NOT NULL AND {field} != ''").fetchall()
        filters[field] = [row[field] for row in rows]
    rows = conn.execute("SELECT DISTINCT expression FROM expressions WHERE expression IS NOT NULL AND expression != ''").fetchall()
    filters['expression'] = [row['expression'] for row in rows]
    filters['sound'] = ["Все", "Есть звук", "Нет звука"]
    conn.close()
    return filters

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
    filter_options = get_filter_options()
    return render_template("find.html", filter_options=filter_options)

@app.route("/search_result", methods=['GET', 'POST'])
def search_result():
    filter_options = get_filter_options()
    results = []
    if request.method == 'POST':
        # Get form data
        mwu = request.form.get('mwu', '')
        context = request.form.get('context', '')
        roles = request.form.get('roles', '')
        expression = request.form.get('expression', '')
        sound = request.form.get('sound', '')
        
        # Build the query dynamically based on provided filters
        query = '''
            SELECT sr.*
            FROM search_results sr
            LEFT JOIN expressions e ON sr.id = e.search_result_id
            '''

        wheres = ['1 = 1']
        params = []
        
        if mwu:
            wheres.append('sr.mwu = ?')
            params.append(mwu)
        if context:
            wheres.append('sr.context = ?')
            params.append(context)
        if roles:
            wheres.append('sr.roles = ?')
            params.append(roles)
        if expression:
            wheres.append('e.expression = ?')
            params.append(expression)
        if sound == "Есть звук":
            wheres.append('sr.sound = 1')
        elif sound == "Нет звука":
            wheres.append('sr.sound = 0')
        # if sound:
        #     wheres.append('sr.sound = ?')
        #     params.append(sound)
        
        query += ' WHERE ' + ' AND '.join(wheres)
        query += ' GROUP BY sr.id'

        # Execute query
        conn = get_db_connection()
        results = conn.execute(query, params).fetchall()
        conn.close()
        
        print(f"Query: {query}")  # Debug print
        print(f"Params: {params}")  # Debug print
        print(f"Results: {results}")  # Debug print
        
        return render_template("search_result.html", results=results, request=request, filter_options=filter_options)
    
    return render_template("search_result.html", results=[], request=request, filter_options=filter_options)

@app.route("/contacts")
def contacts():
    return render_template("contacts.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
