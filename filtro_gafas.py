import cv2
import numpy as np

# 1. CARGAMOS EL CASCADA DE CARA
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 2. CARGAMOS LA IMAGEN DE LAS GAFAS (Con canal Alpha/Transparencia)
# El parámetro -1 (o cv2.IMREAD_UNCHANGED) es VITAL para leer la transparencia
img_gafas = cv2.imread('gafas.png', -1)

if img_gafas is None:
    print("❌ Error: No encuentro 'gafas.png'. Asegúrate de descargar una y ponerla en la carpeta.")
    exit()

# --- FUNCIÓN MAESTRA: SUPERPOSICIÓN CON TRANSPARENCIA ---
def superponer_transparencia(fondo, img_overlay, x, y, w_obj, h_obj):
    try:
        # A. Redimensionar el objeto (las gafas) al tamaño deseado
        img_overlay_resized = cv2.resize(img_overlay, (w_obj, h_obj))

        # B. Separar canales: Color (BGR) y Máscara (Alpha)
        # alpha_s es la transparencia de las gafas (0 a 1)
        alpha_s = img_overlay_resized[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s # Inverso (lo que se ve del fondo)

        # C. Recortar la región del fondo donde van las gafas
        # (y1, y2, x1, x2) son las coordenadas en el video
        y1, y2 = y, y + h_obj
        x1, x2 = x, x + w_obj

        # Verificación de seguridad: Si las gafas se salen de la pantalla, no dibujar
        if y1 < 0 or y2 > fondo.shape[0] or x1 < 0 or x2 > fondo.shape[1]:
            return fondo

        # D. La Mezcla Mágica (Pixel a Pixel para los 3 canales de color)
        for c in range(0, 3):
            # Color Final = (Gafas * Alpha) + (Fondo * (1-Alpha))
            fondo[y1:y2, x1:x2, c] = (alpha_s * img_overlay_resized[:, :, c] +
                                      alpha_l * fondo[y1:y2, x1:x2, c])
        return fondo

    except Exception as e:
        print(f"Error al superponer: {e}")
        return fondo

# 3. INICIAR CÁMARA
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

while True:
    ret, frame = cap.read()
    if not ret: break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # --- LÓGICA DE POSICIONAMIENTO ---
        # No detectamos ojos para ir más rápido. Usamos geometría:
        # Las gafas suelen ocupar el ancho de la cara y estar al 35% de la altura.
        
        ancho_gafas = w # Mismo ancho que la cara
        alto_gafas = int(ancho_gafas * img_gafas.shape[0] / img_gafas.shape[1]) # Mantener proporción original
        
        # Ajuste fino de posición (Juega con estos números)
        x_gafas = x
        y_gafas = y + int(h * 0.25) # Bajamos un 25% desde la frente

        # Llamamos a la función mágica
        frame = superponer_transparencia(frame, img_gafas, x_gafas, y_gafas, ancho_gafas, alto_gafas)

        # (Opcional) Dibujar caja para depurar
        # cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 1)

    cv2.imshow('Filtro Gafas AR', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()