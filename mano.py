import cv2
import mediapipe as mp
import time

# Inicializar MediaPipe UNA sola vez
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils


# 🔥 FUNCIÓN que usa Flask
def procesar_imagen(ruta_imagen):
    global hands

    frame = cv2.imread(ruta_imagen)

    if frame is None:
        return "Error: Image not found"

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = hands.process(rgb)

    letra = ""
    palabra = ""

    if resultado.multi_hand_landmarks:
        for mano in resultado.multi_hand_landmarks:

            dedos = []

            if mano.landmark[8].y < mano.landmark[6].y:
                dedos.append(1)
            else:
                dedos.append(0)

            if mano.landmark[12].y < mano.landmark[10].y:
                dedos.append(1)
            else:
                dedos.append(0)

            if mano.landmark[16].y < mano.landmark[14].y:
                dedos.append(1)
            else:
                dedos.append(0)

            if mano.landmark[20].y < mano.landmark[18].y:
                dedos.append(1)
            else:
                dedos.append(0)

            num = sum(dedos)

            if num == 0:
                letra = "A"
            elif num == 1:
                letra = "B"
            elif num == 2:
                letra = "C"
            elif num == 3:
                letra = "D"
            elif num == 4:
                letra = "E"

    # 🔥 devolver resultado al HTML
    return f"Letter: {letra}"


# 🚫 ESTO SOLO corre si ejecutas mano.py directo
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    letra = ""
    palabra = ""
    ultimo_tiempo = time.time()

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado = hands.process(rgb)

        if resultado.multi_hand_landmarks:
            for mano in resultado.multi_hand_landmarks:

                mp_drawing.draw_landmarks(
                    frame,
                    mano,
                    mp_hands.HAND_CONNECTIONS
                )

                dedos = []

                if mano.landmark[8].y < mano.landmark[6].y:
                    dedos.append(1)
                else:
                    dedos.append(0)

                if mano.landmark[12].y < mano.landmark[10].y:
                    dedos.append(1)
                else:
                    dedos.append(0)

                if mano.landmark[16].y < mano.landmark[14].y:
                    dedos.append(1)
                else:
                    dedos.append(0)

                if mano.landmark[20].y < mano.landmark[18].y:
                    dedos.append(1)
                else:
                    dedos.append(0)

                num = sum(dedos)

                if num == 0:
                    letra = "A"
                elif num == 1:
                    letra = "B"
                elif num == 2:
                    letra = "C"
                elif num == 3:
                    letra = "D"
                elif num == 4:
                    letra = "E"

        tiempo_actual = time.time()

        if letra != "" and tiempo_actual - ultimo_tiempo > 2:
            palabra += letra
            ultimo_tiempo = tiempo_actual

        cv2.putText(frame, "Letter: " + letra, (30,70),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3)

        cv2.putText(frame, "Word: " + palabra, (30,150),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 3)

        cv2.imshow("Sign Translator", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    