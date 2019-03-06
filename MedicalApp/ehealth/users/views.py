from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, PractitionerRegisterForm, UserUpdateForm, RegularProfileUpdateForm, PractitionerProfileUpdateForm, MedicalForm
from .models import RegularProfile, PractitionerProfile, User
from .decorators import regular_required, practitioner_required
from django.views.generic import CreateView


def welcome(request):
    """WELCOME PAGE"""
    
    return render(request, 'users/welcome.html')

@login_required
def home(request):
    """HOME PAGE"""

    num = RegularProfile.objects.all().count()
    regular = RegularProfile.objects.all()
    malaria = []
    typhoid = []
    cholera = []
    fever = []
    small_pox = []
    apollo = []
    measles = []

    for i in range(num):
        if regular[i].malaria == "YES":
            malaria.append(regular[i].user)
        if regular[i].typhoid == "YES":
            typhoid.append(regular[i].user)
        if regular[i].cholera == "YES":
            cholera.append(regular[i].user)
        if regular[i].fever == "YES":
            fever.append(regular[i].user)
        if regular[i].small_pox == "YES":
            small_pox.append(regular[i].user)
        if regular[i].apollo == "YES":
            apollo.append(regular[i].user)
        if regular[i].measles == "YES":
            measles.append(regular[i].user)

    context = {
        'malaria': malaria,
        'typhoid': typhoid,
        'cholera': cholera,
        'fever': fever,
        'small_pox': small_pox,
        'apollo': apollo,
        'measles': measles
    }

    return render(request, 'users/home.html', context)

def signup(request):
    """SIGN UP PAGE WHERE USER TYPE DECISION IS MADE"""

    return render(request, 'users/signup.html')

def about(request):
    """ABOUT PAGE"""

    return render(request, 'users/about.html')

class regular_register(CreateView):
    """USER REGISTRATION PAGE"""

    model = User
    form_class = UserRegisterForm
    template_name = 'users/r_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'regular'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        login(self.request, user)
        messages.success(self.request, f'Account created for {username}!')
        return redirect('info')        

class practitioner_register(CreateView):
    """PRACTITIONER REGISTRATION PAGE"""

    model = User
    form_class = PractitionerRegisterForm
    template_name = 'users/p_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'practitioner'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        login(self.request, user)
        messages.success(self.request, f'Account created for {username}!')
        return redirect('home')        

@login_required
@regular_required
def regular_profile(request):
    """REGULAR USER PROFILE PAGE"""

    u_form = UserUpdateForm(instance=request.user)
    rp_form = RegularProfileUpdateForm(request.POST, request.FILES, instance=request.user.regularprofile)   

    context = {
        'u_form': u_form,
        'rp_form': rp_form
        }

    return render(request, 'users/r_profile.html', context)

@login_required
@practitioner_required
def practitioner_profile(request):
    """MEDICAL PRACTITIONER PROFILE PAGE"""

    try:
        profile = request.user.practitionerprofile
    except PractitionerProfile.DoesNotExist:
        profile = PractitionerProfile(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        pp_form = PractitionerProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and pp_form.is_valid():
            user = u_form.save(commit=False)
            profile = pp_form.save(commit=False)
            profile.save()
            user.save()
            messages.success(request, f'Profile successfully updated!')
            return redirect('p_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        pp_form = PractitionerProfileUpdateForm(request.POST, request.FILES, instance=profile)

    context = {
        'u_form': u_form,
        'pp_form': pp_form
        }

    return render(request, 'users/p_profile.html', context)

@login_required
@regular_required
def update_profile(request):
    """UPDATING PROFILE"""

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        rp_form = RegularProfileUpdateForm(request.POST, request.FILES, instance=request.user.regularprofile)
        if u_form.is_valid() and rp_form.is_valid():
            user = u_form.save(commit=False)
            profile = rp_form.save(commit=False)
            profile.save()
            user.save()
            messages.success(request, f'Profile successfully updated!')
            return redirect('r_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        rp_form = RegularProfileUpdateForm(instance=request.user.regularprofile)

    context = {
        'u_form': u_form, 
        'rp_form': rp_form
        }

    return render(request, 'users/update_profile.html', context)


@regular_required
def medical_info(request):
    """UPDATING MEDICAL INFORMATION"""

    try:
        profile = request.user.regularprofile
    except RegularProfile.DoesNotExist:
        profile = RegularProfile(user=request.user)
    if request.method == 'POST':
        m_form = MedicalForm(request.POST, instance=profile)
        if m_form.is_valid():
            malaria = m_form.cleaned_data.get('malaria')
            user = m_form.save(commit=False)
            user.save()
            messages.success(request, f'Medical Information successfully updated!')
            return redirect('home')
    else:
        m_form = MedicalForm(instance=profile)

    context = {
        'm_form': m_form
        }    

    return render(request, 'users/info.html', context)


def get_data(request, *args, **kwargs):
    """GETTING CHART DATA"""
    
    profile = RegularProfile.objects.all()
    num_profile = len(profile)
    items = [0, 0, 0, 0, 0, 0, 0]   
    for i in range(num_profile):
        if profile[i].malaria == "YES":
            items[0] += 1
        if profile[i].typhoid == "YES":
            items[1] += 1
        if profile[i].cholera == "YES":
            items[2] += 1
        if profile[i].fever == "YES":
            items[3] += 1
        if profile[i].small_pox == "YES":
            items[4] += 1
        if profile[i].apollo == "YES":
            items[5] += 1
        if profile[i].measles == "YES":
            items[6] += 1

    labels = ['Malaria', 'Typhoid', 'Cholera', 'Fever', 'Small Pox', 'Apollo', 'Measles']
    data = {
            "labels": labels,
            "items": items
    }
    
    return JsonResponse(data)

@practitioner_required
def table(request):
    """TABLE PAGE FOR ALL EXISTING USERS"""

    profile = User.objects.all()
    num = User.objects.all().count()
    profiles = []
    for n in range(num):
        if profile[n].is_regular == True:
            profiles.append(profile[n])

    context = { 'profile': profiles }

    return render(request, 'users/table.html', context)
