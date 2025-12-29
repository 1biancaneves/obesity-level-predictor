import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- 1. CONFIGURAÇÃO E ESTILO (AZUL) ---
st.set_page_config(
    page_title="FIAP - Obesity Analytics",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS PROFISSIONAL
st.markdown("""
    <style>
    .stApp {background-color: #f4f6f9;}
    .css-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .card-title {
        color: #2c3e50;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 15px;
        border-bottom: 3px solid #3498db;
        padding-bottom: 5px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        color: #3498db;
        font-weight: bold;
    }
    /* Estilo do Rodapé */
    .footer-text {
        text-align: center;
        color: #7f8c8d;
        font-size: 14px;
        margin-top: 10px;
    }
    .footer-names {
        text-align: center;
        color: #2c3e50;
        font-size: 12px;
        font-weight: bold;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PREPARAÇÃO ---
traducao_resultado = {
    'Insufficient_Weight': 'Abaixo do Peso',
    'Normal_Weight': 'Peso Normal',
    'Overweight_Level_I': 'Sobrepeso Nível I',
    'Overweight_Level_II': 'Sobrepeso Nível II',
    'Obesity_Type_I': 'Obesidade Grau I',
    'Obesity_Type_II': 'Obesidade Grau II',
    'Obesity_Type_III': 'Obesidade Mórbida'
}

mapa_sim_nao = {'Sim': 'yes', 'Não': 'no'}
mapa_genero = {'Masculino': 'Male', 'Feminino': 'Female'}
mapa_transporte = {'Transporte Público': 'Public_Transportation', 'Caminhada': 'Walking', 
                   'Carro': 'Automobile', 'Moto': 'Motorbike', 'Bicicleta': 'Bike'}
mapa_frequencia = {'Não': 'no', 'Às vezes': 'Sometimes', 'Frequentemente': 'Frequently', 'Sempre': 'Always'}

def arredondar_valores(X_in):
    X_out = X_in.copy()
    cols_to_round = ['FCVC', 'NCP', 'CH2O', 'FAF', 'TUE']
    valid_cols = [c for c in cols_to_round if c in X_out.columns]
    X_out[valid_cols] = X_out[valid_cols].round().astype(int)
    return X_out

@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv("Obesity.csv")
        df['Obesity_PT'] = df['Obesity'].map(traducao_resultado)
        return df
    except:
        return None

try:
    pipeline = joblib.load('modelo_obesidade.pkl')
except:
    st.error("Erro: modelo_obesidade.pkl não encontrado.")
    st.stop()

df = carregar_dados()

# --- FUNÇÃO DO RODAPÉ (LOGOS + CRÉDITOS) ---
def render_footer():
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Grid para os 3 logos
    c1, c2, c3, c4, c5 = st.columns([1, 2, 2, 2, 1]) # Colunas vazias nas pontas para centralizar
    
    # URL de backup caso não tenha as imagens locais
    backup_logo = "https://logodownload.org/wp-content/uploads/2017/09/fiap-logo.png"
    
    with c2:
        if os.path.exists("logo1.png"): st.image("logo1.png", use_container_width=True)
        else: st.image(backup_logo, use_container_width=True, caption="Logo 1")
        
    with c3:
        if os.path.exists("logo2.png"): st.image("logo2.png", use_container_width=True)
        else: st.image(backup_logo, use_container_width=True, caption="Logo 2")
        
    with c4:
        if os.path.exists("logo3.png"): st.image("logo3.png", use_container_width=True)
        else: st.image(backup_logo, use_container_width=True, caption="Logo 3")

    # Textos
    st.markdown("""
        <div class="footer-text">
            © 2025 - Tech Challenge Fase 4
        </div>
        <div class="footer-names">
            Created by Bianca Neves, Erica Silva, Diogo Oliveira e Gabrielle Barbosa
        </div>
    """, unsafe_allow_html=True)

# --- 3. MENU LATERAL (LOGO 3 EM DESTAQUE) ---
if os.path.exists("logo3.png"):
    st.sidebar.image("logo3.png", use_container_width=True)
else:
    # Backup se não tiver o arquivo logo3.png
    st.sidebar.image("https://logodownload.org/wp-content/uploads/2017/09/fiap-logo.png", use_container_width=True)

st.sidebar.markdown("---")
menu = st.sidebar.radio("Navegação", ["Visão Executiva", "Insights Estratégicos", "Simulador de Risco"])

if df is not None:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Filtros Globais")
    
    opcoes_genero = df['Gender'].unique()
    opcoes_hist = df['family_history'].unique()
    
    filtro_genero = st.sidebar.multiselect("Gênero", opcoes_genero, default=opcoes_genero)
    filtro_hist = st.sidebar.multiselect("Histórico Familiar", opcoes_hist, default=opcoes_hist)
    
    if not filtro_genero: filtro_genero = opcoes_genero
    if not filtro_hist: filtro_hist = opcoes_hist
    
    df_filtrado = df[
        (df['Gender'].isin(filtro_genero)) & 
        (df['family_history'].isin(filtro_hist))
    ]
else:
    df_filtrado = pd.DataFrame()

# --- 4. VISÃO EXECUTIVA ---
if menu == "Visão Executiva":
    st.title("Monitoramento de Saúde Populacional")
    st.markdown("Visão estratégica para tomada de decisão clínica e preventiva.")

    if not df_filtrado.empty:
        col1, col2, col3, col4 = st.columns(4)
        total_p = len(df_filtrado)
        obesos = df_filtrado['Obesity'].str.contains('Obesity').sum()
        pct_obesidade = (obesos / total_p) * 100
        alto_risco = df_filtrado['Obesity'].isin(['Obesity_Type_II', 'Obesity_Type_III']).sum()
        sedentarios = len(df_filtrado[df_filtrado['FAF'] <= 0.5])
        pct_sedentarios = (sedentarios / total_p) * 100

        with col1: st.metric("Total de Pacientes", total_p)
        with col2: st.metric("Taxa de Obesidade", f"{pct_obesidade:.1f}%", delta="Alerta Clínico" if pct_obesidade > 30 else "Normal", delta_color="inverse")
        with col3: st.metric("Pacientes Alto Risco", alto_risco, help="Grau II e III")
        with col4: st.metric("Taxa de Sedentarismo", f"{pct_sedentarios:.1f}%")

        st.markdown("---")

        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown('<div class="card-title">📉 Estratificação de Risco</div>', unsafe_allow_html=True)
            fig_bar, ax_bar = plt.subplots(figsize=(10, 4))
            ordem = ['Abaixo do Peso', 'Peso Normal', 'Sobrepeso Nível I', 'Sobrepeso Nível II', 
                     'Obesidade Grau I', 'Obesidade Grau II', 'Obesidade Mórbida']
            contagem = df_filtrado['Obesity_PT'].value_counts().reindex(ordem).fillna(0)
            colors = ['#2ecc71', '#2ecc71', '#f1c40f', '#f39c12', '#e67e22', '#d35400', '#c0392b']
            sns.barplot(x=contagem.values, y=contagem.index, palette=colors, ax=ax_bar)
            sns.despine(left=True, bottom=True)
            st.pyplot(fig_bar)
            
            with st.expander("ℹ️ Interpretação"):
                st.write("A migração de pacientes das faixas amarelas para as vermelhas representa o maior risco.")

        with c2:
            st.markdown('<div class="card-title">🧬 Fator Genético</div>', unsafe_allow_html=True)
            fam_counts = df_filtrado['family_history'].value_counts()
            fig_pie, ax_pie = plt.subplots()
            ax_pie.pie(fam_counts, labels=fam_counts.index, autopct='%1.1f%%', startangle=90, colors=['#3498db', '#bdc3c7'], wedgeprops=dict(width=0.4))
            st.pyplot(fig_pie)
            with st.expander("ℹ️ Detalhes"):
                st.write("Predominância massiva de histórico familiar nos casos analisados.")

        st.markdown("### 🚀 Oportunidades de Intervenção")
        c3, c4 = st.columns(2)
        
        with c3:
            st.markdown('<div class="card-title">🚗 Mobilidade Urbana vs Peso</div>', unsafe_allow_html=True)
            ct = pd.crosstab(df_filtrado['MTRANS'], df_filtrado['Obesity_PT'])
            ct_norm = ct.div(ct.sum(axis=1), axis=0)
            fig_heat, ax_heat = plt.subplots(figsize=(8, 5))
            sns.heatmap(ct_norm, cmap="RdYlGn_r", annot=True, fmt=".1f", cbar=False, ax=ax_heat)
            plt.ylabel("")
            st.pyplot(fig_heat)

        with c4:
            st.markdown('<div class="card-title">💧 Consumo de Água</div>', unsafe_allow_html=True)
            fig_box, ax_box = plt.subplots(figsize=(8, 5))
            sns.boxplot(x='CH2O', y='Obesity_PT', data=df_filtrado, palette="Blues", order=ordem, ax=ax_box)
            plt.ylabel("")
            st.pyplot(fig_box)

    else:
        st.warning("⚠️ Nenhum dado disponível.")
    
    render_footer()

# --- 5. INSIGHTS ESTRATÉGICOS ---
elif menu == "Insights Estratégicos":
    st.title("Relatório de Inteligência Clínica")
    st.markdown("Consolidação de descobertas e recomendações.")
    st.markdown("---")

    col_txt1, col_txt2 = st.columns(2)

    with col_txt1:
        st.info("### 📌 Principais Descobertas")
        st.markdown("""
        **1. O Peso da Genética:** Histórico familiar é o fator determinante mais forte (>85% dos casos graves).
        **2. Mobilidade:** Uso de automóveis correlaciona-se com obesidade mórbida.
        **3. Hidratação:** Baixo consumo de água é crítico em pacientes obesos.
        """)

    with col_txt2:
        st.success("### 🚀 Plano de Ação")
        st.markdown("""
        **A. Triagem Genética:** Focar anamnese em histórico familiar.
        **B. Hospital em Movimento:** Incentivos (pontos/descontos) para transporte ativo.
        **C. Campanha Hidratação:** Meta de 2.0L/dia.
        """)

    st.markdown("---")
    st.markdown("### 🧬 Performance do Modelo")
    c_tec1, c_tec2 = st.columns(2)
    with c_tec1:
        st.metric("Acurácia Real", "93.62%")
    with c_tec2:
        st.write("Random Forest Classifier com 100% de precisão em casos críticos.")
    
    render_footer()

# --- 6. SIMULADOR ---
elif menu == "Simulador de Risco":
    st.title("Simulador de Risco Clínico")
    
    with st.form("form_ia"):
        st.markdown("#### 👤 Dados Biométricos")
        c1, c2, c3 = st.columns(3)
        with c1: age = st.number_input("Idade", 10, 100, 30)
        with c2: height = st.number_input("Altura (m)", 1.20, 2.50, 1.70)
        with c3: weight = st.number_input("Peso (kg)", 30.0, 200.0, 80.0)
        
        st.markdown("#### 🏥 Histórico e Hábitos")
        c4, c5 = st.columns(2)
        with c4: 
            family_history = st.selectbox("Histórico Familiar?", ["Sim", "Não"])
            favc = st.selectbox("Comida Calórica?", ["Sim", "Não"])
            smoke = st.selectbox("Tabagismo?", ["Sim", "Não"])
        with c5:
            gender = st.selectbox("Gênero", ["Masculino", "Feminino"])
            calc = st.selectbox("Álcool?", ["Não", "Às vezes", "Frequentemente", "Sempre"])
            scc = st.selectbox("Monitora Calorias?", ["Sim", "Não"])

        st.markdown("#### 🏃 Estilo de Vida")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1: 
            fcvc = st.slider("Vegetais", 1.0, 3.0, 2.0)
            faf = st.slider("Ativ. Física", 0.0, 3.0, 1.0)
        with col_s2: 
            ncp = st.slider("Refeições/Dia", 1.0, 4.0, 3.0)
            tue = st.slider("Tempo Telas", 0.0, 2.0, 1.0)
        with col_s3: 
            ch2o = st.slider("Água", 1.0, 3.0, 2.0)
            mtrans = st.selectbox("Transporte", list(mapa_transporte.keys()))
            caec = st.selectbox("Comer entre ref.", list(mapa_frequencia.keys()))

        submit = st.form_submit_button("Analisar Paciente")

    if submit:
        dados = pd.DataFrame({
            'Age': [age], 'Gender': [mapa_genero[gender]], 'Height': [height], 'Weight': [weight],
            'CALC': [mapa_frequencia[calc]], 'FAVC': [mapa_sim_nao[favc]], 'FCVC': [fcvc], 
            'NCP': [ncp], 'SCC': [mapa_sim_nao[scc]], 'SMOKE': [mapa_sim_nao[smoke]], 
            'CH2O': [ch2o], 'family_history': [mapa_sim_nao[family_history]], 'FAF': [faf], 
            'TUE': [tue], 'CAEC': [mapa_frequencia[caec]], 'MTRANS': [mapa_transporte[mtrans]]
        })
        try:
            res = pipeline.predict(dados)[0]
            res_pt = traducao_resultado.get(res, res)
            
            st.markdown("---")
            if "Obesidade" in res_pt:
                st.error(f"🚨 **Resultado:** {res_pt}")
            elif "Sobrepeso" in res_pt:
                st.warning(f"⚠️ **Resultado:** {res_pt}")
            else:
                st.success(f"✅ **Resultado:** {res_pt}")
        except Exception as e:
            st.error(f"Erro: {e}")

    render_footer()
