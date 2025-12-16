import streamlit as st
import numpy as npimport streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import gaussian
import random

# -------------------------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------------------------
st.set_page_config(
    page_title="Entrenador ESS – Poligrafía",
    layout="wide"
)

st.title("🧪 Entrenador ESS – Análisis de Gráficas EDA y CARDIO")
st.markdown("""
Aplicación de **entrenamiento profesional para poligrafistas**, basada en
criterios del **Empirical Scoring System (ESS)**.
""")

# -------------------------------------------------
# FUNCIONES DE SIMULACIÓN
# -------------------------------------------------

def generar_eda(duracion=60, fs=10):
    t = np.linspace(0, duracion, duracion * fs)
    tonic = 2 + 0.05 * np.sin(0.05 * t)
    noise = np.random.normal(0, 0.03, len(t))

    onset = random.randint(15, 25) * fs
    amp = random.uniform(0.6, 1.2)
    width = random.randint(20, 40)

    phasic = np.zeros_like(t)
    kernel = gaussian(width * 2, std=width / 3)
    phasic[onset:onset + len(kernel)] = amp * kernel[:len(phasic[onset:onset + len(kernel)])]

    return t, tonic + phasic + noise


def generar_cardio(duracion=60, fs=10):
    t = np.linspace(0, duracion, duracion * fs)
    baseline = 80 + 3 * np.sin(0.1 * t)
    noise = np.random.normal(0, 1.2, len(t))

    cardio = baseline + noise
    inicio = random.randint(20, 30) * fs
    cardio[inicio:inicio + 100] += np.linspace(0, -8, 100)
    cardio[inicio + 100:inicio + 200] += np.linspace(-8, 5, 100)

    return t, cardio

# -------------------------------------------------
# EJERCICIOS ESS
# -------------------------------------------------

ejercicios = [
    {
        "tipo": "EDA",
        "pregunta": "Según criterios ESS, ¿cómo se clasifica esta reacción EDA?",
        "opciones": [
            "No reacción significativa",
            "Reacción moderada significativa",
            "Reacción compleja de alta magnitud"
        ],
        "correcta": 1,
        "explicacion": """
Se observa una **respuesta fásica clara**, con incremento rápido de amplitud,
duración adecuada y relación temporal correcta con el estímulo.
Bajo ESS corresponde a una **reacción moderada significativa**.
"""
    },
    {
        "tipo": "CARDIO",
        "pregunta": "Según ESS, ¿qué patrón cardiovascular se observa?",
        "opciones": [
            "Estabilidad fisiológica",
            "Supresión cardiovascular reactiva",
            "Artefacto de movimiento"
        ],
        "correcta": 1,
        "explicacion": """
Se evidencia una **supresión de amplitud**, cambio sostenido del patrón
y recuperación progresiva, compatible con **respuesta cardiovascular reactiva**.
"""
    }
]

# -------------------------------------------------
# CONTROL DE ESTADO
# -------------------------------------------------

if "indice" not in st.session_state:
    st.session_state.indice = 0
if "respondido" not in st.session_state:
    st.session_state.respondido = False

ej = ejercicios[st.session_state.indice]

# -------------------------------------------------
# INTERFAZ
# -------------------------------------------------

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"📈 Canal {ej['tipo']}")

    if ej["tipo"] == "EDA":
        t, signal = generar_eda()
        ylabel = "Conductancia (µS)"
    else:
        t, signal = generar_cardio()
        ylabel = "Frecuencia Cardíaca (BPM)"

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(t, signal, linewidth=1.5)
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)

    st.pyplot(fig)

with col2:
    st.subheader("📝 Evaluación ESS")
    st.markdown(f"**{ej['pregunta']}**")

    respuesta = st.radio("Seleccione una opción:", ej["opciones"], index=None)

    if st.button("Validar respuesta"):
        if respuesta is None:
            st.warning("Debe seleccionar una respuesta.")
        else:
            st.session_state.respondido = True
            seleccion = ej["opciones"].index(respuesta)

            if seleccion == ej["correcta"]:
                st.success("✅ Respuesta correcta")
            else:
                st.error("❌ Respuesta incorrecta")

            st.info(ej["explicacion"])

    if st.session_state.respondido:
        if st.button("🔄 Reintentar"):
            st.session_state.respondido = False

        if st.button("➡️ Siguiente ejercicio"):
            st.session_state.indice = (st.session_state.indice + 1) % len(ejercicios)
            st.session_state.respondido = False
            st.experimental_rerun()import matplotlib.pyplot as plt
from scipy.signal import gaussian
import random

# -----------------------------------------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------------------------------------
st.set_page_config(
    page_title="Entrenador ESS – Análisis de Gráficas Poligráficas",
    layout="wide"
)

st.title("🧪 Entrenador ESS – Análisis de Gráficas EDA y CARDIO")
st.markdown("""
Ejercicio interactivo orientado a **poligrafistas profesionales**, enfocado en el
**análisis técnico de reacciones fisiológicas** bajo criterios del **Empirical Scoring System (ESS)**.
""")

# -----------------------------------------------------------
# FUNCIONES DE SIMULACIÓN DE SEÑALES
# -----------------------------------------------------------

