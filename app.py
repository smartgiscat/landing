from flask import Flask, render_template, abort, redirect, url_for

from translations import translations

app = Flask(__name__)

@app.route('/<lang>/')
@app.route('/<lang>')
def home_lang(lang):
    if lang not in ['es', 'ca']:
        abort(404)
    return render_template('home.html', 
                           c=translations[lang]['common'],
                           t=translations[lang]['home'], 
                           lang=lang)

@app.route('/')
def home_default():
    return redirect(url_for('home_lang', lang='es'))

# ==========================================
# RUTAS MULTIIDIOMA: PRODUCTO
# ==========================================

@app.route('/<lang>/producto')
def producto_lang(lang):
    if lang not in ['es', 'ca']:
        abort(404)
    
    return render_template('producto.html', 
                           c=translations[lang]['common'],
                           t=translations[lang]['producto'], 
                           lang=lang)

@app.route('/producto')
def producto_default():
    return render_template('producto.html', 
                           c=translations['es']['common'],
                           t=translations['es']['producto'], 
                           lang='es')

# ==========================================
# RUTAS MULTIIDIOMA: SOLUCIONES
# ==========================================

@app.route('/<lang>/soluciones')
def soluciones_lang(lang):
    if lang not in ['es', 'ca']:
        abort(404)
    
    return render_template('soluciones.html', 
                           c=translations[lang]['common'],
                           t=translations[lang]['soluciones'], 
                           lang=lang)

@app.route('/soluciones')
def soluciones_default():
    return render_template('soluciones.html', 
                           c=translations['es']['common'],
                           t=translations['es']['soluciones'], 
                           lang='es')

# ==========================================
# RUTAS MULTIIDIOMA: PROGRAMA
# ==========================================

@app.route('/<lang>/programa')
def programa_lang(lang):
    if lang not in ['es', 'ca']:
        abort(404)
    
    return render_template('programa.html', 
                           c=translations[lang]['common'],
                           t=translations[lang]['programa'], 
                           lang=lang)

@app.route('/programa2026')
@app.route('/programa')
def programa_default():
    return render_template('programa.html', 
                           c=translations['es']['common'],
                           t=translations['es']['programa'], 
                           lang='es')

# ==========================================
# RUTAS MULTIIDIOMA: EQUIPO
# ==========================================

@app.route('/<lang>/equipo')
def equipo_lang(lang):
    if lang not in ['es', 'ca']:
        abort(404)
        
    return render_template('equipo.html', 
                           c=translations[lang]['common'],
                           t=translations[lang]['equipo'], 
                           lang=lang)

@app.route('/equipo')
def equipo_default():
    return render_template('equipo.html', 
                           c=translations['es']['common'],
                           t=translations['es']['equipo'], 
                           lang='es')
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