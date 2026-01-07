from flask import Flask, render_template
from auth.routes import auth_bp
from ml.ml_routes import ml_bp 
from flask_cors import CORS 
from config import Config


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = Config.FLASK_SECRET_KEY
    app.register_blueprint(auth_bp)
    app.register_blueprint(ml_bp)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
