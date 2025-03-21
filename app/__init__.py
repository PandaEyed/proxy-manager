from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # app = Flask(__name__)
    app = Flask(__name__, static_folder='static')
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.routes import login_manager
    login_manager.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app