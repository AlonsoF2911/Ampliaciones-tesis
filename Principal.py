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
# Aquí creamos la franja verde, justificamos textos y cambiamos tamaños
st.markdown("""
<style>
    /* Franja superior verde con texto blanco */
    .franja-verde {
        background-color: #1E7B44; /* Verde institucional */
        color: white;
        padding: 25px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 25px;
    }
    /* Estilo para justificar textos y achicar la letra del propósito */
    .texto-justificado-chico {
        text-align: justify;
        font-size: 14px;
        background-color: #F8F9F9; /* Fondo gris muy clarito para destacar */
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #1E7B44; /* Linea decorativa verde a la izquierda */
    }
    .texto-justificado {
        text-align: justify;
        font-size: 16px;
        margin-bottom: 10px;
    }
    /* Diferenciación de letras para los Títulos de las leyes */
    .titulo-ley {
        color: #1E7B44;
        font-size: 22px;
        font-weight: bold;
        margin-top: 25px;
        margin-bottom: 5px;
    }
    /* Estilo para los links */
    .link-documento {
        font-size: 14px;
        font-style: italic;
        margin-bottom: 15px;
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

# Menú de navegación principal en la barra lateral
opcion = st.sidebar.radio(
    "Navegación del Sistema",
    [
        "1. Presentación y Marco Normativo", 
        "2. Glosario y Conceptos Clave", 
        "3. Módulo de Ingreso de Datos"
    ]
)

# ==========================================
# SECCIÓN 1: PRESENTACIÓN Y MARCO NORMATIVO
# ==========================================
if opcion == "1. Presentación y Marco Normativo":
    
    # FRANJA SUPERIOR VERDE
    st.markdown("""
    <div class="franja-verde">
        <h1 style="color: white; margin-bottom: 0px;">🏗️ Prototipo de Software para Validación Normativa de Ampliaciones Domiciliarias</h1>
        <p style="font-size: 18px; color: white;">Comuna de San Miguel | Aplicación de OGUC, Ley N° 20.898 y Plan Regulador Comunal</p>
    </div>
    """, unsafe_allow_html=True)
    
    # PROPÓSITO ACADÉMICO (Chico y Justificado)
    st.markdown("""
    <div class="texto-justificado-chico">
        <strong>Propósito Académico:</strong> Este software ha sido desarrollado como prototipo de titulación para la carrera de Ingeniería en Construcción. 
        Su objetivo es actuar como un sistema de asistencia técnica y normativa en la etapa preliminar de diseño de ampliaciones 
        residenciales, garantizando el cumplimiento de la reglamentación vigente en Chile y en la comuna de San Miguel.
    </div>
    <hr>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📜 Pilares Normativos Integrados")
    
    # 1. OGUC (Vertical: Título -> Definición general justificada -> Link)
    st.markdown('<div class="titulo-ley">1. Ordenanza General de Urbanismo y Construcciones (OGUC)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="texto-justificado">
    Es el reglamento rector que complementa y hace operativa la Ley General de Urbanismo y Construcciones en Chile. 
    Establece las disposiciones normativas a nivel nacional técnico y administrativo para la planificación urbana, 
    la urbanización de terrenos y las exigencias mínimas de diseño, seguridad y habitabilidad que debe cumplir 
    toda obra de construcción o ampliación en el país.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="link-documento">🔗 <a href="https://www.bcn.cl/leychile/navegar?idNorma=13511" target="_blank">Ver documento oficial en la Biblioteca del Congreso Nacional de Chile (BCN)</a></div>', unsafe_allow_html=True)
    
    # 2. LEY 20.898 (Vertical: Título -> Definición justificada -> Link)
    st.markdown('<div class="titulo-ley">2. Ley N° 20.898 (Procedimiento Simplificado)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="texto-justificado">
    Conocida comúnmente como "Ley del Mono", es un cuerpo legal transitorio que establece un procedimiento simplificado 
    para la regularización de viviendas de autoconstrucción y ampliaciones que cumplen con metrajes y avalúos específicos. 
    Permite obtener la recepción definitiva acreditando condiciones mínimas de habitabilidad y seguridad estructural mediante 
    el patrocinio de un profesional competente.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="link-documento">🔗 <a href="https://www.bcn.cl/leychile/navegar?idNorma=1087195" target="_blank">Ver documento oficial en la Biblioteca del Congreso Nacional de Chile (BCN)</a></div>', unsafe_allow_html=True)
    
    # 3. PRC (Vertical: Título -> Definición justificada -> Link)
    st.markdown('<div class="titulo-ley">3. Plan Regulador Comunal (PRC) - San Miguel</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="texto-justificado">
    Es el instrumento de planificación territorial que regula el desarrollo físico de las áreas urbanas a nivel local. 
    Define la zonificación de la comuna, los usos de suelo permitidos y las normas urbanísticas específicas (como coeficientes 
    de constructibilidad, ocupación de suelo, distanciamientos y rasantes) que condicionan la forma y tamaño de las ampliaciones.
    </div>
    """, unsafe_allow_html=True)
    # Nota: Los PRC dependen de la municipalidad, no de la Biblioteca Nacional, por eso el link apunta a la fuente comunal.
    st.markdown('<div class="link-documento">🔗 <a href="https://www.sanmiguel.cl/plan-regulador-comunal/" target="_blank">Ver documentos oficiales en la Municipalidad de San Miguel</a></div>', unsafe_allow_html=True)


# ==========================================
# SECCIÓN 2: GLOSARIO Y CONCEPTOS CLAVE (Oculto por ahora para mantener corto el código)
# ==========================================
elif opcion == "2. Glosario y Conceptos Clave":
    st.header("📚 Glosario de Términos Urbanísticos")
    st.write("Aquí irá el contenido del glosario...")

# ==========================================
# SECCIÓN 3: MÓDULO DE INGRESO DE DATOS (Oculto por ahora)
# ==========================================
elif opcion == "3. Módulo de Ingreso de Datos":
    st.header("📝 Módulo de Evaluación de Proyecto")
    st.write("Aquí irán los inputs del usuario...")
    
    if st.button("Procesar Datos"):
        total = sup_existente + sup_ampliacion
        st.success(f"Superficie total registrada para análisis: {total} m²")
