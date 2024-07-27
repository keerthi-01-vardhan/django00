from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import StudentForm
from .models import Student
import csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.core.files.storage import FileSystemStorage

def index(request):
    form = StudentForm()
    return render(request, 'enrollment/index.html', {'form': form})

@csrf_exempt
def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'invalid method'})

def generate_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email', 'Phone Number', 'Date of Birth'])

    students = Student.objects.all().values_list('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth')
    for student in students:
        writer.writerow(student)

    return response

def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, "List of Students")
    
    students = Student.objects.all()
    y = 750
    for student in students:
        p.drawString(100, y, f"{student.first_name} {student.last_name} - {student.email}")
        y -= 20

    p.showPage()
    p.save()
    return response



