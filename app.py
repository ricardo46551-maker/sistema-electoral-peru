import streamlit as st
from scraper import consultar_multa

# Configuración de la página
st.set_page_config(page_title="Consulta Multas JNE", page_icon="🇵🇪")

st.title("🇵🇪 Monitor Electoral")
st.write("Consulta si tienes multas electorales pendientes.")

# Entrada de datos
dni = st.text_input("Ingresa tu número de DNI", max_chars=8)

if st.button("Consultar DNI"):
    if len(dni) == 8 and dni.isdigit():
        with st.spinner('Consultando al JNE... por favor espera'):
            # Llamamos a la función del otro archivo
            resultado = consultar_multa(dni)
            
            # Mostramos resultado
            if "Error" in resultado:
                st.error(resultado)
            else:
                st.success("Resultado encontrado:")
                st.info(resultado)
    else:
        st.warning("Por favor ingresa un DNI válido de 8 dígitos.")