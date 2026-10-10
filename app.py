from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# CONFIGURAÇÃO
# =========================================================

st.set_page_config(
    page_title="DataPulse | Inteligência de Vendas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "raw"

AZUL = "#2563EB"
AZUL_ESCURO = "#111827"
CIANO = "#06B6D4"
TEXTO = "#1E293B"


# =========================================================
# ESTILO VISUAL
# =========================================================

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #F3F6FC;
    }

    [data-testid="stHeader"] {
        background-color: transparent;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #263247;
    }

    [data-testid="stSidebar"] * {
        color: #F8FAFC;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #CBD5E1;
    }

    .brand {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -1px;
        color: #FFFFFF;
        margin-bottom: 4px;
    }

    .brand span {
        color: #60A5FA;
    }

    .sidebar-description {
        color: #94A3B8;
        font-size: 12px;
        margin-bottom: 30px;
    }

    .page-title {
        color: #111827;
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 2px;
    }

    .page-subtitle {
        color: #64748B;
        font-size: 14px;
        margin-bottom: 24px;
    }

    .section-title {
        font-size: 19px;
        font-weight: 700;
        color: #1E293B;
        margin-top: 12px;
        margin-bottom: 3px;
    }

    .section-subtitle {
        font-size: 12px;
        color: #64748B;
        margin-bottom: 15px;
    }

    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.035);
    }

    [data-testid="stMetricLabel"] {
        color: #64748B;
        font-size: 13px;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #111827;
        font-size: 25px;
        font-weight: 800;
    }

    div[data-testid="stPlotlyChart"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 10px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.035);
    }

    .filter-note {
        background: #1E293B;
        padding: 12px;
        border-radius: 9px;
        color: #CBD5E1;
        font-size: 12px;
        margin-top: 18px;
    }

    .footer {
        text-align: center;
        color: #94A3B8;
        font-size: 11px;
        padding: 22px 0 10px 0;
        border-top: 1px solid #E2E8F0;
        margin-top: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def formatar_brl(valor):
    """Formata valores monetários em reais."""
    valor = float(valor)
    formatado = f"{valor:,.2f}"
    formatado = formatado.replace(",", "X")
    formatado = formatado.replace(".", ",")
    formatado = formatado.replace("X", ".")
    return f"R$ {formatado}"


def configurar_grafico(fig):
    """Aplica um padrão visual aos gráficos."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, sans-serif",
            color=TEXTO,
            size=12,
        ),
        margin=dict(l=15, r=25, t=25, b=15),
        hoverlabel=dict(
            bgcolor="#111827",
            font_color="#FFFFFF",
        ),
    )
    return fig


def formatar_quantidade(valor):
    return f"{valor:,.0f}".replace(",", ".")


# =========================================================
# CARREGAMENTO DOS DADOS
# =========================================================

try:
    pedidos = pd.read_csv(
        DATA_DIR / "olist_orders_dataset.csv"
    )
    itens = pd.read_csv(
        DATA_DIR / "olist_order_items_dataset.csv"
    )
    produtos = pd.read_csv(
        DATA_DIR / "olist_products_dataset.csv"
    )
    pagamentos = pd.read_csv(
        DATA_DIR / "olist_order_payments_dataset.csv"
    )

    # Arquivos complementares para análises adicionais
    clientes = None

    caminho_clientes = DATA_DIR / "olist_customers_dataset.csv"

    if caminho_clientes.exists():
        clientes = pd.read_csv(caminho_clientes)

except FileNotFoundError as erro:
    st.error(f"Arquivo CSV não encontrado: {erro.filename}")
    st.info("Confira se os arquivos estão dentro da pasta data/raw.")
    st.stop()


# =========================================================
# PREPARAÇÃO DOS DADOS
# =========================================================

pedidos["order_purchase_timestamp"] = pd.to_datetime(
    pedidos["order_purchase_timestamp"],
    errors="coerce",
)

for coluna in [
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]:
    if coluna in pedidos.columns:
        pedidos[coluna] = pd.to_datetime(
            pedidos[coluna],
            errors="coerce",
        )

datas_validas = pedidos[
    "order_purchase_timestamp"
].dropna()

if datas_validas.empty:
    st.error("Não existem datas válidas nos pedidos.")
    st.stop()

data_minima = datas_validas.min().date()
data_maxima = datas_validas.max().date()


# =========================================================
# SIDEBAR — FILTROS
# =========================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">Data<span>Pulse</span></div>
        <div class="sidebar-description">
            INTELIGÊNCIA DE VENDAS
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### ⚙️ Filtros")
    st.caption("Personalize os dados exibidos.")

    st.markdown("#### 📅 Período de análise")

    # Dois seletores independentes
    inicio = st.date_input(
        "Data inicial",
        value=data_minima,
        min_value=data_minima,
        max_value=data_maxima,
        format="DD/MM/YYYY",
        key="data_inicio",
    )

    fim = st.date_input(
        "Data final",
        value=data_maxima,
        min_value=data_minima,
        max_value=data_maxima,
        format="DD/MM/YYYY",
        key="data_fim",
    )

    status_disponiveis = sorted(
        pedidos["order_status"].dropna().unique().tolist()
    )

    status_padrao = (
        ["delivered"]
        if "delivered" in status_disponiveis
        else status_disponiveis
    )

    status = st.multiselect(
        "📦 Status dos pedidos",
        options=status_disponiveis,
        default=status_padrao,
    )

    st.markdown(
        """
        <div class="filter-note">
            <b>Fonte dos dados</b><br>
            Olist — conjunto público de dados de e-commerce.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# VALIDAÇÃO DOS FILTROS
# =========================================================

if inicio > fim:
    st.error(
        "A data inicial não pode ser posterior à data final. "
        "Ajuste os filtros na barra lateral."
    )
    st.stop()


# =========================================================
# APLICAÇÃO DOS FILTROS
# =========================================================

pedidos_filtrados = pedidos[
    pedidos["order_purchase_timestamp"].dt.date.between(
        inicio, fim
    )
    & pedidos["order_status"].isin(status)
].copy()

itens_filtrados = itens.merge(
    pedidos_filtrados[
        ["order_id", "order_purchase_timestamp"]
    ],
    on="order_id",
    how="inner",
)

itens_filtrados = itens_filtrados.merge(
    produtos[["product_id", "product_category_name"]],
    on="product_id",
    how="left",
)

pagamentos_filtrados = pagamentos.merge(
    pedidos_filtrados[["order_id"]],
    on="order_id",
    how="inner",
)

if clientes is not None and "customer_id" in pedidos_filtrados.columns:
    pedidos_com_clientes = pedidos_filtrados.merge(
        clientes[["customer_id", "customer_unique_id"]],
        on="customer_id",
        how="left",
    )
    clientes_unicos = pedidos_com_clientes[
        "customer_unique_id"
    ].nunique()
else:
    clientes_unicos = (
        pedidos_filtrados["customer_id"].nunique()
        if "customer_id" in pedidos_filtrados.columns
        else 0
    )


# =========================================================
# INDICADORES PRINCIPAIS
# =========================================================

receita = itens_filtrados["price"].sum()
total_pedidos = pedidos_filtrados["order_id"].nunique()
total_itens = len(itens_filtrados)

ticket_medio = (
    receita / total_pedidos
    if total_pedidos > 0
    else 0
)

st.markdown(
    '<div class="page-title">Visão geral das vendas</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="page-subtitle">'
    'Acompanhe os principais indicadores de desempenho do e-commerce.'
    '</div>',
    unsafe_allow_html=True,
)

st.caption(
    f"📅 {inicio.strftime('%d/%m/%Y')} até "
    f"{fim.strftime('%d/%m/%Y')}  |  "
    f"📦 {formatar_quantidade(total_pedidos)} pedidos"
)

st.markdown("#### Indicadores principais")

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Receita dos itens", formatar_brl(receita))
c2.metric("📦 Total de pedidos", formatar_quantidade(total_pedidos))
c3.metric("🎯 Ticket médio", formatar_brl(ticket_medio))
c4.metric("🛒 Itens vendidos", formatar_quantidade(total_itens))


# =========================================================
# INDICADORES COMPLEMENTARES
# =========================================================

st.markdown("---")
st.markdown("## 📊 Indicadores complementares")

frete_total = (
    itens_filtrados["freight_value"].sum()
    if "freight_value" in itens_filtrados.columns
    else 0
)

frete_medio = (
    frete_total / total_itens
    if total_itens > 0
    else 0
)

categorias_ativas = (
    itens_filtrados["product_category_name"].nunique()
    if not itens_filtrados.empty
    else 0
)

media_itens = (
    total_itens / total_pedidos
    if total_pedidos > 0
    else 0
)

i1, i2, i3, i4, i5 = st.columns(5)

i1.metric("👥 Clientes únicos", formatar_quantidade(clientes_unicos))
i2.metric("🚚 Frete total", formatar_brl(frete_total))
i3.metric("📦 Itens por pedido", f"{media_itens:.2f}".replace(".", ","))
i4.metric("🏷️ Categorias", formatar_quantidade(categorias_ativas))
i5.metric("💵 Frete médio por item", formatar_brl(frete_medio))


# =========================================================
# RECEITA MENSAL
# =========================================================

st.markdown("---")
st.markdown("## 📈 Análise de vendas")

col1, col2 = st.columns([1.15, 1])

with col1:
    st.markdown("### Evolução da receita mensal")

    if not itens_filtrados.empty:
        mensal = itens_filtrados.copy()

        mensal["mes"] = (
            mensal["order_purchase_timestamp"]
            .dt.to_period("M")
            .astype(str)
        )

        mensal = (
            mensal.groupby("mes", as_index=False)
            .agg(receita=("price", "sum"))
            .sort_values("mes")
        )

        fig = px.line(
            mensal,
            x="mes",
            y="receita",
            markers=True,
            labels={
                "mes": "Mês",
                "receita": "Receita (R$)",
            },
        )

        fig.update_traces(
            line=dict(color=AZUL, width=3),
            marker=dict(size=7),
            fill="tozeroy",
            fillcolor="rgba(37,99,235,0.08)",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Receita: R$ %{y:,.2f}<extra></extra>"
            ),
        )

        fig.update_xaxes(title=None, showgrid=False)
        fig.update_yaxes(
            title=None,
            gridcolor="#E2E8F0",
            tickprefix="R$ ",
            tickformat="~s",
        )

        st.plotly_chart(
            configurar_grafico(fig),
            use_container_width=True,
        )
    else:
        st.info("Não existem itens para o período selecionado.")


