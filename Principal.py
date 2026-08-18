import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
from pathlib import Path
from io import BytesIO

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
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
    [data-testid="stAppViewContainer"] {
        background-color: #F0F4F2;
    }

    .franja-verde {
        background-color: #1E7B44;
        color: white;
        padding: 25px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }

    .caja-blanca {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }

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

    .titulo-ley {
        color: #1E7B44;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 8px;
    }

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
# VARIABLES DE SESIÓN
# ==========================================
if "cantidad_habitaciones_piso1" not in st.session_state:
    st.session_state.cantidad_habitaciones_piso1 = 1

if "cantidad_habitaciones_piso2" not in st.session_state:
    st.session_state.cantidad_habitaciones_piso2 = 1

if "datos_propiedad" not in st.session_state:
    st.session_state.datos_propiedad = None

if "cantidad_modulos_ampliacion" not in st.session_state:
    st.session_state.cantidad_modulos_ampliacion = 1

if "propuesta_ampliacion" not in st.session_state:
    st.session_state.propuesta_ampliacion = None

# ==========================================
# BASE NORMATIVA PRC SAN MIGUEL
# ==========================================
@st.cache_data
def cargar_base_normativa():
    carpeta_proyecto = Path(__file__).resolve().parent
    ruta_excel = carpeta_proyecto / "Base_Normativa_PRC_San_Miguel.xlsx"

    if not ruta_excel.exists():
        return None

    base = pd.read_excel(ruta_excel, sheet_name="Coeficientes_PRC")
    base.columns = base.columns.str.strip()

    columnas_numericas = [
        "Superficie_Desde_m2",
        "Superficie_Hasta_m2",
        "Coef_Constructibilidad",
        "Coef_Ocupacion_1a3_Pisos",
        "Coef_Ocupacion_Sobre3_Pisos"
    ]

    for columna in columnas_numericas:
        if columna in base.columns:
            base[columna] = pd.to_numeric(base[columna], errors="coerce")

    columnas_texto = [
        "Zona",
        "Nombre_Zona",
        "Uso_Aplicable",
        "Residencial_General",
        "Tramo_Superficie_PRC",
        "Observacion",
        "Fuente"
    ]

    for columna in columnas_texto:
        if columna in base.columns:
            base[columna] = (
                base[columna]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    return base


def buscar_norma_residencial(base, zona, superficie_terreno):
    if base is None:
        return None

    datos_zona = base[
        base["Zona"].str.upper() == zona.upper()
    ].copy()

    if datos_zona.empty:
        return None

    datos_residenciales = datos_zona[
        (datos_zona["Residencial_General"].str.upper() == "SI")
        &
        (datos_zona["Uso_Aplicable"].str.lower() == "vivienda")
    ].copy()

    if datos_residenciales.empty:
        return None

    datos_residenciales = datos_residenciales.sort_values("Superficie_Desde_m2")

    for _, fila in datos_residenciales.iterrows():
        desde = fila["Superficie_Desde_m2"]
        hasta = fila["Superficie_Hasta_m2"]

        if pd.isna(desde):
            desde = 0

        if pd.isna(hasta):
            if superficie_terreno >= desde:
                return fila
        else:
            if superficie_terreno >= desde and superficie_terreno <= hasta:
                return fila

    return None


def formatear_tramo_m2(tramo):
    texto = str(tramo).strip()

    if not texto or texto.lower() == "nan":
        return "No definido"

    if "m²" in texto or "m2" in texto.lower():
        return texto

    texto_lower = texto.lower()

    if "y más" in texto_lower:
        posicion = texto_lower.find("y más")
        numero = texto[:posicion].strip()
        return f"{numero} m² y más"

    if "y mas" in texto_lower:
        posicion = texto_lower.find("y mas")
        numero = texto[:posicion].strip()
        return f"{numero} m² y más"

    if texto_lower == "no aplica":
        return "No aplica"

    return f"{texto} m²"


# ==========================================
# CROQUIS AUTOMÁTICO PRELIMINAR
# ==========================================
def crear_croquis_preliminar(datos, modulos):
    """
    Crea una representación automática y preliminar del terreno,
    la envolvente aproximada de la vivienda existente y los módulos
    de ampliación de primer piso.

    IMPORTANTE: la vivienda se representa como una envolvente rectangular
    aproximada a partir de los distanciamientos ingresados. No corresponde
    a un levantamiento arquitectónico exacto.
    """

    ancho_terreno = float(datos.get("ancho_terreno", 0) or 0)
    largo_terreno = float(datos.get("largo_terreno", 0) or 0)

    if ancho_terreno <= 0 or largo_terreno <= 0:
        return None, [], None

    izquierda = 0.0 if datos.get("adosado_izquierdo", False) else float(datos.get("distancia_izquierda", 0) or 0)
    derecha = 0.0 if datos.get("adosado_derecho", False) else float(datos.get("distancia_derecha", 0) or 0)
    posterior = 0.0 if datos.get("adosado_posterior", False) else float(datos.get("distancia_posterior", 0) or 0)
    antejardin = float(datos.get("antejardin_actual", 0) or 0)

    # Envolvente rectangular aproximada de la vivienda actual.
    casa_x = izquierda
    casa_y = antejardin
    casa_ancho = ancho_terreno - izquierda - derecha
    casa_largo = largo_terreno - antejardin - posterior

    # Si las distancias ingresadas generan una geometría imposible,
    # se usa una huella esquemática de respaldo para evitar romper el croquis.
    geometria_aproximada = True
    if casa_ancho <= 0 or casa_largo <= 0:
        superficie_p1 = max(float(datos.get("superficie_piso1", 0) or 0), 1.0)
        casa_ancho = min(ancho_terreno * 0.60, max(1.0, ancho_terreno - 0.5))
        casa_largo = min(largo_terreno * 0.55, max(1.0, superficie_p1 / casa_ancho))
        casa_x = max((ancho_terreno - casa_ancho) / 2, 0)
        casa_y = min(max(antejardin, 0), max(largo_terreno - casa_largo, 0))

    fig, ax = plt.subplots(figsize=(8, 10))

    # Terreno
    ax.add_patch(
        Rectangle(
            (0, 0),
            ancho_terreno,
            largo_terreno,
            fill=False,
            linewidth=2.2,
            edgecolor="#263238"
        )
    )

    # Antejardín medido
    if antejardin > 0 and antejardin < largo_terreno:
        ax.add_patch(
            Rectangle(
                (0, 0),
                ancho_terreno,
                antejardin,
                facecolor="#d5f5e3",
                edgecolor="none",
                alpha=0.65
            )
        )
        ax.text(
            ancho_terreno / 2,
            antejardin / 2,
            f"ANTEJARDÍN\n{antejardin:.2f} m",
            ha="center",
            va="center",
            fontsize=9
        )

    # Vivienda existente como envolvente aproximada
    ax.add_patch(
        Rectangle(
            (casa_x, casa_y),
            casa_ancho,
            casa_largo,
            facecolor="#85c1e9",
            edgecolor="#1b4f72",
            linewidth=1.8,
            alpha=0.78
        )
    )

    ax.text(
        casa_x + casa_ancho / 2,
        casa_y + casa_largo / 2,
        "VIVIENDA ACTUAL\n(envolvente aproximada)",
        ha="center",
        va="center",
        fontsize=9,
        weight="bold"
    )

    # Calle (banda exterior inferior)
    alto_calle = max(largo_terreno * 0.08, 1.2)
    ax.add_patch(
        Rectangle(
            (0, -alto_calle),
            ancho_terreno,
            alto_calle,
            facecolor="#d7dbdd",
            edgecolor="#7b7d7d",
            linewidth=1.0
        )
    )

    ax.text(
        ancho_terreno / 2,
        -alto_calle / 2,
        "CALLE / FRENTE DEL PREDIO",
        ha="center",
        va="center",
        fontsize=9,
        weight="bold"
    )

    # Ubicación automática de ampliaciones de Piso 1
    desplazamiento_izq = 0.0
    desplazamiento_der = 0.0
    desplazamiento_post = 0.0
    separacion = max(min(ancho_terreno, largo_terreno) * 0.01, 0.10)

    validaciones = []
    modulos_piso2 = []

    for modulo in modulos:
        if float(modulo.get("superficie", 0) or 0) <= 0:
            continue

        if modulo.get("piso") == "Piso 2":
            modulos_piso2.append(modulo)
            continue

        largo_modulo = float(modulo.get("largo", 0) or 0)
        ancho_modulo = float(modulo.get("ancho", 0) or 0)
        rotado = bool(modulo.get("rotado", False))

        # En planta: ancho = eje horizontal, largo = eje vertical.
        modulo_ancho = ancho_modulo
        modulo_largo = largo_modulo

        if rotado:
            modulo_ancho, modulo_largo = modulo_largo, modulo_ancho

        ubicacion = modulo.get("ubicacion", "")
        numero = modulo.get("numero", "")

        if ubicacion == "Lado izquierdo de la vivienda":
            x = casa_x - modulo_ancho
            y = casa_y + desplazamiento_izq
            desplazamiento_izq += modulo_largo + separacion

        elif ubicacion == "Lado derecho de la vivienda":
            x = casa_x + casa_ancho
            y = casa_y + desplazamiento_der
            desplazamiento_der += modulo_largo + separacion

        elif ubicacion == "Parte posterior de la vivienda":
            x = casa_x + desplazamiento_post
            y = casa_y + casa_largo
            desplazamiento_post += modulo_ancho + separacion

        else:
            validaciones.append(
                {
                    "numero": numero,
                    "cumple": False,
                    "mensaje": "No tiene una ubicación referencial definida."
                }
            )
            continue

        dentro_terreno = (
            x >= -1e-9
            and y >= -1e-9
            and (x + modulo_ancho) <= ancho_terreno + 1e-9
            and (y + modulo_largo) <= largo_terreno + 1e-9
        )

        respeta_frente = y >= antejardin - 1e-9
        cumple_geometria = dentro_terreno and respeta_frente

        color_modulo = "#f8c471" if cumple_geometria else "#f1948a"
        borde_modulo = "#935116" if cumple_geometria else "#922b21"

        ax.add_patch(
            Rectangle(
                (x, y),
                modulo_ancho,
                modulo_largo,
                facecolor=color_modulo,
                edgecolor=borde_modulo,
                linewidth=1.8,
                alpha=0.86
            )
        )

        ax.text(
            x + modulo_ancho / 2,
            y + modulo_largo / 2,
            f"AMPL. {numero}\n{modulo_ancho:.2f} × {modulo_largo:.2f} m",
            ha="center",
            va="center",
            fontsize=8,
            weight="bold"
        )

        if cumple_geometria:
            mensaje = "El módulo cabe dentro del terreno en esta ubicación automática."
        else:
            mensaje = "El módulo no cabe completamente en el espacio disponible de esta ubicación automática."

        validaciones.append(
            {
                "numero": numero,
                "cumple": cumple_geometria,
                "mensaje": mensaje
            }
        )

    # Cotas generales simples
    margen_cota = max(min(ancho_terreno, largo_terreno) * 0.06, 0.6)

    ax.annotate(
        "",
        xy=(0, largo_terreno + margen_cota),
        xytext=(ancho_terreno, largo_terreno + margen_cota),
        arrowprops=dict(arrowstyle="<->", linewidth=1.1)
    )
    ax.text(
        ancho_terreno / 2,
        largo_terreno + margen_cota * 1.18,
        f"Frente / ancho: {ancho_terreno:.2f} m",
        ha="center",
        va="bottom",
        fontsize=9
    )

    ax.annotate(
        "",
        xy=(-margen_cota, 0),
        xytext=(-margen_cota, largo_terreno),
        arrowprops=dict(arrowstyle="<->", linewidth=1.1)
    )
    ax.text(
        -margen_cota * 1.35,
        largo_terreno / 2,
        f"Largo: {largo_terreno:.2f} m",
        ha="center",
        va="center",
        rotation=90,
        fontsize=9
    )

    # Etiquetas de deslindes
    ax.text(
        ancho_terreno / 2,
        largo_terreno + margen_cota * 0.25,
        "DESLINDE POSTERIOR",
        ha="center",
        va="bottom",
        fontsize=8
    )

    ax.text(
        -margen_cota * 0.15,
        largo_terreno / 2,
        "DESLINDE IZQUIERDO",
        ha="right",
        va="center",
        rotation=90,
        fontsize=7
    )

    ax.text(
        ancho_terreno + margen_cota * 0.15,
        largo_terreno / 2,
        "DESLINDE DERECHO",
        ha="left",
        va="center",
        rotation=90,
        fontsize=7
    )

    # Aviso de segundo piso dentro de la figura
    if modulos_piso2:
        superficie_p2 = sum(float(m.get("superficie", 0) or 0) for m in modulos_piso2)
        ax.text(
            ancho_terreno / 2,
            largo_terreno + margen_cota * 2.05,
            f"Ampliación Piso 2: {superficie_p2:.2f} m² (se representará en planta separada)",
            ha="center",
            va="bottom",
            fontsize=8,
            style="italic"
        )

    leyenda = [
        Patch(facecolor="#85c1e9", edgecolor="#1b4f72", label="Vivienda existente (envolvente aprox.)"),
        Patch(facecolor="#f8c471", edgecolor="#935116", label="Ampliación que cabe en el terreno"),
        Patch(facecolor="#f1948a", edgecolor="#922b21", label="Ampliación fuera del espacio disponible"),
        Patch(facecolor="#d5f5e3", edgecolor="none", label="Antejardín medido")
    ]

    ax.legend(
        handles=leyenda,
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        borderaxespad=0,
        fontsize=8
    )

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-margen_cota * 2.0, ancho_terreno + margen_cota * 2.0)
    ax.set_ylim(-alto_calle - margen_cota * 0.4, largo_terreno + margen_cota * 2.8)
    ax.axis("off")
    ax.set_title(
        "Croquis Preliminar de Emplazamiento – Piso 1",
        fontsize=13,
        weight="bold",
        pad=18
    )

    fig.tight_layout()

    buffer_png = BytesIO()
    fig.savefig(
        buffer_png,
        format="png",
        dpi=200,
        bbox_inches="tight"
    )
    buffer_png.seek(0)

    return fig, validaciones, buffer_png


