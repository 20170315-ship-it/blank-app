import streamlit as st

st.title("Hidrología")
st.write(
    "Let's go"
)
import pandas as pd  # Importamos pandas para la gestión de la tabla de datos

# =====================================================================
# 1. CONFIGURACIÓN Y TÍTULO DE LA APP
# =====================================================================
st.set_page_config(page_title="Tiempo de Concentración", layout="centered")
st.title("Estimación del Tiempo de Concentración ($T_c$)")

st.markdown("""
El tiempo de concentración ($T_c$) se define como el tiempo que tarda una gota de lluvia 
que cae en el punto hidráulicamente más alejado de la cuenca, hasta llegar al punto de drenaje de la misma.
""")

# =====================================================================
# 2. NUEVA SECCIÓN 2: MOSTRAR LA TABLA INFORMATIVA DE MÉTODOS
# =====================================================================
# Creamos la estructura de datos fiel a la tabla que proporcionaste
datos_tabla = {
    "Método (Año)": [
        "Kirpich (1940)", "",
        "California Culverts Practice (1942)", "",
        "Izzard (1946)", "", "", "",
        "Federal Aviation Administration (1970)", "", "",
        "Ecuaciones de onda cinemática (1965/1973)", "", "", "",
        "Ecuación de retardo SCS (1973)", "", ""
    ],
    "Input": [
        "L", "S",
        "L", "H",
        "i", "c", "L", "S",
        "C", "L", "S",
        "L", "n", "i", "S",
        "L", "CN", "S"
    ],
    "Descripción": [
        "Longitud del canal desde aguas arriba hasta la salida.", "Pendiente promedio de la cuenca.",
        "Longitud del curso de agua más largo.", "Diferencia de nivel entre la divisoria de aguas y la salida.",
        "Intensidad de lluvia.", "Coeficiente de retardo.", "Longitud de la trayectoria de flujo.", "Pendiente de la trayectoria de flujo.",
        "Coeficiente de escorrentía del método racional.", "Longitud del flujo superficial.", "Pendiente de la superficie.",
        "Longitud del flujo superficial.", "Coeficiente de rugosidad de Manning.", "Intensidad de lluvia.", "Pendiente promedio del terreno.",
        "Longitud hidráulica de la cuenca (mayor trayectoria de flujo).", "Número de curva SCS.", "Pendiente promedio de la cuenca."
    ],
    "Unidades": [
        "m", "m/m",
        "m", "m",
        "mm/h", "-", "m", "m/m",
        "-", "m", "m/m",
        "m", "-", "mm/h", "m/m",
        "m", "-", "m/m"
    ],
    "Observación": [
        "Desarrollada a partir de información del SCS de siete cuencas rurales de Tennessee con canales bien definidos y pendientes empinadas (3-10%); para flujo superficial en superficie de concreto o asfalto. Multiplicar tc por 0,4; para canales de concreto, multiplicar por 0,2; sin ajustes para flujo superficial en suelo descubierto o para flujo en cunetas.", "",
        "Esencialmente es la ecuación de Kirpich; desarrollada para pequeñas cuencas montañosas en California.", "",
        "Desarrollada experimentalmente en laboratorio por el Bureau of Public Roads para flujo superficial en caminos y áreas de césped; los valores del coeficiente de retardo varían desde 0,0070 para pavimentos muy lisos hasta 0,012 para pavimentos de concreto y 0,06 para superficies densamente cubiertas de pasto; la solución requiere de procesos iterativos; el producto de i por L debe ser ≤ 3800.", "", "", "",
        "Desarrollada con información sobre el drenaje de aeropuertos, recopilada por el Corps of Engineers; el método tiene como finalidad el ser usado en problemas de drenaje de aeropuertos, pero ha sido frecuentemente usado para flujo superficial en cuencas urbanas.", "", "",
        "Ecuación para flujo superficial desarrollada a partir del análisis de onda cinemática de la escorrentía superficial desde superficies desarrolladas; el método requiere iteraciones debido a que tanto i como tc son desconocidos; la superposición de una curva de intensidad-duración-frecuencia da una solución gráfica directa para tc.", "", "", "",
        "Ecuación desarrollada por el SCS a partir de información de cuencas de uso agrícola; ha sido adaptada a pequeñas cuencas urbanas con áreas inferiores a 810 ha; se ha encontrado que generalmente es buena cuando el área se encuentra completamente pavimentada; para áreas mixtas tiene tendencia a la sobreestimación; se aplican factores de ajuste para corregir efectos de mejoras en canales e impermeabilización de superficies; la ecuación supone que tc = 1,67 veces el retardo de la cuenca.", "", ""
    ]
}

