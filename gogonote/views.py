from django.shortcuts import render, redirect
from gogonote.models import userentry, foldername, notenames
from django.contrib import messages
import uuid
from gogonote.helper import confirmation_mailing, send_password_encrypted, forget_password_mail
from datetime import datetime
from gogonote.encrypt import encrypting
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

# Create your views here.


def homepage(request):
    return render (request, 'homepage.html')

def login(request):
    return render (request,'login.html')

def signup(request):
    return render (request, 'signup.html')

@csrf_exempt
def newuserentry(request):
    if request.method == 'POST':
        email = request.POST['newuseremail']
        password = request.POST['newuserpassword']
        cpassword = request.POST['newusercpassword']
        
        verify =True 
        
        if verify == True:
            if userentry.objects.filter(Email=email).exists():
                messages.error(request, 'Email Already Registered')
                return redirect('signup')
            elif password == cpassword:
                token = str(uuid.uuid4())
                confirmation_mailing(email,email, token)
                # confirmation_mailing.delay(email,email, token)
                messages.success(request, 'An confirmation mail has been sent to your email')
                
                # password = encrypting.hashing(password)
                a = int(uuid.uuid4())
                newuser = userentry(Email=email, Password = password, random1=a ,signup_date=datetime.now(),register_token=token)
                newuser.save()
                return  redirect('signup')
            else:
                messages.error(request, 'Password not match')
                return redirect('signup')
        else:       
            return render(request,'login.html')
    else:
        return render(request, 'login.html')


def success_register(request, token):
    print(token)
    try:
        if userentry.objects.get(register_token=token):
                pas = userentry.objects.get(register_token=token) 
                password = pas.Password
                email = pas.Email
                # user_name = pas.Name
                
                #send passsword encrypt
                # send_password_encrypted.delay(user_name,password,email)
                send_password_encrypted(email, password, email)
                password = encrypting.hashing(password)
                
                userentry.objects.filter(register_token=token).update(Password=password)
                userentry.objects.filter(register_token=token).update(success=True)
                userentry.objects.filter(register_token=token).update(register_token="")
                messages.success(request, 'Email Verification Success')
                print('succes')
                return redirect('login')
    except:
        return redirect('register')

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        email = request.POST['useremail']
        password = request.POST['userpassword']
        print(email, password)

        if userentry.objects.filter(Email=email).exists():
            data = userentry.objects.get(Email=email)
            if data.success:
                if str(data.Password) == str(encrypting.hashing(password)):
                        
                    request.session['id1'] = data.random1
                    request.session['paskey'] = (encrypting.get_encrypted_password(password))
                    print('\n;id1 = ', request.session['id1'])
                    print(';paskey = ', request.session['paskey'],'\n')

                    return redirect('folder_note')
                else:
                    messages.error(request, 'Password incorrect')
                    return redirect('login')
            else:
                messages.error(request,'Email not activated')
                return redirect('login')
        else:
            messages.error(request, 'Email not registered')
            return redirect('login')
    else:
        return render(request, 'login.html')


# FOLDERS AND NOTES

def folder_note(request):
    if request.session.get('id1', None):
        random1 = request.session['id1']
        paskey = request.session['paskey']

        if foldername.objects.filter(random1=random1).exists():

            folders_data = foldername.objects.filter(random1=random1).values()
            folder1_random2 = folders_data[0]['random2']
        else:
            print("\n NO FOLDERS \n")
            return render (request, 'folder_note.html',{'user_random':random1})

        print("folder1 random2 :: :: :: ",folder1_random2)
        print("folder1 random2 :: :: :: ",folder1_random2)

        notedata = notenames.objects.filter(random2=folder1_random2).values()

        notedata = decrypt_note(notedata, paskey)

        return render (request, 'folder_note.html',{'folder_name':folders_data,'user_random':random1, 'folder1_random':folder1_random2, 'notedata':notedata})
    return render (request, 'login.html')

@csrf_exempt
def addfolder(request):
    if request.method == 'POST':
        new_folder_name = request.POST.get('new_folder_name')
        user_random = request.POST.get('user_random')
        # random1 = request.session['id1']
        # print("random  :: " ,random1)
        user_email = userentry.objects.get(random1=user_random)
        user_email = user_email.Email
        print("user_random :: " , user_random)
        print("user_email :: " , user_email)
        # print(user_email)
        a = int(uuid.uuid4())
        foldername(Email=user_email,foldername=new_folder_name,random1=user_random,random2=a).save()

        fold = foldername.objects.filter(random1=user_random).values()
        fold = list(fold)
        return JsonResponse({'status': 1,'folder_name':fold})
    else:
        return JsonResponse({'status': 0})

@csrf_exempt
def loadfolder(request):
    if request.method == 'POST':
        user_random = request.POST.get('user_random')
        fold = foldername.objects.filter(random1=user_random).values()
        # fold = fold.values()
        fold = list(fold)
        return JsonResponse({'status': 1,'folder_name':fold})
    else:
        return JsonResponse({'status': 0})

@csrf_exempt
def editfolder(request):
    if request.method == 'POST':
        new_folder_name = request.POST.get('folder_name')
        data_sid = request.POST.get('data_sid')
        user_random = request.POST.get('user_random')

        data = foldername.objects.get(random2=data_sid)
        print(data)
        foldername.objects.filter(random2=data_sid).update(foldername = new_folder_name)

        fold = foldername.objects.filter(random1=user_random).values()
        fold = list(fold)
        return JsonResponse({'status': 1,'folder_name':fold})
    else:
        return JsonResponse({'status': 0})
 
@csrf_exempt
def delfolder(request):
    if request.method == 'POST':
        data_sid = request.POST.get('data_sid')
        foldername.objects.get(random2=data_sid).delete()       # delete not only folder del with notes + folder
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})

# NOTES (ENCRYPTION IN THIS ONLY) 
@csrf_exempt
def add_note(request):
    if request.method == 'POST':
        paskey = request.session['paskey']
        title = request.POST.get('postTitle')
        note = request.POST.get('postDescription')
        user_random = request.POST.get('user_random')
        user_email = userentry.objects.get(random1=user_random)
        user_email = user_email.Email
        random3 = request.POST.get('random3')
        random2 = request.POST.get('dataid3')

        if random3 == "":
            rand3 = str(int(uuid.uuid4()))
            rand3 = int(rand3[:10])
            notenames(Email=user_email, title=title, note=encrypting.encrypt(note,paskey), random2=random2, random3=rand3,random1=user_random).save()
            return JsonResponse({'status': 1,'random3':rand3})
        else:
            notenames.objects.filter(random3=random3).update(note=encrypting.encrypt(note,paskey), title=title)

            return JsonResponse({'status': 1,'random3':random3})
    else:
        return JsonResponse({'status': 0})
@csrf_exempt
def show_note(request):
    if request.method == 'POST':
        paskey = request.session['paskey']
        random2 = request.POST.get('random2')
        user_random = request.POST.get('user_random')
        notedata = notenames.objects.filter(random2=random2).values()

        notedata = decrypt_note(notedata, paskey)
        notedata = list(notedata)
        
        if len(notedata) == 0:
            return JsonResponse({'status': 1,'notedata':''})
        return JsonResponse({'status': 1,'notedata':notedata})
    else:
        return JsonResponse({'status': 0})
@csrf_exempt
def edit_note(request):
    if request.method == 'POST':
        paskey = request.session['paskey']
        random3 = request.POST.get('random3')
        notedata = notenames.objects.filter(random3=random3).values()
        notedata = decrypt_note(notedata, paskey)
        notedata = list(notedata)
        
        return JsonResponse({'status': 1,'notedata':notedata})
    else:
        return JsonResponse({'status': 0})

@csrf_exempt
def del_note(request):
    if request.method == 'POST':
        random3 = request.POST.get('random3')
        notenames.objects.get(random3=random3).delete()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})

def logout(request):
    print("logout")
    try:
        del request.session['id1']
        return redirect('login')
        
    except:
        return redirect('login')

    
