from django.shortcuts import get_object_or_404, render, redirect
from .models import Student,mentor,Task, TaskCompletion
from django.http import HttpResponse,JsonResponse
import pandas as pd
def index(request):
    mentors = mentor.objects.all()
    return render(request, 'index.html', {'mentors': mentors})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def leaderboard(request):
    try:
        top_members = Student.objects.order_by('-rating')[:]
    except IndexError:
        top_members = []
    return render(request, 'leaderboard.html', {'top_members': top_members})




from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from .models import Student, Task, TaskCompletion

def complete_task(request):
    if request.method == "POST":
        web_mem_id = request.POST.get("web_mem_id")
        task_id = request.POST.get("task_id")

        student = get_object_or_404(Student, web_mem=web_mem_id)
        task = get_object_or_404(Task, id=task_id)

        # Check if already completed
        if TaskCompletion.objects.filter(student=student, task=task).exists():
            return JsonResponse({"message": "Task already completed!"}, status=400)

        # Save the completion
        TaskCompletion.objects.create(student=student, task=task)
        return JsonResponse({"message": "Task marked as completed!"})
    
    # Fetch tasks for the context
    tasks = Task.objects.all()
    return render(request, 'tasks.html', {'tasks': tasks})



def upload_students(request):
    if request.method == "POST":
        excel_file = request.FILES.get("file")
        if not excel_file:
            return HttpResponse("Please upload an Excel file", status=400)
        
        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            return HttpResponse(f"Error reading the file: {e}", status=400)

        required_columns = {"FULL NAME", "ROLL NUMBER", "YEAR", "DEPARTMENT"}
        if not required_columns.issubset(df.columns):
            return HttpResponse(f"Missing required columns: {required_columns}", status=400)

        year_mapping = {
            "I": 1,
            "II": 2,
            "III": 3,
            "IV": 4
        }

        for _, row in df.iterrows():
            roll_no = row["ROLL NUMBER"]
            first_two_digits = str(roll_no)[:2]
            last_four_digits = str(roll_no)[-4:]
            section_char = 'H' if str(roll_no)[4] == '1' else 'M'
            web_mem = f"{first_two_digits}WEB{section_char}{last_four_digits}"

            year = year_mapping.get(row["YEAR"], None)
            if year is None:
                return HttpResponse(f"Invalid Year value in row {row.name + 1}: {row['YEAR']}", status=400)

            Student.objects.create(
                name=row["FULL NAME"],
                roll_no=row["ROLL NUMBER"],
                year=year,
                dept=row["DEPARTMENT"],
                web_mem=web_mem,
            )

        return HttpResponse("Students uploaded successfully!")

    return render(request, "upload_students.html")
