from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from django.http import HttpResponse
from datetime import date
from decimal import Decimal


def generate_invoice(order):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("<b>INVOICE</b>", styles['Title']))
    elements.append(Spacer(1, 12))

    # Company Info
    elements.append(Paragraph("<b>INVOYGER</b>", styles['Normal']))
    elements.append(Paragraph("Billing System Project", styles['Normal']))
    elements.append(Paragraph("Email: support@invoyger.com", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Customer Info
    elements.append(Paragraph(f"<b>Invoice ID:</b> {order.id}", styles['Normal']))
    elements.append(Paragraph(f"<b>Date:</b> {date.today()}", styles['Normal']))
    elements.append(Paragraph(f"<b>Customer:</b> {order.user.username}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Table
    data = [
        ["Product", "Qty", "Price", "Total"]
    ]

    total_amount = 0
    for item in order.items.all():
        total = item.quantity * item.price
        total_amount += total
        data.append([
            item.product.name,
            item.quantity,
            f"₹{item.price}",
            f"₹{total}"
        ])

    table = Table(data, colWidths=[180, 60, 80, 80])
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # Summary
    gst = total_amount * Decimal('0.18')
    grand_total = total_amount + gst

    elements.append(Paragraph(f"<b>Subtotal:</b> ₹{total_amount}", styles['Normal']))
    elements.append(Paragraph(f"<b>GST (18%):</b> ₹{gst:.2f}", styles['Normal']))
    elements.append(Paragraph(f"<b>Grand Total:</b> ₹{grand_total:.2f}", styles['Normal']))

    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Thank you for shopping with us!", styles['Italic']))

    doc.build(elements)
    return response
