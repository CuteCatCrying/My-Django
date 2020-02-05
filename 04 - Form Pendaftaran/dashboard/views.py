from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import FormView, ListView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count

from .forms import ProfileForm, NotificationForm
from .models import Notification
from pendaftaran.models import SignUp
from utils.parsing import parsing_noHp


def notification_context(request):
    user_id = request.user.id
    # filter notification contain viewed=false
    notification_contains_viewed_false = Notification.objects.filter(viewed=False, user_id=user_id)
    return {'notifications_unread': notification_contains_viewed_false}


def get_name_of_user(request):
    # noHp bisa langsung dipanggil karena noHp merupakan username dari akun
    noHp = request.user
    nama = SignUp.objects.get(noHp=noHp).nama
    return nama


@login_required
def logoutView(request):
    logout(request)
    return redirect('pendaftaran:index')


class DashboardView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        # call function get_name_of_user
        name = get_name_of_user(request)

        context = {
            'name': name,
        }

        if request.user.is_staff:
            template_name = 'dashboard/admin.html'
            context['page_title'] = 'Admin'
        else:
            template_name = 'dashboard/user.html'
            context['page_title'] = 'User'

        return render(request, template_name, context)


class ProfileView(LoginRequiredMixin, FormView):
    login_url = '/login'
    form_class = ProfileForm
    template_name = 'dashboard/profile.html'

    def get(self, request, **kwargs):
        # call function get_name_of_user
        name = get_name_of_user(request)
        # create data for form using noHp as primary key
        profile = SignUp.objects.get(noHp=request.user)
        data = {
            'nama': profile.nama,
            'noHp': profile.noHp,
            'email': profile.email,
            'tanggalLahir': profile.tanggalLahir,
            'status': profile.status,
        }
        profile_form = self.form_class(initial=data)

        self.extra_context = {
                'page_title': 'Profile',
                'name': name,
                'profile_form': profile_form,
        }

        return self.render_to_response(self.get_context_data())

    def post(self, request, **kwargs):
        update_signup_model = SignUp.objects.filter(noHp=request.user)
        update_user_model = User.objects.filter(username=request.user)

        form = self.get_form()
        if form.is_valid():
            nama = form.cleaned_data.get('nama')
            # parsing no hp
            noHp = parsing_noHp(form.cleaned_data.get('noHp'))
            email = form.cleaned_data.get('email')
            tanggalLahir = form.cleaned_data.get('tanggalLahir')
            status = form.cleaned_data.get('status')

            update_user_model.update(username=noHp, email=email)
            update_signup_model.update(nama=nama, noHp=noHp, email=email, tanggalLahir=tanggalLahir, status=status)

            messages.add_message(request, messages.INFO, 'Data berhasil di update')
        else:
            # message error from pendaftaran.validators override
            messages.add_message(request, messages.INFO, 'Data tidak valid')

        return redirect('dashboard:profile')


class NotificationUtils:
    def set_agree_diasgree(self, get_request):
        # declare global variable
        notification_answer = Notification.objects.get(id=0)
        if get_request.__contains__('agree'):
            notification_answer = Notification.objects.get(id=get_request['agree'])
            notification_answer.value_confirm_message = True
        elif get_request.__contains__('disagree'):
            notification_answer = Notification.objects.get(id=get_request['disagree'])
            notification_answer.value_confirm_message = False

        notification_answer.is_answered = True
        notification_answer.save()

        # call function with parameter get request
        user_id = str(notification_answer.id)
        self.set_mark_as_read(get_request={'mark-as-read': user_id})

    def set_mark_as_read(self, get_request):
        if get_request.__contains__('mark-as-read'):
            notification_mark_as_read = Notification.objects.get(id=get_request['mark-as-read'])
            notification_mark_as_read.viewed = True
            notification_mark_as_read.save()


class NotificationView(NotificationUtils, LoginRequiredMixin, FormView):
    login_url = '/login'
    form_class = NotificationForm
    template_name = 'dashboard/notification.html'
    success_url = reverse_lazy('dashboard:notification')

    def get(self, request, *args, **kwargs):
        if request.GET:
            self.set_agree_diasgree(request.GET)
            self.set_mark_as_read(request.GET)
            return redirect('dashboard:notification')

        # get notification based on foreign key user_id from models User
        notification_to_view = Notification.objects.filter(user_id=request.user.id)
        self.extra_context = {
            'page_title': 'Notification',
            'notifications': notification_to_view,
        }
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        # list user exist
        users = User.objects.all()

        # call function get_name_of_user
        name = get_name_of_user(request)
        title = request.POST['title']
        message = request.POST['message']
        # why you set False as the default value: if got null, make it false
        '''
            request.POST['sth'] will raise a KeyError exception if 'sth' is not in request.POST.
            
            request.POST.get('sth') will return None if 'sth' is not in request.POST.
        '''
        is_confirm_message = request.POST.get('is_confirm_message', False)

        bulk_data = []
        # if is_confirm_message checklist value return is 'on',
        # so we must convert it to boolean
        if is_confirm_message == 'on':
            is_confirm_message = True
            confirm_message = request.POST['confirm_message']

            # create data bulk, with user_id on user.id models User
            for user in users:
                bulk_data.append(
                    Notification(created_by=name, title=title, message=message, user_id=user.id, is_confirm_message=is_confirm_message, confirm_message=confirm_message)
                )
        else:
            # create data bulk, with user_id on user.id models User
            for user in users:
                bulk_data.append(
                    Notification(created_by=name, title=title, message=message, user_id=user.id)
                )

        # bulk create
        Notification.objects.bulk_create(bulk_data)

        return redirect('dashboard:notification')

    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)


