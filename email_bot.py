import smtplib
import ssl
from email.message import EmailMessage

# --- CONFIGURACIÓN (CONSTANTES) ---
# Lo ideal es que estas dos no cambien
EMAIL_EMISOR = "emisor@correo.com"
PASSWORD = "tu_contraseña_aqui" 

def enviar_correo(destinatario, asunto, cuerpo):
    """
    Envía un correo electrónico de forma segura.
    """
    # 1. Crear el objeto Mensaje
    em = EmailMessage()
    em['From'] = EMAIL_EMISOR
    em['To'] = destinatario
    em['Subject'] = asunto
    em.set_content(cuerpo)

    # 2. Configurar seguridad
    contexto = ssl.create_default_context()

    # 3. Intentar conectar y enviar
    try:
        print(f"conectando con Gmail para enviar a {destinatario}...")
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:
            smtp.login(EMAIL_EMISOR, PASSWORD)
            smtp.sendmail(EMAIL_EMISOR, destinatario, em.as_string())
            
        print("✅ ¡Correo enviado con éxito!")
        return True # Devuelve True si salió bien
        
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")
        return False # Devuelve False si falló

# --- MAIN (PRUEBA) ---
if __name__ == "__main__":
    # Ahora puedes enviar correos así de fácil:
    enviar_correo(
        "example@correo.com", 
        "Alerta de Seguridad", 
        "Se ha detectado un inicio de sesión en tu servidor."
    )
    
    # Podrías meter esto en un bucle para enviar a una lista de personas