@csrf_exempt
def forgetpassword(request):
    if request.method == 'POST':
        username = request.POST.get('useremail')
        
        #recaptcha stuff
        clientkey = request.POST['g-recaptcha-response']
        GOOGLE_RECAPTCHA_SECRET_KEY = '6LcDNsAbAAAAAHMeQwvPZY26To2FMemHeEKEtfRf'
        captchaData = {
            'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
            'response':clientkey,
        }
        r = requests.post(url ='https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        verify = response['success']

        if verify == True:
            print('\n',username,"\n")
            if userentry.objects.filter(Email=username).exists():
                user_name = userentry.objects.get(Email=username)
                user_name = user_name.Email

                token = str(uuid.uuid4())
                
                forget_password_mail(user_name,username,token)
                # send_forget_password_mail(username,token)
                messages.success(request,'An email is sent to change password')
                
                data = userentry.objects.get(Email=username)
                data.forget_password_token = token
                data.save()
                return redirect('forgetpassword')
            else:
                messages.error(request,"user not registered")
                return render(request, 'forgetpassword.html')
        else:
            return render(request,'forgetpassword.html')
    else:
        return render(request,'forgetpassword.html')

@csrf_exempt
def change_password(request,token):
    print("token   ",token)
    try:
        if userentry.objects.get(forget_password_token=token):
            data = userentry.objects.get(forget_password_token=token)
            data = data.Email
        else:
            return redirect('forgetpassword')
    except:
        return redirect('forgetpassword')

    if request.method == 'POST':
        secret_key = request.POST.get('secret_key')
        user = request.POST.get('user')

        if user is None:
            messages.success(request, 'No user  found.')
            return redirect(f'/change-password/{token}/')

        try:
            passkey = encrypting.valid_secret_key(secret_key,user) 
        except:
            messages.error(request, 'Invalid secret key.')
            return redirect(f'/change-password/{token}/')
        
        if passkey is not False:
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')


            if new_password == confirm_password:
                try:               
                    reecrypt_note(passkey,user,new_password)                                       
                except:
                    messages.error(request, 'Enter new secret Key.')
                    return redirect(f'/change-password/{token}/')

                user_data = userentry.objects.get(Email=user)
                user_name = user_data.Email

                send_password_encrypted(user_name,confirm_password,user)
                
                user_data.Password = encrypting.hashing(confirm_password)
                user_data.save()
                # user_data.forget_password_token= str(uuid.uuid4())
                user_data.forget_password_token= ""
                user_data.save()
                messages.success(request, 'Password change success.')
                return redirect('login')
            else:
                messages.error(request, 'Mismatched Password.')
                return redirect(f'/change-password/{token}/')
        else:
            messages.error(request, 'Invalid Secret Key.')
            return redirect(f'/change-password/{token}/')


    return render(request,'change-password.html',{'data':data})



# def change_password(request):
#     return render (request, 'user-change-password.html')

@csrf_exempt
def userchangepassword(request):
    if request.method == 'POST':
        email = request.POST.get('useremailchange')
        oldpass = request.POST.get('oldpasswordchange')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if userentry.objects.filter(Email=email).exists():
            data = userentry.objects.get(Email=email)
            user_name = data.Email
            # if data.success:
            if str(data.Password) == str(encrypting.hashing(oldpass)):
                
                if new_password == confirm_password:
                    # if new_password == oldpass:
                    try:               
                        reecrypt_note(oldpass,email,new_password)                                       
                    except:
                        messages.error(request, 'Re - Try')
                        return redirect('userchangepassword')

                    send_password_encrypted(user_name,confirm_password,email)

                    user_data = userentry.objects.get(Email=email)
                    
                    user_data.Password = encrypting.hashing(confirm_password)
                    user_data.save()
                    messages.success(request, 'Password change success.')
                    return redirect('login')
                else:
                    messages.error(request, "Mismatched New Password")
                    return redirect('userchangepassword')
            else:
                messages.error(request, "Mismatched Old Password")
                return redirect('userchangepassword')
        else:
            messages.error(request, "Email/User Not Exist")
            return redirect('userchangepassword')

    return render(request,'user-change-password.html')

#Decrypt Notes for loop to get all the notes
def decrypt_note(notes_data,paskey):
    notes = encrypting.get_decrypted_not(notes_data,paskey)
    # print(notes)
    # for note in notes_data:
    #     note['Notes'] = encrypting.get_decrypted_not(note['Notes'], paskey)
    return notes


# REENCRYPT NOTES
def reecrypt_note(oldpass,user,newpass):
    passkey1 = encrypting.get_encrypted_password(oldpass)
    passkey2 = encrypting.get_encrypted_password(newpass)
    all_notes = notenames.objects.filter(Email=user)

    all_notes = all_notes.values()
    
    # 1. Here we get new encrypted notes
    new_all_notes = encrypting.reecrypt_allnotes(all_notes, passkey1, passkey2)

    # 2.    Here we have to store/update encrypted notes in the database
    # 2.1   First we have to get random3 of all particular notes then update it by filtering them out through random3 (as it is unique in the database) 
    
    for note in new_all_notes:
        random3 = note['random3']
        notenames.objects.filter(random3=random3).update(title=note['title'], note=note['note'])

    pass






