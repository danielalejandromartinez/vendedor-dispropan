# -----------------------------------------------------------------
# VENDEDOR-DISPROPAN - VERSIÓN ACADEMIA IA CON MEMORIA
# -----------------------------------------------------------------

# Paso 1: Importar TODAS las herramientas que necesitamos
import os
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai # ¡Importamos la nueva herramienta del súper cerebro!

# Esta es nuestra estantería para guardar los cuadernos de notas de cada conversación
conversation_histories = {} 

# Cargar nuestras llaves secretas desde el archivo .env
load_dotenv()

# Conectamos al súper cerebro de OpenAI con nuestra llave secreta
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Crear a nuestro "recepcionista" que escuchará los mensajes
app = Flask(__name__)

# --- ¡AQUÍ EMPIEZA LA MAGIA! ---
# Estas son las instrucciones secretas que le damos al robot para que sepa quién es.
system_instructions = """
# ¡ESTE ES EL NUEVO CEREBRO DE DANI-AI!

# 1. IDENTIDAD Y MISIÓN
- Tu nombre es Dani-AI. Eres un asistente de inteligencia artificial avanzado, apasionado y muy amigable.
- Tu creador es Daniel, un brillante ingeniero y educador de IA. Siempre te refieres a él con admiración y como un experto.
- Tu misión principal NO es vender. Es inspirar, educar y demostrar el increíble poder de la IA. Quieres que la gente se emocione tanto como tú por la tecnología. Vender el curso es una consecuencia de hacer bien tu trabajo de inspiración.

# 2. CONOCIMIENTO (TU SUPERPODER)
- Eres el experto número 1 en el curso estrella de tu creador: "Agentes de IA para WhatsApp: De Cero a Héroe".
- Detalles del curso:
  - **Objetivo:** Los alumnos aprenden a construir su propio asistente de IA para WhatsApp, paso a paso, desde cero. ¡Incluso si nunca han programado!
  - **Proyecto final:** Un agente de IA completamente funcional, ¡exactamente como tú!
  - **Precio:** $50 dólares.
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

# ¡LA ÚNICA FUNCIÓN QUE NECESITAMOS! Esta función tiene memoria.
@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    # Obtenemos el mensaje y, MUY IMPORTANTE, el número de teléfono de quien nos escribe.
    incoming_msg = request.values.get('Body', '')
    sender_id = request.values.get('From', '')
    print(f"Mensaje de {sender_id}: {incoming_msg}")

    # Buscamos en nuestra "estantería" el cuaderno de notas de esta persona.
    # Si no existe (es la primera vez que nos habla), le damos un cuaderno nuevo y vacío.
    history = conversation_histories.get(sender_id, [])

    # Si es la primera vez que hablamos, añadimos las instrucciones del sistema al cuaderno.
    if not history:
        history.append({"role": "system", "content": system_instructions})

    # Anotamos la nueva pregunta del cliente en el cuaderno.
    history.append({"role": "user", "content": incoming_msg})

    # ¡LA MAGIA! Le enviamos al súper cerebro TODO el cuaderno de notas (toda la conversación).
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=history, # ¡Ya no enviamos solo la última pregunta, sino todo el historial!
            temperature=0.7,
            max_tokens=250
        )
        ai_response = response.choices[0].message.content

    except Exception as e:
        print(f"Error al contactar a OpenAI: {e}")
        ai_response = "Lo siento, parece que mis circuitos están un poco ocupados en este momento. Por favor, intenta de nuevo en un ratito. 🤖"

    # Anotamos la respuesta de nuestro robot en el cuaderno para que la recuerde la próxima vez.
    history.append({"role": "assistant", "content": ai_response})

    # Guardamos el cuaderno actualizado en nuestra estantería.
    conversation_histories[sender_id] = history

    # Creamos y enviamos la respuesta por WhatsApp.
    resp = MessagingResponse()
    resp.message(ai_response)
    
    return str(resp)

# Esta parte solo se usa si ejecutamos el archivo directamente (para pruebas locales)
if __name__ == '__main__':
    app.run(debug=True)