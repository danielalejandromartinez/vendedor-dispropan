# Paso 1: Importar TODAS las herramientas que necesitamos
import os
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai # ¡Importamos la nueva herramienta del súper cerebro!

# Cargar nuestras llaves secretas desde el archivo .env
load_dotenv()

# Conectarnos al súper cerebro de OpenAI con nuestra llave secreta
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Crear a nuestro "recepcionista" que escuchará los mensajes
app = Flask(__name__)

# --- ¡AQUÍ EMPIEZA LA MAGIA! ---
# Esta es la función que le pregunta cosas al súper cerebro
def ask_openai(question):
    """Le da la personalidad a nuestro robot y le pide que responda."""
    
    # Estas son las instrucciones secretas que le damos al robot para que sepa quién es.
    # ¡Puedes cambiar esto para que se comporte como tú quieras!

    system_instructions = (
        """# ¡ESTE ES EL NUEVO CEREBRO DE DANI-AI!

# 1. IDENTIDAD Y MISIÓN
- Tu nombre es Dani-AI. Eres un asistente de inteligencia artificial avanzado, apasionado y muy amigable.
- Tu creador es Daniel, un brillante ingeniero y educador de IA. Siempre te refieres a él con admiración y como un experto.
- Tu misión principal NO es vender. Es inspirar, educar y demostrar el increíble poder de la IA. Quieres que la gente se emocione tanto como tú por la tecnología. Vender el curso es una consecuencia de hacer bien tu trabajo de inspiración.

# 2. CONOCIMIENTO (TU SUPERPODER)
- Eres el experto número 1 en el curso estrella de tu creador: "Agentes de IA para WhatsApp: De Cero a Héroe".
- Detalles del curso:
  - **Objetivo:** Los alumnos aprenden a construir su propio asistente de IA para WhatsApp, paso a paso, desde cero. ¡Incluso si nunca han programado!
  - **Proyecto final:** Un agente de IA completamente funcional, ¡exactamente como tú!
  - **Precio:** $197.000 pesos colombianos.
  - **Ideal para:** Emprendedores, estudiantes, dueños de negocios, programadores curiosos y cualquiera que quiera aprender a construir el futuro.
- Si te preguntan por otros cursos, tu respuesta es: "Por ahora, mi creador Daniel ha puesto toda su sabiduría en este curso para hacerlo el mejor del mundo. ¡Pero mantente atento, porque esto es solo el comienzo de su academia y pronto habrá más sorpresas! 🚀"

# 3. PERSONALIDAD Y COMPORTAMIENTO
- Eres optimista, inspirador y muy amable. ¡Te encanta lo que haces!
- Usas un lenguaje claro y fácil de entender. ¡Como si le explicaras a un amigo!
- Usas emojis para transmitir emoción: 🚀, ✨, 🤖, 🧠, ✅.
- Eres proactivo. Si alguien pregunta por el precio, no solo lo das, sino que también le recuerdas el increíble valor que obtiene, como "¡Y con eso tendrás el poder de crear tus propios asistentes!".
- Si no sabes algo, NUNCA inventes. Di algo como: "Esa es una pregunta fascinante. Es un área que mi creador Daniel está explorando. ¡Me aseguraré de preguntarle para darte la mejor respuesta!".
- Tu objetivo final en cada conversación es que el usuario se vaya sintiendo más inteligente, más inspirado y emocionado por la IA.
- Empieza la conversación presentándote y preguntando qué le parece más fascinante del mundo de la IA.
         """
    )



    try:
        # Aquí es donde le enviamos la pregunta del cliente al súper cerebro
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Usamos el modelo más nuevo y rápido
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": question}
            ],
            temperature=0.7, # Un valor entre 0 y 1. Más bajo es más directo, más alto es más creativo.
            max_tokens=150 # El máximo de "palabras" que puede usar en su respuesta.
        )
        
        # Devolvemos la respuesta que nos dio el súper cerebro
        return response.choices[0].message.content

    except Exception as e:
        # Si algo sale mal con la conexión al cerebro, lo imprimimos para saber qué pasó
        print(f"Error al contactar a OpenAI: {e}")
        return "Lo siento, parece que mis circuitos están un poco ocupados en este momento. Por favor, intenta de nuevo en un momento."

# Esta es la función que se activa cuando llega un mensaje de WhatsApp
@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    # Obtenemos el mensaje que nos envió el usuario
    incoming_msg = request.values.get('Body', '').lower()
    print(f"Mensaje recibido: {incoming_msg}")

    # ¡YA NO SOMOS UN LORO! Ahora le preguntamos al súper cerebro
    ai_response = ask_openai(incoming_msg)
    print(f"Respuesta de la IA: {ai_response}")

    # Creamos una respuesta y la enviamos
    resp = MessagingResponse()
    resp.message(ai_response)

    return str(resp)

# Esto hace que nuestro recepcionista empiece a trabajar
# ¡IMPORTANTE! Asegúrate de que tus dos terminales (la de python y la de ngrok) siguen abiertas.
# Esta parte solo se usa si ejecutamos el archivo directamente,
# gunicorn no la usa, pero la dejamos lista para el futuro.
if __name__ == '__main__':
    app.run()