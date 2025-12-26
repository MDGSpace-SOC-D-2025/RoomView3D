from flask import Flask
from auth.routes import auth_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.register_blueprint(auth_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
