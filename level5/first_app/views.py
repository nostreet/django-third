from django.shortcuts import render
from first_app.forms import UserProfileInfoForm, UserForm

#Login stuff
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
#simply add @login_required to make a view login required
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'first_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in, nice!")
    # return render(request, 'first_app/special.html')

#so that a person can only logout if he's logeed in!
@login_required
def user_logout(request):
    logout(request)
    #logs them right away out and redirects to index
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user # OneTo One relationship

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors,  profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'first_app/register.html',
            {
            'user_form':user_form,
            'profile_form':profile_form,
            'registered':registered,
            })

# login

def user_login(request):
    if request.method == 'POST':
        # username and pw supply with varibles from the html file
        username = request.POST.get('username')
        password = request.POST.get('password')
        #authenticates the user with oneliner from django
        user = authenticate(username = username, password = password)

        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                print("im here now")
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("failed")
            return HttpResponse("invalid login details supplied")
