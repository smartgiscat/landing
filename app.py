import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_mail import Mail
from dotenv import load_dotenv

from translations import translations
from inscripcions import send_inscription_emails

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Flask-Mail lee la configuración mapeada directamente desde el .env
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 465))
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Inicializamos Mail con la app
mail = Mail(app)

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
# RUTAS MULTIIDIOMA: CASOS DE USO
# ==========================================

@app.route('/<lang>/casos-uso')
def casos_uso_lang(lang):
    if lang not in ['es', 'ca']:
        abort(404)
    
    return render_template('casos_uso.html', 
                           c=translations[lang]['common'],
                           t=translations[lang]['casos_uso'], 
                           lang=lang)

@app.route('/casos-uso')
def casos_uso_default():
    return render_template('casos_uso.html', 
                           c=translations['es']['common'],
                           t=translations['es']['casos_uso'], 
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

# ==========================================
# RUTAS LEGALES
# ==========================================

@app.route('/cookies')
def cookies():
    return render_template('cookies.html')

@app.route('/privacidad')
def privacidad():
    return render_template('privacidad.html')

@app.route('/aviso-legal')
def aviso_legal():
    return render_template('aviso-legal.html')

# ==========================================
# RUTA DEL FORMULARIO
# ==========================================

@app.route('/inscribir', methods=['POST'])
def inscribir():
    # Detectar el idioma actual para los mensajes Flash
    lang = request.referrer.split('/')[-2] if request.referrer else 'es'
    if lang not in ['es', 'ca']: lang = 'es'
    
    # SOLUCIÓN 1: Llamamos directamente al diccionario de traducciones
    texts = translations.get(lang, translations['es'])
    
    # Recoger datos del formulario
    form_data = {
        'city': request.form.get('city'),
        'name': request.form.get('name'),
        'position': request.form.get('position'),
        'email': request.form.get('email'),
        'phone': request.form.get('phone'),
        'observations': request.form.get('observations', '')
    }
    
    # Validación básica backend
    if not all([form_data['city'], form_data['name'], form_data['email'], form_data['position'], form_data['phone']]):
        flash("Por favor, rellena todos los campos obligatorios." if lang == 'es' else "Si us plau, omple tots els camps obligatoris.")
        return redirect(request.referrer)

    # Procesar el envío
    success = send_inscription_emails(mail, form_data, texts['programa'])
    
    # Feedback al usuario
    if success:
        if lang == 'es':
            flash("¡Candidatura enviada con éxito! Revisa tu correo electrónico para ver la confirmación.")
        else:
            flash("Candidatura enviada amb èxit! Revisa el teu correu electrònic per veure la confirmació.")
    else:
        if lang == 'es':
            flash("Ha habido un error al enviar tu solicitud. Por favor, inténtalo más tarde o contáctanos directamente.")
        else:
            flash("Hi ha hagut un error en enviar la teva sol·licitud. Si us plau, intenta-ho més tard o contacta amb nosaltres.")
            
    # SOLUCIÓN 2: Redirigir usando 'programa_lang' en lugar de 'programa_view'
    return redirect(url_for('programa_lang', lang=lang) + "#inscripcio-form")

# Pon esto temporalmente para ver qué lee realmente Flask
@app.route('/debug-mail')
def debug_mail():
    return {
        "SERVER": app.config.get('MAIL_SERVER'),
        "PORT": app.config.get('MAIL_PORT'),
        "TLS": app.config.get('MAIL_USE_TLS'),
        "SSL": app.config.get('MAIL_USE_SSL'),
        "USER": app.config.get('MAIL_USERNAME'),
        # Mostramos solo el principio de la password para ver si hay espacios raros
        "PASS_START": str(app.config.get('MAIL_PASSWORD'))[:2] if app.config.get('MAIL_PASSWORD') else None
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)