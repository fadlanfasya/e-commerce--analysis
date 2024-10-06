import streamlit as st
import nbformat
from nbconvert import PythonExporter
import matplotlib.pyplot as plt
import pandas as pd

# Define the path to your Jupyter notebook
NOTEBOOK_PATH = "./analysis_data.ipynb"

# Load the Jupyter notebook
def load_notebook(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return nbformat.read(f, as_version=4)

# Convert Jupyter notebook to Python code
def convert_notebook_to_python(nb):
    exporter = PythonExporter()
    python_code, _ = exporter.from_notebook_node(nb)
    return python_code

# Extract markdown and raw text cells from notebook
def extract_notebook_text(nb):
    texts = []
    for cell in nb.cells:
        if cell.cell_type == 'markdown' or cell.cell_type == 'raw':
            texts.append(cell.source)
    return texts

# Execute the converted notebook code and capture matplotlib figures
def run_notebook_code(python_code, globals_dict):
    exec(python_code, globals_dict)

# Streamlit App Interface
def main():
    st.title("Ecommerce Analysis Dashboard")

    # Load and convert notebook
    notebook_content = load_notebook(NOTEBOOK_PATH)
    python_code = convert_notebook_to_python(notebook_content)

    # Extract text sections from the notebook
    notebook_texts = extract_notebook_text(notebook_content)
    
    # Display notebook text sections
    st.subheader("Notebook Sections:")
    for text in notebook_texts:
        st.markdown(text)  # Render markdown or raw text in Streamlit

    # Automatically run the notebook
    output_globals = {}

    # Clear any previous figures in case notebook contains multiple plot commands
    plt.close('all')
    
    # Run the notebook code and capture output
    run_notebook_code(python_code, output_globals)
    
    # Display variables from the notebook
    st.subheader("Analysis Results:")
    for var_name, value in output_globals.items():
        if not var_name.startswith("__"):  # Skip internal variables
            if isinstance(value, pd.DataFrame):  # Check if it's a DataFrame
                st.subheader(f"DataFrame: {var_name}")
                st.dataframe(value)  # Display the DataFrame as an interactive table
            else:
                st.write(f"{var_name}: {value}")

    # Display any matplotlib figures
    st.subheader("Generated Plots:")
    figures = [plt.figure(i) for i in plt.get_fignums()]
    
    if not figures:
        st.write("No plots were generated.")
    
    # Render and display each plot in Streamlit
    for fig in figures:
        st.pyplot(fig)

if __name__ == "__main__":
    main()
