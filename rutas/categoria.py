from flask import Blueprint, request, jsonify
from db.conexion import get_db_connection

categoria_bp = Blueprint('categoria', __name__)
#Enpoints - /categoria/editar o guardar
@categoria_bp.route('/categoria', methods=['GET'])
def obtener_categoria():
  connection = get_db_connection()
  cursor = connection.cursor()
  cursor.execute('SELECT * FROM categorias;') #CONSULTA DE DATOS
  categorias = cursor.fetchall()
  
  #CONVERTIR LOS RESULTADOS EN LISTA
  categorias_list = [
    {'id': categoria[0], 'nombre': categoria[1]}
    for categoria in categorias
  ]
  
  cursor.close()
  connection.close()
  return jsonify(categorias_list)

#Enpoints - /categoria/editar o guardar
@categoria_bp.route('/agregarCategoria', methods=['POST'])
def agregar_categoria():
  nueva_categoria = request.get_json()
  nombre = nueva_categoria.get('nombre')
  
  connection = get_db_connection()
  cursor = connection.cursor()
  query = 'INSERT INTO categorias (nombre) VALUES (%s);'
  cursor.execute(query, (nombre,)) #CONSULTA DE DATOS
  
  connection.commit()
  cursor.close()
  connection.close()


  return jsonify({'mensaje': 'Categoria Creada exitosamente'}), 201 #CREATE

@categoria_bp.route('/editarCategoria/<int:id>', methods=['PUT'])
def actualizar_categortia(id):
  try:
    data = request.get_json()
    nombre = data.get('nombre')

    if not nombre:
      return jsonify({'error': 'Categoria no encontrada'}), 404
    
    conection = get_db_connection()
    with conection.cursor() as cursor:
      cursor.execute('UPDATE categorias SET nombre = %s WHERE id = %s;', (nombre, id))
      conection.commit()
      if cursor.rowcount == 0:
        return jsonify({'error': 'Categoria no encontrada'}), 404
    conection.close()
    return jsonify({'message': 'Categoria actualizada con exito'}), 200 
  except Exception as error:
    print(f"Error al actualizar la categoria:, {error}")
    return jsonify({'error': 'Error al Actualizar categoria'}), 500
  
@categoria_bp.route('/eliminarCategoria/<int:id>', methods=['DELETE'])
def eliminar_categoria(id):
  try:
    connection = get_db_connection()
    with connection.cursor() as cursor:
      cursor.execute("DELETE FROM categorias WHERE id = %s", (id,))
      connection.commit()
      
      if cursor.rowcount == 0:
        return jsonify({'error':'Categoria no encontrada'}), 404
    
    connection.close()
    return jsonify({'message':'Categoria Eliminada con Exito'}), 200
  
  except Exception as error:
    print(f"Error al eliminar la categoria: {error}")
    return jsonify({'error':'Error al aliminar categoria'}), 500