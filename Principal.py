import streamlit as st
from pathlib import Path

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
# VARIABLES TEMPORALES PARA HABITACIONES
# ==========================================

# El Piso 1 comienza con un sector/habitación
if "cantidad_habitaciones_piso1" not in st.session_state:
    st.session_state.cantidad_habitaciones_piso1 = 1

# El Piso 2 también comenzará con un sector cuando sea activado
if "cantidad_habitaciones_piso2" not in st.session_state:
    st.session_state.cantidad_habitaciones_piso2 = 1


# ==========================================
# BARRA LATERAL (SIDEBAR) - MENÚ DE NAVEGACIÓN
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ Panel de Navegación")
    
    # Este es el menú que cambiará la pantalla principal
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
        <div class="link-documento">🔗 <a href="https://www.bcn.cl/leychile/navegar?idNorma=13511" target="_blank">Ver documento oficial en la BCN</a></div>
    </div>
    """, unsafe_allow_html=True)

    # 2. LEY 20.898
    st.markdown("""
    <div class="caja-blanca">
        <div class="titulo-ley">2. Ley N° 20.898 (Procedimiento Simplificado)</div>
        <div class="texto-justificado">
            Conocida comúnmente como "Ley del Mono", es un cuerpo legal transitorio que establece un procedimiento simplificado 
            para la regularización de viviendas de autoconstrucción y ampliaciones que cumplen con metrajes y avalúos específicos. 
            Permite obtener la recepción definitiva acreditando condiciones mínimas de habitabilidad y seguridad estructural.
        </div>
        <div class="link-documento">🔗 <a href="https://www.bcn.cl/leychile/navegar?idNorma=1087285" target="_blank">Ver documento oficial en la BCN</a></div>
    </div>
    """, unsafe_allow_html=True)

    # 3. PRC
    st.markdown("""
    <div class="caja-blanca">
        <div class="titulo-ley">3. Plan Regulador Comunal (PRC) - San Miguel</div>
        <div class="texto-justificado">
            Es el instrumento de planificación territorial que regula el desarrollo físico de las áreas urbanas a nivel local. 
            Define la zonificación de la comuna, los usos de suelo permitidos y las normas urbanísticas específicas.
        </div>
        <div class="link-documento">🔗 <a href="https://web.sanmiguel.cl/doctos/ordenanzas/plan_regulador/2.pdf" target="_blank">Ver documento oficial en la Municipalidad de San Miguel</a></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # GLOSARIO
    st.markdown("### 📚 Glosario de Conceptos Urbanísticos")
    st.write("Haz clic en cada concepto para desplegar su definición técnica:")

    with st.expander("📐 Coeficiente de Constructibilidad"):
        st.write("Es el factor que, multiplicado por la superficie total del predio, determina la cantidad máxima de metros cuadrados que se permite construir en él. Las ampliaciones no deben sobrepasar el volumen total permitido por este coeficiente.")

    with st.expander("📍 Coeficiente de Ocupación de Suelo"):
        st.write("Es el porcentaje máximo de la superficie del terreno que puede ser ocupado por la edificación en el primer piso. Define cuánto \"patio\" o área libre debe quedar obligatoriamente.")

    with st.expander("📏 Rasante y Distanciamiento"):
        st.write("**Rasante:** Línea imaginaria inclinada que nace desde los deslindes del terreno e impone una envolvente máxima de altura para la edificación. \n\n**Distanciamiento:** Distancia mínima que debe existir entre la edificación y los deslindes del predio, variando según la altura de la construcción y si tiene o no ventanas.")

    with st.expander("🌡️ Zona Térmica"):
        st.write("Clasificación geográfica que determina las exigencias mínimas de acondicionamiento térmico (aislación en techumbres, muros y pisos ventilados). La comuna de San Miguel se encuentra en la **Zona Térmica 3**, lo que exige materiales con una Transmitancia Térmica (U) específica según la OGUC.")


