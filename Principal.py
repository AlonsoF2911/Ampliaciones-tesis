import streamlit as st
import base64  # Necesario para manejar archivos en binario si se requiere

# Configuración formal de la página
st.set_page_config(
    page_title="Validador Normativo de Ampliaciones",
    page_icon="🏗️",
    layout="wide"
)

# ==========================================
# ESTILOS VISUALES PERSONALIZADOS (CSS)
# ==========================================
st.markdown("""
<style>
    /* CAMBIO DE FONDO: Le da un tono gris/verde muy suave a toda la app */
    [data-testid="stAppViewContainer"] {
        background-color: #F0F4F2; 
    }
    
    /* Franja superior verde con texto blanco */
    .franja-verde {
        background-color: #1E7B44;
        color: white;
        padding: 25px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Cajas blancas para los textos y definiciones */
    .caja-blanca {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }

    /* Estilo para justificar textos y achicar la letra del propósito */
    .texto-justificado-chico {
        text-align: justify;
        font-size: 14px;
        background-color: white; 
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #1E7B44; 
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
    }
    
    .texto-justificado {
        text-align: justify;
        font-size: 16px;
        margin-bottom: 10px;
        color: #333333;
    }
    
    /* Diferenciación de letras para los Títulos de las leyes */
    .titulo-ley {
        color: #1E7B44;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    
    /* Estilo para los links */
    .link-documento {
        font-size: 14px;
        font-style: italic;
        margin-top: 10px;
    }
    .link-documento a {
        color: #2980B9;
        text-decoration: none;
    }
    .link-documento a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# BARRA LATERAL (SIDEBAR) - MENÚ DE NAVEGACIÓN
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ Panel de Navegación")
    
    menu_seleccionado = st.radio(
        "Seleccione un módulo:",
        ("🏠 Inicio", "🏡 Datos del Terreno")
    )
    
    st.markdown("---")
    st.info("Utilice este menú para navegar por las distintas etapas de la validación normativa.")

# ==========================================
# LÓGICA DE CAMBIO DE PANTALLAS
# ==========================================

# ------------------------------------------
# PANTALLA 1: INICIO
# ------------------------------------------
if menu_seleccionado == "🏠 Inicio":