# =========================================================
# CATEGORIAS POR RECEITA
# =========================================================

with col2:
    st.markdown("### Categorias com maior receita")

    if not itens_filtrados.empty:
        itens_filtrados["product_category_name"] = (
            itens_filtrados["product_category_name"]
            .fillna("Sem categoria")
            .replace("", "Sem categoria")
        )

        categorias = (
            itens_filtrados.groupby(
                "product_category_name",
                as_index=False,
            )
            .agg(receita=("price", "sum"))
            .nlargest(10, "receita")
            .sort_values("receita")
        )

        fig = px.bar(
            categorias,
            x="receita",
            y="product_category_name",
            orientation="h",
            color="receita",
            color_continuous_scale=["#BFDBFE", AZUL],
            labels={
                "receita": "Receita (R$)",
                "product_category_name": "Categoria",
            },
        )

        fig.update_layout(coloraxis_showscale=False)

        fig.update_traces(
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Receita: R$ %{x:,.2f}<extra></extra>"
            )
        )

        fig.update_xaxes(
            title=None,
            gridcolor="#E2E8F0",
            tickprefix="R$ ",
            tickformat="~s",
        )
        fig.update_yaxes(title=None, showgrid=False)

        st.plotly_chart(
            configurar_grafico(fig),
            use_container_width=True,
        )
    else:
        st.info("Não existem categorias para analisar.")


