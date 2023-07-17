from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    user='root',
    password='estibaliZ1.',
    database='fullstack_bottega'
)

@app.route('/items', methods=['GET'])
def get_items():
    # Consulta SQL para obtener todos los registros de la tabla
    query = 'SELECT * FROM items'

    # Ejecutar la consulta
    cursor = db.cursor()
    cursor.execute(query)

    # Obtener los resultados y construir la lista de elementos
    items = []
    for item in cursor.fetchall():
        item_data = {
            'id': item[0],
            'name': item[1]
        }
        items.append(item_data)

    return jsonify(items)

@app.route('/items', methods=['POST'])
def add_item():
    item = request.json.get('name')
    if item:
        # Consulta SQL para insertar un nuevo registro en la tabla
        query = 'INSERT INTO items (name) VALUES (%s)'

        # Datos del nuevo elemento
        item_data = (item,)

        # Ejecutar la consulta
        cursor = db.cursor()
        cursor.execute(query, item_data)
        db.commit()

        return jsonify({'message': 'Item added successfully'})
    else:
        return jsonify({'error': 'Invalid item'})

@app.route('/items/<int:index>', methods=['DELETE', 'PUT'])
def edit_or_delete_item(index):
    if request.method == 'DELETE':
        # Consulta SQL para eliminar un registro de la tabla
        query = 'DELETE FROM items WHERE id = %s'

        # Datos del índice del elemento a eliminar
        item_index = (index,)

        # Ejecutar la consulta
        cursor = db.cursor()
        cursor.execute(query, item_index)
        db.commit()

        return jsonify({'message': 'Item deleted successfully'})
    elif request.method == 'PUT':
        new_name = request.json.get('name')
        if new_name:
            # Consulta SQL para actualizar un registro de la tabla
            query = 'UPDATE items SET name = %s WHERE id = %s'

            # Datos del nuevo nombre y el índice del elemento a editar
            item_data = (new_name, index)

            # Ejecutar la consulta
            cursor = db.cursor()
            cursor.execute(query, item_data)
            db.commit()

            return jsonify({'message': 'Item edited successfully'})
        else:
            return jsonify({'error': 'Invalid item'})

if __name__ == '__main__':
    app.run()
