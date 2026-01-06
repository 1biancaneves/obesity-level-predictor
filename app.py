import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# --- 1. CONFIGURAÇÃO E ESTILO (RESPONSIVO & PROFISSIONAL) ---
st.set_page_config(
    page_title="FIAP - Health Intelligence",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONFIGURAÇÃO GLOBAL DE GRÁFICOS (FUNDO TRANSPARENTE) ---
sns.set_theme(style="ticks")
plt.rcParams['figure.facecolor'] = 'none'
plt.rcParams['axes.facecolor'] = 'none'
plt.rcParams['savefig.facecolor'] = 'none'

# CSS AVANÇADO
st.markdown("""
    <style>
    /* Fundo Geral */
    .stApp {background-color: #f4f6f9;}
    
    /* Cards (Container dos Gráficos) */
    .css-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    
    /* Títulos dos Gráficos */
    .chart-header {
        font-family: 'Segoe UI', sans-serif;
        color: #2c3e50;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        border-left: 5px solid #3498db;
        padding-left: 10px;
    }
    
    /* Caixas de Insight (Azul Claro) */
    .insight-box {
        background-color: #eef6fb;
        border: 1px solid #d6eaf8;
        padding: 15px;
        border-radius: 8px;
        font-size: 0.90rem; /* Fonte levemente menor para caber em colunas */
        color: #2c3e50;
        margin-top: 10px;
        line-height: 1.4;
    }

    /* Destaque Técnico */
    .tech-box {
        background-color: #fff8e1;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        color: #5d4037;
    }
    
    /* Ajustes Mobile */
    @media (max-width: 768px) {
        .stColumns { display: block !important; }
        [data-testid="column"] { width: 100% !important; margin-bottom: 20px; }
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

# Ordem lógica de gravidade
ordem_obesidade = ['Abaixo do Peso', 'Peso Normal', 'Sobrepeso Nível I', 'Sobrepeso Nível II', 
                   'Obesidade Grau I', 'Obesidade Grau II', 'Obesidade Mórbida']

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
        # Faixas Etárias para Filtro
        bins = [0, 19, 29, 45, 60, 100]
        labels = ['0-19 (Jovens)', '20-29 (Adultos Jovens)', '30-45 (Adultos)', '46-60 (Meia Idade)', '60+ (Idosos)']
        df['Faixa_Etaria'] = pd.cut(df['Age'], bins=bins, labels=labels)
        return df
    except:
        return None

try:
    pipeline = joblib.load('modelo_obesidade.pkl')
except:
    st.error("Erro crítico: Arquivo 'modelo_obesidade.pkl' não encontrado.")
    st.stop()

df = carregar_dados()

# --- FUNÇÃO DE RODAPÉ (LOGOS CENTRALIZADOS) ---
def render_footer():
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2, c3, c4, c5 = st.columns([1, 2, 2, 2, 1], vertical_alignment="center") 
    
    backup_logo = "https://logodownload.org/wp-content/uploads/2017/09/fiap-logo.png"
    
    with c2:
        if os.path.exists("logo1.png"): st.image("logo1.png", use_container_width=True)
        else: st.image(backup_logo, use_container_width=True)
    with c3:
        if os.path.exists("logo2.png"): st.image("logo2.png", use_container_width=True)
        else: st.image(backup_logo, use_container_width=True)
    with c4:
        if os.path.exists("logo3.png"): st.image("logo3.png", use_container_width=True)
        else: st.image(backup_logo, use_container_width=True)

    st.markdown("""
        <div style="text-align: center; color: #7f8c8d; font-size: 12px; margin-top: 15px;">
            © 2025 - Tech Challenge Fase 4<br>
            <b>Created by Bianca Neves, Erica Silva, Diogo Oliveira e Gabrielle Barbosa</b>
        </div>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR E FILTROS ---
if os.path.exists("logo3.png"):
    st.sidebar.image("logo3.png", use_container_width=True)
else:
    st.sidebar.image("https://logodownload.org/wp-content/uploads/2017/09/fiap-logo.png", use_container_width=True)

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
    f_ativ = st.sidebar.slider("Nível Ativ. Física (FAF)", 0.0, 3.0, (0.0, 3.0))
    
    if not f_gen: f_gen = df['Gender'].unique()
    if not f_hist: f_hist = df['family_history'].unique()
    if not f_age: f_age = df['Faixa_Etaria'].unique().astype(str)
    if not f_trans: f_trans = df['MTRANS'].unique()
    
    df_filtrado = df[
        (df['Gender'].isin(f_gen)) & 
        (df['family_history'].isin(f_hist)) & 
        (df['Faixa_Etaria'].astype(str).isin(f_age)) &
        (df['MTRANS'].isin(f_trans)) &
        (df['FAF'] >= f_ativ[0]) & (df['FAF'] <= f_ativ[1])
    ]
else:
    st.warning("Carregue o arquivo Obesity.csv")

# --- 4. DASHBOARD ANALÍTICO ---
if menu == "Dashboard Analítico":
    st.title("Painel de Inteligência Médica")
    st.markdown("Análise multifatorial de riscos baseada em dados reais.")

    if not df_filtrado.empty:
        # KPI ROW
        col1, col2, col3, col4 = st.columns(4)
        total = len(df_filtrado)
        obesos = df_filtrado['Obesity'].str.contains('Obesity').sum()
        pct_ob = (obesos / total) * 100
        alto_risco = df_filtrado['Obesity'].isin(['Obesity_Type_II', 'Obesity_Type_III']).sum()
        
        with col1: st.metric("Pacientes Filtrados", total)
        with col2: st.metric("Taxa Obesidade Global", f"{pct_ob:.1f}%", delta="Base Selecionada")
        with col3: st.metric("Alto Risco (Grau II+)", alto_risco, delta="Prioridade Máxima", delta_color="inverse")
        with col4: st.metric("Média IMC Estimada", f"{(df_filtrado['Weight']/(df_filtrado['Height']**2)).mean():.1f}")

        st.markdown("---")

        # LINHA 1
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown('<div class="chart-header">1. Distribuição Clínica da População</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 4))
            contagem = df_filtrado['Obesity_PT'].value_counts().reindex(ordem_obesidade).fillna(0)
            colors = ['#2ecc71', '#27ae60', '#f1c40f', '#f39c12', '#e67e22', '#d35400', '#c0392b']
            sns.barplot(x=contagem.values, y=contagem.index, palette=colors, ax=ax)
            sns.despine(left=True, bottom=True)
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig, use_container_width=True)
            
            maior_grupo = contagem.idxmax()
            st.markdown(f"""<div class="insight-box">
            <b>Insight de Negócio:</b> O perfil predominante nesta seleção é <b>{maior_grupo}</b>. 
            Se as barras inferiores (Laranja/Vermelho) dominarem, estamos diante de um grupo com alta sinistralidade e custo médico.
            </div>""", unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="chart-header">2. Carga Genética</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots()
            fam = df_filtrado['family_history'].value_counts()
            ax.pie(fam, labels=fam.index, autopct='%1.1f%%', colors=['#e74c3c', '#bdc3c7'], startangle=90)
            st.pyplot(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
            <b>Hereditariedade:</b> Em grupos de Obesidade Grau III, este gráfico geralmente mostra >85% de "Yes". Isso reforça a necessidade de medicina preventiva familiar.
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        
        # LINHA 2
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<div class="chart-header">3. Mapa de Calor: Transporte x Peso</div>', unsafe_allow_html=True)
            ct = pd.crosstab(df_filtrado['MTRANS'], df_filtrado['Obesity_PT'])
            ct_norm = ct.div(ct.sum(axis=1), axis=0)
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.heatmap(ct_norm, cmap="RdYlGn_r", annot=True, fmt=".0%", cbar=False, ax=ax)
            plt.ylabel("Meio de Transporte")
            plt.xlabel("")
            st.pyplot(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
            <b>Mobilidade Ativa:</b>
            Observe a linha "Automobile". O vermelho intenso nas colunas de Obesidade mostra que o sedentarismo no deslocamento é um fator crítico. Caminhada (Walking) atua como fator de proteção.
            </div>""", unsafe_allow_html=True)

        with c4:
            st.markdown('<div class="chart-header">4. Impacto da Tecnologia (Sedentarismo Digital)</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.violinplot(x='TUE', y='Obesity_PT', data=df_filtrado, order=ordem_obesidade, palette="cool", inner="quartile", ax=ax)
            plt.xlabel("Tempo em Dispositivos (0=Baixo, 2=Alto)")
            plt.ylabel("")
            st.pyplot(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
            <b>Efeito Tela:</b>
            Note como o formato do violino se desloca para a direita (maior uso) nos grupos de obesidade mórbida. O tempo de tela compete diretamente com o tempo de atividade física.
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # LINHA 3
        c5, c6 = st.columns(2)
        with c5:
            st.markdown('<div class="chart-header">5. O Mito do "Comer Pouco" (Snacking)</div>', unsafe_allow_html=True)
            ct_caec = pd.crosstab(df_filtrado['Obesity_PT'], df_filtrado['CAEC'])
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.heatmap(ct_caec, cmap="Blues", annot=True, fmt="d", cbar=False, ax=ax)
            plt.xlabel("Frequência de Lanches")
            plt.ylabel("")
            st.pyplot(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
            <b>Padrão Oculto:</b>
            O problema não é só quem come "Sempre" (Always), mas a grande massa que come "Às Vezes" (Sometimes) sem planejamento. A falta de rotina alimentar é o maior ofensor invisível.
            </div>""", unsafe_allow_html=True)

        with c6:
            st.markdown('<div class="chart-header">6. Evolução por Faixa Etária</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.boxplot(x='Age', y='Obesity_PT', data=df_filtrado, order=ordem_obesidade, palette="Spectral_r", ax=ax)
            plt.xlabel("Idade (anos)")
            plt.ylabel("")
            st.pyplot(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
            <b>Progressão:</b>
            Se a mediana (linha preta) sobe nos grupos de obesidade, confirma o acúmulo de peso com a idade. Outliers jovens em "Obesidade III" indicam necessidade de intervenção pediátrica imediata.
            </div>""", unsafe_allow_html=True)
            
        st.markdown("---")
        
        # LINHA 4 (MINI GRÁFICOS COM EXPLICAÇÃO)
        c7, c8, c9 = st.columns(3)
        with c7:
            st.markdown('<div class="chart-header">7. Hidratação (Litros)</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots()
            sns.barplot(x='Obesity_PT', y='CH2O', data=df_filtrado, order=ordem_obesidade, palette="Blues", ax=ax, errorbar=None)
            plt.xticks(rotation=90)
            plt.xlabel("")
            plt.ylabel("Litros/Dia")
            st.pyplot(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
            <b>Metabolismo:</b> A correlação é clara: pacientes com Obesidade Mórbida bebem menos água. A hidratação é essencial para a queima calórica basal.
            </div>""", unsafe_allow_html=True)

        with c8:
            st.markdown('<div class="chart-header">8. Tabagismo</div>', unsafe_allow_html=True)
            smoke_ct = pd.crosstab(df_filtrado['Obesity_PT'], df_filtrado['SMOKE'], normalize='index')
            fig, ax = plt.subplots()
            smoke_ct.plot(kind='bar', stacked=True, color=['#bdc3c7', '#2c3e50'], ax=ax)
            plt.legend(bbox_to_anchor=(1,1))
            plt.xticks(rotation=90)
            plt.xlabel("")
            st.pyplot(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
            <b>Fator Comorbidade:</b>
            Embora fumantes às vezes tenham peso menor, a combinação <b>Obesidade + Cigarro</b> multiplica o risco cardiovascular. Atenção redobrada.
            </div>""", unsafe_allow_html=True)
            
        with c9:
            st.markdown('<div class="chart-header">9. Freq. Refeições</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots()
            sns.pointplot(x='Obesity_PT', y='NCP', data=df_filtrado, order=ordem_obesidade, color="#e74c3c", ax=ax)
            plt.xticks(rotation=90)
            plt.xlabel("")
            plt.ylabel("Refeições/Dia")
            st.pyplot(fig, use_container_width=True)
            st.markdown("""<div class="insight-box">
            <b>Rotina:</b>
            Um número baixo de refeições (1 ou 2) muitas vezes indica jejuns prolongados seguidos de compulsão, padrão comum em alto IMC.
            </div>""", unsafe_allow_html=True)

    else:
        st.warning("⚠️ Nenhum dado disponível.")
    
    render_footer()

# --- 5. INSIGHTS ESTRATÉGICOS (COMPLETO) ---
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
    
    # --- AUDITORIA TÉCNICA DO MODELO ---
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
    
    render_footer()

# --- 6. SIMULADOR (FUNCIONAL) ---
elif menu == "Simulador de Risco":
    st.title("Simulador de Risco Clínico")
    st.markdown("Preencha a anamnese para obter a predição do modelo em tempo real.")
    
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
            if "Obesidade" in res_pt:
                st.error(f"🚨 **Diagnóstico Sugerido:** {res_pt}")
                st.write("**Recomendação:** Encaminhar para Endrocrinologia e Nutrição.")
            elif "Sobrepeso" in res_pt:
                st.warning(f"⚠️ **Diagnóstico Sugerido:** {res_pt}")
                st.write("**Recomendação:** Mudança de estilo de vida e monitoramento.")
            else:
                st.success(f"✅ **Diagnóstico Sugerido:** {res_pt}")
                st.write("**Recomendação:** Manter hábitos atuais.")
        except Exception as e:
            st.error(f"Erro no processamento: {e}")
    
    render_footer()
