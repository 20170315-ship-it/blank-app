import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
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
# 2. MOSTRAR LA IMAGEN ADJUNTA (Tabla de Fórmulas)
# =====================================================================
nombre_imagen = "image_ebb78a.jpg"
if os.path.exists(nombre_imagen):
    st.image(nombre_imagen, caption="Resumen de las ecuaciones de tiempo de concentración (Chow, 1994)", use_container_width=True)
else:
    st.warning(f"Aviso: Coloque la imagen '{nombre_imagen}' en la misma carpeta del script para visualizar la tabla resumen.")

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
    st.info("**Observación:** Desarrollada para cuencas rurales con canales bien definidos y pendientes empinadas.")
    
    # Campo L
    L = st.number_input("Longitud del canal desde aguas arriba hasta la salida (L) [m]", value=0.0, step=10.0)
    if L <= 0:
        st.error("❌ Error: La longitud (L) debe ser un número mayor a cero.")
        inputs_validos = False
        
    # Campo S
    S = st.number_input("Pendiente promedio de la cuenca (S) [m/m]", value=0.0, step=0.001, format="%.4f")
    if S <= 0:
        st.error("❌ Error: La pendiente (S) debe ser un número mayor a cero.")
        inputs_validos = False

    # Cálculo final si pasa la validación
    if inputs_validos:
        tc = 0.01947 * (L ** 0.77) * (S ** -0.385)

elif metodo == "California Culverts Practice (1942)":
    st.info("**Observación:** Esencialmente la ecuación de Kirpich; desarrollada para pequeñas cuencas montañosas en California.")
    
    # Campo L
    L = st.number_input("Longitud del curso de agua más largo (L) [m]", value=0.0, step=10.0)
    if L <= 0:
        st.error("❌ Error: La longitud (L) debe ser un número mayor a cero.")
        inputs_validos = False
        
    # Campo H
    H = st.number_input("Diferencia de nivel entre la divisoria de aguas y la salida (H) [m]", value=0.0, step=1.0)
    if H <= 0:
        st.error("❌ Error: La diferencia de nivel (H) debe ser un número mayor a cero.")
        inputs_validos = False

    if inputs_validos:
        tc = 0.0195 * ((L ** 3) / H) ** 0.385

elif metodo == "Izzard (1946)":
    st.info("**Observación:** Desarrollada para flujo superficial en caminos y césped. Requiere que el producto de $i \\cdot L \\le 3800$.")
    
    # Campo i
    i_lluvia = st.number_input("Intensidad de lluvia (i) [mm/h]", value=0.0, step=1.0)
    if i_lluvia <= 0:
        st.error("❌ Error: La intensidad de lluvia (i) debe ser mayor a cero.")
        inputs_validos = False
        
    # Campo c
    c = st.number_input("Coeficiente de retardo (c) [adimensional]", value=0.0, step=0.01, format="%.3f")
    if c <= 0:
        st.error("❌ Error: El coeficiente de retardo (c) debe ser mayor a cero.")
        inputs_validos = False
        
    # Campo L
    L = st.number_input("Longitud de la trayectoria de flujo (L) [m]", value=0.0, step=5.0)
    if L <= 0:
        st.error("❌ Error: La longitud (L) debe ser mayor a cero.")
        inputs_validos = False
        
    # Campo S
    S = st.number_input("Pendiente de la trayectoria de flujo (S) [m/m]", value=0.0, step=0.001, format="%.4f")
    if S <= 0:
        st.error("❌ Error: La pendiente (S) debe ser mayor a cero.")
        inputs_validos = False

    # Validación adicional del límite específico del método de Izzard
    if inputs_validos:
        producto_il = i_lluvia * L
        if producto_il > 3800:
            st.warning(f"⚠️ Advertencia: El producto de i · L ({producto_il:.1f}) es mayor que 3800. El método puede perder precisión.")
        
        # Fórmula de Izzard
        numerador = 525 * (0.0000276 * i_lluvia + c) * (L ** 0.33)
        denominador = (S ** 0.333) * (i_lluvia ** 0.667)
        tc = numerador / denominador