# =========================================================
# PEDIDOS POR MÊS E DIA DA SEMANA
# =========================================================

col3, col4 = st.columns(2)

with col3:
    st.markdown("### Quantidade de pedidos por mês")

    mensal_pedidos = pedidos_filtrados.dropna(
        subset=["order_purchase_timestamp"]
    ).copy()

    mensal_pedidos["mes"] = (
        mensal_pedidos["order_purchase_timestamp"]
        .dt.to_period("M")
        .astype(str)
    )

    mensal_pedidos = (
        mensal_pedidos.groupby("mes", as_index=False)
        .agg(pedidos=("order_id", "nunique"))
        .sort_values("mes")
    )

    fig = px.bar(
        mensal_pedidos,
        x="mes",
        y="pedidos",
        labels={"mes": "Mês", "pedidos": "Pedidos"},
        color_discrete_sequence=[AZUL],
    )

    fig.update_layout(showlegend=False)
    fig.update_xaxes(title=None, showgrid=False)
    fig.update_yaxes(title=None, gridcolor="#E2E8F0")

    st.plotly_chart(
        configurar_grafico(fig),
        use_container_width=True,
    )


with col4:
    st.markdown("### Pedidos por dia da semana")

    dias_semana = {
        0: "Segunda-feira",
        1: "Terça-feira",
        2: "Quarta-feira",
        3: "Quinta-feira",
        4: "Sexta-feira",
        5: "Sábado",
        6: "Domingo",
    }

    por_dia = pedidos_filtrados.dropna(
        subset=["order_purchase_timestamp"]
    ).copy()

    por_dia["dia_numero"] = (
        por_dia["order_purchase_timestamp"].dt.dayofweek
    )
    por_dia["dia"] = por_dia["dia_numero"].map(dias_semana)

    por_dia = (
        por_dia.groupby(
            ["dia_numero", "dia"],
            as_index=False,
        )
        .agg(pedidos=("order_id", "nunique"))
        .sort_values("dia_numero")
    )

    fig = px.bar(
        por_dia,
        x="dia",
        y="pedidos",
        labels={"dia": "Dia da semana", "pedidos": "Pedidos"},
        color_discrete_sequence=[CIANO],
    )

    fig.update_layout(showlegend=False)
    fig.update_xaxes(title=None, tickangle=-30, showgrid=False)
    fig.update_yaxes(title=None, gridcolor="#E2E8F0")

    st.plotly_chart(
        configurar_grafico(fig),
        use_container_width=True,
    )


