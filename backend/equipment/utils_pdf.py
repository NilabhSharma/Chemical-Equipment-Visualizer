from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO


def generate_pdf(dataset):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, height - 50, "Chemical Equipment Report")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, height - 90, f"Filename: {dataset.filename}")
    pdf.drawString(50, height - 110, f"Uploaded At: {dataset.uploaded_at}")

    y = height - 150
    summary = dataset.summary

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Summary")
    y -= 25

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Total Equipment: {summary['total_equipment']}")
    y -= 20

    averages = summary["averages"]
    pdf.drawString(50, y, f"Average Flowrate: {averages['flowrate']}")
    y -= 20
    pdf.drawString(50, y, f"Average Pressure: {averages['pressure']}")
    y -= 20
    pdf.drawString(50, y, f"Average Temperature: {averages['temperature']}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Equipment Type Distribution")
    y -= 25

    pdf.setFont("Helvetica", 11)
    for k, v in summary["type_distribution"]["raw"].items():
        pdf.drawString(70, y, f"{k}: {v}")
        y -= 18

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer
