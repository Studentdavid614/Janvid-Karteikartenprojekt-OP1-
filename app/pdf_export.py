from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from typing import List

try:
    from .models import Card, CardSet
except ImportError:
    try:
        from app.models import Card, CardSet
    except ImportError:
        from models import Card, CardSet


def generate_pdf(card_set: CardSet, cards: List[Card]) -> BytesIO:
    """Generate a PDF from a card set."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#FFB800'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#FFB800'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6
    )
    
    elements = []
    
    # Add title
    title = Paragraph(card_set.name, title_style)
    elements.append(title)
    
    if card_set.description:
        desc = Paragraph(f"<b>Beschreibung:</b> {card_set.description}", normal_style)
        elements.append(desc)
        elements.append(Spacer(1, 0.2*inch))
    
    # Add cards
    for idx, card in enumerate(cards, 1):
        # Card number and front
        front_para = Paragraph(
            f"<b>Frage {idx}:</b> {card.front}",
            heading_style
        )
        elements.append(front_para)
        
        # Answer
        back_para = Paragraph(
            f"<b>Antwort:</b> {card.back}",
            normal_style
        )
        elements.append(back_para)
        
        # Spacing between cards
        elements.append(Spacer(1, 0.1*inch))
        
        # Page break every 4 cards
        if idx % 4 == 0 and idx < len(cards):
            elements.append(PageBreak())
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
