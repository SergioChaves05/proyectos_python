import cv2

# 1. CARGAR EL "CEREBRO" (El modelo pre-entrenado)
# OpenCV ya trae este archivo xml instalado
ruta_modelo = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(ruta_modelo)

# 2. INICIAR LA CÁMARA (Usa el índice que te funcionó: 0, 1 o 2)
# Mantén el backend V4L2 si estás en Linux
cap = cv2.VideoCapture(0, cv2.CAP_V4L2) 

print("✅ Detector iniciado. Pulsa 'q' para salir.")

while True:
    # A. Leer fotograma
    ret, frame = cap.read()
    if not ret: break

    # B. Convertir a Escala de Grises
    # La IA funciona mejor y más rápido en blanco y negro
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # C. DETECTAR ROSTROS (La Magia)
    # scaleFactor=1.1: Reduce la imagen un 10% en cada pasada para buscar caras grandes y pequeñas
    # minNeighbors=5: Cuántos "rectángulos candidatos" debe tener cerca para confirmar que es una cara (menos = más falsos positivos)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # D. DIBUJAR LOS RECTÁNGULOS
    # La función nos devuelve una lista de coordenadas (x, y, ancho, alto)
    for (x, y, w, h) in faces:
        # Dibujamos un rectángulo VERDE (0, 255, 0) de grosor 2
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Opcional: Poner texto "Rostro"
        cv2.putText(frame, "Rostro", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # E. Mostrar el resultado
    cv2.imshow('Detector Facial IA', frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Limpieza
cap.release()
cv2.destroyAllWindows()