def generar_eda(duracion=60, fs=10, tipo="reaccion"):
    """
    Genera una señal EDA simulada con características realistas:
    - Nivel tónico
    - Respuesta fásica
    - Complejidad y ruido fisiológico
    """
    t = np.linspace(0, duracion, duracion * fs)
    tonic = 2 + 0.05 * np.sin(0.05 * t)
    noise = np.random.normal(0, 0.03, len(t))

    if tipo == "reaccion":
        onset = random.randint(15, 25) * fs
        amp = random.uniform(0.6, 1.2)
        width = random.randint(20, 40)
        phasic = np.zeros_like(t)
        kernel = gaussian(width * 2, std=width / 3)
        phasic[onset:onset + len(kernel)] = amp * kernel[:len(phasic[onset:onset + len(kernel)])]
    else:
        phasic = np.zeros_like(t)

    eda = tonic + phasic + noise
    return t, eda


def generar_cardio(duracion=60, fs=10, tipo="reaccion"):
    """
    Simula una señal CARDIO con:
    - Ritmo basal
    - Variabilidad
    - Cambios de amplitud y duración asociados a reactividad
    """
    t = np.linspace(0, duracion, duracion * fs)
    baseline = 80 + 3 * np.sin(0.1 * t)
    noise = np.random.normal(0, 1.2, len(t))

    cardio = baseline + noise

    if tipo == "reaccion":
        inicio = random.randint(20, 30) * fs
        cardio[inicio:inicio + 100] += np.linspace(0, -8, 100)
        cardio[inicio + 100:inicio + 200] += np.linspace(-8, 5, 100)

    return t, cardio


# -----------------------------------------------------------
# BANCO DE EJERCICIOS
# -----------------------------------------------------------

ejercicios = [
    {
        "tipo": "EDA",
        "pregunta": "Según criterios ESS, ¿cómo se clasifica esta reacción EDA?",
        "opciones": [
            "No reacción significativa",
            "Reacción moderada (aumento claro de amplitud)",
            "Reacción compleja con alta significancia"
        ],
        "correcta": 1,
        "explicacion": """
La gráfica muestra una **respuesta fásica clara**, con:
- Incremento rápido de amplitud (>0.5 µS)
- Duración adecuada
- Relación temporal consistente con el estímulo

Bajo ESS, esto corresponde a una **reacción moderada significativa**.
"""
    },
    {
        "tipo": "CARDIO",
        "pregunta": "Desde el enfoque ESS, ¿qué patrón CARDIO se observa?",
        "opciones": [
            "Estabilidad fisiológica",
            "Supresión cardiovascular reactiva",
            "Artefacto o interferencia"
        ],
        "correcta": 1,
        "explicacion": """
Se observa:
- Disminución clara de la amplitud
- Cambio sostenido en el patrón
- Recuperación progresiva

Esto es típico de una **supresión cardiovascular reactiva**, indicativa de activación autonómica.
"""
    }
]

# -----------------------------------------------------------
# CONTROL DE ESTADO
# -----------------------------------------------------------

if "indice" not in st.session_state:
    st.session_state.indice = 0
if "respondido" not in st.session_state:
    st.session_state.respondido = False

ejercicio = ejercicios[st.session_state.indice]

# -----------------------------------------------------------
# GENERACIÓN Y VISUALIZACIÓN
# -----------------------------------------------------------

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"📈 Gráfica {ejercicio['tipo']}")

    if ejercicio["tipo"] == "EDA":
        t, signal = generar_eda(tipo="reaccion")
        ylabel = "Conductancia (µS)"
    else:
        t, signal = generar_cardio(tipo="reaccion")
        ylabel = "Frecuencia Cardíaca (BPM)"

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(t, signal, linewidth=1.5)
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel(ylabel)
    ax.set_title(f"Simulación {ejercicio['tipo']} – Respuesta fisiológica")
    ax.grid(alpha=0.3)

    st.pyplot(fig)

# -----------------------------------------------------------
# INTERACCIÓN TIPO TEST
# -----------------------------------------------------------

with col2:
    st.subheader("📝 Análisis ESS")
    st.markdown(f"**{ejercicio['pregunta']}**")

    respuesta = st.radio(
        "Seleccione la opción correcta:",
        ejercicio["opciones"],
        index=None
    )

    if st.button("Validar respuesta"):
        if respuesta is not None:
            st.session_state.respondido = True
            seleccion = ejercicio["opciones"].index(respuesta)

            if seleccion == ejercicio["correcta"]:
                st.success("✅ Respuesta correcta")
            else:
                st.error("❌ Respuesta incorrecta")

            st.markdown("### 📚 Retroalimentación técnica")
            st.info(ejercicio["explicacion"])
        else:
            st.warning("Seleccione una respuesta antes de validar.")

    if st.session_state.respondido:
        if st.button("🔄 Reintentar"):
            st.session_state.respondido = False

        if st.button("➡️ Siguiente ejercicio"):
            st.session_state.indice = (st.session_state.indice + 1) % len(ejercicios)
            st.session_state.respondido = False
            st.experimental_rerun()
