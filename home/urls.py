from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("donors_list/<int:myid>/", views.donors_list, name="donors_list"),
    path("donors_details/<int:myid>/", views.donors_details, name="donors_details"),
    path("request_blood/", views.request_blood, name="request_blood"),
    path("see_all_request/", views.see_all_request, name="see_all_request"),
    path("become_donor/", views.become_donor, name="become_donor"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_status/', views.change_status, name='change_status'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('campaigns/', views.campaigns, name='campaigns'),
    path('custom_admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('custom_admin/delete_donor/<int:donor_id>/', views.delete_donor, name='delete_donor'),
    path('custom_admin/fulfill_request/<int:request_id>/', views.fulfill_request, name='fulfill_request'),
    path('custom_admin/delete_request/<int:request_id>/', views.delete_request, name='delete_request'),
    path('custom_admin/manage_donors/', views.manage_donors, name='manage_donors'),
    path('custom_admin/manage_requests/', views.manage_donors, name='manage_requests'),
    
]


