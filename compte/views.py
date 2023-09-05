from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .forms import SignupForm
from .tokens import account_activation_token
from Laboratoire.models import Laboratoire
from .models import UserProfile

# Create your views here.
def gestionnaire(request):
    return render(request,'gestionnaire.html')
def signup(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():    
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            current_site = get_current_site(request)  
            mail_subject = 'Le lien d\'activation de votre compte '  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),  
                'token': account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(mail_subject, message, to=[to_email])  
            email.send()  
            return HttpResponse('Veuillez confirmer votre adresse e-mail pour finaliser l\'inscription')  
    else:  
        form = SignupForm()  
    return render(request, 'compte/inscription.html', {'form': form})  

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        messages.info(request, 'Merci pour la confirmation de votre adresse e-mail. Vous pouvez maintenant vous connecter à votre compte.') 
        return redirect('connexion') 
    else:  
        return HttpResponse('Le lien d\'activation est invalide !')


def accesPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                user_profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                user_profile = None

            if user_profile is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect('accueil')
                elif user_profile.role == 'gestionnaire':
                    login(request, user)
                    return redirect('gestionnaire')
                elif user_profile.role == 'visiteur':
                    login(request, user)
                    return redirect('accueil_visiteur')
            else:
                messages.error(request, "Utilisateur et/ou mot de passe incorrect(s)")
                return redirect('connexion')
        else:
            messages.error(request, "Utilisateur et/ou mot de passe incorrect(s)")
            return redirect('connexion')
    return render(request, 'compte/connexion.html')


def equipement(request):
    laboratoires = Laboratoire.objects.all()
    context = {
        'laboratoires': laboratoires
    }

    return render(request, 'equipement.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/')