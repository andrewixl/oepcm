# URL Management Imports
from django.shortcuts import render, redirect
# Site Messages Import
from django.contrib import messages
# Model Imports
from .models import Change
from ..login_app.models import User
# Advanced Django Queries
from django.db.models import Q
# Dates
from datetime import date, datetime

############################################################################################

def genErrors(request, Emessages):
	for message in Emessages:
		messages.warning(request, message)

def checkLogin(request):
	try:
		if request.session['email']:
			return True
		else:
			return False
	except:
		return False
def checkActive(request):
	try:
		if request.session['active']:
			return True
		else:
			return False
	except:
		return False

############################################################################################

def index(request):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	if results[1] == False:
		return redirect('/account-suspended')

	changes = Change.objects.filter().all()	
	active_changes = Change.objects.filter(Q(status = 'in_progress') | Q(status = 'new'))
	active_changes_num = Change.objects.filter(Q(status = 'in_progress') | Q(status = 'new')).count()

	past_due_changes = 0
	for change in active_changes:
		if change.daysLeft < 0:
			past_due_changes += 1
	
	latest_changes = Change.objects.filter(Q(status = 'in_progress') | Q(status = 'new')).order_by('-updated_at')[:5]


	context = {
		"page": "index",
		"active_changes": active_changes_num,
		"past_due_changes": past_due_changes,
		"changes": changes,
		"latest_changes": latest_changes
	}
	return render( request, 'main/index.html', context)

############################################################################################

def myRequests(request):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	if results[1] == False:
		return redirect('/account-suspended')
	user = User.objects.get(id = request.session['user_id'])
	active_changes = Change.objects.filter(requestor = user).filter(Q(status = 'in_progress') | Q(status = 'new'))
	past_changes = Change.objects.filter(requestor = user).filter(Q(status = 'cancelled') | Q(status = 'done'))
	context = {
		'page': 'my-requests',
		'active_changes': active_changes,
		'past_changes': past_changes,
	}
	return render( request, 'main/my-requests.html', context)

############################################################################################

def requestChange(request):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	if results[1] == False:
		return redirect('/account-suspended')

	# Getting Requestor
	user = User.objects.get(id = request.session['user_id'])

	# Getting Entry Date
	from datetime import date
	today = date.today()
	today = today.strftime("%Y-%m-%d")

	context = {
	'page': 'request-change',
	'user': user,
	'today': today,
	'types': Change.TYPE,
	'enviornments': Change.ENVIRONMENT,
	}
	return render( request, 'main/request-change.html', context)

from django.core.files.storage import FileSystemStorage
def changeCreation(request):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	if results[1] == False:
		return redirect('/account-suspended')
	
	try:
		request.FILES['fileUpload']
	except:
		request.FILES['fileUpload'] = None

	fs = FileSystemStorage()
	uploaded_file_url = fs.url("")
	if request.FILES['fileUpload'] != None:
		myfile = request.FILES['fileUpload']
		fs = FileSystemStorage()
		filename = fs.save('supplemental/' + myfile.name, myfile)
		uploaded_file_url = fs.url(filename)

	user = User.objects.get(id = request.session['user_id'])
	change = Change.objects.createChange(request.POST, user, uploaded_file_url)
	messages.success(request, "Change <a href='/change/req" + str(change.id) + "'>REQ" + str(change.id) + "</a> Has Been Created." )
	return redirect("/my-requests")

############################################################################################

def assignedMe(request):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	if results[1] == False:
		return redirect('/account-suspended')
	user = User.objects.get(id = request.session['user_id'])
	active_changes = Change.objects.filter(assignee = user).filter(Q(status = 'in_progress') | Q(status = 'new'))
	past_changes = Change.objects.filter(assignee = user).filter(Q(status = 'cancelled') | Q(status = 'done'))
	context = {
		'page': 'assigned-me',
		'active_changes': active_changes,
		'past_changes': past_changes,
	}
	return render( request, 'main/assigned-me.html', context)

############################################################################################

def activeChanges(request):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	if results[1] == False:
		return redirect('/account-suspended')
	changes = Change.objects.filter(Q(status = 'in_progress') | Q(status = 'new'))
	context = {
	"page": "active-changes",
	"types": Change.TYPE,
	"changes": changes,
	}
	return render( request, 'main/active-changes.html', context)

############################################################################################

