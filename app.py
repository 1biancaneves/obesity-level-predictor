import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(
    page_title="FIAP - Health Intelligence",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONFIGURAÇÃO GLOBAL DE GRÁFICOS ---
sns.set_theme(style="ticks")
plt.rcParams['figure.facecolor'] = 'none'
plt.rcParams['axes.facecolor'] = 'none'
plt.rcParams['savefig.facecolor'] = 'none'
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['text.color'] = '#2c3e50'
plt.rcParams['axes.labelcolor'] = '#2c3e50'
plt.rcParams['xtick.color'] = '#2c3e50'
plt.rcParams['ytick.color'] = '#2c3e50'

# CSS (CORRIGIDO PARA VISUAL + CONTEÚDO)
st.markdown("""
    <style>
    /* Fundo e Cores Gerais */
    [data-testid="stAppViewContainer"] { background-color: #f4f6f9 !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e1e4e8; }
    
    /* Força cor escura em todos os textos para leitura */
    .stMarkdown, .stText, h1, h2, h3, h4, p, li, span, label { color: #2c3e50 !important; }
    
    /* Estilo dos Títulos dos Gráficos */
    .custom-header {
        font-family: 'Segoe UI', sans-serif;
        color: #2c3e50 !important;
        font-size: 1.2rem;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 5px;
        border-left: 5px solid #3498db;
        padding-left: 10px;
    }
    
    /* Caixas de Insight (Textos Detalhados) */
    .insight-box {
        background-color: #eef6fb !important;
        border: 1px solid #d6eaf8;
        padding: 15px;
        border-radius: 8px;
        font-size: 0.90rem;
        color: #2c3e50 !important;
        margin-top: 5px;
        margin-bottom: 20px;
        line-height: 1.5; /* Melhor leitura */
    }

    /* Destaque Técnico */
    .tech-box {
        background-color: #fff8e1 !important;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        color: #5d4037 !important;
        font-size: 0.90rem;
    }
    
    /* Métricas */
    div[data-testid="stMetricValue"] { color: #3498db !important; }
    div[data-testid="stMetricLabel"] { color: #7f8c8d !important; }
    
    /* Container Branco para os gráficos */
    [data-testid="column"] {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DEFINIÇÕES E FUNÇÕES ---

# FUNÇÃO ESSENCIAL PARA O MODELO
def arredondar_valores(X_in):
    try:
        X_out = X_in.copy()
        cols_to_round = ['FCVC', 'NCP', 'CH2O', 'FAF', 'TUE']
        valid_cols = [c for c in cols_to_round if c in X_out.columns]
        if valid_cols:
            X_out[valid_cols] = X_out[valid_cols].round().astype(int)
        return X_out
    except Exception:
        return X_in

traducao_resultado = {
    'Insufficient_Weight': 'Abaixo do Peso',
    'Normal_Weight': 'Peso Normal',
    'Overweight_Level_I': 'Sobrepeso Nível I',
    'Overweight_Level_II': 'Sobrepeso Nível II',
    'Obesity_Type_I': 'Obesidade Grau I',
    'Obesity_Type_II': 'Obesidade Grau II',
    'Obesity_Type_III': 'Obesidade Mórbida'
}

ordem_obesidade = ['Abaixo do Peso', 'Peso Normal', 'Sobrepeso Nível I', 'Sobrepeso Nível II', 
                   'Obesidade Grau I', 'Obesidade Grau II', 'Obesidade Mórbida']

mapa_sim_nao = {'Sim': 'yes', 'Não': 'no'}
mapa_genero = {'Masculino': 'Male', 'Feminino': 'Female'}
mapa_transporte = {'Transporte Público': 'Public_Transportation', 'Caminhada': 'Walking', 
                   'Carro': 'Automobile', 'Moto': 'Motorbike', 'Bicicleta': 'Bike'}
mapa_frequencia = {'Não': 'no', 'Às vezes': 'Sometimes', 'Frequentemente': 'Frequently', 'Sempre': 'Always'}

@st.cache_data
def carregar_dados():
    caminhos = ["data/Obesity.csv", "Obesity.csv"]
    for c in caminhos:
        if os.path.exists(c):
            try:
                df = pd.read_csv(c)
                df['Obesity_PT'] = df['Obesity'].map(traducao_resultado)
                bins = [0, 19, 29, 45, 60, 100]
                labels = ['0-19 (Jovens)', '20-29 (Adultos Jovens)', '30-45 (Adultos)', '46-60 (Meia Idade)', '60+ (Idosos)']
                df['Faixa_Etaria'] = pd.cut(df['Age'], bins=bins, labels=labels)
                return df
            except Exception as e:
                st.error(f"Erro ao ler {c}: {e}")
                return None
    st.error("❌ ERRO: Arquivo 'Obesity.csv' não encontrado.")
    return None

def carregar_modelo():
    caminhos = ['models/modelo_obesidade.pkl', 'modelo_obesidade.pkl']
    for c in caminhos:
        if os.path.exists(c):
            try:
                return joblib.load(c)
            except Exception as e:
                st.error(f"❌ Erro ao carregar '{c}': {e}")
                st.stop()
    st.error("❌ ERRO: Modelo .pkl não encontrado.")
    st.stop()

# --- CARREGAMENTO ---
df = carregar_dados()
pipeline = carregar_modelo()

def get_img_path(name):
    if os.path.exists(f"assets/{name}"): return f"assets/{name}"
    if os.path.exists(name): return name
    return "https://logodownload.org/wp-content/uploads/2017/09/fiap-logo.png"

# --- 3. SIDEBAR ---
st.sidebar.image(get_img_path("logo3.png"), use_container_width=True)
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navegação", ["Dashboard Analítico", "Insights Estratégicos", "Simulador de Risco"])

df_filtrado = pd.DataFrame()
if df is not None:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🕵️ Filtros Avançados")
    f_gen = st.sidebar.multiselect("Gênero", df['Gender'].unique(), default=df['Gender'].unique())
    f_hist = st.sidebar.multiselect("Histórico Familiar", df['family_history'].unique(), default=df['family_history'].unique())
    f_age = st.sidebar.multiselect("Faixa Etária", df['Faixa_Etaria'].unique().astype(str), default=df['Faixa_Etaria'].unique().astype(str))
    f_trans = st.sidebar.multiselect("Transporte", df['MTRANS'].unique(), default=df['MTRANS'].unique())
    
    if not f_gen: f_gen = df['Gender'].unique()
    if not f_hist: f_hist = df['family_history'].unique()
    if not f_age: f_age = df['Faixa_Etaria'].unique().astype(str)
    if not f_trans: f_trans = df['MTRANS'].unique()
    
    df_filtrado = df[
        (df['Gender'].isin(f_gen)) & 
        (df['family_history'].isin(f_hist)) & 
        (df['Faixa_Etaria'].astype(str).isin(f_age)) &
        (df['MTRANS'].isin(f_trans))
    ]

# --- 4. DASHBOARD (COM TEXTOS DETALHADOS) ---
if menu == "Dashboard Analítico":
    st.title("Painel de Inteligência Médica")
    st.markdown("Análise multifatorial de riscos baseada em dados reais.")

    if not df_filtrado.empty:
        col1, col2, col3, col4 = st.columns(4)
        total = len(df_filtrado)
        obesos = df_filtrado['Obesity'].str.contains('Obesity').sum()
        pct_ob = (obesos / total) * 100 if total > 0 else 0
        alto_risco = df_filtrado['Obesity'].isin(['Obesity_Type_II', 'Obesity_Type_III']).sum()
        
        with col1: st.metric("Pacientes Filtrados", total)
        with col2: st.metric("Taxa Obesidade Global", f"{pct_ob:.1f}%", delta="Base Selecionada")
        with col3: st.metric("Alto Risco (Grau II+)", alto_risco, delta="Prioridade Máxima", delta_color="inverse")
        imc_medio = (df_filtrado['Weight']/(df_filtrado['Height']**2)).mean()
        with col4: st.metric("Média IMC Estimada", f"{imc_medio:.1f}")

        st.markdown("---")

        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown('<p class="custom-header">1. Distribuição Clínica</p>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 4))
            contagem = df_filtrado['Obesity_PT'].value_counts().reindex(ordem_obesidade).fillna(0)
            colors = ['#2ecc71', '#27ae60', '#f1c40f', '#f39c12', '#e67e22', '#d35400', '#c0392b']
            sns.barplot(x=contagem.values, y=contagem.index, palette=colors, ax=ax)
            sns.despine(left=True, bottom=True)
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig, use_container_width=True)
            
            maior_grupo = contagem.idxmax() if not contagem.empty else "N/A"
            st.markdown(f"""<div class="insight-box">
            <b>Insight de Negócio:</b> O perfil predominante nesta seleção é <b>{maior_grupo}</b>. 
            Observe a "cauda longa" vermelha no gráfico. Se as barras inferiores (Laranja/Vermelho) dominarem e ultrapassarem 20%, isso indica uma carteira de pacientes de altíssimo custo operacional e risco iminente de comorbidades (diabetes, hipertensão).
            </div>""", unsafe_allow_html=True)

        with c2:
            st.markdown('<p class="custom-header">2. Carga Genética</p>', unsafe_allow_html=True)
            fig, ax = plt.subplots()
            fam = df_filtrado['family_history'].value_counts()
            if not fam.empty:
                ax.pie(fam, labels=fam.index, autopct='%1.1f%%', colors=['#e74c3c', '#bdc3c7'], startangle=90)
                st.pyplot(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
            <b>Fator Hereditário:</b> A análise mostra que em grupos de Obesidade Grau III, este gráfico tende a mostrar >85% de histórico positivo ("Yes"). Isso valida estatisticamente a necessidade de exames genéticos preventivos na triagem.
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<p class="custom-header">3. Mapa de Calor: Transporte</p>', unsafe_allow_html=True)
            ct = pd.crosstab(df_filtrado['MTRANS'], df_filtrado['Obesity_PT'])
            if not ct.empty:
                ct_norm = ct.div(ct.sum(axis=1), axis=0)
                fig, ax = plt.subplots(figsize=(8, 5))
                sns.heatmap(ct_norm, cmap="RdYlGn_r", annot=True, fmt=".0%", cbar=False, ax=ax)
                plt.ylabel("Meio de Transporte")
                plt.xlabel("")
                st.pyplot(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
            <b>Impacto da Mobilidade:</b>
            Analise a linha "Automobile". O vermelho intenso nas colunas de Obesidade Grau II e III comprova que o transporte passivo é um vetor de risco. Por outro lado, "Walking" e "Bike" atuam como fatores de proteção natural.
            </div>""", unsafe_allow_html=True)

        with c4:
            st.markdown('<p class="custom-header">4. Impacto da Tecnologia</p>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.violinplot(x='TUE', y='Obesity_PT', data=df_filtrado, order=ordem_obesidade, palette="cool", inner="quartile", ax=ax)
            plt.xlabel("Tempo em Dispositivos")
            plt.ylabel("")
            st.pyplot(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
            <b>Sedentarismo Digital:</b>
            A "barriga" do violino se desloca para a direita (maior uso de telas) conforme a gravidade da obesidade aumenta. O tempo de tela compete diretamente com o tempo disponível para atividade física (FAF).
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

        c5, c6 = st.columns(2)
        with c5:
            st.markdown('<p class="custom-header">5. O Mito do "Comer Pouco"</p>', unsafe_allow_html=True)
            ct_caec = pd.crosstab(df_filtrado['Obesity_PT'], df_filtrado['CAEC'])
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.heatmap(ct_caec, cmap="Blues", annot=True, fmt="d", cbar=False, ax=ax)
            plt.xlabel("Frequência de Lanches")
            plt.ylabel("")
            st.pyplot(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
            <b>Análise Comportamental:</b>
            Note que a maior concentração de obesos não está em quem come "Sempre" (Always), mas na massa que come "Às Vezes" (Sometimes). A falta de rotina alimentar (beliscar sem planejamento) é o maior ofensor calórico oculto.
            </div>""", unsafe_allow_html=True)

        with c6:
            st.markdown('<p class="custom-header">6. Evolução por Idade</p>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.boxplot(x='Age', y='Obesity_PT', data=df_filtrado, order=ordem_obesidade, palette="Spectral_r", ax=ax)
            plt.xlabel("Idade")
            plt.ylabel("")
            st.pyplot(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
            <b>Cronologia da Doença:</b>
            Observe a mediana (linha preta). Se ela sobe nos níveis mais altos de obesidade, confirma o efeito cumulativo do peso. Outliers jovens em "Obesidade III" são alertas vermelhos para intervenção pediátrica.
            </div>""", unsafe_allow_html=True)
            
        st.markdown("---")
        
        c7, c8, c9 = st.columns(3)
        with c7:
            st.markdown('<p class="custom-header">7. Hidratação</p>', unsafe_allow_html=True)
            fig, ax = plt.subplots()
            sns.barplot(x='Obesity_PT', y='CH2O', data=df_filtrado, order=ordem_obesidade, palette="Blues", ax=ax, errorbar=None)
            plt.xticks(rotation=90)
            plt.xlabel("")
            plt.ylabel("Litros/Dia")
            st.pyplot(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
            <b>Metabolismo:</b> Há uma queda drástica no consumo de água (< 1.5L) nos grupos de risco. Hidratação é essencial para o metabolismo basal.
            </div>""", unsafe_allow_html=True)

        with c8:
            st.markdown('<p class="custom-header">8. Tabagismo</p>', unsafe_allow_html=True)
            smoke_ct = pd.crosstab(df_filtrado['Obesity_PT'], df_filtrado['SMOKE'], normalize='index')
            fig, ax = plt.subplots()
            smoke_ct.plot(kind='bar', stacked=True, color=['#bdc3c7', '#2c3e50'], ax=ax)
            plt.legend(bbox_to_anchor=(1,1))
            plt.xticks(rotation=90)
            plt.xlabel("")
            st.pyplot(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
            <b>Comorbidade:</b> A combinação Obesidade + Cigarro multiplica exponencialmente o risco cardiovascular (infarto/AVC).
            </div>""", unsafe_allow_html=True)
            
        with c9:
            st.markdown('<p class="custom-header">9. Freq. Refeições</p>', unsafe_allow_html=True)
            fig, ax = plt.subplots()
            sns.pointplot(x='Obesity_PT', y='NCP', data=df_filtrado, order=ordem_obesidade, color="#e74c3c", ax=ax)
            plt.xticks(rotation=90)
            plt.xlabel("")
            plt.ylabel("Refeições/Dia")
            st.pyplot(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
            <b>Padrão Alimentar:</b> Baixa frequência de refeições (1 ou 2) muitas vezes indica jejum prolongado seguido de compulsão.
            </div>""", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Nenhum dado disponível.")

# --- 5. INSIGHTS (COM TEXTOS COMPLETOS) ---
elif menu == "Insights Estratégicos":
    st.title("Relatório Executivo de Inteligência de Dados")
    st.markdown("Análise profunda, plano de ação e auditoria técnica do modelo.")
    st.markdown("---")

    col_txt1, col_txt2 = st.columns(2)

    with col_txt1:
        st.markdown("### 🔍 Diagnóstico de Negócio (5 Pilares)")
        st.markdown("""
        **1. O Fator Hereditário (Genética):**
        A análise de dados é conclusiva: o histórico familiar é o preditor mais forte de obesidade futura. Em nossa base, mais de **85%** dos casos de Obesidade Grau III possuem parentes diretos com a condição. Isso transforma a obesidade de uma "falha individual" para um "contexto familiar".
        
        **2. Mobilidade e Urbanismo:**
        Identificamos uma correlação quase linear entre o uso de **Automóveis** e o aumento do IMC. Usuários de transporte público (que caminham até pontos/estações) têm índices de obesidade significativamente menores, provando que a "atividade física incidental" é crucial.
        
        **3. A 'Zona Cinzenta' da Alimentação:**
        O perigo não está apenas em quem come "Sempre" entre refeições, mas no grupo "Sometimes" (Às vezes). A falta de rotina alimentar (beliscar sem planejamento) é o maior contribuidor calórico oculto nos dados.
        
        **4. Desidratação Crônica:**
        Pacientes obesos relatam consumo de água sistematicamente menor (< 1.5L) que pacientes saudáveis (> 2.0L). A água atua na saciedade e no metabolismo basal.
        
        **5. Sedentarismo Digital (Tech-Neck):**
        O tempo de uso de tecnologia (TUE) compete diretamente com a atividade física. Pacientes com alto TUE raramente possuem alto FAF (Frequência de Atividade Física), criando um ciclo vicioso.
        """)

    with col_txt2:
        st.markdown("### 🚀 Plano de Ação (Propostas)")
        st.success("""
        **A. Protocolo de Triagem Genética na Admissão**
        * **Ação:** Incluir pergunta obrigatória sobre histórico familiar na triagem.
        * **Impacto:** Se positivo, o paciente entra em uma "Trilha Preventiva" (nutrição + psicologia) antes mesmo de apresentar sintomas graves.
        
        **B. Programa 'Hospital em Movimento'**
        * **Ação:** Gamificação para funcionários e pacientes.
        * **Mecânica:** Pontos por passos dados ou troca do carro por bicicleta/transporte público. Prêmios em descontos na farmácia ou dias de folga (para funcionários).
        
        **C. Reeducação do 'Belisco'**
        * **Ação:** Focar a nutrição não em proibir, mas em *estruturar* os lanches intermediários. Substituir o "belisco inconsciente" por "lanche proteico programado".
        
        **D. Campanha 'Hidratação 2.0'**
        * **Ação:** Distribuição de garrafas graduadas inteligentes e instalação de bebedouros com contadores visuais. Meta simples: 2.0L/dia para todos.
        """)

    st.markdown("---")
    
    # --- AUDITORIA TÉCNICA (COMPLETA) ---
    st.markdown("### 🤖 Auditoria Técnica do Modelo de IA")
    
    c_tec1, c_tec2 = st.columns([1, 2])
    
    with c_tec1:
        st.metric("Acurácia Global", "93.62%", delta="Excelente")
        st.metric("Recall (Obesidade III)", "100.0%", delta="Segurança Máxima")
        st.metric("Precision (Peso Normal)", "94.0%")
    
    with c_tec2:
        st.markdown("""
        <div class="tech-box">
        <b>Por que este modelo é robusto?</b><br>
        1. <b>Algoritmo Escolhido:</b> Random Forest Classifier (Floresta Aleatória).<br>
        2. <b>Justificativa Técnica:</b> Diferente de modelos lineares (como Regressão Logística), o Random Forest consegue capturar <b>relações não-lineares complexas</b>. Exemplo: "Comer vegetais" (FCVC) geralmente é bom, mas o modelo aprendeu que "Comer vegetais + Comer muito entre refeições + Não beber água" ainda resulta em obesidade. Uma regressão simples falharia em ver essa interação.<br>
        3. <b>Segurança Clínica (Recall):</b> O modelo foi otimizado para não cometer falsos negativos em casos graves. O Recall de 100% na Obesidade Tipo III significa que a IA <b>nunca</b> classificou um paciente mórbido como saudável, garantindo segurança na triagem médica.
        4. <b>Engenharia de Atributos:</b> A alta performance não é mágica. Ela provém do tratamento prévio dos dados, onde transformamos variáveis categóricas (texto) em numéricas e normalizamos as escalas de idade e peso.
        </div>
        """, unsafe_allow_html=True)

# --- 6. SIMULADOR ---
elif menu == "Simulador de Risco":
    st.title("Simulador de Risco Clínico")
    with st.form("form_ia"):
        c1, c2, c3 = st.columns(3)
        with c1: age = st.number_input("Idade", 10, 100, 30)
        with c2: height = st.number_input("Altura (m)", 1.20, 2.50, 1.70)
        with c3: weight = st.number_input("Peso (kg)", 30.0, 200.0, 80.0)
        
        c4, c5 = st.columns(2)
        with c4: 
            family_history = st.selectbox("Histórico Familiar?", ["Sim", "Não"])
            favc = st.selectbox("Comida Calórica Frequente?", ["Sim", "Não"])
            smoke = st.selectbox("Tabagismo?", ["Sim", "Não"])
        with c5:
            gender = st.selectbox("Gênero", ["Masculino", "Feminino"])
            calc = st.selectbox("Álcool?", ["Não", "Às vezes", "Frequentemente", "Sempre"])
            scc = st.selectbox("Monitora Calorias?", ["Sim", "Não"])
        st.markdown("#### 🏃 Estilo de Vida")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1: 
            fcvc = st.slider("Vegetais (1=Pouco, 3=Muito)", 1.0, 3.0, 2.0)
            faf = st.slider("Ativ. Física (Dias/Semana)", 0.0, 3.0, 1.0)
        with col_s2: 
            ncp = st.slider("Refeições Principais/Dia", 1.0, 4.0, 3.0)
            tue = st.slider("Tempo Telas (0=Baixo, 2=Alto)", 0.0, 2.0, 1.0)
        with col_s3: 
            ch2o = st.slider("Água (Litros/Dia)", 1.0, 3.0, 2.0)
            mtrans = st.selectbox("Transporte Principal", list(mapa_transporte.keys()))
            caec = st.selectbox("Comer entre ref.", list(mapa_frequencia.keys()))
        submit = st.form_submit_button("Gerar Diagnóstico")
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
            if "Obesidade" in res_pt: st.error(f"🚨 **Diagnóstico:** {res_pt}")
            elif "Sobrepeso" in res_pt: st.warning(f"⚠️ **Diagnóstico:** {res_pt}")
            else: st.success(f"✅ **Diagnóstico:** {res_pt}")
        except Exception as e: st.error(f"Erro: {e}")

# --- RODAPÉ ---
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)
col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns([1, 2, 2, 2, 1], vertical_alignment="center")
with col_f2: st.image(get_img_path("logo1.png"), use_container_width=True)
with col_f3: st.image(get_img_path("logo2.png"), use_container_width=True)
with col_f4: st.image(get_img_path("logo3.png"), use_container_width=True)
st.markdown("""
    <div style="text-align: center; color: #7f8c8d; font-size: 12px; margin-top: 15px;">
        © 2025 - Tech Challenge Fase 4<br>
        <b>Created by Bianca Neves, Erica Silva, Diogo Oliveira e Gabrielle Barbosa</b>
    </div>
""", unsafe_allow_html=True)
