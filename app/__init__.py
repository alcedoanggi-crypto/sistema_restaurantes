from flask import Flask
from app.models import db, User  # Importamos db y el modelo User
from werkzeug.security import generate_password_hash # Para encriptar la clave
import os

def create_app():
    app = Flask(__name__)

    # Configuración de seguridad y base de datos
    app.config['SECRET_KEY'] = 'dev_key_123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schema.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar la base de datos
    db.init_app(app)

    # Registrar las rutas (Blueprint)
    from app.routes import main
    app.register_blueprint(main)

    # Crear tablas y usuario administrador por defecto
    with app.app_context():
        db.create_all()

        # Verificamos si ya existe el usuario 'admin' para no duplicarlo
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password=generate_password_hash('admin123'), # Clave encriptada
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("Usuario admin creado con éxito: admin / admin123")
        else:
            print("El usuario admin ya existe en la base de datos.")

    return app