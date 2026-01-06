# --- BLOCO DE DIAGNÓSTICO (DEBUG) ---
import os
st.write("📂 --- DIAGNÓSTICO DE ARQUIVOS ---")
st.write(f"Diretório Atual: {os.getcwd()}")

# 1. Verificar se a pasta models existe
if os.path.exists("models"):
    st.write("✅ Pasta 'models' encontrada.")
    st.write("Conteúdo da pasta 'models':")
    arquivos = os.listdir("models")
    st.write(arquivos)
    
    # 2. Verificar detalhes do arquivo
    if "modelo_obesidade.pkl" in arquivos:
        tamanho = os.path.getsize("models/modelo_obesidade.pkl")
        st.write(f"📦 Tamanho do arquivo .pkl: {tamanho / 1024:.2f} KB")
        if tamanho < 5: # Se for menor que 1KB, é erro de upload ou Git LFS
            st.error("🚨 O ARQUIVO ESTÁ VAZIO OU É APENAS UM PONTEIRO GIT LFS!")
    else:
        st.error("🚨 O arquivo 'modelo_obesidade.pkl' NÃO está dentro da pasta 'models'.")
else:
    st.error("🚨 A pasta 'models' NÃO foi encontrada.")
st.write("-----------------------------------")
# -------------------------------------
