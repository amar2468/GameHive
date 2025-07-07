from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('guess_the_digit/', include('guess_the_digit.urls')),
    path('rock_paper_scissors/', include('rock_paper_scissors.urls')),
    path('', views.homepage, name='homepage'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('testimonials_page/', views.testimonials_page, name='testimonials_page'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('password_reset_view/<uidb64>/<token>/', views.password_reset_view, name='password_reset_view'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('update_personal_details/', views.update_personal_details, name='update_personal_details'),
    path('change_password/', views.change_password, name='change_password'),
    path('redeeming_points/', views.redeeming_points, name='redeeming_points'),
    path('customer_support/', views.customer_support, name='customer_support'),
    path('remove_testimonial/', views.remove_testimonial, name='remove_testimonial'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('edit_user_info/', views.edit_user_info, name='edit_user_info'),
    path('user_request_mgmt/', views.user_request_mgmt, name='user_request_mgmt'),
    path('display_ticket_info/', views.display_ticket_info, name='display_ticket_info'),
    path('testimonials_mgmt/', views.testimonials_mgmt, name='testimonials_mgmt'),
    path('add_comment_customer_support_ticket/', views.add_comment_customer_support_ticket, name='add_comment_customer_support_ticket'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.log_out, name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.page_does_not_exist
