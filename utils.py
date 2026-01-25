from typing import Dict, Tuple
import pandas as pd

def format_currency_brl(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def compute_scenario(faturamento: float, despesas: float, pro_labore: float, dividendos_total: float, num_pf: int, aliquota_irpj_csll: float = 0.34, limite_dividendos_pf: float = 50_000.0, aliquota_irrf_dividendos: float = 0.10) -> Dict[str, float]:
    faturamento = max(0, faturamento)
    despesas = max(0, despesas)
    pro_labore = max(0, pro_labore)
    dividendos_total = max(0, dividendos_total)
    num_pf = max(1, num_pf)
    lucro_antes_impostos = max(0, faturamento - despesas - pro_labore)
    irpj_csll = aliquota_irpj_csll * lucro_antes_impostos
    dividendos_por_pf = dividendos_total / num_pf
    irrf_dividendos = 0.0
    estourou_gatilho = dividendos_por_pf > limite_dividendos_pf
    if estourou_gatilho:
        irrf_dividendos = aliquota_irrf_dividendos * dividendos_total
    total_impostos = irpj_csll + irrf_dividendos
    carga_efetiva = (total_impostos / faturamento * 100) if faturamento > 0 else 0
    caixa_apos_impostos = faturamento - despesas - pro_labore - total_impostos
    lucro_apos_irpj_csll = lucro_antes_impostos - irpj_csll
    return {"faturamento": faturamento, "despesas": despesas, "pro_labore": pro_labore, "lucro_antes_impostos": lucro_antes_impostos, "irpj_csll": irpj_csll, "lucro_apos_irpj_csll": lucro_apos_irpj_csll, "dividendos_total": dividendos_total, "dividendos_por_pf": dividendos_por_pf, "estourou_gatilho": estourou_gatilho, "irrf_dividendos": irrf_dividendos, "total_impostos": total_impostos, "carga_efetiva": carga_efetiva, "caixa_apos_impostos": caixa_apos_impostos}

def validate_inputs(faturamento: float, despesas: float, pro_labore: float, dividendos_total: float) -> Tuple[bool, str]:
    alertas = []
    if any(v < 0 for v in [faturamento, despesas, pro_labore, dividendos_total]):
        return False, "❌ Erro: Valores não podem ser negativos."
    if faturamento == 0:
        return False, "❌ Erro: Faturamento deve ser maior que zero."
    if despesas + pro_labore > faturamento:
        alertas.append("⚠️ Atenção: Despesas + Pró-labore excedem o faturamento (lucro negativo).")
    lucro_estimado = max(0, faturamento - despesas - pro_labore)
    lucro_apos_ir_estimado = lucro_estimado * 0.66
    if dividendos_total > lucro_apos_ir_estimado * 1.1:
        alertas.append("⚠️ Atenção: Dividendos informados excedem o lucro líquido estimado. Verifique os valores.")
    if faturamento > 0 and pro_labore / faturamento < 0.05:
        alertas.append("⚠️ Alerta: Pró-labore muito baixo em relação ao faturamento. Isso pode gerar questionamentos fiscais.")
    mensagem = "\n".join(alertas) if alertas else ""
    return True, mensagem

def generate_summary_text(cenario_atual: Dict[str, float], cenario_otimizado: Dict[str, float], economia_mensal: float, economia_anual: float, num_pf: int, limite_dividendos_pf: float = 50_000.0) -> str:
    texto = "### 📊 Resumo Executivo\n\n"
    if cenario_atual["estourou_gatilho"]:
        texto += f"**Cenário Atual:** ⚠️ ATENÇÃO! Os dividendos por pessoa física ({format_currency_brl(cenario_atual['dividendos_por_pf'])}) **excedem o limite de {format_currency_brl(limite_dividendos_pf)}/mês**. Isso gera **IRRF de {format_currency_brl(cenario_atual['irrf_dividendos'])}** sobre os dividendos distribuídos.\n\n"
    else:
        texto += f"**Cenário Atual:** ✅ Dividendos por PF ({format_currency_brl(cenario_atual['dividendos_por_pf'])}) dentro do limite de {format_currency_brl(limite_dividendos_pf)}/mês. Sem IRRF sobre dividendos.\n\n"
    if cenario_otimizado["estourou_gatilho"]:
        texto += f"**Cenário Otimizado:** ⚠️ Ainda há IRRF de {format_currency_brl(cenario_otimizado['irrf_dividendos'])} ({format_currency_brl(cenario_otimizado['dividendos_por_pf'])} por PF). Considere reduzir dividendos ou aumentar número de sócios.\n\n"
    else:
        texto += f"**Cenário Otimizado:** ✅ Dividendos por PF ({format_currency_brl(cenario_otimizado['dividendos_por_pf'])}) dentro do limite. Sem IRRF sobre dividendos.\n\n"
    if economia_mensal > 0:
        texto += f"**💰 Economia Mensal:** {format_currency_brl(economia_mensal)}  \n**💰 Economia Anual:** {format_currency_brl(economia_anual)}  \n\n**Estratégia:** Aumentar despesas operacionais na PJ (despesas dedutíveis) reduz o lucro tributável, diminuindo IRPJ/CSLL e permitindo distribuir dividendos dentro do limite sem IRRF.\n"
    elif economia_mensal < 0:
        texto += f"**📈 Impacto:** O cenário otimizado resulta em **aumento** de impostos de {format_currency_brl(abs(economia_mensal))}/mês. Revise os parâmetros.\n"
    else:
        texto += "**📊 Impacto:** Ambos os cenários têm carga tributária equivalente.\n"
    return texto

def create_comparison_table(cenario_atual: Dict[str, float], cenario_otimizado: Dict[str, float]) -> pd.DataFrame:
    data = {"Métrica": ["Faturamento Mensal", "Despesas Operacionais", "Pró-labore", "Lucro Antes de Impostos", "IRPJ + CSLL (34%)", "Lucro Após IRPJ/CSLL", "Dividendos Distribuídos", "Dividendos por PF", "IRRF sobre Dividendos (10%)", "TOTAL IMPOSTOS", "Carga Efetiva (%)", "Caixa Após Impostos"], "Cenário Atual": [format_currency_brl(cenario_atual["faturamento"]), format_currency_brl(cenario_atual["despesas"]), format_currency_brl(cenario_atual["pro_labore"]), format_currency_brl(cenario_atual["lucro_antes_impostos"]), format_currency_brl(cenario_atual["irpj_csll"]), format_currency_brl(cenario_atual["lucro_apos_irpj_csll"]), format_currency_brl(cenario_atual["dividendos_total"]), format_currency_brl(cenario_atual["dividendos_por_pf"]), format_currency_brl(cenario_atual["irrf_dividendos"]), format_currency_brl(cenario_atual["total_impostos"]), f"{cenario_atual['carga_efetiva']:.2f}%", format_currency_brl(cenario_atual["caixa_apos_impostos"])], "Cenário Otimizado": [format_currency_brl(cenario_otimizado["faturamento"]), format_currency_brl(cenario_otimizado["despesas"]), format_currency_brl(cenario_otimizado["pro_labore"]), format_currency_brl(cenario_otimizado["lucro_antes_impostos"]), format_currency_brl(cenario_otimizado["irpj_csll"]), format_currency_brl(cenario_otimizado["lucro_apos_irpj_csll"]), format_currency_brl(cenario_otimizado["dividendos_total"]), format_currency_brl(cenario_otimizado["dividendos_por_pf"]), format_currency_brl(cenario_otimizado["irrf_dividendos"]), format_currency_brl(cenario_otimizado["total_impostos"]), f"{cenario_otimizado['carga_efetiva']:.2f}%", format_currency_brl(cenario_otimizado["caixa_apos_impostos"])]}
    return pd.DataFrame(data)