# Convertimos el diccionario en un DataFrame de Pandas
df_metodos = pd.DataFrame(datos_tabla)

# Usamos un expander para que la tabla no ocupe demasiado espacio vertical de forma fija
with st.expander("📋 Ver Tabla de Referencia: Métodos, Parámetros y Observaciones", expanded=False):
    # Mostramos la tabla optimizada para el ancho del contenedor y ocultamos la columna de índices por defecto
    st.dataframe(df_metodos, hide_index=True, use_container_width=True)

# =====================================================================
# 3. PESTAÑA DESPLEGABLE PARA SELECCIÓN DEL MÉTODO
# =====================================================================
st.subheader("Configuración del Cálculo")
metodo = st.selectbox(
    "Seleccione el método que desea utilizar:",
    [
        "Kirpich (1940)",
        "California Culverts Practice (1942)",
        "Izzard (1946)",
        "Federal Aviation Administration (1970)",
        "Ecuaciones de onda cinemática (Morgali y Linsley, 1965 / Aron y Erborge, 1973)",
        "Ecuación de retardo SCS (1973)"
    ]
)

# Variable de control para saber si los datos ingresados son válidos
inputs_validos = True

# =====================================================================
# 4. CAPTURA DE INPUTS SEGÚN EL MÉTODO SELECCIONADO Y VALIDACIÓN
# =====================================================================
st.markdown("### Parámetros de Entrada")

if metodo == "Kirpich (1940)":
    st.info("**Observación:** Adecuado para cuencas rurales con pendientes empinadas (3-10%).")
    
    L = st.number_input("Longitud del canal desde aguas arriba hasta la salida (L) [m]", value=0.0, step=10.0)
    if L <= 0:
        st.error("❌ Error: La longitud (L) debe ser un número mayor a cero.")
        inputs_validos = False
        
    S = st.number_input("Pendiente promedio de la cuenca (S) [m/m]", value=0.0, step=0.001, format="%.4f")
    if S <= 0:
        st.error("❌ Error: La pendiente (S) debe ser un número mayor a cero.")
        inputs_validos = False

    if inputs_validos:
        tc = 0.01947 * (L ** 0.77) * (S ** -0.385)

elif metodo == "California Culverts Practice (1942)":
    st.info("**Observación:** Desarrollada para pequeñas cuencas montañosas en California.")
    
    L = st.number_input("Longitud del curso de agua más largo (L) [m]", value=0.0, step=10.0)
    if L <= 0:
        st.error("❌ Error: La longitud (L) debe ser un número mayor a cero.")
        inputs_validos = False
        
    H = st.number_input("Diferencia de nivel entre la divisoria de aguas y la salida (H) [m]", value=0.0, step=1.0)
    if H <= 0:
        st.error("❌ Error: La diferencia de nivel (H) debe ser un número mayor a cero.")
        inputs_validos = False

    if inputs_validos:
        tc = 0.0195 * ((L ** 3) / H) ** 0.385

elif metodo == "Izzard (1946)":
    st.info("**Observación:** Flujo superficial en caminos y césped. Requiere que $i \\cdot L \\le 3800$.")
    
    i_lluvia = st.number_input("Intensidad de lluvia (i) [mm/h]", value=0.0, step=1.0)
    if i_lluvia <= 0:
        st.error("❌ Error: La intensidad de lluvia (i) debe ser mayor a cero.")
        inputs_validos = False
        
    c = st.number_input("Coeficiente de retardo (c) [adimensional]", value=0.0, step=0.01, format="%.3f")
    if c <= 0:
        st.error("❌ Error: El coeficiente de retardo (c) debe ser mayor a cero.")
        inputs_validos = False
        
    L = st.number_input("Longitud de la trayectoria de flujo (L) [m]", value=0.0, step=5.0)
    if L <= 0:
        st.error("❌ Error: La longitud (L) debe ser mayor a cero.")
        inputs_validos = False
        
    S = st.number_input("Pendiente de la trayectoria de flujo (S) [m/m]", value=0.0, step=0.001, format="%.4f")
    if S <= 0:
        st.error("❌ Error: La pendiente (S) debe ser mayor a cero.")
        inputs_validos = False

    if inputs_validos:
        producto_il = i_lluvia * L
        if producto_il > 3800:
            st.warning(f"⚠️ Advertencia: El producto de i · L ({producto_il:.1f}) es mayor que 3800. El método puede perder precisión.")
        
        numerador = 525 * (0.0000276 * i_lluvia + c) * (L ** 0.33)
        denominador = (S ** 0.333) * (i_lluvia ** 0.667)
        tc = numerador / denominador

