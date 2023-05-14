from django.contrib import admin
from django.urls import path,include
from gogonote import views

urlpatterns = [
    path('', views.homepage, name='gogohome'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('newuserentry', views.newuserentry, name='newuserentry'),

    path('loginpage/<token>/', views.success_register, name='success_register'),

    path('folder_note', views.folder_note, name='folder_note'),
    path('addfolder',views.addfolder,name='addfolder'),
    path('loadfolder',views.loadfolder,name='loadfolder'),
    path('editfolder',views.editfolder,name='editfolder'),
    path('delfolder',views.delfolder,name='delfolder'),

    path('shownote',views.show_note,name='shownote'),
    path('addnote',views.add_note,name='addnote'),
    # path('folder',views.pagefolder,name='pagefolder'),

    path('editnote',views.edit_note,name='editnote'),
    path('delnote',views.del_note,name='delnote'),

    path('logout', views.logout, name='logout'),

    path('forgetpassword', views.forgetpassword, name='forgetpassword'),
    path('change-password/<token>/',views.change_password,name='change-password'),
    # path('change-password',views.change_password,name='changepassword'),

    path('userchangepassword',views.userchangepassword,name='userchangepassword'),
]





