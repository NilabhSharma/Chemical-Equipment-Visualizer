from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import EquipmentDataset

import io

from .models import EquipmentDataset
from .serializers import EquipmentDatasetSerializer, CSVUploadSerializer
from .utils import analyze_csv
from django.http import FileResponse
from .utils_pdf import generate_pdf
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


class UploadCSVView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CSVUploadSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {"message": "Upload CSV using POST request with a file field named 'file'"},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        file = serializer.validated_data["file"]

        try:
            summary, data = analyze_csv(file)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        EquipmentDataset.objects.create(
            filename=file.name,
            summary=summary
        )

        if EquipmentDataset.objects.count() > 5:
            EquipmentDataset.objects.order_by("uploaded_at").first().delete()

        return Response(
            {"summary": summary, "data": data},
            status=status.HTTP_201_CREATED
        )




class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        datasets = EquipmentDataset.objects.order_by("-uploaded_at")[:5]
        serializer = EquipmentDatasetSerializer(datasets, many=True)
        return Response(serializer.data)
class HomeView(APIView):
    def get(self, request):
        return Response({
            "message": "Chemical Equipment Visualizer API",
            "endpoints": {
                "upload_csv": "/api/upload/",
                "history": "/api/history/"
            }
        })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_report(request, dataset_id):
    try:
        dataset = EquipmentDataset.objects.get(id=dataset_id)
    except EquipmentDataset.DoesNotExist:
        return HttpResponse(
            "Dataset not found", status=404
        )

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    y = 800
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Dataset Report")
    y -= 40

    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Filename: {dataset.filename}")
    y -= 25
    p.drawString(50, y, f"Uploaded: {dataset.uploaded_at}")
    y -= 40

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Summary Statistics")
    y -= 25

    p.setFont("Helvetica", 11)
    for key, value in dataset.summary.items():
        p.drawString(70, y, f"{key}: {value}")
        y -= 20
        if y < 100:
            p.showPage()
            y = 800

    p.save()
    buffer.seek(0)

    return HttpResponse(
        buffer,
        content_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="report_{dataset_id}.pdf"'}
    )