def pastChanges(request):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	if results[1] == False:
		return redirect('/account-suspended')
	changes = Change.objects.filter(Q(status = 'cancelled') | Q(status = 'done'))
	context = {
	"page": "past-changes",
	"types": Change.TYPE,
	"changes": changes,
	}
	return render( request, 'main/past-Changes.html', context)

############################################################################################

def viewChange(request, id):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	if results[1] == False:
		return redirect('/account-suspended')

	# Get Change
	change = Change.objects.get(id = id)

	users = User.objects.filter().all()

	print(change.assignee)

	context = {
	'change': change,
	'statuses': Change.STATUS,
	'types': Change.TYPE,
	'environments': Change.ENVIRONMENT,
	'users': users,
	}
	return render( request, 'main/view-change.html', context)

def updateChange(request, id):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	if results[1] == False:
		return redirect('/account-suspended')
	
	change = Change.objects.get(id = id)

	change.status = request.POST['status']
	change.targetDate = request.POST['targetDate'] 
	change.requestType = request.POST['requestType'] 
	change.environment = request.POST['environment']
	if request.POST['assignee'] == "None":
		change.assignee = None
	else:
		user = User.objects.get(id = request.POST['assignee'])
		change.assignee = user 
	change.shortDescription = request.POST['shortDescription'] 
	change.longDescription = request.POST['longDescription'] 
	change.changeImpact = request.POST['changeImpact'] 
	# change.fileUpload = 
	change.updated_at = datetime.now()
	change.save()

	messages.success(request, 'REQ' + str(change.id) + " Was Successfully Updated")

	return redirect("/change/req" + id)

def deleteChange(request, id):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	if results[1] == False:
		return redirect('/account-suspended')
	Change.objects.filter(id = id).delete()
	messages.success(request, 'REQ' + str(id) + " Was Successfully Deleted")
	return redirect("/")

############################################################################################

def error500(request):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	if results[1] == False:
		return redirect('/account-suspended')
	return render( request, 'main/500.html')

############################################################################################

def error403(request):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	# if results[1] == False:
	# 	return redirect('/account-suspended')
	return render( request, 'main/pages-403.html')

############################################################################################

from django.template import RequestContext

# HTTP Error 404
def error404(request, exception):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	if results[1] == False:
		return redirect('/account-suspended')

	data = {}
	return render(request,'main/404.html', data)

############################################################################################

def statusPage(request):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	if results[1] == False:
		return redirect('/account-suspended')
	return render( request, 'main/status-page.html')

############################################################################################

def accountManagement(request):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	if results[1] == False:
		return redirect('/account-suspended')
	return render( request, 'main/account-management.html')

def updateAccountInfo(request):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	if results[1] == False:
		return redirect('/account-suspended')

	user = User.objects.get(id = request.session['user_id'])
	user.firstName = request.POST['firstName']
	user.lastName = request.POST['lastName']
	user.email = request.POST['email']
	user.save()
	request.session['firstName'] = user.firstName
	request.session['lastName'] = user.lastName
	request.session['email'] = user.email
	messages.success(request, "Your Account Info has Been Updated.")
	return render( request, 'main/account-management.html')

def updatePassword(request):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	if results[1] == False:
		return redirect('/account-suspended')

	results = User.objects.changePassword(request.POST, request.session['user_id'])
	if results['status'] == False:
		print("THERE IS AN ERROR")
		genErrors(request, results['errors'])
		return redirect('/account#password')
	messages.success(request, "Your Password has Been Successfully Updated.")
	return redirect('/account')

############################################################################################

from json import dumps
from django.http import JsonResponse, HttpResponse
  
def data(request):
	
	today = date.today()
	year = today.strftime("%Y")
	# print(today)
	success = []
	for i in range(1,13):
		success.append(Change.objects.filter(entryDate__year = year, entryDate__month = i, status="done").count())
	in_progress = []
	for i in range(1,13):
		in_progress.append(Change.objects.filter(entryDate__year = year, entryDate__month = i, status="in_progress").count())
	failure = []
	for i in range(1,13):
		failure.append(Change.objects.filter(entryDate__year = year, entryDate__month = i, status="cancelled").count())
    # create data dictionary
	dataDictionary = {
        "success": success,
		"in_progress": in_progress,
        "failure": failure,
    }
	return JsonResponse(dataDictionary)