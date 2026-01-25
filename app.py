import streamlit as st
import matplotlib.pyplot as plt
from utils import compute_scenario, validate_inputs, generate_summary_text, create_comparison_table, format_currency_brl

st.set_page_config(page_title="Simulador Reforma Tributária 2026", page_icon="💰", layout="wide")

st.title("💰 Simulador Reforma Tributária 2026 – Profissionais de Saúde")
st.markdown("Analise o impacto da **nova tributação sobre dividendos** (IRRF de 10% quando dividendos/mês por PF > R$ 50.000)")
st.divider()

with st.sidebar:
    st.header("⚙️ Parâmetros Tributários")
    aliquota_irpj_csll = st.slider("Alíquota IRPJ + CSLL (%)", 0.0, 50.0, 34.0, 0.5) / 100
    limite_dividendos_pf = st.number_input("Limite Dividendos/mês por PF (R$)", min_value=0.0, value=50_000.0, step=1_000.0)
    aliquota_irrf_dividendos = st.slider("Alíquota IRRF Dividendos (%)", 0.0, 30.0, 10.0, 0.5) / 100

col1, col2 = st.columns(2)
with col1:
    st.subheader("📋 Dados Básicos")
    regime = st.selectbox("Regime Tributário", ["Lucro Real", "Lucro Presumido", "Simples Nacional"])
    if regime != "Lucro Real":
        st.warning(f"⚠️ **{regime}** em modo simplificado. Apenas Lucro Real tem cálculo completo.")
        st.stop()
    municipio = st.text_input("Município", "São Paulo - SP")
    faturamento_mensal = st.number_input("Faturamento Mensal (R$)", 0.0, value=300_000.0, step=10_000.0)
    num_pf = st.number_input("Número de Sócios PF", 1, value=1, step=1)

with col2:
    st.subheader("📊 Cenário Atual")
    desp_atual = st.number_input("Despesas Atuais (R$)", 0.0, value=50_000.0, step=5_000.0, key="da")
    pl_atual = st.number_input("Pró-labore Atual (R$)", 0.0, value=15_000.0, step=1_000.0, key="pa")
    div_atual = st.number_input("Dividendos Atuais (R$)", 0.0, value=150_000.0, step=5_000.0, key="di")

st.divider()
st.subheader("🎯 Cenário Otimizado")
c3, c4, c5 = st.columns(3)
with c3:
    desp_otim = st.number_input("Despesas Otimizadas (R$)", 0.0, value=80_000.0, step=5_000.0, key="do")
with c4:
    pl_otim = st.number_input("Pró-labore Otimizado (R$)", 0.0, value=15_000.0, step=1_000.0, key="po")
with c5:
    div_otim = st.number_input("Dividendos Otimizados (R$)", 0.0, value=130_000.0, step=5_000.0, key="divo")

st.divider()
if st.button("🧮 Calcular", type="primary", use_container_width=True):
    v1, m1 = validate_inputs(faturamento_mensal, desp_atual, pl_atual, div_atual)
    v2, m2 = validate_inputs(faturamento_mensal, desp_otim, pl_otim, div_otim)
    if not v1 or not v2:
        st.error(m1 or m2)
        st.stop()
    if m1:
        st.warning(f"Atual: {m1}")
    if m2:
        st.warning(f"Otimizado: {m2}")
    
    c_atual = compute_scenario(faturamento_mensal, desp_atual, pl_atual, div_atual, num_pf, aliquota_irpj_csll, limite_dividendos_pf, aliquota_irrf_dividendos)
    c_otim = compute_scenario(faturamento_mensal, desp_otim, pl_otim, div_otim, num_pf, aliquota_irpj_csll, limite_dividendos_pf, aliquota_irrf_dividendos)
    
    eco_mensal = c_atual["total_impostos"] - c_otim["total_impostos"]
    eco_anual = eco_mensal * 12
    
    st.divider()
    st.subheader("📈 KPIs")
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Impostos Atual", format_currency_brl(c_atual["total_impostos"]))
    k2.metric("Impostos Otimizado", format_currency_brl(c_otim["total_impostos"]))
    k3.metric("Economia Mensal", format_currency_brl(eco_mensal))
    k4.metric("Economia Anual", format_currency_brl(eco_anual))
    red = (eco_mensal/c_atual["total_impostos"]*100) if c_atual["total_impostos"]>0 else 0
    k5.metric("Redução (%)", f"{red:.1f}%")
    
    st.divider()
    st.markdown(generate_summary_text(c_atual, c_otim, eco_mensal, eco_anual, num_pf, limite_dividendos_pf))
    
    st.divider()
    st.subheader("📊 Comparativo")
    st.dataframe(create_comparison_table(c_atual, c_otim), use_container_width=True, hide_index=True)
    
    st.divider()
    st.subheader("📊 Gráfico")
    fig, ax = plt.subplots(figsize=(10, 6))
    cats = ["IRPJ+CSLL", "IRRF Div", "TOTAL"]
    v_atual = [c_atual["irpj_csll"], c_atual["irrf_dividendos"], c_atual["total_impostos"]]
    v_otim = [c_otim["irpj_csll"], c_otim["irrf_dividendos"], c_otim["total_impostos"]]
    x = range(3)
    w = 0.35
    ax.bar([i-w/2 for i in x], v_atual, w, label="Atual", color="#FF6B6B")
    ax.bar([i+w/2 for i in x], v_otim, w, label="Otimizado", color="#4ECDC4")
    ax.set_xticks(x)
    ax.set_xticklabels(cats)
    ax.legend()
    ax.set_ylabel("R$")
    ax.set_title("Comparação de Impostos")
    st.pyplot(fig)
    
    st.divider()
    st.caption("⚠️ DISCLAIMER: Simulador educativo. Consulte um contador.")
