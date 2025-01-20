from flask import Blueprint, request, jsonify
from db.conexion import get_db_connection

producto_bp = Blueprint('producto', __name__)

@producto_bp.route('/producto', methods=['GET'])
def get_producto():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT p.id, p.nombre, p.price, p.stock, p.image_url, p.created_at, c.id AS categoria_id, c.nombre AS categoria_nombre from productos p JOIN categorias c ON p.categoria_id = c.id 
                           """)
            productos = cursor. fetchall()
            connection.close()

            #representacion de los datod en un array 

            productos_list = [
                {
                    'id': row[0],
                    'nombre': row[1],
                    'price': row[2],
                    'stock': row[3],
                    'image_url': row[4],
                    'created_at': row[5]. strftime("%Y-%m-%d %H:%M:%S"),
                    'categoria': {
                        'categoria_id': row[5],
                        'nombre': row[6]
                    }
                } for row in productos
            ]
            return jsonify(productos_list), 200
    except Exception as e:
        print(f"Error al obtener los productos: {e}")
        return jsonify({'error': 'Error al obtener los productos'}),500
    
@producto_bp.route('/crearProducto', methods=['POST'])
def post_producto():
    """
    Endpoint para crear un nuevo producto en la base de datos.
    """
    try:
        # Obtener datos de la solicitud
        data = request.get_json()
        nombre = data.get('nombre')
        price = data.get('price')
        stock = data.get('stock')
        categoria_id = data.get('categoria_id')
        image_url = data.get('image_url')
        
        # Validar que todos los campos sean proporcionados
        if not nombre or price is None or stock is None or not categoria_id or not image_url:
            return jsonify({'error': 'Todos los campos son obligatorios'}), 400
        
        # Conectar a la base de datos
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Insertar el producto en la base de datos
            cursor.execute("""
                INSERT INTO productos (nombre, price, stock, categoria_id, image_url, created_at) 
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (nombre, price, stock, categoria_id, image_url))  # Agrupar valores en una tupla
            connection.commit()
        
        # Cerrar la conexión
        connection.close()
        
        return jsonify({'message': 'Producto creado exitosamente'}), 201

    except Exception as e:
        # Manejar errores y devolver un mensaje de error genérico
        print(f"Error al crear el producto: {e}")
        return jsonify({'error': 'Error al crear el producto'}),500

@producto_bp.route('/actualizarProducto/<int:id>', methods=['PUT'])
def put_producto(id):
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        price = data.get('price')
        stock = data.get('stock')
        categoria_id = data.get('categoria_id')
        image_url = data.get('image_url')

        if not nombre or price is None or stock is None or not categoria_id or not image_url:
            return jsonify({'error': 'Todos los campos son obligatorios'}), 400

        connection = get_db_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
            producto = cursor.fetchone()
            if not producto:
                return jsonify({'error': 'Producto no existe'}), 404
            #actualizar el producto en la base de datos
            cursor.execute("""
                           UPDATE productos 
                           SET nombre = %s, price = %s, stock = %s, categoria_id = %s, image_url = %s 
                           WHERE id = %s
                           """, (nombre, price, stock, categoria_id, image_url, id))
            connection.commit()
            connection.close()
            return jsonify({'message': 'Producto actualizado con Exito'}), 200
    except Exception as e:
            print(f"Error al actualizar el producto: {e}")
            return jsonify({'error': 'Error al actualizar el producto'}),500
    
@producto_bp.route('/eliminarProducto/<int:id>', methods=['DELETE'])
def delete_producto(id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                           DELETE FROM productos
                           WHERE id = %s
                            """, (id,))
            if cursor.rowcount == 0:
                return jsonify({'error': 'Producto no encontrado'}), 404
            connection.commit()
            connection.close()
            return jsonify({'message': 'Producto eliminado con exito'}), 200
    except Exception as e:
        print(f"Error al eliminar el producto: {e}")
        return jsonify({'error': 'Error al eliminar el producto'}),500
        
