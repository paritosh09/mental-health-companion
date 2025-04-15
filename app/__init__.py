from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import environ
import pymysql

# Use PyMySQL instead of MySQLdb
pymysql.install_as_MySQLdb()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Database configuration for MySQL with PyMySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 
        'mysql+pymysql://root:root@localhost/python_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Ensure all tables are created
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Error creating database tables: {e}")
    
    return app

# Create the application instance
app = create_app()

# To run the app
if __name__ == '__main__':
    app.run(debug=True)
