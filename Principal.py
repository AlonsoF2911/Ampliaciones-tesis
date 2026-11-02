# VERSION: PASO18_LEY_MONO_COLOR_2026_11_02
# BASE: PASO8_PUZZLE_FRENTE_IMAGENES_2026_10_19
# VERSION: PASO6_RESULTADO_FINAL_REGULARIZACION_2026_10_19
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
from pathlib import Path
from io import BytesIO
import math
import html
from datetime import datetime

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib.utils import ImageReader
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        Image as PDFImage, PageBreak, KeepTogether
    )
    REPORTLAB_DISPONIBLE = True
except Exception:
    REPORTLAB_DISPONIBLE = False

# VERSION: PASO5_ENVOLVENTE_EXISTENTE_PISOS_TECHUMBRES_2026_10_19

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Orientación Normativa de Ampliaciones",
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

    /* Separación visual del panel lateral */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #DDEBE3 0%, #EEF5F1 100%);
        border-right: 3px solid #1E7B44;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.2rem;
    }

    [data-testid="stSidebar"] h3 {
        color: #14532D;
        font-weight: 800;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(30, 123, 68, 0.28);
    }

    .aviso-orientativo {
        background-color: #FFF8E1;
        border: 1px solid #E8C56A;
        border-left: 6px solid #E0A800;
        color: #4B3A00;
        padding: 14px 16px;
        border-radius: 8px;
        margin: 8px 0 22px 0;
        font-size: 14px;
        line-height: 1.55;
    }

    .subtitulo-inicio {
        font-size: 18px;
        color: #E8F8F5;
        margin-top: 10px;
        line-height: 1.45;
    }

    .titulo-glosario-grupo {
        color: #1E7B44;
        font-weight: 700;
        font-size: 17px;
        margin: 6px 0 10px 0;
    }

    /* ==========================================
       DATOS DEL TERRENO - PASO 16
       ========================================== */
    .datos-hero {
        background: linear-gradient(135deg, #14532D 0%, #1E7B44 58%, #2E8B57 100%);
        color: white;
        padding: 24px 26px;
        border-radius: 14px;
        margin-bottom: 14px;
        box-shadow: 0 7px 18px rgba(20, 83, 45, 0.18);
    }

    .datos-hero h2 {
        margin: 0 0 7px 0;
        font-size: 28px;
        font-weight: 800;
        color: white;
    }

    .datos-hero p {
        margin: 0;
        color: #EAF7EF;
        font-size: 15px;
        line-height: 1.55;
    }

    .datos-pasos {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 10px;
        margin: 4px 0 22px 0;
    }

    .datos-paso {
        background: white;
        border: 1px solid #D9E5DE;
        border-radius: 10px;
        padding: 10px 12px;
        font-size: 13px;
        font-weight: 700;
        color: #334139;
        box-shadow: 0 2px 7px rgba(0,0,0,0.035);
    }

    .datos-paso span {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        color: white;
        margin-right: 6px;
        font-size: 12px;
    }

    .paso-verde span { background: #2E7D32; }
    .paso-azul span { background: #1976D2; }
    .paso-ambar span { background: #D88700; }
    .paso-oscuro span { background: #14532D; }

    .datos-section {
        padding: 14px 18px;
        border-radius: 12px;
        margin: 8px 0 14px 0;
        border-left: 7px solid;
        box-shadow: 0 3px 10px rgba(0,0,0,0.04);
    }

    .datos-section .numero {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        color: white;
        font-weight: 800;
        margin-right: 8px;
    }

    .datos-section .titulo {
        font-size: 20px;
        font-weight: 800;
        vertical-align: middle;
    }

    .datos-section .descripcion {
        display: block;
        margin: 5px 0 0 40px;
        font-size: 13px;
        line-height: 1.45;
        color: #55635A;
    }

    .sec-ubicacion {
        background: linear-gradient(90deg, #EAF6ED 0%, #F8FCF9 100%);
        border-left-color: #2E7D32;
    }
    .sec-ubicacion .numero { background: #2E7D32; }
    .sec-ubicacion .titulo { color: #205B26; }

    .sec-medicion {
        background: linear-gradient(90deg, #E9F3FC 0%, #F8FBFE 100%);
        border-left-color: #1976D2;
    }
    .sec-medicion .numero { background: #1976D2; }
    .sec-medicion .titulo { color: #155A9C; }

    .sec-emplazamiento {
        background: linear-gradient(90deg, #FFF4DD 0%, #FFFDF8 100%);
        border-left-color: #D88700;
    }
    .sec-emplazamiento .numero { background: #D88700; }
    .sec-emplazamiento .titulo { color: #8A5700; }

    .sec-prc {
        background: linear-gradient(90deg, #E6F1EA 0%, #F7FBF8 100%);
        border-left-color: #14532D;
    }
    .sec-prc .numero { background: #14532D; }
    .sec-prc .titulo { color: #14532D; }

    .datos-subtitulo {
        font-size: 17px;
        font-weight: 800;
        margin: 13px 0 8px 0;
        padding: 8px 12px;
        border-radius: 8px;
        background: #F7FAF8;
        border-left: 4px solid #6F9D7F;
        color: #264D33;
    }

    .datos-resumen {
        background: linear-gradient(135deg, #EDF7F1 0%, #F7FBF9 100%);
        border: 1px solid #CFE3D6;
        border-top: 5px solid #1E7B44;
        border-radius: 13px;
        padding: 15px 18px 8px 18px;
        margin: 18px 0 12px 0;
    }

    .datos-resumen-titulo {
        color: #14532D;
        font-size: 21px;
        font-weight: 800;
        margin-bottom: 2px;
    }

    @media (max-width: 900px) {
        .datos-pasos { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }

    /* ==========================================
       FUTURA AMPLIACION - PASO 17
       ========================================== */
    .amp-hero {
        background: linear-gradient(135deg, #173B57 0%, #1F5D78 58%, #2F7894 100%);
        color: white;
        padding: 25px 27px;
        border-radius: 14px;
        margin-bottom: 14px;
        box-shadow: 0 7px 18px rgba(23, 59, 87, 0.20);
    }

    .amp-hero h2 {
        margin: 0 0 7px 0;
        font-size: 29px;
        font-weight: 800;
        color: white;
    }

    .amp-hero p {
        margin: 0;
        color: #EAF5FA;
        font-size: 15px;
        line-height: 1.55;
    }

    .amp-pasos {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 9px;
        margin: 5px 0 22px 0;
    }

    .amp-paso {
        background: white;
        border: 1px solid #D6E0E6;
        border-radius: 10px;
        padding: 9px 11px;
        font-size: 12.5px;
        font-weight: 750;
        color: #354955;
        box-shadow: 0 2px 7px rgba(0,0,0,0.035);
    }

    .amp-paso span {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 23px;
        height: 23px;
        border-radius: 50%;
        color: white;
        margin-right: 6px;
        font-size: 11px;
        font-weight: 800;
    }

    .amp-p1 span { background: #2878A0; }
    .amp-p2 span { background: #D97706; }
    .amp-p3 span { background: #0F766E; }
    .amp-p4 span { background: #2E7D32; }
    .amp-p5 span { background: #6D4C91; }
    .amp-p6 span { background: #A45A00; }
    .amp-p7 span { background: #16869A; }
    .amp-p8 span { background: #14532D; }

    .amp-section {
        padding: 14px 18px;
        border-radius: 12px;
        margin: 13px 0 14px 0;
        border-left: 7px solid;
        box-shadow: 0 3px 10px rgba(0,0,0,0.045);
    }

    .amp-section .numero {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        color: white;
        font-weight: 800;
        margin-right: 8px;
    }

    .amp-section .titulo {
        font-size: 20px;
        font-weight: 800;
        vertical-align: middle;
    }

    .amp-section .descripcion {
        display: block;
        margin: 5px 0 0 40px;
        font-size: 13px;
        line-height: 1.45;
        color: #56656D;
    }

    .amp-base { background: linear-gradient(90deg, #E9F4FA 0%, #F8FCFE 100%); border-left-color: #2878A0; }
    .amp-base .numero { background: #2878A0; } .amp-base .titulo { color: #1B5C7B; }
    .amp-modulos { background: linear-gradient(90deg, #FFF1DF 0%, #FFFDF8 100%); border-left-color: #D97706; }
    .amp-modulos .numero { background: #D97706; } .amp-modulos .titulo { color: #985005; }
    .amp-resumen { background: linear-gradient(90deg, #E7F7F4 0%, #F8FCFB 100%); border-left-color: #0F766E; }
    .amp-resumen .numero { background: #0F766E; } .amp-resumen .titulo { color: #0C5F58; }
    .amp-revision { background: linear-gradient(90deg, #EAF6ED 0%, #F8FCF9 100%); border-left-color: #2E7D32; }
    .amp-revision .numero { background: #2E7D32; } .amp-revision .titulo { color: #205B26; }
    .amp-croquis { background: linear-gradient(90deg, #F0EBF7 0%, #FCFAFE 100%); border-left-color: #6D4C91; }
    .amp-croquis .numero { background: #6D4C91; } .amp-croquis .titulo { color: #52356F; }
    .amp-soluciones { background: linear-gradient(90deg, #FFF2E0 0%, #FFFCF8 100%); border-left-color: #A45A00; }
    .amp-soluciones .numero { background: #A45A00; } .amp-soluciones .titulo { color: #7B4300; }
    .amp-estacionamientos { background: linear-gradient(90deg, #E6F6F8 0%, #F8FCFD 100%); border-left-color: #16869A; }
    .amp-estacionamientos .numero { background: #16869A; } .amp-estacionamientos .titulo { color: #0E6877; }
    .amp-resultado { background: linear-gradient(90deg, #E7F1EA 0%, #F8FBF9 100%); border-left-color: #14532D; }
    .amp-resultado .numero { background: #14532D; } .amp-resultado .titulo { color: #14532D; }

    .amp-subtitulo {
        font-size: 17px;
        font-weight: 800;
        margin: 13px 0 8px 0;
        padding: 8px 12px;
        border-radius: 8px;
        background: #F7FAFB;
        border-left: 4px solid #5A879D;
        color: #294D5D;
    }

    .amp-modulo-titulo {
        display: inline-block;
        background: #FFF3E4;
        border: 1px solid #F0C991;
        border-left: 5px solid #D97706;
        color: #8A4A05;
        font-size: 17px;
        font-weight: 800;
        padding: 8px 13px;
        border-radius: 8px;
        margin: 4px 0 8px 0;
    }

    .amp-pdf {
        background: linear-gradient(135deg, #EEF5FA 0%, #F9FCFE 100%);
        border: 1px solid #CCDDE8;
        border-top: 5px solid #2878A0;
        border-radius: 13px;
        padding: 14px 17px 6px 17px;
        margin: 18px 0 10px 0;
    }

    .amp-pdf-titulo {
        color: #1B5C7B;
        font-size: 21px;
        font-weight: 800;
        margin-bottom: 2px;
    }

    @media (max-width: 900px) {
        .amp-pasos { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }


    /* ==========================================
       REGULARIZACION LEY 20.898 - PASO 18
       ========================================== */
    .reg-hero {
        background: linear-gradient(135deg, #6B3428 0%, #8B4B36 55%, #AA6549 100%);
        color: white;
        padding: 25px 27px;
        border-radius: 14px;
        margin-bottom: 14px;
        box-shadow: 0 7px 18px rgba(107, 52, 40, 0.21);
    }

    .reg-hero h2 {
        margin: 0 0 7px 0;
        font-size: 29px;
        font-weight: 800;
        color: white;
    }

    .reg-hero p {
        margin: 0;
        color: #FFF1EB;
        font-size: 15px;
        line-height: 1.55;
    }

    .reg-pasos {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 9px;
        margin: 5px 0 22px 0;
    }

    .reg-paso {
        background: white;
        border: 1px solid #E4DAD6;
        border-radius: 10px;
        padding: 9px 10px;
        font-size: 12px;
        font-weight: 750;
        color: #51433E;
        box-shadow: 0 2px 7px rgba(0,0,0,0.035);
    }

    .reg-paso span {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 23px;
        height: 23px;
        border-radius: 50%;
        color: white;
        margin-right: 5px;
        font-size: 11px;
        font-weight: 800;
    }

    .reg-p1 span { background: #2878A0; }
    .reg-p2 span { background: #C57A16; }
    .reg-p3 span { background: #7952A3; }
    .reg-p4 span { background: #2E7D32; }
    .reg-p5 span { background: #A74832; }
    .reg-p6 span { background: #A45A00; }
    .reg-p7 span { background: #526D82; }
    .reg-p8 span { background: #16869A; }
    .reg-p9 span { background: #73558E; }
    .reg-p10 span { background: #14532D; }

    .reg-section {
        padding: 14px 18px;
        border-radius: 12px;
        margin: 13px 0 14px 0;
        border-left: 7px solid;
        box-shadow: 0 3px 10px rgba(0,0,0,0.045);
    }

    .reg-section .numero {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        color: white;
        font-weight: 800;
        margin-right: 8px;
    }

    .reg-section .titulo {
        font-size: 20px;
        font-weight: 800;
        vertical-align: middle;
    }

    .reg-section .descripcion {
        display: block;
        margin: 5px 0 0 40px;
        font-size: 13px;
        line-height: 1.45;
        color: #615B58;
    }

    .reg-datos { background: linear-gradient(90deg, #E9F4FA 0%, #F8FCFE 100%); border-left-color: #2878A0; }
    .reg-datos .numero { background: #2878A0; } .reg-datos .titulo { color: #1B5C7B; }
    .reg-condiciones { background: linear-gradient(90deg, #FFF3DF 0%, #FFFDF8 100%); border-left-color: #C57A16; }
    .reg-condiciones .numero { background: #C57A16; } .reg-condiciones .titulo { color: #8A5700; }
    .reg-ruta { background: linear-gradient(90deg, #F2ECF8 0%, #FCFAFE 100%); border-left-color: #7952A3; }
    .reg-ruta .numero { background: #7952A3; } .reg-ruta .titulo { color: #593B7B; }
    .reg-urbana { background: linear-gradient(90deg, #EAF6ED 0%, #F8FCF9 100%); border-left-color: #2E7D32; }
    .reg-urbana .numero { background: #2E7D32; } .reg-urbana .titulo { color: #205B26; }
    .reg-tecnica { background: linear-gradient(90deg, #FCECE8 0%, #FFF9F7 100%); border-left-color: #A74832; }
    .reg-tecnica .numero { background: #A74832; } .reg-tecnica .titulo { color: #813524; }
    .reg-muros { background: linear-gradient(90deg, #FFF2E0 0%, #FFFCF8 100%); border-left-color: #A45A00; }
    .reg-muros .numero { background: #A45A00; } .reg-muros .titulo { color: #7B4300; }
    .reg-piso { background: linear-gradient(90deg, #EDF2F5 0%, #FAFCFD 100%); border-left-color: #526D82; }
    .reg-piso .numero { background: #526D82; } .reg-piso .titulo { color: #3E5669; }
    .reg-techumbre { background: linear-gradient(90deg, #E6F6F8 0%, #F8FCFD 100%); border-left-color: #16869A; }
    .reg-techumbre .numero { background: #16869A; } .reg-techumbre .titulo { color: #0E6877; }
    .reg-documentos { background: linear-gradient(90deg, #F1ECF5 0%, #FCFAFD 100%); border-left-color: #73558E; }
    .reg-documentos .numero { background: #73558E; } .reg-documentos .titulo { color: #563D6B; }
    .reg-resultado { background: linear-gradient(90deg, #E7F1EA 0%, #F8FBF9 100%); border-left-color: #14532D; }
    .reg-resultado .numero { background: #14532D; } .reg-resultado .titulo { color: #14532D; }

    .reg-subtitulo {
        font-size: 16.5px;
        font-weight: 800;
        margin: 13px 0 8px 0;
        padding: 8px 12px;
        border-radius: 8px;
        background: #FAF8F7;
        border-left: 4px solid #9B6B5A;
        color: #543F37;
    }

    .reg-aviso {
        background: linear-gradient(90deg, #FFF4E8 0%, #FFF9F4 100%);
        border: 1px solid #E9C7AD;
        border-left: 6px solid #B9683E;
        color: #55382A;
        padding: 14px 16px;
        border-radius: 9px;
        margin: 8px 0 20px 0;
        font-size: 14px;
        line-height: 1.55;
    }

    .reg-cierre {
        background: linear-gradient(135deg, #EDF7F1 0%, #FAFCFB 100%);
        border: 1px solid #CFE3D6;
        border-top: 5px solid #1E7B44;
        border-radius: 13px;
        padding: 13px 16px 4px 16px;
        margin: 18px 0 10px 0;
    }

    @media (max-width: 1050px) {
        .reg-pasos { grid-template-columns: repeat(2, minmax(0, 1fr)); }
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

# Posiciones editables de los módulos en el editor tipo puzle.
if "posiciones_puzzle" not in st.session_state:
    st.session_state.posiciones_puzzle = {}

# Posiciones editables de los sectores de la vivienda existente.
if "posiciones_vivienda" not in st.session_state:
    st.session_state.posiciones_vivienda = {}

# Resultado guardado del módulo orientativo de regularización Ley N.º 20.898.
if "resultado_regularizacion" not in st.session_state:
    st.session_state.resultado_regularizacion = None

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


@st.cache_data
def cargar_soluciones_muros():
    """Carga las soluciones constructivas de muro seleccionadas para el prototipo."""
    carpeta_proyecto = Path(__file__).resolve().parent
    ruta_excel = carpeta_proyecto / "Base_Normativa_PRC_San_Miguel.xlsx"

    if not ruta_excel.exists():
        return None

    try:
        soluciones = pd.read_excel(ruta_excel, sheet_name="Soluciones_Muros")
    except Exception:
        return None

    soluciones.columns = soluciones.columns.str.strip()

    columnas_numericas = [
        "Espesor_Rev_Int_mm",
        "Espesor_Aislante_mm",
        "Densidad_Aislante_kg_m3",
        "Espesor_Placa_mm",
        "Espesor_Aislacion_Ext_mm",
        "Densidad_Aislacion_Ext_kg_m3",
        "Espesor_Rev_Ext_mm",
        "U_W_m2K",
        "Rt_m2K_W",
        "U_Max_Zona_D",
        "Rt_Min_Zona_D",
    ]

    for columna in columnas_numericas:
        if columna in soluciones.columns:
            soluciones[columna] = pd.to_numeric(soluciones[columna], errors="coerce")

    columnas_texto = [
        "Codigo_Solucion",
        "Elemento",
        "Sistema",
        "Estructura_Principal",
        "Revestimiento_Interior",
        "Barrera_Vapor",
        "Aislante_Entre_Estructura",
        "Placa_Estructural",
        "Aislacion_Exterior",
        "Barrera_Humedad",
        "Revestimiento_Exterior",
        "Compatibilidad_Zona_D",
        "Fuente",
        "Observacion",
        "Uso_Especial",
        "Resistencia_Fuego",
        "Fuente_Fuego",
    ]

    for columna in columnas_texto:
        if columna in soluciones.columns:
            soluciones[columna] = soluciones[columna].fillna("").astype(str).str.strip()

    return soluciones


@st.cache_data
def cargar_soluciones_pisos():
    """Carga las soluciones/criterios de piso seleccionados para el prototipo."""
    carpeta_proyecto = Path(__file__).resolve().parent
    ruta_excel = carpeta_proyecto / "Base_Normativa_PRC_San_Miguel.xlsx"

    if not ruta_excel.exists():
        return None

    try:
        soluciones = pd.read_excel(ruta_excel, sheet_name="Soluciones_Pisos")
    except Exception:
        return None

    soluciones.columns = soluciones.columns.str.strip()

    columnas_numericas = [
        "Espesor_Placa_Min_mm",
        "Espesor_Placa_Max_mm",
        "Espesor_Aislante_mm",
        "Densidad_Aislante_kg_m3",
        "Espesor_Rev_Inferior_mm",
        "Cama_Ripio_mm",
        "Radier_Hormigon_mm",
        "R100_Min_Sobrecimiento",
        "U_W_m2K",
        "Rt_m2K_W",
        "U_Max_Zona_D",
        "Rt_Min_Zona_D",
    ]

    for columna in columnas_numericas:
        if columna in soluciones.columns:
            soluciones[columna] = pd.to_numeric(soluciones[columna], errors="coerce")

    columnas_texto = [
        "Codigo_Solucion",
        "Elemento",
        "Condicion_Piso",
        "Sistema",
        "Tipo_Referencia",
        "Pavimento_Terminacion",
        "Placa_Estructural",
        "Estructura_Principal",
        "Aislante",
        "Barrera_Humedad_Viento",
        "Revestimiento_Inferior",
        "Aislacion_Sobrecimiento",
        "Compatibilidad_Zona_D",
        "Fuente",
        "Observacion",
    ]

    for columna in columnas_texto:
        if columna in soluciones.columns:
            soluciones[columna] = soluciones[columna].fillna("").astype(str).str.strip()

    return soluciones


@st.cache_data
def cargar_soluciones_techumbres():
    """Carga las soluciones de techumbre seleccionadas para el prototipo."""
    carpeta_proyecto = Path(__file__).resolve().parent
    ruta_excel = carpeta_proyecto / "Base_Normativa_PRC_San_Miguel.xlsx"

    if not ruta_excel.exists():
        return None

    try:
        soluciones = pd.read_excel(ruta_excel, sheet_name="Soluciones_Techumbres")
    except Exception:
        return None

    soluciones.columns = soluciones.columns.str.strip()

    columnas_numericas = [
        "Espesor_Cielo_mm",
        "Espesor_Aislante_mm",
        "Densidad_Aislante_Min_kg_m3",
        "Separacion_Cerchas_cm",
        "U_W_m2K",
        "Rt_m2K_W",
        "U_Max_Zona_D",
        "Rt_Min_Zona_D",
    ]

    for columna in columnas_numericas:
        if columna in soluciones.columns:
            soluciones[columna] = pd.to_numeric(soluciones[columna], errors="coerce")

    columnas_texto = [
        "Codigo_Solucion",
        "Elemento",
        "Sistema",
        "Geometria",
        "Cielo_Interior",
        "Barrera_Vapor",
        "Listoneado_Cielo",
        "Aislante",
        "Estructura_Principal",
        "Espacio_Entretecho",
        "Ventilacion_Entretecho",
        "Cubierta_Exterior",
        "Compatibilidad_Zona_D",
        "Fuente",
        "Observacion",
    ]

    for columna in columnas_texto:
        if columna in soluciones.columns:
            soluciones[columna] = soluciones[columna].fillna("").astype(str).str.strip()

    return soluciones


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
# RECURSOS VISUALES Y REFERENCIAS GEOMÉTRICAS
# ==========================================
CARPETA_PROYECTO = Path(__file__).resolve().parent

IMAGENES_SOLUCIONES = {
    "muro_madera": "detalle_muro_madera.png",
    "muro_acero": "detalle_muro_acero.png",
    "muro_albanileria": "detalle_muro_albanileria_eifs.png",
    "muro_f60": "detalle_muro_f60.png",
    "piso_radier": "detalle_radier.png",
    "piso_ventilado": "detalle_piso_ventilado.png",
    "techumbre_madera": "detalle_techumbre_madera.png",
}

def mostrar_imagen_solucion(clave, caption=None, ancho=None):
    """Muestra un detalle constructivo si el archivo está disponible en el proyecto."""
    nombre = IMAGENES_SOLUCIONES.get(clave)
    if not nombre:
        return False
    ruta = CARPETA_PROYECTO / nombre
    if not ruta.exists():
        st.caption(f"🖼️ Detalle visual no disponible: falta `{nombre}` en el repositorio.")
        return False
    kwargs = {"caption": caption} if caption else {}
    if ancho is not None:
        kwargs["width"] = ancho
    else:
        kwargs["use_container_width"] = True
    st.image(str(ruta), **kwargs)
    return True

def clave_imagen_muro(sistema, codigo=""):
    sistema = str(sistema or "").strip().lower()
    codigo = str(codigo or "").strip().lower()
    if "asim.1.60.24" in codigo or "f-60" in sistema or "f60" in sistema or "resistencia al fuego" in sistema:
        return "muro_f60"
    if "madera" in sistema:
        return "muro_madera"
    if "acero" in sistema:
        return "muro_acero"
    if "albañiler" in sistema or "albaniler" in sistema or "eifs" in sistema:
        return "muro_albanileria"
    return None

def calcular_antejardin_referencia(datos):
    """
    Devuelve el antejardín mínimo de referencia usado por el editor de futura ampliación.
    Se adopta un criterio conservador cuando la excepción depende de verificar el tramo/cuadra.
    """
    via = str(datos.get("via_frente", "") or "").strip()
    if via == "Gran Avenida José Miguel Carrera":
        return 0.0
    # Santa Rosa y Lo Ovalle pueden requerir 5 m en ciertos tramos; mientras no se
    # acredite esa condición, el editor usa 3 m como referencia y mantiene la advertencia.
    return 3.0

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
    antejardin_minimo = calcular_antejardin_referencia(datos)

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
    desplazamiento_frente = 0.0
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

        elif ubicacion == "Parte frontal de la vivienda (hacia la calle)":
            x = casa_x + desplazamiento_frente
            y = casa_y - modulo_largo
            desplazamiento_frente += modulo_ancho + separacion

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

        respeta_frente = y >= antejardin_minimo - 1e-9
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
# CROQUIS AUTOMÁTICO PRELIMINAR - PISO 2
# ==========================================
def crear_croquis_piso2(datos, modulos):
    """
    Crea una planta esquemática del segundo piso.

    La huella del Piso 1 se utiliza únicamente como referencia y la forma
    exacta del Piso 2 sigue siendo aproximada hasta incorporar el editor
    gráfico tipo puzle.
    """

    ancho_terreno = float(datos.get("ancho_terreno", 0) or 0)
    largo_terreno = float(datos.get("largo_terreno", 0) or 0)

    if ancho_terreno <= 0 or largo_terreno <= 0:
        return None, [], None

    izquierda = (
        0.0
        if datos.get("adosado_izquierdo", False)
        else float(datos.get("distancia_izquierda", 0) or 0)
    )
    derecha = (
        0.0
        if datos.get("adosado_derecho", False)
        else float(datos.get("distancia_derecha", 0) or 0)
    )
    posterior = (
        0.0
        if datos.get("adosado_posterior", False)
        else float(datos.get("distancia_posterior", 0) or 0)
    )
    antejardin = float(datos.get("antejardin_actual", 0) or 0)

    # Huella aproximada de la vivienda en Piso 1, usada como referencia.
    casa_x = izquierda
    casa_y = antejardin
    casa_ancho = ancho_terreno - izquierda - derecha
    casa_largo = largo_terreno - antejardin - posterior

    if casa_ancho <= 0 or casa_largo <= 0:
        superficie_p1 = max(float(datos.get("superficie_piso1", 0) or 0), 1.0)
        casa_ancho = min(ancho_terreno * 0.60, max(1.0, ancho_terreno - 0.5))
        casa_largo = min(largo_terreno * 0.55, max(1.0, superficie_p1 / casa_ancho))
        casa_x = max((ancho_terreno - casa_ancho) / 2, 0)
        casa_y = min(max(antejardin, 0), max(largo_terreno - casa_largo, 0))

    fig, ax = plt.subplots(figsize=(8, 10))

    # Terreno como marco de referencia.
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

    # Calle / frente.
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

    # Huella Piso 1 como referencia, sin afirmar que sea la forma real.
    ax.add_patch(
        Rectangle(
            (casa_x, casa_y),
            casa_ancho,
            casa_largo,
            facecolor="#ebedef",
            edgecolor="#5d6d7e",
            linewidth=1.5,
            linestyle="--",
            alpha=0.70
        )
    )
    ax.text(
        casa_x + casa_ancho / 2,
        casa_y + casa_largo * 0.08,
        "HUELLA PISO 1\n(referencia)",
        ha="center",
        va="center",
        fontsize=8
    )

    # Representación aproximada del Piso 2 existente usando su superficie.
    superficie_p2_actual = float(datos.get("superficie_piso2", 0) or 0)
    area_huella = max(casa_ancho * casa_largo, 0)

    if superficie_p2_actual > 0 and area_huella > 0:
        area_objetivo = min(superficie_p2_actual, area_huella)
        proporcion = casa_ancho / casa_largo if casa_largo > 0 else 1.0

        piso2_ancho = min(casa_ancho, max(0.5, (area_objetivo * proporcion) ** 0.5))
        piso2_largo = area_objetivo / piso2_ancho if piso2_ancho > 0 else 0

        if piso2_largo > casa_largo:
            piso2_largo = casa_largo
            piso2_ancho = area_objetivo / piso2_largo if piso2_largo > 0 else 0

        piso2_ancho = min(piso2_ancho, casa_ancho)
        piso2_largo = min(piso2_largo, casa_largo)

        piso2_x = casa_x + (casa_ancho - piso2_ancho) / 2
        piso2_y = casa_y + (casa_largo - piso2_largo) / 2

        ax.add_patch(
            Rectangle(
                (piso2_x, piso2_y),
                piso2_ancho,
                piso2_largo,
                facecolor="#85c1e9",
                edgecolor="#1b4f72",
                linewidth=1.8,
                alpha=0.80
            )
        )
        ax.text(
            piso2_x + piso2_ancho / 2,
            piso2_y + piso2_largo / 2,
            f"PISO 2 ACTUAL\n{superficie_p2_actual:.2f} m² aprox.",
            ha="center",
            va="center",
            fontsize=8,
            weight="bold"
        )
    else:
        ax.text(
            casa_x + casa_ancho / 2,
            casa_y + casa_largo / 2,
            "SIN PISO 2 EXISTENTE\nregistrado",
            ha="center",
            va="center",
            fontsize=9,
            style="italic"
        )

    # Módulos proyectados en Piso 2. Se acomodan automáticamente sobre la
    # huella de referencia para visualizar si caben esquemáticamente.
    modulos_piso2 = [
        modulo
        for modulo in modulos
        if modulo.get("piso") == "Piso 2"
        and float(modulo.get("superficie", 0) or 0) > 0
    ]

    validaciones = []
    cursor_x = casa_x
    cursor_y = casa_y
    alto_fila = 0.0
    separacion = max(min(ancho_terreno, largo_terreno) * 0.01, 0.10)

    for modulo in modulos_piso2:
        numero = modulo.get("numero", "")
        modulo_ancho = float(modulo.get("ancho", 0) or 0)
        modulo_largo = float(modulo.get("largo", 0) or 0)

        # Si el módulo no cabe horizontalmente en la fila, inicia una nueva.
        if cursor_x + modulo_ancho > casa_x + casa_ancho + 1e-9:
            cursor_x = casa_x
            cursor_y += alto_fila + separacion
            alto_fila = 0.0

        x = cursor_x
        y = cursor_y

        dentro_huella = (
            x >= casa_x - 1e-9
            and y >= casa_y - 1e-9
            and (x + modulo_ancho) <= casa_x + casa_ancho + 1e-9
            and (y + modulo_largo) <= casa_y + casa_largo + 1e-9
        )

        color_modulo = "#f8c471" if dentro_huella else "#f1948a"
        borde_modulo = "#935116" if dentro_huella else "#922b21"

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

        if dentro_huella:
            mensaje = (
                "El módulo cabe dentro de la huella aproximada utilizada como referencia. "
                "Debe verificarse estructuralmente su ubicación real."
            )
        else:
            mensaje = (
                "El módulo no cabe completamente dentro de la huella aproximada de referencia "
                "con esta disposición automática."
            )

        validaciones.append(
            {
                "numero": numero,
                "cumple": dentro_huella,
                "mensaje": mensaje
            }
        )

        cursor_x += modulo_ancho + separacion
        alto_fila = max(alto_fila, modulo_largo)

    margen_cota = max(min(ancho_terreno, largo_terreno) * 0.06, 0.6)

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

    leyenda = [
        Patch(facecolor="#85c1e9", edgecolor="#1b4f72", label="Piso 2 existente (aprox.)"),
        Patch(facecolor="#ebedef", edgecolor="#5d6d7e", label="Huella Piso 1 de referencia"),
        Patch(facecolor="#f8c471", edgecolor="#935116", label="Ampliación Piso 2 en referencia"),
        Patch(facecolor="#f1948a", edgecolor="#922b21", label="Módulo fuera de referencia")
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
    ax.set_ylim(-alto_calle - margen_cota * 0.4, largo_terreno + margen_cota * 1.7)
    ax.axis("off")
    ax.set_title(
        "Croquis Preliminar de Emplazamiento – Piso 2",
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
# EDITOR TIPO PUZLE - FUNCIONES AUXILIARES
# ==========================================
def obtener_geometria_referencia(datos):
    """Devuelve la geometría base utilizada por los croquis y el editor."""

    ancho_terreno = float(datos.get("ancho_terreno", 0) or 0)
    largo_terreno = float(datos.get("largo_terreno", 0) or 0)

    izquierda = (
        0.0
        if datos.get("adosado_izquierdo", False)
        else float(datos.get("distancia_izquierda", 0) or 0)
    )
    derecha = (
        0.0
        if datos.get("adosado_derecho", False)
        else float(datos.get("distancia_derecha", 0) or 0)
    )
    posterior = (
        0.0
        if datos.get("adosado_posterior", False)
        else float(datos.get("distancia_posterior", 0) or 0)
    )
    antejardin = float(datos.get("antejardin_actual", 0) or 0)
    antejardin_minimo = calcular_antejardin_referencia(datos)

    casa_x = izquierda
    casa_y = antejardin
    casa_ancho = ancho_terreno - izquierda - derecha
    casa_largo = largo_terreno - antejardin - posterior

    if casa_ancho <= 0 or casa_largo <= 0:
        superficie_p1 = max(float(datos.get("superficie_piso1", 0) or 0), 1.0)
        casa_ancho = min(ancho_terreno * 0.60, max(1.0, ancho_terreno - 0.5))
        casa_largo = min(
            largo_terreno * 0.55,
            max(1.0, superficie_p1 / casa_ancho)
        )
        casa_x = max((ancho_terreno - casa_ancho) / 2, 0)
        casa_y = min(max(antejardin, 0), max(largo_terreno - casa_largo, 0))

    return {
        "ancho_terreno": ancho_terreno,
        "largo_terreno": largo_terreno,
        "antejardin": antejardin,
        "antejardin_minimo": antejardin_minimo,
        "casa_x": casa_x,
        "casa_y": casa_y,
        "casa_ancho": casa_ancho,
        "casa_largo": casa_largo,
    }


def clave_modulo_puzzle(modulo):
    piso = str(modulo.get("piso", "Piso 1")).replace(" ", "_")
    numero = modulo.get("numero", 0)
    return f"ampliacion_{piso}_modulo_{numero}"


def clave_sector_vivienda(piso, sector):
    piso_clave = str(piso).replace(" ", "_")
    numero = sector.get("numero", 0)
    return f"vivienda_{piso_clave}_sector_{numero}"


def calcular_posicion_inicial_puzzle(datos, modulo):
    """Calcula una posición inicial razonable para una ampliación."""

    g = obtener_geometria_referencia(datos)

    numero = int(modulo.get("numero", 1) or 1)
    piso = modulo.get("piso", "Piso 1")
    rotado = bool(modulo.get("rotado", False))

    ancho_modulo = float(modulo.get("ancho", 0) or 0)
    largo_modulo = float(modulo.get("largo", 0) or 0)

    if rotado:
        ancho_modulo, largo_modulo = largo_modulo, ancho_modulo

    separacion = max(min(g["ancho_terreno"], g["largo_terreno"]) * 0.015, 0.15)
    desplazamiento = (numero - 1) * separacion

    if piso == "Piso 2":
        x = g["casa_x"] + desplazamiento
        y = g["casa_y"] + desplazamiento
    else:
        ubicacion = modulo.get("ubicacion", "")

        if ubicacion == "Lado izquierdo de la vivienda":
            x = g["casa_x"] - ancho_modulo
            y = g["casa_y"] + desplazamiento

        elif ubicacion == "Lado derecho de la vivienda":
            x = g["casa_x"] + g["casa_ancho"]
            y = g["casa_y"] + desplazamiento

        elif ubicacion == "Parte posterior de la vivienda":
            x = g["casa_x"] + desplazamiento
            y = g["casa_y"] + g["casa_largo"]

        elif ubicacion == "Parte frontal de la vivienda (hacia la calle)":
            x = g["casa_x"] + desplazamiento
            y = g["casa_y"] - largo_modulo

        else:
            x = g["casa_x"]
            y = g["casa_y"]

    return {
        "x": float(x),
        "y": float(y),
        "rotado": rotado,
    }


def calcular_posiciones_iniciales_vivienda(datos, piso):
    """
    Distribuye los sectores existentes inicialmente dentro de la envolvente
    aproximada. Luego el usuario puede moverlos para reproducir la forma real.
    """

    g = obtener_geometria_referencia(datos)
    clave_lista = "sectores_piso1" if piso == "Piso 1" else "sectores_piso2"
    sectores = [
        s for s in datos.get(clave_lista, [])
        if float(s.get("superficie", 0) or 0) > 0
    ]

    posiciones = {}
    cursor_x = g["casa_x"]
    cursor_y = g["casa_y"]
    alto_fila = 0.0
    separacion = 0.0

    for sector in sectores:
        ancho = float(sector.get("ancho", 0) or 0)
        largo = float(sector.get("largo", 0) or 0)

        if ancho <= 0 or largo <= 0:
            continue

        if (
            cursor_x > g["casa_x"]
            and cursor_x + ancho > g["casa_x"] + g["casa_ancho"] + 1e-9
        ):
            cursor_x = g["casa_x"]
            cursor_y += alto_fila + separacion
            alto_fila = 0.0

        if cursor_y + largo > g["largo_terreno"]:
            cursor_y = max(g["casa_y"], g["largo_terreno"] - largo)

        clave = clave_sector_vivienda(piso, sector)
        posiciones[clave] = {
            "x": float(cursor_x),
            "y": float(cursor_y),
            "rotado": False,
        }

        cursor_x += ancho + separacion
        alto_fila = max(alto_fila, largo)

    return posiciones


def asegurar_posiciones_puzzle(datos, modulos):
    """Inicializa ampliaciones nuevas sin borrar posiciones ya editadas."""

    posiciones = {
        k: dict(v)
        for k, v in st.session_state.posiciones_puzzle.items()
    }

    for modulo in modulos:
        if float(modulo.get("superficie", 0) or 0) <= 0:
            continue

        clave = clave_modulo_puzzle(modulo)

        if clave not in posiciones:
            posiciones[clave] = calcular_posicion_inicial_puzzle(datos, modulo)

    st.session_state.posiciones_puzzle = posiciones


def asegurar_posiciones_vivienda(datos):
    """Inicializa sectores existentes de ambos pisos sin borrar cambios."""

    posiciones = {
        k: dict(v)
        for k, v in st.session_state.posiciones_vivienda.items()
    }

    for piso in ["Piso 1", "Piso 2"]:
        iniciales = calcular_posiciones_iniciales_vivienda(datos, piso)
        for clave, valor in iniciales.items():
            if clave not in posiciones:
                posiciones[clave] = valor

    st.session_state.posiciones_vivienda = posiciones


def dimensiones_pieza(objeto, posicion):
    ancho = float(objeto.get("ancho", 0) or 0)
    largo = float(objeto.get("largo", 0) or 0)

    if bool(posicion.get("rotado", False)):
        ancho, largo = largo, ancho

    return ancho, largo


def construir_lista_piezas(datos, modulos, piso):
    """Construye una lista común de vivienda existente y ampliaciones."""

    piezas = []
    clave_lista = "sectores_piso1" if piso == "Piso 1" else "sectores_piso2"

    for sector in datos.get(clave_lista, []):
        if float(sector.get("superficie", 0) or 0) <= 0:
            continue

        clave = clave_sector_vivienda(piso, sector)
        posicion = st.session_state.posiciones_vivienda.get(clave)
        if posicion is None:
            continue

        ancho, largo = dimensiones_pieza(sector, posicion)
        piezas.append({
            "clave": clave,
            "tipo": "vivienda",
            "numero": sector.get("numero", ""),
            "piso": piso,
            "objeto": sector,
            "x": float(posicion.get("x", 0) or 0),
            "y": float(posicion.get("y", 0) or 0),
            "ancho": ancho,
            "largo": largo,
            "rotado": bool(posicion.get("rotado", False)),
        })

    for modulo in modulos:
        if modulo.get("piso") != piso:
            continue
        if float(modulo.get("superficie", 0) or 0) <= 0:
            continue

        clave = clave_modulo_puzzle(modulo)
        posicion = st.session_state.posiciones_puzzle.get(clave)
        if posicion is None:
            continue

        ancho, largo = dimensiones_pieza(modulo, posicion)
        piezas.append({
            "clave": clave,
            "tipo": "ampliacion",
            "numero": modulo.get("numero", ""),
            "piso": piso,
            "objeto": modulo,
            "x": float(posicion.get("x", 0) or 0),
            "y": float(posicion.get("y", 0) or 0),
            "ancho": ancho,
            "largo": largo,
            "rotado": bool(posicion.get("rotado", False)),
        })

    return piezas


def rectangulos_superpuestos(a, b, tolerancia=1e-6):
    """True cuando dos piezas tienen un área común real; tocar bordes no cuenta."""

    return not (
        a["x"] + a["ancho"] <= b["x"] + tolerancia
        or b["x"] + b["ancho"] <= a["x"] + tolerancia
        or a["y"] + a["largo"] <= b["y"] + tolerancia
        or b["y"] + b["largo"] <= a["y"] + tolerancia
    )


def mover_pieza_unificada(clave, tipo, dx=0.0, dy=0.0):
    nombre_estado = "posiciones_vivienda" if tipo == "vivienda" else "posiciones_puzzle"
    posiciones = {
        k: dict(v)
        for k, v in st.session_state[nombre_estado].items()
    }

    if clave not in posiciones:
        return

    posiciones[clave]["x"] = float(posiciones[clave].get("x", 0)) + float(dx)
    posiciones[clave]["y"] = float(posiciones[clave].get("y", 0)) + float(dy)
    st.session_state[nombre_estado] = posiciones


def rotar_pieza_unificada(clave, tipo):
    nombre_estado = "posiciones_vivienda" if tipo == "vivienda" else "posiciones_puzzle"
    posiciones = {
        k: dict(v)
        for k, v in st.session_state[nombre_estado].items()
    }

    if clave not in posiciones:
        return

    posiciones[clave]["rotado"] = not bool(posiciones[clave].get("rotado", False))
    st.session_state[nombre_estado] = posiciones


def reiniciar_pieza_unificada(datos, objeto, piso, tipo):
    if tipo == "ampliacion":
        clave = clave_modulo_puzzle(objeto)
        posiciones = {
            k: dict(v)
            for k, v in st.session_state.posiciones_puzzle.items()
        }
        posiciones[clave] = calcular_posicion_inicial_puzzle(datos, objeto)
        st.session_state.posiciones_puzzle = posiciones
    else:
        clave = clave_sector_vivienda(piso, objeto)
        iniciales = calcular_posiciones_iniciales_vivienda(datos, piso)
        if clave in iniciales:
            posiciones = {
                k: dict(v)
                for k, v in st.session_state.posiciones_vivienda.items()
            }
            posiciones[clave] = iniciales[clave]
            st.session_state.posiciones_vivienda = posiciones


def reiniciar_piso_vivienda(datos, piso):
    iniciales = calcular_posiciones_iniciales_vivienda(datos, piso)
    posiciones = {
        k: dict(v)
        for k, v in st.session_state.posiciones_vivienda.items()
    }

    prefijo = f"vivienda_{piso.replace(' ', '_')}_sector_"
    posiciones = {
        k: v for k, v in posiciones.items()
        if not k.startswith(prefijo)
    }
    posiciones.update(iniciales)
    st.session_state.posiciones_vivienda = posiciones


def pieza_dentro_terreno(pieza, g):
    return (
        pieza["x"] >= -1e-9
        and pieza["y"] >= -1e-9
        and pieza["x"] + pieza["ancho"] <= g["ancho_terreno"] + 1e-9
        and pieza["y"] + pieza["largo"] <= g["largo_terreno"] + 1e-9
    )


def aplicar_encaje_magnetico(datos, modulos, piso, clave, tipo, umbral=0.50):
    """
    Encaja una pieza por proximidad REAL de sus bordes.

    A diferencia de la versión anterior, no exige que la pieza esté alineada
    simultáneamente en X e Y para detectar un borde cercano. Si las proyecciones
    de dos rectángulos se solapan en el eje perpendicular, basta con acercar un
    borde al otro para que se produzca el encaje.
    """

    g = obtener_geometria_referencia(datos)
    piezas = construir_lista_piezas(datos, modulos, piso)
    seleccionada = next((p for p in piezas if p["clave"] == clave), None)

    if seleccionada is None:
        return False

    actual_x = float(seleccionada["x"])
    actual_y = float(seleccionada["y"])
    w = float(seleccionada["ancho"])
    h = float(seleccionada["largo"])

    candidatos = []

    def agregar(cx, cy, distancia, motivo):
        if distancia <= umbral + 1e-9:
            candidatos.append((float(distancia), float(cx), float(cy), motivo))

    # 1) Bordes laterales y posterior del terreno.
    agregar(0.0, actual_y, abs(actual_x), "deslinde izquierdo del terreno")
    agregar(
        g["ancho_terreno"] - w,
        actual_y,
        abs((actual_x + w) - g["ancho_terreno"]),
        "deslinde derecho del terreno"
    )
    agregar(
        actual_x,
        g["largo_terreno"] - h,
        abs((actual_y + h) - g["largo_terreno"]),
        "deslinde posterior del terreno"
    )

    # En Piso 1, una futura ampliación se encaja hacia la línea mínima de antejardín,
    # no hacia el borde de calle cuando eso significaría invadir el antejardín.
    if piso == "Piso 1" and tipo == "ampliacion":
        y_frente = float(g.get("antejardin_minimo", 0.0))
        agregar(actual_x, y_frente, abs(actual_y - y_frente), "línea mínima de antejardín")
    else:
        agregar(actual_x, 0.0, abs(actual_y), "frente del terreno")

    # 2) Encaje con vivienda existente u otros módulos.
    for otra in piezas:
        if otra["clave"] == clave:
            continue

        ox, oy = float(otra["x"]), float(otra["y"])
        ow, oh = float(otra["ancho"]), float(otra["largo"])

        # Solape de las proyecciones. Un pequeño margen permite encajar también
        # cuando las esquinas están apenas separadas.
        solape_vertical = min(actual_y + h, oy + oh) - max(actual_y, oy)
        solape_horizontal = min(actual_x + w, ox + ow) - max(actual_x, ox)

        if solape_vertical >= -umbral:
            # Borde derecho de la seleccionada con borde izquierdo de la otra.
            target_x = ox - w
            agregar(target_x, actual_y, abs((actual_x + w) - ox), "borde izquierdo de otra pieza")

            # Borde izquierdo de la seleccionada con borde derecho de la otra.
            target_x = ox + ow
            agregar(target_x, actual_y, abs(actual_x - (ox + ow)), "borde derecho de otra pieza")

        if solape_horizontal >= -umbral:
            # Borde superior de seleccionada con borde inferior de otra.
            target_y = oy - h
            agregar(actual_x, target_y, abs((actual_y + h) - oy), "borde frontal de otra pieza")

            # Borde inferior de seleccionada con borde superior de otra.
            target_y = oy + oh
            agregar(actual_x, target_y, abs(actual_y - (oy + oh)), "borde posterior de otra pieza")

        # Alineaciones auxiliares de caras cuando ya están casi lado a lado.
        if solape_vertical >= -umbral:
            agregar(ox, actual_y, abs(actual_x - ox), "alineación lateral")
            agregar(ox + ow - w, actual_y, abs((actual_x + w) - (ox + ow)), "alineación lateral")
        if solape_horizontal >= -umbral:
            agregar(actual_x, oy, abs(actual_y - oy), "alineación frontal/posterior")
            agregar(actual_x, oy + oh - h, abs((actual_y + h) - (oy + oh)), "alineación frontal/posterior")

    # Se prueba desde el borde más cercano al más lejano.
    candidatos.sort(key=lambda item: item[0])

    for distancia, cx, cy, motivo in candidatos:
        candidata = dict(seleccionada)
        candidata["x"] = cx
        candidata["y"] = cy

        if not pieza_dentro_terreno(candidata, g):
            continue

        if (
            tipo == "ampliacion"
            and piso == "Piso 1"
            and cy < float(g.get("antejardin_minimo", 0.0)) - 1e-9
        ):
            continue

        # No encajar en una posición que se monte sobre otra pieza.
        colision = False
        for otra in piezas:
            if otra["clave"] == clave:
                continue
            if rectangulos_superpuestos(candidata, otra):
                colision = True
                break

        if colision:
            continue

        nombre_estado = "posiciones_vivienda" if tipo == "vivienda" else "posiciones_puzzle"
        posiciones = {
            k: dict(v)
            for k, v in st.session_state[nombre_estado].items()
        }
        posiciones[clave]["x"] = float(cx)
        posiciones[clave]["y"] = float(cy)
        st.session_state[nombre_estado] = posiciones
        st.session_state["ultimo_encaje_puzzle"] = motivo
        return True

    return False


def validar_piezas_puzzle(datos, modulos, piso):
    g = obtener_geometria_referencia(datos)
    piezas = construir_lista_piezas(datos, modulos, piso)
    resultados = []

    for pieza in piezas:
        errores = []
        avisos = []

        if not pieza_dentro_terreno(pieza, g):
            errores.append("sale fuera del terreno")

        if pieza["tipo"] == "ampliacion" and piso == "Piso 1":
            if pieza["y"] < g.get("antejardin_minimo", 0.0) - 1e-9:
                errores.append("invade el antejardín mínimo de referencia")

        if pieza["tipo"] == "ampliacion" and piso == "Piso 2":
            dentro_huella_referencia = (
                pieza["x"] >= g["casa_x"] - 1e-9
                and pieza["y"] >= g["casa_y"] - 1e-9
                and pieza["x"] + pieza["ancho"] <= g["casa_x"] + g["casa_ancho"] + 1e-9
                and pieza["y"] + pieza["largo"] <= g["casa_y"] + g["casa_largo"] + 1e-9
            )
            if not dentro_huella_referencia:
                avisos.append(
                    "se proyecta fuera de la huella aproximada del Piso 1; requiere revisión estructural"
                )

        superposiciones = []
        for otra in piezas:
            if otra["clave"] == pieza["clave"]:
                continue
            if rectangulos_superpuestos(pieza, otra):
                etiqueta = (
                    f"sector existente {otra['numero']}"
                    if otra["tipo"] == "vivienda"
                    else f"módulo de ampliación {otra['numero']}"
                )
                superposiciones.append(etiqueta)

        if superposiciones:
            errores.append("se superpone con " + ", ".join(sorted(set(superposiciones))))

        if errores:
            nivel = "error"
            mensaje = "La pieza " + "; ".join(errores) + "."
        elif avisos:
            nivel = "warning"
            mensaje = "La pieza está dentro del terreno, pero " + "; ".join(avisos) + "."
        else:
            nivel = "ok"
            if pieza["tipo"] == "vivienda":
                mensaje = "Sector de vivienda existente ubicado dentro del terreno sin superposición."
            else:
                mensaje = "Módulo de ampliación ubicado sin superposición y dentro de los límites preliminares."

        resultados.append({
            **pieza,
            "nivel": nivel,
            "cumple": nivel != "error",
            "mensaje": mensaje,
        })

    return resultados


def crear_croquis_puzzle(datos, modulos, piso, modulo_seleccionado=None):
    """
    Dibuja vivienda existente y futura ampliación usando posiciones editables.
    En Piso 2 muestra el Piso 1 como huella de referencia, pero permite ubicar
    libremente los sectores ya construidos del segundo piso.
    """

    g = obtener_geometria_referencia(datos)

    if g["ancho_terreno"] <= 0 or g["largo_terreno"] <= 0:
        return None, [], None

    fig, ax = plt.subplots(figsize=(7.2, 8.5))

    # Cuadrícula métrica.
    paso_grilla = 1.0
    x = 0.0
    while x <= g["ancho_terreno"] + 1e-9:
        ax.plot([x, x], [0, g["largo_terreno"]], linewidth=0.35, alpha=0.18, zorder=0)
        x += paso_grilla

    y = 0.0
    while y <= g["largo_terreno"] + 1e-9:
        ax.plot([0, g["ancho_terreno"]], [y, y], linewidth=0.35, alpha=0.18, zorder=0)
        y += paso_grilla

    ax.add_patch(
        Rectangle(
            (0, 0),
            g["ancho_terreno"],
            g["largo_terreno"],
            fill=False,
            linewidth=2.2,
            zorder=6
        )
    )

    alto_calle = max(g["largo_terreno"] * 0.07, 1.0)
    ax.add_patch(
        Rectangle(
            (0, -alto_calle),
            g["ancho_terreno"],
            alto_calle,
            alpha=0.22,
            zorder=0
        )
    )
    ax.text(
        g["ancho_terreno"] / 2,
        -alto_calle / 2,
        "CALLE / FRENTE",
        ha="center",
        va="center",
        fontsize=8,
        weight="bold"
    )

    if piso == "Piso 1" and 0 < g["antejardin"] < g["largo_terreno"]:
        ax.add_patch(
            Rectangle(
                (0, 0),
                g["ancho_terreno"],
                g["antejardin"],
                facecolor="#d5f5e3",
                alpha=0.30,
                zorder=0
            )
        )
        ax.text(
            g["ancho_terreno"] / 2,
            g["antejardin"] / 2,
            f"ANTEJARDÍN {g['antejardin']:.2f} m",
            ha="center",
            va="center",
            fontsize=7
        )

    # Piso 2: mostrar el Piso 1 únicamente como REFERENCIA FIJA.
    # Ni la vivienda ni las ampliaciones del Piso 1 entran en la lista editable
    # del Piso 2; por lo tanto, no pueden seleccionarse ni moverse desde esta vista.
    if piso == "Piso 2":
        piezas_piso1 = construir_lista_piezas(datos, modulos, "Piso 1")
        sectores_p1 = [p for p in piezas_piso1 if p["tipo"] == "vivienda"]
        ampliaciones_p1_ref = [p for p in piezas_piso1 if p["tipo"] == "ampliacion"]

        if sectores_p1:
            for pieza in sectores_p1:
                ax.add_patch(
                    Rectangle(
                        (pieza["x"], pieza["y"]),
                        pieza["ancho"],
                        pieza["largo"],
                        facecolor="#ebedef",
                        edgecolor="#7f8c8d",
                        linewidth=1.1,
                        linestyle="--",
                        alpha=0.42,
                        zorder=1
                    )
                )
        else:
            ax.add_patch(
                Rectangle(
                    (g["casa_x"], g["casa_y"]),
                    g["casa_ancho"],
                    g["casa_largo"],
                    fill=False,
                    edgecolor="#7f8c8d",
                    linewidth=1.2,
                    linestyle="--",
                    alpha=0.55,
                    zorder=1
                )
            )

        # Si ya existe una ampliación propuesta en Piso 1, también se muestra
        # como sombra para entender qué elemento puede servir de apoyo al Piso 2.
        # Se dibuja con baja opacidad y NO se incorpora a validaciones ni controles.
        for pieza in ampliaciones_p1_ref:
            ax.add_patch(
                Rectangle(
                    (pieza["x"], pieza["y"]),
                    pieza["ancho"],
                    pieza["largo"],
                    facecolor="#f8c471",
                    edgecolor="#b9770e",
                    linewidth=1.1,
                    linestyle="--",
                    alpha=0.28,
                    zorder=1
                )
            )
            ax.text(
                pieza["x"] + pieza["ancho"] / 2,
                pieza["y"] + pieza["largo"] / 2,
                f"AMPL. P1 {pieza['numero']}\nREFERENCIA FIJA",
                ha="center",
                va="center",
                fontsize=6,
                color="#7d6608",
                zorder=2
            )

        ax.text(
            g["casa_x"],
            max(g["casa_y"] - 0.25, 0),
            "Piso 1 = referencia fija (no editable desde Piso 2)",
            ha="left",
            va="top",
            fontsize=7,
            style="italic"
        )

    validaciones = validar_piezas_puzzle(datos, modulos, piso)

    # Primero vivienda existente, luego ampliaciones.
    for tipo in ["vivienda", "ampliacion"]:
        for revision in validaciones:
            if revision["tipo"] != tipo:
                continue

            seleccionado = revision["clave"] == modulo_seleccionado
            nivel = revision["nivel"]

            if tipo == "vivienda":
                facecolor = "#85c1e9" if piso == "Piso 1" else "#a9cce3"
                edgecolor_base = "#1b4f72"
            else:
                if nivel == "error":
                    facecolor = "#f1948a"
                    edgecolor_base = "#922b21"
                elif nivel == "warning":
                    facecolor = "#f9e79f"
                    edgecolor_base = "#9a7d0a"
                else:
                    facecolor = "#f8c471"
                    edgecolor_base = "#935116"

            edgecolor = "#6c3483" if seleccionado else edgecolor_base
            linewidth = 3.2 if seleccionado else 1.8

            ax.add_patch(
                Rectangle(
                    (revision["x"], revision["y"]),
                    revision["ancho"],
                    revision["largo"],
                    facecolor=facecolor,
                    edgecolor=edgecolor,
                    linewidth=linewidth,
                    alpha=0.88,
                    zorder=3 if tipo == "vivienda" else 4
                )
            )

            prefijo = "CASA" if tipo == "vivienda" else "AMPL."
            ax.text(
                revision["x"] + revision["ancho"] / 2,
                revision["y"] + revision["largo"] / 2,
                f"{prefijo} {revision['numero']}\n{revision['ancho']:.2f} × {revision['largo']:.2f} m",
                ha="center",
                va="center",
                fontsize=7,
                weight="bold",
                zorder=5
            )

    margen = max(min(g["ancho_terreno"], g["largo_terreno"]) * 0.05, 0.5)

    ax.text(
        g["ancho_terreno"] / 2,
        g["largo_terreno"] + margen * 0.20,
        "DESLINDE POSTERIOR",
        ha="center",
        va="bottom",
        fontsize=7
    )

    leyenda = [
        Patch(facecolor="#85c1e9", edgecolor="#1b4f72", label="Vivienda existente del piso editado"),
        Patch(facecolor="#f8c471", edgecolor="#935116", label="Futura ampliación del piso editado"),
        Patch(facecolor="#f9e79f", edgecolor="#9a7d0a", label="Requiere revisión"),
        Patch(facecolor="#f1948a", edgecolor="#922b21", label="Posición con conflicto"),
    ]
    if piso == "Piso 2":
        leyenda.append(
            Patch(
                facecolor="#f8c471",
                edgecolor="#b9770e",
                alpha=0.28,
                label="Ampliación Piso 1 (referencia fija)"
            )
        )

    ax.legend(
        handles=leyenda,
        loc="upper left",
        bbox_to_anchor=(1.01, 1.0),
        borderaxespad=0,
        fontsize=7
    )

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-margen, g["ancho_terreno"] + margen)
    ax.set_ylim(-alto_calle - margen * 0.2, g["largo_terreno"] + margen)
    ax.axis("off")
    ax.set_title(
        f"Editor tipo Puzle – {piso}",
        fontsize=12,
        weight="bold",
        pad=12
    )

    fig.tight_layout()

    buffer_png = BytesIO()
    fig.savefig(
        buffer_png,
        format="png",
        dpi=180,
        bbox_inches="tight"
    )
    buffer_png.seek(0)

    return fig, validaciones, buffer_png


def distancia_minima_oguc_263(altura_m, tiene_vano):
    """Distanciamiento mínimo de referencia según tabla del art. 2.6.3 OGUC."""
    altura = float(altura_m or 0)
    if altura <= 0:
        return None
    if altura <= 3.5:
        return 3.0 if tiene_vano else 1.4
    if altura <= 7.0:
        return 3.0 if tiene_vano else 2.5
    return 4.0


def altura_maxima_rasante_rm(distancia_m, angulo_grados=70.0):
    """
    Aproximación geométrica de rasante para la Región Metropolitana,
    suponiendo terreno horizontal y aplicación desde suelo natural.
    """
    distancia = max(float(distancia_m or 0), 0.0)
    return distancia * math.tan(math.radians(float(angulo_grados)))


def unir_longitudes_intervalos(intervalos, tolerancia=1e-9):
    """Longitud de la unión de intervalos 1D, evitando duplicar tramos superpuestos."""
    limpios = []
    for inicio, fin in intervalos:
        a = float(min(inicio, fin))
        b = float(max(inicio, fin))
        if b - a > tolerancia:
            limpios.append((a, b))
    if not limpios:
        return 0.0
    limpios.sort()
    total = 0.0
    ini, fin = limpios[0]
    for a, b in limpios[1:]:
        if a <= fin + tolerancia:
            fin = max(fin, b)
        else:
            total += fin - ini
            ini, fin = a, b
    total += fin - ini
    return float(total)


def obtener_intervalos_adosamiento_futuro(datos, modulos, tolerancia=0.05):
    """Devuelve los tramos de futura ampliación que contactan cada deslinde."""
    g = obtener_geometria_referencia(datos)
    intervalos = {"Izquierdo": [], "Derecho": [], "Posterior": []}

    for modulo in modulos:
        if float(modulo.get("superficie", 0) or 0) <= 0:
            continue
        clave = clave_modulo_puzzle(modulo)
        posicion = st.session_state.posiciones_puzzle.get(clave)
        if posicion is None:
            posicion = calcular_posicion_inicial_puzzle(datos, modulo)
        ancho, largo = dimensiones_pieza(modulo, posicion)
        x = float(posicion.get("x", 0) or 0)
        y = float(posicion.get("y", 0) or 0)

        if abs(x) <= tolerancia:
            intervalos["Izquierdo"].append((y, y + largo))
        if abs((x + ancho) - g["ancho_terreno"]) <= tolerancia:
            intervalos["Derecho"].append((y, y + largo))
        if abs((y + largo) - g["largo_terreno"]) <= tolerancia:
            intervalos["Posterior"].append((x, x + ancho))

    return intervalos


def obtener_intervalos_adosamiento_existente(datos, tolerancia=0.05):
    """
    Detecta desde el puzle los tramos de la vivienda existente que ya contactan
    los deslindes. Los sectores coincidentes entre Piso 1 y Piso 2 se unen y se
    contabilizan una sola vez.
    """
    g = obtener_geometria_referencia(datos)
    intervalos = {"Izquierdo": [], "Derecho": [], "Posterior": []}

    for piso in ["Piso 1", "Piso 2"]:
        clave_lista = "sectores_piso1" if piso == "Piso 1" else "sectores_piso2"
        for sector in datos.get(clave_lista, []):
            if float(sector.get("superficie", 0) or 0) <= 0:
                continue
            clave = clave_sector_vivienda(piso, sector)
            posicion = st.session_state.posiciones_vivienda.get(clave)
            if posicion is None:
                posicion = calcular_posiciones_iniciales_vivienda(datos, piso).get(clave)
            if posicion is None:
                continue
            ancho, largo = dimensiones_pieza(sector, posicion)
            x = float(posicion.get("x", 0) or 0)
            y = float(posicion.get("y", 0) or 0)

            if abs(x) <= tolerancia:
                intervalos["Izquierdo"].append((y, y + largo))
            if abs((x + ancho) - g["ancho_terreno"]) <= tolerancia:
                intervalos["Derecho"].append((y, y + largo))
            if abs((y + largo) - g["largo_terreno"]) <= tolerancia:
                intervalos["Posterior"].append((x, x + ancho))

    return intervalos


def calcular_adosamiento_futuro(datos, modulos, tolerancia=0.05):
    """Longitud futura por deslinde, sin duplicar tramos superpuestos entre pisos."""
    intervalos = obtener_intervalos_adosamiento_futuro(datos, modulos, tolerancia)
    return {lado: unir_longitudes_intervalos(tramos) for lado, tramos in intervalos.items()}



# ==========================================
# INFORME PDF PARA REVISIÓN PROFESIONAL
# ==========================================
def _limpiar_texto_pdf(valor):
    """Normaliza texto para las fuentes estándar de ReportLab."""
    if valor is None:
        return "-"
    texto = str(valor)
    reemplazos = {
        "✅": "OK -",
        "⚠️": "OBS -",
        "⚠": "OBS -",
        "❌": "REVISAR -",
        "🟨": "ADOSAMIENTO -",
        "🔥": "",
        "🧱": "",
        "🏠": "",
        "📐": "",
        "🚗": "",
        "📋": "",
        "⬛": "",
        "→": "->",
        "≤": "<=",
        "≥": ">=",
        "×": "x",
        "²": "2",
        "–": "-",
        "—": "-",
        "•": "-",
    }
    for a, b in reemplazos.items():
        texto = texto.replace(a, b)
    return " ".join(texto.split())


def _parrafo_pdf(texto, estilo):
    return Paragraph(html.escape(_limpiar_texto_pdf(texto)), estilo)


def _imagen_pdf_ajustada(origen, max_ancho, max_alto):
    """Crea una imagen Platypus manteniendo proporción."""
    try:
        if hasattr(origen, "getvalue"):
            contenido = origen.getvalue()
            fuente_lector = BytesIO(contenido)
            fuente_pdf = BytesIO(contenido)
        else:
            fuente_lector = origen
            fuente_pdf = origen

        lector = ImageReader(fuente_lector)
        ancho_px, alto_px = lector.getSize()
        if ancho_px <= 0 or alto_px <= 0:
            return None
        escala = min(float(max_ancho) / float(ancho_px), float(max_alto) / float(alto_px))
        ancho = ancho_px * escala
        alto = alto_px * escala
        return PDFImage(fuente_pdf, width=ancho, height=alto)
    except Exception:
        return None


def _tabla_datos_pdf(filas, estilo_celda, anchos=None, encabezado=False):
    data = []
    for fila in filas:
        data.append([_parrafo_pdf(celda, estilo_celda) for celda in fila])
    tabla = Table(data, colWidths=anchos, repeatRows=1 if encabezado else 0, hAlign='LEFT')
    estilo = [
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.35, colors.HexColor('#CDD6D2')),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]
    if encabezado and data:
        estilo += [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8F1EC')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#174B36')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]
    else:
        for i in range(len(data)):
            if i % 2 == 1:
                estilo.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F7F9F8')))
    tabla.setStyle(TableStyle(estilo))
    return tabla


def _filas_solucion_pdf(solucion, tipo):
    if not solucion:
        return [["Estado", "Pendiente / no seleccionada"]]

    if tipo == 'muro':
        campos = [
            ('Código', 'Codigo_Solucion'),
            ('Sistema', 'Sistema'),
            ('Estructura principal', 'Estructura_Principal'),
            ('Revestimiento interior', 'Revestimiento_Interior'),
            ('Barrera de vapor', 'Barrera_Vapor'),
            ('Aislación entre estructura', 'Aislante_Entre_Estructura'),
            ('Placa estructural', 'Placa_Estructural'),
            ('Aislación exterior', 'Aislacion_Exterior'),
            ('Barrera de humedad', 'Barrera_Humedad'),
            ('Revestimiento exterior', 'Revestimiento_Exterior'),
            ('Transmitancia U', 'U_W_m2K'),
            ('Resistencia térmica Rt', 'Rt_m2K_W'),
            ('Compatibilidad Zona D', 'Compatibilidad_Zona_D'),
            ('Resistencia al fuego', 'Resistencia_Fuego'),
            ('Uso especial', 'Uso_Especial'),
            ('Fuente', 'Fuente'),
            ('Fuente fuego', 'Fuente_Fuego'),
            ('Observación', 'Observacion'),
        ]
    elif tipo == 'piso':
        campos = [
            ('Código', 'Codigo_Solucion'),
            ('Condición', 'Condicion_Piso'),
            ('Sistema', 'Sistema'),
            ('Pavimento', 'Pavimento_Terminacion'),
            ('Placa estructural', 'Placa_Estructural'),
            ('Estructura principal', 'Estructura_Principal'),
            ('Aislante', 'Aislante'),
            ('Barrera humedad/viento', 'Barrera_Humedad_Viento'),
            ('Revestimiento inferior', 'Revestimiento_Inferior'),
            ('Cama de ripio', 'Cama_Ripio_mm'),
            ('Radier hormigón', 'Radier_Hormigon_mm'),
            ('R100 mínimo sobrecimiento', 'R100_Min_Sobrecimiento'),
            ('Transmitancia U', 'U_W_m2K'),
            ('Resistencia térmica Rt', 'Rt_m2K_W'),
            ('Compatibilidad Zona D', 'Compatibilidad_Zona_D'),
            ('Fuente', 'Fuente'),
            ('Observación', 'Observacion'),
        ]
    else:
        campos = [
            ('Código', 'Codigo_Solucion'),
            ('Sistema', 'Sistema'),
            ('Geometría', 'Geometria'),
            ('Cielo interior', 'Cielo_Interior'),
            ('Barrera de vapor', 'Barrera_Vapor'),
            ('Listoneado', 'Listoneado_Cielo'),
            ('Aislante', 'Aislante'),
            ('Estructura principal', 'Estructura_Principal'),
            ('Entretecho', 'Espacio_Entretecho'),
            ('Ventilación', 'Ventilacion_Entretecho'),
            ('Cubierta exterior', 'Cubierta_Exterior'),
            ('Transmitancia U', 'U_W_m2K'),
            ('Resistencia térmica Rt', 'Rt_m2K_W'),
            ('Compatibilidad Zona D', 'Compatibilidad_Zona_D'),
            ('Fuente', 'Fuente'),
            ('Observación', 'Observacion'),
        ]

    filas = []
    for etiqueta, clave in campos:
        valor = solucion.get(clave)
        if valor is None:
            continue
        try:
            if pd.isna(valor):
                continue
        except Exception:
            pass
        texto = str(valor).strip()
        if not texto or texto.lower() == 'nan':
            continue
        if clave in {'U_W_m2K', 'Rt_m2K_W'}:
            try:
                texto = f"{float(valor):.2f}"
            except Exception:
                pass
        elif clave in {'Cama_Ripio_mm', 'Radier_Hormigon_mm'}:
            try:
                texto = f"{float(valor):.0f} mm"
            except Exception:
                pass
        filas.append([etiqueta, texto])
    return filas or [["Información", "Sin antecedentes adicionales"]]


def _clave_imagen_piso_pdf(solucion):
    if not solucion:
        return None
    codigo = str(solucion.get('Codigo_Solucion', '') or '').lower()
    sistema = str(solucion.get('Sistema', '') or '').lower()
    condicion = str(solucion.get('Condicion_Piso', '') or '').lower()
    if 'radier' in codigo or 'radier' in sistema or 'terreno' in condicion:
        return 'piso_radier'
    if 'pv' in codigo or 'ventil' in sistema or 'ventil' in condicion:
        return 'piso_ventilado'
    return None


def _encabezado_pagina_pdf(canvas, doc):
    canvas.saveState()
    w, h = A4
    verde = colors.HexColor('#1E7B44')
    azul = colors.HexColor('#23445C')

    # Logo vectorial propio del prototipo: casa + bloques.
    x0, y0 = 18 * mm, h - 22 * mm
    canvas.setFillColor(verde)
    canvas.roundRect(x0, y0, 17 * mm, 12 * mm, 2.2 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.rect(x0 + 4.0 * mm, y0 + 2.5 * mm, 8.5 * mm, 5.5 * mm, fill=0, stroke=1)
    canvas.line(x0 + 3.2 * mm, y0 + 8.0 * mm, x0 + 8.3 * mm, y0 + 10.7 * mm)
    canvas.line(x0 + 8.3 * mm, y0 + 10.7 * mm, x0 + 13.4 * mm, y0 + 8.0 * mm)
    canvas.rect(x0 + 5.4 * mm, y0 + 3.0 * mm, 2.0 * mm, 3.0 * mm, fill=1, stroke=0)

    canvas.setFillColor(azul)
    canvas.setFont('Helvetica-Bold', 11)
    canvas.drawString(39 * mm, h - 14.2 * mm, 'VALIDADOR NORMATIVO DE AMPLIACIONES')
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(colors.HexColor('#5B6B64'))
    canvas.drawString(39 * mm, h - 18.2 * mm, 'Prototipo de apoyo preliminar - Caso de estudio: San Miguel')
    canvas.setStrokeColor(colors.HexColor('#B9C7C0'))
    canvas.line(18 * mm, h - 25 * mm, w - 18 * mm, h - 25 * mm)

    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(colors.HexColor('#68746F'))
    canvas.drawString(18 * mm, 10 * mm, 'Documento orientativo generado por el prototipo. Requiere revisión profesional y municipal.')
    canvas.drawRightString(w - 18 * mm, 10 * mm, f'Página {doc.page}')
    canvas.restoreState()


def generar_informe_pdf_futura_ampliacion(datos, propuesta):
    """Genera un informe PDF preliminar de la futura ampliación para revisión profesional."""
    if not REPORTLAB_DISPONIBLE:
        return None

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=31 * mm,
        bottomMargin=18 * mm,
        title='Informe preliminar de futura ampliación',
        author='Validador Normativo de Ampliaciones',
    )

    estilos_base = getSampleStyleSheet()
    estilos = {
        'titulo': ParagraphStyle(
            'TituloInforme', parent=estilos_base['Title'], fontName='Helvetica-Bold',
            fontSize=17, leading=20, textColor=colors.HexColor('#23445C'), spaceAfter=4,
            alignment=TA_CENTER,
        ),
        'subtitulo': ParagraphStyle(
            'SubtituloInforme', parent=estilos_base['Normal'], fontName='Helvetica',
            fontSize=9.5, leading=13, textColor=colors.HexColor('#5B6B64'), spaceAfter=12,
            alignment=TA_CENTER,
        ),
        'h1': ParagraphStyle(
            'Seccion', parent=estilos_base['Heading2'], fontName='Helvetica-Bold',
            fontSize=12.5, leading=15, textColor=colors.HexColor('#1E7B44'),
            spaceBefore=10, spaceAfter=6,
        ),
        'h2': ParagraphStyle(
            'Subseccion', parent=estilos_base['Heading3'], fontName='Helvetica-Bold',
            fontSize=10.5, leading=13, textColor=colors.HexColor('#23445C'),
            spaceBefore=7, spaceAfter=4,
        ),
        'normal': ParagraphStyle(
            'NormalInforme', parent=estilos_base['Normal'], fontName='Helvetica',
            fontSize=8.5, leading=11.2, textColor=colors.HexColor('#25332D'), spaceAfter=4,
        ),
        'small': ParagraphStyle(
            'SmallInforme', parent=estilos_base['Normal'], fontName='Helvetica',
            fontSize=7.3, leading=9.4, textColor=colors.HexColor('#25332D'),
        ),
        'nota': ParagraphStyle(
            'NotaInforme', parent=estilos_base['Normal'], fontName='Helvetica-Oblique',
            fontSize=7.5, leading=10, textColor=colors.HexColor('#5B6B64'),
            leftIndent=5, rightIndent=5, spaceBefore=4, spaceAfter=6,
        ),
    }

    story = []
    story.append(_parrafo_pdf('INFORME PRELIMINAR PARA REVISIÓN PROFESIONAL', estilos['titulo']))
    story.append(_parrafo_pdf('Futura ampliación domiciliaria - San Miguel', estilos['subtitulo']))

    fecha = datetime.now().strftime('%d-%m-%Y %H:%M')
    cabecera = [
        ['Fecha de emisión', fecha],
        ['Dirección informada', datos.get('direccion') or 'No informada'],
        ['Zona PRC', datos.get('zona_completa') or datos.get('zona_codigo') or 'No informada'],
        ['Resultado global', propuesta.get('resultado_global') or 'No evaluado'],
    ]
    story.append(_tabla_datos_pdf(cabecera, estilos['small'], anchos=[43 * mm, 124 * mm]))
    story.append(Spacer(1, 5 * mm))
    story.append(_parrafo_pdf(
        'Este documento resume los antecedentes ingresados al prototipo y sus verificaciones automatizadas. '
        'No constituye permiso de edificación, aprobación de la Dirección de Obras Municipales ni certificación '
        'estructural, térmica o de resistencia al fuego.', estilos['nota']))

    # 1. Datos del predio y vivienda existente
    story.append(_parrafo_pdf('1. Datos del predio y vivienda existente', estilos['h1']))
    filas_predio = [
        ['Superficie del terreno', f"{float(datos.get('superficie_terreno', 0) or 0):.2f} m2"],
        ['Dimensiones del terreno', f"{float(datos.get('ancho_terreno', 0) or 0):.2f} m x {float(datos.get('largo_terreno', 0) or 0):.2f} m"],
        ['Frente predial', f"{float(datos.get('frente_predio', 0) or 0):.2f} m"],
        ['Vía que enfrenta', datos.get('via_frente') or 'No informada'],
        ['Superficie existente Piso 1', f"{float(datos.get('superficie_piso1', 0) or 0):.2f} m2"],
        ['Superficie existente Piso 2', f"{float(datos.get('superficie_piso2', 0) or 0):.2f} m2"],
        ['Superficie total existente', f"{float(datos.get('superficie_total_vivienda', 0) or 0):.2f} m2"],
        ['Antejardín informado', f"{float(datos.get('antejardin_actual', 0) or 0):.2f} m"],
        ['Deslinde izquierdo', 'Adosado' if datos.get('adosado_izquierdo') else f"{float(datos.get('distancia_izquierda', 0) or 0):.2f} m"],
        ['Deslinde derecho', 'Adosado' if datos.get('adosado_derecho') else f"{float(datos.get('distancia_derecha', 0) or 0):.2f} m"],
        ['Deslinde posterior', 'Adosado' if datos.get('adosado_posterior') else f"{float(datos.get('distancia_posterior', 0) or 0):.2f} m"],
    ]
    story.append(_tabla_datos_pdf(filas_predio, estilos['small'], anchos=[57 * mm, 110 * mm]))

    story.append(_parrafo_pdf('Parámetros urbanísticos utilizados', estilos['h2']))
    filas_urbanas = [
        ['Coeficiente de ocupación', f"{float(datos.get('coef_ocupacion')):.2f}" if datos.get('coef_ocupacion') is not None else 'No disponible'],
        ['Coeficiente de constructibilidad', f"{float(datos.get('coef_constructibilidad')):.2f}" if datos.get('coef_constructibilidad') is not None else 'No disponible'],
        ['Máxima ocupación preliminar', f"{float(datos.get('superficie_maxima_ocupacion')):.2f} m2" if datos.get('superficie_maxima_ocupacion') is not None else 'No disponible'],
        ['Máxima superficie construible', f"{float(datos.get('superficie_maxima_construible')):.2f} m2" if datos.get('superficie_maxima_construible') is not None else 'No disponible'],
    ]
    story.append(_tabla_datos_pdf(filas_urbanas, estilos['small'], anchos=[57 * mm, 110 * mm]))

    # 2. Propuesta
    story.append(_parrafo_pdf('2. Futura ampliación propuesta', estilos['h1']))
    filas_sup = [
        ['Ampliación Piso 1', f"{float(propuesta.get('superficie_ampliacion_piso1', 0) or 0):.2f} m2"],
        ['Ampliación Piso 2', f"{float(propuesta.get('superficie_ampliacion_piso2', 0) or 0):.2f} m2"],
        ['Ampliación total', f"{float(propuesta.get('superficie_total_ampliacion', 0) or 0):.2f} m2"],
        ['Piso 1 proyectado', f"{float(propuesta.get('piso1_proyectado', 0) or 0):.2f} m2"],
        ['Piso 2 proyectado', f"{float(propuesta.get('piso2_proyectado', 0) or 0):.2f} m2"],
        ['Vivienda total proyectada', f"{float(propuesta.get('vivienda_total_proyectada', 0) or 0):.2f} m2"],
    ]
    story.append(_tabla_datos_pdf(filas_sup, estilos['small'], anchos=[57 * mm, 110 * mm]))

    rev_mods = {}
    for r in propuesta.get('revision_emplazamiento', {}).get('modulos', []):
        rev_mods[(r.get('numero'), r.get('piso'))] = r
    filas_modulos = [['Módulo', 'Piso', 'Dimensiones', 'Superficie', 'Ubicación', 'Altura']]
    for m in propuesta.get('modulos', []):
        rev = rev_mods.get((m.get('numero'), m.get('piso')), {})
        altura = rev.get('altura_total_m')
        filas_modulos.append([
            str(m.get('numero', '')),
            m.get('piso', ''),
            f"{float(m.get('largo', 0) or 0):.2f} x {float(m.get('ancho', 0) or 0):.2f} m",
            f"{float(m.get('superficie', 0) or 0):.2f} m2",
            m.get('ubicacion', ''),
            f"{float(altura):.2f} m" if altura is not None else 'Pendiente',
        ])
    story.append(Spacer(1, 2 * mm))
    story.append(_tabla_datos_pdf(
        filas_modulos, estilos['small'], encabezado=True,
        anchos=[12 * mm, 20 * mm, 30 * mm, 23 * mm, 58 * mm, 24 * mm]
    ))

    # Croquis del puzle guardado
    story.append(_parrafo_pdf('Croquis de emplazamiento guardado', estilos['h2']))
    posiciones_puzzle_original = dict(st.session_state.get('posiciones_puzzle', {}))
    posiciones_vivienda_original = dict(st.session_state.get('posiciones_vivienda', {}))
    try:
        st.session_state.posiciones_puzzle = {
            k: dict(v) for k, v in propuesta.get('posiciones_puzzle', {}).items()
        }
        st.session_state.posiciones_vivienda = {
            k: dict(v) for k, v in propuesta.get('posiciones_vivienda', {}).items()
        }
        pisos_reporte = ['Piso 1']
        if float(propuesta.get('superficie_ampliacion_piso2', 0) or 0) > 0 or bool(datos.get('tiene_piso2')):
            pisos_reporte.append('Piso 2')
        for piso_rep in pisos_reporte:
            fig_rep, _, img_rep = crear_croquis_puzzle(datos, propuesta.get('modulos', []), piso_rep)
            if img_rep is not None:
                bytes_img = img_rep.getvalue()
                img_pdf = _imagen_pdf_ajustada(BytesIO(bytes_img), 155 * mm, 105 * mm)
                if img_pdf is not None:
                    story.append(_parrafo_pdf(piso_rep, estilos['h2']))
                    story.append(img_pdf)
                    story.append(Spacer(1, 2 * mm))
            if fig_rep is not None:
                plt.close(fig_rep)
    except Exception as exc:
        story.append(_parrafo_pdf(f'Croquis no disponible en el informe: {exc}', estilos['nota']))
    finally:
        st.session_state.posiciones_puzzle = posiciones_puzzle_original
        st.session_state.posiciones_vivienda = posiciones_vivienda_original

    # 3. Revisión normativa
    story.append(PageBreak())
    story.append(_parrafo_pdf('3. Resumen de verificaciones preliminares', estilos['h1']))
    filas_resumen = [['Área revisada', 'Estado', 'Detalle']]
    for fila in propuesta.get('resumen_final', []):
        filas_resumen.append([
            fila.get('Área revisada', ''),
            fila.get('Estado', ''),
            fila.get('Detalle', ''),
        ])
    story.append(_tabla_datos_pdf(
        filas_resumen, estilos['small'], encabezado=True,
        anchos=[37 * mm, 38 * mm, 92 * mm]
    ))

    # Detalle de vanos, distancias y rasante
    story.append(_parrafo_pdf('Altura, vanos, distanciamientos y rasante', estilos['h2']))
    for r in propuesta.get('revision_emplazamiento', {}).get('modulos', []):
        story.append(_parrafo_pdf(
            f"Módulo {r.get('numero')} - {r.get('piso')} - altura declarada: {float(r.get('altura_total_m', 0) or 0):.2f} m",
            estilos['normal']))
        filas_lados = [['Deslinde', 'Distancia', 'Vano', 'Mínimo', 'Rasante aprox.', 'Resultado']]
        for lado in r.get('resultados_lados', []):
            dist = lado.get('distancia')
            minimo = lado.get('distancia_minima')
            hmax = lado.get('altura_maxima_rasante_aprox')
            if lado.get('tipo') == 'adosado':
                minimo_txt = 'Adosamiento'
                hmax_txt = 'No aplica a tramo adosado'
                resultado = 'Adosamiento detectado' if lado.get('estado') == 'ok' else 'Revisar condición especial'
            elif lado.get('estado') == 'pendiente':
                minimo_txt = 'Pendiente'
                hmax_txt = 'Pendiente'
                resultado = 'Pendiente'
            else:
                minimo_txt = f"{float(minimo):.2f} m" if minimo is not None else '-'
                hmax_txt = f"{float(hmax):.2f} m" if hmax is not None else '-'
                resultado = 'Compatible' if lado.get('estado') == 'ok' else 'Revisar'
            filas_lados.append([
                lado.get('lado', ''),
                f"{float(dist):.2f} m" if dist is not None else '-',
                'Sí' if lado.get('vano') else 'No',
                minimo_txt,
                hmax_txt,
                resultado,
            ])
        story.append(_tabla_datos_pdf(
            filas_lados, estilos['small'], encabezado=True,
            anchos=[25 * mm, 25 * mm, 16 * mm, 27 * mm, 42 * mm, 32 * mm]
        ))
        story.append(Spacer(1, 3 * mm))

    # Adosamientos
    ados = propuesta.get('revision_emplazamiento', {}).get('adosamientos', {})
    if ados:
        story.append(_parrafo_pdf('Revisión global de adosamiento', estilos['h2']))
        filas_ados = [['Deslinde', 'Existente', 'Futuro', 'Total unión', '%', 'Resultado']]
        for lado, info in ados.items():
            filas_ados.append([
                lado,
                f"{float(info.get('longitud_existente_detectada_m', 0) or 0):.2f} m",
                f"{float(info.get('longitud_futura_m', 0) or 0):.2f} m",
                f"{float(info.get('longitud_total_union_m', 0) or 0):.2f} m",
                f"{float(info.get('porcentaje_preliminar', 0) or 0):.1f}%",
                'Dentro 40%' if info.get('cumple_limite_general_40') else 'Revisar / supera 40%',
            ])
        story.append(_tabla_datos_pdf(
            filas_ados, estilos['small'], encabezado=True,
            anchos=[28 * mm, 27 * mm, 27 * mm, 30 * mm, 20 * mm, 35 * mm]
        ))

    # Estacionamientos
    story.append(_parrafo_pdf('Estacionamientos', estilos['h2']))
    filas_est = [
        ['Tramo PRC', propuesta.get('tramo_estacionamiento_prc', '-')],
        ['Regla utilizada', propuesta.get('regla_estacionamiento_prc', '-')],
        ['Requeridos preliminarmente', str(propuesta.get('estacionamientos_requeridos', '-'))],
        ['Disponibles declarados', str(propuesta.get('estacionamientos_disponibles', '-'))],
    ]
    story.append(_tabla_datos_pdf(filas_est, estilos['small'], anchos=[57 * mm, 110 * mm]))

    # 4. Soluciones constructivas
    story.append(PageBreak())
    story.append(_parrafo_pdf('4. Especificaciones técnicas de soluciones seleccionadas', estilos['h1']))

    soluciones = [
        ('Muro perimetral', propuesta.get('solucion_muro'), 'muro', None),
    ]
    if propuesta.get('hay_adosamiento_futuro'):
        soluciones.append(('Muro especial de adosamiento F-60', propuesta.get('solucion_muro_adosamiento_f60'), 'muro', 'muro_f60'))
    if float(propuesta.get('superficie_ampliacion_piso1', 0) or 0) > 0:
        soluciones.append(('Piso ampliación - Piso 1', propuesta.get('solucion_piso1'), 'piso', None))
    if float(propuesta.get('superficie_ampliacion_piso2', 0) or 0) > 0:
        soluciones.append(('Piso ampliación - Piso 2', propuesta.get('solucion_piso2'), 'piso', None))
    soluciones.append(('Techumbre', propuesta.get('solucion_techumbre'), 'techumbre', 'techumbre_madera'))

    for titulo_sol, sol, tipo_sol, clave_img_forzada in soluciones:
        story.append(_parrafo_pdf(titulo_sol, estilos['h2']))
        story.append(_tabla_datos_pdf(
            _filas_solucion_pdf(sol, tipo_sol), estilos['small'], anchos=[52 * mm, 115 * mm]
        ))

        clave_img = clave_img_forzada
        if tipo_sol == 'muro' and clave_img is None and sol:
            clave_img = clave_imagen_muro(sol.get('Sistema', ''), sol.get('Codigo_Solucion', ''))
        elif tipo_sol == 'piso' and clave_img is None:
            clave_img = _clave_imagen_piso_pdf(sol)

        nombre_img = IMAGENES_SOLUCIONES.get(clave_img) if clave_img else None
        if nombre_img:
            ruta_img = CARPETA_PROYECTO / nombre_img
            if ruta_img.exists():
                img_pdf = _imagen_pdf_ajustada(str(ruta_img), 145 * mm, 90 * mm)
                if img_pdf is not None:
                    story.append(Spacer(1, 2 * mm))
                    story.append(img_pdf)
        story.append(Spacer(1, 5 * mm))

    # 5. Observaciones y espacio para revisión
    story.append(PageBreak())
    story.append(_parrafo_pdf('5. Observaciones finales', estilos['h1']))
    grupos = [
        ('Incompatibilidades detectadas', propuesta.get('incompatibilidades_finales', [])),
        ('Observaciones / revisiones complementarias', propuesta.get('observaciones_finales', [])),
        ('Antecedentes pendientes', propuesta.get('pendientes_finales', [])),
    ]
    hay_items = False
    for nombre_grupo, items in grupos:
        if items:
            hay_items = True
            story.append(_parrafo_pdf(nombre_grupo, estilos['h2']))
            for item in items:
                story.append(_parrafo_pdf(f"- {item}", estilos['normal']))
    if not hay_items:
        story.append(_parrafo_pdf('No se registran observaciones adicionales en los parámetros automatizados.', estilos['normal']))

    story.append(Spacer(1, 7 * mm))
    story.append(_parrafo_pdf('Espacio para revisión profesional', estilos['h1']))
    filas_revision_prof = [
        ['Profesional revisor', '____________________________________________'],
        ['Profesión / especialidad', '____________________________________________'],
        ['Fecha de revisión', '____________________________________________'],
        ['Observación 1', '____________________________________________'],
        ['Observación 2', '____________________________________________'],
        ['Observación 3', '____________________________________________'],
    ]
    tabla_prof = _tabla_datos_pdf(filas_revision_prof, estilos['small'], anchos=[48 * mm, 119 * mm])
    story.append(tabla_prof)
    story.append(Spacer(1, 5 * mm))
    story.append(_parrafo_pdf(
        'Nota: el informe está diseñado para facilitar una revisión preliminar. La definición final del proyecto, '
        'sus cálculos, especificaciones y antecedentes para permiso deben ser desarrollados o validados por los '
        'profesionales competentes y revisados por la Dirección de Obras Municipales según corresponda.', estilos['nota']))

    doc.build(story, onFirstPage=_encabezado_pagina_pdf, onLaterPages=_encabezado_pagina_pdf)
    buffer.seek(0)
    return buffer.getvalue()

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
            "🧱 Futura Ampliación",
            "📋 Regularización Ley 20.898"
        )
    )

    st.markdown("---")

    st.info(
        "Utilice este menú para navegar por las distintas "
        "etapas de orientación técnica y normativa."
    )

    if st.session_state.datos_propiedad is not None:
        st.success("✅ Datos de la propiedad guardados")

    if st.session_state.propuesta_ampliacion is not None:
        st.success("✅ Propuesta de ampliación guardada")

    if st.session_state.resultado_regularizacion is not None:
        st.success("✅ Orientación de regularización guardada")


# ==========================================
# PANTALLA 1: INICIO
# ==========================================
if menu_seleccionado == "🏠 Inicio":

    # FRANJA SUPERIOR
    st.markdown("""
    <div class="franja-verde">
        <h1 style="color: white; margin-bottom: 0px; font-size: 32px;">🏗️ Prototipo de Orientación Técnica y Normativa para Ampliaciones Domiciliarias</h1>
        <p class="subtitulo-inicio">Comuna de San Miguel · OGUC · Ley N.º 20.898 · Plan Regulador Comunal · criterios técnicos constructivos</p>
    </div>
    """, unsafe_allow_html=True)

    # PROPÓSITO ACADÉMICO
    st.markdown("""
    <div class="texto-justificado-chico">
        <strong>Propósito académico:</strong> Este software fue desarrollado como prototipo de titulación para la carrera de Ingeniería en Construcción.
        Su objetivo es <strong>orientar la revisión preliminar</strong> de futuras ampliaciones domiciliarias y de edificaciones existentes que puedan requerir regularización,
        organizando antecedentes del predio, parámetros urbanísticos y criterios técnico-constructivos para identificar compatibilidades, observaciones y materias que requieren revisión profesional.
    </div>
    <div class="aviso-orientativo">
        <strong>⚠️ Alcance del prototipo:</strong> los resultados son orientativos y preliminares. La herramienta no aprueba proyectos, no emite permisos,
        no reemplaza la intervención de los profesionales competentes y no sustituye la revisión de la Dirección de Obras Municipales.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📜 Pilares Normativos Integrados")

    st.markdown("""
    <div class="caja-blanca">
        <div class="titulo-ley">1. Ordenanza General de Urbanismo y Construcciones (OGUC)</div>
        <div class="texto-justificado">
            Reglamento de aplicación nacional que establece disposiciones técnicas y administrativas para la edificación, incluyendo condiciones de habitabilidad,
            seguridad, acondicionamiento térmico, distanciamientos, rasantes, adosamientos y procedimientos asociados a permisos de construcción.
        </div>
        <div class="link-documento">🔗 <a href="https://www.bcn.cl/leychile/navegar?idNorma=13511" target="_blank">Ver documento oficial en la BCN</a></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="caja-blanca">
        <div class="titulo-ley">2. Ley N.º 20.898 — Procedimiento especial de regularización</div>
        <div class="texto-justificado">
            Conocida comúnmente como “Ley del Mono”, establece procedimientos especiales para determinadas edificaciones existentes sin recepción definitiva
            que cumplan las condiciones indicadas por la ley. Dentro del prototipo se utiliza únicamente para orientar la revisión de edificaciones existentes,
            separándola de la evaluación de una futura ampliación.
        </div>
        <div class="link-documento">🔗 <a href="https://www.bcn.cl/leychile/navegar?idNorma=1087285" target="_blank">Ver documento oficial en la BCN</a></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="caja-blanca">
        <div class="titulo-ley">3. Plan Regulador Comunal (PRC) de San Miguel</div>
        <div class="texto-justificado">
            Instrumento local que define la zonificación comunal, usos de suelo y normas urbanísticas aplicables al predio, como coeficientes de ocupación y constructibilidad,
            antejardines, sistemas de agrupamiento y estándares de estacionamientos.
        </div>
        <div class="link-documento">🔗 <a href="https://web.sanmiguel.cl/doctos/ordenanzas/plan_regulador/2.pdf" target="_blank">Ver documento oficial en la Municipalidad de San Miguel</a></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # GLOSARIO
    st.markdown("### 📚 Glosario de conceptos")
    st.caption("Definiciones simples para comprender los términos que utiliza el prototipo. Haz clic en cada concepto para desplegarlo.")

    glos_col1, glos_col2 = st.columns(2, gap="large")

    with glos_col1:
        st.markdown('<div class="titulo-glosario-grupo">📍 Terreno y emplazamiento</div>', unsafe_allow_html=True)

        with st.expander("🏡 Predio"):
            st.write("Es el terreno o propiedad sobre el cual se emplaza la vivienda. Sus dimensiones y superficie sirven de base para aplicar las normas urbanísticas del PRC.")

        with st.expander("📏 Deslinde"):
            st.write("Es el límite que separa el predio de las propiedades vecinas. En el prototipo se revisan principalmente los deslindes izquierdo, derecho y posterior.")

        with st.expander("🌿 Antejardín"):
            st.write("Es la franja ubicada entre la línea oficial del terreno y la edificación. Su profundidad mínima depende de las reglas del Plan Regulador Comunal y de ciertas excepciones asociadas a la vía o al predio.")

        with st.expander("🛣️ Línea oficial"):
            st.write("Es la línea que separa el espacio público del predio privado. Se utiliza como referencia para medir el antejardín y otras condiciones de emplazamiento.")

        with st.expander("🏠 Línea de edificación"):
            st.write("Es la línea a partir de la cual puede comenzar la edificación según las condiciones urbanísticas aplicables. No siempre coincide con la línea oficial, porque puede existir un antejardín obligatorio.")

        with st.expander("🧱 Adosamiento"):
            st.write("Situación en que una construcción se ubica directamente junto a un deslinde. Cuando existe adosamiento se aplican reglas especiales de longitud, altura, antejardín y resistencia al fuego del muro correspondiente.")

        with st.expander("📐 Rasante"):
            st.write("Línea imaginaria inclinada que nace desde los deslindes y limita el volumen o altura que puede alcanzar una edificación a medida que se aproxima al vecino.")

        with st.expander("↔️ Distanciamiento"):
            st.write("Separación mínima entre una edificación y el deslinde del terreno. La distancia exigible puede variar según la altura de la construcción y la presencia de vanos en la fachada.")

        with st.expander("🪟 Vano"):
            st.write("Abertura en un muro o fachada, por ejemplo una ventana o puerta. Su presencia puede modificar el distanciamiento mínimo exigible hacia un deslinde.")

    with glos_col2:
        st.markdown('<div class="titulo-glosario-grupo">🏗️ Normas urbanísticas y técnicas</div>', unsafe_allow_html=True)

        with st.expander("📍 Coeficiente de Ocupación de Suelo"):
            st.write("Factor que determina qué superficie máxima del terreno puede ser ocupada por la edificación en el nivel de suelo. En el prototipo se usa para estimar cuánto puede ocupar el primer piso después de la ampliación.")

        with st.expander("📐 Coeficiente de Constructibilidad"):
            st.write("Factor que, multiplicado por la superficie del predio, permite estimar la superficie edificable total máxima que corresponde al terreno según el PRC.")

        with st.expander("🗺️ Zona PRC"):
            st.write("Sector definido por el Plan Regulador Comunal al que pertenece el predio. Cada zona puede tener usos de suelo y condiciones de edificación diferentes.")

        with st.expander("🏘️ Uso de suelo"):
            st.write("Define qué actividades o destinos pueden desarrollarse en un sector, por ejemplo vivienda, comercio, equipamiento o actividad productiva. Antes de aplicar coeficientes residenciales debe verificarse que la zona admita vivienda.")

        with st.expander("📏 Superficie construida / edificada"):
            st.write("Corresponde a los metros cuadrados construidos de la vivienda. En el prototipo se diferencia la superficie existente, la ampliación propuesta y la superficie total proyectada.")

        with st.expander("🚗 Dotación de estacionamientos"):
            st.write("Cantidad de estacionamientos que debe considerarse según el destino y superficie de la edificación, de acuerdo con los estándares del PRC. El prototipo revisa de manera preliminar la cantidad para vivienda.")

        with st.expander("🔥 Clasificación F-60"):
            st.write("Clasificación de resistencia al fuego que indica que un elemento constructivo acreditado mantiene el desempeño exigido durante al menos 60 minutos bajo las condiciones del ensayo correspondiente. Es especialmente relevante en muros de adosamiento.")

        with st.expander("🌡️ Zona Térmica D"):
            st.write("Clasificación térmica vigente aplicable a San Miguel. Define exigencias de desempeño para distintos elementos de la envolvente, como muros, techumbres y pisos ventilados.")

        with st.expander("🌡️ Transmitancia térmica U"):
            st.write("Indicador de cuánto calor atraviesa un elemento constructivo. En términos simples, mientras menor sea el valor U, mayor es su capacidad de limitar las pérdidas o ganancias de calor.")

        with st.expander("🧊 Resistencia térmica Rt"):
            st.write("Indicador de la oposición de un elemento al paso del calor. En términos generales, mientras mayor sea Rt, mejor es su desempeño aislante.")

        with st.expander("📄 Recepción definitiva"):
            st.write("Acto mediante el cual la Dirección de Obras Municipales verifica formalmente, dentro de su competencia, que una obra ejecutada puede ser recibida conforme al procedimiento aplicable. No debe confundirse con el permiso para construir.")

        with st.expander("🛠️ Permiso de Obra Menor"):
            st.write("Procedimiento municipal que puede corresponder a determinadas ampliaciones u obras menores según la OGUC. La herramienta solo orienta sobre su posible aplicación; no tramita ni otorga el permiso.")


# ==========================================
# PANTALLA 2: DATOS DEL TERRENO
# ==========================================
elif menu_seleccionado == "🏡 Datos del Terreno":

    st.markdown(
        """
        <div class="datos-hero">
            <h2>🏡 Datos del Terreno y Vivienda Existente</h2>
            <p>Registra los antecedentes básicos del predio y de la vivienda. Con esta información, el prototipo podrá orientar los cálculos urbanísticos y preparar la futura ampliación.</p>
        </div>
        <div class="datos-pasos">
            <div class="datos-paso paso-verde"><span>1</span>Ubicación</div>
            <div class="datos-paso paso-azul"><span>2</span>Mediciones</div>
            <div class="datos-paso paso-ambar"><span>3</span>Emplazamiento</div>
            <div class="datos-paso paso-oscuro"><span>4</span>Revisión PRC</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ==========================================
    # 1. UBICACIÓN
    # ==========================================
    st.markdown(
        """
        <div class="datos-section sec-ubicacion">
            <span class="numero">1</span><span class="titulo">📍 Ubicación de la Propiedad</span>
            <span class="descripcion">Identifica la zona del Plan Regulador Comunal y registra una referencia del inmueble.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

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


    # ==========================================
    # 2. MEDICIONES
    # ==========================================
    st.markdown(
        """
        <div class="datos-section sec-medicion">
            <span class="numero">2</span><span class="titulo">📏 Mediciones del Terreno y Vivienda</span>
            <span class="descripcion">Ingresa las dimensiones para calcular automáticamente las superficies del terreno y de la vivienda existente.</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write(
        "Ingrese las dimensiones del terreno y de la vivienda. "
        "El software calculará automáticamente las superficies "
        "en metros cuadrados."
    )

    st.markdown('<div class="datos-subtitulo">🌳 Dimensiones del Terreno</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="datos-subtitulo">🏠 Superficie Construida de la Vivienda</div>', unsafe_allow_html=True)
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
        st.markdown('<div class="datos-subtitulo">🏠 Piso 1</div>', unsafe_allow_html=True)
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
        st.markdown('<div class="datos-subtitulo">🏘️ Piso 2</div>', unsafe_allow_html=True)
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

    st.markdown('<div class="datos-subtitulo">🧮 Superficie Construida Total</div>', unsafe_allow_html=True)
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


    # ==========================================
    # 3. DISTANCIAMIENTOS
    # ==========================================
    st.markdown(
        """
        <div class="datos-section sec-emplazamiento">
            <span class="numero">3</span><span class="titulo">📐 Distanciamientos y Emplazamiento</span>
            <span class="descripcion">Registra la relación de la vivienda con los deslindes, el antejardín y la vía que enfrenta el predio.</span>
        </div>
        """,
        unsafe_allow_html=True
    )
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
    st.markdown('<div class="datos-subtitulo">🌿 Antejardín · espacio entre la calle y la vivienda</div>', unsafe_allow_html=True)
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

    st.markdown("##### 🧾 Revisión preliminar de antejardín")

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
        "ℹ️ Esta revisión corresponde a la regla general del PRC. "
        "La aplicación de procedimientos especiales de regularización puede modificar las exigencias aplicables."
    )


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
    st.markdown(
        """
        <div class="datos-section sec-prc">
            <span class="numero">4</span><span class="titulo">🧾 Revisión Automática según PRC</span>
            <span class="descripcion">El prototipo consulta la base normativa de San Miguel para orientar la ocupación de suelo y la constructibilidad aplicables al predio.</span>
        </div>
        """,
        unsafe_allow_html=True
    )
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
        st.info("Ingrese el largo y ancho del terreno para realizar la revisión normativa preliminar.")

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

                    st.markdown('<div class="datos-subtitulo">🧮 Resultados Normativos</div>', unsafe_allow_html=True)
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

                    st.markdown('<div class="datos-subtitulo">🏗️ Superficie Disponible Preliminar</div>', unsafe_allow_html=True)
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
                        st.markdown('<div class="datos-subtitulo">✅ Comparación con la Vivienda Actual</div>', unsafe_allow_html=True)

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


    # ==========================================
    # RESUMEN
    # ==========================================
    st.markdown(
        """
        <div class="datos-resumen">
            <div class="datos-resumen-titulo">📋 Resumen de la Propiedad</div>
            <div style="font-size:13px;color:#557061;">Síntesis de los datos ingresados y de los márgenes urbanísticos calculados hasta este punto.</div>
        </div>
        """,
        unsafe_allow_html=True
    )
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
            st.session_state.posiciones_puzzle = {}
            st.session_state.posiciones_vivienda = {}

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

    st.markdown(
        """
        <div class="amp-hero">
            <h2>🧱 Futura Ampliación</h2>
            <p>Diseñe una propuesta preliminar, organice sus módulos y revise los principales criterios urbanísticos y técnico-constructivos antes de una evaluación profesional.</p>
        </div>
        <div class="amp-pasos">
            <div class="amp-paso amp-p1"><span>1</span>Datos base</div>
            <div class="amp-paso amp-p2"><span>2</span>Módulos</div>
            <div class="amp-paso amp-p3"><span>3</span>Superficies</div>
            <div class="amp-paso amp-p4"><span>4</span>Revisión normativa</div>
            <div class="amp-paso amp-p5"><span>5</span>Croquis</div>
            <div class="amp-paso amp-p6"><span>6</span>Soluciones</div>
            <div class="amp-paso amp-p7"><span>7</span>Estacionamientos</div>
            <div class="amp-paso amp-p8"><span>8</span>Resultado</div>
        </div>
        """,
        unsafe_allow_html=True
    )

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
        st.markdown("""
        <div class="amp-section amp-base">
            <span class="numero">1</span><span class="titulo">📋 Datos Base de la Propiedad</span>
            <span class="descripcion">Recupera automáticamente los antecedentes guardados del terreno y la vivienda existente.</span>
        </div>
        """, unsafe_allow_html=True)

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
        st.markdown("""
        <div class="amp-section amp-modulos">
            <span class="numero">2</span><span class="titulo">🧩 Módulos de Ampliación</span>
            <span class="descripcion">Construya la propuesta mediante rectángulos simples y defina el piso y la ubicación referencial de cada módulo.</span>
        </div>
        """, unsafe_allow_html=True)
        st.info(
            "📐 Divida la ampliación que desea realizar en **rectángulos simples**. "
            "Puede agregar tantos módulos como sea necesario."
        )

        modulos_ampliacion = []
        superficie_ampliacion_piso1 = 0.0
        superficie_ampliacion_piso2 = 0.0

        for i in range(st.session_state.cantidad_modulos_ampliacion):
            st.markdown(
                f'<div class="amp-modulo-titulo">🧱 Módulo de Ampliación {i + 1}</div>',
                unsafe_allow_html=True
            )

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
                        "Parte posterior de la vivienda",
                        "Parte frontal de la vivienda (hacia la calle)"
                    ],
                    key=f"ubicacion_ampliacion_{i}"
                )

                if ubicacion_modulo == "Parte frontal de la vivienda (hacia la calle)":
                    st.caption(
                        "La ampliación se ubicará hacia el frente del predio. El croquis y el puzle "
                        "verificarán que no invada el antejardín mínimo de referencia."
                    )
                    if datos.get("via_frente") in ["Avenida Santa Rosa", "Avenida / Callejón Lo Ovalle"]:
                        st.warning(
                            "⚠️ En esta vía pueden existir tramos con exigencia histórica de 5 m. "
                            "El editor usa 3 m como referencia preliminar y esta condición debe verificarse antes de definir la ubicación final."
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

        st.markdown("""
        <div class="amp-section amp-resumen">
            <span class="numero">3</span><span class="titulo">🧮 Resumen de la Ampliación Propuesta</span>
            <span class="descripcion">Compare la superficie de la ampliación con la vivienda existente y revise el total proyectado.</span>
        </div>
        """, unsafe_allow_html=True)
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

        st.markdown('<div class="amp-subtitulo">🏡 Vivienda después de la ampliación</div>', unsafe_allow_html=True)
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
        st.markdown("""
        <div class="amp-section amp-revision">
            <span class="numero">4</span><span class="titulo">✅ Revisión Preliminar de la Ampliación</span>
            <span class="descripcion">Orienta la compatibilidad de la propuesta con ocupación de suelo, constructibilidad y otros criterios aplicables.</span>
        </div>
        """, unsafe_allow_html=True)

        superficie_maxima_ocupacion_guardada = datos.get("superficie_maxima_ocupacion")
        superficie_maxima_construible_guardada = datos.get("superficie_maxima_construible")

        margen_ocupacion_proyectada = None
        margen_constructibilidad_proyectada = None

        st.markdown('<div class="amp-subtitulo">📍 Ocupación de Suelo</div>', unsafe_allow_html=True)

        if superficie_maxima_ocupacion_guardada is None:
            st.warning(
                "⚠️ No existe un valor de ocupación de suelo disponible para revisar preliminarmente esta propuesta."
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

        st.markdown('<div class="amp-subtitulo">📐 Constructibilidad</div>', unsafe_allow_html=True)

        if superficie_maxima_construible_guardada is None:
            st.warning(
                "⚠️ No existe un valor de constructibilidad disponible para revisar preliminarmente esta propuesta."
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
            st.markdown('<div class="amp-subtitulo">📍 Ubicación Referencial</div>', unsafe_allow_html=True)

            for modulo in modulos_ampliacion:
                if modulo["piso"] == "Piso 1" and modulo["superficie"] > 0:
                    texto_rotacion = " (rotado 90°)" if modulo.get("rotado") else ""
                    st.write(
                        f"**Módulo {modulo['numero']}:** {modulo['ubicacion']} — "
                        f"{modulo['superficie']:.2f} m²{texto_rotacion}"
                    )

        st.markdown("---")

        # ==========================================
        # 5. CROQUIS INTERACTIVO / EDITOR TIPO PUZLE
        # ==========================================
        st.markdown("""
        <div class="amp-section amp-croquis">
            <span class="numero">5</span><span class="titulo">🧩 Croquis Interactivo de la Ampliación</span>
            <span class="descripcion">Ubique la vivienda existente y los módulos propuestos para revisar su relación con el terreno y los deslindes.</span>
        </div>
        """, unsafe_allow_html=True)

        st.info(
            "Este es el **único croquis de emplazamiento** de la propuesta. Puedes editar tanto la **vivienda existente** como la **futura ampliación**. "
            "Esto permite representar mejor una casa en L, un segundo piso ubicado al fondo o a un costado, "
            "y luego hacer que las ampliaciones encajen con las piezas reales de la vivienda."
        )

        st.caption(
            "📐 El origen del dibujo se considera desde la esquina inferior izquierda del terreno: "
            "X aumenta hacia la derecha e Y aumenta desde la calle hacia el deslinde posterior."
        )
        g_puzzle_info = obtener_geometria_referencia(datos)
        st.caption(
            f"Frente del predio: Y = 0,00 m · Línea mínima de antejardín usada por el editor: "
            f"Y = {g_puzzle_info.get('antejardin_minimo', 0.0):.2f} m · Frente de la vivienda existente: "
            f"Y ≈ {g_puzzle_info.get('casa_y', 0.0):.2f} m."
        )

        modulos_puzzle = [
            modulo
            for modulo in modulos_ampliacion
            if float(modulo.get("superficie", 0) or 0) > 0
        ]

        asegurar_posiciones_puzzle(datos, modulos_puzzle)
        asegurar_posiciones_vivienda(datos)

        piso_puzzle = st.radio(
            "🏠 Piso que deseas editar:",
            ["Piso 1", "Piso 2"],
            horizontal=True,
            key="piso_editor_puzzle"
        )

        sectores_clave = "sectores_piso1" if piso_puzzle == "Piso 1" else "sectores_piso2"
        sectores_existentes_piso = [
            sector
            for sector in datos.get(sectores_clave, [])
            if float(sector.get("superficie", 0) or 0) > 0
        ]

        modulos_piso_puzzle = [
            modulo
            for modulo in modulos_puzzle
            if modulo.get("piso") == piso_puzzle
        ]

        tipos_disponibles = []
        if sectores_existentes_piso:
            tipos_disponibles.append("Vivienda existente")
        if modulos_piso_puzzle:
            tipos_disponibles.append("Futura ampliación")

        if not tipos_disponibles:
            st.warning(
                f"⚠️ No existen piezas registradas para **{piso_puzzle}**. "
                "Si corresponde, vuelve a Datos del Terreno para registrar ese piso o agrega un módulo de ampliación."
            )

        else:
            st.markdown("#### ✏️ Configuración de la planta")

            config_col1, config_col2, config_col3 = st.columns([1.1, 1.1, 1.3])

            with config_col1:
                tipo_visible = st.radio(
                    "Tipo de pieza:",
                    tipos_disponibles,
                    horizontal=False,
                    key=f"tipo_pieza_puzzle_{piso_puzzle}"
                )

            with config_col2:
                encaje_magnetico = st.toggle(
                    "🧲 Encaje magnético",
                    value=True,
                    key=f"encaje_magnetico_{piso_puzzle}",
                    help=(
                        "Detecta bordes cercanos de la vivienda, otros módulos, el terreno o la línea mínima de antejardín "
                        "y ajusta la pieza para que queden exactamente contiguos."
                    )
                )

            with config_col3:
                paso_movimiento = st.selectbox(
                    "Precisión del movimiento:",
                    [0.10, 0.25, 0.50, 1.00],
                    index=1,
                    format_func=lambda valor: f"{valor:.2f} m",
                    key=f"paso_movimiento_puzzle_{piso_puzzle}"
                )

            st.caption(
                "🧲 El encaje ahora trabaja borde con borde: basta acercar la pieza al costado de la vivienda, "
                "otro módulo o un límite válido del terreno. El ajuste automático usa una tolerancia de 0,50 m."
            )

            if tipo_visible == "Vivienda existente":
                opciones = {
                    f"Sector existente {sector['numero']}": sector
                    for sector in sectores_existentes_piso
                }
                etiqueta_seleccion = "Sector de la vivienda que deseas mover:"
            else:
                opciones = {
                    f"Módulo de ampliación {modulo['numero']}": modulo
                    for modulo in modulos_piso_puzzle
                }
                etiqueta_seleccion = "Módulo de ampliación que deseas mover:"

            nombre_pieza = st.selectbox(
                etiqueta_seleccion,
                list(opciones.keys()),
                key=f"pieza_seleccionada_puzzle_{piso_puzzle}_{tipo_visible}"
            )

            objeto_seleccionado = opciones[nombre_pieza]
            tipo_interno = "vivienda" if tipo_visible == "Vivienda existente" else "ampliacion"

            if tipo_interno == "vivienda":
                clave_seleccionada = clave_sector_vivienda(
                    piso_puzzle,
                    objeto_seleccionado
                )
                posicion_actual = st.session_state.posiciones_vivienda.get(
                    clave_seleccionada,
                    {"x": 0.0, "y": 0.0, "rotado": False}
                )
            else:
                clave_seleccionada = clave_modulo_puzzle(
                    objeto_seleccionado
                )
                posicion_actual = st.session_state.posiciones_puzzle.get(
                    clave_seleccionada,
                    {"x": 0.0, "y": 0.0, "rotado": False}
                )

            ancho_actual, largo_actual = dimensiones_pieza(
                objeto_seleccionado,
                posicion_actual
            )

            st.markdown("---")

            controles_puzzle, vista_puzzle = st.columns([1.0, 2.3])

            with controles_puzzle:
                st.markdown("#### 🎮 Mover pieza")

                st.metric(
                    "Coordenada X",
                    f"{float(posicion_actual.get('x', 0)):.2f} m"
                )
                st.metric(
                    "Coordenada Y",
                    f"{float(posicion_actual.get('y', 0)):.2f} m"
                )
                st.caption(
                    f"Tamaño actual: **{ancho_actual:.2f} × {largo_actual:.2f} m**"
                )

                flecha_arriba_1, flecha_arriba_2, flecha_arriba_3 = st.columns(3)

                with flecha_arriba_2:
                    if st.button(
                        "⬆️",
                        key=f"puzzle_arriba_{piso_puzzle}_{tipo_interno}_{clave_seleccionada}",
                        help="Mover hacia el deslinde posterior"
                    ):
                        mover_pieza_unificada(
                            clave_seleccionada,
                            tipo_interno,
                            dy=paso_movimiento
                        )
                        if encaje_magnetico:
                            aplicar_encaje_magnetico(
                                datos,
                                modulos_puzzle,
                                piso_puzzle,
                                clave_seleccionada,
                                tipo_interno
                            )
                        st.rerun()

                flecha_centro_1, flecha_centro_2, flecha_centro_3 = st.columns(3)

                with flecha_centro_1:
                    if st.button(
                        "⬅️",
                        key=f"puzzle_izquierda_{piso_puzzle}_{tipo_interno}_{clave_seleccionada}",
                        help="Mover hacia el deslinde izquierdo"
                    ):
                        mover_pieza_unificada(
                            clave_seleccionada,
                            tipo_interno,
                            dx=-paso_movimiento
                        )
                        if encaje_magnetico:
                            aplicar_encaje_magnetico(
                                datos,
                                modulos_puzzle,
                                piso_puzzle,
                                clave_seleccionada,
                                tipo_interno
                            )
                        st.rerun()

                with flecha_centro_2:
                    st.markdown(
                        "<div style='text-align:center; padding-top:8px;'>🧱</div>",
                        unsafe_allow_html=True
                    )

                with flecha_centro_3:
                    if st.button(
                        "➡️",
                        key=f"puzzle_derecha_{piso_puzzle}_{tipo_interno}_{clave_seleccionada}",
                        help="Mover hacia el deslinde derecho"
                    ):
                        mover_pieza_unificada(
                            clave_seleccionada,
                            tipo_interno,
                            dx=paso_movimiento
                        )
                        if encaje_magnetico:
                            aplicar_encaje_magnetico(
                                datos,
                                modulos_puzzle,
                                piso_puzzle,
                                clave_seleccionada,
                                tipo_interno
                            )
                        st.rerun()

                flecha_abajo_1, flecha_abajo_2, flecha_abajo_3 = st.columns(3)

                with flecha_abajo_2:
                    if st.button(
                        "⬇️",
                        key=f"puzzle_abajo_{piso_puzzle}_{tipo_interno}_{clave_seleccionada}",
                        help="Mover hacia la calle"
                    ):
                        mover_pieza_unificada(
                            clave_seleccionada,
                            tipo_interno,
                            dy=-paso_movimiento
                        )
                        if encaje_magnetico:
                            aplicar_encaje_magnetico(
                                datos,
                                modulos_puzzle,
                                piso_puzzle,
                                clave_seleccionada,
                                tipo_interno
                            )
                        st.rerun()

                st.markdown("---")

                boton_rotar, boton_encajar = st.columns(2)

                with boton_rotar:
                    if st.button(
                        "🔄 Rotar 90°",
                        key=f"puzzle_rotar_{piso_puzzle}_{tipo_interno}_{clave_seleccionada}"
                    ):
                        rotar_pieza_unificada(
                            clave_seleccionada,
                            tipo_interno
                        )
                        if encaje_magnetico:
                            aplicar_encaje_magnetico(
                                datos,
                                modulos_puzzle,
                                piso_puzzle,
                                clave_seleccionada,
                                tipo_interno
                            )
                        st.rerun()

                with boton_encajar:
                    if st.button(
                        "🧲 Encajar ahora",
                        key=f"puzzle_encajar_{piso_puzzle}_{tipo_interno}_{clave_seleccionada}",
                        help="Busca un borde cercano y ajusta la pieza exactamente"
                    ):
                        encontro = aplicar_encaje_magnetico(
                            datos,
                            modulos_puzzle,
                            piso_puzzle,
                            clave_seleccionada,
                            tipo_interno,
                            umbral=1.00
                        )
                        if not encontro:
                            st.toast("No se encontró un borde compatible dentro de 1,00 m.")
                        else:
                            motivo = st.session_state.get("ultimo_encaje_puzzle", "borde cercano")
                            st.toast(f"🧲 Pieza encajada con {motivo}.")
                        st.rerun()

                boton_reiniciar, boton_reiniciar_piso = st.columns(2)

                with boton_reiniciar:
                    if st.button(
                        "↩️ Reiniciar pieza",
                        key=f"puzzle_reiniciar_{piso_puzzle}_{tipo_interno}_{clave_seleccionada}"
                    ):
                        reiniciar_pieza_unificada(
                            datos,
                            objeto_seleccionado,
                            piso_puzzle,
                            tipo_interno
                        )
                        st.rerun()

                with boton_reiniciar_piso:
                    if tipo_interno == "vivienda":
                        if st.button(
                            "🏠 Reiniciar vivienda",
                            key=f"puzzle_reiniciar_vivienda_{piso_puzzle}"
                        ):
                            reiniciar_piso_vivienda(
                                datos,
                                piso_puzzle
                            )
                            st.rerun()

                if tipo_interno == "vivienda":
                    st.info(
                        "✏️ Estás moviendo una pieza de la **vivienda ya construida**. "
                        "Úsala para reproducir la ubicación real de la casa; no significa que la vivienda se vaya a mover físicamente."
                    )
                else:
                    st.info(
                        "🧱 Estás moviendo una pieza de la **futura ampliación**. "
                        "Las piezas se pueden dejar pegadas a la vivienda existente sin superponerlas."
                    )

            with vista_puzzle:
                figura_puzzle, validaciones_puzzle, imagen_puzzle = crear_croquis_puzzle(
                    datos,
                    modulos_puzzle,
                    piso_puzzle,
                    modulo_seleccionado=clave_seleccionada
                )

                if figura_puzzle is None:
                    st.error(
                        "❌ No fue posible generar el editor porque faltan dimensiones del terreno."
                    )
                else:
                    st.pyplot(figura_puzzle)

                    st.caption(
                        "La pieza seleccionada se destaca con borde morado. "
                        "Azul = vivienda existente; naranjo = futura ampliación; "
                        "amarillo = requiere revisión; rojo = posición con conflicto."
                    )

                    if imagen_puzzle is not None:
                        st.download_button(
                            f"📥 Descargar distribución editable – {piso_puzzle}",
                            data=imagen_puzzle,
                            file_name=f"Distribucion_Puzzle_{piso_puzzle.replace(' ', '_')}.png",
                            mime="image/png",
                            key=f"descargar_puzzle_{piso_puzzle}"
                        )

                    plt.close(figura_puzzle)

            if validaciones_puzzle:
                with st.expander(
                    f"🔎 Ver revisión de posiciones – {piso_puzzle}"
                ):
                    for revision in validaciones_puzzle:
                        if revision["nivel"] == "ok":
                            simbolo = "✅"
                        elif revision["nivel"] == "warning":
                            simbolo = "⚠️"
                        else:
                            simbolo = "❌"

                        tipo_texto = (
                            "Sector existente"
                            if revision["tipo"] == "vivienda"
                            else "Módulo de ampliación"
                        )
                        giro = "Sí" if revision["rotado"] else "No"

                        st.write(
                            f"{simbolo} **{tipo_texto} {revision['numero']}** — "
                            f"X: {revision['x']:.2f} m | "
                            f"Y: {revision['y']:.2f} m | "
                            f"Rotado: {giro}. {revision['mensaje']}"
                        )

            if piso_puzzle == "Piso 2":
                st.info(
                    "🔒 **Edición independiente por piso:** al editar Piso 2, solo se pueden seleccionar y mover piezas del Piso 2. "
                    "La vivienda y cualquier ampliación del Piso 1 se muestran únicamente como **referencia fija** y no responden a los controles."
                )
                st.warning(
                    "⚠️ Si una futura ampliación de Piso 2 queda fuera de la huella del primer piso, el programa la marca para "
                    "**revisión estructural**, pero no la considera automáticamente imposible."
                )

            st.success(
                "🧲 **Consejo:** para unir dos piezas, muévelas hasta quedar cerca. "
                "Con el encaje magnético activado, el sistema intentará dejar sus bordes exactamente coincidentes."
            )

        st.markdown("---")

        # ==========================================
        # 5.1 ALTURA, VANOS, DISTANCIAMIENTOS Y ADOSAMIENTO
        # ==========================================
        st.markdown('<div class="amp-subtitulo">📐 Altura, Vanos, Distanciamientos y Adosamiento</div>', unsafe_allow_html=True)
        st.info(
            "Esta revisión usa la posición actual de cada módulo en el puzle. Para las partes aisladas se compara "
            "la distancia a los deslindes laterales y posterior con la tabla del **art. 2.6.3 OGUC**, considerando "
            "la altura y la existencia de vanos. Para la Región Metropolitana también se muestra una comprobación "
            "geométrica preliminar de la rasante de **70°**. Si una pieza queda contigua al deslinde, se trata como "
            "posible adosamiento y se revisan separadamente las condiciones generales del **art. 2.6.2**."
        )
        st.caption(
            "Para esta herramienta, 'vano' significa una abertura relevante en la fachada hacia el deslinde, como ventana o puerta. "
            "La revisión es preliminar y supone terreno horizontal para el cálculo simplificado de rasante."
        )

        revision_emplazamiento_futura = {
            "modulos": [],
            "adosamientos": {},
            "pendientes": [],
            "observaciones": [],
            "criterio_rasante_rm_grados": 70.0,
        }
        ados_futuro = {"Izquierdo": 0.0, "Derecho": 0.0, "Posterior": 0.0}
        hay_adosamiento_futuro = False

        g_empl = obtener_geometria_referencia(datos)
        modulos_validos_empl = [
            m for m in modulos_puzzle
            if float(m.get("superficie", 0) or 0) > 0
        ]

        if not modulos_validos_empl:
            st.warning("⚠️ Agrega al menos un módulo de ampliación para realizar esta revisión.")
            revision_emplazamiento_futura["pendientes"].append("No existen módulos de ampliación para revisar.")
        else:
            for modulo in modulos_validos_empl:
                numero = modulo.get("numero")
                piso_mod = modulo.get("piso", "Piso 1")
                clave_mod = clave_modulo_puzzle(modulo)
                posicion_mod = st.session_state.posiciones_puzzle.get(clave_mod)
                if posicion_mod is None:
                    posicion_mod = calcular_posicion_inicial_puzzle(datos, modulo)

                ancho_mod, largo_mod = dimensiones_pieza(modulo, posicion_mod)
                x_mod = float(posicion_mod.get("x", 0) or 0)
                y_mod = float(posicion_mod.get("y", 0) or 0)

                dist_izq = max(x_mod, 0.0)
                dist_der = max(g_empl["ancho_terreno"] - (x_mod + ancho_mod), 0.0)
                dist_post = max(g_empl["largo_terreno"] - (y_mod + largo_mod), 0.0)
                dist_frente = max(y_mod, 0.0)

                with st.expander(
                    f"🏗️ Módulo {numero} — {piso_mod} · altura y fachadas",
                    expanded=(len(modulos_validos_empl) == 1)
                ):
                    st.write(
                        f"**Posición actual en puzle:** X {x_mod:.2f} m · Y {y_mod:.2f} m · "
                        f"dimensiones en planta {ancho_mod:.2f} × {largo_mod:.2f} m."
                    )

                    col_altura, col_info = st.columns([1, 2])
                    with col_altura:
                        altura_mod = st.number_input(
                            "Altura total desde suelo natural (m):",
                            min_value=0.0,
                            max_value=20.0,
                            value=0.0,
                            step=0.10,
                            format="%.2f",
                            key=f"altura_total_modulo_{numero}_{piso_mod.replace(' ', '_')}",
                            help=(
                                "Ingrese la altura total de la parte de ampliación desde el suelo natural hasta el punto más alto "
                                "de la fachada que se está revisando. En Piso 2 debe considerar la altura total desde terreno, no solo la altura del recinto."
                            )
                        )
                    with col_info:
                        if altura_mod <= 0:
                            st.warning("⚠️ Altura pendiente. Sin este dato no se puede cerrar la revisión de distanciamientos ni rasante.")
                        else:
                            st.success(f"Altura declarada para esta revisión: **{altura_mod:.2f} m**.")

                    st.markdown("**¿La fachada de este módulo tiene vanos orientados hacia cada deslinde?**")
                    v1, v2, v3 = st.columns(3)
                    with v1:
                        vano_izq = st.checkbox(
                            "Vanos hacia deslinde izquierdo",
                            key=f"vano_izq_mod_{numero}_{piso_mod.replace(' ', '_')}"
                        )
                    with v2:
                        vano_der = st.checkbox(
                            "Vanos hacia deslinde derecho",
                            key=f"vano_der_mod_{numero}_{piso_mod.replace(' ', '_')}"
                        )
                    with v3:
                        vano_post = st.checkbox(
                            "Vanos hacia deslinde posterior",
                            key=f"vano_post_mod_{numero}_{piso_mod.replace(' ', '_')}"
                        )

                    tolerancia_ados = 0.05
                    lados = [
                        ("Izquierdo", dist_izq, vano_izq),
                        ("Derecho", dist_der, vano_der),
                        ("Posterior", dist_post, vano_post),
                    ]
                    filas_revision = []
                    resultados_lados = []

                    for lado, distancia_real, tiene_vano in lados:
                        es_adosado = distancia_real <= tolerancia_ados
                        if altura_mod <= 0:
                            filas_revision.append({
                                "Deslinde": lado,
                                "Distancia actual": f"{distancia_real:.2f} m",
                                "Vanos": "Sí" if tiene_vano else "No",
                                "Mínimo OGUC": "Pendiente altura",
                                "Rasante 70°": "Pendiente altura",
                                "Resultado": "⚠️ Pendiente",
                            })
                            resultados_lados.append({
                                "lado": lado,
                                "estado": "pendiente",
                                "distancia": distancia_real,
                                "vano": bool(tiene_vano),
                            })
                            continue

                        if es_adosado:
                            estado = "ok" if altura_mod <= 3.5 + 1e-9 else "observacion"
                            texto_estado = (
                                "🟨 Adosamiento detectado"
                                if altura_mod <= 3.5 + 1e-9
                                else "⚠️ Revisar excepción de altura"
                            )
                            filas_revision.append({
                                "Deslinde": lado,
                                "Distancia actual": "0,00 m (adosado)",
                                "Vanos": "Sí" if tiene_vano else "No",
                                "Mínimo OGUC": "No aplica 2.6.3 a parte adosada",
                                "Rasante 70°": "No aplica a parte adosada",
                                "Resultado": texto_estado,
                            })
                            resultados_lados.append({
                                "lado": lado,
                                "estado": estado,
                                "tipo": "adosado",
                                "distancia": distancia_real,
                                "vano": bool(tiene_vano),
                                "altura": float(altura_mod),
                            })
                            if altura_mod > 3.5 + 1e-9:
                                revision_emplazamiento_futura["observaciones"].append(
                                    f"Módulo {numero}: altura {altura_mod:.2f} m en adosamiento {lado.lower()} supera la altura general de 3,50 m; revisar si procede excepción por edificación vecina aprobada."
                                )
                            if tiene_vano:
                                revision_emplazamiento_futura["observaciones"].append(
                                    f"Módulo {numero}: se declaró vano en muro adosado hacia el deslinde {lado.lower()}; requiere revisar autorización del vecino, seguridad y proyecto estructural."
                                )
                        else:
                            minimo = distancia_minima_oguc_263(altura_mod, tiene_vano)
                            altura_rasante = altura_maxima_rasante_rm(distancia_real, 70.0)
                            cumple_dist = distancia_real + 1e-9 >= float(minimo)
                            cumple_ras = altura_mod <= altura_rasante + 1e-9
                            cumple = cumple_dist and cumple_ras
                            filas_revision.append({
                                "Deslinde": lado,
                                "Distancia actual": f"{distancia_real:.2f} m",
                                "Vanos": "Sí" if tiene_vano else "No",
                                "Mínimo OGUC": f"{minimo:.2f} m",
                                "Rasante 70°": f"H máx. aprox. {altura_rasante:.2f} m",
                                "Resultado": "✅ Compatible" if cumple else "❌ Revisar",
                            })
                            resultados_lados.append({
                                "lado": lado,
                                "estado": "ok" if cumple else "error",
                                "tipo": "aislado",
                                "distancia": float(distancia_real),
                                "vano": bool(tiene_vano),
                                "altura": float(altura_mod),
                                "distancia_minima": float(minimo),
                                "altura_maxima_rasante_aprox": float(altura_rasante),
                                "cumple_distanciamiento": bool(cumple_dist),
                                "cumple_rasante_aprox": bool(cumple_ras),
                            })
                            if not cumple_dist:
                                revision_emplazamiento_futura["observaciones"].append(
                                    f"Módulo {numero}: distancia al deslinde {lado.lower()} ({distancia_real:.2f} m) es menor al mínimo preliminar de {minimo:.2f} m para la altura/vanos declarados."
                                )
                            if not cumple_ras:
                                revision_emplazamiento_futura["observaciones"].append(
                                    f"Módulo {numero}: con la aproximación de rasante 70° y terreno horizontal, la altura {altura_mod:.2f} m supera la altura geométrica aproximada de {altura_rasante:.2f} m hacia el deslinde {lado.lower()}."
                                )

                    st.dataframe(pd.DataFrame(filas_revision), use_container_width=True, hide_index=True)

                    if piso_mod == "Piso 1":
                        antejardin_ref = float(g_empl.get("antejardin_minimo", 0.0) or 0.0)
                        if dist_frente + 1e-9 >= antejardin_ref:
                            st.success(
                                f"✅ **Frente:** el módulo comienza a {dist_frente:.2f} m desde la línea frontal del terreno; "
                                f"la referencia de antejardín usada por el prototipo es {antejardin_ref:.2f} m."
                            )
                        else:
                            st.error(
                                f"❌ **Frente:** el módulo comienza a {dist_frente:.2f} m y entra en la franja de antejardín de referencia ({antejardin_ref:.2f} m)."
                            )
                    else:
                        st.caption(
                            f"Frente del módulo de Piso 2: Y = {dist_frente:.2f} m. La proyección de pisos superiores sobre antejardín/cuerpos salientes requiere una revisión específica y no se aprueba automáticamente aquí."
                        )

                    revision_emplazamiento_futura["modulos"].append({
                        "numero": numero,
                        "piso": piso_mod,
                        "altura_total_m": float(altura_mod),
                        "posicion": {"x": x_mod, "y": y_mod},
                        "dimensiones": {"ancho": ancho_mod, "largo": largo_mod},
                        "vanos": {
                            "izquierdo": bool(vano_izq),
                            "derecho": bool(vano_der),
                            "posterior": bool(vano_post),
                        },
                        "distancias": {
                            "izquierdo": dist_izq,
                            "derecho": dist_der,
                            "posterior": dist_post,
                            "frente": dist_frente,
                        },
                        "resultados_lados": resultados_lados,
                    })
                    if altura_mod <= 0:
                        revision_emplazamiento_futura["pendientes"].append(
                            f"Ingresar altura total del módulo {numero} ({piso_mod})."
                        )

            # Resumen de adosamiento de toda la futura ampliación.
            st.markdown('<div class="amp-subtitulo">🧱 Revisión global de adosamiento</div>', unsafe_allow_html=True)
            st.caption(
                "El sistema identifica como contacto con deslinde las piezas ubicadas a 5 cm o menos. "
                "La longitud se calcula como unión de tramos para no duplicar módulos superpuestos entre pisos."
            )

            intervalos_futuros = obtener_intervalos_adosamiento_futuro(
                datos, modulos_validos_empl, tolerancia=0.05
            )
            intervalos_existentes = obtener_intervalos_adosamiento_existente(
                datos, tolerancia=0.05
            )
            ados_futuro = {
                lado: unir_longitudes_intervalos(intervalos_futuros[lado])
                for lado in intervalos_futuros
            }
            ados_existente = {
                lado: unir_longitudes_intervalos(intervalos_existentes[lado])
                for lado in intervalos_existentes
            }
            hay_adosamiento_futuro = any(float(v or 0) > 0.0 for v in ados_futuro.values())

            lados_config = [
                ("Izquierdo", g_empl["largo_terreno"]),
                ("Derecho", g_empl["largo_terreno"]),
                ("Posterior", g_empl["ancho_terreno"]),
            ]

            st.info(
                "ℹ️ La longitud de la vivienda existente ya adosada se detecta automáticamente desde el puzle. "
                "El total corresponde a la **unión real de los tramos existentes y futuros**, por lo que si un Piso 2 "
                "queda sobre un tramo ya ocupado en Piso 1, ese sector no se cuenta dos veces."
            )

            filas_adosamiento = []
            for lado, largo_deslinde in lados_config:
                futuro = float(ados_futuro.get(lado, 0.0) or 0.0)
                existente = float(ados_existente.get(lado, 0.0) or 0.0)
                intervalos_union = list(intervalos_existentes.get(lado, [])) + list(intervalos_futuros.get(lado, []))
                total = unir_longitudes_intervalos(intervalos_union)
                porcentaje = (total / largo_deslinde * 100.0) if largo_deslinde > 0 else 0.0
                cumple_40 = porcentaje <= 40.0 + 1e-9
                filas_adosamiento.append({
                    "Deslinde": lado,
                    "Largo deslinde": f"{largo_deslinde:.2f} m",
                    "Vivienda existente ya adosada": f"{existente:.2f} m",
                    "Futuro detectado": f"{futuro:.2f} m",
                    "Total sin duplicar": f"{total:.2f} m",
                    "% adosamiento": f"{porcentaje:.1f}%",
                    "Límite general": "40%",
                    "Resultado": "✅ Dentro del 40%" if cumple_40 else "❌ Supera 40%",
                })
                revision_emplazamiento_futura["adosamientos"][lado] = {
                    "largo_deslinde_m": float(largo_deslinde),
                    "longitud_existente_detectada_m": existente,
                    "longitud_futura_m": futuro,
                    "longitud_total_union_m": total,
                    "porcentaje_preliminar": porcentaje,
                    "cumple_limite_general_40": bool(cumple_40),
                }
                if not cumple_40:
                    revision_emplazamiento_futura["observaciones"].append(
                        f"Adosamiento {lado.lower()}: la unión de vivienda existente y futura equivale a {porcentaje:.1f}% del deslinde y supera el límite general de 40%; revisar si existe una excepción aplicable."
                    )

            st.dataframe(pd.DataFrame(filas_adosamiento), use_container_width=True, hide_index=True)

            if hay_adosamiento_futuro:
                st.warning(
                    "🔥 **Hay futura ampliación en contacto con uno o más deslindes.** Además de longitud y altura, debe verificarse "
                    "la envolvente de adosamiento de 45°, la solución de aguas lluvia y la resistencia al fuego que corresponda. "
                    "La solución térmica seleccionada para el muro **no acredita por sí sola** el desempeño al fuego."
                )
                st.caption(
                    "El prototipo no automatiza la envolvente tridimensional de 45° ni las excepciones por coincidencia con una edificación vecina aprobada; esas condiciones quedan para revisión profesional."
                )

            if revision_emplazamiento_futura["observaciones"]:
                with st.expander("⚠️ Ver observaciones de emplazamiento", expanded=True):
                    for obs in revision_emplazamiento_futura["observaciones"]:
                        st.write(f"• {obs}")
            elif not revision_emplazamiento_futura["pendientes"]:
                st.success(
                    "✅ Con los datos ingresados, no se detectaron conflictos preliminares de distanciamiento, rasante simplificada o porcentaje general de adosamiento."
                )

        st.markdown("---")

        # ==========================================
        # 6. SOLUCIONES CONSTRUCTIVAS DE LA FUTURA AMPLIACIÓN
        # ==========================================
        st.markdown("""
        <div class="amp-section amp-soluciones">
            <span class="numero">6</span><span class="titulo">🧰 Soluciones Constructivas</span>
            <span class="descripcion">Seleccione soluciones de muro, piso y techumbre compatibles con los criterios técnicos incorporados al prototipo.</span>
        </div>
        """, unsafe_allow_html=True)
        st.info(
            "Seleccione soluciones de referencia para **muros, pisos y techumbre** de la ampliación. "
            "Las alternativas provienen de la base técnica incorporada al prototipo y se muestran con "
            "carácter orientativo. Su selección no reemplaza el proyecto, cálculo, especificación ni "
            "acreditación que pueda exigir un profesional competente o la Dirección de Obras Municipales."
        )

        solucion_muro_futura = None
        solucion_muro_adosamiento_futura = None
        solucion_piso1_futura = None
        solucion_piso2_futura = None
        solucion_techumbre_futura = None

        def _texto_valor_futuro(valor, decimales=2, sufijo=""):
            if valor is None or pd.isna(valor):
                return "No informado"
            try:
                return f"{float(valor):.{decimales}f}{sufijo}"
            except (TypeError, ValueError):
                return str(valor)

        def _fila_a_dict_seguro(fila):
            resultado = {}
            for clave, valor in fila.to_dict().items():
                if pd.isna(valor):
                    resultado[clave] = None
                elif hasattr(valor, "item"):
                    try:
                        resultado[clave] = valor.item()
                    except Exception:
                        resultado[clave] = valor
                else:
                    resultado[clave] = valor
            return resultado

        # ------------------------------------------
        # 6.1 MURO
        # ------------------------------------------
        st.markdown('<div class="amp-subtitulo">🧱 Muros</div>', unsafe_allow_html=True)

        try:
            base_muros_futura = cargar_soluciones_muros()
        except Exception:
            base_muros_futura = None

        if base_muros_futura is None or base_muros_futura.empty:
            st.warning(
                "⚠️ No fue posible cargar **Soluciones_Muros** desde la base normativa. "
                "La propuesta puede continuar, pero la solución de muro quedará pendiente."
            )
        else:
            opciones_muros_futura = ["Seleccione una solución..."]
            mapa_muros_futura = {}

            for _, fila_muro in base_muros_futura.iterrows():
                uso_especial = str(fila_muro.get("Uso_Especial", "") or "").strip().lower()
                resistencia_fuego = str(fila_muro.get("Resistencia_Fuego", "") or "").strip().upper()
                if "adosamiento" in uso_especial or resistencia_fuego == "F-60":
                    continue
                etiqueta = f"{fila_muro['Codigo_Solucion']} — {fila_muro['Sistema']}"
                opciones_muros_futura.append(etiqueta)
                mapa_muros_futura[etiqueta] = fila_muro

            muro_elegido_futura = st.selectbox(
                "Solución propuesta para los muros perimetrales de la ampliación:",
                opciones_muros_futura,
                key="futura_solucion_muro"
            )

            if muro_elegido_futura != "Seleccione una solución...":
                fila_muro = mapa_muros_futura[muro_elegido_futura]
                solucion_muro_futura = _fila_a_dict_seguro(fila_muro)

                clave_img_muro = clave_imagen_muro(fila_muro.get("Sistema", ""), fila_muro.get("Codigo_Solucion", ""))
                if clave_img_muro:
                    with st.expander("🖼️ Ver detalle visual de la solución de muro", expanded=True):
                        mostrar_imagen_solucion(
                            clave_img_muro,
                            caption=f"Detalle visual de referencia — {fila_muro.get('Codigo_Solucion', '')} · {fila_muro.get('Sistema', '')}"
                        )

                col_muro_a, col_muro_b, col_muro_c = st.columns(3)
                with col_muro_a:
                    st.metric("Transmitancia U", _texto_valor_futuro(fila_muro.get("U_W_m2K"), 2, " W/m²K"))
                with col_muro_b:
                    st.metric("Resistencia Rt", _texto_valor_futuro(fila_muro.get("Rt_m2K_W"), 2, " m²K/W"))
                with col_muro_c:
                    st.metric("Referencia térmica", str(fila_muro.get("Compatibilidad_Zona_D", "Pendiente")))

                u_muro = fila_muro.get("U_W_m2K")
                u_max_muro = fila_muro.get("U_Max_Zona_D")
                rt_muro = fila_muro.get("Rt_m2K_W")
                rt_min_muro = fila_muro.get("Rt_Min_Zona_D")

                if (
                    pd.notna(u_muro) and pd.notna(u_max_muro)
                    and pd.notna(rt_muro) and pd.notna(rt_min_muro)
                    and float(u_muro) <= float(u_max_muro)
                    and float(rt_muro) >= float(rt_min_muro)
                ):
                    st.success(
                        f"✅ La solución de referencia presenta valores compatibles con Zona Térmica D: "
                        f"**U = {float(u_muro):.2f} W/m²K ≤ {float(u_max_muro):.2f}** y "
                        f"**Rt = {float(rt_muro):.2f} m²K/W ≥ {float(rt_min_muro):.2f}**."
                    )

                with st.expander("🔎 Ver composición del muro seleccionado"):
                    st.write(f"**Código:** {fila_muro.get('Codigo_Solucion', '')}")
                    st.write(f"**Sistema:** {fila_muro.get('Sistema', '')}")
                    st.write(f"**Estructura principal:** {fila_muro.get('Estructura_Principal', '')}")

                    if pd.notna(fila_muro.get("Revestimiento_Interior")) and str(fila_muro.get("Revestimiento_Interior", "")).strip():
                        st.write(
                            f"**Revestimiento interior:** {fila_muro.get('Revestimiento_Interior')} "
                            f"({_texto_valor_futuro(fila_muro.get('Espesor_Rev_Int_mm'), 1, ' mm')})"
                        )
                    if pd.notna(fila_muro.get("Aislante_Entre_Estructura")) and str(fila_muro.get("Aislante_Entre_Estructura", "")).strip():
                        st.write(
                            f"**Aislación entre estructura:** {fila_muro.get('Aislante_Entre_Estructura')} "
                            f"({_texto_valor_futuro(fila_muro.get('Espesor_Aislante_mm'), 1, ' mm')})"
                        )
                    if pd.notna(fila_muro.get("Placa_Estructural")) and str(fila_muro.get("Placa_Estructural", "")).strip():
                        st.write(
                            f"**Placa estructural:** {fila_muro.get('Placa_Estructural')} "
                            f"({_texto_valor_futuro(fila_muro.get('Espesor_Placa_mm'), 1, ' mm')})"
                        )
                    if pd.notna(fila_muro.get("Aislacion_Exterior")) and str(fila_muro.get("Aislacion_Exterior", "")).strip():
                        st.write(
                            f"**Aislación exterior:** {fila_muro.get('Aislacion_Exterior')} "
                            f"({_texto_valor_futuro(fila_muro.get('Espesor_Aislacion_Ext_mm'), 1, ' mm')})"
                        )
                    if pd.notna(fila_muro.get("Barrera_Humedad")) and str(fila_muro.get("Barrera_Humedad", "")).strip():
                        st.write(f"**Barrera de humedad:** {fila_muro.get('Barrera_Humedad')}")
                    if pd.notna(fila_muro.get("Revestimiento_Exterior")) and str(fila_muro.get("Revestimiento_Exterior", "")).strip():
                        esp_ext = fila_muro.get("Espesor_Rev_Ext_mm")
                        texto_esp_ext = "" if pd.isna(esp_ext) else f" ({float(esp_ext):.1f} mm)"
                        st.write(f"**Revestimiento exterior:** {fila_muro.get('Revestimiento_Exterior')}{texto_esp_ext}")
                    if pd.notna(fila_muro.get("Barrera_Vapor")) and str(fila_muro.get("Barrera_Vapor", "")).strip():
                        st.write(f"**Barrera de vapor:** {fila_muro.get('Barrera_Vapor')}")
                    st.caption(f"Fuente: {fila_muro.get('Fuente', '')}")

                st.warning(
                    "🔥 La compatibilidad térmica de esta solución **no acredita por sí sola resistencia al fuego, "
                    "estabilidad estructural ni condiciones de encuentro**. Esas materias deben revisarse por separado."
                )

        # ------------------------------------------
        # 6.1 B MURO ESPECIAL DE ADOSAMIENTO F-60
        # ------------------------------------------
        st.markdown("##### 🔥 Muro especial de adosamiento F-60")

        if hay_adosamiento_futuro:
            st.warning(
                "El croquis detectó **uno o más tramos de la futura ampliación adosados al deslinde**. "
                "Para esos tramos debe acreditarse una resistencia al fuego mínima **F-60**. "
                "Los muros térmicos generales seleccionados arriba no acreditan automáticamente esta condición."
            )

            filas_f60 = pd.DataFrame()
            if base_muros_futura is not None and not base_muros_futura.empty:
                mascara_f60 = base_muros_futura.apply(
                    lambda r: (
                        "adosamiento" in str(r.get("Uso_Especial", "") or "").lower()
                        or str(r.get("Resistencia_Fuego", "") or "").strip().upper() == "F-60"
                        or str(r.get("Codigo_Solucion", "") or "").strip().upper() == "ASIM.1.60.24"
                    ),
                    axis=1
                )
                filas_f60 = base_muros_futura[mascara_f60]

            if filas_f60.empty:
                st.error(
                    "❌ No se encontró la solución **ASIM.1.60.24** en la hoja `Soluciones_Muros`. "
                    "Actualiza también la base Excel que acompaña esta versión del software."
                )
                revision_emplazamiento_futura["pendientes"].append(
                    "Definir/acreditar solución F-60 para el muro de adosamiento."
                )
            else:
                fila_f60 = filas_f60.iloc[0]
                solucion_muro_adosamiento_futura = _fila_a_dict_seguro(fila_f60)

                st.success(
                    f"✅ **Solución de referencia para el tramo adosado:** "
                    f"{fila_f60.get('Codigo_Solucion', '')} — {fila_f60.get('Sistema', '')}. "
                    f"Clasificación: **{fila_f60.get('Resistencia_Fuego', 'F-60')}**."
                )

                with st.expander("🖼️ Ver detalle constructivo del muro F-60", expanded=True):
                    mostrar_imagen_solucion(
                        "muro_f60",
                        caption=(
                            "Muro N.º 4 — Entramado de madera para adosamiento. "
                            "Referencia ASIM.1.60.24 · resistencia al fuego F-60."
                        )
                    )

                c_f1, c_f2, c_f3 = st.columns(3)
                with c_f1:
                    st.metric("Resistencia al fuego", str(fila_f60.get("Resistencia_Fuego", "F-60")))
                with c_f2:
                    st.metric("Altura mínima muro", "2,00 m")
                with c_f3:
                    st.metric("Uso", "Adosamiento")

                with st.expander("🔎 Ver composición de la solución F-60"):
                    st.write(f"**Código:** {fila_f60.get('Codigo_Solucion', '')}")
                    st.write(f"**Estructura:** {fila_f60.get('Estructura_Principal', '')}")
                    st.write(
                        f"**Cara expuesta al fuego:** {fila_f60.get('Revestimiento_Interior', '')} "
                        f"({_texto_valor_futuro(fila_f60.get('Espesor_Rev_Int_mm'), 1, ' mm')})"
                    )
                    st.write(
                        f"**Aislación interior:** {fila_f60.get('Aislante_Entre_Estructura', '')} "
                        f"({_texto_valor_futuro(fila_f60.get('Espesor_Aislante_mm'), 1, ' mm')}; "
                        f"densidad nominal {_texto_valor_futuro(fila_f60.get('Densidad_Aislante_kg_m3'), 0, ' kg/m³')})"
                    )
                    st.write(
                        f"**Cara no expuesta:** {fila_f60.get('Placa_Estructural', '')} "
                        f"({_texto_valor_futuro(fila_f60.get('Espesor_Placa_mm'), 1, ' mm')})"
                    )
                    st.caption(f"Fuente fuego: {fila_f60.get('Fuente_Fuego') or fila_f60.get('Fuente', '')}")

                st.info(
                    "🌡️ **Importante:** la clasificación F-60 acredita el comportamiento frente al fuego. "
                    "Esta ficha **no asigna automáticamente U ni Rt**; si el muro forma parte de la envolvente térmica, "
                    "su desempeño para Zona D debe verificarse separadamente."
                )
        else:
            st.info(
                "ℹ️ En la posición actual del croquis no se detecta ampliación adosada al deslinde, por lo que "
                "la solución especial F-60 no se activa. Si acercas un módulo hasta el deslinde, esta revisión aparecerá automáticamente."
            )

        st.markdown("---")

        # ------------------------------------------
        # 6.2 PISO
        # ------------------------------------------
        st.markdown('<div class="amp-subtitulo">⬛ Piso</div>', unsafe_allow_html=True)
        st.caption(
            "La condición del piso se revisa de manera distinta según se trate de una ampliación apoyada sobre terreno, "
            "un piso expuesto/ventilado o un entrepiso interior."
        )

        try:
            base_pisos_futura = cargar_soluciones_pisos()
        except Exception:
            base_pisos_futura = None

        if base_pisos_futura is None or base_pisos_futura.empty:
            st.warning(
                "⚠️ No fue posible cargar **Soluciones_Pisos** desde la base normativa. "
                "Las soluciones de piso quedarán pendientes."
            )
        else:
            # Piso 1: normalmente apoyado sobre terreno, aunque se permite indicar una solución elevada/ventilada.
            if superficie_ampliacion_piso1 > 0:
                st.markdown("**Ampliación ubicada en Piso 1**")
                opciones_piso1 = ["Seleccione una solución..."]
                mapa_piso1 = {}
                for _, fila_op_p1 in base_pisos_futura.iterrows():
                    condicion_op = str(fila_op_p1.get("Condicion_Piso", "")).strip().lower()
                    if condicion_op not in {"apoyado sobre terreno", "ventilado"}:
                        continue
                    etiqueta_op = f"{fila_op_p1.get('Codigo_Solucion', '')} — {fila_op_p1.get('Sistema', '')}"
                    opciones_piso1.append(etiqueta_op)
                    mapa_piso1[etiqueta_op] = fila_op_p1

                piso1_elegido = st.selectbox(
                    "Solución propuesta para el piso de la ampliación en primer nivel:",
                    opciones_piso1,
                    key="futura_condicion_piso1_select"
                )

                if piso1_elegido in mapa_piso1:
                    fila_piso1 = mapa_piso1[piso1_elegido]
                    condicion_busqueda_p1 = str(fila_piso1.get("Condicion_Piso", ""))
                    coincidencias_p1 = base_pisos_futura.loc[[fila_piso1.name]]
                else:
                    condicion_busqueda_p1 = ""
                    coincidencias_p1 = base_pisos_futura.iloc[0:0]

                if not coincidencias_p1.empty:
                    fila_piso1 = coincidencias_p1.iloc[0]
                    solucion_piso1_futura = _fila_a_dict_seguro(fila_piso1)

                    st.write(
                        f"**Referencia seleccionada:** {fila_piso1.get('Codigo_Solucion', '')} — "
                        f"{fila_piso1.get('Sistema', '')}"
                    )

                    clave_img_piso1 = "piso_radier" if condicion_busqueda_p1 == "Apoyado sobre terreno" else "piso_ventilado"
                    with st.expander("🖼️ Ver detalle visual del piso seleccionado", expanded=True):
                        mostrar_imagen_solucion(
                            clave_img_piso1,
                            caption=f"Detalle visual de referencia — {fila_piso1.get('Sistema', '')}"
                        )

                    if condicion_busqueda_p1 == "Apoyado sobre terreno":
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.metric("Ripio de referencia", _texto_valor_futuro(fila_piso1.get("Cama_Ripio_mm"), 0, " mm"))
                        with c2:
                            st.metric("Radier de referencia", _texto_valor_futuro(fila_piso1.get("Radier_Hormigon_mm"), 0, " mm"))
                        with c3:
                            st.metric("R100 sobrecimiento", f"≥ {_texto_valor_futuro(fila_piso1.get('R100_Min_Sobrecimiento'), 0)}")

                        st.success(
                            "✅ Para esta alternativa, la revisión térmica considerada en el prototipo se concentra en la "
                            "**aislación exterior del sobrecimiento con R100 ≥ 45**. Los espesores de ripio y radier "
                            "corresponden a referencias constructivas adoptadas en la tesis y no a una exigencia general de la OGUC."
                        )
                    else:
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.metric("U referencia", _texto_valor_futuro(fila_piso1.get("U_W_m2K"), 2, " W/m²K"))
                        with c2:
                            st.metric("Rt referencia", _texto_valor_futuro(fila_piso1.get("Rt_m2K_W"), 2, " m²K/W"))
                        with c3:
                            st.metric("Zona D", str(fila_piso1.get("Compatibilidad_Zona_D", "Pendiente")))

                        st.success(
                            f"✅ Referencia para piso ventilado: **U ≤ {float(fila_piso1.get('U_Max_Zona_D')):.2f} W/m²K** "
                            f"o **Rt ≥ {float(fila_piso1.get('Rt_Min_Zona_D')):.2f} m²K/W**."
                        )

                    with st.expander("🔎 Ver composición/referencia del piso de Piso 1"):
                        st.write(f"**Sistema:** {fila_piso1.get('Sistema', '')}")
                        if condicion_busqueda_p1 == "Ventilado":
                            st.write(f"**Placa estructural:** {fila_piso1.get('Placa_Estructural', '')} aprox. {_texto_valor_futuro(fila_piso1.get('Espesor_Placa_Min_mm'), 1)}–{_texto_valor_futuro(fila_piso1.get('Espesor_Placa_Max_mm'), 1)} mm")
                            st.write(f"**Estructura:** {fila_piso1.get('Estructura_Principal', '')}")
                            st.write(f"**Aislante:** {fila_piso1.get('Aislante', '')}, {_texto_valor_futuro(fila_piso1.get('Espesor_Aislante_mm'), 0, ' mm')}")
                            st.write(f"**Barrera:** {fila_piso1.get('Barrera_Humedad_Viento', '')}")
                            st.write(f"**Revestimiento inferior:** {fila_piso1.get('Revestimiento_Inferior', '')}, {_texto_valor_futuro(fila_piso1.get('Espesor_Rev_Inferior_mm'), 0, ' mm')}")
                        else:
                            st.write(f"**Base:** ripio compactado de referencia {_texto_valor_futuro(fila_piso1.get('Cama_Ripio_mm'), 0, ' mm')}")
                            st.write(f"**Radier:** hormigón de referencia {_texto_valor_futuro(fila_piso1.get('Radier_Hormigon_mm'), 0, ' mm')}")
                            st.write(f"**Aislación térmica:** {fila_piso1.get('Aislacion_Sobrecimiento', '')}")
                        st.caption(f"Fuente: {fila_piso1.get('Fuente', '')}")

            # Piso 2: se distingue un entrepiso interior de un piso que forma parte de la envolvente por estar expuesto abajo.
            if superficie_ampliacion_piso2 > 0:
                st.markdown("**Ampliación ubicada en Piso 2**")
                opciones_piso2 = ["Seleccione una solución...", "Entrepiso sobre recinto cerrado — definición estructural"]
                mapa_piso2 = {}
                coincidencias_vent_p2 = base_pisos_futura[
                    base_pisos_futura["Condicion_Piso"].str.lower() == "ventilado"
                ]
                for _, fila_op_p2 in coincidencias_vent_p2.iterrows():
                    etiqueta_op = f"{fila_op_p2.get('Codigo_Solucion', '')} — {fila_op_p2.get('Sistema', '')}"
                    opciones_piso2.append(etiqueta_op)
                    mapa_piso2[etiqueta_op] = fila_op_p2

                piso2_elegido = st.selectbox(
                    "Solución propuesta para el piso del segundo nivel:",
                    opciones_piso2,
                    key="futura_condicion_piso2_select"
                )

                if piso2_elegido == "Entrepiso sobre recinto cerrado — definición estructural":
                    condicion_piso2_futura = "Entrepiso sobre recinto cerrado"
                    solucion_piso2_futura = {
                        "Condicion_Piso": condicion_piso2_futura,
                        "Codigo_Solucion": None,
                        "Sistema": "Definición estructural de entrepiso",
                        "Compatibilidad_Zona_D": "No evaluado como piso ventilado",
                        "Observacion": (
                            "Cuando el piso separa recintos interiores acondicionados, el prototipo no le asigna "
                            "automáticamente la exigencia U/Rt correspondiente a un piso ventilado. La solución estructural "
                            "del entrepiso debe definirse según el proyecto."
                        )
                    }
                    st.info(
                        "ℹ️ Este caso **no se compara automáticamente con la exigencia térmica de piso ventilado**, "
                        "porque el elemento puede no formar parte de la envolvente térmica exterior. La estructura del "
                        "entrepiso debe ser definida y revisada según las condiciones reales del proyecto."
                    )
                elif piso2_elegido in mapa_piso2:
                    condicion_piso2_futura = "Piso expuesto/ventilado hacia el exterior"
                    fila_piso2 = mapa_piso2[piso2_elegido]
                    coincidencias_p2 = base_pisos_futura.loc[[fila_piso2.name]]
                    if not coincidencias_p2.empty:
                        solucion_piso2_futura = _fila_a_dict_seguro(fila_piso2)

                        with st.expander("🖼️ Ver detalle visual del piso ventilado", expanded=True):
                            mostrar_imagen_solucion(
                                "piso_ventilado",
                                caption=f"Detalle visual de referencia — {fila_piso2.get('Codigo_Solucion', '')} · {fila_piso2.get('Sistema', '')}"
                            )

                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.metric("U referencia", _texto_valor_futuro(fila_piso2.get("U_W_m2K"), 2, " W/m²K"))
                        with c2:
                            st.metric("Rt referencia", _texto_valor_futuro(fila_piso2.get("Rt_m2K_W"), 2, " m²K/W"))
                        with c3:
                            st.metric("Zona D", str(fila_piso2.get("Compatibilidad_Zona_D", "Pendiente")))

                        st.success(
                            f"✅ Se propone como referencia **{fila_piso2.get('Codigo_Solucion', '')} — {fila_piso2.get('Sistema', '')}**."
                        )
                        st.warning(
                            "🏗️ En una ampliación de segundo piso, esta selección térmica no sustituye la revisión de la "
                            "capacidad resistente de la vivienda existente ni el diseño estructural del nuevo entrepiso."
                        )

            if superficie_ampliacion_piso1 <= 0 and superficie_ampliacion_piso2 <= 0:
                st.caption("Ingrese superficie de ampliación para habilitar la selección de piso correspondiente.")

        st.markdown("---")

        # ------------------------------------------
        # 6.3 TECHUMBRE
        # ------------------------------------------
        st.markdown('<div class="amp-subtitulo">🏠 Techumbre</div>', unsafe_allow_html=True)

        try:
            base_techumbres_futura = cargar_soluciones_techumbres()
        except Exception:
            base_techumbres_futura = None

        if base_techumbres_futura is None or base_techumbres_futura.empty:
            st.warning(
                "⚠️ No fue posible cargar **Soluciones_Techumbres** desde la base normativa. "
                "La solución de techumbre quedará pendiente."
            )
        else:
            opciones_tech_futura = ["Seleccione una solución...", "Definir otra solución con profesional"]
            mapa_tech_futura = {}

            for _, fila_tech in base_techumbres_futura.iterrows():
                etiqueta = f"{fila_tech['Codigo_Solucion']} — {fila_tech['Sistema']}"
                opciones_tech_futura.insert(-1, etiqueta)
                mapa_tech_futura[etiqueta] = fila_tech

            tech_elegida_futura = st.selectbox(
                "Solución propuesta para la techumbre de la ampliación:",
                opciones_tech_futura,
                key="futura_solucion_techumbre"
            )

            if tech_elegida_futura in mapa_tech_futura:
                fila_tech = mapa_tech_futura[tech_elegida_futura]
                solucion_techumbre_futura = _fila_a_dict_seguro(fila_tech)

                with st.expander("🖼️ Ver detalle visual de la techumbre", expanded=True):
                    mostrar_imagen_solucion(
                        "techumbre_madera",
                        caption=f"Detalle visual de referencia — {fila_tech.get('Codigo_Solucion', '')} · {fila_tech.get('Sistema', '')}"
                    )

                col_t1, col_t2, col_t3 = st.columns(3)
                with col_t1:
                    st.metric("U referencia", _texto_valor_futuro(fila_tech.get("U_W_m2K"), 2, " W/m²K"))
                with col_t2:
                    st.metric("Rt referencia", _texto_valor_futuro(fila_tech.get("Rt_m2K_W"), 2, " m²K/W"))
                with col_t3:
                    st.metric("Zona D", str(fila_tech.get("Compatibilidad_Zona_D", "Pendiente")))

                st.success(
                    f"✅ La solución de referencia presenta **U = {float(fila_tech.get('U_W_m2K')):.2f} W/m²K** y "
                    f"**Rt = {float(fila_tech.get('Rt_m2K_W')):.2f} m²K/W**, frente a una referencia Zona D de "
                    f"**U ≤ {float(fila_tech.get('U_Max_Zona_D')):.2f}** o **Rt ≥ {float(fila_tech.get('Rt_Min_Zona_D')):.2f}**."
                )

                with st.expander("🔎 Ver composición de la techumbre seleccionada"):
                    st.write(f"**Código:** {fila_tech.get('Codigo_Solucion', '')}")
                    st.write(f"**Geometría:** {fila_tech.get('Geometria', '')}")
                    st.write(f"**Cielo interior:** {fila_tech.get('Cielo_Interior', '')}, {_texto_valor_futuro(fila_tech.get('Espesor_Cielo_mm'), 0, ' mm')}")
                    st.write(f"**Listoneado:** {fila_tech.get('Listoneado_Cielo', '')}")
                    st.write(f"**Aislación:** {fila_tech.get('Aislante', '')}, {_texto_valor_futuro(fila_tech.get('Espesor_Aislante_mm'), 0, ' mm')}")
                    st.write(f"**Estructura:** {fila_tech.get('Estructura_Principal', '')}")
                    st.write(f"**Separación referencial de cerchas:** {_texto_valor_futuro(fila_tech.get('Separacion_Cerchas_cm'), 0, ' cm')}")
                    st.write(f"**Entretecho:** {fila_tech.get('Espacio_Entretecho', '')} — {fila_tech.get('Ventilacion_Entretecho', '')}")
                    st.write(f"**Cubierta exterior:** {fila_tech.get('Cubierta_Exterior', '')}")
                    st.write(f"**Barrera de vapor:** {fila_tech.get('Barrera_Vapor', '')}")
                    st.caption(f"Fuente: {fila_tech.get('Fuente', '')}")

            elif tech_elegida_futura == "Definir otra solución con profesional":
                solucion_techumbre_futura = {
                    "Codigo_Solucion": None,
                    "Sistema": "Otra solución por definir",
                    "Compatibilidad_Zona_D": "Pendiente de acreditación",
                    "Observacion": (
                        "La solución deberá demostrar el desempeño térmico correspondiente mediante un antecedente técnico "
                        "válido, como solución acreditada, ensayo o memoria de cálculo, según corresponda."
                    )
                }
                st.warning(
                    "⚠️ La solución queda **pendiente de acreditación técnica**. No se asignan automáticamente valores U o Rt."
                )

        # ------------------------------------------
        # 6.4 RESUMEN TÉCNICO
        # ------------------------------------------
        st.markdown('<div class="amp-subtitulo">📋 Especificación Técnica Preliminar</div>', unsafe_allow_html=True)

        nombre_muro_futura = (
            f"{solucion_muro_futura.get('Codigo_Solucion')} — {solucion_muro_futura.get('Sistema')}"
            if solucion_muro_futura
            else "Pendiente de selección"
        )
        nombre_piso1_futura = (
            f"{solucion_piso1_futura.get('Codigo_Solucion') or 'Sin código'} — {solucion_piso1_futura.get('Sistema', '')}"
            if solucion_piso1_futura
            else ("No aplica" if superficie_ampliacion_piso1 <= 0 else "Pendiente")
        )
        nombre_piso2_futura = (
            f"{solucion_piso2_futura.get('Codigo_Solucion') or 'Sin código'} — {solucion_piso2_futura.get('Sistema', '')}"
            if solucion_piso2_futura
            else ("No aplica" if superficie_ampliacion_piso2 <= 0 else "Pendiente")
        )
        nombre_tech_futura = (
            f"{solucion_techumbre_futura.get('Codigo_Solucion') or 'Sin código'} — {solucion_techumbre_futura.get('Sistema', '')}"
            if solucion_techumbre_futura
            else "Pendiente de selección"
        )

        resumen_soluciones_futura = pd.DataFrame(
            [
                {"Elemento": "Muro perimetral", "Solución propuesta": nombre_muro_futura},
                {
                    "Elemento": "Muro de adosamiento F-60",
                    "Solución propuesta": (
                        f"{solucion_muro_adosamiento_futura.get('Codigo_Solucion')} — {solucion_muro_adosamiento_futura.get('Sistema')}"
                        if solucion_muro_adosamiento_futura
                        else ("No aplica" if not hay_adosamiento_futuro else "Pendiente de acreditación")
                    )
                },
                {"Elemento": "Piso ampliación Piso 1", "Solución propuesta": nombre_piso1_futura},
                {"Elemento": "Piso ampliación Piso 2", "Solución propuesta": nombre_piso2_futura},
                {"Elemento": "Techumbre", "Solución propuesta": nombre_tech_futura},
            ]
        )
        st.dataframe(resumen_soluciones_futura, use_container_width=True, hide_index=True)

        pendientes_tecnicos_futura = []
        if solucion_muro_futura is None:
            pendientes_tecnicos_futura.append("muro perimetral")
        if hay_adosamiento_futuro and solucion_muro_adosamiento_futura is None:
            pendientes_tecnicos_futura.append("muro de adosamiento F-60")
        if superficie_ampliacion_piso1 > 0 and solucion_piso1_futura is None:
            pendientes_tecnicos_futura.append("piso de la ampliación en Piso 1")
        if superficie_ampliacion_piso2 > 0 and solucion_piso2_futura is None:
            pendientes_tecnicos_futura.append("piso de la ampliación en Piso 2")
        if solucion_techumbre_futura is None:
            pendientes_tecnicos_futura.append("techumbre")
        if revision_emplazamiento_futura.get("pendientes"):
            pendientes_tecnicos_futura.append("altura / emplazamiento de uno o más módulos")

        if pendientes_tecnicos_futura:
            st.warning(
                "⚠️ La propuesta todavía tiene definiciones técnicas pendientes: "
                + ", ".join(pendientes_tecnicos_futura)
                + ". Puedes guardar el diseño igualmente y completarlas después."
            )
        else:
            st.success(
                "✅ La propuesta cuenta con una definición preliminar de muro, piso y techumbre para los elementos que corresponden."
            )

        st.caption(
            "Estas alternativas son referencias técnicas del prototipo. La ejecución debe considerar encuentros, fijaciones, "
            "continuidad de aislación, humedad, condensación, resistencia al fuego, estructura e instalaciones según corresponda."
        )

        st.markdown("---")

        # ==========================================
        # 7. ESTACIONAMIENTOS SEGÚN PRC SAN MIGUEL
        # ==========================================
        st.markdown("""
        <div class="amp-section amp-estacionamientos">
            <span class="numero">7</span><span class="titulo">🚗 Estacionamientos según PRC de San Miguel</span>
            <span class="descripcion">Calcula la dotación preliminar de estacionamientos según la superficie total proyectada de la vivienda.</span>
        </div>
        """, unsafe_allow_html=True)
        st.write(
            "El PRC establece una dotación de estacionamientos para uso vivienda según la superficie "
            "de cada unidad. Para este prototipo se considera **una vivienda unifamiliar** y la superficie "
            "total proyectada después de la ampliación."
        )

        # Estándares residenciales del art. 14 del PRC. Las Zonas C y E poseen los mismos
        # estándares para vivienda dentro del alcance de este prototipo. Las cifras intermedias
        # resultantes deben aproximarse al entero superior.
        if vivienda_total_proyectada <= 35:
            factor_estacionamiento = 1 / 5
            tramo_estacionamiento = "0 a 35 m²"
            regla_estacionamiento = "1 estacionamiento por cada 5 viviendas"
        elif vivienda_total_proyectada <= 50:
            factor_estacionamiento = 1 / 4
            tramo_estacionamiento = "Más de 35 y hasta 50 m²"
            regla_estacionamiento = "1 estacionamiento por cada 4 viviendas"
        elif vivienda_total_proyectada <= 100:
            factor_estacionamiento = 1 / 3
            tramo_estacionamiento = "Más de 50 y hasta 100 m²"
            regla_estacionamiento = "1 estacionamiento por cada 3 viviendas"
        elif vivienda_total_proyectada <= 150:
            factor_estacionamiento = 1.0
            tramo_estacionamiento = "Más de 100 y hasta 150 m²"
            regla_estacionamiento = "1 estacionamiento por vivienda"
        else:
            factor_estacionamiento = 2.0
            tramo_estacionamiento = "Más de 150 m²"
            regla_estacionamiento = "2 estacionamientos por vivienda"

        numero_viviendas_estacionamiento = 1
        estacionamientos_requeridos = int(math.ceil(factor_estacionamiento * numero_viviendas_estacionamiento - 1e-12))

        est_col1, est_col2, est_col3 = st.columns(3)
        with est_col1:
            st.metric("Superficie final vivienda", f"{vivienda_total_proyectada:.2f} m²")
        with est_col2:
            st.metric("Tramo PRC", tramo_estacionamiento)
        with est_col3:
            st.metric("Dotación preliminar", f"{estacionamientos_requeridos} estacionamiento" + ("" if estacionamientos_requeridos == 1 else "s"))

        st.info(
            f"📘 **Regla utilizada:** {regla_estacionamiento}. Como el proyecto corresponde a una sola vivienda, "
            f"el cálculo da {factor_estacionamiento * numero_viviendas_estacionamiento:.2f} y el PRC indica que las "
            "cifras intermedias deben aproximarse al entero superior."
        )

        estacionamientos_disponibles = st.number_input(
            "¿Cuántos estacionamientos utilizables quedarán dentro del predio después de ejecutar la ampliación?",
            min_value=0,
            max_value=10,
            value=int(st.session_state.get("estacionamientos_disponibles_futura", 1)),
            step=1,
            key="estacionamientos_disponibles_futura_input",
            help=(
                "Indique cuántos espacios de estacionamiento podrán seguir utilizándose una vez construida la ampliación. "
                "El prototipo compara la cantidad, pero no valida automáticamente sus dimensiones, accesos ni maniobras."
            ),
        )
        st.session_state.estacionamientos_disponibles_futura = int(estacionamientos_disponibles)

        if estacionamientos_disponibles >= estacionamientos_requeridos:
            estado_estacionamientos = "✅ Compatible en cantidad"
            detalle_estacionamientos = (
                f"Se requieren preliminarmente {estacionamientos_requeridos} y se declaran "
                f"{int(estacionamientos_disponibles)} disponibles después de la ampliación."
            )
            st.success(
                f"✅ **Cantidad compatible preliminarmente:** se requieren {estacionamientos_requeridos} y quedarán "
                f"{int(estacionamientos_disponibles)} estacionamiento(s) utilizable(s)."
            )
        else:
            estado_estacionamientos = "❌ Revisar"
            detalle_estacionamientos = (
                f"Se requieren preliminarmente {estacionamientos_requeridos}, pero se declaran "
                f"{int(estacionamientos_disponibles)} disponibles después de la ampliación."
            )
            st.error(
                f"❌ **Falta dotación de estacionamientos:** el PRC arroja {estacionamientos_requeridos} "
                f"estacionamiento(s) y quedarían {int(estacionamientos_disponibles)}."
            )

        with st.expander("ℹ️ ¿Qué revisa y qué no revisa este cálculo?"):
            st.write(
                "• **Sí revisa:** la cantidad preliminar de estacionamientos según la superficie final de la vivienda.\n"
                "• **No revisa automáticamente:** dimensiones del cajón, radios de giro, ancho de acceso, rebajes de solera, "
                "pendientes de rampas ni otras condiciones particulares del proyecto.\n"
                "• Para vivienda, los estándares indicados por el PRC son equivalentes en las Zonas C y E consideradas para estacionamientos."
            )

        st.caption(
            "La revisión de estacionamientos es orientativa y se limita a la dotación cuantitativa incorporada al prototipo."
        )

        st.markdown("---")

        # ==========================================
        # 8. RESULTADO FINAL DE FUTURA AMPLIACIÓN
        # ==========================================
        st.markdown("""
        <div class="amp-section amp-resultado">
            <span class="numero">8</span><span class="titulo">📋 Resultado Final de la Revisión Preliminar</span>
            <span class="descripcion">Consolida compatibilidades, observaciones y antecedentes pendientes para facilitar una revisión profesional.</span>
        </div>
        """, unsafe_allow_html=True)
        st.write(
            "Este resumen reúne los principales resultados urbanísticos, geométricos y constructivos "
            "de la propuesta. Su resultado es **preliminar** y no constituye permiso, aprobación municipal "
            "ni reemplaza la revisión de un profesional competente."
        )

        incompatibilidades_finales_futura = []
        observaciones_finales_futura = []
        pendientes_finales_futura = []
        filas_resultado_final_futura = []

        # ------------------------------
        # Superficies / parámetros PRC
        # ------------------------------
        if superficie_maxima_ocupacion_guardada is None:
            estado_ocupacion = "⚠️ Pendiente"
            detalle_ocupacion = "No existe un valor PRC disponible para revisar preliminarmente la ocupación de suelo."
            pendientes_finales_futura.append("Verificar ocupación de suelo con un coeficiente PRC disponible.")
        elif margen_ocupacion_proyectada is not None and margen_ocupacion_proyectada >= -1e-9:
            estado_ocupacion = "✅ Compatible"
            detalle_ocupacion = (
                f"Piso 1 proyectado: {piso1_proyectado:.2f} m² / máximo preliminar: "
                f"{superficie_maxima_ocupacion_guardada:.2f} m²."
            )
        else:
            estado_ocupacion = "❌ Revisar"
            detalle_ocupacion = (
                f"Piso 1 proyectado: {piso1_proyectado:.2f} m² / máximo preliminar: "
                f"{superficie_maxima_ocupacion_guardada:.2f} m²."
            )
            incompatibilidades_finales_futura.append(
                f"La ocupación de suelo proyectada excede el máximo preliminar en {abs(float(margen_ocupacion_proyectada or 0)):.2f} m²."
            )

        filas_resultado_final_futura.append({
            "Área revisada": "Ocupación de suelo",
            "Estado": estado_ocupacion,
            "Detalle": detalle_ocupacion,
        })

        if superficie_maxima_construible_guardada is None:
            estado_construct = "⚠️ Pendiente"
            detalle_construct = "No existe un valor PRC disponible para revisar preliminarmente la constructibilidad."
            pendientes_finales_futura.append("Verificar constructibilidad con un coeficiente PRC disponible.")
        elif margen_constructibilidad_proyectada is not None and margen_constructibilidad_proyectada >= -1e-9:
            estado_construct = "✅ Compatible"
            detalle_construct = (
                f"Vivienda total proyectada: {vivienda_total_proyectada:.2f} m² / máximo preliminar: "
                f"{superficie_maxima_construible_guardada:.2f} m²."
            )
        else:
            estado_construct = "❌ Revisar"
            detalle_construct = (
                f"Vivienda total proyectada: {vivienda_total_proyectada:.2f} m² / máximo preliminar: "
                f"{superficie_maxima_construible_guardada:.2f} m²."
            )
            incompatibilidades_finales_futura.append(
                f"La superficie total proyectada excede la constructibilidad preliminar en {abs(float(margen_constructibilidad_proyectada or 0)):.2f} m²."
            )

        filas_resultado_final_futura.append({
            "Área revisada": "Constructibilidad",
            "Estado": estado_construct,
            "Detalle": detalle_construct,
        })

        # ------------------------------
        # Estacionamientos
        # ------------------------------
        filas_resultado_final_futura.append({
            "Área revisada": "Estacionamientos",
            "Estado": estado_estacionamientos,
            "Detalle": detalle_estacionamientos,
        })
        if estacionamientos_disponibles < estacionamientos_requeridos:
            incompatibilidades_finales_futura.append(
                f"La vivienda proyectada requiere preliminarmente {estacionamientos_requeridos} estacionamiento(s), "
                f"pero se declararon {int(estacionamientos_disponibles)} disponibles después de la ampliación."
            )

        # ------------------------------
        # Emplazamiento: distancias, rasante y antejardín
        # ------------------------------
        errores_emplazamiento = []
        observaciones_emplazamiento = []
        pendientes_emplazamiento = list(revision_emplazamiento_futura.get("pendientes", []))
        antejardin_ref_resumen = float(g_empl.get("antejardin_minimo", 0.0) or 0.0)
        invade_antejardin = False

        for modulo_rev in revision_emplazamiento_futura.get("modulos", []):
            numero_rev = modulo_rev.get("numero")
            piso_rev = modulo_rev.get("piso")
            if piso_rev == "Piso 1":
                frente_rev = float(modulo_rev.get("distancias", {}).get("frente", 0.0) or 0.0)
                if frente_rev + 1e-9 < antejardin_ref_resumen:
                    invade_antejardin = True
                    errores_emplazamiento.append(
                        f"Módulo {numero_rev}: invade la franja de antejardín de referencia "
                        f"({frente_rev:.2f} m < {antejardin_ref_resumen:.2f} m)."
                    )

            for lado_rev in modulo_rev.get("resultados_lados", []):
                estado_lado = lado_rev.get("estado")
                if estado_lado == "error":
                    lado_txt = str(lado_rev.get("lado", "deslinde")).lower()
                    errores_emplazamiento.append(
                        f"Módulo {numero_rev}: revisar distanciamiento/rasante hacia el {lado_txt}."
                    )
                elif estado_lado == "observacion":
                    observaciones_emplazamiento.append(
                        f"Módulo {numero_rev}: condición especial de adosamiento que requiere revisión adicional."
                    )
                elif estado_lado == "pendiente":
                    pendientes_emplazamiento.append(
                        f"Módulo {numero_rev}: completar altura para revisar emplazamiento."
                    )

        if errores_emplazamiento:
            estado_emplazamiento = "❌ Revisar"
            detalle_emplazamiento = "Se detectaron incompatibilidades preliminares de antejardín, distanciamiento o rasante."
            incompatibilidades_finales_futura.extend(errores_emplazamiento)
        elif pendientes_emplazamiento:
            estado_emplazamiento = "⚠️ Pendiente"
            detalle_emplazamiento = "Faltan antecedentes para cerrar la revisión de uno o más módulos."
            pendientes_finales_futura.extend(pendientes_emplazamiento)
        else:
            estado_emplazamiento = "✅ Compatible"
            detalle_emplazamiento = "No se detectaron conflictos preliminares de antejardín, distanciamiento o rasante simplificada."

        filas_resultado_final_futura.append({
            "Área revisada": "Emplazamiento",
            "Estado": estado_emplazamiento,
            "Detalle": detalle_emplazamiento,
        })

        # ------------------------------
        # Adosamiento y F-60
        # ------------------------------
        adosamientos_fuera_40 = []
        for lado_ados, info_ados in revision_emplazamiento_futura.get("adosamientos", {}).items():
            if float(info_ados.get("longitud_futura_m", 0.0) or 0.0) > 0 and not bool(info_ados.get("cumple_limite_general_40", True)):
                adosamientos_fuera_40.append(
                    f"{lado_ados}: {float(info_ados.get('porcentaje_preliminar', 0.0) or 0.0):.1f}%"
                )

        if not hay_adosamiento_futuro:
            estado_adosamiento = "✅ No aplica"
            detalle_adosamiento = "No se detectaron tramos futuros en contacto con deslindes."
        elif solucion_muro_adosamiento_futura is None:
            estado_adosamiento = "⚠️ Pendiente"
            detalle_adosamiento = "Existe adosamiento futuro y falta acreditar/definir el muro F-60."
            pendientes_finales_futura.append("Definir o acreditar la solución F-60 del muro de adosamiento.")
        elif adosamientos_fuera_40:
            estado_adosamiento = "⚠️ Revisión especial"
            detalle_adosamiento = (
                "El muro F-60 está identificado, pero el porcentaje general de adosamiento supera 40% en: "
                + ", ".join(adosamientos_fuera_40)
                + ". Debe revisarse si procede una excepción."
            )
            observaciones_finales_futura.append(detalle_adosamiento)
        else:
            estado_adosamiento = "✅ Referencia F-60 incorporada"
            detalle_adosamiento = (
                f"Se detectó adosamiento y se incorporó {solucion_muro_adosamiento_futura.get('Codigo_Solucion') or 'solución de referencia'} "
                f"con clasificación {solucion_muro_adosamiento_futura.get('Resistencia_Fuego') or 'F-60'}. "
                "La envolvente de 45° y aguas lluvia quedan para revisión profesional."
            )
            observaciones_finales_futura.append(
                "El adosamiento requiere verificar profesionalmente la envolvente de 45° y la evacuación de aguas lluvia."
            )

        filas_resultado_final_futura.append({
            "Área revisada": "Adosamiento / fuego",
            "Estado": estado_adosamiento,
            "Detalle": detalle_adosamiento,
        })

        # ------------------------------
        # Soluciones constructivas
        # ------------------------------
        def _estado_solucion_resumen(solucion, aplica=True):
            if not aplica:
                return "✅ No aplica", "No corresponde para esta propuesta."
            if solucion is None:
                return "⚠️ Pendiente", "No se ha seleccionado una solución."
            compat = str(solucion.get("Compatibilidad_Zona_D", "") or "").lower()
            if "pendiente" in compat:
                return "⚠️ Pendiente", str(solucion.get("Observacion", "Requiere acreditación técnica adicional."))
            codigo = solucion.get("Codigo_Solucion") or "Sin código"
            sistema = solucion.get("Sistema") or "Solución seleccionada"
            return "✅ Definida", f"{codigo} — {sistema}"

        estado_muro_res, detalle_muro_res = _estado_solucion_resumen(solucion_muro_futura, True)
        estado_p1_res, detalle_p1_res = _estado_solucion_resumen(
            solucion_piso1_futura, superficie_ampliacion_piso1 > 0
        )
        estado_p2_res, detalle_p2_res = _estado_solucion_resumen(
            solucion_piso2_futura, superficie_ampliacion_piso2 > 0
        )
        estado_tech_res, detalle_tech_res = _estado_solucion_resumen(solucion_techumbre_futura, True)

        soluciones_resumen = [
            ("Muro perimetral", estado_muro_res, detalle_muro_res),
            ("Piso ampliación Piso 1", estado_p1_res, detalle_p1_res),
            ("Piso ampliación Piso 2", estado_p2_res, detalle_p2_res),
            ("Techumbre", estado_tech_res, detalle_tech_res),
        ]
        for area_sol, estado_sol, detalle_sol in soluciones_resumen:
            filas_resultado_final_futura.append({
                "Área revisada": area_sol,
                "Estado": estado_sol,
                "Detalle": detalle_sol,
            })
            if estado_sol.startswith("⚠️"):
                pendientes_finales_futura.append(f"Completar/acreditar {area_sol.lower()}.")

        # ------------------------------
        # Alertas estructurales y antecedentes generales
        # ------------------------------
        if vivienda_total_proyectada >= 100:
            observaciones_finales_futura.append(
                f"La vivienda proyectada alcanza {vivienda_total_proyectada:.2f} m²; debe verificarse si corresponde proyecto de cálculo estructural."
            )
        if superficie_ampliacion_piso2 > 0 and datos.get("superficie_piso2", 0) <= 0:
            observaciones_finales_futura.append(
                "La propuesta incorpora un nuevo segundo piso; debe revisarse la capacidad resistente de la vivienda existente."
            )

        ubicaciones_faltantes_resumen = [
            m.get("numero") for m in modulos_ampliacion
            if float(m.get("superficie", 0) or 0) > 0
            and m.get("piso") == "Piso 1"
            and m.get("ubicacion") == "Seleccione una ubicación..."
        ]
        if ubicaciones_faltantes_resumen:
            pendientes_finales_futura.append(
                "Definir ubicación referencial de los módulos de Piso 1: "
                + ", ".join(str(n) for n in ubicaciones_faltantes_resumen)
                + "."
            )

        # Evitar duplicados conservando el orden.
        incompatibilidades_finales_futura = list(dict.fromkeys(incompatibilidades_finales_futura))
        observaciones_finales_futura = list(dict.fromkeys(observaciones_finales_futura))
        pendientes_finales_futura = list(dict.fromkeys(pendientes_finales_futura))

        # ------------------------------
        # Presentación del resumen
        # ------------------------------
        resumen_col1, resumen_col2, resumen_col3, resumen_col4 = st.columns(4)
        with resumen_col1:
            st.metric("Vivienda actual", f"{datos['superficie_total_vivienda']:.2f} m²")
        with resumen_col2:
            st.metric("Ampliación propuesta", f"{superficie_total_ampliacion:.2f} m²")
        with resumen_col3:
            st.metric("Total proyectado", f"{vivienda_total_proyectada:.2f} m²")
        with resumen_col4:
            st.metric("Módulos", str(len([m for m in modulos_ampliacion if float(m.get('superficie', 0) or 0) > 0])))

        st.dataframe(
            pd.DataFrame(filas_resultado_final_futura),
            use_container_width=True,
            hide_index=True,
        )

        if incompatibilidades_finales_futura:
            resultado_global_futura = "❌ Presenta incompatibilidades preliminares"
            st.error(
                "❌ **La propuesta presenta una o más incompatibilidades preliminares.** "
                "Conviene modificar el diseño o revisar los antecedentes antes de avanzar con una definición formal."
            )
        elif pendientes_finales_futura or observaciones_finales_futura:
            resultado_global_futura = "⚠️ Compatible preliminarmente con observaciones"
            st.warning(
                "⚠️ **La propuesta es compatible preliminarmente en los parámetros evaluados, pero mantiene observaciones, "
                "antecedentes pendientes o revisiones profesionales que deben resolverse.**"
            )
        else:
            resultado_global_futura = "✅ Compatible preliminarmente"
            st.success(
                "✅ **Con los antecedentes ingresados, no se detectaron incompatibilidades preliminares en los parámetros "
                "automatizados por el prototipo.**"
            )

        if incompatibilidades_finales_futura:
            with st.expander("❌ Ver incompatibilidades detectadas", expanded=True):
                for item in incompatibilidades_finales_futura:
                    st.write(f"• {item}")

        if observaciones_finales_futura:
            with st.expander("⚠️ Ver observaciones y revisiones complementarias", expanded=False):
                for item in observaciones_finales_futura:
                    st.write(f"• {item}")

        if pendientes_finales_futura:
            with st.expander("📝 Ver antecedentes pendientes", expanded=False):
                for item in pendientes_finales_futura:
                    st.write(f"• {item}")

        st.caption(
            "El resultado resume únicamente las reglas incorporadas al prototipo. No constituye un permiso de edificación, "
            "una aprobación de la DOM ni una certificación estructural, térmica o de resistencia al fuego del proyecto ejecutado."
        )

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
                        ),
                        "estacionamientos_requeridos": int(estacionamientos_requeridos),
                        "estacionamientos_disponibles": int(estacionamientos_disponibles),
                        "tramo_estacionamiento_prc": tramo_estacionamiento,
                        "regla_estacionamiento_prc": regla_estacionamiento,
                        "posiciones_puzzle": {
                            clave: dict(valor)
                            for clave, valor in st.session_state.posiciones_puzzle.items()
                        },
                        "posiciones_vivienda": {
                            clave: dict(valor)
                            for clave, valor in st.session_state.posiciones_vivienda.items()
                        },
                        "solucion_muro": solucion_muro_futura,
                        "solucion_muro_adosamiento_f60": solucion_muro_adosamiento_futura,
                        "hay_adosamiento_futuro": bool(hay_adosamiento_futuro),
                        "solucion_piso1": solucion_piso1_futura,
                        "solucion_piso2": solucion_piso2_futura,
                        "solucion_techumbre": solucion_techumbre_futura,
                        "revision_emplazamiento": revision_emplazamiento_futura,
                        "pendientes_tecnicos": list(pendientes_tecnicos_futura),
                        "resultado_global": resultado_global_futura,
                        "resumen_final": list(filas_resultado_final_futura),
                        "incompatibilidades_finales": list(incompatibilidades_finales_futura),
                        "observaciones_finales": list(observaciones_finales_futura),
                        "pendientes_finales": list(pendientes_finales_futura),
                    }

                    st.success("✅ **Propuesta de ampliación guardada correctamente.**")
                    st.info(
                        "🗺️ Se guardaron los módulos, su distribución y las soluciones constructivas seleccionadas. "
                        "Si algún elemento quedó pendiente, podrás completarlo posteriormente."
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
                if propuesta.get("resultado_global"):
                    st.write(f"**Resultado global:** {propuesta.get('resultado_global')}")
                if propuesta.get("estacionamientos_requeridos") is not None:
                    st.write(
                        f"**Estacionamientos:** {propuesta.get('estacionamientos_disponibles', 0)} disponibles / "
                        f"{propuesta.get('estacionamientos_requeridos', 0)} requeridos preliminarmente"
                    )

                st.markdown("**Módulos:**")

                for modulo in propuesta["modulos"]:
                    rotacion = " — Rotado 90°" if modulo.get("rotado", False) else ""
                    st.write(
                        f"• Módulo {modulo['numero']} — {modulo['piso']} — "
                        f"{modulo['largo']:.2f} m × {modulo['ancho']:.2f} m — "
                        f"{modulo['superficie']:.2f} m² — {modulo['ubicacion']}{rotacion}"
                    )

                revision_guardada = propuesta.get("revision_emplazamiento", {})
                if revision_guardada:
                    st.markdown("**Revisión de emplazamiento guardada:**")
                    n_obs = len(revision_guardada.get("observaciones", []))
                    n_pend = len(revision_guardada.get("pendientes", []))
                    st.write(
                        f"• Módulos revisados: {len(revision_guardada.get('modulos', []))} · "
                        f"Observaciones: {n_obs} · Pendientes: {n_pend}"
                    )

                st.markdown("**Soluciones constructivas guardadas:**")

                sol_muro_guardada = propuesta.get("solucion_muro")
                if sol_muro_guardada:
                    st.write(
                        f"• **Muro:** {sol_muro_guardada.get('Codigo_Solucion') or 'Sin código'} — "
                        f"{sol_muro_guardada.get('Sistema', '')}"
                    )
                else:
                    st.write("• **Muro:** Pendiente")

                sol_p1_guardada = propuesta.get("solucion_piso1")
                if sol_p1_guardada:
                    st.write(
                        f"• **Piso ampliación Piso 1:** {sol_p1_guardada.get('Codigo_Solucion') or 'Sin código'} — "
                        f"{sol_p1_guardada.get('Sistema', '')}"
                    )
                elif propuesta.get("superficie_ampliacion_piso1", 0) > 0:
                    st.write("• **Piso ampliación Piso 1:** Pendiente")

                sol_p2_guardada = propuesta.get("solucion_piso2")
                if sol_p2_guardada:
                    st.write(
                        f"• **Piso ampliación Piso 2:** {sol_p2_guardada.get('Codigo_Solucion') or 'Sin código'} — "
                        f"{sol_p2_guardada.get('Sistema', '')}"
                    )
                elif propuesta.get("superficie_ampliacion_piso2", 0) > 0:
                    st.write("• **Piso ampliación Piso 2:** Pendiente")

                sol_tech_guardada = propuesta.get("solucion_techumbre")
                if sol_tech_guardada:
                    st.write(
                        f"• **Techumbre:** {sol_tech_guardada.get('Codigo_Solucion') or 'Sin código'} — "
                        f"{sol_tech_guardada.get('Sistema', '')}"
                    )
                else:
                    st.write("• **Techumbre:** Pendiente")

                if propuesta.get("pendientes_tecnicos"):
                    st.warning(
                        "⚠️ Pendientes técnicos guardados: "
                        + ", ".join(propuesta.get("pendientes_tecnicos", []))
                    )

            st.markdown("""
            <div class="amp-pdf">
                <div class="amp-pdf-titulo">📄 Informe PDF para revisión profesional</div>
            </div>
            """, unsafe_allow_html=True)
            st.write(
                "Descarga una ficha técnica preliminar con los datos del predio, la futura ampliación, "
                "el croquis del puzle, verificaciones normativas, estacionamientos y las especificaciones "
                "de las soluciones constructivas seleccionadas."
            )
            st.caption(
                "El PDF está pensado como antecedente de apoyo para que un profesional pueda revisar la propuesta con mayor facilidad."
            )

            if REPORTLAB_DISPONIBLE:
                try:
                    pdf_informe = generar_informe_pdf_futura_ampliacion(datos, propuesta)
                    if pdf_informe:
                        st.download_button(
                            label="📥 Descargar informe preliminar en PDF",
                            data=pdf_informe,
                            file_name="Informe_Preliminar_Futura_Ampliacion_San_Miguel.pdf",
                            mime="application/pdf",
                            type="primary",
                            use_container_width=True,
                            key="descargar_pdf_futura_ampliacion",
                        )
                except Exception as error_pdf:
                    st.error(
                        "No fue posible generar el PDF en esta sesión. Verifica que `reportlab` esté instalado "
                        "y vuelve a intentar. Detalle: " + str(error_pdf)
                    )
            else:
                st.warning(
                    "⚠️ Para habilitar la descarga PDF en Streamlit debe instalarse la dependencia `reportlab`. "
                    "Sube también el archivo `requirements.txt` entregado con esta versión."
                )

        st.markdown("---")
        st.info(
            "✅ **Ruta de Futura Ampliación consolidada.** La propuesta integra geometría, ocupación y constructibilidad, "
            "emplazamiento, adosamiento, soluciones constructivas y dotación preliminar de estacionamientos. "
            "Las siguientes etapas se orientan al diseño visual y a los casos de prueba del prototipo."
        )

# ==========================================
# PANTALLA 4: REGULARIZACIÓN LEY N.º 20.898
# ==========================================
elif menu_seleccionado == "📋 Regularización Ley 20.898":

    st.markdown("""
    <div class="reg-hero">
        <h2>📋 Regularización de Edificación Existente — Ley N.º 20.898</h2>
        <p>Ruta orientativa para viviendas existentes sin regularizar · evaluación preliminar de requisitos, condiciones técnicas y antecedentes para revisión profesional.</p>
    </div>
    <div class="reg-pasos">
        <div class="reg-paso reg-p1"><span>1</span>Datos del inmueble</div>
        <div class="reg-paso reg-p2"><span>2</span>Condiciones generales</div>
        <div class="reg-paso reg-p3"><span>3</span>Vía orientativa</div>
        <div class="reg-paso reg-p4"><span>4</span>Revisión urbana</div>
        <div class="reg-paso reg-p5"><span>5</span>Condiciones técnicas</div>
        <div class="reg-paso reg-p6"><span>6</span>Muro existente</div>
        <div class="reg-paso reg-p7"><span>7</span>Piso existente</div>
        <div class="reg-paso reg-p8"><span>8</span>Techumbre</div>
        <div class="reg-paso reg-p9"><span>9</span>Documentos</div>
        <div class="reg-paso reg-p10"><span>10</span>Resultado</div>
    </div>
    <div class="reg-aviso">
        <strong>⚠️ Alcance de esta ruta:</strong> el resultado es únicamente orientativo. No constituye aprobación, permiso, recepción definitiva ni certificación de cumplimiento. La procedencia del procedimiento debe ser revisada por un profesional competente y por la Dirección de Obras Municipales.
    </div>
    """, unsafe_allow_html=True)

    opciones_si_no = ["Seleccione una opción...", "Sí", "No", "No estoy seguro/a"]

    # Variables que se utilizarán durante toda la evaluación.
    superficie_terreno_reg = 0.0
    superficie_piso1_reg = 0.0
    superficie_piso2_reg = 0.0
    superficie_otros_pisos_reg = 0.0
    superficie_regularizar = 0.0
    numero_pisos_reg = 1
    zona_regularizacion = "Seleccione una zona..."
    zona_codigo_reg = None
    fuente_datos_regularizacion = "Ingreso manual"
    coef_ocupacion_suelo_real = None
    coef_ocupacion_piso2_real = None
    coef_constructibilidad_real = None
    coef_ocupacion_relevante_art3 = None
    norma_prc_regularizacion = None
    coef_ocupacion_prc_reg = None
    coef_constructibilidad_prc_reg = None
    zona_residencial_automatica = None
    evaluacion_ocupacion_art3 = "No evaluada"
    evaluacion_constructibilidad_art3 = "No evaluada"
    resultado_muro_regularizacion = {
        "estado": "No evaluado",
        "sistema_ingresado": None,
        "codigo_referencia": None,
        "u_referencia": None,
        "rt_referencia": None,
        "diferencias": [],
    }
    resultado_piso_regularizacion = {
        "estado": "No evaluado",
        "sistema_ingresado": None,
        "codigo_referencia": None,
        "u_referencia": None,
        "rt_referencia": None,
        "diferencias": [],
    }
    resultado_techumbre_regularizacion = {
        "estado": "No evaluado",
        "sistema_ingresado": None,
        "codigo_referencia": None,
        "u_referencia": None,
        "rt_referencia": None,
        "diferencias": [],
    }

    # Estados consolidados que alimentan el resultado final de regularización.
    evaluacion_habitabilidad_reg = {
        "estado": "No evaluado",
        "observaciones": [],
    }
    evaluacion_seguridad_reg = {
        "estado": "No evaluado",
        "observaciones": [],
    }
    evaluacion_estabilidad_reg = {
        "estado": "No evaluado",
        "observaciones": [],
    }

    # Valores por defecto de la revisión técnica. Se inicializan aquí para que
    # el resumen final funcione tanto para Art. 1° como para Art. 3°.
    altura_cielo = None
    locales_habitables_ventilan = "No aplica"
    zonas_humedas_sin_ventana = "No aplica"
    ducto_016 = "No aplica"
    resistencia_f15 = "No aplica"
    vivienda_adosada = "No aplica"
    resistencia_f60 = "No aplica"
    materialidad_estructura = "No evaluado"
    luz_maxima = 0.0
    orientacion_calculo = "No evaluada"

    # ==========================================
    # 1. DATOS DEL INMUEBLE A REGULARIZAR
    # ==========================================
    st.markdown("""
    <div class="reg-section reg-datos">
        <span class="numero">1</span><span class="titulo">🏠 Datos del Inmueble a Regularizar</span>
        <span class="descripcion">Reúne la geometría, superficie, zona PRC y avalúo fiscal de la edificación existente.</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption(
        "Estos datos permiten calcular la ocupación real del predio y la constructibilidad de la edificación existente. "
        "Si ya completaste 'Datos del Terreno', puedes reutilizar esa información."
    )

    tiene_datos_guardados = st.session_state.datos_propiedad is not None

    if tiene_datos_guardados:
        modo_datos_regularizacion = st.radio(
            "¿Cómo deseas ingresar los datos geométricos?",
            ["Usar datos guardados de la propiedad", "Ingresar datos manualmente"],
            horizontal=True,
            key="reg_modo_datos"
        )
    else:
        modo_datos_regularizacion = "Ingresar datos manualmente"
        st.info(
            "ℹ️ No existen datos guardados desde el módulo 'Datos del Terreno'. "
            "Puedes ingresar aquí los antecedentes de la vivienda existente."
        )

    if modo_datos_regularizacion == "Usar datos guardados de la propiedad":
        datos_reg = st.session_state.datos_propiedad
        fuente_datos_regularizacion = "Datos guardados de la propiedad"

        superficie_terreno_reg = float(datos_reg.get("superficie_terreno", 0.0) or 0.0)
        superficie_piso1_reg = float(datos_reg.get("superficie_piso1", 0.0) or 0.0)
        superficie_piso2_reg = float(datos_reg.get("superficie_piso2", 0.0) or 0.0)
        superficie_otros_pisos_reg = 0.0
        superficie_regularizar = float(datos_reg.get("superficie_total_vivienda", 0.0) or 0.0)
        numero_pisos_reg = 2 if superficie_piso2_reg > 0 else 1
        zona_regularizacion = datos_reg.get("zona_completa", "Seleccione una zona...")
        zona_codigo_reg = datos_reg.get("zona_codigo")

        st.success("✅ Se utilizarán los antecedentes guardados en 'Datos del Terreno'.")

        guard_col1, guard_col2, guard_col3, guard_col4 = st.columns(4)
        with guard_col1:
            st.metric("🌳 Terreno", f"{superficie_terreno_reg:.2f} m²")
        with guard_col2:
            st.metric("🏠 Piso 1", f"{superficie_piso1_reg:.2f} m²")
        with guard_col3:
            st.metric("🏘️ Piso 2", f"{superficie_piso2_reg:.2f} m²")
        with guard_col4:
            st.metric("📐 Total existente", f"{superficie_regularizar:.2f} m²")

        st.caption(
            f"Zona guardada: **{zona_regularizacion}** · Número de pisos identificado: **{numero_pisos_reg}**"
        )

    else:
        fuente_datos_regularizacion = "Ingreso manual"
        st.markdown('<div class="reg-subtitulo">📐 Geometría existente</div>', unsafe_allow_html=True)

        man_col1, man_col2 = st.columns(2)
        with man_col1:
            superficie_terreno_reg = st.number_input(
                "Superficie total del terreno (m²):",
                min_value=0.0,
                value=0.0,
                step=0.10,
                format="%.2f",
                key="reg_superficie_terreno_manual"
            )
        with man_col2:
            numero_pisos_reg = st.selectbox(
                "Número de pisos de la edificación existente:",
                [1, 2, "3 o más"],
                key="reg_numero_pisos_manual"
            )

        pisos_col1, pisos_col2 = st.columns(2)
        with pisos_col1:
            superficie_piso1_reg = st.number_input(
                "Superficie construida del Piso 1 (m²):",
                min_value=0.0,
                value=0.0,
                step=0.10,
                format="%.2f",
                key="reg_superficie_piso1_manual"
            )

        with pisos_col2:
            if numero_pisos_reg in [2, "3 o más"]:
                superficie_piso2_reg = st.number_input(
                    "Superficie construida del Piso 2 (m²):",
                    min_value=0.0,
                    value=0.0,
                    step=0.10,
                    format="%.2f",
                    key="reg_superficie_piso2_manual"
                )
            else:
                superficie_piso2_reg = 0.0
                st.metric("Superficie Piso 2", "0,00 m²")

        if numero_pisos_reg == "3 o más":
            superficie_otros_pisos_reg = st.number_input(
                "Superficie construida conjunta de los pisos 3 y superiores (m²):",
                min_value=0.0,
                value=0.0,
                step=0.10,
                format="%.2f",
                key="reg_superficie_otros_pisos_manual"
            )
            st.warning(
                "⚠️ El prototipo desarrolla la revisión geométrica detallada principalmente para viviendas de hasta dos pisos. "
                "En edificaciones de tres o más pisos, algunas verificaciones quedarán sujetas a revisión profesional."
            )
        else:
            superficie_otros_pisos_reg = 0.0

        superficie_regularizar = (
            float(superficie_piso1_reg)
            + float(superficie_piso2_reg)
            + float(superficie_otros_pisos_reg)
        )

        st.metric("🏠 Superficie edificada total calculada", f"{superficie_regularizar:.2f} m²")

        zona_regularizacion = st.selectbox(
            "Zona según Plan Regulador Comunal de San Miguel:",
            [
                "Seleccione una zona...",
                "ZU-1 - Comercial Preferente y Residencial",
                "ZU-2 - Residencial de Renovación",
                "ZU-3 - Industrial Exclusiva",
                "ZU-4 - Industrial Mixta",
                "ZU-5 - Equipamiento Regional de Salud",
                "ZU-6 - Ferroviaria",
                "No estoy seguro/a"
            ],
            key="reg_zona_manual"
        )

        if zona_regularizacion.startswith("ZU-"):
            zona_codigo_reg = zona_regularizacion.split(" - ")[0]

    st.markdown('<div class="reg-subtitulo">💰 Avalúo fiscal</div>', unsafe_allow_html=True)
    avaluo_fiscal_uf = st.number_input(
        "Avalúo fiscal de la vivienda (UF):",
        min_value=0.0,
        value=0.0,
        step=10.0,
        format="%.2f",
        key="reg_avaluo"
    )

    # Cálculos geométricos reales de la edificación existente.
    if superficie_terreno_reg > 0:
        coef_ocupacion_suelo_real = superficie_piso1_reg / superficie_terreno_reg
        coef_constructibilidad_real = superficie_regularizar / superficie_terreno_reg

        if superficie_piso2_reg > 0:
            coef_ocupacion_piso2_real = superficie_piso2_reg / superficie_terreno_reg
            coef_ocupacion_relevante_art3 = max(
                coef_ocupacion_suelo_real,
                coef_ocupacion_piso2_real
            )
        else:
            coef_ocupacion_piso2_real = 0.0
            coef_ocupacion_relevante_art3 = coef_ocupacion_suelo_real

        calc_col1, calc_col2, calc_col3 = st.columns(3)
        with calc_col1:
            st.metric("Coef. ocupación real Piso 1", f"{coef_ocupacion_suelo_real:.2f}")
        with calc_col2:
            if superficie_piso2_reg > 0:
                st.metric("Coef. ocupación real Piso 2", f"{coef_ocupacion_piso2_real:.2f}")
            else:
                st.metric("Coef. ocupación real Piso 2", "No aplica")
        with calc_col3:
            st.metric("Coef. constructibilidad real", f"{coef_constructibilidad_real:.2f}")
    else:
        st.info("ℹ️ Ingresa la superficie del terreno para calcular los coeficientes reales de la edificación.")

    # Consulta de la base PRC como referencia, sin mezclarla automáticamente con las excepciones de la ley.
    base_normativa_reg = None
    try:
        base_normativa_reg = cargar_base_normativa()
    except Exception:
        base_normativa_reg = None

    if base_normativa_reg is not None and zona_codigo_reg:
        filas_zona_reg = base_normativa_reg[
            base_normativa_reg["Zona"].str.upper() == zona_codigo_reg.upper()
        ].copy()

        if not filas_zona_reg.empty:
            zona_residencial_automatica = bool(
                (filas_zona_reg["Residencial_General"].str.upper() == "SI").any()
            )

            if zona_residencial_automatica:
                st.success(
                    f"✅ La zona **{zona_codigo_reg}** se encuentra registrada en la base del prototipo como compatible "
                    "con uso residencial general."
                )
            else:
                st.warning(
                    f"⚠️ La zona **{zona_codigo_reg}** no se encuentra registrada como zona de uso residencial general. "
                    "Este antecedente requiere revisión antes de continuar con una orientación de regularización residencial."
                )

        if superficie_terreno_reg > 0:
            norma_prc_regularizacion = buscar_norma_residencial(
                base_normativa_reg,
                zona_codigo_reg,
                superficie_terreno_reg
            )

            if norma_prc_regularizacion is not None:
                if pd.notna(norma_prc_regularizacion["Coef_Ocupacion_1a3_Pisos"]):
                    coef_ocupacion_prc_reg = float(
                        norma_prc_regularizacion["Coef_Ocupacion_1a3_Pisos"]
                    )
                if pd.notna(norma_prc_regularizacion["Coef_Constructibilidad"]):
                    coef_constructibilidad_prc_reg = float(
                        norma_prc_regularizacion["Coef_Constructibilidad"]
                    )

                with st.expander("📚 Ver coeficientes PRC de referencia del predio"):
                    st.write(f"**Zona:** {zona_codigo_reg}")
                    st.write(
                        f"**Tramo aplicado:** {formatear_tramo_m2(norma_prc_regularizacion['Tramo_Superficie_PRC'])}"
                    )
                    if coef_ocupacion_prc_reg is not None:
                        st.write(f"**Coeficiente de ocupación PRC:** {coef_ocupacion_prc_reg:.2f}")
                    if coef_constructibilidad_prc_reg is not None:
                        st.write(f"**Coeficiente de constructibilidad PRC:** {coef_constructibilidad_prc_reg:.2f}")
                    st.caption(
                        "Estos valores se muestran como referencia. En el artículo 3° existen excepciones específicas "
                        "que se evalúan separadamente en este módulo."
                    )

    # ==========================================
    # 2. CONDICIONES GENERALES
    # ==========================================
    st.markdown("""
    <div class="reg-section reg-condiciones">
        <span class="numero">2</span><span class="titulo">🧭 Condiciones Generales de la Edificación Existente</span>
        <span class="descripcion">Revisa antecedentes básicos que permiten orientar si la vivienda puede continuar por una vía especial de regularización.</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption(
        "Responde según los antecedentes disponibles. Cuando no tengas certeza, selecciona "
        "'No estoy seguro/a' para que el sistema mantenga la condición como pendiente de revisión."
    )

    reg_col1, reg_col2 = st.columns(2)

    with reg_col1:
        sin_recepcion = st.selectbox(
            "¿La vivienda no cuenta con recepción definitiva total o parcial?",
            opciones_si_no,
            key="reg_sin_recepcion"
        )
        construida_antes_ley = st.selectbox(
            "¿La edificación existía antes de la publicación de la Ley N.º 20.898?",
            opciones_si_no,
            key="reg_antiguedad"
        )

        if zona_residencial_automatica is True:
            uso_residencial = "Sí"
            st.info(
                f"🏘️ **Uso residencial:** se utilizará la compatibilidad registrada para la zona {zona_codigo_reg}."
            )
        elif zona_residencial_automatica is False:
            uso_residencial = "No"
            st.warning(
                f"🏘️ **Uso residencial:** la base normativa no identifica la zona {zona_codigo_reg} como residencial general."
            )
        else:
            uso_residencial = st.selectbox(
                "Si el predio está en área urbana, ¿el uso de suelo admite vivienda?",
                opciones_si_no,
                key="reg_uso_residencial"
            )

    with reg_col2:
        area_restringida = st.selectbox(
            "¿La vivienda se ubica en área de riesgo/protección, terreno declarado de utilidad pública o bien nacional de uso público?",
            opciones_si_no,
            key="reg_area_restringida"
        )
        reclamaciones = st.selectbox(
            "¿Existen reclamaciones escritas pendientes por incumplimiento de normas urbanísticas?",
            opciones_si_no,
            key="reg_reclamaciones"
        )
        st.info(
            "📅 El procedimiento considerado en esta investigación mantiene como referencia "
            "el plazo señalado en la Ley N.º 20.898 hasta el **31 de diciembre de 2027**."
        )

    # ==========================================
    # 3. EVALUACIÓN DE ACCESO
    # ==========================================
    st.markdown("""
    <div class="reg-section reg-ruta">
        <span class="numero">3</span><span class="titulo">🌳 Árbol de Orientación del Procedimiento</span>
        <span class="descripcion">Relaciona los antecedentes ingresados con los umbrales del artículo 1° o artículo 3°, sin constituir una calificación definitiva.</span>
    </div>
    """, unsafe_allow_html=True)

    respuestas_obligatorias = [
        sin_recepcion,
        construida_antes_ley,
        uso_residencial,
        area_restringida,
        reclamaciones,
    ]

    faltan_respuestas = any(r == "Seleccione una opción..." for r in respuestas_obligatorias)
    hay_incertidumbre = any(r == "No estoy seguro/a" for r in respuestas_obligatorias)

    condiciones_comunes_confirmadas = (
        sin_recepcion == "Sí"
        and construida_antes_ley == "Sí"
        and uso_residencial == "Sí"
        and area_restringida == "No"
        and reclamaciones == "No"
    )

    impedimento_confirmado = (
        sin_recepcion == "No"
        or construida_antes_ley == "No"
        or uso_residencial == "No"
        or area_restringida == "Sí"
        or reclamaciones == "Sí"
    )

    posible_art1 = (
        condiciones_comunes_confirmadas
        and superficie_regularizar > 0
        and superficie_regularizar <= 90
        and avaluo_fiscal_uf > 0
        and avaluo_fiscal_uf <= 1000
    )

    posible_art3 = (
        condiciones_comunes_confirmadas
        and superficie_regularizar > 0
        and superficie_regularizar <= 140
        and avaluo_fiscal_uf > 0
        and avaluo_fiscal_uf <= 2000
    )

    procedimiento_orientativo = "Pendiente"

    if faltan_respuestas or superficie_regularizar <= 0 or avaluo_fiscal_uf <= 0:
        st.info(
            "ℹ️ Completa las preguntas, la geometría de la vivienda y el avalúo fiscal para obtener una orientación preliminar."
        )

    elif impedimento_confirmado:
        procedimiento_orientativo = "No se identifica acceso preliminar"
        st.error(
            "❌ Con los antecedentes ingresados existe al menos una condición que impide identificar "
            "preliminarmente el acceso a los procedimientos analizados de la Ley N.º 20.898."
        )
        st.caption(
            "El resultado no determina la situación jurídica definitiva del inmueble. Corresponde revisar "
            "los antecedentes específicos con un profesional competente y la DOM."
        )

    elif hay_incertidumbre:
        procedimiento_orientativo = "Requiere antecedentes adicionales"
        st.warning(
            "⚠️ Existen respuestas marcadas como 'No estoy seguro/a'. No es posible determinar una ruta "
            "preliminar sin verificar esos antecedentes."
        )

    elif posible_art1:
        procedimiento_orientativo = "Artículo 1°"
        st.success(
            "✅ **Orientación preliminar: condiciones compatibles con el procedimiento del artículo 1°.**"
        )
        st.write(
            f"La superficie edificada total calculada es **{superficie_regularizar:.2f} m²** "
            f"(referencia: hasta 90 m²) y el avalúo informado es **{avaluo_fiscal_uf:.2f} UF** "
            "(referencia: hasta 1.000 UF)."
        )
        st.info(
            "Esta ruta considera exigencias técnicas especiales de habitabilidad, seguridad contra incendios "
            "y estabilidad. Los coeficientes urbanísticos se muestran como información de contexto, pero no se "
            "aplican en este prototipo como el mismo filtro utilizado para una futura ampliación."
        )

    elif posible_art3:
        procedimiento_orientativo = "Artículo 3°"
        st.success(
            "✅ **Orientación preliminar: condiciones compatibles con el procedimiento del artículo 3°.**"
        )
        st.write(
            f"La superficie edificada total calculada es **{superficie_regularizar:.2f} m²** "
            f"(referencia: hasta 140 m²) y el avalúo informado es **{avaluo_fiscal_uf:.2f} UF** "
            "(referencia: hasta 2.000 UF)."
        )
        st.warning(
            "⚠️ En esta vía deben cumplirse las normas de habitabilidad, estabilidad y seguridad que correspondan. "
            "Además, determinadas normas urbanísticas cuentan con excepciones específicas que deben evaluarse "
            "sin confundirlas con la revisión normal de una futura ampliación."
        )

    else:
        procedimiento_orientativo = "Fuera de los umbrales analizados"
        st.warning(
            "⚠️ Con la superficie y/o avalúo ingresados no se identifica preliminarmente ninguno de los "
            "dos procedimientos analizados en este prototipo (artículos 1° y 3°)."
        )
        if superficie_regularizar > 140:
            st.write("• La superficie informada supera **140 m²**.")
        if avaluo_fiscal_uf > 2000:
            st.write("• El avalúo informado supera **2.000 UF**.")

    # ==========================================
    # 4. REVISIÓN URBANÍSTICA ESPECIAL ARTÍCULO 3
    # ==========================================
    st.markdown("""
    <div class="reg-section reg-urbana">
        <span class="numero">4</span><span class="titulo">📐 Revisión Urbanística Especial</span>
        <span class="descripcion">Presenta las condiciones urbanísticas especiales consideradas para la vía del artículo 3° y las compara con los datos existentes.</span>
    </div>
    """, unsafe_allow_html=True)

    if procedimiento_orientativo == "Artículo 3°":
        st.caption(
            "En esta sección se evalúan separadamente las excepciones relacionadas con ocupación de suelo/pisos "
            "superiores y constructibilidad previstas para esta vía de regularización."
        )

        if superficie_terreno_reg <= 0:
            st.warning(
                "⚠️ No es posible calcular los coeficientes porque falta la superficie del terreno."
            )
        else:
            st.markdown('<div class="reg-subtitulo">📍 Coeficiente de ocupación</div>', unsafe_allow_html=True)

            ocup_col1, ocup_col2, ocup_col3 = st.columns(3)
            with ocup_col1:
                st.metric("Ocupación Piso 1", f"{coef_ocupacion_suelo_real:.2f}")
            with ocup_col2:
                if superficie_piso2_reg > 0:
                    st.metric("Ocupación Piso 2", f"{coef_ocupacion_piso2_real:.2f}")
                else:
                    st.metric("Ocupación Piso 2", "No aplica")
            with ocup_col3:
                st.metric("Límite especial Art. 3°", "0,80")

            if numero_pisos_reg == "3 o más":
                st.warning(
                    "⚠️ La edificación tiene tres o más pisos. El prototipo puede calcular la ocupación del Piso 1 y Piso 2, "
                    "pero no dispone del área individual de cada piso superior para revisar completamente este criterio."
                )

            if coef_ocupacion_relevante_art3 is not None:
                if coef_ocupacion_relevante_art3 <= 0.80 + 1e-9:
                    evaluacion_ocupacion_art3 = "Dentro del límite especial de 0,80"
                    st.success(
                        f"✅ El mayor coeficiente calculado entre las plantas informadas es **{coef_ocupacion_relevante_art3:.2f}**, "
                        "por lo que se encuentra dentro del límite especial de **0,80** considerado para esta excepción."
                    )
                else:
                    evaluacion_ocupacion_art3 = "Supera el límite especial de 0,80"
                    st.error(
                        f"❌ El mayor coeficiente calculado es **{coef_ocupacion_relevante_art3:.2f}**, superior a **0,80**. "
                        "Con estos antecedentes no puede asumirse la excepción especial de ocupación del artículo 3°."
                    )

            st.markdown('<div class="reg-subtitulo">🏗️ Coeficiente de constructibilidad</div>', unsafe_allow_html=True)
            cons_col1, cons_col2, cons_col3 = st.columns(3)
            with cons_col1:
                st.metric("Constructibilidad real", f"{coef_constructibilidad_real:.2f}")
            with cons_col2:
                st.metric("Número de pisos", str(numero_pisos_reg))
            with cons_col3:
                if coef_constructibilidad_prc_reg is not None:
                    st.metric("Coef. PRC de referencia", f"{coef_constructibilidad_prc_reg:.2f}")
                else:
                    st.metric("Coef. PRC de referencia", "No disponible")

            if numero_pisos_reg in [1, 2]:
                evaluacion_constructibilidad_art3 = "Excepción aplicable preliminarmente por altura ≤ 2 pisos"
                st.success(
                    "✅ La edificación informada no supera **dos pisos**. Para esta vía, el artículo 3° contempla "
                    "una excepción al coeficiente de constructibilidad bajo esa condición."
                )
                if (
                    coef_constructibilidad_prc_reg is not None
                    and coef_constructibilidad_real is not None
                    and coef_constructibilidad_real > coef_constructibilidad_prc_reg
                ):
                    st.info(
                        f"ℹ️ El coeficiente real (**{coef_constructibilidad_real:.2f}**) supera el valor PRC de referencia "
                        f"(**{coef_constructibilidad_prc_reg:.2f}**), pero esta diferencia no se utiliza aquí como rechazo "
                        "automático porque se está evaluando la excepción específica del artículo 3°."
                    )
            else:
                evaluacion_constructibilidad_art3 = "La excepción de constructibilidad no puede asumirse por superar 2 pisos"
                st.warning(
                    "⚠️ La edificación supera dos pisos. No debe aplicarse automáticamente la excepción al coeficiente "
                    "de constructibilidad prevista para construcciones de hasta dos pisos."
                )

                if coef_constructibilidad_prc_reg is not None and coef_constructibilidad_real is not None:
                    if coef_constructibilidad_real <= coef_constructibilidad_prc_reg + 1e-9:
                        st.success(
                            f"✅ Como referencia, el coeficiente real (**{coef_constructibilidad_real:.2f}**) no supera "
                            f"el coeficiente PRC identificado (**{coef_constructibilidad_prc_reg:.2f}**). "
                            "La situación completa debe ser revisada profesionalmente."
                        )
                    else:
                        st.error(
                            f"❌ Como referencia, el coeficiente real (**{coef_constructibilidad_real:.2f}**) supera "
                            f"el coeficiente PRC identificado (**{coef_constructibilidad_prc_reg:.2f}**). "
                            "Al no poder asumirse la excepción por altura, esta situación requiere revisión normativa específica."
                        )
                else:
                    st.info(
                        "ℹ️ No fue posible identificar automáticamente un coeficiente PRC residencial de referencia. "
                        "Debe revisarse la norma urbanística aplicable al predio."
                    )

        with st.expander("📚 Ver otras excepciones urbanísticas orientativas asociadas al artículo 3°"):
            st.write("• **Antejardines:** el procedimiento contempla una excepción específica.")
            st.write("• **Estacionamientos:** el procedimiento contempla una excepción específica.")
            st.write("• **Altura de cierros:** se exceptúa la norma correspondiente, manteniendo el límite señalado por la ley.")
            st.write("• **Adosamientos:** pueden existir excepciones, manteniéndose las condiciones técnicas que correspondan.")
            st.write("• **Constructibilidad:** la excepción se condiciona a que la construcción no supere dos pisos, incluyendo mansardas.")
            st.write("• **Ocupación de suelo o pisos superiores:** la excepción se considera mientras el coeficiente resultante no sea superior a 0,80.")

    elif procedimiento_orientativo == "Artículo 1°":
        st.info(
            "ℹ️ Para la orientación del artículo 1° este prototipo no aplica automáticamente los coeficientes de ocupación "
            "y constructibilidad del PRC como el mismo filtro utilizado para una futura ampliación. Los valores calculados "
            "se conservan como antecedentes geométricos de la vivienda existente."
        )
    else:
        st.info(
            "La revisión urbanística diferenciada se habilita cuando el árbol de orientación identifica una vía preliminar."
        )

    # ==========================================
    # 5. REVISIÓN TÉCNICA ARTÍCULO 1
    # ==========================================
    st.markdown("""
    <div class="reg-section reg-tecnica">
        <span class="numero">5</span><span class="titulo">🧱 Revisión Técnica Orientativa</span>
        <span class="descripcion">Organiza condiciones de habitabilidad, seguridad, resistencia al fuego y antecedentes estructurales de la vivienda existente.</span>
    </div>
    """, unsafe_allow_html=True)

    if procedimiento_orientativo == "Artículo 1°":
        st.caption(
            "Estas preguntas representan condiciones técnicas identificadas para el procedimiento del artículo 1°. "
            "Su revisión no reemplaza la declaración ni el informe del profesional competente."
        )

        tec_col1, tec_col2 = st.columns(2)

        with tec_col1:
            altura_cielo = st.number_input(
                "Altura mínima piso a cielo medida en obra terminada (m):",
                min_value=0.0,
                value=2.00,
                step=0.05,
                format="%.2f",
                key="reg_altura_cielo"
            )
            locales_habitables_ventilan = st.selectbox(
                "¿Los locales habitables cuentan al menos con una ventana que permita entrada de aire y luz exterior?",
                opciones_si_no,
                key="reg_vent_habitables"
            )
            zonas_humedas_sin_ventana = st.selectbox(
                "¿Existen baños, cocinas o lavaderos sin ventana exterior para renovación de aire?",
                opciones_si_no,
                key="reg_zonas_humedas"
            )

            ducto_016 = "No aplica"
            if zonas_humedas_sin_ventana == "Sí":
                ducto_016 = st.selectbox(
                    "¿Cuentan con ducto de ventilación o solución equivalente conforme a la condición aplicable?",
                    opciones_si_no,
                    key="reg_ducto_016"
                )

        with tec_col2:
            resistencia_f15 = st.selectbox(
                "Para el caso analizado, ¿los elementos/componentes soportantes cuentan con antecedente de resistencia al fuego F-15 cuando corresponde?",
                opciones_si_no,
                key="reg_f15"
            )
            vivienda_adosada = st.selectbox(
                "¿La edificación está adosada a un deslinde?",
                opciones_si_no,
                key="reg_adosada"
            )

            resistencia_f60 = "No aplica"
            if vivienda_adosada == "Sí":
                resistencia_f60 = st.selectbox(
                    "¿El muro de adosamiento cuenta con antecedente F-60 y llega hasta la cubierta del cuerpo adosado?",
                    opciones_si_no,
                    key="reg_f60"
                )

            materialidad_estructura = st.selectbox(
                "Sistema estructural predominante de la vivienda:",
                [
                    "Seleccione una opción...",
                    "Estructura de madera",
                    "Albañilería armada/reforzada u hormigón armado",
                    "Sistema mixto de 2 pisos",
                    "Otro / No estoy seguro/a"
                ],
                key="reg_materialidad"
            )
            luz_maxima = st.number_input(
                "Mayor distancia libre entre apoyos en habitaciones (m):",
                min_value=0.0,
                value=0.0,
                step=0.10,
                format="%.2f",
                key="reg_luz_apoyos"
            )

        # Consolidación de habitabilidad para el resultado final.
        observaciones_hab = []
        hab_incumplimiento = False
        hab_pendiente = False

        if altura_cielo < 2.00:
            hab_incumplimiento = True
            observaciones_hab.append(
                f"Altura piso-cielo informada ({altura_cielo:.2f} m) inferior a la referencia de 2,00 m."
            )

        if locales_habitables_ventilan == "No":
            hab_incumplimiento = True
            observaciones_hab.append("Se informó falta de ventilación/iluminación exterior en locales habitables.")
        elif locales_habitables_ventilan not in ["Sí", "No"]:
            hab_pendiente = True
            observaciones_hab.append("Ventilación/iluminación de locales habitables pendiente de verificar.")

        if zonas_humedas_sin_ventana == "Sí":
            if ducto_016 == "No":
                hab_incumplimiento = True
                observaciones_hab.append("Recintos húmedos sin ventana informados sin solución de ventilación verificada.")
            elif ducto_016 != "Sí":
                hab_pendiente = True
                observaciones_hab.append("Solución de ventilación de recintos húmedos pendiente de verificar.")
        elif zonas_humedas_sin_ventana not in ["No", "Sí"]:
            hab_pendiente = True
            observaciones_hab.append("Existencia de recintos húmedos sin ventana pendiente de verificar.")

        if hab_incumplimiento:
            evaluacion_habitabilidad_reg = {
                "estado": "Presenta observaciones",
                "observaciones": observaciones_hab,
            }
        elif hab_pendiente:
            evaluacion_habitabilidad_reg = {
                "estado": "Requiere antecedentes",
                "observaciones": observaciones_hab,
            }
        else:
            evaluacion_habitabilidad_reg = {
                "estado": "Compatible preliminarmente",
                "observaciones": ["Las condiciones consultadas de habitabilidad no presentan observaciones con los datos ingresados."],
            }

        # Consolidación de seguridad contra incendios para el resultado final.
        observaciones_seg = []
        seg_incumplimiento = False
        seg_pendiente = False

        if resistencia_f15 == "No":
            seg_incumplimiento = True
            observaciones_seg.append("No se informó antecedente F-15 para los elementos/componentes soportantes cuando corresponde.")
        elif resistencia_f15 != "Sí":
            seg_pendiente = True
            observaciones_seg.append("Antecedente F-15 pendiente de verificar.")

        if vivienda_adosada == "Sí":
            if resistencia_f60 == "No":
                seg_incumplimiento = True
                observaciones_seg.append("Muro de adosamiento sin antecedente F-60/configuración acreditada según lo informado.")
            elif resistencia_f60 != "Sí":
                seg_pendiente = True
                observaciones_seg.append("Condición F-60 del muro de adosamiento pendiente de verificar.")
        elif vivienda_adosada not in ["No", "Sí"]:
            seg_pendiente = True
            observaciones_seg.append("Condición de adosamiento pendiente de verificar.")

        if seg_incumplimiento:
            evaluacion_seguridad_reg = {
                "estado": "Presenta observaciones",
                "observaciones": observaciones_seg,
            }
        elif seg_pendiente:
            evaluacion_seguridad_reg = {
                "estado": "Requiere antecedentes",
                "observaciones": observaciones_seg,
            }
        else:
            evaluacion_seguridad_reg = {
                "estado": "Compatible preliminarmente",
                "observaciones": ["Las condiciones de resistencia al fuego consultadas no presentan observaciones con los datos ingresados."],
            }

        # Consolidación de estabilidad. La salida nunca certifica estabilidad:
        # sólo informa si la configuración coincide preliminarmente con un caso especial.
        observaciones_est = []
        estabilidad_compatible = False
        estabilidad_pendiente = False

        if materialidad_estructura == "Estructura de madera":
            if luz_maxima <= 0:
                estabilidad_pendiente = True
                observaciones_est.append("Falta informar la mayor distancia libre entre apoyos.")
            elif numero_pisos_reg in [1, 2] and luz_maxima <= 3.0:
                estabilidad_compatible = True
                observaciones_est.append("Configuración compatible preliminarmente con el caso especial de estructura de madera; requiere declaración profesional.")
            else:
                observaciones_est.append("No puede asumirse el caso especial de estructura de madera con los datos ingresados.")
        elif materialidad_estructura == "Albañilería armada/reforzada u hormigón armado":
            if luz_maxima <= 0:
                estabilidad_pendiente = True
                observaciones_est.append("Falta informar la mayor distancia libre entre apoyos.")
            elif numero_pisos_reg == 1 and luz_maxima <= 3.0:
                estabilidad_compatible = True
                observaciones_est.append("Configuración compatible preliminarmente con el caso especial de un piso; requiere declaración profesional.")
            else:
                observaciones_est.append("No puede asumirse el caso especial de albañilería/hormigón con los datos ingresados.")
        elif materialidad_estructura == "Sistema mixto de 2 pisos":
            if luz_maxima <= 0:
                estabilidad_pendiente = True
                observaciones_est.append("Falta informar la mayor distancia libre entre apoyos.")
            elif numero_pisos_reg == 2 and luz_maxima <= 3.0:
                estabilidad_compatible = True
                observaciones_est.append("Configuración potencialmente compatible con el caso especial mixto; deben verificarse materialidad por nivel, entramado de piso y segundo piso liviano.")
            else:
                observaciones_est.append("No puede asumirse el caso especial del sistema mixto con los datos ingresados.")
        else:
            estabilidad_pendiente = True
            observaciones_est.append("Sistema estructural no identificado suficientemente para orientar la posible excepción de cálculo.")

        if estabilidad_compatible:
            evaluacion_estabilidad_reg = {
                "estado": "Compatible preliminarmente con caso especial",
                "observaciones": observaciones_est,
            }
        elif estabilidad_pendiente:
            evaluacion_estabilidad_reg = {
                "estado": "Requiere antecedentes",
                "observaciones": observaciones_est,
            }
        else:
            evaluacion_estabilidad_reg = {
                "estado": "Requiere revisión estructural",
                "observaciones": observaciones_est,
            }

        st.markdown('<div class="reg-subtitulo">🔎 Resultado técnico preliminar</div>', unsafe_allow_html=True)

        if altura_cielo >= 2.00:
            st.success(
                f"✅ Altura informada: **{altura_cielo:.2f} m**. Alcanza la referencia mínima de 2,00 m considerada para esta vía."
            )
        else:
            st.error(
                f"❌ Altura informada: **{altura_cielo:.2f} m**. Es inferior a la referencia de 2,00 m considerada para esta vía."
            )

        if locales_habitables_ventilan == "Sí":
            st.success("✅ Se informó ventilación/iluminación exterior en los locales habitables.")
        elif locales_habitables_ventilan == "No":
            st.error("❌ Se informó al menos una condición que requiere revisión de ventilación/iluminación en locales habitables.")
        else:
            st.info("ℹ️ La condición de ventilación de locales habitables quedó pendiente de verificar.")

        if zonas_humedas_sin_ventana == "Sí":
            if ducto_016 == "Sí":
                st.success("✅ Se informó una solución de ventilación para los recintos húmedos sin ventana exterior.")
            elif ducto_016 == "No":
                st.error("❌ Los recintos húmedos sin ventana exterior requieren revisar la solución de ventilación.")
            else:
                st.info("ℹ️ Debe verificarse la solución de ventilación de los recintos húmedos sin ventana exterior.")

        if resistencia_f15 == "No":
            st.error("❌ Debe revisarse el antecedente de resistencia al fuego de los elementos/componentes soportantes.")
        elif resistencia_f15 == "Sí":
            st.success("✅ Se informó antecedente F-15 cuando corresponde al caso analizado.")

        if vivienda_adosada == "Sí":
            if resistencia_f60 == "Sí":
                st.success("✅ Se informó antecedente F-60 para el muro de adosamiento.")
            elif resistencia_f60 == "No":
                st.error("❌ Debe revisarse la resistencia al fuego y configuración del muro de adosamiento.")
            else:
                st.info("ℹ️ La condición F-60 del muro de adosamiento quedó pendiente de verificar.")

        st.markdown('<div class="reg-subtitulo">🏗️ Orientación sobre proyecto de cálculo estructural</div>', unsafe_allow_html=True)
        orientacion_calculo = "Debe verificarse según OGUC y antecedentes del proyecto."

        if materialidad_estructura == "Estructura de madera" and luz_maxima > 0:
            if numero_pisos_reg in [1, 2] and luz_maxima <= 3.0:
                orientacion_calculo = (
                    "La configuración informada podría encontrarse dentro de uno de los casos especiales "
                    "considerados por la ley para estructura de madera, sujeto a las demás condiciones y a declaración profesional."
                )
            elif luz_maxima > 3.0:
                orientacion_calculo = "La luz informada supera 3,0 m; no debe asumirse la excepción por esta condición."
            else:
                orientacion_calculo = "La cantidad de pisos informada requiere una revisión específica antes de asumir la excepción."

        elif materialidad_estructura == "Albañilería armada/reforzada u hormigón armado" and luz_maxima > 0:
            if numero_pisos_reg == 1 and luz_maxima <= 3.0:
                orientacion_calculo = (
                    "La configuración informada podría encontrarse dentro del caso especial descrito para vivienda de un piso "
                    "en albañilería armada/reforzada u hormigón armado, sujeto a declaración profesional."
                )
            else:
                orientacion_calculo = (
                    "La excepción descrita para esta materialidad requiere, entre otras condiciones, máximo un piso y luces "
                    "entre apoyos no superiores a 3,0 m. Debe ser verificada por el profesional competente."
                )

        elif materialidad_estructura == "Sistema mixto de 2 pisos" and luz_maxima > 0:
            if numero_pisos_reg == 2 and luz_maxima <= 3.0:
                orientacion_calculo = (
                    "La ley contempla un caso especial para determinadas configuraciones mixtas de dos pisos. "
                    "Debe verificarse además la materialidad de cada nivel, el entramado de piso y la declaración profesional."
                )
            else:
                orientacion_calculo = (
                    "La configuración informada no permite asumir automáticamente el caso especial del sistema mixto. "
                    "Debe revisarse la cantidad de pisos, la luz entre apoyos y la configuración estructural completa."
                )

        st.info(f"🏗️ {orientacion_calculo}")

    elif procedimiento_orientativo == "Artículo 3°":
        evaluacion_habitabilidad_reg = {
            "estado": "Revisión OGUC requerida",
            "observaciones": ["El artículo 3° no utiliza las flexibilidades técnicas del artículo 1°; la habitabilidad debe revisarse según OGUC."],
        }
        evaluacion_seguridad_reg = {
            "estado": "Revisión OGUC requerida",
            "observaciones": ["La seguridad debe revisarse según OGUC y antecedentes específicos de la vivienda."],
        }
        evaluacion_estabilidad_reg = {
            "estado": "Revisión OGUC requerida",
            "observaciones": ["La estabilidad y la exigencia de proyecto de cálculo estructural deben determinarse según OGUC."],
        }
        st.info(
            "ℹ️ Para el artículo 3° deben cumplirse las normas de habitabilidad, estabilidad y seguridad de la OGUC. "
            "La revisión técnica específica se integrará con los módulos generales del prototipo, sin aplicar automáticamente "
            "las flexibilidades técnicas propias del artículo 1°."
        )
    else:
        st.info(
            "La revisión técnica diferenciada se habilita cuando el árbol de orientación identifica una vía preliminar."
        )

    # ==========================================
    # 6. REVISIÓN CONSTRUCTIVA Y TÉRMICA DE MUROS
    # ==========================================
    st.markdown("""
    <div class="reg-section reg-muros">
        <span class="numero">6</span><span class="titulo">🧱 Revisión Constructiva y Térmica del Muro Existente</span>
        <span class="descripcion">Compara la composición informada por el usuario con las soluciones de referencia seleccionadas para Zona Térmica D.</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption(
        "Describe el muro perimetral predominante de la vivienda. El prototipo comparará la configuración "
        "ingresada con las soluciones de referencia seleccionadas desde LOSCAT para la Zona Térmica D. "
        "La comparación es orientativa y no reemplaza una memoria de cálculo, ensayo o certificación profesional."
    )

    try:
        base_muros = cargar_soluciones_muros()
    except Exception:
        base_muros = None

    if base_muros is None or base_muros.empty:
        st.warning(
            "⚠️ No fue posible cargar la hoja **Soluciones_Muros** desde `Base_Normativa_PRC_San_Miguel.xlsx`. "
            "Para utilizar esta revisión debes subir también la versión actualizada de la base normativa."
        )
    else:
        opciones_sistema_muro = [
            "Seleccione una opción...",
            "Entramado de madera",
            "Entramado de acero galvanizado",
            "Albañilería con EIFS",
            "Otro sistema",
            "No sé cómo está construido",
        ]

        sistema_muro_reg = st.selectbox(
            "Sistema predominante del muro perimetral existente:",
            opciones_sistema_muro,
            key="reg_muro_sistema"
        )

        fila_ref_muro = None
        datos_muro_ingresados = {}
        diferencias_muro = []

        if sistema_muro_reg in [
            "Entramado de madera",
            "Entramado de acero galvanizado",
            "Albañilería con EIFS",
        ]:
            coincidencias = base_muros[
                base_muros["Sistema"].str.lower() == sistema_muro_reg.lower()
            ]

            if not coincidencias.empty:
                fila_ref_muro = coincidencias.iloc[0]

        if fila_ref_muro is not None:
            clave_img_reg_muro = clave_imagen_muro(sistema_muro_reg)
            if clave_img_reg_muro:
                with st.expander("🖼️ Ver solución visual de referencia", expanded=False):
                    mostrar_imagen_solucion(
                        clave_img_reg_muro,
                        caption=f"Referencia visual para comparar con el muro existente — {fila_ref_muro.get('Codigo_Solucion', '')}"
                    )
                    st.caption(
                        "La imagen sirve para reconocer la composición de referencia; por sí sola no demuestra que el muro existente coincida con ella."
                    )

        if sistema_muro_reg == "Entramado de madera":
            st.markdown('<div class="reg-subtitulo">🪵 Composición informada – entramado de madera</div>', unsafe_allow_html=True)
            muro_col1, muro_col2 = st.columns(2)

            with muro_col1:
                estructura_muro = st.selectbox(
                    "Estructura principal:",
                    ["No sé", "Pino 2x4", "Pino 2x3", "Otra"],
                    key="reg_muro_mad_estructura"
                )
                rev_int_muro = st.selectbox(
                    "Revestimiento interior:",
                    ["No sé", "Yeso-cartón", "Madera", "Sin revestimiento", "Otro"],
                    key="reg_muro_mad_rev_int"
                )
                esp_rev_int_muro = st.number_input(
                    "Espesor del revestimiento interior (mm):",
                    min_value=0.0, value=0.0, step=0.5, format="%.1f",
                    key="reg_muro_mad_esp_rev_int"
                )
                aislante_muro = st.selectbox(
                    "Aislante entre pies derechos:",
                    ["No sé", "Lana de fibra de vidrio", "Lana mineral", "EPS", "Sin aislación", "Otro"],
                    key="reg_muro_mad_aislante"
                )
                esp_aislante_muro = st.number_input(
                    "Espesor del aislante entre pies derechos (mm):",
                    min_value=0.0, value=0.0, step=5.0, format="%.1f",
                    key="reg_muro_mad_esp_aislante"
                )

            with muro_col2:
                placa_muro = st.selectbox(
                    "Placa estructural/exterior:",
                    ["No sé", "OSB estructural", "Terciado", "Sin placa", "Otra"],
                    key="reg_muro_mad_placa"
                )
                esp_placa_muro = st.number_input(
                    "Espesor de la placa (mm):",
                    min_value=0.0, value=0.0, step=0.5, format="%.1f",
                    key="reg_muro_mad_esp_placa"
                )
                aisl_ext_muro = st.selectbox(
                    "Aislación exterior:",
                    ["No sé", "EPS", "Lana mineral", "Sin aislación exterior", "Otra"],
                    key="reg_muro_mad_aisl_ext"
                )
                esp_aisl_ext_muro = st.number_input(
                    "Espesor de la aislación exterior (mm):",
                    min_value=0.0, value=0.0, step=5.0, format="%.1f",
                    key="reg_muro_mad_esp_aisl_ext"
                )
                rev_ext_muro = st.selectbox(
                    "Revestimiento exterior:",
                    ["No sé", "Fibrocemento", "Siding", "Madera", "Estuco", "Otro"],
                    key="reg_muro_mad_rev_ext"
                )
                esp_rev_ext_muro = st.number_input(
                    "Espesor del revestimiento exterior (mm):",
                    min_value=0.0, value=0.0, step=0.5, format="%.1f",
                    key="reg_muro_mad_esp_rev_ext"
                )

            datos_muro_ingresados = {
                "Estructura_Principal": estructura_muro,
                "Revestimiento_Interior": rev_int_muro,
                "Espesor_Rev_Int_mm": esp_rev_int_muro,
                "Aislante_Entre_Estructura": aislante_muro,
                "Espesor_Aislante_mm": esp_aislante_muro,
                "Placa_Estructural": placa_muro,
                "Espesor_Placa_mm": esp_placa_muro,
                "Aislacion_Exterior": aisl_ext_muro,
                "Espesor_Aislacion_Ext_mm": esp_aisl_ext_muro,
                "Revestimiento_Exterior": rev_ext_muro,
                "Espesor_Rev_Ext_mm": esp_rev_ext_muro,
            }

        elif sistema_muro_reg == "Entramado de acero galvanizado":
            st.markdown('<div class="reg-subtitulo">🔩 Composición informada – entramado de acero galvanizado</div>', unsafe_allow_html=True)
            muro_col1, muro_col2 = st.columns(2)

            with muro_col1:
                estructura_muro = st.selectbox(
                    "Perfil estructural principal:",
                    ["No sé", "Perfil 60C085", "Otro perfil"],
                    key="reg_muro_ac_estructura"
                )
                rev_int_muro = st.selectbox(
                    "Revestimiento interior:",
                    ["No sé", "Yeso-cartón", "Otro"],
                    key="reg_muro_ac_rev_int"
                )
                esp_rev_int_muro = st.number_input(
                    "Espesor del revestimiento interior (mm):",
                    min_value=0.0, value=0.0, step=0.5, format="%.1f",
                    key="reg_muro_ac_esp_rev_int"
                )
                aislante_muro = st.selectbox(
                    "Aislante entre montantes:",
                    ["No sé", "Lana de fibra de vidrio", "Lana mineral", "Sin aislación", "Otro"],
                    key="reg_muro_ac_aislante"
                )
                esp_aislante_muro = st.number_input(
                    "Espesor del aislante entre montantes (mm):",
                    min_value=0.0, value=0.0, step=5.0, format="%.1f",
                    key="reg_muro_ac_esp_aislante"
                )

            with muro_col2:
                placa_muro = st.selectbox(
                    "Placa estructural:",
                    ["No sé", "OSB estructural", "Otra", "Sin placa"],
                    key="reg_muro_ac_placa"
                )
                esp_placa_muro = st.number_input(
                    "Espesor de la placa (mm):",
                    min_value=0.0, value=0.0, step=0.5, format="%.1f",
                    key="reg_muro_ac_esp_placa"
                )
                aisl_ext_muro = st.selectbox(
                    "Aislación exterior:",
                    ["No sé", "EPS", "Lana mineral", "Sin aislación exterior", "Otra"],
                    key="reg_muro_ac_aisl_ext"
                )
                esp_aisl_ext_muro = st.number_input(
                    "Espesor de la aislación exterior (mm):",
                    min_value=0.0, value=0.0, step=5.0, format="%.1f",
                    key="reg_muro_ac_esp_aisl_ext"
                )
                rev_ext_muro = st.selectbox(
                    "Revestimiento exterior:",
                    ["No sé", "Fibrocemento", "Siding", "Otro"],
                    key="reg_muro_ac_rev_ext"
                )
                esp_rev_ext_muro = st.number_input(
                    "Espesor del revestimiento exterior (mm):",
                    min_value=0.0, value=0.0, step=0.5, format="%.1f",
                    key="reg_muro_ac_esp_rev_ext"
                )

            datos_muro_ingresados = {
                "Estructura_Principal": estructura_muro,
                "Revestimiento_Interior": rev_int_muro,
                "Espesor_Rev_Int_mm": esp_rev_int_muro,
                "Aislante_Entre_Estructura": aislante_muro,
                "Espesor_Aislante_mm": esp_aislante_muro,
                "Placa_Estructural": placa_muro,
                "Espesor_Placa_mm": esp_placa_muro,
                "Aislacion_Exterior": aisl_ext_muro,
                "Espesor_Aislacion_Ext_mm": esp_aisl_ext_muro,
                "Revestimiento_Exterior": rev_ext_muro,
                "Espesor_Rev_Ext_mm": esp_rev_ext_muro,
            }

        elif sistema_muro_reg == "Albañilería con EIFS":
            st.markdown('<div class="reg-subtitulo">🧱 Composición informada – albañilería con aislación exterior</div>', unsafe_allow_html=True)
            muro_col1, muro_col2 = st.columns(2)

            with muro_col1:
                estructura_muro = st.selectbox(
                    "Tipo de albañilería:",
                    [
                        "No sé",
                        "Ladrillo cerámico Santiago 7",
                        "Otro ladrillo cerámico",
                        "Bloque de hormigón",
                        "Otra"
                    ],
                    key="reg_muro_alb_estructura"
                )
                esp_muro_base = st.number_input(
                    "Espesor nominal aproximado del muro base (mm):",
                    min_value=0.0, value=0.0, step=5.0, format="%.1f",
                    key="reg_muro_alb_esp_base"
                )
                mortero_ref = st.selectbox(
                    "¿La solución utiliza mortero 1:3 y junta aproximada de 15 ± 3 mm?",
                    opciones_si_no,
                    key="reg_muro_alb_mortero"
                )

            with muro_col2:
                aisl_ext_muro = st.selectbox(
                    "Sistema de aislación exterior:",
                    ["No sé", "EIFS con EPS", "Otro sistema EIFS", "Sin aislación exterior", "Otro"],
                    key="reg_muro_alb_aisl_ext"
                )
                esp_aisl_ext_muro = st.number_input(
                    "Espesor del aislante exterior (mm):",
                    min_value=0.0, value=0.0, step=5.0, format="%.1f",
                    key="reg_muro_alb_esp_aisl_ext"
                )
                densidad_eps_muro = st.number_input(
                    "Densidad del EPS exterior, si se conoce (kg/m³):",
                    min_value=0.0, value=0.0, step=1.0, format="%.1f",
                    key="reg_muro_alb_densidad_eps"
                )

            datos_muro_ingresados = {
                "Estructura_Principal": estructura_muro,
                "Espesor_Muro_Base_mm": esp_muro_base,
                "Mortero_Referencia": mortero_ref,
                "Aislacion_Exterior": aisl_ext_muro,
                "Espesor_Aislacion_Ext_mm": esp_aisl_ext_muro,
                "Densidad_Aislacion_Ext_kg_m3": densidad_eps_muro,
            }

        if fila_ref_muro is not None and datos_muro_ingresados:
            st.markdown('<div class="reg-subtitulo">🔎 Comparación con solución de referencia</div>', unsafe_allow_html=True)

            # Funciones auxiliares locales para comparar sin atribuir prestaciones cuando faltan datos.
            def _texto_igual(valor_ingresado, valor_ref):
                return str(valor_ingresado).strip().lower() == str(valor_ref).strip().lower()

            def _numero_igual(valor_ingresado, valor_ref, tolerancia=0.26):
                try:
                    if pd.isna(valor_ref):
                        return None
                    return abs(float(valor_ingresado) - float(valor_ref)) <= tolerancia
                except Exception:
                    return None

            estado_comparacion = {"conocidos": 0, "totales": 0, "todos": True}

            def registrar_texto(nombre, ingresado, columna_ref, desconocidos=None):
                if desconocidos is None:
                    desconocidos = {"no sé", "seleccione una opción...", "no estoy seguro/a", ""}
                estado_comparacion["totales"] += 1
                if str(ingresado).strip().lower() in desconocidos:
                    estado_comparacion["todos"] = False
                    diferencias_muro.append(f"{nombre}: dato no informado o no conocido.")
                    return
                estado_comparacion["conocidos"] += 1
                esperado = fila_ref_muro.get(columna_ref, "")
                if not _texto_igual(ingresado, esperado):
                    estado_comparacion["todos"] = False
                    diferencias_muro.append(f"{nombre}: ingresado '{ingresado}' · referencia '{esperado}'.")

            def registrar_numero(nombre, ingresado, columna_ref, tolerancia=0.26):
                estado_comparacion["totales"] += 1
                if ingresado is None or float(ingresado) <= 0:
                    estado_comparacion["todos"] = False
                    diferencias_muro.append(f"{nombre}: espesor/característica no informada.")
                    return
                esperado = fila_ref_muro.get(columna_ref, None)
                comparacion = _numero_igual(ingresado, esperado, tolerancia)
                if comparacion is None:
                    estado_comparacion["todos"] = False
                    diferencias_muro.append(f"{nombre}: la referencia no permite comparación automática.")
                    return
                estado_comparacion["conocidos"] += 1
                if not comparacion:
                    estado_comparacion["todos"] = False
                    diferencias_muro.append(f"{nombre}: ingresado {float(ingresado):.1f} mm · referencia {float(esperado):.1f} mm.")

            if sistema_muro_reg in ["Entramado de madera", "Entramado de acero galvanizado"]:
                registrar_texto("Estructura principal", datos_muro_ingresados["Estructura_Principal"], "Estructura_Principal")
                registrar_texto("Revestimiento interior", datos_muro_ingresados["Revestimiento_Interior"], "Revestimiento_Interior")
                registrar_numero("Espesor revestimiento interior", datos_muro_ingresados["Espesor_Rev_Int_mm"], "Espesor_Rev_Int_mm")
                registrar_texto("Aislante interior", datos_muro_ingresados["Aislante_Entre_Estructura"], "Aislante_Entre_Estructura")
                registrar_numero("Espesor aislante interior", datos_muro_ingresados["Espesor_Aislante_mm"], "Espesor_Aislante_mm")
                registrar_texto("Placa estructural", datos_muro_ingresados["Placa_Estructural"], "Placa_Estructural")
                registrar_numero("Espesor placa estructural", datos_muro_ingresados["Espesor_Placa_mm"], "Espesor_Placa_mm")
                registrar_texto("Aislación exterior", datos_muro_ingresados["Aislacion_Exterior"], "Aislacion_Exterior")
                registrar_numero("Espesor aislación exterior", datos_muro_ingresados["Espesor_Aislacion_Ext_mm"], "Espesor_Aislacion_Ext_mm")
                registrar_texto("Revestimiento exterior", datos_muro_ingresados["Revestimiento_Exterior"], "Revestimiento_Exterior")
                registrar_numero("Espesor revestimiento exterior", datos_muro_ingresados["Espesor_Rev_Ext_mm"], "Espesor_Rev_Ext_mm")

            elif sistema_muro_reg == "Albañilería con EIFS":
                registrar_texto("Tipo de albañilería", datos_muro_ingresados["Estructura_Principal"], "Estructura_Principal")

                # La solución seleccionada usa ladrillo de 140 mm de ancho nominal.
                estado_comparacion["totales"] += 1
                if datos_muro_ingresados["Espesor_Muro_Base_mm"] <= 0:
                    estado_comparacion["todos"] = False
                    diferencias_muro.append("Espesor muro base: dato no informado.")
                else:
                    estado_comparacion["conocidos"] += 1
                    if abs(float(datos_muro_ingresados["Espesor_Muro_Base_mm"]) - 140.0) > 2.0:
                        estado_comparacion["todos"] = False
                        diferencias_muro.append(
                            f"Espesor muro base: ingresado {datos_muro_ingresados['Espesor_Muro_Base_mm']:.1f} mm · referencia 140 mm."
                        )

                estado_comparacion["totales"] += 1
                if datos_muro_ingresados["Mortero_Referencia"] == "Sí":
                    estado_comparacion["conocidos"] += 1
                elif datos_muro_ingresados["Mortero_Referencia"] == "No":
                    estado_comparacion["conocidos"] += 1
                    estado_comparacion["todos"] = False
                    diferencias_muro.append("Mortero/junta: no coincide con la configuración de referencia 1:3 y 15 ± 3 mm.")
                else:
                    estado_comparacion["todos"] = False
                    diferencias_muro.append("Mortero/junta: condición no verificada.")

                registrar_texto("Aislación exterior", datos_muro_ingresados["Aislacion_Exterior"], "Aislacion_Exterior")
                registrar_numero("Espesor aislación exterior", datos_muro_ingresados["Espesor_Aislacion_Ext_mm"], "Espesor_Aislacion_Ext_mm")

                estado_comparacion["totales"] += 1
                if datos_muro_ingresados["Densidad_Aislacion_Ext_kg_m3"] <= 0:
                    estado_comparacion["todos"] = False
                    diferencias_muro.append("Densidad del EPS: dato no informado.")
                else:
                    estado_comparacion["conocidos"] += 1
                    esperado_densidad = fila_ref_muro.get("Densidad_Aislacion_Ext_kg_m3", None)
                    if pd.isna(esperado_densidad) or abs(float(datos_muro_ingresados["Densidad_Aislacion_Ext_kg_m3"]) - float(esperado_densidad)) > 0.6:
                        estado_comparacion["todos"] = False
                        diferencias_muro.append(
                            f"Densidad EPS: ingresada {datos_muro_ingresados['Densidad_Aislacion_Ext_kg_m3']:.1f} kg/m³ · referencia {float(esperado_densidad):.1f} kg/m³."
                        )

            codigo_ref = str(fila_ref_muro.get("Codigo_Solucion", ""))
            u_ref = fila_ref_muro.get("U_W_m2K", None)
            rt_ref = fila_ref_muro.get("Rt_m2K_W", None)
            u_max_ref = fila_ref_muro.get("U_Max_Zona_D", None)
            rt_min_ref = fila_ref_muro.get("Rt_Min_Zona_D", None)

            if estado_comparacion["todos"] and estado_comparacion["conocidos"] == estado_comparacion["totales"]:
                resultado_muro_regularizacion = {
                    "estado": "Coincidencia con solución de referencia",
                    "sistema_ingresado": sistema_muro_reg,
                    "codigo_referencia": codigo_ref,
                    "u_referencia": float(u_ref) if pd.notna(u_ref) else None,
                    "rt_referencia": float(rt_ref) if pd.notna(rt_ref) else None,
                    "diferencias": [],
                }
                st.success(
                    f"✅ **Coincidencia con solución de referencia {codigo_ref}.** "
                    "La configuración ingresada coincide con los parámetros críticos registrados en la base del prototipo."
                )

                ref_col1, ref_col2, ref_col3, ref_col4 = st.columns(4)
                with ref_col1:
                    st.metric("U de referencia", f"{float(u_ref):.2f} W/m²K")
                with ref_col2:
                    st.metric("Rt de referencia", f"{float(rt_ref):.2f} m²K/W")
                with ref_col3:
                    st.metric("U máx. Zona D", f"{float(u_max_ref):.2f} W/m²K")
                with ref_col4:
                    st.metric("Rt mín. Zona D", f"{float(rt_min_ref):.2f} m²K/W")

                if (pd.notna(u_ref) and pd.notna(u_max_ref) and float(u_ref) <= float(u_max_ref)) or (
                    pd.notna(rt_ref) and pd.notna(rt_min_ref) and float(rt_ref) >= float(rt_min_ref)
                ):
                    st.success(
                        "🌡️ La **solución de referencia** presenta un desempeño térmico compatible con los valores "
                        "considerados para muros perimetrales de Zona Térmica D."
                    )
            else:
                if estado_comparacion["conocidos"] == 0:
                    estado_muro = "No verificable"
                else:
                    estado_muro = "Coincidencia parcial / requiere verificación"

                resultado_muro_regularizacion = {
                    "estado": estado_muro,
                    "sistema_ingresado": sistema_muro_reg,
                    "codigo_referencia": codigo_ref,
                    "u_referencia": None,
                    "rt_referencia": None,
                    "diferencias": diferencias_muro,
                }

                st.warning(
                    f"⚠️ **{estado_muro}.** La configuración fue comparada con la solución {codigo_ref}, "
                    "pero no coincide completamente o faltan antecedentes. Por esta razón el prototipo **no asigna "
                    "automáticamente el valor U ni Rt de la solución LOSCAT** al muro existente."
                )

                with st.expander("🔎 Ver diferencias o antecedentes pendientes"):
                    for diferencia in diferencias_muro:
                        st.write(f"• {diferencia}")

            with st.expander("📚 Ver solución LOSCAT utilizada como referencia"):
                st.write(f"**Código:** {codigo_ref}")
                st.write(f"**Sistema:** {fila_ref_muro.get('Sistema', '')}")
                st.write(f"**Estructura principal:** {fila_ref_muro.get('Estructura_Principal', '')}")
                if fila_ref_muro.get("Aislante_Entre_Estructura", ""):
                    st.write(
                        f"**Aislación interior:** {fila_ref_muro.get('Aislante_Entre_Estructura', '')} "
                        f"{fila_ref_muro.get('Espesor_Aislante_mm', '')} mm"
                    )
                if fila_ref_muro.get("Aislacion_Exterior", ""):
                    st.write(
                        f"**Aislación exterior:** {fila_ref_muro.get('Aislacion_Exterior', '')} "
                        f"{fila_ref_muro.get('Espesor_Aislacion_Ext_mm', '')} mm"
                    )
                st.write(f"**Fuente:** {fila_ref_muro.get('Fuente', '')}")
                if fila_ref_muro.get("Observacion", ""):
                    st.write(f"**Observación:** {fila_ref_muro.get('Observacion', '')}")

        elif sistema_muro_reg == "Otro sistema":
            descripcion_otro_muro = st.text_area(
                "Describe los materiales y espesores que conozcas:",
                placeholder="Ej.: ladrillo, estuco interior, 20 mm de aislación exterior...",
                key="reg_muro_otro_descripcion"
            )
            resultado_muro_regularizacion = {
                "estado": "No verificable con las soluciones registradas",
                "sistema_ingresado": "Otro sistema",
                "codigo_referencia": None,
                "u_referencia": None,
                "rt_referencia": None,
                "diferencias": [descripcion_otro_muro] if descripcion_otro_muro else [],
            }
            st.info(
                "ℹ️ La base actual del prototipo contiene un conjunto acotado de soluciones de referencia. "
                "La descripción ingresada deberá revisarse mediante una solución acreditada, ensayo o memoria de cálculo cuando corresponda."
            )

        elif sistema_muro_reg == "No sé cómo está construido":
            resultado_muro_regularizacion = {
                "estado": "No verificable por falta de antecedentes",
                "sistema_ingresado": "No identificado",
                "codigo_referencia": None,
                "u_referencia": None,
                "rt_referencia": None,
                "diferencias": ["El usuario no conoce la composición del muro existente."],
            }
            st.info(
                "ℹ️ No se asignará un valor térmico al muro. Para verificarlo se requiere identificar su composición "
                "y espesores o contar con antecedentes técnicos de la solución constructiva."
            )

        elif sistema_muro_reg == "Seleccione una opción...":
            st.info("Selecciona el sistema de muro para iniciar la comparación constructiva.")

        st.caption(
            "🔥 La coincidencia térmica con una solución de referencia **no acredita por sí sola resistencia al fuego F-15 o F-60**, "
            "ni reemplaza la verificación de estabilidad o el informe del profesional competente."
        )

    # ==========================================
    # 7. REVISIÓN CONSTRUCTIVA Y TÉRMICA DEL PISO
    # ==========================================
    st.markdown("""
    <div class="reg-section reg-piso">
        <span class="numero">7</span><span class="titulo">⬛ Revisión Constructiva y Térmica del Piso Existente</span>
        <span class="descripcion">Distingue entre piso apoyado sobre terreno y piso ventilado para orientar su revisión constructiva y térmica.</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption(
        "Selecciona la condición predominante del piso. Para un piso apoyado sobre terreno, el prototipo revisa "
        "el criterio constructivo de referencia y la aislación exterior del sobrecimiento. Para un piso ventilado, "
        "compara la composición ingresada con la solución MINVU seleccionada en la tesis. Esta revisión es orientativa."
    )

    try:
        base_pisos = cargar_soluciones_pisos()
    except Exception:
        base_pisos = None

    if base_pisos is None or base_pisos.empty:
        st.warning(
            "⚠️ No fue posible cargar la hoja **Soluciones_Pisos** desde `Base_Normativa_PRC_San_Miguel.xlsx`. "
            "Para utilizar esta revisión debes subir también la versión actualizada de la base normativa."
        )
    else:
        tipo_piso_reg = st.selectbox(
            "Condición predominante del piso existente:",
            [
                "Seleccione una opción...",
                "Piso apoyado sobre terreno (radier)",
                "Piso ventilado de madera",
                "Otro sistema",
                "No sé cómo está construido",
            ],
            key="reg_piso_tipo"
        )

        if tipo_piso_reg == "Piso apoyado sobre terreno (radier)":
            referencia_piso = base_pisos[
                base_pisos["Condicion_Piso"].str.lower() == "apoyado sobre terreno"
            ]
            fila_ref_piso = referencia_piso.iloc[0] if not referencia_piso.empty else None

            st.markdown('<div class="reg-subtitulo">🧱 Piso apoyado directamente sobre terreno</div>', unsafe_allow_html=True)
            with st.expander("🖼️ Ver detalle visual de referencia del radier", expanded=False):
                mostrar_imagen_solucion(
                    "piso_radier",
                    caption="Detalle visual de referencia — radier de hormigón sobre base granular"
                )
                st.caption(
                    "La imagen corresponde a la referencia constructiva utilizada por el prototipo. "
                    "La verificación térmica se realiza respecto de la aislación exterior del sobrecimiento."
                )
            st.info(
                "ℹ️ En esta alternativa, los espesores de ripio y radier se muestran como **criterios constructivos de referencia**. "
                "La revisión térmica se concentra en la aislación exterior del sobrecimiento para Zona Térmica D."
            )

            piso_col1, piso_col2 = st.columns(2)
            with piso_col1:
                espesor_ripio_piso = st.number_input(
                    "Espesor aproximado de la cama de ripio (mm; 0 = no sé):",
                    min_value=0.0, value=0.0, step=10.0, format="%.0f",
                    key="reg_piso_radier_ripio"
                )
                espesor_radier_piso = st.number_input(
                    "Espesor aproximado del radier de hormigón (mm; 0 = no sé):",
                    min_value=0.0, value=0.0, step=10.0, format="%.0f",
                    key="reg_piso_radier_espesor"
                )

            with piso_col2:
                aislacion_sobrecimiento = st.selectbox(
                    "¿Existe aislación térmica exterior en el sobrecimiento?",
                    opciones_si_no,
                    key="reg_piso_sobrecimiento_aislacion"
                )
                r100_sobrecimiento = 0.0
                if aislacion_sobrecimiento == "Sí":
                    r100_sobrecimiento = st.number_input(
                        "R100 informado de la aislación del sobrecimiento (0 = no sé):",
                        min_value=0.0, value=0.0, step=5.0, format="%.0f",
                        key="reg_piso_sobrecimiento_r100"
                    )

            diferencias_piso = []
            if fila_ref_piso is not None:
                ripio_ref = fila_ref_piso.get("Cama_Ripio_mm", None)
                radier_ref = fila_ref_piso.get("Radier_Hormigon_mm", None)
                r100_min_ref = fila_ref_piso.get("R100_Min_Sobrecimiento", None)
                codigo_ref_piso = str(fila_ref_piso.get("Codigo_Solucion", "PST-REF-ZD"))

                if espesor_ripio_piso > 0 and pd.notna(ripio_ref) and abs(float(espesor_ripio_piso) - float(ripio_ref)) > 1.0:
                    diferencias_piso.append(
                        f"Cama de ripio: ingresada {espesor_ripio_piso:.0f} mm · referencia constructiva {float(ripio_ref):.0f} mm."
                    )
                if espesor_radier_piso > 0 and pd.notna(radier_ref) and abs(float(espesor_radier_piso) - float(radier_ref)) > 1.0:
                    diferencias_piso.append(
                        f"Radier: ingresado {espesor_radier_piso:.0f} mm · referencia constructiva {float(radier_ref):.0f} mm."
                    )

                if aislacion_sobrecimiento == "Sí" and r100_sobrecimiento > 0 and pd.notna(r100_min_ref):
                    if float(r100_sobrecimiento) >= float(r100_min_ref):
                        estado_piso = "Referencia térmica compatible para piso sobre terreno"
                        st.success(
                            f"✅ El R100 informado (**{r100_sobrecimiento:.0f}**) alcanza el valor de referencia "
                            f"considerado para Zona Térmica D (**R100 ≥ {float(r100_min_ref):.0f}**)."
                        )
                    else:
                        estado_piso = "Requiere revisión térmica del sobrecimiento"
                        diferencias_piso.append(
                            f"R100 del sobrecimiento: informado {r100_sobrecimiento:.0f} · referencia mínima {float(r100_min_ref):.0f}."
                        )
                        st.error(
                            f"❌ El R100 informado (**{r100_sobrecimiento:.0f}**) es inferior al valor de referencia "
                            f"(**{float(r100_min_ref):.0f}**)."
                        )
                elif aislacion_sobrecimiento == "No":
                    estado_piso = "Requiere revisión térmica del sobrecimiento"
                    diferencias_piso.append("Se informó que el sobrecimiento no cuenta con aislación térmica exterior.")
                    st.warning(
                        "⚠️ Se informó ausencia de aislación exterior en el sobrecimiento. Debe revisarse la condición térmica aplicable."
                    )
                else:
                    estado_piso = "No verificable por falta de antecedentes térmicos"
                    diferencias_piso.append("No se dispone de un R100 verificable para la aislación exterior del sobrecimiento.")
                    st.info(
                        "ℹ️ No es posible verificar térmicamente el piso sobre terreno sin antecedentes de la aislación del sobrecimiento."
                    )

                resultado_piso_regularizacion = {
                    "estado": estado_piso,
                    "sistema_ingresado": tipo_piso_reg,
                    "codigo_referencia": codigo_ref_piso,
                    "u_referencia": None,
                    "rt_referencia": None,
                    "r100_sobrecimiento": float(r100_sobrecimiento) if r100_sobrecimiento > 0 else None,
                    "diferencias": diferencias_piso,
                }

                with st.expander("📚 Ver criterio de referencia para piso sobre terreno"):
                    st.write(f"**Código interno de referencia:** {codigo_ref_piso}")
                    st.write(f"**Cama de ripio de referencia:** {float(ripio_ref):.0f} mm" if pd.notna(ripio_ref) else "**Cama de ripio:** sin dato")
                    st.write(f"**Radier de referencia:** {float(radier_ref):.0f} mm" if pd.notna(radier_ref) else "**Radier:** sin dato")
                    st.write(f"**Aislación de sobrecimiento:** {fila_ref_piso.get('Aislacion_Sobrecimiento', '')}")
                    st.write(f"**R100 mínimo de referencia:** {float(r100_min_ref):.0f}" if pd.notna(r100_min_ref) else "**R100:** sin dato")
                    st.write(f"**Fuente:** {fila_ref_piso.get('Fuente', '')}")
                    st.write(f"**Observación:** {fila_ref_piso.get('Observacion', '')}")

                if diferencias_piso:
                    with st.expander("🔎 Ver diferencias respecto del criterio de referencia"):
                        for diferencia in diferencias_piso:
                            st.write(f"• {diferencia}")

        elif tipo_piso_reg == "Piso ventilado de madera":
            with st.expander("🖼️ Ver detalle visual de referencia del piso ventilado", expanded=False):
                mostrar_imagen_solucion(
                    "piso_ventilado",
                    caption="Detalle visual de referencia — piso ventilado de entramado de madera con aislación"
                )
                st.caption(
                    "Utiliza la imagen para reconocer la disposición general de capas; la coincidencia se determina con los datos ingresados."
                )
            referencia_piso = base_pisos[
                base_pisos["Condicion_Piso"].str.lower() == "ventilado"
            ]
            fila_ref_piso = referencia_piso.iloc[0] if not referencia_piso.empty else None

            st.markdown('<div class="reg-subtitulo">🪵 Piso ventilado – entramado de madera</div>', unsafe_allow_html=True)
            piso_col1, piso_col2 = st.columns(2)

            with piso_col1:
                placa_piso = st.selectbox(
                    "Placa estructural superior:",
                    ["No sé", "OSB", "Terciado estructural", "Otra"],
                    key="reg_piso_vent_placa"
                )
                espesor_placa_piso = st.number_input(
                    "Espesor de la placa estructural (mm; 0 = no sé):",
                    min_value=0.0, value=0.0, step=0.5, format="%.1f",
                    key="reg_piso_vent_esp_placa"
                )
                estructura_piso = st.selectbox(
                    "Envigado estructural:",
                    ["No sé", 'Pino 2"x8"', 'Pino 2"x6"', "Otra"],
                    key="reg_piso_vent_estructura"
                )
                aislante_piso = st.selectbox(
                    "Aislante entre vigas:",
                    ["No sé", "Lana de fibra de vidrio", "Lana mineral", "EPS", "Sin aislación", "Otro"],
                    key="reg_piso_vent_aislante"
                )

            with piso_col2:
                espesor_aislante_piso = st.number_input(
                    "Espesor del aislante (mm; 0 = no sé):",
                    min_value=0.0, value=0.0, step=10.0, format="%.0f",
                    key="reg_piso_vent_esp_aislante"
                )
                densidad_aislante_piso = st.number_input(
                    "Densidad aproximada del aislante (kg/m³; 0 = no sé):",
                    min_value=0.0, value=0.0, step=1.0, format="%.1f",
                    key="reg_piso_vent_densidad"
                )
                barrera_piso = st.selectbox(
                    "¿Cuenta con barrera de humedad y viento bajo el complejo?",
                    opciones_si_no,
                    key="reg_piso_vent_barrera"
                )
                revestimiento_inf_piso = st.selectbox(
                    "Revestimiento inferior:",
                    ["No sé", "Fibrocemento", "Yeso-cartón", "Madera", "Sin revestimiento", "Otro"],
                    key="reg_piso_vent_rev_inf"
                )
                espesor_rev_inf_piso = st.number_input(
                    "Espesor del revestimiento inferior (mm; 0 = no sé):",
                    min_value=0.0, value=0.0, step=1.0, format="%.0f",
                    key="reg_piso_vent_esp_rev_inf"
                )

            if fila_ref_piso is not None:
                diferencias_piso = []
                conocidos_piso = 0
                totales_piso = 8
                cumple_piso = True

                esperado_placa = str(fila_ref_piso.get("Placa_Estructural", ""))
                if placa_piso != "No sé":
                    conocidos_piso += 1
                    if placa_piso.lower() != esperado_placa.lower():
                        cumple_piso = False
                        diferencias_piso.append(f"Placa estructural: ingresada {placa_piso} · referencia {esperado_placa}.")

                min_placa = fila_ref_piso.get("Espesor_Placa_Min_mm", None)
                max_placa = fila_ref_piso.get("Espesor_Placa_Max_mm", None)
                if espesor_placa_piso > 0:
                    conocidos_piso += 1
                    if pd.notna(min_placa) and pd.notna(max_placa):
                        if not (float(min_placa) - 0.05 <= float(espesor_placa_piso) <= float(max_placa) + 0.05):
                            cumple_piso = False
                            diferencias_piso.append(
                                f"Espesor OSB: ingresado {espesor_placa_piso:.1f} mm · referencia aprox. {float(min_placa):.1f}–{float(max_placa):.1f} mm."
                            )

                esperado_estructura = str(fila_ref_piso.get("Estructura_Principal", ""))
                if estructura_piso != "No sé":
                    conocidos_piso += 1
                    if estructura_piso.lower() != esperado_estructura.lower():
                        cumple_piso = False
                        diferencias_piso.append(f"Envigado: ingresado {estructura_piso} · referencia {esperado_estructura}.")

                esperado_aislante = str(fila_ref_piso.get("Aislante", ""))
                if aislante_piso != "No sé":
                    conocidos_piso += 1
                    if aislante_piso.lower() != esperado_aislante.lower():
                        cumple_piso = False
                        diferencias_piso.append(f"Aislante: ingresado {aislante_piso} · referencia {esperado_aislante}.")

                esperado_esp_aislante = fila_ref_piso.get("Espesor_Aislante_mm", None)
                if espesor_aislante_piso > 0:
                    conocidos_piso += 1
                    if pd.notna(esperado_esp_aislante) and abs(float(espesor_aislante_piso) - float(esperado_esp_aislante)) > 0.5:
                        cumple_piso = False
                        diferencias_piso.append(
                            f"Espesor aislante: ingresado {espesor_aislante_piso:.0f} mm · referencia {float(esperado_esp_aislante):.0f} mm."
                        )

                esperado_densidad = fila_ref_piso.get("Densidad_Aislante_kg_m3", None)
                if densidad_aislante_piso > 0:
                    conocidos_piso += 1
                    if pd.notna(esperado_densidad) and float(densidad_aislante_piso) + 1e-9 < float(esperado_densidad):
                        cumple_piso = False
                        diferencias_piso.append(
                            f"Densidad aislante: ingresada {densidad_aislante_piso:.1f} kg/m³ · referencia aprox. {float(esperado_densidad):.1f} kg/m³."
                        )

                if barrera_piso != "Seleccione una opción..." and barrera_piso != "No estoy seguro/a":
                    conocidos_piso += 1
                    if barrera_piso != "Sí":
                        cumple_piso = False
                        diferencias_piso.append("No se informó barrera de humedad y viento incorporada bajo el complejo.")

                esperado_rev_inf = str(fila_ref_piso.get("Revestimiento_Inferior", ""))
                if revestimiento_inf_piso != "No sé":
                    conocidos_piso += 1
                    if revestimiento_inf_piso.lower() != esperado_rev_inf.lower():
                        cumple_piso = False
                        diferencias_piso.append(
                            f"Revestimiento inferior: ingresado {revestimiento_inf_piso} · referencia {esperado_rev_inf}."
                        )

                # El espesor del revestimiento inferior se considera dato adicional; si se conoce y difiere, se informa.
                esperado_esp_rev_inf = fila_ref_piso.get("Espesor_Rev_Inferior_mm", None)
                if espesor_rev_inf_piso > 0 and pd.notna(esperado_esp_rev_inf):
                    if abs(float(espesor_rev_inf_piso) - float(esperado_esp_rev_inf)) > 0.5:
                        cumple_piso = False
                        diferencias_piso.append(
                            f"Espesor revestimiento inferior: ingresado {espesor_rev_inf_piso:.0f} mm · referencia {float(esperado_esp_rev_inf):.0f} mm."
                        )

                codigo_ref_piso = str(fila_ref_piso.get("Codigo_Solucion", ""))
                u_ref_piso = fila_ref_piso.get("U_W_m2K", None)
                rt_ref_piso = fila_ref_piso.get("Rt_m2K_W", None)
                u_max_piso = fila_ref_piso.get("U_Max_Zona_D", None)
                rt_min_piso = fila_ref_piso.get("Rt_Min_Zona_D", None)

                if cumple_piso and conocidos_piso == totales_piso:
                    resultado_piso_regularizacion = {
                        "estado": "Coincidencia con solución de referencia",
                        "sistema_ingresado": tipo_piso_reg,
                        "codigo_referencia": codigo_ref_piso,
                        "u_referencia": float(u_ref_piso) if pd.notna(u_ref_piso) else None,
                        "rt_referencia": float(rt_ref_piso) if pd.notna(rt_ref_piso) else None,
                        "diferencias": [],
                    }
                    st.success(
                        f"✅ La composición ingresada coincide con los parámetros críticos registrados para la solución **{codigo_ref_piso}**."
                    )
                    piso_m1, piso_m2, piso_m3, piso_m4 = st.columns(4)
                    with piso_m1:
                        st.metric("U referencia", f"{float(u_ref_piso):.2f} W/m²K")
                    with piso_m2:
                        st.metric("Rt referencia", f"{float(rt_ref_piso):.2f} m²K/W")
                    with piso_m3:
                        st.metric("U máx. Zona D", f"{float(u_max_piso):.2f} W/m²K")
                    with piso_m4:
                        st.metric("Rt mín. Zona D", f"{float(rt_min_piso):.2f} m²K/W")
                    st.success("🌡️ La solución de referencia presenta un desempeño térmico compatible con Zona Térmica D.")
                else:
                    estado_piso = "No verificable" if conocidos_piso == 0 else "Coincidencia parcial / requiere verificación"
                    resultado_piso_regularizacion = {
                        "estado": estado_piso,
                        "sistema_ingresado": tipo_piso_reg,
                        "codigo_referencia": codigo_ref_piso,
                        "u_referencia": None,
                        "rt_referencia": None,
                        "diferencias": diferencias_piso,
                    }
                    st.warning(
                        f"⚠️ **{estado_piso}.** No se asignan automáticamente U ni Rt porque faltan antecedentes "
                        "o la composición no coincide completamente con la solución de referencia."
                    )
                    if diferencias_piso:
                        with st.expander("🔎 Ver diferencias o antecedentes pendientes"):
                            for diferencia in diferencias_piso:
                                st.write(f"• {diferencia}")

                with st.expander("📚 Ver solución MINVU utilizada como referencia"):
                    st.write(f"**Código:** {codigo_ref_piso}")
                    st.write(f"**Sistema:** {fila_ref_piso.get('Sistema', '')}")
                    st.write(
                        f"**Placa estructural:** {fila_ref_piso.get('Placa_Estructural', '')} "
                        f"aprox. {fila_ref_piso.get('Espesor_Placa_Min_mm', '')}–{fila_ref_piso.get('Espesor_Placa_Max_mm', '')} mm"
                    )
                    st.write(f"**Estructura:** {fila_ref_piso.get('Estructura_Principal', '')}")
                    st.write(
                        f"**Aislación:** {fila_ref_piso.get('Aislante', '')} "
                        f"{fila_ref_piso.get('Espesor_Aislante_mm', '')} mm"
                    )
                    st.write(f"**Revestimiento inferior:** {fila_ref_piso.get('Revestimiento_Inferior', '')} {fila_ref_piso.get('Espesor_Rev_Inferior_mm', '')} mm")
                    st.write(f"**Fuente:** {fila_ref_piso.get('Fuente', '')}")
                    st.write(f"**Observación:** {fila_ref_piso.get('Observacion', '')}")

        elif tipo_piso_reg == "Otro sistema":
            descripcion_otro_piso = st.text_area(
                "Describe los materiales y espesores del piso que conozcas:",
                placeholder="Ej.: envigado de madera, tablero, aislante, revestimiento inferior...",
                key="reg_piso_otro_descripcion"
            )
            resultado_piso_regularizacion = {
                "estado": "No verificable con las soluciones registradas",
                "sistema_ingresado": "Otro sistema",
                "codigo_referencia": None,
                "u_referencia": None,
                "rt_referencia": None,
                "diferencias": [descripcion_otro_piso] if descripcion_otro_piso else [],
            }
            st.info(
                "ℹ️ La base del prototipo contiene un conjunto acotado de referencias. La solución descrita requiere "
                "antecedentes técnicos, ensayo, memoria de cálculo o una solución acreditada cuando corresponda."
            )

        elif tipo_piso_reg == "No sé cómo está construido":
            resultado_piso_regularizacion = {
                "estado": "No verificable por falta de antecedentes",
                "sistema_ingresado": "No identificado",
                "codigo_referencia": None,
                "u_referencia": None,
                "rt_referencia": None,
                "diferencias": ["El usuario no conoce la composición del piso existente."],
            }
            st.info("ℹ️ Para verificar el piso se requiere identificar su condición y composición constructiva.")

        elif tipo_piso_reg == "Seleccione una opción...":
            st.info("Selecciona la condición del piso para iniciar la revisión.")

    # ==========================================
    # 8. REVISIÓN CONSTRUCTIVA Y TÉRMICA DE TECHUMBRE
    # ==========================================
    st.markdown("""
    <div class="reg-section reg-techumbre">
        <span class="numero">8</span><span class="titulo">🏠 Revisión Constructiva y Térmica de la Techumbre Existente</span>
        <span class="descripcion">Compara la techumbre informada con la solución de referencia utilizada en la tesis para Zona Térmica D.</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption(
        "Describe la techumbre predominante. El prototipo compara los parámetros térmicos críticos ingresados "
        "con la solución LOSCAT de referencia seleccionada en la tesis para Zona Térmica D."
    )

    try:
        base_techumbres = cargar_soluciones_techumbres()
    except Exception:
        base_techumbres = None

    if base_techumbres is None or base_techumbres.empty:
        st.warning(
            "⚠️ No fue posible cargar la hoja **Soluciones_Techumbres** desde `Base_Normativa_PRC_San_Miguel.xlsx`. "
            "Para utilizar esta revisión debes subir también la versión actualizada de la base normativa."
        )
    else:
        tipo_techumbre_reg = st.selectbox(
            "Sistema predominante de techumbre existente:",
            [
                "Seleccione una opción...",
                "Cerchas de madera con lana de fibra de vidrio sobre cielo horizontal",
                "Otro sistema",
                "No sé cómo está construida",
            ],
            key="reg_tech_tipo"
        )

        if tipo_techumbre_reg == "Cerchas de madera con lana de fibra de vidrio sobre cielo horizontal":
            fila_ref_tech = base_techumbres.iloc[0]
            with st.expander("🖼️ Ver detalle visual de referencia de la techumbre", expanded=False):
                mostrar_imagen_solucion(
                    "techumbre_madera",
                    caption="Detalle visual de referencia — cerchas de madera con lana de fibra de vidrio sobre cielo horizontal"
                )
                st.caption(
                    "La imagen es una ayuda de reconocimiento; la verificación se realiza comparando la composición y espesores informados."
                )
            st.markdown('<div class="reg-subtitulo">🏠 Composición informada – techumbre liviana</div>', unsafe_allow_html=True)
            tech_col1, tech_col2 = st.columns(2)

            with tech_col1:
                cielo_tech = st.selectbox(
                    "Cielo interior:",
                    ["No sé", "Yeso-cartón", "Madera", "Otro", "Sin cielo"],
                    key="reg_tech_cielo"
                )
                espesor_cielo_tech = st.number_input(
                    "Espesor del cielo interior (mm; 0 = no sé):",
                    min_value=0.0, value=0.0, step=1.0, format="%.0f",
                    key="reg_tech_esp_cielo"
                )
                estructura_tech = st.selectbox(
                    "Estructura principal:",
                    ["No sé", "Cerchas de madera", "Cerchas metálicas", "Vigas de madera", "Otra"],
                    key="reg_tech_estructura"
                )
                separacion_tech = st.number_input(
                    "Separación aproximada entre cerchas (cm; 0 = no sé):",
                    min_value=0.0, value=0.0, step=5.0, format="%.0f",
                    key="reg_tech_separacion"
                )

            with tech_col2:
                aislante_tech = st.selectbox(
                    "Aislación térmica:",
                    ["No sé", "Lana de fibra de vidrio", "Lana mineral", "EPS", "Sin aislación", "Otro"],
                    key="reg_tech_aislante"
                )
                espesor_aislante_tech = st.number_input(
                    "Espesor de aislación (mm; 0 = no sé):",
                    min_value=0.0, value=0.0, step=10.0, format="%.0f",
                    key="reg_tech_esp_aislante"
                )
                densidad_aislante_tech = st.number_input(
                    "Densidad del aislante (kg/m³; 0 = no sé):",
                    min_value=0.0, value=0.0, step=1.0, format="%.1f",
                    key="reg_tech_densidad"
                )
                entretecho_tech = st.selectbox(
                    "¿Existe espacio de entretecho?",
                    opciones_si_no,
                    key="reg_tech_entretecho"
                )
                ventilacion_tech = "No aplica"
                if entretecho_tech == "Sí":
                    ventilacion_tech = st.selectbox(
                        "¿El entretecho cuenta con ventilación cruzada?",
                        opciones_si_no,
                        key="reg_tech_ventilacion"
                    )

            diferencias_tech = []
            conocidos_tech = 0
            totales_tech = 6
            cumple_tech = True

            esperado_cielo = str(fila_ref_tech.get("Cielo_Interior", ""))
            if cielo_tech != "No sé":
                conocidos_tech += 1
                if cielo_tech.lower() != esperado_cielo.lower():
                    cumple_tech = False
                    diferencias_tech.append(f"Cielo interior: ingresado {cielo_tech} · referencia {esperado_cielo}.")

            esperado_esp_cielo = fila_ref_tech.get("Espesor_Cielo_mm", None)
            if espesor_cielo_tech > 0:
                conocidos_tech += 1
                if pd.notna(esperado_esp_cielo) and abs(float(espesor_cielo_tech) - float(esperado_esp_cielo)) > 0.5:
                    cumple_tech = False
                    diferencias_tech.append(
                        f"Espesor cielo: ingresado {espesor_cielo_tech:.0f} mm · referencia {float(esperado_esp_cielo):.0f} mm."
                    )

            esperado_estructura_tech = str(fila_ref_tech.get("Estructura_Principal", ""))
            if estructura_tech != "No sé":
                conocidos_tech += 1
                if estructura_tech.lower() != esperado_estructura_tech.lower():
                    cumple_tech = False
                    diferencias_tech.append(
                        f"Estructura principal: ingresada {estructura_tech} · referencia {esperado_estructura_tech}."
                    )

            esperado_aislante_tech = str(fila_ref_tech.get("Aislante", ""))
            if aislante_tech != "No sé":
                conocidos_tech += 1
                if aislante_tech.lower() != esperado_aislante_tech.lower():
                    cumple_tech = False
                    diferencias_tech.append(
                        f"Aislante: ingresado {aislante_tech} · referencia {esperado_aislante_tech}."
                    )

            esperado_esp_aislante_tech = fila_ref_tech.get("Espesor_Aislante_mm", None)
            if espesor_aislante_tech > 0:
                conocidos_tech += 1
                if pd.notna(esperado_esp_aislante_tech) and abs(float(espesor_aislante_tech) - float(esperado_esp_aislante_tech)) > 0.5:
                    cumple_tech = False
                    diferencias_tech.append(
                        f"Espesor aislante: ingresado {espesor_aislante_tech:.0f} mm · referencia {float(esperado_esp_aislante_tech):.0f} mm."
                    )

            esperado_densidad_tech = fila_ref_tech.get("Densidad_Aislante_Min_kg_m3", None)
            if densidad_aislante_tech > 0:
                conocidos_tech += 1
                if pd.notna(esperado_densidad_tech) and float(densidad_aislante_tech) + 1e-9 < float(esperado_densidad_tech):
                    cumple_tech = False
                    diferencias_tech.append(
                        f"Densidad aislante: ingresada {densidad_aislante_tech:.1f} kg/m³ · referencia mínima {float(esperado_densidad_tech):.1f} kg/m³."
                    )

            # La separación y ventilación se informan como antecedentes complementarios, porque la solución
            # de referencia los contempla aproximadamente/según corresponda.
            separacion_ref_tech = fila_ref_tech.get("Separacion_Cerchas_cm", None)
            if separacion_tech > 0 and pd.notna(separacion_ref_tech) and abs(float(separacion_tech) - float(separacion_ref_tech)) > 5.0:
                diferencias_tech.append(
                    f"Separación entre cerchas: ingresada {separacion_tech:.0f} cm · referencia aproximada {float(separacion_ref_tech):.0f} cm."
                )
            if entretecho_tech == "Sí" and ventilacion_tech == "No":
                diferencias_tech.append("Se informó entretecho sin ventilación cruzada; la solución de referencia la contempla cuando corresponde.")

            codigo_ref_tech = str(fila_ref_tech.get("Codigo_Solucion", ""))
            u_ref_tech = fila_ref_tech.get("U_W_m2K", None)
            rt_ref_tech = fila_ref_tech.get("Rt_m2K_W", None)
            u_max_tech = fila_ref_tech.get("U_Max_Zona_D", None)
            rt_min_tech = fila_ref_tech.get("Rt_Min_Zona_D", None)

            if cumple_tech and conocidos_tech == totales_tech:
                resultado_techumbre_regularizacion = {
                    "estado": "Coincidencia con solución de referencia",
                    "sistema_ingresado": tipo_techumbre_reg,
                    "codigo_referencia": codigo_ref_tech,
                    "u_referencia": float(u_ref_tech) if pd.notna(u_ref_tech) else None,
                    "rt_referencia": float(rt_ref_tech) if pd.notna(rt_ref_tech) else None,
                    "diferencias": diferencias_tech,
                }
                st.success(
                    f"✅ Los parámetros térmicos críticos ingresados coinciden con la solución de referencia **{codigo_ref_tech}**."
                )
                tech_m1, tech_m2, tech_m3, tech_m4 = st.columns(4)
                with tech_m1:
                    st.metric("U referencia", f"{float(u_ref_tech):.2f} W/m²K")
                with tech_m2:
                    st.metric("Rt referencia", f"{float(rt_ref_tech):.2f} m²K/W")
                with tech_m3:
                    st.metric("U máx. Zona D", f"{float(u_max_tech):.2f} W/m²K")
                with tech_m4:
                    st.metric("Rt mín. Zona D", f"{float(rt_min_tech):.2f} m²K/W")
                st.success("🌡️ La solución de referencia presenta un desempeño térmico compatible con Zona Térmica D.")
                if diferencias_tech:
                    st.info(
                        "ℹ️ Existen antecedentes complementarios que difieren o requieren revisión, pero no se utilizaron "
                        "para atribuir automáticamente el valor térmico de referencia."
                    )
            else:
                estado_tech = "No verificable" if conocidos_tech == 0 else "Coincidencia parcial / requiere verificación"
                resultado_techumbre_regularizacion = {
                    "estado": estado_tech,
                    "sistema_ingresado": tipo_techumbre_reg,
                    "codigo_referencia": codigo_ref_tech,
                    "u_referencia": None,
                    "rt_referencia": None,
                    "diferencias": diferencias_tech,
                }
                st.warning(
                    f"⚠️ **{estado_tech}.** No se asignan automáticamente U ni Rt porque faltan antecedentes "
                    "o los parámetros térmicos críticos no coinciden completamente con la solución LOSCAT."
                )

            if diferencias_tech:
                with st.expander("🔎 Ver diferencias o antecedentes complementarios"):
                    for diferencia in diferencias_tech:
                        st.write(f"• {diferencia}")

            with st.expander("📚 Ver solución LOSCAT utilizada como referencia"):
                st.write(f"**Código:** {codigo_ref_tech}")
                st.write(f"**Sistema:** {fila_ref_tech.get('Sistema', '')}")
                st.write(f"**Cielo interior:** {fila_ref_tech.get('Cielo_Interior', '')} {fila_ref_tech.get('Espesor_Cielo_mm', '')} mm")
                st.write(f"**Estructura:** {fila_ref_tech.get('Estructura_Principal', '')}")
                st.write(f"**Aislación:** {fila_ref_tech.get('Aislante', '')} {fila_ref_tech.get('Espesor_Aislante_mm', '')} mm")
                st.write(f"**Densidad mínima de referencia:** {fila_ref_tech.get('Densidad_Aislante_Min_kg_m3', '')} kg/m³")
                st.write(f"**Ventilación:** {fila_ref_tech.get('Ventilacion_Entretecho', '')}")
                st.write(f"**Fuente:** {fila_ref_tech.get('Fuente', '')}")
                st.write(f"**Observación:** {fila_ref_tech.get('Observacion', '')}")

        elif tipo_techumbre_reg == "Otro sistema":
            descripcion_otra_tech = st.text_area(
                "Describe la estructura, cielo, aislación y cubierta que conozcas:",
                placeholder="Ej.: vigas de madera, cielo de yeso-cartón, lana mineral 100 mm, cubierta metálica...",
                key="reg_tech_otro_descripcion"
            )
            resultado_techumbre_regularizacion = {
                "estado": "No verificable con las soluciones registradas",
                "sistema_ingresado": "Otro sistema",
                "codigo_referencia": None,
                "u_referencia": None,
                "rt_referencia": None,
                "diferencias": [descripcion_otra_tech] if descripcion_otra_tech else [],
            }
            st.info(
                "ℹ️ La solución ingresada no coincide con el conjunto acotado de referencias del prototipo. "
                "Su desempeño deberá respaldarse mediante antecedente técnico adecuado."
            )

        elif tipo_techumbre_reg == "No sé cómo está construida":
            resultado_techumbre_regularizacion = {
                "estado": "No verificable por falta de antecedentes",
                "sistema_ingresado": "No identificado",
                "codigo_referencia": None,
                "u_referencia": None,
                "rt_referencia": None,
                "diferencias": ["El usuario no conoce la composición de la techumbre existente."],
            }
            st.info("ℹ️ Para verificar la techumbre se requiere identificar su estructura, cielo y aislación térmica.")

        elif tipo_techumbre_reg == "Seleccione una opción...":
            st.info("Selecciona el sistema de techumbre para iniciar la comparación.")

    st.caption(
        "🌡️ Los valores U y Rt se muestran únicamente cuando la configuración ingresada coincide con los parámetros "
        "críticos de una referencia registrada. Esta revisión no reemplaza memoria de cálculo, ensayo, certificación ni revisión profesional."
    )

    # ==========================================
    # 9. CHECKLIST DOCUMENTAL
    # ==========================================
    st.markdown("""
    <div class="reg-section reg-documentos">
        <span class="numero">9</span><span class="titulo">📑 Checklist Orientativo de Antecedentes</span>
        <span class="descripcion">Permite organizar los principales documentos y antecedentes que deberán revisarse para la tramitación correspondiente.</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption(
        "Este listado sirve únicamente para organizar antecedentes. No valida documentos ni reemplaza "
        "la elaboración, firma o revisión profesional correspondiente."
    )

    documentos = [
        ("Declaración simple del propietario", "reg_doc_declaracion"),
        ("Especificaciones técnicas resumidas", "reg_doc_eett"),
        ("Croquis de ubicación", "reg_doc_croquis"),
        ("Plano de emplazamiento", "reg_doc_emplazamiento"),
        ("Planos de arquitectura", "reg_doc_planos"),
        ("Cuadro e información de superficies", "reg_doc_superficies"),
        ("Informe del profesional competente", "reg_doc_informe"),
        ("Antecedentes para acreditar antigüedad de la edificación", "reg_doc_antiguedad"),
        ("Certificado de avalúo fiscal", "reg_doc_avaluo"),
        ("Formulario/certificado de estadísticas de edificación, cuando corresponda", "reg_doc_estadisticas"),
    ]

    docs_marcados = []
    doc_col1, doc_col2 = st.columns(2)
    mitad_docs = (len(documentos) + 1) // 2

    for idx, (nombre_doc, clave_doc) in enumerate(documentos):
        columna = doc_col1 if idx < mitad_docs else doc_col2
        with columna:
            tiene_doc = st.checkbox(nombre_doc, key=clave_doc)
            docs_marcados.append((nombre_doc, tiene_doc))

    total_docs = len(documentos)
    cantidad_docs = sum(1 for _, marcado in docs_marcados if marcado)
    st.progress(cantidad_docs / total_docs if total_docs else 0)
    st.caption(f"Antecedentes marcados: **{cantidad_docs} de {total_docs}**")

    faltantes_docs = [nombre for nombre, marcado in docs_marcados if not marcado]
    if faltantes_docs:
        with st.expander("📌 Ver antecedentes aún no marcados"):
            for nombre in faltantes_docs:
                st.write(f"• {nombre}")
    else:
        st.success("✅ Todos los antecedentes del checklist orientativo fueron marcados.")

    # ==========================================
    # 10. RESULTADO FINAL Y GUARDADO
    # ==========================================
    st.markdown("""
    <div class="reg-section reg-resultado">
        <span class="numero">10</span><span class="titulo">📋 Resultado Final de la Revisión Preliminar</span>
        <span class="descripcion">Consolida la vía orientativa, revisión urbanística, condiciones técnicas, envolvente existente y documentación pendiente.</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption(
        "La síntesis reúne los antecedentes ingresados durante toda la evaluación. "
        "Los estados indican compatibilidad preliminar, observaciones o información pendiente; "
        "no equivalen a una aprobación municipal ni a una certificación profesional."
    )

    # ---------- Utilidades del resumen ----------
    def _estado_envolvente(resultado):
        estado = str(resultado.get("estado", "No evaluado"))
        estado_lower = estado.lower()
        if "coincidencia con solución" in estado_lower or "referencia térmica compatible" in estado_lower:
            return "ok", estado
        if "no evaluado" in estado_lower:
            return "pendiente", estado
        if "parcial" in estado_lower or "no verificable" in estado_lower or "requiere" in estado_lower:
            return "pendiente", estado
        return "pendiente", estado

    def _mostrar_estado(etiqueta, tipo, texto):
        if tipo == "ok":
            st.success(f"✅ **{etiqueta}:** {texto}")
        elif tipo == "error":
            st.error(f"❌ **{etiqueta}:** {texto}")
        elif tipo == "info":
            st.info(f"ℹ️ **{etiqueta}:** {texto}")
        else:
            st.warning(f"⚠️ **{etiqueta}:** {texto}")

    observaciones_finales = []
    pendientes_finales = []

    # ---------- A. Ruta y datos generales ----------
    st.markdown('<div class="reg-subtitulo">🧭 A. Vía preliminar identificada</div>', unsafe_allow_html=True)
    if procedimiento_orientativo in ["Artículo 1°", "Artículo 3°"]:
        _mostrar_estado("Procedimiento", "ok", procedimiento_orientativo)
    elif procedimiento_orientativo in ["No se identifica acceso preliminar", "Fuera de los umbrales analizados"]:
        _mostrar_estado("Procedimiento", "error", procedimiento_orientativo)
        observaciones_finales.append(f"Ruta de regularización: {procedimiento_orientativo}.")
    else:
        _mostrar_estado("Procedimiento", "pendiente", procedimiento_orientativo)
        pendientes_finales.append("Faltan antecedentes para identificar de manera preliminar el procedimiento aplicable.")

    limite_sup = 90.0 if procedimiento_orientativo == "Artículo 1°" else 140.0 if procedimiento_orientativo == "Artículo 3°" else None
    limite_av = 1000.0 if procedimiento_orientativo == "Artículo 1°" else 2000.0 if procedimiento_orientativo == "Artículo 3°" else None

    datos_col1, datos_col2, datos_col3, datos_col4 = st.columns(4)
    with datos_col1:
        st.metric("Superficie edificada", f"{superficie_regularizar:.2f} m²")
    with datos_col2:
        st.metric("Avalúo informado", f"{avaluo_fiscal_uf:.2f} UF")
    with datos_col3:
        st.metric("Número de pisos", str(numero_pisos_reg))
    with datos_col4:
        st.metric("Zona PRC", zona_codigo_reg if zona_codigo_reg else "Pendiente")

    if limite_sup is not None:
        _mostrar_estado(
            "Superficie",
            "ok" if superficie_regularizar <= limite_sup else "error",
            f"{superficie_regularizar:.2f} m² / referencia de la vía: hasta {limite_sup:.0f} m²"
        )
    if limite_av is not None:
        _mostrar_estado(
            "Avalúo fiscal",
            "ok" if avaluo_fiscal_uf <= limite_av else "error",
            f"{avaluo_fiscal_uf:.2f} UF / referencia de la vía: hasta {limite_av:.0f} UF"
        )

    condiciones_generales = [
        ("Recepción definitiva", sin_recepcion == "Sí", sin_recepcion, "Se informó que la vivienda no cuenta con recepción definitiva total o parcial."),
        ("Antigüedad", construida_antes_ley == "Sí", construida_antes_ley, "Se informó que la edificación existía antes de la publicación de la Ley N.º 20.898."),
        ("Uso residencial", uso_residencial == "Sí", uso_residencial, "El uso residencial aparece compatible según los antecedentes ingresados."),
        ("Área restringida", area_restringida == "No", area_restringida, "No se informó emplazamiento en área de riesgo/protección, utilidad pública o bien nacional de uso público."),
        ("Reclamaciones", reclamaciones == "No", reclamaciones, "No se informaron reclamaciones escritas pendientes por incumplimiento urbanístico."),
    ]

    with st.expander("🏠 Ver condiciones generales de acceso"):
        for nombre, cumple, respuesta, texto_ok in condiciones_generales:
            if cumple:
                st.write(f"✅ **{nombre}:** {texto_ok}")
            elif respuesta in ["Seleccione una opción...", "No estoy seguro/a"]:
                st.write(f"⚠️ **{nombre}:** pendiente de verificar.")
                pendientes_finales.append(f"{nombre}: antecedente pendiente de verificar.")
            else:
                st.write(f"❌ **{nombre}:** la respuesta ingresada requiere revisión para esta vía.")
                observaciones_finales.append(f"{nombre}: la respuesta ingresada requiere revisión.")

    # ---------- B. Revisión urbanística ----------
    st.markdown('<div class="reg-subtitulo">📐 B. Revisión urbanística</div>', unsafe_allow_html=True)
    if procedimiento_orientativo == "Artículo 3°":
        if evaluacion_ocupacion_art3 == "Dentro del límite especial de 0,80":
            _mostrar_estado("Ocupación de suelo/pisos", "ok", evaluacion_ocupacion_art3)
        elif "Supera" in evaluacion_ocupacion_art3:
            _mostrar_estado("Ocupación de suelo/pisos", "error", evaluacion_ocupacion_art3)
            observaciones_finales.append("El coeficiente de ocupación calculado supera 0,80; no puede asumirse esa excepción del artículo 3°.")
        else:
            _mostrar_estado("Ocupación de suelo/pisos", "pendiente", evaluacion_ocupacion_art3)
            pendientes_finales.append("Revisión del coeficiente de ocupación pendiente.")

        if "Excepción aplicable preliminarmente" in evaluacion_constructibilidad_art3:
            _mostrar_estado("Constructibilidad", "ok", evaluacion_constructibilidad_art3)
        else:
            _mostrar_estado("Constructibilidad", "pendiente", evaluacion_constructibilidad_art3)
            pendientes_finales.append("La excepción de constructibilidad no puede asumirse automáticamente; revisar norma aplicable.")

        if coef_ocupacion_suelo_real is not None:
            st.caption(
                f"Ocupación Piso 1: {coef_ocupacion_suelo_real:.2f} · "
                + (f"Piso 2: {coef_ocupacion_piso2_real:.2f} · " if superficie_piso2_reg > 0 else "")
                + f"Constructibilidad real: {coef_constructibilidad_real:.2f}"
            )
    elif procedimiento_orientativo == "Artículo 1°":
        _mostrar_estado(
            "Coeficientes PRC",
            "info",
            "Se conservan como antecedentes geométricos; no se aplican en este prototipo como el mismo filtro de una futura ampliación."
        )
    else:
        _mostrar_estado("Revisión urbanística", "pendiente", "Se habilita una vez identificada una vía preliminar.")

    # ---------- C. Habitabilidad, seguridad y estabilidad ----------
    st.markdown('<div class="reg-subtitulo">🧱 C. Habitabilidad, seguridad y estabilidad</div>', unsafe_allow_html=True)

    def _tipo_estado_tecnico(estado):
        est = str(estado).lower()
        if "compatible preliminarmente" in est:
            return "ok"
        if "presenta observaciones" in est:
            return "error"
        if "requiere" in est or "no evaluado" in est:
            return "pendiente"
        return "pendiente"

    for etiqueta, evaluacion in [
        ("Habitabilidad", evaluacion_habitabilidad_reg),
        ("Seguridad contra incendios", evaluacion_seguridad_reg),
        ("Estabilidad estructural", evaluacion_estabilidad_reg),
    ]:
        tipo_eval = _tipo_estado_tecnico(evaluacion.get("estado", "No evaluado"))
        _mostrar_estado(etiqueta, tipo_eval, evaluacion.get("estado", "No evaluado"))
        if tipo_eval == "error":
            observaciones_finales.extend(evaluacion.get("observaciones", []))
        elif tipo_eval == "pendiente":
            pendientes_finales.extend(evaluacion.get("observaciones", []))

        if evaluacion.get("observaciones"):
            with st.expander(f"Ver detalle: {etiqueta}"):
                for obs in evaluacion.get("observaciones", []):
                    st.write(f"• {obs}")

    # ---------- D. Envolvente existente ----------
    st.markdown('<div class="reg-subtitulo">🌡️ D. Envolvente constructiva existente</div>', unsafe_allow_html=True)
    envolventes = [
        ("Muro", resultado_muro_regularizacion),
        ("Piso", resultado_piso_regularizacion),
        ("Techumbre", resultado_techumbre_regularizacion),
    ]

    for etiqueta, resultado_env in envolventes:
        tipo_env, texto_env = _estado_envolvente(resultado_env)
        _mostrar_estado(etiqueta, tipo_env, texto_env)

        if tipo_env != "ok":
            pendientes_finales.append(f"{etiqueta}: {texto_env}.")

        codigo_env = resultado_env.get("codigo_referencia")
        u_env = resultado_env.get("u_referencia")
        rt_env = resultado_env.get("rt_referencia")
        detalles = []
        if codigo_env:
            detalles.append(f"referencia {codigo_env}")
        if u_env is not None:
            detalles.append(f"U = {u_env:.2f} W/m²K")
        if rt_env is not None:
            detalles.append(f"Rt = {rt_env:.2f} m²K/W")
        if detalles:
            st.caption(f"{etiqueta}: " + " · ".join(detalles))

    st.caption(
        "Una coincidencia con una solución de referencia permite comparar la composición y su desempeño térmico registrado; "
        "no constituye por sí sola certificación del elemento existente ni acredita resistencia al fuego o estabilidad."
    )

    # ---------- E. Documentación ----------
    st.markdown('<div class="reg-subtitulo">📑 E. Antecedentes documentales</div>', unsafe_allow_html=True)
    docs_col_a, docs_col_b = st.columns(2)
    with docs_col_a:
        st.metric("Antecedentes identificados", f"{cantidad_docs} de {total_docs}")
    with docs_col_b:
        st.metric("Pendientes", len(faltantes_docs))

    if faltantes_docs:
        _mostrar_estado(
            "Documentación",
            "pendiente",
            f"Faltan {len(faltantes_docs)} antecedente(s) del checklist orientativo."
        )
        pendientes_finales.append(f"Faltan {len(faltantes_docs)} antecedentes del checklist documental.")
        with st.expander("📌 Ver documentos pendientes en el resultado final"):
            for doc in faltantes_docs:
                st.write(f"• {doc}")
    else:
        _mostrar_estado("Documentación", "ok", "Todos los antecedentes del checklist fueron marcados.")

    # Eliminar duplicados conservando el orden para una salida limpia.
    observaciones_finales = list(dict.fromkeys([x for x in observaciones_finales if x]))
    pendientes_finales = list(dict.fromkeys([x for x in pendientes_finales if x]))

    # ---------- F. Conclusión global ----------
    st.markdown('<div class="reg-subtitulo">🧾 F. Conclusión preliminar</div>', unsafe_allow_html=True)

    if procedimiento_orientativo not in ["Artículo 1°", "Artículo 3°"]:
        if procedimiento_orientativo in ["No se identifica acceso preliminar", "Fuera de los umbrales analizados"]:
            resultado_global_reg = "No se identifica una vía preliminar compatible con los antecedentes ingresados"
            st.error(
                "❌ **No se identifica una vía preliminar compatible con los antecedentes ingresados.** "
                "Esto no equivale a una resolución definitiva; corresponde revisar el caso y sus antecedentes con un profesional competente y la DOM."
            )
        else:
            resultado_global_reg = "No es posible concluir por falta de antecedentes"
            st.warning(
                "⚠️ **No es posible concluir todavía.** Faltan antecedentes para identificar y revisar de manera preliminar la vía de regularización."
            )
    elif observaciones_finales:
        resultado_global_reg = "Condiciones preliminares de acceso con observaciones que deben resolverse o acreditarse"
        st.warning(
            f"⚠️ **La vivienda presenta condiciones preliminares asociadas al {procedimiento_orientativo}, "
            "pero existen observaciones técnicas o normativas que deben resolverse, corregirse o acreditarse antes de una tramitación formal.**"
        )
    elif pendientes_finales:
        resultado_global_reg = "Condiciones preliminares compatibles con antecedentes pendientes de verificación"
        st.warning(
            f"⚠️ **La vivienda presenta condiciones preliminares compatibles con el {procedimiento_orientativo}, "
            "pero todavía existen antecedentes o verificaciones pendientes.**"
        )
    else:
        resultado_global_reg = "Condiciones preliminares compatibles, sujetas a revisión profesional y DOM"
        st.success(
            f"✅ **Con los antecedentes ingresados, la vivienda presenta condiciones preliminares compatibles con el {procedimiento_orientativo}.** "
            "La tramitación continúa requiriendo los antecedentes, intervención profesional y revisión de la Dirección de Obras Municipales que correspondan."
        )

    if observaciones_finales:
        with st.expander(f"❌ Observaciones detectadas ({len(observaciones_finales)})"):
            for obs in observaciones_finales:
                st.write(f"• {obs}")

    if pendientes_finales:
        with st.expander(f"⚠️ Antecedentes o verificaciones pendientes ({len(pendientes_finales)})"):
            for pendiente in pendientes_finales:
                st.write(f"• {pendiente}")

    st.info(
        "📌 **Alcance del resultado:** esta síntesis es una herramienta de apoyo preliminar. "
        "No reemplaza el informe del profesional competente, los antecedentes técnicos que deban acreditarse, "
        "ni la revisión y resolución de la Dirección de Obras Municipales."
    )

    # ---------- Guardado ----------
    if st.button("💾 Guardar Resultado de Regularización", type="primary"):
        st.session_state.resultado_regularizacion = {
            "procedimiento_orientativo": procedimiento_orientativo,
            "resultado_global": resultado_global_reg,
            "fuente_datos": fuente_datos_regularizacion,
            "superficie_terreno_m2": float(superficie_terreno_reg),
            "superficie_piso1_m2": float(superficie_piso1_reg),
            "superficie_piso2_m2": float(superficie_piso2_reg),
            "superficie_otros_pisos_m2": float(superficie_otros_pisos_reg),
            "superficie_m2": float(superficie_regularizar),
            "numero_pisos": numero_pisos_reg,
            "zona_codigo": zona_codigo_reg,
            "avaluo_uf": float(avaluo_fiscal_uf),
            "coef_ocupacion_suelo_real": (
                float(coef_ocupacion_suelo_real)
                if coef_ocupacion_suelo_real is not None
                else None
            ),
            "coef_ocupacion_piso2_real": (
                float(coef_ocupacion_piso2_real)
                if coef_ocupacion_piso2_real is not None
                else None
            ),
            "coef_constructibilidad_real": (
                float(coef_constructibilidad_real)
                if coef_constructibilidad_real is not None
                else None
            ),
            "coef_ocupacion_prc_referencia": coef_ocupacion_prc_reg,
            "coef_constructibilidad_prc_referencia": coef_constructibilidad_prc_reg,
            "evaluacion_ocupacion_art3": evaluacion_ocupacion_art3,
            "evaluacion_constructibilidad_art3": evaluacion_constructibilidad_art3,
            "evaluacion_habitabilidad": evaluacion_habitabilidad_reg,
            "evaluacion_seguridad": evaluacion_seguridad_reg,
            "evaluacion_estabilidad": evaluacion_estabilidad_reg,
            "revision_muro": resultado_muro_regularizacion,
            "revision_piso": resultado_piso_regularizacion,
            "revision_techumbre": resultado_techumbre_regularizacion,
            "sin_recepcion": sin_recepcion,
            "construida_antes_ley": construida_antes_ley,
            "uso_residencial": uso_residencial,
            "area_restringida": area_restringida,
            "reclamaciones": reclamaciones,
            "documentos_marcados": [nombre for nombre, marcado in docs_marcados if marcado],
            "documentos_pendientes": faltantes_docs,
            "observaciones_finales": observaciones_finales,
            "pendientes_finales": pendientes_finales,
        }
        st.success("✅ Resultado preliminar de regularización guardado correctamente.")

    if st.session_state.resultado_regularizacion is not None:
        with st.expander("✅ Ver último resultado guardado"):
            reg_guardada = st.session_state.resultado_regularizacion
            st.write(f"**Ruta preliminar:** {reg_guardada.get('procedimiento_orientativo', 'Pendiente')}")
            st.write(f"**Resultado global:** {reg_guardada.get('resultado_global', 'Sin síntesis guardada')}")
            st.write(f"**Superficie del terreno:** {reg_guardada.get('superficie_terreno_m2', 0.0):.2f} m²")
            st.write(f"**Superficie edificada:** {reg_guardada.get('superficie_m2', 0.0):.2f} m²")
            st.write(f"**Avalúo:** {reg_guardada.get('avaluo_uf', 0.0):.2f} UF")
            if reg_guardada.get("coef_ocupacion_suelo_real") is not None:
                st.write(f"**Coeficiente real de ocupación Piso 1:** {reg_guardada['coef_ocupacion_suelo_real']:.2f}")
            if reg_guardada.get("coef_constructibilidad_real") is not None:
                st.write(f"**Coeficiente real de constructibilidad:** {reg_guardada['coef_constructibilidad_real']:.2f}")
            st.write(f"**Documentos pendientes:** {len(reg_guardada.get('documentos_pendientes', []))}")
            st.write(f"**Muro:** {reg_guardada.get('revision_muro', {}).get('estado', 'No evaluado')}")
            st.write(f"**Piso:** {reg_guardada.get('revision_piso', {}).get('estado', 'No evaluado')}")
            st.write(f"**Techumbre:** {reg_guardada.get('revision_techumbre', {}).get('estado', 'No evaluado')}")
    st.markdown("---")
    st.info(
        "📌 **Ruta diferenciada:** este módulo se mantiene separado de la evaluación de una futura ampliación. "
        "Las flexibilidades o excepciones de la Ley N.º 20.898 no se aplican automáticamente al diseño de una obra nueva."
    )
