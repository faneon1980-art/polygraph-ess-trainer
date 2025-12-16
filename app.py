import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy.signal.windows import gaussian

st.set_page_config(page_title="Entrenador ESS – Poligrafía", layout="centered")

st.title("🧠 Entrenamiento ESS – Análisis de Gráficas Poligráficas")

# -----------------------------
# Estado
# -----------------------------
if "ejercicio_actual" not in st.session_state:
    st.session_state.ejercicio_actual = 1

# -----------------------------
# Simulación EDA
# -----------------------------
def simular_eda():
    t = np.linspace(0, 30, 600)
    base = 1 + 0.05 * np.random.randn(len(t))
    respuesta = gaussian(len(t), std=40)
    respuesta = respuesta / np.max(respuesta) * 0.8
    return t, base + respuesta

# -----------------------------
# Gráfica
# -----------------------------
t, eda = simular_eda()

fig, ax = plt.subplots()
ax.plot(t, eda, linewidth=2)
ax.set_title("EDA – Respuesta electrodérmica")
ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Amplitud")
st.pyplot(fig)

# -----------------------------
# Pregunta ESS
# -----------------------------
st.subheader("Pregunta ESS")

respuesta = st.radio(
    "Según el sistema ESS, esta reacción EDA se considera:",
    [
        "Sin reacción significativa",
        "Reacción leve (SR)",
        "Reacción significativa (R)",
        "Artefacto"
    ],
    key="opcion_respuesta"
)

# -----------------------------
# Validación (SIN ERRORES)
# -----------------------------
if st.button(
    "Validar respuesta",
    key=f"validar_{st.session_state.ejercicio_actual}"
):
    if respuesta == "Reacción significativa (R)":
        st.success(
            "Correcto. La amplitud y duración superan los criterios mínimos ESS."
        )
    else:
        st.error(
            "Incorrecto. La reacción presenta amplitud, duración y forma compatibles con R según ESS."
        )

    st.session_state.ejercicio_actual += 1
