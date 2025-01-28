from django.shortcuts import get_object_or_404, render, redirect
from .models import Student,mentor,Task, TaskCompletion
from django.http import HttpResponse,JsonResponse
import pandas as pd
from math import ceil
from django.db.models import Count





def get_max_students_per_mentor():
    from math import ceil
    total_students = Student.objects.count()
    total_mentors = mentor.objects.count()
    return ceil(total_students / total_mentors) if total_mentors > 0 else 0

def devspace(request):
    if request.method == "POST":
        action = request.POST.get('action')  # Get the action from the hidden input field
        if action == "complete_task":
            web_mem_id = request.POST.get("web_mem_id")
            task_id = request.POST.get("task_id")

            student = get_object_or_404(Student, web_mem=web_mem_id)
            task = get_object_or_404(Task, id=task_id)

            if TaskCompletion.objects.filter(student=student, task=task).exists():
                return JsonResponse({"message": "Task already completed!"}, status=400)

            TaskCompletion.objects.create(student=student, task=task)
            return JsonResponse({"message": "Task marked as completed!"})

        else:
            student_id = request.POST.get('student_id')
            roll = request.POST.get('roll')
            mentor_id = request.POST.get('mentor_id')

            students = Student.objects.filter(web_mem__iexact=student_id, roll_no__iexact=roll)
            if len(students) == 0:
                return JsonResponse({"error": "Student not found"}, status=404)
            student = students[0]
            print(student)
            if student.mentor is not None:
                return JsonResponse({"error": "You cannot change your mentor! Contact Coordinator."}, status=400)

            selected_mentor = get_object_or_404(mentor, id=mentor_id)

            max_students = get_max_students_per_mentor()
            current_students = selected_mentor.mentees.count()

            if current_students >= max_students:
                return JsonResponse({"error": "This mentor has reached the maximum capacity."}, status=400)

            student.mentor = selected_mentor
            student.save()

            return JsonResponse({"message": "Mentor successfully assigned!"})

    elif request.method == "GET":
        # Handle GET requests (if applicable)
        top_members = Student.objects.order_by('-rating')[:5]
        tasks = Task.objects.all()
        print(tasks)
        max_students = get_max_students_per_mentor()
        mentors = mentor.objects.annotate(student_count=Count('mentees'))

        return render(request, 'devspace.html', {
            'top_members': top_members,
            'tasks': tasks,
            'mentors': mentors,
            'max_students': max_students
        })

    return JsonResponse({"error": "Invalid request method"}, status=405)


def assign_task(request):
    if request.method == "POST":
        mentor_id = request.POST.get('mentor_id')
        mentor_roll_no = request.POST.get('mentor_roll_no')
        task_title = request.POST.get('title')
        task_description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        assign_to_all = request.POST.get('assign_to_all') == 'on'
        print(assign_to_all)
        try:
            mentor_obj = get_object_or_404(mentor, id=mentor_id, roll_no=mentor_roll_no)
        except:
            return JsonResponse({"error": "Invalid mentor ID or roll number."}, status=400)

        task = Task.objects.create(
            title=task_title,
            description=task_description,
            due_date=due_date,
        )

        if assign_to_all:
            students = Student.objects.all()
        else:
            students = Student.objects.filter(mentor=mentor_obj)

        if not students.exists():
            return JsonResponse({"error": "No students found to assign this task."}, status=400)

        task.assigned_to.set(students)
        return JsonResponse({"message": f"Task successfully assigned to {'all students' if assign_to_all else 'your mentees'}!"})

    return render(request, 'assign_task.html')



########################### Don't Edit #####################################
def deassign_all_mentors(request):
    if request.method == "POST":
        Student.objects.update(mentor=None)
        return JsonResponse({"message": "All mentors have been deassigned from students successfully."})
    
    return JsonResponse({"error": "Invalid request method. Use POST to deassign mentors."}, status=405)


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
