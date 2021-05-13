# URL Management Imports
from django.shortcuts import render, redirect
# Site Messages Import
from django.contrib import messages
# Model Imports
from .models import Change
from ..login_app.models import User
# Advanced Django Queries
from django.db.models import Q

############################################################################################

def genErrors(request, Emessages):
	for message in Emessages:
		messages.error(request, message)

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
	active_changes = Change.objects.filter().all().count()

	past_due_changes = 0
	for change in changes:
		if change.daysLeft < 0:
			past_due_changes += 1


	context = {
		"page": "index",
		"active_changes": active_changes,
		"past_due_changes": past_due_changes,
		"changes": changes,
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
	'enviornments': Change.ENVIORNMENT,
	}
	return render( request, 'main/request-change.html', context)

def changeCreation(request):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	if results[1] == False:
		return redirect('/account-suspended')
	user = User.objects.get(id = request.session['user_id'])
	change = Change.objects.createChange(request.POST, user)
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

	context = {
	'change': change,
	'types': Change.TYPE,
	}
	return render( request, 'main/view-change.html', context)

############################################################################################

def error500(request):
	results = []
	results.append(checkLogin(request))
	results.append(checkActive(request))
	if results[0] == False:
		return redirect('/login')
	if results[1] == False:
		return redirect('/account-suspended')
	return render( request, 'main/pages-500.html')

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