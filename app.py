import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Obesity Analytics", layout="wide")

# --- FUNÇÃO DE ARREDONDAMENTO (NECESSÁRIA) ---
def arredondar_valores(X_in):
    X_out = X_in.copy()
    cols_to_round = ['FCVC', 'NCP', 'CH2O', 'FAF', 'TUE']
    valid_cols = [c for c in cols_to_round if c in X_out.columns]
    X_out[valid_cols] = X_out[valid_cols].round().astype(int)
    return X_out

# --- CARREGAR DADOS E MODELO ---
@st.cache_data
def carregar_dados():
    # Tenta carregar o CSV para o dashboard (se estiver no repo)
    try:
        return pd.read_csv("Obesity.csv")
    except:
        return None

try:
    pipeline = joblib.load('modelo_obesidade.pkl')
except FileNotFoundError:
    st.error("Erro: Modelo não encontrado.")
    st.stop()

df = carregar_dados()

# --- BARRA LATERAL (MENU) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3050/3050523.png", width=100)
st.sidebar.title("Tech Challenge - Fase 4")
st.sidebar.info("Este projeto prevê níveis de obesidade com base em hábitos de vida.")
aba = st.sidebar.radio("Navegação", ["📊 Dashboard Analítico", "🤖 Sistema Preditivo"])

# --- ABA 1: DASHBOARD (O QUE FALTAVA) ---
if aba == "📊 Dashboard Analítico":
    st.title("Painel de Insights Médicos 🏥")
    st.markdown("Visão geral da base de dados utilizada para o treinamento do modelo.")

    if df is not None:
        col1, col2 = st.columns(2)
        
        # Gráfico 1: Distribuição de Obesidade
        with col1:
            st.subheader("Distribuição dos Níveis de Obesidade")
            fig1, ax1 = plt.subplots()
            sns.countplot(y='Obesity', data=df, order=df['Obesity'].value_counts().index, palette="viridis", ax=ax1)
            st.pyplot(fig1)

        # Gráfico 2: IMC por Idade
        with col2:
            st.subheader("Relação Idade vs Peso")
            fig2, ax2 = plt.subplots()
            sns.scatterplot(x='Age', y='Weight', hue='Obesity', data=df, alpha=0.6, ax=ax2)
            st.pyplot(fig2)

        st.markdown("---")
        
        # Gráfico 3: Matriz de Hábitos
        st.subheader("Impacto do Histórico Familiar")
        fig3, ax3 = plt.subplots(figsize=(10, 4))
        sns.countplot(x='Obesity', hue='family_history', data=df, palette="Set2", ax=ax3)
        plt.xticks(rotation=45)
        st.pyplot(fig3)

    else:
        st.warning("⚠️ O arquivo 'Obesity.csv' não foi encontrado no repositório. Faça o upload dele para ver os gráficos.")

# --- ABA 2: PREDIÇÃO (O QUE VOCÊ JÁ TINHA) ---
elif aba == "🤖 Sistema Preditivo":
    st.title("Previsão em Tempo Real 🩺")
    
    with st.form("my_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input("Idade", 10, 100, 25)
            height = st.number_input("Altura (m)", 1.0, 2.5, 1.70)
            weight = st.number_input("Peso (kg)", 30.0, 200.0, 70.0)
            family_history = st.selectbox("Histórico Familiar?", ["yes", "no"])
        with col2:
            gender = st.selectbox("Gênero", ["Male", "Female"])
            favc = st.selectbox("Comida calórica frequente?", ["yes", "no"])
            smoke = st.selectbox("Fuma?", ["yes", "no"])
            calc = st.selectbox("Álcool?", ["no", "Sometimes", "Frequently", "Always"])
        with col3:
            scc = st.selectbox("Monitora calorias?", ["yes", "no"])
            mtrans = st.selectbox("Transporte", ["Public_Transportation", "Walking", "Automobile", "Motorbike", "Bike"])
            caec = st.selectbox("Comer entre ref.?", ["no", "Sometimes", "Frequently", "Always"])

        st.markdown("---")
        st.subheader("Hábitos (Escala 1 a 3)")
        c1, c2, c3 = st.columns(3)
        with c1: fcvc = st.slider("Vegetais (FCVC)", 1.0, 3.0, 2.0)
        with c2: ncp = st.slider("Refeições/dia (NCP)", 1.0, 4.0, 3.0)
        with c3: ch2o = st.slider("Água/dia (CH2O)", 1.0, 3.0, 2.0)
        
        c4, c5 = st.columns(2)
        with c4: faf = st.slider("Ativ. Física (FAF)", 0.0, 3.0, 1.0)
        with c5: tue = st.slider("Tempo Telas (TUE)", 0.0, 2.0, 1.0)

        submitted = st.form_submit_button("Calcular Diagnóstico")

    if submitted:
        dados = pd.DataFrame({
            'Age': [age], 'Gender': [gender], 'Height': [height], 'Weight': [weight],
            'CALC': [calc], 'FAVC': [favc], 'FCVC': [fcvc], 'NCP': [ncp],
            'SCC': [scc], 'SMOKE': [smoke], 'CH2O': [ch2o], 'family_history': [family_history],
            'FAF': [faf], 'TUE': [tue], 'CAEC': [caec], 'MTRANS': [mtrans]
        })
        
        predicao = pipeline.predict(dados)[0]
        
        # Cores para o resultado
        cor = "success"
        if "Obesity" in predicao: cor = "error"
        elif "Overweight" in predicao: cor = "warning"
        
        st.metric("Resultado da Análise:", predicao)
        if cor == "error": st.error(f"Paciente diagnosticado com: {predicao}")
        elif cor == "warning": st.warning(f"Atenção: {predicao}")
        else: st.success(f"Diagnóstico: {predicao}")
