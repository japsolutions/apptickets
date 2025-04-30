import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import time
import io

# Configurar la página de Streamlit
st.set_page_config(page_title="Descriptive Analysis of Tickets Service Now", layout="wide")
st.title("Descriptive Ticket Analysis")

# Función para cargar archivo
def cargar_archivo():
    archivo = st.file_uploader("Upload an Excel or CSV file", type=["csv", "xlsx"])
    if archivo is not None:
        try:
            if archivo.name.endswith('.csv'):
                df = pd.read_csv(archivo)
            elif archivo.name.endswith('.xlsx'):
                df = pd.read_excel(archivo)
            else:
                st.error("Unsupported format.")
                return None
            return df
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return None
    return None

# Cargar datos
df = cargar_archivo()

# Mostrar datos cargados si existen
if df is not None:
    st.subheader("Preview of the Data")
    st.dataframe(df)

    # Análisis descriptivo
    st.subheader("Descriptive Analysis")
    st.write(df.describe(include='all'))

    # Formulario para edición de datos
    with st.form("data_edit_form"):
        st.subheader("Edit Data")
        df_editado = st.data_editor(df)
        submitted = st.form_submit_button("Save Changes")

    # Botón de descarga fuera del formulario
    if submitted:
        try:
            # Preparar el archivo Excel en memoria
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_editado.to_excel(writer, index=False)
            excel_data = output.getvalue()

            # Generar nombre único para el archivo
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"edited_data_{timestamp}.xlsx"

            # Botón para descargar el archivo editado
            st.download_button(
                label="Download Edited Data as Excel",
                data=excel_data,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"Error saving changes: {e}")
    
    # Visualización de las variables
    st.subheader("Variable Visualization")
    columns = st.multiselect("Select Columns to Plot", df.columns)

    for column in columns:
        fig, ax = plt.subplots(figsize=(8, 6))
        
        try:
            if pd.api.types.is_numeric_dtype(df[column]):
                # Histograma para variables numéricas
                df[column].hist(bins=20, color='orange', alpha=0.7, ax=ax)
                ax.set_title(f"Histogram of {column}")
            else:
                # Gráfico de barras para variables categóricas
                df[column].value_counts().plot(kind='bar', color='skyblue', ax=ax)
                ax.set_title(f"Distribution of {column}")
            
            ax.set_xlabel(column)
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
        except Exception as e:
            st.warning(f"Could not plot column {column}: {str(e)}")
else:
    st.info("Please upload a file to start the analysis.")