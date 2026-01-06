import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# --- 1. CONFIGURAÇÃO E ESTILO (RESPONSIVO) ---
st.set_page_config(
    page_title="FIAP - Health Intelligence",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS AVANÇADO PARA MOBILE E PC
st.markdown("""
    <style>
    /* Fundo Geral */
    .stApp {background-color: #f0f2f6;}
    
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
        font-family: 'Helvetica Neue', sans-serif;
        color: #2c3e50;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        border-left: 5px solid #3498db;
        padding-left: 10px;
    }
    
    /* Texto de Insight (Dinâmico) */
    .insight-box {
        background-color: #e8f4f8;
        border-left: 4px solid #3498db;
        padding: 15px;
        border-radius: 5px;
        font-size: 0.9rem;
        color: #2c3e50;
        margin-top: 10px;
    }
    
    /* Ajustes para Mobile (Media Query simulada via CSS Streamlit) */
    @media (max-width: 768px) {
        .stColumns {
            display: block !important;
        }
        [data-testid="column"] {
            width: 100% !important;
            margin-bottom: 20px;
        }
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

# Ordem lógica para gráficos
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
        # Criar Faixa Etária para Filtros
        bins = [0, 18, 30, 45, 60, 100]
        labels = ['0-18 (Jovens)', '19-30 (Adulto Jovem)', '31-45 (Adulto)', '46-60 (Meia Idade)', '60+ (Idoso)']
        df['Faixa_Etaria'] = pd.cut(df['Age'], bins=bins, labels=labels)
        return df
    except:
        return None

try:
    pipeline = joblib.load('modelo_obesidade.pkl')
except:
    st.error("Erro crítico: modelo_obesidade.pkl não encontrado.")
    st.stop()

df = carregar_dados()

# --- FUNÇÃO DE RODAPÉ ---
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

# --- 3. MENU LATERAL E FILTROS COMPLETOS ---
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
    
    # 1. Gênero
    f_gen = st.sidebar.multiselect("Gênero", df['Gender'].unique(), default=df['Gender'].unique())
    # 2. Histórico
    f_hist = st.sidebar.multiselect("Histórico Familiar", df['family_history'].unique(), default=df['family_history'].unique())
    # 3. Faixa Etária (NOVO)
    f_age = st.sidebar.multiselect("Faixa Etária", df['Faixa_Etaria'].unique().astype(str), default=df['Faixa_Etaria'].unique().astype(str))
    # 4. Transporte (NOVO)
    f_trans = st.sidebar.multiselect("Transporte", df['MTRANS'].unique(), default=df['MTRANS'].unique())
    
    # Lógica "Select All" se vazio
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
else:
    st.warning("Carregue o arquivo Obesity.csv")

# --- 4. DASHBOARD (O CORAÇÃO DO SISTEMA) ---
if menu == "Dashboard Analítico":
    st.title("Painel de Inteligência Médica")
    st.markdown("Análise populacional para suporte à decisão clínica.")

    if not df_filtrado.empty:
        # --- LINHA 1: KPIs ---
        col1, col2, col3, col4 = st.columns(4)
        total = len(df_filtrado)
        obesos = df_filtrado['Obesity'].str.contains('Obesity').sum()
        pct_ob = (obesos / total) * 100
        alto_risco = df_filtrado['Obesity'].isin(['Obesity_Type_II', 'Obesity_Type_III']).sum()
        pct_risco = (alto_risco / total) * 100
        
        with col1: st.metric("Pacientes Filtrados", total)
        with col2: st.metric("Taxa Obesidade", f"{pct_ob:.1f}%", delta="Base Filtrada")
        with col3: st.metric("Alto Risco (Grau II/III)", alto_risco, delta="Prioridade", delta_color="inverse")
        with col4: st.metric("Média de Idade", f"{df_filtrado['Age'].mean():.0f} anos")

        st.markdown("---")

        # --- LINHA 2: DISTRIBUIÇÃO E GENÉTICA ---
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown('<div class="chart-header">1. Estratificação de Risco (Quem são nossos pacientes?)</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 4))
            contagem = df_filtrado['Obesity_PT'].value_counts().reindex(ordem_obesidade).fillna(0)
            colors = ['#2ecc71', '#27ae60', '#f1c40f', '#f39c12', '#e67e22', '#d35400', '#c0392b']
            sns.barplot(x=contagem.values, y=contagem.index, palette=colors, ax=ax)
            sns.despine(left=True, bottom=True)
            st.pyplot(fig, use_container_width=True)
            
            # Insight Dinâmico
            maior_grupo = contagem.idxmax()
            pct_maior = (contagem.max() / total) * 100
            st.markdown(f"""
            <div class="insight-box">
            <b>Análise Inteligente:</b> O grupo predominante na seleção atual é <b>{maior_grupo}</b> ({pct_maior:.1f}%).<br>
            Note a progressão das barras. Se a base da pirâmide (laranja/vermelho) for maior que o topo (verde), há uma epidemia instalada no grupo filtrado.
            </div>""", unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="chart-header">2. Hereditariedade</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots()
            fam = df_filtrado['family_history'].value_counts()
            ax.pie(fam, labels=fam.index, autopct='%1.1f%%', colors=['#e74c3c', '#bdc3c7'], startangle=90)
            st.pyplot(fig, use_container_width=True)
            
            # Insight Dinâmico
            pct_fam = (len(df_filtrado[df_filtrado['family_history']=='yes']) / total) * 100
            st.markdown(f"""
            <div class="insight-box">
            <b>Genética:</b> {pct_fam:.1f}% dos pacientes possuem histórico familiar.
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        
        # --- LINHA 3: COMPORTAMENTO (MOBILIDADE E TELAS) ---
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<div class="chart-header">3. Mobilidade Urbana vs Peso</div>', unsafe_allow_html=True)
            # Crosstab normalizado para ver %
            ct = pd.crosstab(df_filtrado['MTRANS'], df_filtrado['Obesity_PT'])
            ct_norm = ct.div(ct.sum(axis=1), axis=0)
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.heatmap(ct_norm, cmap="RdYlGn_r", annot=True, fmt=".1f", cbar=False, ax=ax)
            st.pyplot(fig, use_container_width=True)
            
            st.markdown("""
            <div class="insight-box">
            <b>Impacto do Transporte:</b><br>
            • <b>Vermelho:</b> Alta concentração de obesidade naquele meio.<br>
            • <b>Insight:</b> Compare 'Automobile' com 'Walking'. O transporte passivo (carro) geralmente mostra taxas 2x maiores de Obesidade Grau III.
            </div>""", unsafe_allow_html=True)

        with c4:
            st.markdown('<div class="chart-header">4. O "Efeito Tela" (Sedentarismo Digital)</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.violinplot(x='TUE', y='Obesity_PT', data=df_filtrado, order=ordem_obesidade, palette="cool", inner="quartile", ax=ax)
            plt.xlabel("Tempo em Dispositivos (0 a 2)")
            st.pyplot(fig, use_container_width=True)
            
            st.markdown("""
            <div class="insight-box">
            <b>Interpretação:</b> Quanto mais "gordo" o violino para a direita, mais tempo de tela.<br>
            <b>Alerta:</b> Observe os grupos de Obesidade Mórbida. Eles tendem a ter uma mediana de tempo de tela superior aos grupos de Peso Normal.
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # --- LINHA 4: NUTRIÇÃO E HÁBITOS (NOVOS GRÁFICOS) ---
        c5, c6 = st.columns(2)
        with c5:
            st.markdown('<div class="chart-header">5. A Armadilha do "Belisco" (CAEC)</div>', unsafe_allow_html=True)
            ct_caec = pd.crosstab(df_filtrado['Obesity_PT'], df_filtrado['CAEC'])
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.heatmap(ct_caec, cmap="Blues", annot=True, fmt="d", cbar=False, ax=ax)
            st.pyplot(fig, use_container_width=True)
            
            st.markdown("""
            <div class="insight-box">
            <b>Análise de Snacking:</b> Cruza o grau de obesidade com a frequência de comer entre refeições.<br>
            <b>Padrão Oculto:</b> A maioria dos obesos não responde "Sempre" (Always), mas sim "Às vezes" (Sometimes). A falta de rotina é o vilão silencioso.
            </div>""", unsafe_allow_html=True)

        with c6:
            st.markdown('<div class="chart-header">6. Idade vs Evolução do Peso</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.boxplot(x='Age', y='Obesity_PT', data=df_filtrado, order=ordem_obesidade, palette="Spectral_r", ax=ax)
            st.pyplot(fig, use_container_width=True)
            
            st.markdown("""
            <div class="insight-box">
            <b>Progressão da Doença:</b><br>
            Se as caixas dos grupos de Obesidade estiverem mais à direita (idades maiores), indica que o peso se acumula com o tempo. Se estiverem à esquerda, alerta para obesidade juvenil.
            </div>""", unsafe_allow_html=True)
            
        st.markdown("---")
        
        # --- LINHA 5: COMORBIDDADES (ÁLCOOL E TABAGISMO) ---
        c7, c8, c9 = st.columns(3)
        with c7:
            st.markdown('<div class="chart-header">7. Consumo de Água</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots()
            sns.barplot(x='Obesity_PT', y='CH2O', data=df_filtrado, order=ordem_obesidade, palette="Blues", ax=ax, errorbar=None)
            plt.xticks(rotation=90)
            st.pyplot(fig, use_container_width=True)
            st.caption("Média de litros/dia por categoria.")

        with c8:
            st.markdown('<div class="chart-header">8. Tabagismo</div>', unsafe_allow_html=True)
            smoke_ct = pd.crosstab(df_filtrado['Obesity_PT'], df_filtrado['SMOKE'], normalize='index')
            fig, ax = plt.subplots()
            smoke_ct.plot(kind='bar', stacked=True, color=['#95a5a6', '#34495e'], ax=ax)
            plt.legend(title="Fuma?", bbox_to_anchor=(1,1))
            st.pyplot(fig, use_container_width=True)
            st.caption("Proporção de fumantes por grau.")
            
        with c9:
            st.markdown('<div class="chart-header">9. Frequência Refeições</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots()
            sns.pointplot(x='Obesity_PT', y='NCP', data=df_filtrado, order=ordem_obesidade, color="#e74c3c", ax=ax)
            plt.xticks(rotation=90)
            st.pyplot(fig, use_container_width=True)
            st.caption("Média de refeições principais/dia.")

    else:
        st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")
    
    render_footer()

# --- 5. INSIGHTS ESTRATÉGICOS (TEXTO MELHORADO) ---
elif menu == "Insights Estratégicos":
    st.title("Relatório Executivo")
    st.markdown("Principais descobertas baseadas nos dados analisados.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("### 🩺 Diagnóstico Clínico")
        st.write("""
        **1. Hereditariedade Dominante:** Pacientes com histórico familiar têm probabilidade significativamente maior de desenvolver obesidade severa. O fator genético é o preditor mais forte do modelo.
        
        **2. O Paradoxo do 'Belisco':** A obesidade não está correlacionada apenas com comer "Sempre", mas com a falta de rotina (comer "Às Vezes" entre refeições). Isso sugere que dietas muito restritivas que geram fome fora de hora podem ser contraproducentes.
        
        **3. Deserto de Hidratação:** Existe uma correlação inversa clara: quanto maior o peso, menor o consumo de água reportado.
        """)
    
    with col2:
        st.success("### 🚀 Plano de Ação (Negócio)")
        st.write("""
        **A. Foco no Transporte:** Parcerias com empresas para incentivar transporte ativo. O uso de carro é o maior correlato ambiental de obesidade grau III.
        
        **B. Triagem Precoce:** Implementar teste genético/familiar na admissão do plano de saúde.
        
        **C. Tecnologia:** Campanhas de "Detox Digital". O tempo de tela (TUE) compete diretamente com a atividade física (FAF).
        """)
        
    st.markdown("### 🧬 Sobre o Modelo")
    st.write(f"O modelo preditivo utiliza **Random Forest** com acurácia de **93.62%**.")
    st.write("A alta precisão deve-se à engenharia de atributos (cálculo de interações entre Peso/Altura) e à robustez do algoritmo contra dados não-lineares.")

    render_footer()

# --- 6. SIMULADOR (MANTIDO IGUAL) ---
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
            favc = st.selectbox("Comida Calórica?", ["Sim", "Não"])
            smoke = st.selectbox("Tabagismo?", ["Sim", "Não"])
        with c5:
            gender = st.selectbox("Gênero", ["Masculino", "Feminino"])
            calc = st.selectbox("Álcool?", ["Não", "Às vezes", "Frequentemente", "Sempre"])
            scc = st.selectbox("Monitora Calorias?", ["Sim", "Não"])

        st.markdown("##### Estilo de Vida")
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
            if "Obesidade" in res_pt: st.error(f"🚨 Resultado: {res_pt}")
            elif "Sobrepeso" in res_pt: st.warning(f"⚠️ Resultado: {res_pt}")
            else: st.success(f"✅ Resultado: {res_pt}")
        except Exception as e:
            st.error(f"Erro: {e}")
    
    render_footer()
