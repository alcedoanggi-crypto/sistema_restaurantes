# 🍽️ Sistema de Gestión de Restaurantes

Aplicación web para la administración operativa de un restaurante:
pedidos, mesas, menú y control de ventas.

Este proyecto demuestra desarrollo backend con **Python y Flask**,
arquitectura **MVC**, y persistencia de datos con **PostgreSQL**.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📸 Vista Previa

> Agrega aquí 2-3 capturas de pantalla (mapa de mesas, toma de pedido,
> cierre de cuenta).
>
> ```markdown
> ![Mapa de mesas](docs/screenshots/mesas.png)
> ![Toma de pedido](docs/screenshots/pedido.png)
> ```

**Demo en vivo:** _(agrega aquí el link si despliegas en Render/Railway)_

---

## 🚀 Características Principales

- **Gestión de mesas:** control de estado (libre, ocupada, reservada).
- **Toma de pedidos:** selección de platos/bebidas del menú por mesa.
- **Menú digital:** productos organizados por categoría con precio.
- **Cierre de cuenta:** cálculo automático del total por mesa, con opción
  de dividir cuenta.
- **Reportes de ventas:** consulta de ventas por día/producto.
- **Autenticación de usuarios:** control de acceso para meseros/admin.

## 🛠️ Tecnologías Utilizadas

| Categoría        | Tecnología                                   |
|-------------------|-----------------------------------------------|
| Backend           | Python 3.11 + Flask                           |
| Base de datos     | PostgreSQL (gestionada con Flask-SQLAlchemy)  |
| Frontend          | HTML5 (Jinja2), CSS3, JavaScript              |
| Seguridad         | Variables de entorno (python-dotenv)          |

## 📁 Estructura del Proyecto

```
sistema_restaurantes/
├── app/
│   ├── static/        # CSS, JS y recursos estáticos
│   ├── templates/      # Vistas Jinja2 (mesas, pedidos, menú)
│   ├── models.py       # Estructura de la base de datos (Mesa, Producto, Pedido)
│   └── routes.py       # Lógica de navegación y toma de pedidos
├── config.py            # Configuración segura del servidor
├── requirements.txt      # Dependencias del proyecto
├── run.py                # Punto de entrada de la aplicación
└── .env.example           # Ejemplo de variables de entorno requeridas
```

---

## 🔧 Instalación y Uso Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/alcedoanggi-crypto/sistema_restaurantes.git
cd sistema_restaurantes
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv

# En Linux/Mac
source venv/bin/activate

# En Windows
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto basado en `.env.example`:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta_aqui
DATABASE_URL=postgresql://usuario:password@localhost:5432/restaurante_db
```

### 5. Crear la base de datos y aplicar migraciones

```bash
flask db upgrade
```

> Si el proyecto no usa Flask-Migrate todavía, inicializa las tablas con:
> `python -c "from app import db; db.create_all()"`

### 6. (Opcional) Cargar datos de prueba

```bash
python seed.py
```

### 7. Ejecutar la aplicación

```bash
flask run
```

La aplicación estará disponible en `http://127.0.0.1:5000`

**Credenciales de prueba** _(si aplica)_:
- Usuario: `admin@demo.com`
- Contraseña: `demo1234`

---

## 🧪 Próximas Mejoras

- [ ] Comanda digital para cocina en tiempo real
- [ ] Integración con impresora de tickets
- [ ] Tests automatizados con Pytest
- [ ] Despliegue con Docker

## 👩‍💻 Autora

**Anggie Alcedo** — Ingeniera de Sistemas | Full Stack Developer & QA
Automation
[GitHub](https://github.com/alcedoanggi-crypto) ·
[LinkedIn](#) · alcedoanggi@gmail.com

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más
detalles.
