import io
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def generate_completion_certificate(student_name: str, course_name: str, issue_date: str) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Decorative Border
    c.setStrokeColor(colors.HexColor("#7c3aed"))
    c.setLineWidth(5)
    c.rect(20, 20, width - 40, height - 40)
    
    c.setStrokeColor(colors.HexColor("#f59e0b"))
    c.setLineWidth(2)
    c.rect(26, 26, width - 52, height - 52)

    # Header
    c.setFont("Helvetica-Bold", 32)
    c.setFillColor(colors.HexColor("#4c1d95"))
    c.drawCentredString(width / 2, height - 100, "SIR ABDULLAH ACADEMY")

    c.setFont("Helvetica", 14)
    c.setFillColor(colors.HexColor("#64748b"))
    c.drawCentredString(width / 2, height - 130, "Certificate of Completion")

    # Body
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.HexColor("#0f172a"))
    c.drawCentredString(width / 2, height - 200, "This is to certify that")

    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(colors.HexColor("#7c3aed"))
    c.drawCentredString(width / 2, height - 240, student_name)

    c.setFont("Helvetica", 12)
    c.setFillColor(colors.HexColor("#0f172a"))
    c.drawCentredString(width / 2, height - 280, f"has successfully completed all requirements for the course")

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor("#1e1b4b"))
    c.drawCentredString(width / 2, height - 315, course_name)

    # Footer Signatures
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#64748b"))
    c.drawString(100, 80, f"Date Issued: {issue_date}")
    
    c.setStrokeColor(colors.HexColor("#0f172a"))
    c.setLineWidth(1)
    c.line(width - 250, 95, width - 100, 95)
    c.drawCentredString(width - 175, 80, "Sir Abdullah (Founder & Head Instructor)")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
