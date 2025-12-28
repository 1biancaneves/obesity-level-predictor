import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- 1. CONFIGURAÇÃO VISUAL (TEMA E LAYOUT) ---
st.set_page_config(
    page_title="Health Analytics",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS para deixar mais bonito (remove margens excessivas)
st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    h1 {color: #2c3e50;}
    h2 {color: #34495e;}
    .stMetric {background-color: white; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DICIONÁRIOS DE TRADUÇÃO (IMPORTANTE!) ---
# Traduz o que o modelo cospe (Inglês) para o que o médico lê (Português)
traducao_resultado = {
    'Insufficient_Weight': 'Abaixo do Peso',
    'Normal_Weight': 'Peso Normal',
    'Overweight_Level_I': 'Sobrepeso Nível I',
    'Overweight_Level_II': 'Sobrepeso Nível II',
    'Obesity_Type_I': 'Obesidade Grau I',
    'Obesity_Type_II': 'Obesidade Grau II',
    'Obesity_Type_III': 'Obesidade Mórbida (Grau III)'
}

# Traduz o que o usuário seleciona na tela para o que o modelo entende
mapa_sim_nao = {'Sim': 'yes', 'Não': 'no'}
mapa_genero = {'Masculino': 'Male', 'Feminino': 'Female'}
mapa_transporte = {
    'Transporte Público': 'Public_Transportation',
    'Caminhada': 'Walking',
    'Carro': 'Automobile',
    'Moto': 'Motorbike',
    'Bicicleta': 'Bike'
}
mapa_frequencia = {
    'Não': 'no',
    'Às vezes': 'Sometimes',
    'Frequentemente': 'Frequently',
    'Sempre': 'Always'
}

# --- 3. FUNÇÕES AUXILIARES ---
def arredondar_valores(X_in):
    # (Mesma função do treino, obrigatória para o joblib funcionar)
    X_out = X_in.copy()
    cols_to_round = ['FCVC', 'NCP', 'CH2O', 'FAF', 'TUE']
    valid_cols = [c for c in cols_to_round if c in X_out.columns]
    X_out[valid_cols] = X_out[valid_cols].round().astype(int)
    return X_out

@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv("Obesity.csv")
        # Traduzir a coluna alvo para os gráficos ficarem em PT-BR
        df['Obesity_PT'] = df['Obesity'].map(traducao_resultado)
        return df
    except:
        return None

# Carregar modelo
try:
    pipeline = joblib.load('modelo_obesidade.pkl')
except FileNotFoundError:
    st.error("🚨 Erro Crítico: O arquivo 'modelo_obesidade.pkl' não foi encontrado.")
    st.stop()

df = carregar_dados()

# --- 4. BARRA LATERAL ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3050/3050523.png", width=80)
st.sidebar.markdown("## Health Analytics v1.0")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navegação", ["📊 Painel Médico (Dashboard)", "🔍 Diagnóstico (IA)"])
st.sidebar.markdown("---")
st.sidebar.info("Desenvolvido para o Tech Challenge - Fase 4")

# --- 5. TELA 1: DASHBOARD MÉDICO ---
if menu == "📊 Painel Médico (Dashboard)":
    st.title("Painel de Inteligência Clínica 🏥")
    st.markdown("Análise epidemiológica da base de dados de obesidade.")

    if df is not None:
        # Métricas de Cabeçalho (KPIs)
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Total de Pacientes", len(df))
        kpi1.markdown("---") # Espaçamento visual
        kpi2.metric("Média de Idade", f"{df['Age'].mean():.1f} anos")
        kpi2.markdown("---")
        kpi3.metric("Peso Médio", f"{df['Weight'].mean():.1f} kg")
        kpi3.markdown("---")
        pct_obesos = (df['Obesity'].str.contains('Obesity').sum() / len(df)) * 100
        kpi4.metric("Taxa de Obesidade", f"{pct_obesos:.1f}%")
        kpi4.markdown("---")

        st.markdown("### 1. Fatores de Risco & Comportamento")
        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            st.markdown("**Distribuição de Idade por Condição**")
            fig1, ax1 = plt.subplots(figsize=(8, 6))
            sns.boxplot(x='Age', y='Obesity_PT', data=df, palette="coolwarm", ax=ax1, 
                        order=['Abaixo do Peso', 'Peso Normal', 'Sobrepeso Nível I', 'Sobrepeso Nível II', 'Obesidade Grau I', 'Obesidade Grau II', 'Obesidade Mórbida (Grau III)'])
            plt.xlabel("Idade (anos)")
            plt.ylabel("")
            st.pyplot(fig1)
            with st.expander("💡 Insight Médico"):
                st.write("Observe a mediana de idade. Se a caixa (box) estiver mais à direita nos níveis de obesidade, indica que a condição piora com o envelhecimento.")

        with col_graf2:
            st.markdown("**Impacto da Atividade Física (FAF)**")
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            # Vamos agrupar por nível de obesidade e pegar média de FAF
            mean_faf = df.groupby('Obesity_PT')['FAF'].mean().sort_values()
            sns.barplot(x=mean_faf.values, y=mean_faf.index, palette="viridis", ax=ax2)
            plt.xlabel("Frequência de Ativ. Física (0=Sedentário, 3=Alto)")
            plt.ylabel("")
            st.pyplot(fig2)
            with st.expander("💡 Insight Médico"):
                st.write("Correlação direta: Níveis mais graves de obesidade tendem a ter índices menores de atividade física (barras menores).")

        st.markdown("---")
        st.markdown("### 2. Análise de Hábitos Alimentares")
        
        col_graf3, col_graf4 = st.columns([2, 1])
        
        with col_graf3:
             st.markdown("**Matriz de Risco: Histórico Familiar vs Obesidade**")
             # Crosstab para ver números absolutos
             cross = pd.crosstab(df['Obesity_PT'], df['family_history'])
             fig3, ax3 = plt.subplots(figsize=(10, 5))
             sns.heatmap(cross, annot=True, fmt='d', cmap="Reds", ax=ax3)
             st.pyplot(fig3)
             with st.expander("💡 Insight Médico"):
                st.write("O mapa de calor revela a predisposição genética. Áreas vermelho-escuras mostram forte concentração de casos onde há histórico familiar positivo.")
        
        with col_graf4:
            st.markdown("**Consumo Calórico (FAVC)**")
            fig4, ax4 = plt.subplots()
            df['FAVC_PT'] = df['FAVC'].map({'yes': 'Sim', 'no': 'Não'})
            df['FAVC_PT'].value_counts().plot.pie(autopct='%1.1f%%', colors=['#ff9999','#66b3ff'], ax=ax4)
            plt.ylabel("")
            st.pyplot(fig4)

    else:
        st.warning("⚠️ Arquivo 'Obesity.csv' não detectado. Faça o upload para visualizar o Dashboard.")

# --- 6. TELA 2: PREDIÇÃO ---
elif menu == "🔍 Diagnóstico (IA)":
    st.title("Sistema de Apoio à Decisão Clínica 🩺")
    st.write("Preencha a anamnese do paciente para obter o prognóstico sugerido pela IA.")

    with st.form("form_medico"):
        st.subheader("1. Dados Biométricos")
        c1, c2, c3, c4 = st.columns(4)
        with c1: age = st.number_input("Idade", 10, 100, 30)
        with c2: height = st.number_input("Altura (m)", 1.20, 2.50, 1.70)
        with c3: weight = st.number_input("Peso (kg)", 30.0, 200.0, 80.0)
        with c4: gender = st.selectbox("Gênero", ["Masculino", "Feminino"])

        st.subheader("2. Histórico e Hábitos")
        c5, c6, c7 = st.columns(3)
        with c5: 
            family_history = st.selectbox("Histórico Familiar de Obesidade?", ["Sim", "Não"])
            favc = st.selectbox("Consome alimentos calóricos frequente?", ["Sim", "Não"])
        with c6:
            smoke = st.selectbox("Tabagismo?", ["Sim", "Não"])
            scc = st.selectbox("Monitora Calorias?", ["Sim", "Não"])
        with c7:
            caec = st.selectbox("Come entre refeições?", ["Não", "Às vezes", "Frequentemente", "Sempre"])
            calc = st.selectbox("Consome Álcool?", ["Não", "Às vezes", "Frequentemente", "Sempre"])

        st.subheader("3. Estilo de Vida (Escala 1 a 3)")
        st.info("ℹ️ Escala: 1 (Baixo/Nunca) a 3 (Alto/Sempre)")
        
        c8, c9, c10 = st.columns(3)
        with c8: 
            fcvc = st.slider("Consumo de Vegetais (FCVC)", 1.0, 3.0, 2.0)
            ncp = st.slider("Refeições principais/dia (NCP)", 1.0, 4.0, 3.0)
        with c9:
            ch2o = st.slider("Consumo de Água (CH2O)", 1.0, 3.0, 2.0)
            faf = st.slider("Atividade Física (FAF)", 0.0, 3.0, 1.0)
        with c10:
            tue = st.slider("Tempo em Telas (TUE)", 0.0, 2.0, 1.0)
            mtrans = st.selectbox("Transporte Principal", list(mapa_transporte.keys()))

        submit = st.form_submit_button("Gerar Diagnóstico")

    if submit:
        # CONVERSÃO DOS DADOS (PT-BR -> INGLÊS DO MODELO)
        dados_input = pd.DataFrame({
            'Age': [age],
            'Gender': [mapa_genero[gender]],
            'Height': [height],
            'Weight': [weight],
            'CALC': [mapa_frequencia[calc]],
            'FAVC': [mapa_sim_nao[favc]],
            'FCVC': [fcvc],
            'NCP': [ncp],
            'SCC': [mapa_sim_nao[scc]],
            'SMOKE': [mapa_sim_nao[smoke]],
            'CH2O': [ch2o],
            'family_history': [mapa_sim_nao[family_history]],
            'FAF': [faf],
            'TUE': [tue],
            'CAEC': [mapa_frequencia[caec]],
            'MTRANS': [mapa_transporte[mtrans]]
        })

        try:
            # Predição
            resultado_raw = pipeline.predict(dados_input)[0]
            
            # Tradução do Resultado
            resultado_pt = traducao_resultado.get(resultado_raw, resultado_raw)

            # Exibição do Resultado
            st.markdown("---")
            if "Obesidade" in resultado_pt:
                st.error(f"### 🚩 Diagnóstico Sugerido: {resultado_pt}")
                st.write("**Recomendação:** Encaminhar para nutricionista e avaliar comorbidades.")
            elif "Sobrepeso" in resultado_pt:
                st.warning(f"### ⚠️ Diagnóstico Sugerido: {resultado_pt}")
                st.write("**Recomendação:** Reeducação alimentar e aumento de atividade física.")
            else:
                st.success(f"### ✅ Diagnóstico Sugerido: {resultado_pt}")
                st.write("**Recomendação:** Manter hábitos saudáveis.")

        except Exception as e:
            st.error(f"Erro no processamento: {e}")
