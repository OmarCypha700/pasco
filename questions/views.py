import os
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_list_or_404, render, redirect, get_object_or_404
from .models import PastQuestion
from django.contrib.auth.decorators import login_required, permission_required

import zipfile
# Create your views here.

@login_required(login_url='/auth/login')
def question_list(request):
    questions = PastQuestion.objects.all()
    return render(request, 'questions/question_list.html', {'questions': questions})

def upload_question(request):
    if request.method == 'POST':
        title = request.POST.get('title') 
        course_code = request.POST.get('course_code')
        academic_year = request.POST.get('academic_year')
        pdf_file = request.FILES.get('file') 

        # Create a new PastQuestion instance and save it to the database
        past_question = PastQuestion(title=title, course_code=course_code, academic_year=academic_year, pdf_file=pdf_file)
        past_question.save()

        # Redirect to the question list page after successful upload
        return redirect('question_list')
    
    # For GET requests, render the upload form
    return render(request, 'questions/upload_question.html')


def view_question(request, question_id):
    question = get_object_or_404(PastQuestion, pk=question_id)
    file_path = question.pdf_file.path
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

def download_question(request, question_id):
    question = get_object_or_404(PastQuestion, pk=question_id)
    file_path = question.pdf_file.path
    
    try:
        # Open the PDF file in binary mode
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        # Set Content-Disposition header to force download
        response['Content-Disposition'] = f'attachment; filename="{question.title}_{question.course_code}.pdf"'
        return response
    except FileNotFoundError:
        raise Http404("File not found")
    

def download_multiple_questions(request):
    if request.method == 'POST':
        # Get the selected question IDs from the form
        question_ids = request.POST.getlist('question_ids[]')  # Expecting an array of ids

        if not question_ids:
            # No files were selected
            return HttpResponse("No files selected for download.")

        # Retrieve the selected past questions
        questions = get_list_or_404(PastQuestion, pk__in=question_ids)

        # Create a temporary zip file in memory
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="past_questions.zip"'

        with zipfile.ZipFile(response, 'w') as zip_file:
            for question in questions:
                # Get the file path of the PDF
                file_path = question.pdf_file.path
                if os.path.exists(file_path):
                    # Add the file to the zip archive
                    zip_file.write(file_path, os.path.basename(file_path))
                else:
                    raise Http404(f"File for '{question.title}' not found")

        return response



def delete(request, question_id):
    PastQuestion.objects.get(pk=question_id).delete()
    return redirect('question_list')