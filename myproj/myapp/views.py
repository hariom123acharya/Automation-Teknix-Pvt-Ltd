from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import OCRResult
import pytesseract
from PIL import Image

def home(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            text = extract_image(image_file)
            OCRResult.objects.create(image=image_file, text=text)
        else:
            return HttpResponse('No image file provided')
        
        return render(request, 'result.html', {'text': text})
    return render(request, 'index.html')


def extract_image(image_file):
    img = Image.open(image_file)
    text = pytesseract.image_to_string(img)
    return text

def download_text(request):
    text = request.GET.get('text', '')
    response = HttpResponse(text, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="extracted_text.txt"'
    return response

def download_pdf(request):
    text = request.GET.get('text', '')
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, text)
    p.showPage()
    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="extracted_text.pdf"'
    return response
