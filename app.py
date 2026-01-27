import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from utils import compute_scenario, validate_inputs, generate_summary_text, create_comparison_table, format_currency_brl

st.set_page_config(
    page_title="Simulador Reforma Tributária 2026",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Google Analytics
st.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XFVCFPN1H6"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XFVCFPN1H6');
</script>
""")

# EmailJS Library
st.html("""
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/@emailjs/browser@3/dist/email.min.js"></script>
<script type="text/javascript">
   (function(){
      emailjs.init("ZZRaJaP0r4vfr4mYV");
   })();
</script>
""")

# CSS customizado - Estilo Apple/Profissional
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
    }
    
    h1 {
        color: #1e3a5f !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem !important;
    }
    
    h2, h3 {
        color: #2c5282 !important;
        font-weight: 600 !important;
        letter-spacing: -0.3px;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 4px 15px rgba(30, 58, 95, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30, 58, 95, 0.4) !important;
    }
    
    .stNumberInput>div>div>input {
        border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput>div>div>input:focus {
        border-color: #1e3a5f !important;
        box-shadow: 0 0 0 3px rgba(30, 58, 95, 0.1) !important;
    }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 0.75rem !important;
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: #1e3a5f !important;
        box-shadow: 0 0 0 3px rgba(30, 58, 95, 0.1) !important;
    }
    
    .stSelectbox>div>div {
        border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important;
    }
    
    .stSlider>div>div>div>div {
        background: linear-gradient(90deg, #1e3a5f 0%, #2c5282 100%) !important;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #1e3a5f !important;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 2px solid #e2e8f0;
    }
    
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }
    
    .icon-text {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        color: #1e3a5f;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .helper-text {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 400;
        margin-top: 0.25rem;
        line-height: 1.4;
    }
    
    .section-header {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #1e3a5f;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    .feedback-box {
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
        border-radius: 16px;
        padding: 2rem;
        border: 2px solid #bae6fd;
        box-shadow: 0 4px 16px rgba(30, 58, 95, 0.1);
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>💰 Simulador Reforma Tributária 2026</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; font-size: 1.1rem; margin-top: -0.5rem;'>Profissionais de Saúde</p>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; font-size: 0.95rem;'>Analise o impacto da <strong>nova tributação sobre dividendos</strong> (IRRF de 10% quando dividendos/mês por PF > R$ 50.000)</p>", unsafe_allow_html=True)

st.divider()

# Sidebar
with st.sidebar:
    st.markdown("<div class='section-header'><h2 style='margin:0; font-size:1.3rem;'>⚙️ Parâmetros Tributários</h2></div>", unsafe_allow_html=True)
    
    aliquota_irpj_csll = st.slider(
        "Alíquota IRPJ + CSLL (%)",
        0.0, 50.0, 34.0, 0.5,
        help="Alíquota combinada de IRPJ e CSLL"
    ) / 100
    
    limite_dividendos_pf = st.number_input(
        "Limite Dividendos/mês por PF (R$)",
        min_value=0.0,
        value=50_000.0,
        step=1_000.0,
        help="Limite mensal antes de incidir IRRF"
    )
    
    aliquota_irrf_dividendos = st.slider(
        "Alíquota IRRF Dividendos (%)",
        0.0, 30.0, 10.0, 0.5,
        help="Alíquota do IRRF sobre dividendos excedentes"
    ) / 100
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("💡 Ajuste os parâmetros conforme a legislação vigente")

# Conteúdo principal
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='section-header'><h3 style='margin:0;'>📋 Dados Básicos</h3></div>", unsafe_allow_html=True)
    
    regime = st.selectbox(
        "Regime Tributário",
        ["Lucro Real", "Lucro Presumido", "Simples Nacional"],
        help="Selecione o regime fiscal da empresa"
    )
    
    if regime != "Lucro Real":
        st.warning(f"⚠️ **{regime}** em modo simplificado. Apenas Lucro Real tem cálculo completo.")
        st.stop()
    
    municipio = st.text_input("Município", "São Paulo - SP")
    
    st.markdown("<div class='icon-text'>💵 Faturamento Mensal</div>", unsafe_allow_html=True)
    faturamento_mensal = st.number_input(
        "Faturamento (R$)",
        0.0,
        value=300_000.0,
        step=10_000.0,
        label_visibility="collapsed"
    )
    
    st.markdown("<div class='icon-text'>👥 Número de Sócios PF</div>", unsafe_allow_html=True)
    num_pf = st.number_input(
        "Sócios",
        1,
        value=1,
        step=1,
        label_visibility="collapsed",
        help="Pessoas físicas que recebem dividendos"
    )

with col2:
    st.markdown("""
    <div class='section-header'>
        <h3 style='margin:0; margin-bottom: 0.5rem;'>📊 Cenário Atual</h3>
        <p class='helper-text' style='margin:0;'>Como é feito o lançamento das despesas na PJ e a retirada para PF atualmente</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='icon-text'>💼 Despesas Operacionais Atuais</div>", unsafe_allow_html=True)
    st.markdown("<p class='helper-text'>Despesas pagas e declaradas pela PJ</p>", unsafe_allow_html=True)
    desp_atual = st.number_input("Despesas atuais (R$)", 0.0, value=50_000.0, step=5_000.0, key="da", label_visibility="collapsed")
    
    st.markdown("<div class='icon-text'>👔 Pró-labore Atual</div>", unsafe_allow_html=True)
    st.markdown("<p class='helper-text'>Pró-labore declarado e pago oficialmente</p>", unsafe_allow_html=True)
    pl_atual = st.number_input("Pró-labore atual (R$)", 0.0, value=15_000.0, step=1_000.0, key="pa", label_visibility="collapsed")
    
    st.markdown("<div class='icon-text'>💰 Dividendos Mensais Atuais</div>", unsafe_allow_html=True)
    st.markdown("<p class='helper-text'>Transferência de lucros da PJ para PF</p>", unsafe_allow_html=True)
    div_atual = st.number_input("Dividendos atuais (R$)", 0.0, value=150_000.0, step=5_000.0, key="di", label_visibility="collapsed")

st.divider()

st.markdown("""
<div class='section-header'>
    <h3 style='margin:0; margin-bottom: 0.5rem;'>🎯 Cenário Otimizado</h3>
    <p class='helper-text' style='margin:0;'>Valores que ajustará para uma otimização da carga tributária</p>
</div>
""", unsafe_allow_html=True)

c3, c4, c5 = st.columns(3)

with c3:
    st.markdown("<div class='icon-text'>💼 Despesas Otimizadas</div>", unsafe_allow_html=True)
    st.markdown("<p class='helper-text'>Despesas pagas e declaradas pela PJ</p>", unsafe_allow_html=True)
    desp_otim = st.number_input("Despesas otimizadas (R$)", 0.0, value=80_000.0, step=5_000.0, key="do", label_visibility="collapsed")

with c4:
    st.markdown("<div class='icon-text'>👔 Pró-labore Otimizado</div>", unsafe_allow_html=True)
    st.markdown("<p class='helper-text'>Pró-labore declarado e pago oficialmente</p>", unsafe_allow_html=True)
    pl_otim = st.number_input("Pró-labore otimizado (R$)", 0.0, value=15_000.0, step=1_000.0, key="po", label_visibility="collapsed")

with c5:
    st.markdown("<div class='icon-text'>💰 Dividendos Otimizados</div>", unsafe_allow_html=True)
    st.markdown("<p class='helper-text'>Transferência de lucros da PJ para PF</p>", unsafe_allow_html=True)
    div_otim = st.number_input("Dividendos otimizados (R$)", 0.0, value=130_000.0, step=5_000.0, key="divo", label_visibility="collapsed")

st.divider()

if st.button("🧮 Calcular Análise Comparativa", type="primary", use_container_width=True):
    st.html("""
    <script>
        gtag('event', 'simulation_calculated', {
            'event_category': 'engagement',
            'event_label': 'tax_simulation'
        });
    </script>
    """)
    
    v1, m1 = validate_inputs(faturamento_mensal, desp_atual, pl_atual, div_atual)
    v2, m2 = validate_inputs(faturamento_mensal, desp_otim, pl_otim, div_otim)
    
    if not v1 or not v2:
        st.error(m1 or m2)
        st.stop()
    
    if m1:
        st.warning("**Cenário Atual:**\n" + m1)
    if m2:
        st.warning("**Cenário Otimizado:**\n" + m2)
    
    c_atual = compute_scenario(faturamento_mensal, desp_atual, pl_atual, div_atual, num_pf, aliquota_irpj_csll, limite_dividendos_pf, aliquota_irrf_dividendos)
    c_otim = compute_scenario(faturamento_mensal, desp_otim, pl_otim, div_otim, num_pf, aliquota_irpj_csll, limite_dividendos_pf, aliquota_irrf_dividendos)
    
    eco_mensal = c_atual["total_impostos"] - c_otim["total_impostos"]
    eco_anual = eco_mensal * 12
    
    st.divider()
    st.markdown("<div class='section-header'><h2 style='margin:0;'>📈 Indicadores-Chave (KPIs)</h2></div>", unsafe_allow_html=True)
    
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("💸 Impostos Atual", format_currency_brl(c_atual["total_impostos"]))
    k2.metric("✨ Impostos Otimizado", format_currency_brl(c_otim["total_impostos"]))
    k3.metric("💰 Economia Mensal", format_currency_brl(eco_mensal))
    k4.metric("🎯 Economia Anual", format_currency_brl(eco_anual))
    red = (eco_mensal/c_atual["total_impostos"]*100) if c_atual["total_impostos"]>0 else 0
    k5.metric("📊 Redução", f"{red:.1f}%")
    
    st.divider()
    st.markdown(generate_summary_text(c_atual, c_otim, eco_mensal, eco_anual, num_pf, limite_dividendos_pf))
    
    st.divider()
    st.markdown("<div class='section-header'><h2 style='margin:0;'>📊 Comparativo Detalhado</h2></div>", unsafe_allow_html=True)
    st.dataframe(create_comparison_table(c_atual, c_otim), use_container_width=True, hide_index=True)
    
    st.divider()
    st.markdown("<div class='section-header'><h2 style='margin:0;'>📊 Visualização: Impostos por Cenário</h2></div>", unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#f8fafc')
    
    cats = ["IRPJ + CSLL", "IRRF Dividendos", "TOTAL"]
    v_atual = [c_atual["irpj_csll"], c_atual["irrf_dividendos"], c_atual["total_impostos"]]
    v_otim = [c_otim["irpj_csll"], c_otim["irrf_dividendos"], c_otim["total_impostos"]]
    
    x = range(3)
    w = 0.35
    
    bars1 = ax.bar([i-w/2 for i in x], v_atual, w, label="Cenário Atual", color="#ef4444", alpha=0.85, edgecolor='white', linewidth=2)
    bars2 = ax.bar([i+w/2 for i in x], v_otim, w, label="Cenário Otimizado", color="#1e3a5f", alpha=0.85, edgecolor='white', linewidth=2)
    
    ax.set_xlabel("Categoria de Imposto", fontsize=13, fontweight='600', color='#1e3a5f')
    ax.set_ylabel("Valor (R$)", fontsize=13, fontweight='600', color='#1e3a5f')
    ax.set_title("Comparação de Impostos: Atual vs Otimizado", fontsize=16, fontweight='700', color='#1e3a5f', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(cats, fontsize=11)
    ax.legend(frameon=True, fancybox=True, shadow=True, fontsize=11)
    ax.grid(axis="y", alpha=0.2, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, height, f"R$ {height:,.0f}", 
                   ha="center", va="bottom", fontsize=10, fontweight='600')
    
    st.pyplot(fig)
    
    st.divider()
    st.markdown("<div class='section-header'><h2 style='margin:0;'>💡 Insights e Recomendações</h2></div>", unsafe_allow_html=True)
    
    if c_atual["estourou_gatilho"] and not c_otim["estourou_gatilho"]:
        st.success("✅ **Excelente!** O cenário otimizado elimina o IRRF sobre dividendos, mantendo distribuição por PF abaixo do limite de R$ 50.000/mês.")
    elif c_atual["estourou_gatilho"] and c_otim["estourou_gatilho"]:
        st.info("ℹ️ **Oportunidade:** Ambos os cenários ainda geram IRRF. Considere aumentar o número de sócios, reduzir dividendos ou aumentar despesas dedutíveis na PJ.")
    
    if eco_mensal > 10_000:
        st.success(f"💰 **Economia significativa!** Você pode economizar {format_currency_brl(eco_anual)} por ano. Recomendamos consultar um contador.")

# Seção de Feedback
st.divider()
st.markdown("""
<div class='feedback-box'>
    <h2 style='color: #1e3a5f; margin-top: 0;'>💬 Ajude-nos a Melhorar!</h2>
    <p style='color: #64748b; font-size: 1rem; margin-bottom: 1.5rem;'>
        Esta plataforma é um <strong>MVP (Produto Mínimo Viável)</strong> e estamos em constante evolução. 
        Sua opinião é fundamental para desenvolvermos uma ferramenta cada vez mais útil para profissionais de saúde.
        <strong>Todas as sugestões são muito bem-vindas!</strong> 🙏
    </p>
</div>
""", unsafe_allow_html=True)

# Campos do formulário
col_f1, col_f2 = st.columns(2)

with col_f1:
    nome = st.text_input("Nome (opcional)", placeholder="Seu nome", key="nome_input")
    email_user = st.text_input("E-mail (opcional)", placeholder="seu@email.com", key="email_input")

with col_f2:
    cidade = st.text_input("Cidade/Estado (opcional)", placeholder="Ex: São Paulo - SP", key="cidade_input")
    profissao = st.text_input("Profissão (opcional)", placeholder="Ex: Médico, Contador", key="prof_input")

sugestao = st.text_area(
    "Sua sugestão, crítica ou ideia de melhoria:",
    placeholder="Conte-nos o que você achou, o que poderia ser melhorado, quais funcionalidades gostaria de ver...",
    height=150,
    key="sugestao_input"
)

# Container para mensagens
message_container = st.empty()

if st.button("📤 Enviar Feedback", use_container_width=True, key="btn_feedback"):
    if sugestao.strip():
        # Limpar e escapar dados
        nome_clean = nome.replace("'", "\\'").replace('"', '\\"').replace("\n", " ") if nome else "Anônimo"
        email_clean = email_user.replace("'", "\\'").replace('"', '\\"') if email_user else "Não informado"
        cidade_clean = cidade.replace("'", "\\'").replace('"', '\\"') if cidade else "Não informado"
        profissao_clean = profissao.replace("'", "\\'").replace('"', '\\"') if profissao else "Não informado"
        sugestao_clean = sugestao.replace("'", "\\'").replace('"', '\\"').replace("\n", "\\n")
        
        # Enviar via EmailJS
        st.html(f"""
        <script>
            emailjs.send('service_tsbp6kf', 'template_il9i7r6', {{
                nome: '{nome_clean}',
                email: '{email_clean}',
                cidade: '{cidade_clean}',
                profissao: '{profissao_clean}',
                sugestao: '{sugestao_clean}'
            }}).then(
                function(response) {{
                    console.log('✅ Email enviado com sucesso!', response.status, response.text);
                    gtag('event', 'feedback_sent', {{
                        'event_category': 'engagement',
                        'event_label': 'user_feedback'
                    }});
                }},
                function(error) {{
                    console.log('❌ Erro ao enviar email:', error);
                }}
            );
        </script>
        """)
        
        message_container.success("✅ Feedback enviado com sucesso! Muito obrigado pela sua contribuição! 🎉")
        st.balloons()
    else:
        message_container.warning("⚠️ Por favor, escreva sua sugestão antes de enviar.")

st.divider()
st.caption("⚠️ **DISCLAIMER:** Este é um simulador educativo e não substitui consultoria contábil ou jurídica.")
