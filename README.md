# 🍽️ GourmetSoft — Sistema de Gestión de Restaurantes

Sistema web para la gestión operativa de un restaurante: control de mesas en tiempo real, toma de pedidos, comandas de cocina, facturación y administración de productos, mesas y usuarios. Construido con **Flask** + **SQLAlchemy** + **Bootstrap 5**.

![Login](docs/screenshots/login.png)

---

## Índice

- [Características](#características)
- [Capturas de pantalla](#capturas-de-pantalla)
- [Stack tecnológico](#stack-tecnológico)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Credenciales por defecto](#credenciales-por-defecto)
- [Roles y permisos](#roles-y-permisos)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Configuración](#configuración)
- [Resumen de cambios de esta actualización](#resumen-de-cambios-de-esta-actualización)
- [Limitaciones conocidas / próximos pasos](#limitaciones-conocidas--próximos-pasos)

---

## Características

- **Login profesional** con diseño propio (glassmorphism, gradientes animados, mostrar/ocultar contraseña).
- **Salón en tiempo real**: mapa visual de mesas (disponible / ocupada) con actualización al instante.
- **Toma de pedidos**: buscador de productos, carrito con notas por plato, cálculo automático de total.
- **Módulo de Cocina**: lista de platos pendientes por orden, marcado individual como "listo".
- **Facturación**: pre-cuenta imprimible y factura/ticket final, además de comanda de cocina imprimible.
- **Panel de Administración** (solo `admin`):
  - CRUD completo de **productos** (crear, editar, eliminar, imagen).
  - CRUD completo de **mesas** (crear, editar número, eliminar — bloqueado si está ocupada).
  - CRUD completo de **usuarios** (crear, cambiar rol/contraseña, eliminar — con protección contra auto-eliminación y contra quedarse sin administradores).
- Base de datos con **auto-reparación de esquema**: si el modelo agrega una columna nueva, la app la añade sola a la base SQLite existente al iniciar (sin necesidad de borrar la base de datos).

## Capturas de pantalla

| Login | Salón / Mesas |
|---|---|
| ![Login](docs/screenshots/login.png) | ![Dashboard](docs/screenshots/dashboard.png) |

| Toma de pedido | Cocina |
|---|---|
| ![Pedido](docs/screenshots/pedido_modal.png) | ![Cocina](docs/screenshots/cocina.png) |

| Panel de Configuración |
|---|
| ![Settings](docs/screenshots/settings.png) |
| ![CRUD mesas y usuarios](docs/screenshots/settings_crud.png) |

## Stack tecnológico

- **Backend**: Python 3, Flask, Flask-SQLAlchemy, Flask-Login, Werkzeug
- **Base de datos**: SQLite (por defecto, configurable a PostgreSQL/MySQL vía variable de entorno)
- **Frontend**: Bootstrap 5, Font Awesome 6, JavaScript vanilla (fetch API)

## Instalación y ejecución

### Requisitos previos
- Python 3.10 o superior instalado.

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/alcedoanggi-crypto/sistema_restaurantes.git
cd sistema_restaurantes

# 2. Crear y activar un entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python run.py
```

La aplicación quedará disponible en **http://127.0.0.1:5000**.

Al iniciar por primera vez, la app crea automáticamente la base de datos SQLite (`instance/schema.db`) y un usuario administrador por defecto.

## Credenciales por defecto

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `admin123` | Administrador |

> ⚠️ **Importante**: cambia esta contraseña desde el Panel de Configuración → Control de Acceso antes de usar el sistema en un entorno real. Estas credenciales son solo para el primer acceso.

Puedes crear usuarios adicionales con rol `mesero` o `cocina` desde el mismo panel.

## Roles y permisos

| Acción | Admin | Mesero | Cocina |
|---|:---:|:---:|:---:|
| Ver salón y tomar pedidos | ✅ | ✅ | ❌ |
| Ver módulo de cocina | ✅ | ❌ | ✅ |
| Marcar platos como listos | ✅ | ❌ | ✅ |
| Facturar / cobrar mesa | ✅ | ❌ | ❌ |
| Panel de Configuración (productos, mesas, usuarios) | ✅ | ❌ | ❌ |

## Estructura del proyecto

```
sistema_restaurantes/
├── app/
│   ├── __init__.py          # Factory de la app, config y auto-migración de esquema
│   ├── models.py            # Modelos: User, Product, TableModel, Order, OrderItem
│   ├── routes.py            # Todas las rutas/vistas (blueprint "main")
│   ├── static/
│   │   ├── css/custom.css   # Estilos globales (login, dashboard, componentes)
│   │   └── uploads/products/ # Imágenes de productos subidas desde el panel
│   └── templates/           # Plantillas Jinja2 (login, dashboard, settings, cocina, tickets...)
├── docs/screenshots/        # Capturas usadas en este README
├── config.py                # Configuración (SECRET_KEY, base de datos)
├── run.py                   # Punto de entrada de la aplicación
└── requirements.txt
```

## Configuración

Por defecto la app usa SQLite sin configuración adicional. Para producción, define variables de entorno:

| Variable | Descripción | Por defecto |
|---|---|---|
| `SECRET_KEY` | Clave secreta de Flask (sesiones/cookies) | clave de desarrollo (¡cámbiala!) |
| `DATABASE_URL` | Cadena de conexión SQLAlchemy (ej. PostgreSQL) | SQLite local en `instance/schema.db` |

Ejemplo:

```bash
set SECRET_KEY=una-clave-larga-y-aleatoria
set DATABASE_URL=postgresql://usuario:clave@localhost:5432/restaurante
python run.py
```

## Resumen de cambios de esta actualización

Esta actualización tomó el MVP inicial y lo llevó a un estado más completo y production-ready:

**Backend**
- `config.py` ahora se usa realmente (antes estaba desconectado de la app).
- Corregido bug de rol inexistente (`cajera`) que rompía un enlace del menú.
- Corregido bug de base de datos: el módulo de Cocina fallaba (`OperationalError`) en bases de datos creadas antes de agregar la columna `status`; ahora la app auto-repara el esquema al iniciar.
- Nuevas rutas con validaciones: `edit_table`, `delete_table` (bloquea mesas ocupadas), `edit_user`, `delete_user` (evita autoeliminarse o borrar al último admin).
- Validación de usuario duplicado al crear accesos.
- Eliminadas rutas muertas (`/add_table`, `/add_user`) que eran solo texto de relleno.
- Eliminado `main.py` (archivo vacío sin uso; `run.py` es el punto de entrada real).

**Frontend**
- **Login rediseñado por completo**: fondo animado con gradientes, tarjeta con efecto glass, panel lateral con beneficios del sistema, mostrar/ocultar contraseña, estado de carga en el botón.
- Panel de Configuración ahora incluye listados con edición/eliminación de **mesas** y **usuarios** (antes solo se podían crear).

**Infraestructura del repositorio**
- Se agregó `.gitignore` y se dejaron de versionar `__pycache__/`, bases de datos locales (`instance/*.db`) y carpetas de IDE (`.idea/`, `.vscode/`).
- Se agregó `requirements.txt` con las dependencias exactas.
- Se agregó esta documentación (`README.md`) con capturas, credenciales y guía de instalación.

## Limitaciones conocidas / próximos pasos

- No hay migraciones formales (Alembic/Flask-Migrate); la app solo agrega columnas nuevas automáticamente, no las elimina ni renombra.
- No hay recuperación de contraseña por correo (el admin debe restablecerla manualmente desde el panel).
- No hay tests automatizados todavía.
- El servidor de desarrollo de Flask no debe usarse en producción; para producción usar un servidor WSGI como Gunicorn o Waitress detrás de un proxy (Nginx).

---

Desarrollado como sistema de gestión interno para restaurantes. Contribuciones y sugerencias son bienvenidas.