elif metodo == "Federal Aviation Administration (1970)":
    st.info("**Observación:** Desarrollada de información sobre el drenaje de aeropuertos. Muy usado para flujo superficial urbano.")
    
    # Campo C
    C = st.number_input("Coeficiente de escorrentía del método racional (C) [adimensional]", value=0.0, min_value=0.0, max_value=1.0, step=0.05)
    if C <= 0 or C >= 1.1: # Ajuste según la fórmula (1.1 - C) requiere que C < 1.1, pero físicamente C <= 1
        st.error("❌ Error: El coeficiente de escorrentía (C) debe estar en el rango típico entre 0 y 1.")
        inputs_validos = False
        
    # Campo L
    L = st.number_input("Longitud del flujo superficial (L) [m]", value=0.0, step=10.0)
    if L <= 0:
        st.error("❌ Error: La longitud (L) debe ser mayor a cero.")
        inputs_validos = False
        
    # Campo S
    S = st.number_input("Pendiente de la superficie (S) [m/m]", value=0.0, step=0.001, format="%.4f")
    if S <= 0:
        st.error("❌ Error: La pendiente (S) debe ser mayor a cero.")
        inputs_validos = False

    if inputs_validos:
        tc = 0.7035 * ((1.1 - C) * (L ** 0.50)) / (S ** 0.333)

elif metodo == "Ecuaciones de onda cinemática (Morgali y Linsley, 1965 / Aron y Erborge, 1973)":
    st.info("**Observación:** Ecuación para flujo superficial basada en análisis hidráulico. Requiere procesos iterativos normalmente si i o tc son desconocidos.")
    
    # Campo L
    L = st.number_input("Longitud del flujo superficial (L) [m]", value=0.0, step=10.0)
    if L <= 0:
        st.error("❌ Error: La longitud (L) debe ser mayor a cero.")
        inputs_validos = False
        
    # Campo n
    n = st.number_input("Coeficiente de rugosidad de Manning (n) [adimensional]", value=0.0, step=0.01, format="%.3f")
    if n <= 0:
        st.error("❌ Error: El coeficiente de Manning (n) debe ser mayor a cero.")
        inputs_validos = False
        
    # Campo i
    i_lluvia = st.number_input("Intensidad de lluvia (i) [mm/h]", value=0.0, step=1.0)
    if i_lluvia <= 0:
        st.error("❌ Error: La intensidad de lluvia (i) debe ser mayor a cero.")
        inputs_validos = False
        
    # Campo S
    S = st.number_input("Pendiente promedio del terreno (S) [m/m]", value=0.0, step=0.001, format="%.4f")
    if S <= 0:
        st.error("❌ Error: La pendiente (S) debe ser mayor a cero.")
        inputs_validos = False

    if inputs_validos:
        tc = (7 * (L ** 0.6) * (n ** 0.6)) / ((i_lluvia ** 0.4) * (S ** 0.3))

elif metodo == "Ecuación de retardo SCS (1973)":
    st.info("**Observación:** Desarrollada por el SCS para cuencas de uso agrícola menores a 810 ha. Tiende a sobreestimar en áreas mixtas.")
    
    # Campo L
    L = st.number_input("Longitud hidráulica de la cuenca / Mayor trayectoria de flujo (L) [m]", value=0.0, step=10.0)
    if L <= 0:
        st.error("❌ Error: La longitud (L) debe ser mayor a cero.")
        inputs_validos = False
        
    # Campo CN
    CN = st.number_input("Número de curva SCS (CN) [adimensional]", value=0.0, step=1.0, max_value=100.0)
    if CN <= 0 or CN > 100:
        st.error("❌ Error: El Número de Curva (CN) debe estar estrictamente entre 0 y 100.")
        inputs_validos = False
        
    # Campo S
    S = st.number_input("Pendiente promedio de la cuenca (S) [m/m]", value=0.0, step=0.001, format="%.4f")
    if S <= 0:
        st.error("❌ Error: La pendiente (S) debe ser mayor a cero.")
        inputs_validos = False

    if inputs_validos:
        # Evitar división por cero o raíces negativas si CN es inválido
        tc = (0.0136 * (L ** 0.8) * (((1000 / CN) - 9) ** 0.7)) / (S ** 0.5)

# =====================================================================
# 5. PRESENTACIÓN DE RESULTADOS
# =====================================================================
st.markdown("---")
st.markdown("### Resultado del Cálculo")

if inputs_validos:
    # Mostrar métrica del resultado destacado
    st.metric(label="Tiempo de Concentración ($T_c$)", value=f"{tc:.2f} min")
    
    # Explicación del resultado mediante texto dinámico
    st.success(f"**Conclusión:** Según el método de **{metodo}**, el tiempo de concentración calculado es de **{tc:.2f}** minutos.")
else:
    st.info("Por favor, corrija los campos marcados en rojo arriba para poder proceder con el cálculo del tiempo de concentración.")
