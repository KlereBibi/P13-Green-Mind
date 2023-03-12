from django.urls import path, reverse
from django.contrib.auth.views import LogoutView
from authentification.views import LoginView, TemplateView
from GreenMind import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from . import views


app_name = "authentification"

urlpatterns = [
                  path('login/', LoginView.as_view(), name='login'),
                  path('register/', views.signup, name='register'),
                  path('logout/', LogoutView.as_view(template_name='welcome/home.html', next_page=None),
                       name='logout'),
                  path('account/', TemplateView.as_view(), name='account'),
                  path('activate/<uidb64>/<token>/', views.activate, name='activate'),
                  path('reset_password/', auth_views.PasswordResetView.as_view(
                      template_name="password/password_reset.html",
                      email_template_name='password/password_reset_content.txt',
                      success_url=reverse_lazy('authentification:password_reset_done'),
                      subject_template_name='password/password_reset_subject.txt'),
                       name='reset_password'),
                  path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
                      template_name="password/password_reset_done.html"),
                       name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
                      template_name="password/password_reset_confirm.html",
                      success_url=reverse_lazy('authentification:password_reset_complete')),
                       name='password_reset_confirm'),
                  path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
                      template_name="password/password_reset_complete.html"),
                       name='password_reset_complete')
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
