import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(
    page_title="Obesity Analytics Pro",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS AVANÇADO: Visual Limpo + Campos Claros
st.markdown("""
    <style>
    /* Fundo Geral */
    .stApp {background-color: #f4f6f9;}
    
    /* Cards brancos estilo Power BI */
    .css-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Títulos dos Cards */
    .card-title {
        color: #2c3e50;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 15px;
        border-bottom: 2px solid #3498db;
        padding-bottom: 5px;
    }
    
    /* MELHORIA NOS CAMPOS DE FORMULÁRIO (PEDIDO DO USUÁRIO) */
    /* Deixa o fundo dos inputs branco e borda mais visível */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div {
        background-color: #ffffff !important;
        border-color: #d1d5db !important;
        color: #1f2937 !important;
    }
    
    /* Métricas Grandes */
    div[data-testid="stMetricValue"] {
        font-size: 26px;
        color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PREPARAÇÃO (TRADUÇÃO E MODELO) ---
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

# --- 3. MENU LATERAL ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3050/3050523.png", width=80)
st.sidebar.title("Hospital Analytics")
menu = st.sidebar.radio("Módulos:", ["Visão Executiva", "Insights Estratégicos", "Simulador de Risco"])

if df is not None:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Filtros Globais")
    
    # Filtros com opção padrão "Todos" se vazio
    opcoes_genero = df['Gender'].unique()
    opcoes_hist = df['family_history'].unique()
    
    filtro_genero = st.sidebar.multiselect("Gênero", opcoes_genero, default=opcoes_genero)
    filtro_hist = st.sidebar.multiselect("Histórico Familiar", opcoes_hist, default=opcoes_hist)
    
    # CORREÇÃO DO BUG: Se o usuário limpar o filtro, seleciona TODOS automaticamente
    if not filtro_genero:
        filtro_genero = opcoes_genero
    if not filtro_hist:
        filtro_hist = opcoes_hist
    
    df_filtrado = df[
        (df['Gender'].isin(filtro_genero)) & 
        (df['family_history'].isin(filtro_hist))
    ]
else:
    df_filtrado = pd.DataFrame()

# --- 4. VISÃO EXECUTIVA (DASHBOARD) ---
if menu == "Visão Executiva":
    st.title("Monitoramento de Saúde Populacional")
    st.markdown("Visão estratégica para tomada de decisão clínica e preventiva.")

    if not df_filtrado.empty:
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        total_p = len(df_filtrado)
        obesos = df_filtrado['Obesity'].str.contains('Obesity').sum()
        pct_obesidade = (obesos / total_p) * 100
        alto_risco = df_filtrado['Obesity'].isin(['Obesity_Type_II', 'Obesity_Type_III']).sum()
        sedentarios = len(df_filtrado[df_filtrado['FAF'] <= 0.5])
        pct_sedentarios = (sedentarios / total_p) * 100

        with col1: st.metric("Total de Pacientes", total_p, delta="Base Atual")
        with col2: st.metric("Taxa de Obesidade", f"{pct_obesidade:.1f}%", delta="Alerta" if pct_obesidade > 30 else "Normal")
        with col3: st.metric("Pacientes Alto Risco", alto_risco, help="Grau II e III")
        with col4: st.metric("Taxa de Sedentarismo", f"{pct_sedentarios:.1f}%")

        st.markdown("---")

        # Gráficos Linha 1
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
            st.caption("Foco: Monitorar migração dos grupos de Sobrepeso para Obesidade.")

        with c2:
            st.markdown('<div class="card-title">🧬 Fator Genético</div>', unsafe_allow_html=True)
            fam_counts = df_filtrado['family_history'].value_counts()
            fig_pie, ax_pie = plt.subplots()
            ax_pie.pie(fam_counts, labels=fam_counts.index, autopct='%1.1f%%', startangle=90, colors=['#e74c3c', '#95a5a6'], wedgeprops=dict(width=0.4))
            st.pyplot(fig_pie)
            st.caption("Histórico Familiar é o principal previsor de risco.")

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
            
            # TEXTO INTERATIVO DE EXPLICAÇÃO
            with st.expander("ℹ️ Entenda este resultado"):
                st.write("""
                **O que o gráfico mostra?**
                Cores vermelhas indicam alta concentração de obesidade naquele meio de transporte. Cores verdes indicam pesos mais saudáveis.
                
                **Insight:**
                Usuários de 'Automóvel' apresentam taxas muito maiores de obesidade Grau II e III. 
                Usuários de 'Transporte Público' e 'Caminhada' tendem a ter controle de peso melhor devido à queima calórica passiva no deslocamento.
                """)

        with c4:
            st.markdown('<div class="card-title">💧 Consumo de Água (Litros)</div>', unsafe_allow_html=True)
            fig_box, ax_box = plt.subplots(figsize=(8, 5))
            sns.boxplot(x='CH2O', y='Obesity_PT', data=df_filtrado, palette="Blues", order=ordem, ax=ax_box)
            plt.ylabel("")
            st.pyplot(fig_box)
            
            # TEXTO INTERATIVO DE EXPLICAÇÃO
            with st.expander("ℹ️ Entenda este resultado"):
                st.write("""
                **Interpretação:**
                O gráfico mostra a distribuição de consumo de água. A linha preta dentro da caixa é a mediana.
                
                **Insight:**
                Note que nos níveis graves de obesidade, a mediana de consumo de água costuma ser baixa (próxima de 1L ou 1.5L). 
                Pacientes com 'Peso Normal' frequentemente aparecem com consumo superior a 2L/dia.
                """)

    else:
        st.warning("⚠️ Nenhum dado disponível. Verifique se o arquivo Obesity.csv está carregado.")

# --- 5. INSIGHTS ESTRATÉGICOS (TEXTO MELHORADO) ---
elif menu == "Insights Estratégicos":
    st.title("Relatório de Inteligência Clínica")
    st.markdown("Consolidação de descobertas e recomendações para a diretoria hospitalar.")
    
    st.markdown("---")

    col_txt1, col_txt2 = st.columns(2)

    with col_txt1:
        st.info("### 📌 Principais Descobertas")
        st.markdown("""
        **1. O Peso da Genética**
        Nossa análise demonstra que o **histórico familiar** é o fator determinante mais forte. Mais de **85%** dos pacientes com Obesidade Tipo II e III possuem familiares com a mesma condição.
        
        **2. A Armadilha do Transporte**
        Identificamos uma correlação direta entre o uso de **automóveis** e o aumento do IMC. Usuários de transporte público e caminhada apresentam índices significativamente menores de obesidade mórbida.
        
        **3. O Efeito da Hidratação**
        Pacientes que consomem menos de **1.5L de água por dia** tendem a se concentrar nas faixas de obesidade. O aumento da ingestão hídrica está associado a grupos de peso normal e sobrepeso leve.
        """)

    with col_txt2:
        st.success("### 🚀 Plano de Ação Sugerido")
        st.markdown("""
        **A. Protocolo de Triagem Genética**
        Implementar anamnese focada em histórico familiar na recepção **ou no consultório de triagem**. Pacientes com resposta positiva devem ser encaminhados para nutrição preventiva.
        
        **B. Programa 'Hospital em Movimento'**
        Criar incentivos para funcionários e pacientes utilizarem bicicletas ou caminhada. O combate ao sedentarismo no deslocamento diário mostra-se mais eficaz que academias esporádicas.
        * **Exemplos de incentivos:** Voucher de desconto em farmácias, estacionamento gratuito para bicicletas ou pontuação em programa de saúde corporativa.
        
        **C. Campanha de Hidratação**
        Instalar bebedouros inteligentes e campanhas visuais. A meta é elevar o consumo médio para **2.0L/dia**, uma intervenção de baixo custo e alto impacto.
        """)

    st.markdown("---")
    st.markdown("### 🧬 Performance Técnica do Modelo")
    
    c_tec1, c_tec2 = st.columns(2)
    with c_tec1:
        st.metric("Acurácia Real (Teste)", "93.62%", help="Assertividade em dados nunca vistos")
        st.metric("F1-Score Médio", "0.94", help="Média harmônica entre precisão e recall")
    
    with c_tec2:
        st.write("""
        Utilizamos um algoritmo **Random Forest Classifier** robusto. 
        
        **Destaques Técnicos:**
        * **Gap de Overfitting Controlado:** A diferença entre treino e teste foi de apenas ~5.8%, indicando ótima generalização.
        * **Precisão nos Extremos:** O modelo atingiu **100% de precisão** na identificação de 'Peso Insuficiente' e 'Obesidade Tipo III'.
        * **Desafio Superado:** A principal dificuldade era distinguir 'Peso Normal' de 'Sobrepeso Nível I' (fronteira tênue). O modelo manteve uma performance sólida (>85% de recall) mesmo nessas classes críticas.
        """)

# --- 6. SIMULADOR DE RISCO (TRIAGEM) ---
elif menu == "Simulador de Risco":
    st.title("Simulador de Risco Clínico")
    st.markdown("Preencha os dados do paciente para obter o diagnóstico sugerido pela IA.")
    
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

        st.markdown("#### 🏃 Estilo de Vida (Escala 1 a 3)")
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