# =========================================================
# DISTRIBUIÇÃO DOS PREÇOS E FRETE
# =========================================================

col5, col6 = st.columns(2)

with col5:
    st.markdown("### Distribuição dos preços")

    if not itens_filtrados.empty:
        fig = px.histogram(
            itens_filtrados,
            x="price",
            nbins=30,
            labels={
                "price": "Preço do item (R$)",
                "count": "Quantidade de itens",
            },
            color_discrete_sequence=["#818CF8"],
        )

        fig.update_layout(showlegend=False)
        fig.update_xaxes(title=None, gridcolor="#E2E8F0")
        fig.update_yaxes(title="Quantidade de itens")

        st.plotly_chart(
            configurar_grafico(fig),
            use_container_width=True,
        )
    else:
        st.info("Não existem itens para analisar.")


with col6:
    st.markdown("### Relação entre preço e frete")

    if (
        not itens_filtrados.empty
        and "freight_value" in itens_filtrados.columns
    ):
        fig = px.scatter(
            itens_filtrados,
            x="price",
            y="freight_value",
            opacity=0.55,
            labels={
                "price": "Preço do item (R$)",
                "freight_value": "Frete (R$)",
            },
            color_discrete_sequence=[AZUL],
        )

        fig.update_layout(showlegend=False)
        fig.update_xaxes(title=None, gridcolor="#E2E8F0")
        fig.update_yaxes(title=None, gridcolor="#E2E8F0")

        st.plotly_chart(
            configurar_grafico(fig),
            use_container_width=True,
        )
    else:
        st.info("Dados de preço ou frete indisponíveis.")


