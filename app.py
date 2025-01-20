from flask import Flask
from rutas.categoria import categoria_bp
from rutas.producto import producto_bp

from flask_cors import CORS

#INICIALIZAR EL APLICAIO
app = Flask(__name__)
CORS(app) #HABILITAR RUTAS

app.register_blueprint(categoria_bp)
app.register_blueprint(producto_bp)


#INICIAR LA APLICACION
if __name__ == '__main__':
  app.run(debug=True)