class ListUserUtils:
    def get_list_user(self, get_request):
        # list_user = None
        if len(get_request) == 0:
            list_user = SignUp.objects.all()
        elif get_request.__contains__('search'):
            list_user = SignUp.objects.filter(nama__contains=(get_request['search']))
        elif get_request.__contains__('status'):
            list_user = SignUp.objects.filter(status=get_request['status'].upper())
        else:
            list_user = SignUp.objects.none()

        return list_user


class ListUserView(ListUserUtils, UserPassesTestMixin, LoginRequiredMixin, ListView):
    def test_func(self):
        return self.request.user.is_staff

    login_url = '/login'
    model = SignUp
    template_name = 'dashboard/list-user.html'

    def get(self, request, *args, **kwargs):
        # List User
        list_user = self.get_list_user(request.GET)

        self.extra_context = {
            'page_title': 'List User',
            'list_user': list_user,
            'total_list_user': list_user.count(),
        }
        return super().get(request, *args, **kwargs)


class ListNotificationUtils:
    # prevent title duplicate
    def get_list_distinct(self):
        return Notification.objects.filter(is_confirm_message=True).values('title').distinct()

    # all notification
    # with aggregation and return dict values
    def get_list_agree(self):
        return Notification.objects.filter(is_confirm_message=True, value_confirm_message=True).values('title').annotate(counter=Count('value_confirm_message'))

    def get_list_disagree(self):
        return Notification.objects.filter(is_confirm_message=True, value_confirm_message=False).values('title').annotate(counter=Count('value_confirm_message'))

    def get_list_user_agree(self):
        result = []
        filter_title_user_id = Notification.objects.filter(is_confirm_message=True, value_confirm_message=True).annotate(counter=Count('value_confirm_message')).values('title', 'user_id')
        for filter in filter_title_user_id:
            name = SignUp.objects.get(id=filter['user_id']).nama
            data = {'title': filter['title'], 'name': name}
            result.append(data)

        return result

    def get_list_user_disagree(self):
        result = []
        filter_title_user_id = Notification.objects.filter(is_confirm_message=True, value_confirm_message=False).annotate(counter=Count('value_confirm_message')).values('title', 'user_id')
        for filter in filter_title_user_id:
            name = SignUp.objects.get(id=filter['user_id']).nama
            data = {'title': filter['title'], 'name': name}
            result.append(data)

        return result

    def get_list_user_base_on_title(self):
        result = []
        filter_title_user_id = Notification.objects.filter(is_confirm_message=True).values('title', 'user_id', 'value_confirm_message')
        for filter in filter_title_user_id:
            name = SignUp.objects.get(id=filter['user_id']).nama
            noHp = SignUp.objects.get(id=filter['user_id']).noHp
            data = {'title': filter['title'], 'name': name, 'noHp': noHp, 'value_confirm_message': filter['value_confirm_message']}
            result.append(data)

        return result



class ListNotificationView(ListNotificationUtils, UserPassesTestMixin, LoginRequiredMixin, ListView):
    def test_func(self):
        return self.request.user.is_staff

    login_url = '/login'
    model = Notification
    template_name = 'dashboard/list-notification.html'

    def get(self, request, *args, **kwargs):
        list_notification_distinct = self.get_list_distinct()
        list_notification_agree = self.get_list_agree()
        list_notification_disagree = self.get_list_disagree()
        list_user_agree = self.get_list_user_agree()
        list_user_disagree = self.get_list_user_disagree()
        list_user_base_on_title = self.get_list_user_base_on_title()

        self.extra_context = {
            'page_title': 'List Notification',
            'list_notification_distinct': list_notification_distinct,
            'list_notification_agree': list_notification_agree,
            'list_notification_disagree': list_notification_disagree,

            'list_user_agree': list_user_agree,
            'list_user_disagree': list_user_disagree,

            'list_user_base_on_title': list_user_base_on_title,
        }

        return super().get(request, *args, **kwargs)

