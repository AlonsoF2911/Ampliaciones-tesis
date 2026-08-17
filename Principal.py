import streamlit as st

# ==========================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS
# ==========================================
st.set_page_config(
    page_title="Validación Normativa de Ampliaciones - San Miguel",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
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
# BARRA LATERAL (MENÚ)
# ==========================================
st.sidebar.title("Menú")
opcion_menu = st.sidebar.radio(
    "Seleccione una sección:",
    ["Inicio", "Datos de terreno"]
)

# ==========================================
# SECCIÓN 1: INICIO (PANTALLA PRINCIPAL ORIGINAL)
# ==========================================
if opcion_menu == "Inicio":
    
    # Encabezado principal
    st.markdown("""
        <div class="caja-blanca">
            <h1>🏗️ Sistema de Validación Normativa para Ampliaciones Residenciales</h1>
            <h3>Comuna de San Miguel | Región Metropolitana</h3>
            <p>Herramienta digital de prefactibilidad técnica orientada a verificar el cumplimiento de la 
            <b>Ley N° 20.898</b> (modificada por Ley N° 21.725), la <b>OGUC</b> (Zona Térmica 3) y el 
            <b>Plan Regulador Comunal de San Miguel</b>.</p>
        </div>
    """, unsafe_allow_html=True)

    # Bloque de Módulos de Entrada y Evaluación
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="caja-blanca">', unsafe_allow_html=True)
        st.subheader("📋 Módulo 1: Regularización / Ley N° 20.898")
        
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
        st.subheader("📐 Módulo 2: Urbanismo y Distanciamientos (PRC San Miguel / OGUC)")
        
        distanciamiento = st.number_input("Distanciamiento al deslinde vecino más cercano (m):", min_value=0.0, value=1.5, step=0.1)
        posee_vanos = st.radio("¿La fachada hacia el deslinde cuenta con ventanas/vanos?", ["No (Muro ciego)", "Sí (Con ventanas)"])
        altura_proyectada = st.number_input("Altura máxima de la ampliación (m):", min_value=0.0, value=3.5, step=0.1)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="caja-blanca">', unsafe_allow_html=True)
        st.subheader("🌡️ Módulo 3: Acondicionamiento Térmico (OGUC Art. 4.1.10 - Zona 3)")
        
        aislacion_techumbre = st.number_input("Espesor de aislante en techumbre (Lana de vidrio mm):", min_value=0, value=80, step=5)
        material_muro = st.selectbox(
            "Estructura principal de muro exterior:",
            ["Tabiquería liviana con Lana de Vidrio (>= 50 mm)", "Tabiquería sin aislación", "Albañilería / Hormigón armado sin aislante adicional"]
        )
        
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="caja-blanca">', unsafe_allow_html=True)
        st.subheader("🔍 Evaluación de Prefactibilidad Normativa")
        
        # Lógica semáforo
        limite_m2 = 90.0 if "90 m²" in tramo_ley else 140.0
        cumple_superficie = superficie_total <= limite_m2

        dist_minimo = 3.0 if posee_vanos == "Sí (Con ventanas)" else 1.4
        cumple_distanciamiento = distanciamiento >= dist_minimo

        cumple_termico = aislacion_techumbre >= 80 and "Lana de Vidrio (>= 50 mm)" in material_muro

        if cumple_superficie and cumple_distanciamiento and cumple_termico:
            st.markdown("""
                <div class="alerta-exito">
                    ✅ PROYECTO PRE-APROBADO: Cumple con los requisitos normativos verificados para la comuna de San Miguel.
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="alerta-error">
                    ❌ REVISIÓN REQUERIDA: El diseño preliminar presenta observaciones técnicas que deben ser corregidas antes de ingresar la carpeta a la DOM.
                </div>
            """, unsafe_allow_html=True)

        st.write("---")
        st.write("**Detalle por parámetro evaluado:**")
        st.write(f"- Metraje y Tramo Ley 20.898: {'✅ Aprobado' if cumple_superficie else f'❌ Excede límite de {limite_m2} m²'}")
        st.write(f"- Distanciamiento mínimo a deslinde: {'✅ Aprobado' if cumple_distanciamiento else f'❌ Requiere mínimo {dist_minimo} m'}")
        st.write(f"- Exigencia Térmica OGUC (Zona 3): {'✅ Aprobado' if cumple_termico else '❌ Aislación insuficiente para muros o techumbre'}")

        st.markdown('</div>', unsafe_allow_html=True)

    # Glosario Informativo
    st.markdown('<div class="caja-blanca">', unsafe_allow_html=True)
    st.subheader("📚 Glosario Normativo e Información Técnica")

    with st.expander("📄 Ley N° 20.898 (Ley del Mono / Modificada por Ley N° 21.725)"):
        st.write("""
        Establece un procedimiento simplificado para la regularización de viviendas unifamiliares. 
        La modificación mediante la Ley N° 21.725 extendió la vigencia para el ingreso de solicitudes ante la DOM hasta el **31 de diciembre de 2027**.
        """)

    with st.expander("📐 Distanciamientos y Rasantes (OGUC Art. 2.6.3 / PRC San Miguel)"):
        st.write("""
        Los distanciamientos corresponden a la distancia mínima horizontal entre la edificación y los deslindes del predio. 
        Para muros ciegos (sin ventanas), el distanciamiento mínimo general es de 1,4 m, mientras que para muros con vanos o ventanas se exige al menos 3,0 m.
        """)

    with st.expander("🌡️ Exigencias de Acondicionamiento Térmico (OGUC Art. 4.1.10)"):
        st.write("""
        La comuna de San Miguel se ubica en la **Zona Térmica 3** (Región Metropolitana). 
        Exige valores máximos de Transmitancia Térmica ($U$) para limitar las pérdidas de calor:
        - **Techumbre:** $U \le 0,38 \text{ W/m}^2\text{K}$ (Aprox. $\ge 80 \text{ mm}$ de lana de vidrio o equivalente).
        - **Muros Exteriores:** $U \le 1,90 \text{ W/m}^2\text{K}$ (Requiere aislación continua en estructura liviana).
        """)

    with st.expander("🔗 Enlaces a Fuentes y Documentos Oficiales"):
        st.markdown("- [Biblioteca del Congreso Nacional - Ley 20.898](https://www.bcn.cl/leychile/navegar?idNorma=1087221)")
        st.markdown("- [Ministerio de Vivienda y Urbanismo (MINVU)](https://www.minwu.gob.cl)")
        st.markdown("- [Portal de Transparencia del Estado de Chile](https://www.portaltransparencia.cl)")

    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# SECCIÓN 2: DATOS DE TERRENO
# ==========================================
elif opcion_menu == "Datos de terreno":
    
    st.markdown("""
        <div class="caja-blanca">
            <h2>📐 Módulo: Datos de Terreno</h2>
            <p>Ingrese los antecedentes geométricos del predio según las escrituras o Certificado de Informaciones Previas (CIP) para verificar coeficientes de ocupación de suelo.</p>
        </div>
    """, unsafe_allow_html=True)

    col_terreno1, col_terreno2 = st.columns(2)
