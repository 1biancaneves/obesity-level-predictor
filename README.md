# TECH CHALLENGE FASE 4 - HEALTH ANALYTICS & PREDICTION

**Curso:** Pós-Tech Data Analytics (FIAP)
**Projeto:** Sistema Preditivo de Obesidade e Dashboard Analítico

---

## 📋 SOBRE O PROJETO

Este projeto simula um desafio real de **Data Science em contexto hospitalar**. O objetivo foi desenvolver um sistema inteligente para auxiliar a equipe médica na triagem e diagnóstico precoce de obesidade, utilizando dados históricos de hábitos de vida e condições genéticas.

O entregável consiste em duas frentes:
1.  **Visão Diagnóstica (Operacional):** Um modelo de Machine Learning em produção para classificar pacientes em tempo real.
2.  **Visão Analítica (Estratégica):** Um dashboard para gestores hospitalares identificarem padrões epidemiológicos.

---

## 🔗 LINKS DE ACESSO (ENTREGAS OBRIGATÓRIAS)

| Aplicação | Descrição | Link de Acesso |
| :--- | :--- | :--- |
| **Simulador de Risco** | Aplicação Web (Streamlit) com o modelo preditivo em produção. | [Acessar Aplicação Streamlit](https://obesity-level-predictor.streamlit.app/) |
| **Dashboard Analítico** | Painel gerencial (Looker Studio) com KPIs e insights de negócio. | [Acessar Dashboard Looker](https://lookerstudio.google.com/u/0/reporting/4d0fd9b6-3102-4077-a1ef-bff6fa6de897/page/3VGkF) |
| **Vídeo de Apresentação** | Pitch explicando a estratégia, o modelo e a visão de negócio. | *[INSIRA O LINK DO YOUTUBE/DRIVE AQUI]* |

---

## 📂 ESTRUTURA DO REPOSITÓRIO

O projeto segue uma arquitetura organizada para facilitar a avaliação técnica:

* **`app.py`**: Código fonte da aplicação Streamlit (Front-end e Back-end).
* **`data/`**: Contém o dataset `Obesity.csv` utilizado para treino e visualização.
* **`models/`**: Contém o arquivo binário `modelo_obesidade.pkl` (modelo treinado e serializado).
* **`assets/`**: Imagens e logotipos utilizados na interface gráfica.
* **`notebooks/`**: (Opcional) Contém o Jupyter Notebook com a análise exploratória (EDA), Feature Engineering e testes de algoritmos.
* **`requirements.txt`**: Lista de dependências Python.

---

## 🧠 PERFORMANCE DO MODELO (MACHINE LEARNING)

Para atender ao requisito de **acurácia superior a 75%**, desenvolvemos e comparamos diversos algoritmos. O modelo escolhido foi o **Random Forest Classifier**.

### Métricas de Teste (Dados não vistos)
* **Acurácia Global:** 93.62% (Superando a meta de 75%)
* **Recall (Obesidade Mórbida):** 100%
* **Precision (Peso Normal):** 94.0%

### Justificativa Técnica
O Random Forest foi selecionado por sua robustez em lidar com dados não-lineares e interações complexas entre variáveis (ex: a relação entre *Consumo de Vegetais* e *Sedentarismo*). Implementamos **Feature Engineering** calculando interações entre peso/altura e convertendo variáveis categóricas para numéricas, o que elevou a precisão do modelo.

---

## 📊 INSIGHTS DE NEGÓCIO (VISÃO ANALÍTICA)

Conforme solicitado no desafio, a análise de dados gerou insights acionáveis para a equipe médica:

1.  **Fator Genético:** Histórico familiar é o preditor mais forte (>85% de correlação com casos graves).
2.  **Mobilidade Urbana:** O uso de transporte passivo (carro) está diretamente ligado à Obesidade Grau III, enquanto transporte ativo (caminhada/transporte público) atua como fator de proteção.
3.  **Hidratação:** Identificamos um padrão de baixo consumo de água (< 1.5L/dia) em pacientes de alto risco.
4.  **Comportamento Alimentar:** O hábito de "beliscar" sem planejamento (comer entre refeições "Às vezes") mostrou-se mais nocivo do que comer frequentemente, devido à falta de rotina metabólica.

---

## 🛠️ COMO EXECUTAR LOCALMENTE

Para rodar a aplicação em sua máquina:

1.  Clone este repositório.
2.  Instale as bibliotecas necessárias:
    ```bash
    pip install -r requirements.txt
    ```
3.  Execute o Streamlit:
    ```bash
    streamlit run app.py
    ```

---

## 👥 AUTORES

**Grupo - FIAP Pós-Tech**

* **Bianca Neves**
* **Erica Silva**
* **Diogo Oliveira**
* **Gabrielle Barbosa**

---
© 2025 - Tech Challenge Fase 4
