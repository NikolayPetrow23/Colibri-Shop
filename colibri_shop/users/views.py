from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from users.models import User, EmailVerification
from products.models import Basket


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def form_valid(self, form):
        response = super().form_valid(form)

        # Добавляем свою проверку на подтверждение email
        if not self.request.user.is_verified_email:
            form.add_error(None, "Чтобы войти, необходимо подтвердить почту.")
            return self.form_invalid(form)

        return response
    #
    # @method_decorator(csrf_exempt)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    # def get_success_url(self):
    #     return reverse_lazy('products:index')


custom_login_view = csrf_exempt(UserLoginView.as_view())


class UserRegisterView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрированы!'

    # def get_success_url(self):
    #     return reverse_lazy('users:login')


class UserProfileView(UpdateView):
    model = User
    template_name = 'users/profile_new.html'
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    # def get_context_data(self, **kwargs):
    #     context = super(UserProfileView, self).get_context_data()
    #     context['baskets'] = Basket.objects.filter(user=self.object)
    #     return context


# class CustomLogoutView(LogoutView):
#
#     def get_success_url(self):
#         return reverse_lazy('products:index')


class EmailVerificationView(TemplateView):
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        UUID = kwargs['UUID']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, UUID=UUID)
        if email_verifications and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return redirect('products:index')
