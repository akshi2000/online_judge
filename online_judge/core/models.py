from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.CharField(max_length=100, null=True)
    institution = models.CharField(max_length=100, null=True)
    correct_submissions = models.IntegerField(default=0)
    incorrect_submissions = models.IntegerField(default=0)
    runtime_error_submissions = models.IntegerField(default=0)
    tle_submissions = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    name = models.CharField(max_length=20)
    statement = models.TextField()
    date = models.DateField(auto_now=True)
    timestamp = models.TimeField(auto_now=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=50)
    statement = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, related_name="questions")
    timelimit = models.DecimalField(max_digits=6, decimal_places=2, default=1)
    memlimit = models.IntegerField(default=128)

    def __str__(self):
        return self.name


class Testcase(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="testcases"
    )
    testcase = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question.name


class Submission(models.Model):
    submission_id = models.IntegerField(primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    ques = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="submissions"
    )
    code = models.TextField()
    lang = models.CharField(max_length=10)
    verdict = models.CharField(max_length=50, default="Submission Queued")

    def __str__(self):
        return self.submission_id
