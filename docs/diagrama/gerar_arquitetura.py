"""
Hotel Pet Analytics: estado atual do repositório x arquitetura-alvo do roadmap.

Fontes da verdade:
  database/02_create_tables.sql ...... 9 tabelas, 8 FOREIGN KEY, CHECK/ENUM/UNIQUE
  database/01..04_*.sql .............. criação, dados de exemplo e teste do fluxo de reserva
  data_generator/generate_synthetic_data.py  Faker pt_BR, seed 42, 300 clientes, 20 quartos,
                                       12 funcionários, 2.500 reservas (2024-01 a 2025-06),
                                       sazonalidade (jan/jul/dez), risco de cancelamento,
                                       saída database/05_insert_synthetic_data.sql (lotes de 500)
  src/*, dags/, docker/, tests/ ...... apenas __init__.py e .gitkeep (não implementados)
  requirements.txt / README .......... stack planejada: PySpark, Delta, Great Expectations,
                                       scikit-learn, Airflow, Docker Compose

Grade (1x): canvas 1920 x 880
  cabeçalho y 0-110 | implementado y 130-450 | alvo y 490-740 | rodapé y 765-865
  Corredores: DDL -> MySQL em y = 410; MySQL -> Ingestão em y = 470 (entre os grupos), saindo em x = 1320 para não cruzar o primeiro.
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from diagram_kit import Diagram, PALETTE as P

d = Diagram(1920, 880)
MYSQL_BLUE = "#00758F"

def planned(cx, y, w, icon, title, lines, isz=40):
    h = isz + 34 + 17 * len(lines) + 12
    x = cx - w / 2
    d.rect(x, y, w, h, fill="#FAFAFA", stroke="#B8C0C2", sw=1.3, dash="5 4")
    d.out.append('<g opacity="0.5">'); d.icon(icon, cx - isz / 2, y + 12, isz); d.out.append("</g>")
    d.text(cx, y + isz + 30, title, 15, "#5F686C", True, maxw=w - 12)
    for i, l in enumerate(lines):
        d.text(cx, y + isz + 49 + 17 * i, l, 12.5, "#879196", maxw=w - 12)
    d.boxes.append((title, x, y, w, h))
    return (x, y, w, h)

d.header("Hotel Pet Analytics", "Plataforma de dados para hotelaria pet: o que já existe e para onde vai",
         "MySQL  ·  Python  ·  Faker  ·  roadmap: PySpark, Delta Lake, Airflow, scikit-learn  ·  https://github.com/Ant4rez/Hotel-Pet-Analytics",
         chip="Projeto autoral · em construção")

# ---------------- Implementado ----------------
d.group(40, 130, 1840, 320, "Implementado  ·  Fase 1 (modelagem relacional) e gerador de dados sintéticos", MYSQL_BLUE, "#F2F8FA")
Y = 190
a1 = d.card(200, Y, 230, "programming/flowchart/multiple-documents.png", "Requisitos e modelagem",
            ["Requisitos.md · MER", "dicionário de dados", "origem: curso de DBA (Senac)"], P["dark"], icon_size=40)
a2 = d.card(520, Y, 240, "mysql", "Esquema MySQL (DDL)",
            ["9 tabelas em 3FN", "8 chaves estrangeiras", "CHECK · ENUM · UNIQUE", "reserva, serviço, pagamento..."], MYSQL_BLUE, icon_size=40)
a3 = d.card(880, Y, 280, "python", "Gerador de dados sintéticos",
            ["Python + Faker pt_BR · seed 42", "300 clientes · 20 quartos · 12 func.", "2.500 reservas (jan/2024 a jun/2025)", "sazonalidade e risco de cancelamento"], "#3776AB", icon_size=40)
a4 = d.card(1250, Y, 240, "mysql", "MySQL · hotel_pet",
            ["base transacional (OLTP)", "scripts 01 a 05_*.sql", "carga em lotes de 500 linhas"], MYSQL_BLUE, icon_size=40)
a5 = d.card(1640, Y, 260, "programming/flowchart/document.png", "Teste do fluxo de reserva",
            ["1. disponibilidade do quarto", "2. reserva → serviço → pagamento", "3. consulta de conferência"], P["dark"], icon_size=40)

d.arrow([(a1[0] + a1[2], 270), (a2[0], 270)], P["dark"], label="define", label_at=((a1[0] + a1[2] + a2[0]) / 2, 262), label_anchor="middle", label_color=P["dark"])
d.arrow([(a3[0] + a3[2], 270), (a4[0], 270)], "#3776AB", label="INSERTs", label_at=((a3[0] + a3[2] + a4[0]) / 2, 262), label_anchor="middle", label_color="#3776AB")
d.arrow([(a4[0] + a4[2], 270), (a5[0], 270)], MYSQL_BLUE, label="valida", label_at=((a4[0] + a4[2] + a5[0]) / 2, 262), label_anchor="middle", label_color=MYSQL_BLUE)
d.arrow([(520, a2[1] + a2[3]), (520, 410), (1250, 410), (1250, a4[1] + a4[3])], MYSQL_BLUE,
        label="cria as 9 tabelas (02_create_tables.sql)", label_at=(885, 405), label_anchor="middle", label_color=MYSQL_BLUE)
d.text(1640, a5[1] + a5[3] + 22, "database/04_test_reserva.sql", 12, P["light"])

# ---------------- Arquitetura-alvo ----------------
d.group(40, 490, 1840, 250, "", "#879196", "#FFFFFF", dash="3 4")
d.text(1864, 512, "Arquitetura-alvo do roadmap (Fases 2 a 7)  ·  pastas criadas, código ainda não implementado  ·  ambiente previsto em Docker Compose", 14, "#879196", True, anchor="end")
items = [
    ("python", "Ingestão", ["src/ingestion", "MySQL → camada Raw", "carga full e incremental"]),
    ("databricks", "Lakehouse Medallion", ["PySpark · Delta Lake", "Raw → Trusted → Refined", "star schema na Refined"]),
    ("python", "Qualidade de dados", ["Great Expectations", "schemas, nulos e limites", "bloqueia a Refined se falhar"]),
    ("python", "Modelo de no-show", ["scikit-learn", "RF · HistGB · LogReg", "métricas: F1 e ROC-AUC"]),
    ("airflow", "Orquestração", ["Apache Airflow", "DAG Medallion", "DAG de treino e inferência"]),
    ("onprem/analytics/powerbi.png", "Consumo", ["dashboards Power BI", "ou Streamlit", "alertas de ocupação"]),
]
W, G = 262, 34
x0 = 40 + (1840 - (6 * W + 5 * G)) / 2
boxes = []
for i, (ic, t, ls) in enumerate(items):
    boxes.append(planned(x0 + W / 2 + i * (W + G), 540, W, ic, t, ls))
for a, b in zip(boxes, boxes[1:]):
    y = a[1] + 55
    d.arrow([(a[0] + a[2], y), (b[0], y)], "#B8C0C2", dash="4 4")
# fonte: MySQL alimenta a ingestão (corredor vertical à esquerda do grupo implementado não é necessário:
# a seta sai da base do grupo implementado, em x do primeiro card planejado)
cx0 = boxes[0][0] + boxes[0][2] / 2
d.arrow([(1320, a4[1] + a4[3]), (1320, 470), (cx0, 470), (cx0, 540)], "#9AA5AB", dash="4 4",
        label="MySQL será a fonte da ingestão", label_at=(cx0 + 10, 464), label_color="#879196")

# ---------------- Rodapé ----------------
d.stats_box(40, 765, 1260, "Números verificáveis no repositório",
            "9 tabelas · 8 chaves estrangeiras · gerador com 300 clientes, 20 quartos, 12 funcionários e 2.500 reservas · seed 42 (reprodutível)")
lx = 1330
d.arrow([(lx, 791), (lx + 34, 791)], P["gray"])
d.text(lx + 42, 795, "fluxo implementado", 13, P["gray"], anchor="start")
d.rect(lx, 808, 34, 18, fill="#FAFAFA", stroke="#B8C0C2", sw=1.2, rx=4, dash="5 4")
d.text(lx + 42, 822, "componente planejado, ainda não implementado", 13, P["gray"], anchor="start")
d.text(1880, 860, "Projeto de portfólio · dados sintéticos · Thiago Fiel de Oliveira", 12.5, P["light"], anchor="end")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else str(HERE.parent / "arquitetura.png")
    for w in d.save(out, save_svg=False):
        print("WARNING:", w)
    print("ok", out)
