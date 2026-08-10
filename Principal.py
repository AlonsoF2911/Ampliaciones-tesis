import streamlit as st

# Configuración básica de la página
st.set_page_config(
    page_title="Software Tesis - Validación Normativa",
    page_icon="🏗️"
)

st.title("Prototipo de Software de Tesis")
st.markdown("Herramienta de validación normativa para proyectos de ampliación.")

# Menú simple de navegación
opcion = st.sidebar.selectbox(
    "Seleccione una opción",
    ["Inicio", "Módulo de Validación"]
)

if opcion == "Inicio":
    st.subheader("Bienvenido")
    st.write("Este software tiene como objetivo verificar parámetros normativos para ampliaciones domiciliarias.")

elif opcion == "Módulo de Validación":
    st.subheader("Módulo Base de Validación")
    
    # Entrada numérica simple
    superficie = st.number_input("Ingrese la superficie a evaluar (m²):", min_value=0.0, value=0.0)
    
    if st.button("Evaluar"):
        st.info(f"Superficie ingresada para análisis: {superficie} m²")