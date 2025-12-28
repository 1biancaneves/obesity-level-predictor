## Sobre o Projeto

Este é um projeto de Machine Learning ponta a ponta (End-to-End) desenvolvido para classificar níveis de obesidade com base em hábitos alimentares e condição física. 

O modelo foi treinado com o algoritmo **Random Forest**, atingindo uma acurácia de **99%** no conjunto de teste, graças à engenharia de atributos (Criação da feature IMC/BMI). A interface foi construída com **Streamlit** para permitir o uso interativo por qualquer usuário.

## Funcionalidades

- **Coleta Interativa:** Formulário amigável para inserir dados de idade, peso, altura e hábitos.
- **Engenharia de Features:** Cálculo automático do IMC (Índice de Massa Corporal) em tempo real.
- **Predição Instantânea:** Classificação entre 7 categorias, desde "Peso Insuficiente" até "Obesidade Tipo III".
- **Feedback Visual:** Resultados codificados por cores para fácil interpretação.

## Tecnologias Utilizadas

- **Python**: Linguagem principal.
- **Pandas & NumPy**: Manipulação de dados.
- **Scikit-Learn**: Treinamento do modelo e pipelines.
- **Streamlit**: Framework para construção do Web App.
- **Joblib**: Persistência do modelo treinado.