# ==========================================
# BARRA LATERAL
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ Panel de Navegación")

    menu_seleccionado = st.radio(
        "Seleccione un módulo:",
        (
            "🏠 Inicio",
            "🏡 Datos del Terreno",
            "🧱 Futura Ampliación"
        )
    )

    st.markdown("---")

    st.info(
        "Utilice este menú para navegar por las distintas "
        "etapas de la validación normativa."
    )

    if st.session_state.datos_propiedad is not None:
        st.success("✅ Datos de la propiedad guardados")

    if st.session_state.propuesta_ampliacion is not None:
        st.success("✅ Propuesta de ampliación guardada")


# ==========================================
# PANTALLA 1: INICIO
# ==========================================
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
        st.write(
            "Es el factor que, multiplicado por la superficie total "
            "del predio, determina la cantidad máxima de metros cuadrados "
            "que se permite construir en él. Las ampliaciones no deben "
            "sobrepasar el volumen total permitido por este coeficiente."
        )

    with st.expander("📍 Coeficiente de Ocupación de Suelo"):
        st.write(
            "Es el porcentaje máximo de la superficie del terreno que "
            "puede ser ocupado por la edificación en el primer piso. "
            "Define cuánto \"patio\" o área libre debe quedar "
            "obligatoriamente."
        )

    with st.expander("📏 Rasante y Distanciamiento"):
        st.write(
            "**Rasante:** Línea imaginaria inclinada que nace desde los "
            "deslindes del terreno e impone una envolvente máxima de altura "
            "para la edificación. \n\n"
            "**Distanciamiento:** Distancia mínima que debe existir entre "
            "la edificación y los deslindes del predio, variando según la "
            "altura de la construcción y si tiene o no ventanas."
        )

    with st.expander("🌡️ Zona Térmica"):
        st.write(
            "Clasificación geográfica que determina las exigencias mínimas "
            "de acondicionamiento térmico (aislación en techumbres, muros y "
            "pisos ventilados). La comuna de San Miguel se encuentra en la "
            "**Zona Térmica 3**, lo que exige materiales con una "
            "Transmitancia Térmica (U) específica según la OGUC."
        )


