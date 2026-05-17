from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os
from app.models import db, User, Product, TableModel, Order, OrderItem

main = Blueprint('main', __name__)

# Configuración de carpeta para imágenes
# Asegúrate de que esta ruta exista en tu proyecto
UPLOAD_FOLDER = 'app/static/uploads/products'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """Comprueba si la extensión del archivo es permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('main.dashboard'))
        else:
            flash('Credenciales incorrectas.', 'danger')
    return render_template('login.html')


@main.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    tables = TableModel.query.order_by(TableModel.number).all()
    products = Product.query.all()
    return render_template('dashboard.html', tables=tables, products=products)


@main.route('/settings', methods=['GET', 'POST'])
def settings():
    # 1. Verificación de seguridad: Solo administradores
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('No tienes permisos de administrador', 'warning')
        return redirect(url_for('main.dashboard'))

    # 2. Procesamiento de formularios (POST)
    if request.method == 'POST':
        action = request.form.get('action')

        # Lógica para crear un nuevo producto
        if action == 'create_product':
            name = request.form.get('name')
            price_str = request.form.get('price')
            price = float(price_str) if price_str else 0.0
            image_filename = None

            # Procesamiento de la imagen
            file = request.files.get('image')
            if file and allowed_file(file.filename):
                # Generamos un nombre seguro usando el nombre del producto
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = secure_filename(f"{name}.{ext}")

                # Crear carpeta si no existe
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)

                # Guardar el archivo físicamente
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                image_filename = filename

            # Crear producto en la base de datos
            new_product = Product(
                name=name,
                price=price,
                image_url=image_filename
            )
            db.session.add(new_product)

        # Lógica para crear una nueva mesa
      # Lógica para crear una nueva mesa
        elif action == 'create_table':
            number = request.form.get('number')
            if number:
                # 1. Verificar si la mesa ya existe para evitar el IntegrityError
                existing_table = TableModel.query.filter_by(number=number).first()
                
                if existing_table:
                    flash(f'La mesa número {number} ya existe en el sistema.', 'danger')
                    return redirect(url_for('main.settings'))
                
                try:
                    # 2. Si no existe, procedemos a crearla
                    new_table = TableModel(number=number, status='disponible')
                    db.session.add(new_table)
                    db.session.commit()
                    flash(f'Mesa {number} añadida correctamente.', 'success')
                except Exception as e:
                    db.session.rollback() # Revierte cambios si hay error
                    flash('Error al guardar la mesa. Inténtalo de nuevo.', 'danger')
            
            return redirect(url_for('main.settings'))

        # Lógica para crear un nuevo usuario
        elif action == 'create_user':
            username = request.form.get('username')
            password = generate_password_hash(request.form.get('password'))
            role = request.form.get('role', 'mesero')
            db.session.add(User(username=username, password=password, role=role))

        # Guardar todos los cambios realizados en el POST
        db.session.commit()
        flash('Registro creado exitosamente', 'success')
        return redirect(url_for('main.settings'))

    # 3. Preparación de la vista (GET)
    # Consultamos todos los productos para que se listen en la tabla inferior
    products = Product.query.all()

    # IMPORTANTE: Pasamos la variable 'products' al template
    return render_template('settings.html', products=products)

@main.route('/edit_product/<int:product_id>', methods=['POST'])
def edit_product(product_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'status': 'error', 'message': 'No autorizado'}), 403

    product = Product.query.get_or_404(product_id)
    product.name = request.form.get('name')
    product.price = float(request.form.get('price'))

    # Procesar nueva imagen solo si se sube una
    file = request.files.get('image')
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = secure_filename(f"{product.name}_{product_id}.{ext}")
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        product.image_url = filename

    db.session.commit()
    flash('Producto actualizado correctamente', 'success')
    return redirect(url_for('main.settings'))

# --- RUTA PARA ELIMINAR PRODUCTO ---
@main.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'status': 'error', 'message': 'No autorizado'}), 403

    product = Product.query.get_or_404(product_id)

    # Opcional: Eliminar la imagen del servidor si existe
    if product.image_url:
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, product.image_url))
        except:
            pass  # Si no existe el archivo, ignorar error

    db.session.delete(product)
    db.session.commit()
    flash('Producto eliminado con éxito', 'success')
    return redirect(url_for('main.settings'))


# --- RUTA PARA CONSULTA/DETALLE (JSON) ---
@main.route('/get_product/<int:product_id>')
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'image_url': product.image_url
    })

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))


# Agrega estas rutas a tu archivo routes.py
# --- EN ROUTES.PY ---

@main.route('/save_order', methods=['POST'])
def save_order():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'No autorizado'}), 401

    data = request.json
    table_id = data.get('table_id')
    items = data.get('items')

    if not items:
        return jsonify({'status': 'error', 'message': 'El pedido está vacío'}), 400

    total_order = sum(item['price'] * item['qty'] for item in items)

    # 1. Crear la orden
    new_order = Order(table_id=table_id, total=total_order, user_id=session['user_id'])
    db.session.add(new_order)
    db.session.flush()  # Para obtener el ID de la orden antes del commit

    # 2. Guardar detalles con notas
    for item in items:
        # Si hay una nota, la incluimos entre paréntesis en el nombre
        full_name = item['name']
        if item.get('note') and item['note'].strip() != "":
            full_name += f" ({item['note'].strip()})"

        detail = OrderItem(
            order_id=new_order.id,
            product_name=full_name,
            quantity=item['qty'],
            subtotal=item['price'] * item['qty']
        )
        db.session.add(detail)

    # 3. Marcar mesa como ocupada
    table = TableModel.query.get(table_id)
    if table:
        table.status = 'ocupada'

    db.session.commit()

    # IMPORTANTE: Devolvemos order_id para que el JS sepa qué imprimir en cocina
    return jsonify({
        'status': 'success',
        'message': 'Pedido enviado a cocina',
        'order_id': new_order.id
    })


@main.route('/get_table_order/<int:table_id>')
def get_table_order(table_id):
    """Ruta para que la cajera vea el consumo actual de una mesa ocupada"""
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'No autorizado'}), 401

    order = Order.query.filter_by(table_id=table_id).order_by(Order.id.desc()).first()

    if not order:
        return jsonify({'status': 'order_not_found', 'items': []})

    items = OrderItem.query.filter_by(order_id=order.id).all()

    order_data = []
    for item in items:
        # Estimamos precio unitario para el carrito del dashboard
        price = item.subtotal / item.quantity if item.quantity > 0 else 0
        order_data.append({
            'name': item.product_name,
            'qty': item.quantity,
            'price': price
        })

    return jsonify({
        'status': 'success',
        'items': order_data,
        'total': order.total
    })

@main.route('/checkout/<int:table_id>', methods=['POST'])
def checkout(table_id):
    # Restricción: Solo el admin (cajero) puede liberar la mesa y cobrar
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'status': 'error', 'message': 'Solo caja puede cobrar'}), 403

    table = TableModel.query.get_or_404(table_id)
    # Busca el último pedido realizado para esta mesa
    order = Order.query.filter_by(table_id=table_id).order_by(Order.id.desc()).first()

    if not order:
        return jsonify({'status': 'error', 'message': 'No hay consumos registrados'}), 404

    # Acción de la Cajera: Liberar la mesa
    table.status = 'disponible'
    db.session.commit()

    return jsonify({
        'status': 'success',
        'order_id': order.id
    })


@main.route('/print_ticket/<int:order_id>')
def print_ticket(order_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    order = Order.query.get_or_404(order_id)
    items = OrderItem.query.filter_by(order_id=order_id).all()

    # Cambiamos 'ticket_print.html' por nuestro nuevo 'invoice_print.html'
    return render_template('invoice_print.html', order=order, items=items)

@main.route('/add_table')
def add_table():
    # Aquí irá tu lógica para crear mesas
    return "Pantalla para crear mesas"

@main.route('/add_user')
def add_user():
    # Aquí irá tu lógica para registrar usuarios
    return "Pantalla para registrar usuarios"


@main.route('/print_pre_cuenta/<int:table_id>')
def print_pre_cuenta(table_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    # Buscamos el último pedido abierto de esa mesa
    order = Order.query.filter_by(table_id=table_id).order_by(Order.id.desc()).first()

    if not order:
        return "<h3>No hay consumos activos para esta mesa.</h3>", 404

    # Obtenemos los productos de ese pedido
    items = OrderItem.query.filter_by(order_id=order.id).all()

    return render_template('pre_cuenta.html', order=order, items=items)

# --- RUTAS PARA EL MÓDULO DE COCINA ---

@main.route('/cocina')
def cocina():
    """Muestra la pantalla con los pedidos pendientes para el chef."""
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    # Solo permitimos acceso a 'admin' o un rol 'cocina' (si lo tienes creado)
    if session.get('role') not in ['admin', 'cocina']:
        flash('No tienes permiso para acceder a cocina', 'danger')
        return redirect(url_for('main.dashboard'))

    # Buscamos los items que NO estén listos, ordenados por el más antiguo primero
    pendientes = OrderItem.query.filter_by(status='pendiente').order_by(OrderItem.id.asc()).all()
    
    return render_template('cocina.html', pendientes=pendientes)


@main.route('/item_listo/<int:item_id>', methods=['POST'])
def item_listo(item_id):
    """Marca un plato individual como terminado."""
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'No autorizado'}), 401

    item = OrderItem.query.get_or_404(item_id)
    
    try:
        item.status = 'listo'
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Plato marcado como listo'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@main.route('/print_kitchen/<int:order_id>')
def print_kitchen(order_id):
    """Ruta para imprimir la comanda física en la impresora de cocina."""
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    order = Order.query.get_or_404(order_id)
    items = OrderItem.query.filter_by(order_id=order_id).all()

    # Usa el archivo kitchen_ticket.html que ya tienes creado
    return render_template('kitchen_ticket.html', order=order, items=items)