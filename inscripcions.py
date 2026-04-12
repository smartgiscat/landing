import os
from flask_mail import Message

def send_inscription_emails(mail, data, texts):
    """
    Gestiona el envío de correos de confirmación y notificación para el piloto.
    
    :param mail: Instancia de Flask-Mail
    :param data: Diccionario con los datos del formulario (city, name, position, email, phone, observations)
    :param texts: Diccionario con los textos traducidos (opcional, para personalizar emails según idioma)
    :return: Boolean (True si éxito, False si error)
    """
    # El remitente será el correo configurado en tu .env
    sender = os.getenv('MAIL_USERNAME')
    
    if not sender:
        print("ERROR: MAIL_USERNAME no está definido en las variables de entorno.")
        return False

    try:
        # ==========================================
        # 1. CORREO PARA EL EQUIPO (Administración)
        # ==========================================
        admin_subject = f"🚨 Nova Inscripció Pilot 2026: {data.get('city', 'Desconeguda')}"
        
        admin_body = f"""
        S'ha rebut una nova sol·licitud oficial per al Programa Pilot 2026:
        
        - AJUNTAMENT: {data.get('city')}
        - PERSONA DE CONTACTE: {data.get('name')}
        - CÀRREC: {data.get('position')}
        - CORREU: {data.get('email')}
        - TELÈFON: {data.get('phone')}
        
        OBSERVACIONS:
        {data.get('observations', 'Sense observacions')}
        """
        
        admin_msg = Message(
            subject=admin_subject,
            sender=sender,
            recipients=[sender], # Te lo envías a ti mismo o al correo de info/ventas
            body=admin_body
        )

        # ==========================================
        # 2. CORREO PARA EL USUARIO (Confirmación)
        # ==========================================
        user_subject = "Confirmació de candidatura - SmartGIS GovTech 2026"
        
        # Usamos HTML para que el correo se vea más profesional e institucional
        user_html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #333;">
            <div style="background-color: #0d3b8a; padding: 20px; border-radius: 10px 10px 0 0;">
                <h2 style="color: white; margin: 0;">SmartGIS | Innovació sobre el territori</h2>
            </div>
            
            <div style="padding: 30px; border: 1px solid #eee; border-top: none; border-radius: 0 0 10px 10px;">
                <p>Hola <strong>{data.get('name')}</strong>,</p>
                
                <p>Hem rebut correctament la candidatura de l'<strong>Ajuntament de {data.get('city')}</strong> per formar part del Programa d'Innovació Territorial 2026.</p>
                
                <p>Aquestes són les dades que hem registrat:</p>
                <ul>
                    <li><strong>Càrrec:</strong> {data.get('position')}</li>
                    <li><strong>Telèfon:</strong> {data.get('phone')}</li>
                </ul>
                
                <p>En els propers dies, el nostre equip tècnic avaluarà la informació i es posarà en contacte amb vostè per concertar una breu reunió de valoració inicial i analitzar la viabilitat del seu cas d'ús.</p>
                
                <br>
                <p>Gràcies per confiar en la tecnologia de SmartGIS.</p>
                <p>Cordialment,<br><strong>L'equip de SmartGIS</strong></p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin-top: 30px;">
                <p style="font-size: 11px; color: #999; text-align: center;">
                    Aquest és un missatge automàtic, si us plau no respongui directament a aquest correu. Si té algun dubte, contacti amb info@smartgis.es.
                </p>
            </div>
        </div>
        """
        
        user_msg = Message(
            subject=user_subject,
            sender=sender,
            recipients=[data.get('email')],
            html=user_html # Enviamos la versión HTML
        )

        # Enviar ambos correos
        mail.send(admin_msg)
        mail.send(user_msg)
        
        return True

    except Exception as e:
        print(f"Error crític enviant correus: {str(e)}")
        # Aquí podrías registrar el error en un log si lo tuvieras implementado
        return False