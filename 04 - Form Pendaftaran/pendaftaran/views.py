from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from utils.parsing import parsing_noHp

from .forms import SignUpForm, LoginForm

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'
    extra_context = {
        'page_title': 'Form Pendaftaran',
    }

class SignUpFormView(FormView):
    form_class = SignUpForm
    template_name = 'pendaftaran/signup.html'
    extra_context = {
        'page_title': 'Sign Up',
        'form_signup': form_class
    }
    success_url = reverse_lazy('pendaftaran:login')

    def post(self, request, *args, **kwargs):
        # mengambil form dan mengecek validasi nya
        form = self.get_form()
        if form.is_valid():
            # membuat record user di table user
            # parsing no hp
            noHp = parsing_noHp(request.POST['noHp'])
            password = request.POST['password']
            email = request.POST['email']

            User.objects.create_user(noHp, email, password)
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def loginView(request):
    form_class = LoginForm(request.POST or None)
    error = None

    if request.method == 'POST':
        if form_class.is_valid():
            # parsing no hp
            inputNoHp = parsing_noHp(request.POST['noHp'])
            inputPassword = request.POST['password']
            user = authenticate(request, username=inputNoHp, password=inputPassword)

            if user is not None:
                login(request, user)
                # redirect to dashboard if login
                return redirect('dashboard:index')

            else:
                error = 'No hp belum terdaftar atau password salah'

    context = {
        'page_title': 'Login',
        'form_login': form_class,
        'error': error,
    }
    return render(request, 'pendaftaran/login.html', context)