# =========================================================
# DESEMPENHO DOS PRODUTOS
# =========================================================

st.markdown("---")
st.markdown("## 🛍️ Desempenho dos produtos")

if not itens_filtrados.empty:
    desempenho = itens_filtrados.copy()

    desempenho["product_category_name"] = (
        desempenho["product_category_name"]
        .fillna("Sem categoria")
        .replace("", "Sem categoria")
    )

    desempenho["order_item_id"] = (
        desempenho["order_item_id"]
        if "order_item_id" in desempenho.columns
        else desempenho["order_id"]
    )

    desempenho = (
        desempenho.groupby(
            "product_category_name",
            as_index=False,
        )
        .agg(
            receita=("price", "sum"),
            itens=("order_item_id", "count"),
        )
    )

    col7, col8 = st.columns(2)

    with col7:
        st.markdown("### Categorias por quantidade vendida")

        top_itens = (
            desempenho.nlargest(10, "itens")
            .sort_values("itens")
        )

        fig = px.bar(
            top_itens,
            x="itens",
            y="product_category_name",
            orientation="h",
            labels={
                "itens": "Itens vendidos",
                "product_category_name": "Categoria",
            },
            color_discrete_sequence=[CIANO],
        )

        fig.update_layout(showlegend=False)
        fig.update_xaxes(title=None, gridcolor="#E2E8F0")
        fig.update_yaxes(title=None, showgrid=False)

        st.plotly_chart(
            configurar_grafico(fig),
            use_container_width=True,
        )

    with col8:
        st.markdown("### Ranking de categorias")

        tabela = (
            desempenho.sort_values("receita", ascending=False)
            .head(10)
            .copy()
        )

        tabela["receita"] = tabela["receita"].apply(formatar_brl)

        tabela = tabela.rename(
            columns={
                "product_category_name": "Categoria",
                "receita": "Receita",
                "itens": "Itens vendidos",
            }
        )

        st.dataframe(
            tabela,
            use_container_width=True,
            hide_index=True,
        )
else:
    st.info("Não existem produtos para os filtros selecionados.")


# =========================================================
# FORMAS DE PAGAMENTO E PARCELAMENTO
# =========================================================

st.markdown("---")
st.markdown("## 💳 Perfil dos pagamentos")

col9, col10 = st.columns(2)

with col9:
    st.markdown("### Formas de pagamento")

    if not pagamentos_filtrados.empty:
        formas = (
            pagamentos_filtrados.groupby(
                "payment_type",
                as_index=False,
            )
            .agg(valor=("payment_value", "sum"))
            .sort_values("valor", ascending=False)
        )

        nomes_pagamento = {
            "credit_card": "Cartão de crédito",
            "debit_card": "Cartão de débito",
            "voucher": "Vale",
            "boleto": "Boleto",
            "not_defined": "Não definido",
        }

        formas["forma"] = formas["payment_type"].map(
            nomes_pagamento
        ).fillna(
            formas["payment_type"]
            .str.replace("_", " ")
            .str.title()
        )

        fig = px.pie(
            formas,
            names="forma",
            values="valor",
            hole=0.62,
            color_discrete_sequence=[
                AZUL,
                CIANO,
                "#818CF8",
                "#F59E0B",
                "#94A3B8",
            ],
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Valor: R$ %{value:,.2f}<br>"
                "Participação: %{percent}<extra></extra>"
            ),
        )

        st.plotly_chart(
            configurar_grafico(fig),
            use_container_width=True,
        )
    else:
        st.info("Não existem pagamentos para os filtros selecionados.")


