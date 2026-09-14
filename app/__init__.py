from flask import Flask
from sqlalchemy import inspect, text
from app.models import db, User  # Importamos db y el modelo User
from werkzeug.security import generate_password_hash  # Para encriptar la clave
from config import Config


def _sync_missing_columns():
    """Añade columnas nuevas del modelo a tablas SQLite ya existentes.

    db.create_all() solo crea tablas que faltan, no altera las existentes.
    Como el proyecto no usa Alembic/Flask-Migrate, esto evita que una base
    de datos antigua (creada antes de agregar un campo al modelo) rompa
    la app con un OperationalError de columna inexistente.
    """
    inspector = inspect(db.engine)
    for model in db.Model.registry.mappers:
        table = model.local_table
        if table is None or not inspector.has_table(table.name):
            continue
        existing_columns = {col['name'] for col in inspector.get_columns(table.name)}
        for column in table.columns:
            if column.name in existing_columns:
                continue
            default_clause = ''
            if column.default is not None and column.default.is_scalar:
                default_clause = f" DEFAULT '{column.default.arg}'"
            db.session.execute(text(
                f'ALTER TABLE {table.name} ADD COLUMN {column.name} {column.type}{default_clause}'
            ))
    db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar la base de datos
    db.init_app(app)

    # Registrar las rutas (Blueprint)
    from app.routes import main
    app.register_blueprint(main)

    # Crear tablas y usuario administrador por defecto
    with app.app_context():
        db.create_all()
        _sync_missing_columns()

        # Verificamos si ya existe el usuario 'admin' para no duplicarlo
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password=generate_password_hash('admin123'),  # Clave encriptada
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("Usuario admin creado con éxito: admin / admin123")
        else:
            print("El usuario admin ya existe en la base de datos.")

    return app
