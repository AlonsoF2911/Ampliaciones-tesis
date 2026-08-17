import streamlit as st

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
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1); /* Sombra para darle profundidad */
    }
    
    /* Cajas blancas para los textos y definiciones (contrasta con el fondo suave) */
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
# BARRA LATERAL (SIDEBAR): DATOS DEL TERRENO
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ Panel de Control")
    st.markdown("---")
    
    st.markdown("### 🏡 Datos del Terreno")
    st.caption("Ingrese la ubicación y las mediciones de la propiedad:")
    
    # 1. Ubicación / Sector dentro de San Miguel
    sector_casa = st.selectbox(
        "📍 Zona / Sector (PRC San Miguel):",
        [
            "Zona ZU-1 (Eje Gran Avenida / Mixta)",
            "Zona ZU-2 (Residencial Mixta Alta Densidad)",
            "Zona ZU-3 (Residencial Media Densidad)",
            "Zona ZU-4 (Barrio El Llano / Conservación)",
            "Otro Sector de San Miguel"
        ]
    )
    
    direccion_casa = st.text_input(
        "📌 Dirección o Referencia del inmueble:",
        placeholder="Ej: Av. El Llano Subercaseaux 1234"
    )
    
    st.markdown("---")
    
    # 2. Mediciones del Terreno
    st.markdown("#### 📏 Mediciones del Terreno")
    
    superficie_terreno = st.number_input(
        "Superficie Total del Terreno (m²):",
        min_value=10.0,
        value=160.0,
        step=5.0
    )
    
    superficie_existente = st.number_input(
        "Superficie Construida Existente (m²):",
        min_value=0.0,
        value=70.0,
        step=5.0
    )
    
    frente_terreno = st.number_input(
        "Ancho / Frente del Terreno (m):",
        min_value=1.0,
        value=10.0,
        step=0.5
    )
    
    fondo_terreno = st.number_input(
        "Fondo / Largo del Terreno (m):",
        min_value=1.0,
        value=16.0,
        step=0.5
    )
    
    st.success("✅ Datos del terreno listos para evaluación.")

# ==========================================
# SECCIÓN 1: PRESENTACIÓN Y MARCO NORMATIVO
# ==========================================

# FRANJA SUPERIOR VERDE
st.markdown("""
<div class="franja-verde">
    <h1 style="color: white; margin-bottom: 0px; font-size: 32px;">🏗️ Prototipo de Software para Validación Normativa de Ampliaciones Domiciliarias</h1>
    <p style="font-size: 18px; color: #E8F8F5; margin-top: 10px;">Comuna de San Miguel | Aplicación de OGUC, Ley N° 20.898 y Plan Regulador Comunal</p>
</div>
""", unsafe_allow_html=True)

# PROPÓSITO ACADÉMICO 
st.markdown("""
<div class="texto-justificado-chico">
    <strong>Propósito Académico:</strong> Este software ha sido desarrollado como prototipo de titulación para la carrera de Ingeniería en Construcción. 
    Su objetivo es actuar como un sistema de asistencia técnica y normativa en la etapa preliminar de diseño de ampliaciones 
    residenciales, garantizando el cumplimiento de la reglamentación vigente en Chile y en la comuna de San Miguel.
</div>
<br>
""", unsafe_allow_html=True)

st.markdown("### 📜 Pilares Normativos Integrados")

# 1. OGUC
st.markdown("""
<div class="caja-blanca">
    <div class="titulo-ley">1. Ordenanza General de Urbanismo y Construcciones (OGUC)</div>
    <div class="texto-justificado">
        Es el reglamento rector que complementa y hace operativa la Ley General de Urbanismo y Construcciones en Chile. 
        Establece las disposiciones normativas a nivel nacional técnico y administrativo para la planificación urbana, 
        la urbanización de terrenos y las exigencias mínimas de diseño, seguridad y habitabilidad que debe cumplir 
        toda obra de construcción o ampliación en el país.
    </div>
    <div class="link-documento">🔗 <a href="https://www.bcn.cl/leychile/navegar?idNorma=13511" target="_blank">Ver documento oficial en la Biblioteca del Congreso Nacional de Chile (BCN)</a></div>
</div>
""", unsafe_allow_html=True)

# 2. LEY 20.898
st.markdown("""
<div class="caja-blanca">
    <div class="titulo-ley">2. Ley N° 20.898 (Procedimiento Simplificado)</div>
    <div class="texto-justificado">
        Conocida comúnmente como "Ley del Mono", es un cuerpo legal transitorio que establece un procedimiento simplificado 
        para la regularización de viviendas de autoconstrucción y ampliaciones que cumplen con metrajes y avalúos específicos. 
        Permite obtener la recepción definitiva acreditando condiciones mínimas de habitabilidad y seguridad estructural mediante 
        el patrocinio de un profesional competente.
    </div>
    <div class="link-documento">🔗 <a href="https://www.bcn.cl/leychile/navegar?idNorma=1087285" target="_blank">Ver documento oficial en la Biblioteca del Congreso Nacional de Chile (BCN)</a></div>
</div>
""", unsafe_allow_html=True)

# 3. PRC
st.markdown("""
<div class="caja-blanca">
    <div class="titulo-ley">3. Plan Regulador Comunal (PRC) - San Miguel</div>
    <div class="texto-justificado">
        Es el instrumento de planificación territorial que regula el desarrollo físico de las áreas urbanas a nivel local. 
        Define la zonificación de la comuna, los usos de suelo permitidos y las normas urbanísticas específicas (como coeficientes 
        de constructibilidad, ocupación de suelo, distanciamientos y rasantes) que condicionan la forma y tamaño de las ampliaciones.
    </div>
    <div class="link-documento">🔗 <a href="https://web.sanmiguel.cl/doctos/ordenanzas/plan_regulador/2.pdf" target="_blank">Ver documento oficial en la Municipalidad de San Miguel</a></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# SECCIÓN 2: GLOSARIO Y CONCEPTOS BÁSICOS
# ==========================================
st.markdown("### 📚 Glosario de Conceptos Urbanísticos")
st.write("Haz clic en cada concepto para desplegar su definición técnica:")

# Se usan "expanders" (cajas desplegables) para hacer la página interactiva
with st.expander("📐 Coeficiente de Constructibilidad"):
    st.write("Es el factor que, multiplicado por la superficie total del predio, determina la cantidad máxima de metros cuadrados que se permite construir en él. Las ampliaciones no deben sobrepasar el volumen total permitido por este coeficiente.")

with st.expander("📍 Coeficiente de Ocupación de Suelo"):
    st.write("Es el porcentaje máximo de la superficie del terreno que puede ser ocupado por la edificación en el primer piso. Define cuánto \"patio\" o área libre debe quedar obligatoriamente.")

with st.expander("📏 Rasante y Distanciamiento"):
    st.write("**Rasante:** Línea imaginaria inclinada que nace desde los deslindes del terreno e impone una envolvente máxima de altura para la edificación. \n\n**Distanciamiento:** Distancia mínima que debe existir entre la edificación y los deslindes del predio, variando según la altura de la construcción y si tiene o no ventanas.")

with st.expander("🌡️ Zona Térmica"):
    st.write("Clasificación geográfica que determina las exigencias mínimas de acondicionamiento térmico (aislación en techumbres, muros y pisos ventilados). La comuna de San Miguel se encuentra en la **Zona Térmica 3**, lo que exige materiales con una Transmitancia Térmica (U) específica según la OGUC.")
