import streamlit as st
import nbformat
from nbconvert import PythonExporter

# Define the path to your Jupyter notebook
NOTEBOOK_PATH = "./analysis_data.ipynb"

# Load the Jupyter notebook
def load_notebook(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return nbformat.read(f, as_version=4)
    except FileNotFoundError:
        st.error(f"Notebook '{filename}' not found. Please check the path.")
        return None

# Convert Jupyter notebook to Python code
def convert_notebook_to_python(nb):
    exporter = PythonExporter()
    python_code, _ = exporter.from_notebook_node(nb)
    return python_code

# Execute the converted notebook code
def run_notebook_code(python_code, globals_dict):
    exec(python_code, globals_dict)

# Streamlit App Interface
def main():
    st.title("Ecommerce Analysis")

    # Load and convert notebook
    notebook_content = load_notebook(NOTEBOOK_PATH)
    if notebook_content is None:
        return

    python_code = convert_notebook_to_python(notebook_content)
    
    st.subheader("Notebook Preview:")
    st.code(python_code, language='python')
    
    if st.button("Run Notebook"):
        st.subheader("Notebook Output:")
        output_globals = {}
        run_notebook_code(python_code, output_globals)
        
        # Display variables from the notebook
        for var_name, value in output_globals.items():
            if not var_name.startswith("__"):
                st.write(f"{var_name}: {value}")

if __name__ == "__main__":
    main()
