from django.contrib import admin
from django.urls import path
from customer import views

urlpatterns = [
    path("", views.home, name='Home'),
    path("app/register", views.register, name='register'),
    path("app/login", views.dologin, name='dologin'),
    path("contact", views.contact, name='Contact'),
    path("search", views.get_item, name='search'),
    path("view_users", views.get_users, name='view'),
    path("edit/<int:id>", views.edit, name='edit'),
    path("update/<int:id>", views.update, name='update'),
    path("upload", views.upload, name='upload'),
    path("user/dashboard", views.dashboard, name='dashboard'),
    path("user/classroom", views.classroom, name='classroom'),
    path("user/profile", views.profile, name='profile'),
    path("user/changepass/", views.change_password, name='change_password'),
    path("app/fpass", views.fpass, name='fpass'),
    path("checkout", views.checkout, name='checkout'),
    path("dologout", views.dologout, name='dologout'),  
    path("getfees", views.getfees, name='getfees'),
    path("payfees", views.payfees, name='payfees'),
    path("drive", views.drive, name='drive'),
    path("update/email/<int:id>", views.addmail, name='addmail'),
    path("update/mobile/", views.addcall, name='addcall'),
    path("app/register/register_success/", views.reg_success, name='reg_success'),
    path("app/register/profile/", views.reg_user, name='reg_user'),
    path("user/archives", views.archives, name='archives'),
    path("user/courses", views.courses, name='courses'),
    path("user/exam", views.exam, name='exam'),
    path("user/form", views.myform, name='myform'),
    # path("app/register/getDetails/<int:user_id>/", views.getDetails, name='getDetails'),
    path("user/getText", views.getText, name='getText'),
    # path("user/user/getPDF", views.getPDF, name='getPDF'),

    
]

handler404 = 'customer.views.error_404'