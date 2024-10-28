from django.db import models

# Create your models here.
class PastQuestion(models.Model):
    title = models.CharField(max_length=200)
    course_code = models.CharField(max_length=10)
    academic_year = models.CharField(max_length=9)
    pdf_file = models.FileField(upload_to='past_questions/')
    uploaded_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title