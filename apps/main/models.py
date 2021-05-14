from django.db import models
from ..login_app.models import User
from datetime import date

# Create your models here.
class ChangeManager(models.Manager):
    def registerVal(self, postData):
        results = {'status': True, 'errors': [], 'user': None}
        return results

    def createChange(self, postData, user, fileURL):
        # Defaults
        status = 'new'

        from datetime import date
        today = date.today()
        entryDate = today.strftime("%Y-%m-%d")
        

        change = Change.objects.create(
			status = status, 
			requestType = postData['requestType'], 
			environment = postData['environment'],
            requestor = user,
            assignee = None,
            entryDate = entryDate,
            targetDate = postData['targetDate'],
            shortDescription = postData['shortDescription'],
            longDescription = postData['longDescription'],
            changeImpact = postData['changeImpact'],
            fileUpload = fileURL,
			)
        return change

class Change(models.Model):
    STATUS = (
        ('new', "New"),
        ('in_progress', "In Progress"),
        ("done", "Done"),
        ("cancelled", "Cancelled"),
    )
    status = models.CharField(max_length=20, choices=STATUS, verbose_name='Status')
    TYPE = (
        ('database', 'Database'),
        ('microsoft-365', 'Microsoft 365'),
        ('customer-platform', 'Customer Platform'),
        ('power-bi', 'Power BI'),
        ('wordpress-site', 'WordPress Site'),
    )
    requestType = models.CharField(max_length=20, choices=TYPE, verbose_name='Request Type')
    ENVIRONMENT = (
        ('development', 'Development'),
        ('test', 'Testing'),
        ('production', 'Production'),
    )
    environment = models.CharField(max_length=20, choices=ENVIRONMENT, verbose_name='Environment')
    requestor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Requestor', related_name="Requestor")
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Assignee', related_name="Assignee", blank=True, null=True)
    entryDate = models.DateField(verbose_name='Entry Date')
    targetDate = models.DateField(verbose_name='Target End Date')
    shortDescription = models.CharField(max_length = 50, verbose_name='Short Description')
    longDescription = models.CharField(max_length = 250, verbose_name='Long Description')
    changeImpact = models.CharField(max_length = 250, verbose_name='Change Impact')
    fileUpload = models.FileField(upload_to ='supplemental', blank=True, null=True, verbose_name='File Upload')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ChangeManager()

    @property
    def daysLeft(self):
        today = date.today()
        result = self.targetDate - today
        return result.days

    def __str__(self):
        return self.shortDescription