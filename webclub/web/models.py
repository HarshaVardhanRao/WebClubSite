from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=12)
    leetcode_user = models.CharField(max_length=58,default="Username")
    DEPT_CHOICES = [
        ("CSE","CSE"),("CAI","CAI"),("CSD","CSD"),("CSM","CSM"),("CSC","CSC"),("CST","CST"),("ECE","ECE"),("EEE","EEE"),("CE","CE"),("ME","ME")
    ]
    SECTION_CHOICES = [
        ("A","A"),("B","B"),("C","C"),("D","D"),("E","E"),("F","F"),("G","G"),("H","H"),("I","I"),("J","J"),
    ]
    dept= models.CharField(max_length=20, choices=DEPT_CHOICES, default="CSE")
    section = models.CharField(max_length=10,choices=SECTION_CHOICES, default="A")
    year = models.IntegerField(default=3)
    github_link = models.URLField(blank=True,null=True)
    web_mem = models.CharField(max_length=20)
    rank = models.IntegerField(default=1)
    rating = models.FloatField(default=0.00)
    def __str__(self):
        return self.name
    def type(self):
        return "student"
    def save(self, *args, **kwargs):
        first_two_digits = self.roll_no[:2]
        last_four_digits = self.roll_no[-4:]
        section_char = 'H' if self.roll_no[4] == '1' else 'M'

        self.web_mem = f"{first_two_digits}WEB{section_char}{last_four_digits}"

        super().save(*args, **kwargs)

class mentor(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=12)
    github_user = models.CharField(max_length=58,default="Username")
    DEPT_CHOICES = [
        ("CSE","CSE"),("CAI","CAI"),("CSD","CSD"),("CSM","CSM"),("CSC","CSC"),("CST","CST"),("ECE","ECE"),("EEE","EEE"),("CE","CE"),("ME","ME")
    ]
    mentor_dept= models.CharField(max_length=20, choices=DEPT_CHOICES, default="CSE")
    year = models.IntegerField(default=3)