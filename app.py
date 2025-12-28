import streamlit as st
import pandas as pd
import joblib

# --- IMPORTANTE: A FUNÇÃO PERSONALIZADA ---
# Precisa estar aqui para o joblib carregar o pipeline corretamente
def arredondar_valores(X_in):
    X_out = X_in.copy()
    cols_to_round = ['FCVC', 'NCP', 'CH2O', 'FAF', 'TUE']
    valid_cols = [c for c in cols_to_round if c in X_out.columns]
    X_out[valid_cols] = X_out[valid_cols].round().astype(int)
    return X_out

# --- CARREGAR O MODELO ---
# Certifique-se de que o arquivo .pkl está na mesma pasta
try:
    pipeline = joblib.load('modelo_obesidade.pkl')
except FileNotFoundError:
    st.error("Erro: O arquivo 'modelo_obesidade.pkl' não foi encontrado. Verifique se ele está no repositório.")
    st.stop()

# --- TÍTULO E DESCRIÇÃO ---
st.title("Previsão de Nível de Obesidade 🩺")
st.write("Preencha os dados abaixo para que o modelo de IA faça a análise.")

# --- FORMULÁRIO DE ENTRADA ---
with st.form("formulario_obesidade"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Idade", min_value=10, max_value=100, value=25)
        height = st.number_input("Altura (m)", min_value=1.0, max_value=2.5, value=1.70)
        weight = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=70.0)
        gender = st.selectbox("Gênero", ["Male", "Female"])
        family_history = st.selectbox("Histórico Familiar de Obesidade?", ["yes", "no"])
        
    with col2:
        favc = st.selectbox("Consome alimentos calóricos com frequência?", ["yes", "no"])
        fcvc = st.slider("Consumo de vegetais (FCVC)", 1.0, 3.0, 2.0)
        ncp = st.slider("Refeições principais por dia (NCP)", 1.0, 4.0, 3.0)
        caec = st.selectbox("Come entre refeições?", ["no", "Sometimes", "Frequently", "Always"])
        smoke = st.selectbox("Fuma?", ["yes", "no"])

    col3, col4 = st.columns(2)
    with col3:
        ch2o = st.slider("Água por dia (litros)", 1.0, 3.0, 2.0)
        scc = st.selectbox("Monitora calorias ingeridas?", ["yes", "no"])
    
    with col4:
        faf = st.slider("Atividade Física (frequência)", 0.0, 3.0, 1.0)
        tue = st.slider("Tempo em dispositivos (celular/TV)", 0.0, 2.0, 1.0)
        calc = st.selectbox("Consumo de Álcool", ["no", "Sometimes", "Frequently", "Always"])
        mtrans = st.selectbox("Meio de Transporte", ["Public_Transportation", "Walking", "Automobile", "Motorbike", "Bike"])

    submit_button = st.form_submit_button("Calcular Nível de Obesidade")

# --- LÓGICA DA PREVISÃO ---
if submit_button:
    # Criar DataFrame com os dados
    dados_entrada = pd.DataFrame({
        'Age': [age],
        'Gender': [gender],
        'Height': [height],
        'Weight': [weight],
        'CALC': [calc],
        'FAVC': [favc],
        'FCVC': [fcvc],
        'NCP': [ncp],
        'SCC': [scc],
        'SMOKE': [smoke],
        'CH2O': [ch2o],
        'family_history': [family_history],
        'FAF': [faf],
        'TUE': [tue],
        'CAEC': [caec],
        'MTRANS': [mtrans]
    })

    # Fazer a predição
    try:
        resultado = pipeline.predict(dados_entrada)[0]
        
        # Exibir resultado com estilo
        st.markdown("---")
        st.subheader(f"Resultado da Análise:")
        
        cor = "blue"
        if "Obesity" in resultado:
            cor = "red"
        elif "Overweight" in resultado:
            cor = "orange"
        else:
            cor = "green"
            
        st.markdown(f"<h2 style='color: {cor};'>{resultado}</h2>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erro ao realizar a predição: {e}")