with col10:
    st.markdown("### Valor por número de parcelas")

    if (
        not pagamentos_filtrados.empty
        and "payment_installments" in pagamentos_filtrados.columns
    ):
        parcelas = (
            pagamentos_filtrados.groupby(
                "payment_installments",
                as_index=False,
            )
            .agg(valor=("payment_value", "sum"))
            .sort_values("payment_installments")
        )

        fig = px.bar(
            parcelas,
            x="payment_installments",
            y="valor",
            labels={
                "payment_installments": "Número de parcelas",
                "valor": "Valor dos pagamentos (R$)",
            },
            color_discrete_sequence=["#6366F1"],
        )

        fig.update_traces(
            hovertemplate=(
                "Parcelas: %{x}<br>"
                "Valor: R$ %{y:,.2f}<extra></extra>"
            )
        )

        fig.update_layout(showlegend=False)
        fig.update_xaxes(title=None, gridcolor="#E2E8F0")
        fig.update_yaxes(
            title=None,
            tickprefix="R$ ",
            tickformat="~s",
            gridcolor="#E2E8F0",
        )

        st.plotly_chart(
            configurar_grafico(fig),
            use_container_width=True,
        )
    else:
        st.info("Não existem dados de parcelamento disponíveis.")


# =========================================================
# LOGÍSTICA E ENTREGAS
# =========================================================

st.markdown("---")
st.markdown("## 🚚 Logística e entregas")

if (
    "order_delivered_customer_date" in pedidos_filtrados.columns
    and "order_purchase_timestamp" in pedidos_filtrados.columns
):
    entregas = pedidos_filtrados.dropna(
        subset=[
            "order_purchase_timestamp",
            "order_delivered_customer_date",
        ]
    ).copy()

    entregas["dias_entrega"] = (
        entregas["order_delivered_customer_date"]
        - entregas["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    entregas = entregas[
        entregas["dias_entrega"] >= 0
    ]

    if not entregas.empty:
        media_entrega = entregas["dias_entrega"].mean()

        atrasos = (
            entregas["order_delivered_customer_date"]
            > entregas["order_estimated_delivery_date"]
        ).sum()

        taxa_atraso = atrasos / len(entregas) * 100

        l1, l2, l3 = st.columns(3)

        l1.metric(
            "⏱️ Tempo médio de entrega",
            f"{media_entrega:.1f} dias".replace(".", ","),
        )

        l2.metric(
            "⚠️ Entregas atrasadas",
            formatar_quantidade(atrasos),
        )

        l3.metric(
            "📉 Taxa de atraso",
            f"{taxa_atraso:.1f}%".replace(".", ","),
        )

        distribuicao_entrega = px.histogram(
            entregas,
            x="dias_entrega",
            nbins=25,
            labels={
                "dias_entrega": "Dias entre compra e entrega",
                "count": "Quantidade de pedidos",
            },
            color_discrete_sequence=[AZUL],
        )

        distribuicao_entrega.update_layout(showlegend=False)
        distribuicao_entrega.update_xaxes(
            title=None,
            gridcolor="#E2E8F0",
        )
        distribuicao_entrega.update_yaxes(
            title="Quantidade de pedidos",
        )

        st.plotly_chart(
            configurar_grafico(distribuicao_entrega),
            use_container_width=True,
        )
    else:
        st.info("Não há entregas concluídas suficientes para calcular o prazo.")
else:
    st.info("As colunas de datas de entrega não estão disponíveis.")


# =========================================================
# RODAPÉ
# =========================================================

st.markdown(
    """
    <div class="footer">
        <b>DataPulse</b> · Inteligência de Vendas para E-commerce<br>
        Dados públicos: Olist · Desenvolvido com Python, Pandas,
        Streamlit e Plotly
    </div>
    """,
    unsafe_allow_html=True,
)