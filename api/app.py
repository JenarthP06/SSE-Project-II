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

# url = os.environ.get("SUPABASE_URL")
# key = os.environ.get("SUPABASE_KEY")


# def create_supabase_client():
#     url = os.environ.get("SUPABASE_URL")
#     key = os.environ.get("SUPABASE_KEY")
#     return create_client(url, key)


# supabase = create_supabase_client()

# # supabase = create_client(url, key)


# @app.route('/')
# def index():
#     response = supabase.table('users').select('*').execute()
#     if hasattr(response, 'data'):
#         data = response.data
#     else:
#         data = []

#     return render_template('index.html', users=data)


# if __name__ == '__main__':
#     app.run(debug=True)
