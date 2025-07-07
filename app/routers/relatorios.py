from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.database import get_connection
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
from datetime import datetime

router = APIRouter(prefix="/v1/relatorios")

@router.get("/estoque/pdf")
def gerar_relatorio_pdf():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, codigo, descricao FROM produtos")
            produtos = cur.fetchall()

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    title = Paragraph("Relatório de Estoque", styles['Title'])
    date = Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal'])
    elements.extend([title, date, Spacer(1, 12)])

    data = [["ID", "Código", "Descrição"]]
    for prod in produtos:
        data.append([str(prod[0]), prod[1], prod[2]])

    table = Table(data, colWidths=[20*mm, 40*mm, 100*mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(table)
    doc.build(elements)
    return FileResponse(path=temp_file.name, filename="relatorio_estoque.pdf", media_type="application/pdf")
