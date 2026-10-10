# DataPulse — Inteligência de Vendas para E-commerce

Dashboard de Business Intelligence desenvolvido em Python para explorar dados de vendas de um e-commerce, acompanhar indicadores comerciais e transformar dados em informações úteis para a tomada de decisões.

## Sobre o projeto

A DataPulse é um projeto de análise de dados que utiliza o conjunto público de dados brasileiros de e-commerce da Olist. A proposta é explorar informações de pedidos, produtos, pagamentos, clientes e entregas por meio de visualizações interativas.

O projeto faz parte do meu portfólio de desenvolvimento de competências em análise de dados e Business Intelligence, combinando programação, tratamento de dados e visualização analítica.

## Objetivos

- Explorar dados reais de operações de e-commerce.
- Acompanhar indicadores de vendas e pedidos.
- Analisar o desempenho de categorias de produtos.
- Investigar informações sobre pagamentos e entregas.
- Apresentar dados de forma visual e acessível para apoiar decisões de negócio.

## Tecnologias utilizadas

- **Python** — programação e manipulação de dados.
- **Pandas** — tratamento, organização e análise de dados.
- **Streamlit** — desenvolvimento da interface interativa.
- **Plotly** — criação de gráficos e visualizações.
- **Git e GitHub** — versionamento e publicação do código.

## Principais análises

O dashboard reúne indicadores e visualizações voltados à exploração de dados comerciais, incluindo:

- Faturamento e volume de pedidos.
- Ticket médio.
- Desempenho de categorias de produtos.
- Evolução mensal das vendas e dos pedidos.
- Distribuição dos meios de pagamento.
- Relação entre preços e frete.
- Indicadores relacionados a entregas.

## Fonte dos dados

O projeto utiliza dados públicos do conjunto Brazilian E-Commerce Public Dataset by Olist, disponibilizado no Kaggle.

Os dados permitem explorar diferentes dimensões da operação de um e-commerce, incluindo pedidos, itens, produtos, clientes, vendedores e pagamentos.

## Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/JohnBalth/DataPulse.git
cd DataPulse
```

### 2. Crie um ambiente virtual

No Windows:

```powershell
python -m venv .venv
```

### 3. Ative o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Execute o dashboard

```bash
streamlit run app.py
```

O Streamlit exibirá o endereço local para abrir o dashboard no navegador.

> **Observação:** a execução depende dos arquivos de dados esperados pelo código. Caso os dados não estejam disponíveis no repositório, será necessário obtê-los na fonte indicada e colocá-los nos caminhos utilizados pela aplicação.

## Estrutura do projeto

```text
DataPulse/
├── analytics/       # Scripts de análise e inspeção de dados
├── config/          # Configurações do projeto
├── dashboard/       # Componentes da aplicação
├── data/            # Arquivos de dados
├── sales/           # Módulo relacionado a vendas
├── app.py           # Aplicação Streamlit
├── manage.py        # Gerenciamento da estrutura Django
├── requirements.txt # Dependências Python
└── README.md        # Documentação do projeto
```

## Competências demonstradas

- Programação com Python.
- Manipulação e exploração de dados com Pandas.
- Construção de dashboards interativos.
- Visualização de dados com Plotly.
- Organização de projetos e controle de versão com Git.
- Análise de indicadores comerciais para apoio à tomada de decisão.

## Autor

**Jonatas Balthazar Nascimento**

Matemático formado pelo IFBA e mestrando no PPGCTA — UFSB/IFBA, em transição de carreira para tecnologia, com foco em Python, análise de dados e Business Intelligence.

- **GitHub:** [@JohnBalth](https://github.com/JohnBalth)
- **Projeto:** [DataPulse](https://github.com/JohnBalth/DataPulse)

---

*Projeto desenvolvido para fins de estudo, prática e construção de portfólio profissional em análise de dados e Business Intelligence.*