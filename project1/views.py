from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def home(request):
    #return HttpResponse("hello world ! you are at the home page.")
    return render(request,'website/index.html')

def about(request):
    return render(request,'website/about.html')

def contact(request):
    return render(request, 'website/contact.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account is ready. You can now place an order.')
            return redirect('coffee')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
