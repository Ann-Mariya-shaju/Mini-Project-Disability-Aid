from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login as auth_login
#from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
#from .models import MyUser
from django.template.loader import render_to_string
@never_cache
def index(request):
    return render(request,'index.html')
#def dashboard(request):
    #return render(request,'dashboard.html')


@never_cache
@login_required(login_url='login')
def dashboard(request):
    if 'username' in request.session:
        response = render(request,"dashboard.html")
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
    else:
        return redirect('login')

def my_profile(request):
    return render(request,'my_profile.html')        





@never_cache
@login_required(login_url='login')
def panchayat(request):
    if 'username' in request.session:
        response = render(request,"panchayat.html")
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
    else:
        return redirect('login')




#def registration(request):
     #if request.method == 'POST':
       # username = request.POST['username']
       # email = request.POST['email']
        #password = request.POST['password']
       # confirm_password = request.POST['confirm_password']  # Make sure this matches your form field name
       # phone_number = request.POST['phone_number'] 
       # medical_certificate = request.POST['medical_certificate']
       # guardian_type = request.POST['guardian_type']

       # if password != confirm_password:
            # Handle password mismatch error
            #return render(request, 'register.html', {'error_message': 'Passwords do not match'})

        # Create a new user object
       
        #user = CustomUser.objects.create_user(username=username, email=email, password=password,phone_number=phone_number,medical_certificate=medical_certificate,guardian_type=guardian_type)
       
        # You may want to do additional processing here if needed

        #return redirect('login')  # Redirect to login page after successful registration

     #return render(request,'registration.html')


@never_cache
def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone_number = request.POST.get('phone_number')
        guardian_type = request.POST.get('guardian_type')

        if password != confirm_password:
            # Handle password mismatch error
            return render(request, 'register.html', {'error_message': 'Passwords do not match'})

        if 'medical_certificate' in request.FILES:
            medical_certificate = request.FILES['medical_certificate']
            # Process the uploaded file as needed
        else:
            # Handle the case where 'medical_certificate' is missing in the form submission
            return render(request, 'registration.html', {'error_message': 'Medical certificate is required'})

        # Create a new user object
        user = CustomUser.objects.create_user(username=username, email=email, password=password, phone_number=phone_number, medical_certificate=medical_certificate, guardian_type=guardian_type)
        # You may want to do additional processing here if needed

        return redirect('login')  # Redirect to the login page after a successful registration

    return render(request, 'registration.html')


from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
@never_cache
def login(request):
    if request.method == 'POST':
        loginusername = request.POST.get('username')
        password = request.POST.get('password')

        if loginusername == "ann" and password == "ann123":
            # For the superuser, redirect to admin_index.html with user list and count
            users = CustomUser.objects.exclude(is_superuser='1')  # Exclude superusers
            user_count = users.count()
            context = {
                "users": users,
                "user_count": user_count
            }
            return render(request, 'admindashboard.html', context)
        else:
            user = authenticate(request, username=loginusername, password=password)
            if user is not None:
                auth_login(request, user)
                request.session['username'] = user.username
                if user.guardian_type == 'father':
                    return redirect('dashboard')
                elif user.guardian_type == 'mother':
                    return redirect('dashboard')
                elif user.guardian_type == 'other':
                    return redirect('dashboard')    
                else:
                    return redirect('admindashboard')            
            else:
                error_message = 'Invalid username or password'
                return render(request, 'login.html', {'error_message': error_message})
    else:
            error_message = 'username and password are required'
            return render(request,'login.html', {'error_message': error_message})
    
    response = render(request,'login.html')
    response['Cache-Control'] = 'no-store,must-revalidate'
    return response

@never_cache
def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

@never_cache
def logout(request):
    auth.logout(request)
    return redirect("/")
@never_cache
@login_required(login_url='login')
def admindashboard(request):
    if request.user.is_superuser:
        users = CustomUser.objects.exclude(is_superuser=True)
        return render(request, "admindashboard.html", {"users": users})
    return redirect("home")
def deactivate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
         # Send deactivation email
        subject = 'Account Deactivation'
        message = 'Your account has been deactivated by the admin.'
        from_email = 'annmariyashaju2024a@mca.ajce.in'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('deactivation_mail.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        messages.success(request, f"User '{user.username}' has been deactivated, and an email has been sent.")
    else:
        messages.warning(request, f"User '{user.username}' is already deactivated.")
    return redirect('admindashboard')

def activate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if not user.is_active:
        user.is_active = True
        user.save()
        subject = 'Account activated'
        message = 'Your account has been activated.'
        from_email = 'annmariyashaju2024a@mca.ajce.in'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('activation_mail.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    else:
        messages.warning(request, f"User '{user.username}' is already active.")
    return redirect('admindashboard')

from django.shortcuts import render, redirect
from .models import Doctor  # Import your Doctor model

@never_cache
def doctor(request):
    if request.method == 'POST':
        # Get the data from the request
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        qualification = request.POST.get('qualification')
        specialization = request.POST.get('specialization')

        # Create a new Doctor instance and save it to the database
        doctor = Doctor(name=name, username=username, email=email, phone=phone,password=password,qualification=qualification, specialization=specialization)
        doctor.save()

        # Redirect to the admin dashboard upon successful registration
        return redirect('admindashboard')
    else:
        return render(request, 'doctor.html')  # Render your registration page

def doctor_view(request):
    # Query the database to get all doctor objects
    doctors = Doctor.objects.all()

    # Create a context dictionary to pass the doctor data to the template
    context = {
        'doctors': doctors
    }

    # Render the template and pass the context
    return render(request, 'doctor_view.html', context)

@login_required
def profile_update(request):
    if request.method == 'POST':
        # Get updated data from the form
        email = request.POST['email']
        username = request.POST['username']
        phone = request.POST['phone']
        medical_certificate = request.POST['medical_certificate']

        # Update the user's profile with the new data
        user = request.user
        user.email = email
        user.username = username
        user.phone = phone
        user.medical_certificate =medical_certificate

        user.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('my_profile')

    return render(request, 'profile_update.html', {'user': request.user})

from django.shortcuts import render, redirect
from store.models import Doctor  # Import the Doctor model
from django.http import HttpResponse

def edit(request, doctor_id):
   # doctor = Doctor.objects.get(id=doctor_id)
    #if request.method == 'POST':
     #  return redirect('admindashboard')
    #return render(request, 'edit.html', {'doctor': doctor})
    
    doctor = Doctor.objects.get(id=doctor_id)

    if request.method == 'POST':
        # Update the doctor's details based on the form data
        doctor.name = request.POST.get('name')
        doctor.username = request.POST.get('username')
        doctor.phone = request.POST.get('phone')
        doctor.qualification = request.POST.get('qualification')
        doctor.specialization = request.POST.get('specialization')
        doctor.save()  # Save the changes
        return redirect('admindashboard')  # Redirect to the doctor list or another page

    return render(request, 'edit.html', {'doctor': doctor})
def delete(request, doctor_id):
    # Retrieve the doctor object by ID
    doctor = Doctor.objects.get(id=doctor_id)

    if request.method == 'POST':
        # Delete the doctor object here
        doctor.delete()

        # Redirect to the doctor list or another page after deletion
        return redirect('doctor_list')

    return render(request, 'delete.html', {'doctor': doctor})