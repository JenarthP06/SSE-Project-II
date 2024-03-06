from flask import Flask, render_template
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

app = Flask(__name__)


supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))


@app.route('/')
def index():
    response = supabase.table('user-profile').select('*').execute()
    users = response.data if response.data else []
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