# ------------------------------------------
# PANTALLA 2: DATOS DEL TERRENO
# ------------------------------------------
elif menu_seleccionado == "🏡 Datos del Terreno":
    
    st.markdown("## 🏡 Ingreso de Datos del Terreno")
    st.markdown(
        "Por favor, ingrese la información de la propiedad para comenzar "
        "con la validación normativa."
    )

    st.markdown("---")


    # ==========================================
    # 1. UBICACIÓN DE LA PROPIEDAD
    # ==========================================
    st.markdown('<div class="caja-blanca">', unsafe_allow_html=True)

    st.markdown("### 📍 1. Ubicación de la Propiedad")


    # ==========================================
    # AYUDA PARA IDENTIFICAR LA ZONA PRC
    # ==========================================
    st.info(
        "🗺️ **¿No sabes en qué zona se encuentra tu propiedad?** "
        "Descarga el Plano Comunal de San Miguel, identifica la ubicación "
        "de tu inmueble y luego selecciona la zona correspondiente."
    )


    # ==========================================
    # PLANO COMUNAL DE SAN MIGUEL
    # ==========================================
    carpeta_proyecto = Path(__file__).resolve().parent

    ruta_plano = carpeta_proyecto / "Plano_Comunal_San_Miguel.pdf"

    if ruta_plano.exists():

        with open(ruta_plano, "rb") as archivo_pdf:

            datos_pdf = archivo_pdf.read()

            st.download_button(
                label="📥 Descargar Plano Comunal de San Miguel",
                data=datos_pdf,
                file_name="Plano_Comunal_San_Miguel.pdf",
                mime="application/pdf"
            )

    else:

        st.warning(
            "⚠️ El Plano Comunal de San Miguel no se encuentra disponible."
        )


    st.markdown("<br>", unsafe_allow_html=True)


    # ==========================================
    # SELECCIÓN DE ZONA Y DIRECCIÓN
    # ==========================================
    col1, col2 = st.columns(2)

    with col1:

        sector_casa = st.selectbox(
            "Zona según Plan Regulador Comunal de San Miguel:",
            [
                "Seleccione una zona...",
                "ZU-1 - Comercial Preferente y Residencial",
                "ZU-2 - Residencial de Renovación",
                "ZU-3 - Industrial Exclusiva",
                "ZU-4 - Industrial Mixta",
                "ZU-5 - Equipamiento Regional de Salud",
                "ZU-6 - Ferroviaria"
            ]
        )

    with col2:

        direccion_casa = st.text_input(
            "Dirección o Referencia del inmueble:",
            placeholder="Ej: Av. El Llano Subercaseaux 1234"
        )


    st.markdown('</div>', unsafe_allow_html=True)



    # ==========================================
    # 2. MEDICIONES DEL TERRENO Y VIVIENDA
    # ==========================================
    st.markdown('<div class="caja-blanca">', unsafe_allow_html=True)

    st.markdown("### 📏 2. Mediciones del Terreno y Vivienda")

    st.write(
        "Ingrese las dimensiones del terreno y de la vivienda. "
        "El software calculará automáticamente las superficies en metros cuadrados."
    )


    # ==========================================
    # DIMENSIONES DEL TERRENO
    # ==========================================
    st.markdown("#### 🌳 Dimensiones del Terreno")

    col3, col4 = st.columns(2)

    with col3:

        largo_terreno = st.number_input(
            "Largo del Terreno (m):",
            min_value=0.0,
            value=0.0,
            step=0.10,
            format="%.2f"
        )

    with col4:

        ancho_terreno = st.number_input(
            "Ancho del Terreno (m):",
            min_value=0.0,
            value=0.0,
            step=0.10,
            format="%.2f"
        )


    superficie_terreno = largo_terreno * ancho_terreno


    st.metric(
        label="📐 Superficie Total del Terreno",
        value=f"{superficie_terreno:.2f} m²"
    )


    if largo_terreno > 0 and ancho_terreno > 0:

        st.success(
            f"✅ {largo_terreno:.2f} m × {ancho_terreno:.2f} m "
            f"= **{superficie_terreno:.2f} m²**"
        )


    st.markdown("---")


    # ==========================================
    # MEDICIÓN DE LA VIVIENDA
    # ==========================================
    st.markdown("#### 🏠 Superficie Construida de la Vivienda")

    st.write(
        "Si la vivienda no tiene una forma rectangular, divida cada piso "
        "en sectores rectangulares simples e ingrese las dimensiones de cada uno."
    )


    # Columna izquierda para mediciones
    # Columna derecha para recomendación técnica
    columna_mediciones, columna_recomendacion = st.columns([2.2, 1])


    # ==========================================
    # COLUMNA IZQUIERDA
    # ==========================================
    with columna_mediciones:


        # ==========================================
        # PISO 1
        # ==========================================
        st.markdown("### 🏠 Piso 1")

        st.caption(
            "Ingrese el largo y ancho de cada habitación o sector. "
            "Si el piso tiene una forma irregular, puede agregar más sectores."
        )


        superficie_piso1 = 0.0


        for i in range(st.session_state.cantidad_habitaciones_piso1):

            st.markdown(f"**Habitación / Sector {i + 1}**")

            col_largo, col_ancho, col_area = st.columns([1, 1, 1])

            with col_largo:

                largo_p1 = st.number_input(
                    f"Largo (m)",
                    min_value=0.0,
                    value=0.0,
                    step=0.10,
                    format="%.2f",
                    key=f"largo_piso1_{i}"
                )

            with col_ancho:

                ancho_p1 = st.number_input(
                    f"Ancho (m)",
                    min_value=0.0,
                    value=0.0,
                    step=0.10,
                    format="%.2f",
                    key=f"ancho_piso1_{i}"
                )


            area_p1 = largo_p1 * ancho_p1

            superficie_piso1 += area_p1


            with col_area:

                st.metric(
                    "Superficie",
                    f"{area_p1:.2f} m²"
                )


        botones_p1_col1, botones_p1_col2 = st.columns(2)


        with botones_p1_col1:

            if st.button(
                "➕ Agregar habitación / sector",
                key="agregar_habitacion_piso1"
            ):

                st.session_state.cantidad_habitaciones_piso1 += 1
                st.rerun()


        with botones_p1_col2:

            if st.session_state.cantidad_habitaciones_piso1 > 1:

                if st.button(
                    "➖ Quitar último sector",
                    key="quitar_habitacion_piso1"
                ):

                    st.session_state.cantidad_habitaciones_piso1 -= 1
                    st.rerun()


        st.success(
            f"🏠 **Superficie calculada Piso 1: "
            f"{superficie_piso1:.2f} m²**"
        )


        st.markdown("---")


        # ==========================================
        # PISO 2
        # ==========================================
        st.markdown("### 🏘️ Piso 2")


        tiene_piso2 = st.checkbox(
            "La vivienda cuenta con segundo piso",
            key="tiene_piso2"
        )


        superficie_piso2 = 0.0


        if tiene_piso2:

            st.caption(
                "Ingrese el largo y ancho de cada habitación o sector del segundo piso. "
                "Puede agregar sectores adicionales cuando sea necesario."
            )


            for i in range(st.session_state.cantidad_habitaciones_piso2):

                st.markdown(f"**Habitación / Sector {i + 1}**")

                col_largo2, col_ancho2, col_area2 = st.columns([1, 1, 1])


                with col_largo2:

                    largo_p2 = st.number_input(
                        f"Largo (m)",
                        min_value=0.0,
                        value=0.0,
                        step=0.10,
                        format="%.2f",
                        key=f"largo_piso2_{i}"
                    )


                with col_ancho2:

                    ancho_p2 = st.number_input(
                        f"Ancho (m)",
                        min_value=0.0,
                        value=0.0,
                        step=0.10,
                        format="%.2f",
                        key=f"ancho_piso2_{i}"
                    )


                area_p2 = largo_p2 * ancho_p2

                superficie_piso2 += area_p2


                with col_area2:

                    st.metric(
                        "Superficie",
                        f"{area_p2:.2f} m²"
                    )


            botones_p2_col1, botones_p2_col2 = st.columns(2)


            with botones_p2_col1:

                if st.button(
                    "➕ Agregar habitación / sector",
                    key="agregar_habitacion_piso2"
                ):

                    st.session_state.cantidad_habitaciones_piso2 += 1
                    st.rerun()


            with botones_p2_col2:

                if st.session_state.cantidad_habitaciones_piso2 > 1:

                    if st.button(
                        "➖ Quitar último sector",
                        key="quitar_habitacion_piso2"
                    ):

                        st.session_state.cantidad_habitaciones_piso2 -= 1
                        st.rerun()


            st.success(
                f"🏘️ **Superficie calculada Piso 2: "
                f"{superficie_piso2:.2f} m²**"
            )


        else:

            st.info(
                "Si la vivienda posee un segundo piso, marque la casilla "
                "para ingresar sus dimensiones."
            )



    # ==========================================
    # COLUMNA DERECHA - AYUDA DE MEDICIÓN
    # ==========================================
    with columna_recomendacion:

        st.info(
            """
            📐 **Recomendación para una medición más precisa**

            Para obtener una estimación más exacta de la **superficie construida**, 
            se recomienda realizar las mediciones por el **exterior de la vivienda**, 
            considerando las dimensiones hasta las caras exteriores de los muros.

            Si no es posible acceder al perímetro exterior, puede medir las 
            dimensiones interiores de cada habitación o sector y considerar 
            adicionalmente el **espesor de los muros** correspondientes para 
            aproximar las dimensiones exteriores.

            Si la vivienda presenta una planta irregular, divídala mentalmente en 
            **figuras rectangulares simples que no se superpongan** e ingrese cada 
            una como un sector independiente.
            """
        )


    st.markdown("---")


    # ==========================================
    # SUPERFICIE TOTAL DE LA VIVIENDA
    # ==========================================
    superficie_total_vivienda = superficie_piso1 + superficie_piso2


    st.markdown("### 🧮 Superficie Construida Total")


    resumen_p1, resumen_p2, resumen_total = st.columns(3)


    with resumen_p1:

        st.metric(
            "Piso 1",
            f"{superficie_piso1:.2f} m²"
        )


    with resumen_p2:

        st.metric(
            "Piso 2",
            f"{superficie_piso2:.2f} m²"
        )


    with resumen_total:

        st.metric(
            "Total Vivienda",
            f"{superficie_total_vivienda:.2f} m²"
        )


    if superficie_total_vivienda > 0:

        st.success(
            f"✅ La superficie construida total calculada de la vivienda es de "
            f"**{superficie_total_vivienda:.2f} m²**."
        )


    st.markdown('</div>', unsafe_allow_html=True)



    # ==========================================
    # RESUMEN GENERAL
    # ==========================================
    if superficie_terreno > 0 or superficie_total_vivienda > 0:

        st.markdown("### 📋 Resumen de la Propiedad")


        resumen1, resumen2 = st.columns(2)


        with resumen1:

            st.metric(
                "🌳 Superficie Total del Terreno",
                f"{superficie_terreno:.2f} m²"
            )


        with resumen2:

            st.metric(
                "🏠 Superficie Construida Total",
                f"{superficie_total_vivienda:.2f} m²"
            )



    # ==========================================
    # BOTÓN GUARDAR DATOS
    # ==========================================
    if st.button("Guardar Datos y Continuar"):

        st.success(
            "¡Datos guardados correctamente en la memoria temporal del software!"
        )
