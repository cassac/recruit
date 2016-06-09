from django.shortcuts import render
from .forms import UserApplyForm

def apply(request):
	form = UserApplyForm()
	context = {
		'form': form,
	}
	return render(request, 'candidates/apply.html',
		context)