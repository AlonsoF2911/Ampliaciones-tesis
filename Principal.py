import streamlit as st

# Configuración formal de la página
st.set_page_config(
    page_title="Validador Normativo de Ampliaciones",
    page_icon="🏗️",
    layout="wide"
)

# Encabezado Principal
st.title("🏗️ Prototipo de Software para Validación Normativa de Ampliaciones Domiciliarias")
st.caption("Comuna de San Miguel | Aplicación de OGUC, Ley N° 20.898 (modificada por Ley N° 21.725) y Plan Regulador Comunal")

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
    st.header("📌 Información del Sistema y Fundamentación Técnica")
    
    # Tarjeta de bienvenida y propósito
    st.info("""
    **Propósito Académico:**
    Este software ha sido desarrollado como prototipo de titulación para la carrera de Ingeniería en Construcción. 
    Su objetivo es actuar como un sistema de asistencia técnica y normativa en la etapa preliminar de diseño de ampliaciones 
    residenciales, garantizando el cumplimiento de la reglamentación vigente en Chile y en la comuna de San Miguel.
    """)
    
    st.subheader("📜 Pilares Normativos Integrados")
    st.markdown("La plataforma sintetiza la información técnica proveniente de tres cuerpos normativos fundamentales:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 1. OGUC")
        st.write("""
        **Ordenanza General de Urbanismo y Construcciones** Establece exigencias mínimas de habitabilidad, estabilidad y acondicionamiento térmico. 
        Para la Región Metropolitana y San Miguel, aplica la **Zona Térmica D**.
        """)
        
    with col2:
        st.markdown("### 2. Ley N° 20.898 / N° 21.725")
        st.write("""
        **Procedimiento Simplificado ("Ley del Mono")** Marco legal de regularización simplificada para viviendas. Incluye las actualizaciones de la Ley N° 21.725 
        (vigencia ampliada hasta el 31 de diciembre de 2027 y requisitos como el FUEE).
        """)
        
    with col3:
        st.markdown("### 3. PRC San Miguel")
        st.write("""
        **Plan Regulador Comunal de San Miguel** Norma urbanística territorial local que fija coeficientes de ocupación de suelo, constructibilidad, 
        líneas de edificación, rasantes y distanciamientos según cada zona predial.
        """)

    st.write("---")
    st.subheader("📋 Ficha Académica del Proyecto")
    st.write("**Proyecto:** Software de Apoyo Normativo para Ampliaciones Domiciliarias")
    st.write("**Carrera:** Ingeniería en Construcción")
    st.write("**Comuna de Aplicación:** San Miguel, Región Metropolitana (**Zona Térmica D**)")
    st.write("**Entorno Tecnológico:** Python & Streamlit Cloud")

# ==========================================
# SECCIÓN 2: GLOSARIO Y CONCEPTOS CLAVE
# ==========================================
elif opcion == "2. Glosario y Conceptos Clave":
    st.header("📚 Glosario de Términos Urbanísticos y Profesionales Competentes")
    st.markdown("Información orientativa esencial que todo propietario o evaluador debe conocer antes de proyectar una ampliación.")
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.subheader("📐 Conceptos Urbanísticos Básicos")
        
        with st.expander("¿Qué es el Deslinde?", expanded=True):
            st.write("""
            Es la línea divisoria o límite legal que separa un terreno o predio de las propiedades vecinas o del espacio público (calle o pasaje). 
            Todas las normas de distanciamiento y adosamiento se miden a partir de los deslindes.
            """)
            
        with st.expander("¿Qué es el Distanciamiento?"):
            st.write("""
            Es la distancia mínima horizontal fijada por la OGUC o el Plan Regulador Comunal que debe existir entre los muros de la edificación 
            y los deslindes del terreno vecinal, con el objetivo de resguardar la privacidad, iluminación y ventilación.
            """)
            
        with st.expander("¿Qué es la Línea Oficial de Edificación?"):
            st.write("""
            Es la línea deslindante trazada por la Dirección de Obras Municipales (DOM) que separa la propiedad privada del bien nacional de uso público (acera, calle o antejardín).
            """)

    with col_g2:
        st.subheader("👷 Profesionales Competentes en Chile")
        st.write("""
        Según la Ley General de Urbanismo y Construcciones (LGUC), los proyectos y expedientes de regularización de ampliaciones deben contar con la firma y patrocinio de profesionales habilitados:
        """)
        
        st.markdown("""
        * **Arquitecto:** Encargado del diseño arquitectónico, cumplimiento normativo general y expedientes de edificación ante la DOM.
        * **Constructor Civil / Ingeniero Constructor:** Profesional capacitado para la ejecución, supervisión técnica, verificación de estabilidad y gestión de las obras de construcción.
        * **Ingeniero Civil:** Especialista responsable del cálculo estructural y memorias técnicas cuando la complejidad o la altura de la estructura lo requieran.
        """)
        
        st.info("ℹ️ **Nota Normativa:** Para regularizaciones simplificadas (Ley N° 20.898), un profesional competente debe suscribir los planos y emitir el informe de habitabilidad y estabilidad de la edificación.")

# ==========================================
# SECCIÓN 3: MÓDULO DE INGRESO DE DATOS
# ==========================================
elif opcion == "3. Módulo de Ingreso de Datos":
    st.header("📝 Módulo de Evaluación de Proyecto")
    st.markdown("Ingrese los parámetros base de la vivienda y la ampliación para iniciar el análisis normativo.")
    
    st.subheader("Antecedentes de Superficie")
    sup_existente = st.number_input("Superficie existente edificada (m²):", min_value=0.0, value=0.0, step=1.0)
    sup_ampliacion = st.number_input("Superficie de ampliación proyectada (m²):", min_value=0.0, value=0.0, step=1.0)
    
    if st.button("Procesar Datos"):
        total = sup_existente + sup_ampliacion
        st.success(f"Superficie total registrada para análisis: {total} m²")