elif metodo == "Federal Aviation Administration (1970)":
    st.info("**Observación:** Frecuentemente usado para flujo superficial en cuencas urbanas y aeropuertos.")
    
    C = st.number_input("Coeficiente de escorrentía del método racional (C) [adimensional]", value=0.0, min_value=0.0, max_value=1.0, step=0.05)
    if C <= 0 or C > 1.0:
        st.error("❌ Error: El coeficiente de escorrentía (C) debe estar entre 0 y 1.")
        inputs_validos = False
        
    L = st.number_input("Longitud del flujo superficial (L) [m]", value=0.0, step=10.0)
    if L <= 0:
        st.error("❌ Error: La longitud (L) debe ser mayor a cero.")
        inputs_validos = False
        
    S = st.number_input("Pendiente de la superficie (S) [m/m]", value=0.0, step=0.001, format="%.4f")
    if S <= 0:
        st.error("❌ Error: La pendiente (S) debe ser mayor a cero.")
        inputs_validos = False

    if inputs_validos:
        tc = 0.7035 * ((1.1 - C) * (L ** 0.50)) / (S ** 0.333)

elif metodo == "Ecuaciones de onda cinemática (Morgali y Linsley, 1965 / Aron y Erborge, 1973)":
    st.info("**Observación:** Basada en análisis hidráulico de escorrentía. Si 'i' y 'tc' dependen entre sí, suele requerir un proceso de iteración gráfica.")
    
    L = st.number_input("Longitud del flujo superficial (L) [m]", value=0.0, step=10.0)
    if L <= 0:
        st.error("❌ Error: La longitud (L) debe ser mayor a cero.")
        inputs_validos = False
        
    n = st.number_input("Coeficiente de rugosidad de Manning (n) [adimensional]", value=0.0, step=0.01, format="%.3f")
    if n <= 0:
        st.error("❌ Error: El coeficiente de Manning (n) debe ser mayor a cero.")
        inputs_validos = False
        
    i_lluvia = st.number_input("Intensidad de lluvia (i) [mm/h]", value=0.0, step=1.0)
    if i_lluvia <= 0:
        st.error("❌ Error: La intensidad de lluvia (i) debe ser mayor a cero.")
        inputs_validos = False
        
    S = st.number_input("Pendiente promedio del terreno (S) [m/m]", value=0.0, step=0.001, format="%.4f")
    if S <= 0:
        st.error("❌ Error: La pendiente (S) debe ser mayor a cero.")
        inputs_validos = False

    if inputs_validos:
        tc = (7 * (L ** 0.6) * (n ** 0.6)) / ((i_lluvia ** 0.4) * (S ** 0.3))

elif metodo == "Ecuación de retardo SCS (1973)":
    st.info("**Observación:** Para cuencas agrícolas e hidrográficas menores a 810 ha. El tiempo calculado equivale a 1.67 veces el retardo de la cuenca.")
    
    L = st.number_input("Longitud hidráulica de la cuenca / Mayor trayectoria de flujo (L) [m]", value=0.0, step=10.0)
    if L <= 0:
        st.error("❌ Error: La longitud (L) debe ser mayor a cero.")
        inputs_validos = False
        
    CN = st.number_input("Número de curva SCS (CN) [adimensional]", value=0.0, step=1.0, max_value=100.0)
    if CN <= 0 or CN > 100:
        st.error("❌ Error: El Número de Curva (CN) debe estar estrictamente entre 0 y 100.")
        inputs_validos = False
        
    S = st.number_input("Pendiente promedio de la cuenca (S) [m/m]", value=0.0, step=0.001, format="%.4f")
    if S <= 0:
        st.error("❌ Error: La pendiente (S) debe ser mayor a cero.")
        inputs_validos = False

    if inputs_validos:
        tc = (0.0136 * (L ** 0.8) * (((1000 / CN) - 9) ** 0.7)) / (S ** 0.5)

# =====================================================================
# 5. PRESENTACIÓN DE RESULTADOS
# =====================================================================
st.markdown("---")
st.subheader("Resultado del Cálculo")

if inputs_validos:
    # Muestra la métrica destacada
    st.metric(label="Tiempo de Concentración ($T_c$)", value=f"{tc:.2f} min")
    
    # Texto dinámico explicativo solicitado
    st.success(f"**Conclusión:** Según el método de **{metodo}**, el tiempo de concentración calculado es de **{tc:.2f}** minutos.")
else:
    st.info("Por favor, corrija los campos marcados en rojo arriba para poder proceder con el cálculo del tiempo de concentración.")
