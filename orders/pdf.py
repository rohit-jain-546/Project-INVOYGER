from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.http import HttpResponse
from django.conf import settings
from datetime import date
import os
from decimal import Decimal


font_dir = os.path.join(settings.BASE_DIR, "static/fonts")

pdfmetrics.registerFont(TTFont("DejaVu", os.path.join(font_dir, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", os.path.join(font_dir, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Oblique", os.path.join(font_dir, "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-BoldOblique", os.path.join(font_dir, "DejaVuSans-BoldOblique.ttf")))

pdfmetrics.registerFontFamily(
    "DejaVu",
    normal="DejaVu",
    bold="DejaVu-Bold",
    italic="DejaVu-Oblique",
    boldItalic="DejaVu-BoldOblique"
)



def generate_invoice(order):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.order_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    
    title_style = ParagraphStyle(
        name="Title",
        fontName="DejaVu",
        fontSize=20,
        alignment=1,
        spaceAfter=18
    )

    header_style = ParagraphStyle(
        name="Header",
        fontName="DejaVu",
        fontSize=12,
        textColor=colors.white
    )

    normal_style = ParagraphStyle(
        name="Normal",
        fontName="DejaVu",
        fontSize=10
    )

    bold_style = ParagraphStyle(
        name="Bold",
        fontName="DejaVu",
        fontSize=10
    )

    
    header = Table([[Paragraph("<b>INVOYGER</b>", header_style)]], colWidths=[520])
    header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#232F3E")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(header)
    elements.append(Spacer(1, 18))

    
    elements.append(Paragraph("<b>Order Invoice</b>", title_style))

    
    info_data = [
        [Paragraph(f"<b>Order ID:</b> {order.order_id}", normal_style),
         Paragraph(f"<b>Date:</b> {date.today()}", normal_style)],

        [Paragraph(f"<b>Customer:</b> {order.user.username}", normal_style),
         Paragraph("<b>Status:</b> Confirmed", normal_style)]
    ]

    info_table = Table(info_data, colWidths=[260, 260])
    elements.append(info_table)
    elements.append(Spacer(1, 20))

    
    data = [["Product", "Qty", "Price", "Amount"]]
    total_amount = 0

    for item in order.items.all():
        total = item.quantity * item.price
        total_amount += total

        data.append([
            Paragraph(item.product.name, normal_style),
            str(item.quantity),
            f"₹ {item.price:.2f}",
            f"₹ {total:.2f}"
        ])

    table = Table(data, colWidths=[250, 70, 100, 100])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EAEAEA")),
        ('GRID', (0,0), (-1,-1), 0.25, colors.grey),

        ('FONTNAME', (0,0), (-1,-1), 'DejaVu'),
        ('ALIGN', (0,1), (0,-1), 'LEFT'),
        ('ALIGN', (1,1), (1,-1), 'CENTER'),
        ('ALIGN', (2,1), (3,-1), 'RIGHT'),

        ('LEFTPADDING', (0,1), (0,-1), 10),
        ('RIGHTPADDING', (2,1), (3,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 25))

    
    gst = total_amount *  Decimal('0.18')
    grand_total = total_amount + gst

    total_table = Table([
        ["Subtotal", f"₹ {total_amount:.2f}"],
        ["GST (18%)", f"₹ {gst:.2f}"],
        ["Grand Total", f"₹ {grand_total:.2f}"]
    ], colWidths=[350, 170])

    total_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'DejaVu'),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),

        ('LINEABOVE', (0,2), (-1,2), 1.5, colors.black),
        ('FONTSIZE', (0,2), (-1,2), 12),

        ('TOPPADDING', (0,2), (-1,2), 10),
        ('BOTTOMPADDING', (0,2), (-1,2), 10),
    ]))

    elements.append(total_table)
    elements.append(Spacer(1, 35))

    
    elements.append(Paragraph("Thank you for shopping with INVOYGER!", normal_style))

    doc.build(elements)
    return response