# ==========================================
# PANTALLA 2: DATOS DEL TERRENO
# ==========================================
elif menu_seleccionado == "🏡 Datos del Terreno":

    st.markdown("## 🏡 Ingreso de Datos del Terreno")
    st.markdown(
        "Por favor, ingrese la información de la propiedad "
        "para comenzar con la validación normativa."
    )
    st.markdown("---")

    # ==========================================
    # 1. UBICACIÓN
    # ==========================================
    st.markdown('<div class="caja-blanca">', unsafe_allow_html=True)
    st.markdown("### 📍 1. Ubicación de la Propiedad")

    st.info(
        "🗺️ **¿No sabes en qué zona se encuentra tu propiedad?** "
        "Descarga el Plano Comunal de San Miguel, identifica la "
        "ubicación de tu inmueble y luego selecciona la zona correspondiente."
    )

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
        st.warning("⚠️ El Plano Comunal de San Miguel no se encuentra disponible.")

    st.markdown("<br>", unsafe_allow_html=True)

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
    # 2. MEDICIONES
    # ==========================================
    st.markdown('<div class="caja-blanca">', unsafe_allow_html=True)
    st.markdown("### 📏 2. Mediciones del Terreno y Vivienda")
    st.write(
        "Ingrese las dimensiones del terreno y de la vivienda. "
        "El software calculará automáticamente las superficies "
        "en metros cuadrados."
    )

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
    st.markdown("#### 🏠 Superficie Construida de la Vivienda")
    st.write(
        "Si la vivienda no tiene una forma rectangular, "
        "divida cada piso en sectores rectangulares simples "
        "e ingrese las dimensiones de cada uno."
    )

    columna_mediciones, columna_recomendacion = st.columns([2.2, 1])
    sectores_piso1 = []
    sectores_piso2 = []

    with columna_mediciones:
        # PISO 1
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
                    "Largo (m)",
                    min_value=0.0,
                    value=0.0,
                    step=0.10,
                    format="%.2f",
                    key=f"largo_piso1_{i}"
                )

            with col_ancho:
                ancho_p1 = st.number_input(
                    "Ancho (m)",
                    min_value=0.0,
                    value=0.0,
                    step=0.10,
                    format="%.2f",
                    key=f"ancho_piso1_{i}"
                )

            area_p1 = largo_p1 * ancho_p1
            superficie_piso1 += area_p1

            sectores_piso1.append(
                {
                    "numero": i + 1,
                    "largo": float(largo_p1),
                    "ancho": float(ancho_p1),
                    "superficie": float(area_p1)
                }
            )

            with col_area:
                st.metric("Superficie", f"{area_p1:.2f} m²")

        botones_p1_col1, botones_p1_col2 = st.columns(2)

        with botones_p1_col1:
            if st.button("➕ Agregar habitación / sector", key="agregar_habitacion_piso1"):
                st.session_state.cantidad_habitaciones_piso1 += 1
                st.rerun()

        with botones_p1_col2:
            if st.session_state.cantidad_habitaciones_piso1 > 1:
                if st.button("➖ Quitar último sector", key="quitar_habitacion_piso1"):
                    st.session_state.cantidad_habitaciones_piso1 -= 1
                    st.rerun()

        st.success(
            f"🏠 **Superficie calculada Piso 1: {superficie_piso1:.2f} m²**"
        )

        st.markdown("---")

        # PISO 2
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
                        "Largo (m)",
                        min_value=0.0,
                        value=0.0,
                        step=0.10,
                        format="%.2f",
                        key=f"largo_piso2_{i}"
                    )

                with col_ancho2:
                    ancho_p2 = st.number_input(
                        "Ancho (m)",
                        min_value=0.0,
                        value=0.0,
                        step=0.10,
                        format="%.2f",
                        key=f"ancho_piso2_{i}"
                    )

                area_p2 = largo_p2 * ancho_p2
                superficie_piso2 += area_p2

                sectores_piso2.append(
                    {
                        "numero": i + 1,
                        "largo": float(largo_p2),
                        "ancho": float(ancho_p2),
                        "superficie": float(area_p2)
                    }
                )

                with col_area2:
                    st.metric("Superficie", f"{area_p2:.2f} m²")

            botones_p2_col1, botones_p2_col2 = st.columns(2)

            with botones_p2_col1:
                if st.button("➕ Agregar habitación / sector", key="agregar_habitacion_piso2"):
                    st.session_state.cantidad_habitaciones_piso2 += 1
                    st.rerun()

            with botones_p2_col2:
                if st.session_state.cantidad_habitaciones_piso2 > 1:
                    if st.button("➖ Quitar último sector", key="quitar_habitacion_piso2"):
                        st.session_state.cantidad_habitaciones_piso2 -= 1
                        st.rerun()

            st.success(
                f"🏘️ **Superficie calculada Piso 2: {superficie_piso2:.2f} m²**"
            )
        else:
            st.info(
                "Si la vivienda posee un segundo piso, marque la casilla "
                "para ingresar sus dimensiones."
            )

    with columna_recomendacion:
        st.info(
            """
            📐 **Recomendación para una medición más precisa**

            Para obtener una estimación más exacta de la **superficie construida**, se recomienda realizar las mediciones por el **exterior de la vivienda**, considerando las dimensiones hasta las caras exteriores de los muros.

            Si no es posible acceder al perímetro exterior, puede medir las dimensiones interiores de cada habitación o sector y considerar adicionalmente el **espesor de los muros** correspondientes para aproximar las dimensiones exteriores.

            Si la vivienda presenta una planta irregular, divídala mentalmente en **figuras rectangulares simples que no se superpongan** e ingrese cada una como un sector independiente.
            """
        )

    st.markdown("---")

    superficie_total_vivienda = superficie_piso1 + superficie_piso2

    st.markdown("### 🧮 Superficie Construida Total")
    resumen_p1, resumen_p2, resumen_total = st.columns(3)

    with resumen_p1:
        st.metric("Piso 1", f"{superficie_piso1:.2f} m²")
    with resumen_p2:
        st.metric("Piso 2", f"{superficie_piso2:.2f} m²")
    with resumen_total:
        st.metric("Total Vivienda", f"{superficie_total_vivienda:.2f} m²")

    if superficie_total_vivienda > 0:
        st.success(
            f"✅ La superficie construida total calculada de la vivienda es de "
            f"**{superficie_total_vivienda:.2f} m²**."
        )

    if superficie_total_vivienda >= 100:
        st.warning(
            "⚠️ **Revisión de cálculo estructural:** "
            "La vivienda calculada alcanza **100 m² o más**. "
            "Debe verificarse si corresponde presentar un **proyecto de cálculo estructural**, "
            "acompañado de memoria de cálculo y planos de estructura."
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # 3. DISTANCIAMIENTOS
    # ==========================================
    st.markdown('<div class="caja-blanca">', unsafe_allow_html=True)
    st.markdown("### 📐 3. Distanciamientos y Emplazamiento")
    st.write(
        "Ingrese las distancias actuales entre la vivienda y los límites del terreno."
    )

    st.info(
        "📏 **¿Cómo realizar esta medición?** "
        "Mida horizontalmente desde la cara exterior del muro de la vivienda hasta el límite "
        "del terreno correspondiente. Si la vivienda se encuentra construida directamente "
        "sobre el deslinde, marque la opción **Adosada al deslinde**."
    )

    deslinde_col1, deslinde_col2, deslinde_col3 = st.columns(3)

    with deslinde_col1:
        st.markdown("#### ⬅️ Deslinde izquierdo (lado izquierdo del terreno)")
        adosado_izquierdo = st.checkbox(
            "Adosada al deslinde izquierdo",
            key="adosado_izquierdo"
        )
        distancia_izquierda = st.number_input(
            "Distancia al deslinde izquierdo (m):",
            min_value=0.0,
            value=0.0,
            step=0.10,
            format="%.2f",
            disabled=adosado_izquierdo,
            key="distancia_izquierda"
        )
        if adosado_izquierdo:
            distancia_izquierda = 0.0

    with deslinde_col2:
        st.markdown("#### ➡️ Deslinde derecho (lado derecho del terreno)")
        adosado_derecho = st.checkbox(
            "Adosada al deslinde derecho",
            key="adosado_derecho"
        )
        distancia_derecha = st.number_input(
            "Distancia al deslinde derecho (m):",
            min_value=0.0,
            value=0.0,
            step=0.10,
            format="%.2f",
            disabled=adosado_derecho,
            key="distancia_derecha"
        )
        if adosado_derecho:
            distancia_derecha = 0.0

    with deslinde_col3:
        st.markdown("#### ⬆️ Deslinde posterior (parte trasera del terreno)")
        adosado_posterior = st.checkbox(
            "Adosada al deslinde posterior",
            key="adosado_posterior"
        )
        distancia_posterior = st.number_input(
            "Distancia al deslinde posterior (m):",
            min_value=0.0,
            value=0.0,
            step=0.10,
            format="%.2f",
            disabled=adosado_posterior,
            key="distancia_posterior"
        )
        if adosado_posterior:
            distancia_posterior = 0.0

    st.markdown("---")
    st.markdown("#### 🌿 Antejardín (espacio entre la calle y la vivienda)")
    st.caption(
        "Mida la distancia entre la línea frontal del terreno y la parte más cercana de la vivienda."
    )

    ante_col1, ante_col2 = st.columns(2)

    with ante_col1:
        antejardin_actual = st.number_input(
            "Distancia actual de antejardín (m):",
            min_value=0.0,
            value=0.0,
            step=0.10,
            format="%.2f"
        )

    with ante_col2:
        via_frente = st.selectbox(
            "Vía que enfrenta la propiedad:",
            [
                "Seleccione una opción...",
                "Otra calle de San Miguel",
                "Gran Avenida José Miguel Carrera",
                "Avenida Santa Rosa",
                "Avenida / Callejón Lo Ovalle",
                "No estoy seguro/a"
            ]
        )

    st.markdown("##### 📏 Frente del predio")

    ancho_es_frente = st.radio(
        "¿El ancho del terreno ingresado anteriormente corresponde al frente que da hacia la calle?",
        ["Sí", "No / No estoy seguro/a"],
        horizontal=True
    )

    if ancho_es_frente == "Sí":
        frente_predio = ancho_terreno
        if ancho_terreno > 0:
            st.caption(
                f"Se utilizará un frente predial aproximado de **{frente_predio:.2f} m**."
            )
    else:
        frente_predio = st.number_input(
            "Frente del terreno hacia la calle (m):",
            min_value=0.0,
            value=0.0,
            step=0.10,
            format="%.2f"
        )

    st.markdown("##### 🧾 Validación preliminar de antejardín")

    if via_frente == "Seleccione una opción...":
        st.info(
            "Seleccione la vía que enfrenta la propiedad para estimar la exigencia de antejardín del PRC."
        )

    elif via_frente == "No estoy seguro/a":
        st.info(
            "No es posible determinar automáticamente el antejardín mínimo sin conocer la vía que enfrenta el predio."
        )

    elif via_frente == "Gran Avenida José Miguel Carrera":
        st.success(
            "✅ **Antejardín mínimo según PRC: no se exige.** "
            "En Gran Avenida José Miguel Carrera no se exige antejardín."
        )

    elif via_frente in ["Avenida Santa Rosa", "Avenida / Callejón Lo Ovalle"]:
        st.warning(
            "⚠️ **Exigencia a verificar: entre 3 m y 5 m.** "
            "El PRC establece una exigencia general mínima de **3 m**, pero en Avenida Santa Rosa "
            "y Callejón Lo Ovalle se mantiene una exigencia histórica de **5 m** en los tramos que "
            "hayan adoptado la línea oficial."
        )

        if antejardin_actual >= 5:
            st.success(
                f"✅ El antejardín medido ({antejardin_actual:.2f} m) alcanza incluso la posible exigencia de 5 m."
            )
        elif antejardin_actual >= 3:
            st.warning(
                f"⚠️ El antejardín medido ({antejardin_actual:.2f} m) cumple la regla general de 3 m, "
                "pero debe verificarse si en este tramo corresponde la exigencia de 5 m."
            )
        else:
            st.error(
                f"❌ El antejardín medido ({antejardin_actual:.2f} m) es inferior a la regla general de 3 m del PRC."
            )

    elif via_frente == "Otra calle de San Miguel":
        posible_excepcion_2m = (
            superficie_terreno > 0
            and superficie_terreno <= 140
            and frente_predio > 0
            and frente_predio < 8
        )

        if posible_excepcion_2m:
            if antejardin_actual >= 3:
                st.success(
                    f"✅ **Antejardín general mínimo: 3,00 m.** El antejardín medido "
                    f"({antejardin_actual:.2f} m) cumple la regla general del PRC."
                )
            elif antejardin_actual >= 2:
                st.warning(
                    f"⚠️ El antejardín medido es de **{antejardin_actual:.2f} m**. "
                    "Podría aplicar una excepción de **2 m**, pero debe verificarse que la condición "
                    "se cumpla en el tramo o cuadra completa."
                )
            else:
                st.error(
                    f"❌ El antejardín medido ({antejardin_actual:.2f} m) es inferior incluso a la posible excepción de 2 m."
                )
        else:
            if antejardin_actual >= 3:
                st.success(
                    f"✅ **Antejardín mínimo de referencia: 3,00 m.** El antejardín medido "
                    f"({antejardin_actual:.2f} m) cumple preliminarmente."
                )
            else:
                st.error(
                    f"❌ **Antejardín mínimo de referencia: 3,00 m.** El antejardín medido "
                    f"({antejardin_actual:.2f} m) presenta un déficit aproximado de "
                    f"**{3.0 - antejardin_actual:.2f} m**."
                )

    st.caption(
        "ℹ️ Esta validación corresponde a la regla general del PRC. "
        "La aplicación de procedimientos especiales de regularización puede modificar las exigencias aplicables."
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # VARIABLES PRC
    # ==========================================
    superficie_maxima_ocupacion = None
    superficie_maxima_construible = None
    margen_primer_piso = None
    margen_constructibilidad = None
    coef_ocupacion = None
    coef_constructibilidad = None
    norma = None

    # ==========================================
    # 4. VALIDACIÓN AUTOMÁTICA PRC
    # ==========================================
    st.markdown('<div class="caja-blanca">', unsafe_allow_html=True)
    st.markdown("### 🧾 4. Validación Automática según PRC")
    st.write(
        "A partir de la zona seleccionada y de la superficie del terreno, el software consulta "
        "automáticamente la base normativa del Plan Regulador Comunal de San Miguel."
    )

    base_normativa = None
    error_base = None

    try:
        base_normativa = cargar_base_normativa()
    except Exception as error:
        error_base = error

    if error_base is not None:
        st.error("❌ Ocurrió un problema al leer la base normativa.")
        st.caption(f"Detalle técnico: {error_base}")

    elif base_normativa is None:
        st.warning("⚠️ No se encontró el archivo `Base_Normativa_PRC_San_Miguel.xlsx`.")

    elif sector_casa == "Seleccione una zona...":
        st.info("Seleccione primero la zona del PRC correspondiente a la propiedad.")

    elif superficie_terreno <= 0:
        st.info("Ingrese el largo y ancho del terreno para realizar la validación normativa.")

    else:
        zona_codigo = sector_casa.split(" - ")[0]

        filas_zona = base_normativa[
            base_normativa["Zona"].str.upper() == zona_codigo.upper()
        ]

        if filas_zona.empty:
            st.warning("⚠️ No se encontraron antecedentes normativos para esta zona.")

        elif not (filas_zona["Residencial_General"].str.upper() == "SI").any():
            nombre_zona = filas_zona.iloc[0]["Nombre_Zona"]
            observacion = filas_zona.iloc[0]["Observacion"]

            st.warning(
                f"⚠️ **{zona_codigo} - {nombre_zona}** no corresponde a una zona de uso residencial general."
            )

            if observacion:
                st.info(f"📌 **Observación normativa:** {observacion}")

            st.error(
                "El software no realizará el cálculo residencial de ocupación de suelo ni constructibilidad para esta zona."
            )

        else:
            norma = buscar_norma_residencial(
                base_normativa,
                zona_codigo,
                superficie_terreno
            )

            if norma is None:
                st.warning(
                    "⚠️ La superficie ingresada no coincide con ningún tramo disponible en la base normativa."
                )
            else:
                coef_constructibilidad = norma["Coef_Constructibilidad"]
                coef_ocupacion = norma["Coef_Ocupacion_1a3_Pisos"]
                tramo_superficie = norma["Tramo_Superficie_PRC"]
                nombre_zona = norma["Nombre_Zona"]

                st.success(
                    f"✅ Norma identificada automáticamente: **{zona_codigo} - {nombre_zona}**"
                )

                norma_col1, norma_col2, norma_col3 = st.columns(3)

                with norma_col1:
                    st.metric(
                        "Tramo de superficie",
                        formatear_tramo_m2(tramo_superficie)
                    )

                with norma_col2:
                    if pd.notna(coef_ocupacion):
                        st.metric("Coef. Ocupación de Suelo", f"{coef_ocupacion:.2f}")
                    else:
                        st.metric("Coef. Ocupación de Suelo", "No definido")

                with norma_col3:
                    if pd.notna(coef_constructibilidad):
                        st.metric("Coef. Constructibilidad", f"{coef_constructibilidad:.2f}")
                    else:
                        st.metric("Coef. Constructibilidad", "No definido")

                st.caption(
                    "ℹ️ El prototipo actualmente considera viviendas de hasta dos pisos."
                )

                if pd.notna(coef_constructibilidad) and pd.notna(coef_ocupacion):
                    superficie_maxima_ocupacion = superficie_terreno * coef_ocupacion
                    superficie_maxima_construible = superficie_terreno * coef_constructibilidad
                    margen_primer_piso = superficie_maxima_ocupacion - superficie_piso1
                    margen_constructibilidad = superficie_maxima_construible - superficie_total_vivienda

                    st.markdown("#### 🧮 Resultados Normativos")
                    resultado_col1, resultado_col2 = st.columns(2)

                    with resultado_col1:
                        st.metric(
                            "Máxima ocupación de suelo",
                            f"{superficie_maxima_ocupacion:.2f} m²"
                        )
                        st.caption(
                            f"{superficie_terreno:.2f} m² × {coef_ocupacion:.2f}"
                        )

                    with resultado_col2:
                        st.metric(
                            "Máxima superficie construible",
                            f"{superficie_maxima_construible:.2f} m²"
                        )
                        st.caption(
                            f"{superficie_terreno:.2f} m² × {coef_constructibilidad:.2f}"
                        )

                    st.markdown("#### 🏗️ Superficie Disponible Preliminar")
                    disponible_col1, disponible_col2 = st.columns(2)

                    with disponible_col1:
                        if margen_primer_piso >= 0:
                            st.success(
                                f"✅ **Disponible en primer piso:** {margen_primer_piso:.2f} m²"
                            )
                        else:
                            st.error(
                                f"❌ La ocupación actual supera el máximo en "
                                f"**{abs(margen_primer_piso):.2f} m²**."
                            )

                    with disponible_col2:
                        if margen_constructibilidad >= 0:
                            st.success(
                                f"✅ **Constructibilidad restante:** {margen_constructibilidad:.2f} m²"
                            )
                        else:
                            st.error(
                                f"❌ La superficie actual supera la constructibilidad máxima en "
                                f"**{abs(margen_constructibilidad):.2f} m²**."
                            )

                    if superficie_total_vivienda > 0:
                        st.markdown("#### ✅ Comparación con la Vivienda Actual")

                        if margen_primer_piso >= 0:
                            st.success(
                                f"✅ **Ocupación de suelo:** El Piso 1 ({superficie_piso1:.2f} m²) "
                                f"está dentro del máximo ({superficie_maxima_ocupacion:.2f} m²)."
                            )
                        else:
                            st.error("❌ **Ocupación de suelo:** El Piso 1 supera el máximo permitido.")

                        if margen_constructibilidad >= 0:
                            st.success(
                                f"✅ **Constructibilidad:** La vivienda ({superficie_total_vivienda:.2f} m²) "
                                f"está dentro del máximo ({superficie_maxima_construible:.2f} m²)."
                            )
                        else:
                            st.error("❌ **Constructibilidad:** La vivienda supera el máximo permitido.")

                    with st.expander("📚 Ver información normativa utilizada"):
                        st.write(f"**Zona:** {zona_codigo}")
                        st.write(f"**Nombre de zona:** {nombre_zona}")
                        st.write(f"**Tramo aplicado:** {formatear_tramo_m2(tramo_superficie)}")
                        st.write(f"**Coeficiente de ocupación de suelo:** {coef_ocupacion:.2f}")
                        st.write(f"**Coeficiente de constructibilidad:** {coef_constructibilidad:.2f}")

                        if norma["Observacion"]:
                            st.write(f"**Observación:** {norma['Observacion']}")

                        if norma["Fuente"]:
                            st.write(f"**Fuente:** {norma['Fuente']}")

    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # RESUMEN
    # ==========================================
    st.markdown("### 📋 Resumen de la Propiedad")
    resumen_col1, resumen_col2, resumen_col3, resumen_col4 = st.columns(4)

    with resumen_col1:
        st.metric("🌳 Superficie del Terreno", f"{superficie_terreno:.2f} m²")

    with resumen_col2:
        st.metric("🏠 Vivienda Construida", f"{superficie_total_vivienda:.2f} m²")

    with resumen_col3:
        if margen_primer_piso is None:
            st.metric("🏗️ Disponible 1er Piso", "Pendiente")
        elif margen_primer_piso >= 0:
            st.metric("🏗️ Disponible 1er Piso", f"{margen_primer_piso:.2f} m²")
        else:
            st.metric("🏗️ Disponible 1er Piso", f"Excede {abs(margen_primer_piso):.2f} m²")

    with resumen_col4:
        if margen_constructibilidad is None:
            st.metric("📐 Constructibilidad Restante", "Pendiente")
        elif margen_constructibilidad >= 0:
            st.metric("📐 Constructibilidad Restante", f"{margen_constructibilidad:.2f} m²")
        else:
            st.metric(
                "📐 Constructibilidad Restante",
                f"Excede {abs(margen_constructibilidad):.2f} m²"
            )

    st.markdown("#### 📍 Emplazamiento Medido")
    emplaza_col1, emplaza_col2, emplaza_col3, emplaza_col4 = st.columns(4)

    with emplaza_col1:
        st.metric("🌿 Antejardín Actual", f"{antejardin_actual:.2f} m")

    with emplaza_col2:
        if adosado_izquierdo:
            st.metric("⬅️ Deslinde Izquierdo", "Adosado")
        else:
            st.metric("⬅️ Deslinde Izquierdo", f"{distancia_izquierda:.2f} m")

    with emplaza_col3:
        if adosado_derecho:
            st.metric("➡️ Deslinde Derecho", "Adosado")
        else:
            st.metric("➡️ Deslinde Derecho", f"{distancia_derecha:.2f} m")

    with emplaza_col4:
        if adosado_posterior:
            st.metric("⬆️ Deslinde Posterior", "Adosado")
        else:
            st.metric("⬆️ Deslinde Posterior", f"{distancia_posterior:.2f} m")

    st.info(
        "ℹ️ **Importante:** La superficie disponible calculada corresponde a un máximo preliminar. "
        "También deben verificarse antejardines, distanciamientos, adosamientos, rasantes y demás exigencias aplicables."
    )

    # ==========================================
    # GUARDAR DATOS
    # ==========================================
    if st.button("💾 Guardar Datos y Continuar", type="primary"):
        errores_guardado = []

        if sector_casa == "Seleccione una zona...":
            errores_guardado.append("Debe seleccionar una zona del PRC.")

        if superficie_terreno <= 0:
            errores_guardado.append("Debe ingresar las dimensiones del terreno.")

        if superficie_total_vivienda <= 0:
            errores_guardado.append("Debe ingresar las dimensiones de la vivienda actual.")

        if errores_guardado:
            st.error("⚠️ Antes de continuar, complete los siguientes datos:")
            for error in errores_guardado:
                st.write(f"• {error}")
        else:
            zona_codigo_guardada = sector_casa.split(" - ")[0]

            coef_ocupacion_guardado = None
            coef_constructibilidad_guardado = None

            if coef_ocupacion is not None and pd.notna(coef_ocupacion):
                coef_ocupacion_guardado = float(coef_ocupacion)

            if coef_constructibilidad is not None and pd.notna(coef_constructibilidad):
                coef_constructibilidad_guardado = float(coef_constructibilidad)

            st.session_state.datos_propiedad = {
                "zona_completa": sector_casa,
                "zona_codigo": zona_codigo_guardada,
                "direccion": direccion_casa,
                "largo_terreno": float(largo_terreno),
                "ancho_terreno": float(ancho_terreno),
                "superficie_terreno": float(superficie_terreno),
                "frente_predio": float(frente_predio),
                "via_frente": via_frente,
                "sectores_piso1": sectores_piso1,
                "superficie_piso1": float(superficie_piso1),
                "tiene_piso2": bool(tiene_piso2),
                "sectores_piso2": sectores_piso2,
                "superficie_piso2": float(superficie_piso2),
                "superficie_total_vivienda": float(superficie_total_vivienda),
                "antejardin_actual": float(antejardin_actual),
                "adosado_izquierdo": bool(adosado_izquierdo),
                "distancia_izquierda": float(distancia_izquierda),
                "adosado_derecho": bool(adosado_derecho),
                "distancia_derecha": float(distancia_derecha),
                "adosado_posterior": bool(adosado_posterior),
                "distancia_posterior": float(distancia_posterior),
                "coef_ocupacion": coef_ocupacion_guardado,
                "coef_constructibilidad": coef_constructibilidad_guardado,
                "superficie_maxima_ocupacion": (
                    float(superficie_maxima_ocupacion)
                    if superficie_maxima_ocupacion is not None
                    else None
                ),
                "superficie_maxima_construible": (
                    float(superficie_maxima_construible)
                    if superficie_maxima_construible is not None
                    else None
                ),
                "margen_primer_piso": (
                    float(margen_primer_piso)
                    if margen_primer_piso is not None
                    else None
                ),
                "margen_constructibilidad": (
                    float(margen_constructibilidad)
                    if margen_constructibilidad is not None
                    else None
                )
            }

            # Si cambian los datos base, la propuesta anterior se invalida.
            st.session_state.propuesta_ampliacion = None

            st.success(
                "✅ **Datos guardados correctamente.** La información de la propiedad ya está disponible "
                "para el módulo de Futura Ampliación."
            )
            st.info(
                "👉 Ahora selecciona **🧱 Futura Ampliación** en el Panel de Navegación."
            )


# ==========================================
# PANTALLA 3: FUTURA AMPLIACIÓN
# ==========================================
elif menu_seleccionado == "🧱 Futura Ampliación":

    st.markdown("## 🧱 Diseño Preliminar de Futura Ampliación")
    st.write(
        "Diseñe una propuesta preliminar agregando uno o más módulos rectangulares de ampliación."
    )
    st.markdown("---")

    if st.session_state.datos_propiedad is None:
        st.warning("⚠️ **Aún no existen datos guardados de la propiedad.**")
        st.info(
            "Primero ingrese a **🏡 Datos del Terreno**, complete la información y presione "
            "**Guardar Datos y Continuar**."
        )

    else:
        datos = st.session_state.datos_propiedad

        # ==========================================
        # 1. DATOS BASE
        # ==========================================
        st.success("✅ Datos de la propiedad recuperados correctamente.")
        st.markdown("### 📋 1. Datos Base de la Propiedad")

        dato_col1, dato_col2, dato_col3, dato_col4 = st.columns(4)

        with dato_col1:
            st.metric("🌳 Terreno", f"{datos['superficie_terreno']:.2f} m²")

        with dato_col2:
            st.metric("🏠 Vivienda Actual", f"{datos['superficie_total_vivienda']:.2f} m²")

        with dato_col3:
            margen_p1_original = datos.get("margen_primer_piso")

            if margen_p1_original is None:
                st.metric("🏗️ Disponible Piso 1", "Pendiente")
            elif margen_p1_original >= 0:
                st.metric("🏗️ Disponible Piso 1", f"{margen_p1_original:.2f} m²")
            else:
                st.metric("🏗️ Disponible Piso 1", f"Excede {abs(margen_p1_original):.2f} m²")

        with dato_col4:
            margen_const_original = datos.get("margen_constructibilidad")

            if margen_const_original is None:
                st.metric("📐 Constructibilidad Restante", "Pendiente")
            elif margen_const_original >= 0:
                st.metric("📐 Constructibilidad Restante", f"{margen_const_original:.2f} m²")
            else:
                st.metric(
                    "📐 Constructibilidad Restante",
                    f"Excede {abs(margen_const_original):.2f} m²"
                )

        with st.expander("📐 Ver información de la propiedad"):
            st.write(f"**Zona:** {datos['zona_completa']}")
            st.write(
                f"**Terreno:** {datos['ancho_terreno']:.2f} m × {datos['largo_terreno']:.2f} m"
            )
            st.write(f"**Piso 1 actual:** {datos['superficie_piso1']:.2f} m²")
            st.write(f"**Piso 2 actual:** {datos['superficie_piso2']:.2f} m²")
            st.write(f"**Antejardín actual:** {datos['antejardin_actual']:.2f} m")

            if datos["adosado_izquierdo"]:
                st.write("**Deslinde izquierdo:** Adosado")
            else:
                st.write(f"**Deslinde izquierdo:** {datos['distancia_izquierda']:.2f} m")

            if datos["adosado_derecho"]:
                st.write("**Deslinde derecho:** Adosado")
            else:
                st.write(f"**Deslinde derecho:** {datos['distancia_derecha']:.2f} m")

            if datos["adosado_posterior"]:
                st.write("**Deslinde posterior:** Adosado")
            else:
                st.write(f"**Deslinde posterior:** {datos['distancia_posterior']:.2f} m")

        st.markdown("---")

        # ==========================================
        # 2. MÓDULOS DE AMPLIACIÓN
        # ==========================================
        st.markdown("### 🧩 2. Módulos de Ampliación")
        st.info(
            "📐 Divida la ampliación que desea realizar en **rectángulos simples**. "
            "Puede agregar tantos módulos como sea necesario."
        )

        modulos_ampliacion = []
        superficie_ampliacion_piso1 = 0.0
        superficie_ampliacion_piso2 = 0.0

        for i in range(st.session_state.cantidad_modulos_ampliacion):
            st.markdown(f"#### 🧱 Módulo de Ampliación {i + 1}")

            piso_modulo = st.radio(
                "¿Dónde se realizará este módulo?",
                ["Piso 1", "Piso 2"],
                horizontal=True,
                key=f"piso_ampliacion_{i}"
            )

            modulo_col1, modulo_col2, modulo_col3 = st.columns(3)

            with modulo_col1:
                largo_ampliacion = st.number_input(
                    "Largo del módulo (m):",
                    min_value=0.0,
                    value=0.0,
                    step=0.10,
                    format="%.2f",
                    key=f"largo_ampliacion_{i}"
                )

            with modulo_col2:
                ancho_ampliacion = st.number_input(
                    "Ancho del módulo (m):",
                    min_value=0.0,
                    value=0.0,
                    step=0.10,
                    format="%.2f",
                    key=f"ancho_ampliacion_{i}"
                )

            superficie_modulo = largo_ampliacion * ancho_ampliacion

            with modulo_col3:
                st.metric("Superficie del módulo", f"{superficie_modulo:.2f} m²")

            if piso_modulo == "Piso 1":
                ubicacion_modulo = st.selectbox(
                    "Ubicación referencial de la ampliación:",
                    [
                        "Seleccione una ubicación...",
                        "Lado izquierdo de la vivienda",
                        "Lado derecho de la vivienda",
                        "Parte posterior de la vivienda"
                    ],
                    key=f"ubicacion_ampliacion_{i}"
                )

                rotado_modulo = st.checkbox(
                    "🔄 Rotar módulo 90° en el croquis",
                    key=f"rotar_ampliacion_{i}"
                )

                if rotado_modulo:
                    st.caption(
                        f"En el croquis se representará como "
                        f"{largo_ampliacion:.2f} m de ancho × {ancho_ampliacion:.2f} m de profundidad."
                    )
                else:
                    st.caption(
                        f"En el croquis se representará como "
                        f"{ancho_ampliacion:.2f} m de ancho × {largo_ampliacion:.2f} m de profundidad."
                    )

                superficie_ampliacion_piso1 += superficie_modulo

            else:
                ubicacion_modulo = "Sobre la vivienda existente"
                rotado_modulo = False

                st.info(
                    "🏘️ Este módulo se considerará como una ampliación en segundo piso sobre la vivienda."
                )

                superficie_ampliacion_piso2 += superficie_modulo

            modulos_ampliacion.append(
                {
                    "numero": i + 1,
                    "piso": piso_modulo,
                    "largo": float(largo_ampliacion),
                    "ancho": float(ancho_ampliacion),
                    "superficie": float(superficie_modulo),
                    "ubicacion": ubicacion_modulo,
                    "rotado": bool(rotado_modulo)
                }
            )

            st.markdown("---")

        boton_modulo1, boton_modulo2 = st.columns(2)

        with boton_modulo1:
            if st.button("➕ Agregar otro módulo", key="agregar_modulo_ampliacion"):
                st.session_state.cantidad_modulos_ampliacion += 1
                st.rerun()

        with boton_modulo2:
            if st.session_state.cantidad_modulos_ampliacion > 1:
                if st.button("➖ Quitar último módulo", key="quitar_modulo_ampliacion"):
                    ultimo = st.session_state.cantidad_modulos_ampliacion - 1

                    claves_eliminar = [
                        f"piso_ampliacion_{ultimo}",
                        f"largo_ampliacion_{ultimo}",
                        f"ancho_ampliacion_{ultimo}",
                        f"ubicacion_ampliacion_{ultimo}",
                        f"rotar_ampliacion_{ultimo}"
                    ]

                    for clave in claves_eliminar:
                        if clave in st.session_state:
                            del st.session_state[clave]

                    st.session_state.cantidad_modulos_ampliacion -= 1
                    st.rerun()

        # ==========================================
        # 3. RESUMEN DE AMPLIACIÓN
        # ==========================================
        superficie_total_ampliacion = (
            superficie_ampliacion_piso1 + superficie_ampliacion_piso2
        )

        st.markdown("### 🧮 3. Resumen de la Ampliación Propuesta")
        ampliacion_col1, ampliacion_col2, ampliacion_col3 = st.columns(3)

        with ampliacion_col1:
            st.metric("🏠 Ampliación Piso 1", f"{superficie_ampliacion_piso1:.2f} m²")

        with ampliacion_col2:
            st.metric("🏘️ Ampliación Piso 2", f"{superficie_ampliacion_piso2:.2f} m²")

        with ampliacion_col3:
            st.metric("🧱 Ampliación Total", f"{superficie_total_ampliacion:.2f} m²")

        piso1_proyectado = datos["superficie_piso1"] + superficie_ampliacion_piso1
        piso2_proyectado = datos["superficie_piso2"] + superficie_ampliacion_piso2
        vivienda_total_proyectada = datos["superficie_total_vivienda"] + superficie_total_ampliacion

        st.markdown("#### 🏡 Vivienda después de la ampliación")
        proyectado_col1, proyectado_col2, proyectado_col3 = st.columns(3)

        with proyectado_col1:
            st.metric(
                "Piso 1 Proyectado",
                f"{piso1_proyectado:.2f} m²",
                delta=f"+{superficie_ampliacion_piso1:.2f} m²"
            )

        with proyectado_col2:
            st.metric(
                "Piso 2 Proyectado",
                f"{piso2_proyectado:.2f} m²",
                delta=f"+{superficie_ampliacion_piso2:.2f} m²"
            )

        with proyectado_col3:
            st.metric(
                "Total Proyectado",
                f"{vivienda_total_proyectada:.2f} m²",
                delta=f"+{superficie_total_ampliacion:.2f} m²"
            )

        st.markdown("---")

        # ==========================================
        # 4. VALIDACIÓN DE LA PROPUESTA
        # ==========================================
        st.markdown("### ✅ 4. Validación Preliminar de la Ampliación")

        superficie_maxima_ocupacion_guardada = datos.get("superficie_maxima_ocupacion")
        superficie_maxima_construible_guardada = datos.get("superficie_maxima_construible")

        margen_ocupacion_proyectada = None
        margen_constructibilidad_proyectada = None

        st.markdown("#### 📍 Ocupación de Suelo")

        if superficie_maxima_ocupacion_guardada is None:
            st.warning(
                "⚠️ No existe un valor de ocupación de suelo disponible para validar esta propuesta."
            )
        else:
            margen_ocupacion_proyectada = (
                superficie_maxima_ocupacion_guardada - piso1_proyectado
            )

            if margen_ocupacion_proyectada >= 0:
                st.success(
                    f"✅ **Cumple preliminarmente con la ocupación de suelo.** "
                    f"El Piso 1 proyectado tendría **{piso1_proyectado:.2f} m²**, mientras que "
                    f"el máximo calculado es **{superficie_maxima_ocupacion_guardada:.2f} m²**."
                )
                st.caption(
                    f"Después de esta ampliación quedarían aproximadamente "
                    f"**{margen_ocupacion_proyectada:.2f} m²** de margen de ocupación."
                )
            else:
                st.error(
                    f"❌ **La ampliación propuesta supera la ocupación máxima de suelo.** "
                    f"El Piso 1 proyectado tendría **{piso1_proyectado:.2f} m²** y el máximo calculado "
                    f"es **{superficie_maxima_ocupacion_guardada:.2f} m²**."
                )
                st.caption(
                    f"La propuesta excede el límite en **{abs(margen_ocupacion_proyectada):.2f} m²**."
                )

        st.markdown("#### 📐 Constructibilidad")

        if superficie_maxima_construible_guardada is None:
            st.warning(
                "⚠️ No existe un valor de constructibilidad disponible para validar esta propuesta."
            )
        else:
            margen_constructibilidad_proyectada = (
                superficie_maxima_construible_guardada - vivienda_total_proyectada
            )

            if margen_constructibilidad_proyectada >= 0:
                st.success(
                    f"✅ **Cumple preliminarmente con la constructibilidad.** "
                    f"La vivienda proyectada tendría **{vivienda_total_proyectada:.2f} m²**, mientras que "
                    f"el máximo calculado es **{superficie_maxima_construible_guardada:.2f} m²**."
                )
                st.caption(
                    f"Después de la ampliación quedarían aproximadamente "
                    f"**{margen_constructibilidad_proyectada:.2f} m²** de constructibilidad disponible."
                )
            else:
                st.error(
                    f"❌ **La ampliación propuesta supera la constructibilidad máxima.** "
                    f"La vivienda proyectada tendría **{vivienda_total_proyectada:.2f} m²**, mientras que "
                    f"el máximo es **{superficie_maxima_construible_guardada:.2f} m²**."
                )
                st.caption(
                    f"La propuesta excede el límite en "
                    f"**{abs(margen_constructibilidad_proyectada):.2f} m²**."
                )

        if vivienda_total_proyectada >= 100:
            st.warning(
                "⚠️ **Alerta estructural:** Con la ampliación propuesta, la vivienda alcanzaría "
                f"**{vivienda_total_proyectada:.2f} m²**. Al llegar a 100 m² o más debe verificarse "
                "si corresponde proyecto de cálculo estructural, memoria de cálculo y planos de estructura."
            )

        if superficie_ampliacion_piso2 > 0 and datos["superficie_piso2"] <= 0:
            st.info(
                "🏘️ **La propuesta incorpora un nuevo segundo piso.** Además de la superficie normativa, "
                "será necesaria una revisión estructural de la vivienda existente para determinar si puede "
                "recibir la nueva carga."
            )

        if superficie_ampliacion_piso1 > 0:
            st.markdown("#### 📍 Ubicación Referencial")

            for modulo in modulos_ampliacion:
                if modulo["piso"] == "Piso 1" and modulo["superficie"] > 0:
                    texto_rotacion = " (rotado 90°)" if modulo.get("rotado") else ""
                    st.write(
                        f"**Módulo {modulo['numero']}:** {modulo['ubicacion']} — "
                        f"{modulo['superficie']:.2f} m²{texto_rotacion}"
                    )

        st.markdown("---")

        # ==========================================
        # 5. CROQUIS PRELIMINAR AUTOMÁTICO
        # ==========================================
        st.markdown("### 🗺️ 5. Croquis Preliminar de la Propuesta")

        st.info(
            "🧩 **Primera versión del croquis automático:** el rectángulo exterior representa el terreno. "
            "La vivienda actual se muestra mediante una **envolvente rectangular aproximada** calculada con "
            "el antejardín y las distancias a los deslindes que guardaste. Los módulos de ampliación del "
            "Piso 1 se ubican automáticamente según el lado seleccionado."
        )

        st.warning(
            "⚠️ Este dibujo es **preliminar y esquemático**. Como todavía no hemos indicado la posición exacta "
            "de cada sector de la vivienda existente, el contorno azul no corresponde necesariamente a la forma "
            "real de la casa. En la siguiente etapa reemplazaremos esta aproximación por el editor tipo puzle."
        )

        distancias_sin_definir = (
            datos.get("antejardin_actual", 0) == 0
            and datos.get("distancia_izquierda", 0) == 0
            and datos.get("distancia_derecha", 0) == 0
            and datos.get("distancia_posterior", 0) == 0
            and not datos.get("adosado_izquierdo", False)
            and not datos.get("adosado_derecho", False)
            and not datos.get("adosado_posterior", False)
        )

        if distancias_sin_definir:
            st.warning(
                "📏 Todas las distancias de emplazamiento están en 0,00 m. El croquis se puede mostrar, "
                "pero será mucho más útil si primero ingresas el antejardín y las distancias reales a los deslindes."
            )

        modulos_para_croquis = [
            modulo
            for modulo in modulos_ampliacion
            if modulo["superficie"] > 0
        ]

        figura_croquis, validaciones_croquis, imagen_croquis = crear_croquis_preliminar(
            datos,
            modulos_para_croquis
        )

        if figura_croquis is None:
            st.error(
                "❌ No fue posible generar el croquis porque faltan las dimensiones del terreno."
            )
        else:
            st.pyplot(figura_croquis)

            st.caption(
                "Orientación del dibujo: la calle se representa en la parte inferior; "
                "el deslinde posterior se encuentra en la parte superior."
            )

            if validaciones_croquis:
                st.markdown("#### 🔎 Revisión geométrica automática del croquis")

                for revision in validaciones_croquis:
                    if revision["cumple"]:
                        st.success(
                            f"✅ **Módulo {revision['numero']}:** {revision['mensaje']}"
                        )
                    else:
                        st.error(
                            f"❌ **Módulo {revision['numero']}:** {revision['mensaje']}"
                        )

            modulos_piso2_croquis = [
                m for m in modulos_para_croquis if m["piso"] == "Piso 2"
            ]

            if modulos_piso2_croquis:
                st.info(
                    "🏘️ Los módulos de **Piso 2** no se dibujan dentro del plano de emplazamiento del primer piso. "
                    "En la siguiente etapa crearemos una planta separada para poder ubicarlos sobre la vivienda existente."
                )

            if imagen_croquis is not None:
                st.download_button(
                    "📥 Descargar croquis preliminar en PNG",
                    data=imagen_croquis,
                    file_name="Croquis_Preliminar_Ampliacion.png",
                    mime="image/png"
                )

            plt.close(figura_croquis)

        st.markdown("---")

        # ==========================================
        # GUARDAR PROPUESTA
        # ==========================================
        if st.button("💾 Guardar Propuesta de Ampliación", type="primary"):
            modulos_validos = [
                modulo
                for modulo in modulos_ampliacion
                if modulo["superficie"] > 0
            ]

            if len(modulos_validos) == 0:
                st.error(
                    "⚠️ Debe ingresar las dimensiones de al menos un módulo de ampliación."
                )
            else:
                ubicaciones_faltantes = []

                for modulo in modulos_validos:
                    if (
                        modulo["piso"] == "Piso 1"
                        and modulo["ubicacion"] == "Seleccione una ubicación..."
                    ):
                        ubicaciones_faltantes.append(modulo["numero"])

                if ubicaciones_faltantes:
                    st.error(
                        "⚠️ Debe seleccionar la ubicación referencial de todos los módulos del Piso 1."
                    )
                else:
                    st.session_state.propuesta_ampliacion = {
                        "modulos": modulos_validos,
                        "superficie_ampliacion_piso1": float(superficie_ampliacion_piso1),
                        "superficie_ampliacion_piso2": float(superficie_ampliacion_piso2),
                        "superficie_total_ampliacion": float(superficie_total_ampliacion),
                        "piso1_proyectado": float(piso1_proyectado),
                        "piso2_proyectado": float(piso2_proyectado),
                        "vivienda_total_proyectada": float(vivienda_total_proyectada),
                        "margen_ocupacion_proyectada": (
                            float(margen_ocupacion_proyectada)
                            if margen_ocupacion_proyectada is not None
                            else None
                        ),
                        "margen_constructibilidad_proyectada": (
                            float(margen_constructibilidad_proyectada)
                            if margen_constructibilidad_proyectada is not None
                            else None
                        )
                    }

                    st.success("✅ **Propuesta de ampliación guardada correctamente.**")
                    st.info(
                        "🗺️ Los módulos, sus dimensiones, orientación y ubicación referencial ya quedaron "
                        "guardados para la siguiente etapa del editor gráfico."
                    )

        if st.session_state.propuesta_ampliacion is not None:
            propuesta = st.session_state.propuesta_ampliacion

            with st.expander("✅ Ver propuesta guardada"):
                st.write(
                    f"**Ampliación Piso 1:** {propuesta['superficie_ampliacion_piso1']:.2f} m²"
                )
                st.write(
                    f"**Ampliación Piso 2:** {propuesta['superficie_ampliacion_piso2']:.2f} m²"
                )
                st.write(
                    f"**Ampliación total:** {propuesta['superficie_total_ampliacion']:.2f} m²"
                )
                st.write(
                    f"**Vivienda total proyectada:** {propuesta['vivienda_total_proyectada']:.2f} m²"
                )

                st.markdown("**Módulos:**")

                for modulo in propuesta["modulos"]:
                    rotacion = " — Rotado 90°" if modulo.get("rotado", False) else ""
                    st.write(
                        f"• Módulo {modulo['numero']} — {modulo['piso']} — "
                        f"{modulo['largo']:.2f} m × {modulo['ancho']:.2f} m — "
                        f"{modulo['superficie']:.2f} m² — {modulo['ubicacion']}{rotacion}"
                    )

        st.markdown("---")
        st.info(
            "🧩 **Próxima etapa:** convertir este croquis automático en un editor tipo puzle, "
            "para que puedas mover los bloques de la vivienda y de la ampliación dentro del terreno."
        )
