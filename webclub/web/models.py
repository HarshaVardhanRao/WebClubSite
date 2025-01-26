from django.db import models
class mentor(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=12)
    github_user = models.CharField(max_length=58,default="Username")
    DEPT_CHOICES = [
        ("CSE","CSE"),("CAI","CAI"),("CSD","CSD"),("CSM","CSM"),("CSC","CSC"),("CST","CST"),("ECE","ECE"),("EEE","EEE"),("CE","CE"),("ME","ME")
    ]
    mentor_dept= models.CharField(max_length=20, choices=DEPT_CHOICES, default="CSE")
    mentor_id = models.CharField(max_length=20, default="Mentor ID")
    year = models.IntegerField(default=3)

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=12)
    leetcode_user = models.CharField(max_length=58,default="Username")
    DEPT_CHOICES = [
        ("CSE","CSE"),("CAI","CAI"),("CSD","CSD"),("CSM","CSM"),("CSC","CSC"),("CST","CST"),("ECE","ECE"),("EEE","EEE"),("CE","CE"),("ME","ME")
    ]
    dept= models.CharField(max_length=20, choices=DEPT_CHOICES, default="CSE")
    year = models.IntegerField(default=3)
    github_link = models.URLField(blank=True,null=True)
    web_mem = models.CharField(max_length=20)
    rank = models.IntegerField(default=1)
    rating = models.FloatField(default=0.00)
    project_score = models.FloatField(default=0.0)
    mentor = models.ForeignKey('mentor', on_delete=models.SET_NULL, null=True, blank=True, related_name='mentees')
    def __str__(self):
        return self.name
    def type(self):
        return "student"
    def save(self, *args, **kwargs):
        first_two_digits = self.roll_no[:2]
        last_four_digits = self.roll_no[-4:]
        section_char = 'H' if self.roll_no[4] == '1' else 'M'

        self.web_mem = f"{first_two_digits}WEB{section_char}{last_four_digits}"
        self.rating = round((self.rank * 100) + (self.project_score), 2)

        

        super().save(*args, **kwargs)


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    # Optional: Assign tasks to specific students or groups
    assigned_to = models.ManyToManyField('Student', blank=True)

    def __str__(self):
        return self.title

class TaskCompletion(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    completion_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} completed {self.task}"