# TECH CHALLENGE FASE 4 - HEALTH ANALYTICS & PREDICTION

Este projeto foi desenvolvido como parte do Tech Challenge da FIAP (Pós-Tech em Data Analytics). O objetivo é apoiar hospitais e clínicas na triagem inteligente de pacientes, predizendo níveis de obesidade com base em hábitos de vida e históricos genéticos.

---

## ACESSO AS APLICACOES

### 1. Simulador de Risco (Streamlit)
Aplicação interativa para médicos realizarem a predição em tempo real durante a consulta.
Link: https://obesity-level-predictor.streamlit.app/

### 2. Dashboard Executivo (Looker Studio)
Painel de BI desenvolvido para a diretoria do hospital acompanhar indicadores macro e demografia.
Link: https://lookerstudio.google.com/u/0/reporting/4d0fd9b6-3102-4077-a1ef-bff6fa6de897/page/3VGkF

---

## ESTRUTURA DO REPOSITORIO

Abaixo, a descrição da organização dos arquivos neste projeto:

* app.py: Código fonte da aplicação Web (Streamlit). Contém o Front-end e a lógica de inferência.
* models/modelo_obesidade.pkl: Arquivo binário contendo o algoritmo Random Forest treinado.
* data/Obesity.csv: Dataset original utilizado para treino e para os gráficos do dashboard no app.
* requirements.txt: Lista de bibliotecas necessárias para a execução do projeto.

---

## SOBRE O MODELO DE MACHINE LEARNING

Utilizamos um algoritmo de Random Forest Classifier devido à sua robustez em lidar com dados não-lineares e alta capacidade de generalização.

* Acurácia Global (Teste): 93.62%
* Recall em Casos Críticos (Obesidade Mórbida): 100%
* Precision (Peso Normal): 94.0%

A escolha deste modelo se justifica pela capacidade de interpretar interações complexas entre variáveis comportamentais (como alimentação desregrada e sedentarismo digital) que modelos lineares tradicionais não capturam com a mesma eficácia.

---

## COMO INTERPRETAR OS RESULTADOS

### No Simulador (App)
O sistema foca na ação imediata de triagem.
1. Preencha os dados da anamnese (biometria e hábitos).
2. O modelo classifica o paciente entre "Peso Normal", "Sobrepeso" ou "Graus de Obesidade".
3. O sistema sugere intervenções baseadas no grau de risco identificado.

### No Dashboard (Looker Studio)
O painel foca na visão gerencial de longo prazo.
* Mapa de Calor: Identifica correlações entre meios de transporte e obesidade.
* Indicadores: Monitoramento da taxa global de sedentarismo e porcentagem de pacientes em risco cardiovascular.

---

## INSTALACAO E EXECUCAO LOCAL

Para executar este projeto em ambiente local:

1. Clone o repositório.
2. Instale as dependências listadas no arquivo requirements.txt.
3. Execute o comando: streamlit run app.py

---

## AUTORES

Projeto desenvolvido pelo Grupo - FIAP:

* Bianca Neves
* Erica Silva
* Diogo Oliveira
* Gabrielle Barbosa

© 2025 - Tech Challenge Fase 4
