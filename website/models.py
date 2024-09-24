from django.db import models
from django.utils import timezone

class Member(models.Model):
	fname = models.CharField(max_length=50)
	lname = models.CharField(max_length=50)
	email = models.EmailField(max_length=50)
	passwd = models.CharField(max_length=50)
	age = models.IntegerField()
 	
	def __str__(self):
		return self.fname + ' ' + self.lname

class Article(models.Model):
	ArticleWebsite = models.CharField(max_length=200) 
	ArticleNumber = models.IntegerField()
	ArticleName = models.CharField(max_length=200)
	ArticleURL = models.URLField()

	def __str__(self):
		return self.ArticleWebsite + ' - ' + self.ArticleName

'''class SubmissionCount(models.Model):
    #count = models.IntegerField(default=0)
    count = models.PositiveIntegerField(default=0)
    late_count = models.PositiveIntegerField(default=0)
    deadline = models.DateTimeField(default=timezone.now)'''

class SubmissionCount(models.Model):
    count = models.IntegerField(default=0)
    late_count = models.IntegerField(default=0)
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
      	return f"Total submissions: {self.count}, Late submissions: {self.late_count}"


class RegisteredEmail(models.Model):
    email = models.EmailField(unique=True)
    date_registered = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email

class User(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	mothers_email = models.EmailField(null=True, blank=True)
	fathers_email = models.EmailField(null=True, blank=True)
	def __str__(self):
		return self.username