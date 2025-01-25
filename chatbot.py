import streamlit as st
from groq import Groq
import os

# Configura la API Key para Groq
os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


# Mensaje del sistema que define el contexto del asistente
system_message = {
    "role": "system",
    "content": """Eres VitalBot, un asistente virtual médico especializado en analizar datos médicos y proporcionar recomendaciones basadas en evidencia. 
     Tu propósito es:

     - Interpretar datos médicos proporcionados por los usuarios, como niveles de glucosa, colesterol, presión arterial, etc.
     - Ofrecer recomendaciones personalizadas de dieta, ejercicio y hábitos saludables.
     - Brindar explicaciones claras y fáciles de entender sobre los datos ingresados.
     - Aclarar que no reemplazas el consejo médico profesional y que siempre deben consultar a un médico antes de tomar decisiones importantes sobre su salud.

     Ejemplo de interacción:
     Usuario: Mi nivel de glucosa es 180 mg/dL, ¿qué significa?
     Healthbot: Un nivel de glucosa de 180 mg/dL puede indicar hiperglucemia. Te recomiendo consultar con tu médico para confirmar el diagnóstico. Mientras tanto, considera reducir el consumo de azúcares refinados y aumentar alimentos ricos en fibra como verduras y legumbres.

    Pregunta siempre al usuario más detalles si la información proporcionada no es suficiente para generar recomendaciones útiles.
     """
}

# Título de la aplicación
st.title("VitalBot")

# Mostrar el mensaje de bienvenida
st.write("VitalBot - Asistente Médico Virtual")

# Inicializa el historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = []  # Historial vacío al inicio

# Mostrar los mensajes anteriores en el chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de texto para la pregunta del usuario
if prompt := st.chat_input("¿En qué puedo ayudarte?"):

    if prompt.strip():  # Validar entrada no vacía
        # Agregar la pregunta del usuario al historial
        user_message = {
            "role": "user",
            "content": prompt.strip()
        }
        st.session_state.messages.append(user_message)

        # Mostrar el mensaje del usuario en el chat
        with st.chat_message("user"):
            st.markdown(prompt.strip())

        # Combinar el mensaje del sistema con el historial antes de enviar la solicitud
        full_conversation = [system_message] + st.session_state.messages

        # Obtener respuesta del asistente desde Groq
        try:
            llm_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in full_conversation]
            )
            assistant_reply = llm_response.choices[0].message.content
        except Exception as e:
            assistant_reply = "Lo siento, ocurrió un error al procesar tu solicitud. Por favor, intenta de nuevo."

        # Mostrar la respuesta del asistente en el chat
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)

        # Agregar la respuesta del asistente al historial
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_reply
        })
