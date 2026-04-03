from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/producto')
def producto():
    return render_template('producto.html')

@app.route('/soluciones')
def soluciones():
    return render_template('soluciones.html')

@app.route('/programa2026')
def programa():
    return render_template('programa.html')

@app.route('/equipo')
def equipo():
    return render_template('equipo.html')

@app.route('/cookies')
def cookies():
    return render_template('cookies.html')

@app.route('/privacidad')
def privacidad():
    return render_template('privacidad.html')

@app.route('/aviso-legal')
def aviso_legal():
    return render_template('aviso-legal.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)