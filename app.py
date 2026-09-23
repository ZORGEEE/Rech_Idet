from flask import Flask
from api.routes import api_bp
from web.routes import web_bp
from config.settings import Config

app = Flask(__name__)

# Регистрируем Blueprints
app.register_blueprint(api_bp)
app.register_blueprint(web_bp)

if __name__ == "__main__":
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT)
