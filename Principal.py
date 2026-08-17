import streamlit as st

# ==========================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS
# ==========================================
st.set_page_config(
    page_title="Validación Normativa de Ampliaciones - San Miguel",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded" # Activamos la barra lateral desplegada
)

# Estilizado personalizado (Fondo gris-verdoso suave #F0F4F2 y tarjetas blancas)
st.markdown("""
    <style>
    /* Fondo principal */
    .stApp {
        background-color: #F0F4F2;
    }
    /* Tarjetas/Contenedores */
    .caja-blanca {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    /* Encabezados y títulos */
    h1, h2, h3 {
        color: #1E3A2B;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Cajas de estado / Semáforo */
    .alerta-exito {
        background-color: #D4EDDA;
        color: #155724;
        padding: 15px;
        border-radius: 8px;
        border-left: 6px solid #28A745;
        font-weight: bold;
    }
    .alerta-error {
        background-color: #F8D7DA;
        color: #721C24;
        padding: 15px;
        border-radius: 8px;
        border-left: 6px solid #DC3545;
        font-weight: bold;
    }
    .alerta-advertencia {
        background-color: #FFF3CD;
        color: #856404;
        padding: 15px;
        border-radius: 8px;
        border-left: 6px solid #FFC107;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# BARRA LATERAL (NAVEGACIÓN Y MENÚ)
# ==========================================
st.sidebar.image("https://img.icons8.com/color/96/construction.png", width=70)
st.sidebar.title("Navegación")

opcion_menu = st.sidebar.radio(
    "Seleccione una sección:",
    ["🏠 Inicio", "📐 Datos de Terreno", "📋 Validación Normativa"]
)

st.sidebar.markdown("---")
st.sidebar.info("**Comuna:** San Miguel\n\n**Normativas aplicadas:**\n- OGUC (Zona 3)\n- Ley N° 20.898 / Ley N° 21.725\n- PRC San Miguel")


# ==========================================
# PÁGINA 1: INICIO
# ==========================================
if opcion_menu == "🏠 Inicio":
    st.markdown("""
        <div class="caja-blanca">
            <h1>🏗️ Plataforma de Pre-factibilidad Normativa para Ampliaciones</h1>
            <h3>Ilustre Municipalidad de San Miguel | Región Metropolitana</h3>
            <p>Bienvenido al sistema digital interactivo diseñado para orientar a propietarios y proyectistas en la verificación preliminar de proyectos de ampliación y regularización residencial.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class="caja-blanca">
                <h4>🎯 Objetivo de la Herramienta</h4>
                <p>Facilitar la autoevaluación técnica de proyectos de ampliación de vivienda unifamiliar antes del ingreso formal de carpetas en la Dirección de Obras Municipales (DOM), reduciendo tasas de rechazo y tiempos de tramitación.</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="caja-blanca">
                <h4>📌 Módulos de Evaluación</h4>
                <ul>
                    <li><b>Datos de Terreno:</b> Verificación de límites urbanísticos y ocupación de suelo.</li>
                    <li><b>Límite de Metraje:</b> Verificación según Ley N° 20.898.</li>
                    <li><b>Acondicionamiento Térmico:</b> Exigencias de la OGUC para Zona Térmica 3.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    # Glosario Informativo
    st.markdown('<div class="caja-blanca">', unsafe_allow_html=True)
    st.subheader("📚 Marco Normativo y Glosario")

    with st.expander("📄 Ley N° 20.898 (Modificada por Ley N° 21.725)"):
        st.write("""
        Establece un procedimiento simplificado de regularización de viviendas unifamiliares. 
        La Ley N° 21.725 extendió la vigencia de ingreso de solicitudes ante la DOM hasta el **31 de diciembre de 2027**.
        """)

    with st.expander("📐 Distanciamientos y Rasantes (OGUC Art. 2.6.3 / PRC San Miguel)"):
        st.write("""
        Normas que regulan las distancias mínimas a deslindes vecinos y la altura máxima de la edificación según sus ángulos de rasante.
        """)

    with st.expander("🌡️ Acondicionamiento Térmico (OGUC Art. 4.1.10 - Zona 3)"):
        st.write("""
        San Miguel pertenece a la **Zona Térmica 3** (RM). Exige una transmitancia térmica máxima de $U \le 0,38 \text{ W/m}^2\text{K}$ en techumbre y $U \le 1,90 \text{ W/m}^2\text{K}$ en muros exteriores.
        """)

    with st.expander("🔗 Enlaces a Fuentes Oficiales"):
        st.markdown("- [Biblioteca del Congreso Nacional - Ley 20.898](https://www.bcn.cl/leychile/navegar?idNorma=1087221)")
        st.markdown("- [Ministerio de Vivienda y Urbanismo (MINVU)](https://www.minwu.gob.cl)")
        st.markdown("- [Portal de Transparencia del Estado de Chile](https://www.portaltransparencia.cl)")

    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# PÁGINA 2: DATOS DE TERRENO
# ==========================================
elif opcion_menu == "📐 Datos de Terreno":
    st.markdown("""
        <div class="caja-blanca">
            <h2>📐 Módulo: Antecedentes y Datos del Terreno</h2>
            <p>Ingrese los parámetros geométricos del predio según sus escrituras o Certificado de Informaciones Previas (CIP) otorgado por la DOM de San Miguel.</p>
        </div>
    """, unsafe_allow_html=True)

    col_terreno1, col_terreno2 = st.columns(2)

    with col_terreno1:
        st.markdown('<div class="caja-blanca">', unsafe_allow_html=True)
        st.subheader("📝 Dimensiones del Predio")
        
        superficie_predio = st.number_input(
            "Superficie Total del Terreno (m²):", 
            min_value=50.0, value=200.0, step=5.0,
            help="Superficie total consignada en el rol o título de dominio."
        )
        
        frente_predio = st.number_input(
            "Ancho del Frente / Línea Oficial (m):", 
            min_value=5.0, value=10.0, step=0.5
        )
        
        fondo_predio = st.number_input(
            "Profundidad / Fondo del Predio (m):", 
            min_value=5.0, value=20.0, step=0.5
        )

        antejardin = st.number_input(
            "Ancho de Antejardín existente o exigido (m):", 
            min_value=0.0, value=3.0, step=0.5,
            help="Distancia desde la Línea Oficial hasta la edificación."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_terreno2:
        st.markdown('<div class="caja-blanca">', unsafe_allow_html=True)
        st.subheader("🏛️ Indicadores Urbanísticos (PRC San Miguel)")
        
        zona_prc = st.selectbox(
            "Zona del Plan Regulador Comunal:",
            ["Zona Residencial Mixta (Z-2)", "Zona Residencial Consolidada (Z-3)", "Otras Zonas Residenciales"]
        )
        
        coef_ocupacion = st.slider(
            "Coeficiente Máximo de Ocupación del Suelo (%):", 
            min_value=30, max_value=80, value=60, step=5,
            help="Porcentaje del terreno que puede ser ocupado por construcciones en primer piso."
        )
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------
    # CÁLCULOS Y RESUMEN DEL TERRENO
    # ------------------------------------
    sup_ocupacion_max = superficie_predio * (coef_ocupacion / 100.0)
    
    st.markdown('<div class="caja-blanca">', unsafe_allow_html=True)
    st.subheader("📊 Capacidad Máxima de Ocupación en Primer Piso")
    
    c_res1, c_res2, c_res3 = st.columns(3)
    c_res1.metric("Superficie del Terreno", f"{superficie_predio:.1f} m²")
    c_res2.metric("Ocupación Suelo Permitida (%)", f"{coef_ocupacion}%")
    c_res3.metric("Ocupación Máxima en 1er Piso", f"{sup_ocupacion_max:.1f} m²")

    st.caption("ℹ️ *Nota: La superficie máxima edificable en primer nivel no podrá superar el valor indicado en la métrica superior para no infringir el Coeficiente de Ocupación de Suelo.*")
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# PÁGINA 3: VALIDACIÓN NORMATIVA
# ==========================================
elif opcion_menu == "📋 Validación Normativa":
    st.markdown("""
        <div class="caja-blanca">
            <h2>📋 Módulo: Validación Normativa y Térmica</h2>
            <p>Evalúe las condiciones específicas de su proyecto de ampliación (superficie, distanciamientos y aislación térmica).</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="caja-blanca">', unsafe_allow_html=True)
        st.subheader("📋 Ley N° 20.898 / Tramo")
        tramo_ley = st.selectbox(
            "Seleccione el Tramo de Aplicación:",
            ["Vivienda Social (Hasta 90 m²)", "Vivienda hasta 140 m² (Avalúo hasta 1.000 UF)"]
        )
        superficie_existente = st.number_input("Superficie construida previa (m²):", min_value=0.0, value=45.0, step=1.0)
        superficie_ampliacion = st.number_input("Superficie proyectada de ampliación (m²):", min_value=0.0, value=25.0, step=1.0)
        superficie_total = superficie_existente + superficie_ampliacion
        st.info(f"📐 **Superficie Total Resultante:** {superficie_total:.2f} m²")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="caja-blanca">', unsafe_allow_html=True)
        st.subheader("📐 Distanciamientos y Fachadas")
        distanciamiento = st.number_input("Distanciamiento al deslinde vecino (m):", min_value=0.0, value=1.5, step=0.1)
        posee_vanos = st.radio("¿La fachada cuenta con ventanas/vanos?", ["No (Muro ciego)", "Sí (Con ventanas)"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="caja-blanca">', unsafe_allow_html=True)
        st.subheader("🌡️ Acondicionamiento Térmico (OGUC Zona 3)")
        aislacion_techumbre = st.number_input("Espesor lana de vidrio en techumbre (mm):", min_value=0, value=80, step=5)
        material_muro = st.selectbox(
            "Estructura de muro exterior:",
            ["Tabiquería liviana con Lana de Vidrio (>= 50 mm)", "Tabiquería sin aislación", "Albañilería / Hormigón armado sin aislante"]
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Validación
        cumple_superficie = superficie_total <= (90.0 if "90 m²" in tramo_ley else 140.0)
        cumple_distanciamiento = distanciamiento >= (3.0 if posee_vanos == "Sí (Con ventanas)" else 1.4)
        cumple_termico = aislacion_techumbre >= 80 and "Lana de Vidrio (>= 50 mm)" in material_muro

        st.markdown('<div class="caja-blanca">', unsafe_allow_html=True)
        st.subheader("🔍 Resultado del Análisis")
        if cumple_superficie and cumple_distanciamiento and cumple_termico:
            st.markdown('<div class="alerta-exito">✅ PROYECTO PRE-APROBADO: Cumple con la normativa.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alerta-error">❌ REVISIÓN REQUERIDA: Presenta observaciones normativas.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
