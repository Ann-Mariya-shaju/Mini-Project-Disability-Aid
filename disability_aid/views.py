import datetime
import random
import smtplib
from email.mime.text import MIMEText

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from disability_aid.models import *


def login(request):
    return render(request, 'login.html')


def login_post(request):
    usn = request.POST['usn']
    psw = request.POST['psw']
    res = Login.objects.filter(username=usn, password=psw)
    if res.exists():
        if res[0].user_type == 'admin':
            request.session['lid'] = res[0].id
            return redirect('/admin_home')
        if res[0].user_type == 'transport':
            request.session['lid'] = res[0].id
            return redirect('/transport_home')
        if res[0].user_type == 'user':
            request.session['lid'] = res[0].id
            return redirect('/user_home')
        if res[0].user_type == 'panchayat':
            request.session['lid'] = res[0].id
            return redirect('/panchayat_home')
        else:
            return HttpResponse("<script>alert('not allowed'); window.location='/'</script>")
    else:
        return HttpResponse("<script>alert('check password/username'); window.location='/'</script>")


def change_password(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('please login');window.location='/'</script>")
    else:
        usr = Login.objects.get(id=request.session['lid'])
        request.session['head'] = 'Change Password'
        if usr.user_type == 'admin':
            return render(request, 'admin/change password.html')
        if usr.user_type == 'transport':
            return render(request, 'transport/change password.html')


def change_password_post(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('please login');window.location='/'</script>")
    else:
        olp = request.POST['textfield']
        nwp = request.POST['textfield2']
        res = Login.objects.filter(id=request.session['lid'], password=olp)
        if res.exists():
                Login.objects.filter(id=request.session['lid']).update(password=nwp)
                return HttpResponse("<script>alert('updated');window.location='/change_password#aaa'</script>")
        else:
            return HttpResponse("<script>alert('wrong password');window.location='/change_password#aaa'</script>")


def logout(request):
    request.session['lid'] = ''
    return redirect('/')


def admin_home(request):
    request.session['head'] = ''
    return render(request, 'admin/index.html')


def add_transport(request):
    request.session['head'] = 'Add Transport Agency'
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        return render(request, 'admin/add transport.html')


def add_transport_post(request):
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        global gmail
        psw = random.randint(0000, 9999)
        nme = request.POST['textfield']
        eml = request.POST['textfield2']
        phn = request.POST['textfield3']
        pls = request.POST['textfield4']
        pst = request.POST['textfield5']
        pin = request.POST['textfield6']
        if Login.objects.filter(username=eml).exists():
            return HttpResponse("<script>alert('user exists'); window.location='/add_transport#aaa'</script>")
        log = Login(
            username=eml,
            user_type='transport',
            password=psw
        )
        log.save()

        obj = Transport(
            LOGIN=log,
            name=nme,
            email=eml,
            phone=phn,
            place=pls,
            post=pst,
            pin=pin,
        )
        obj.save()
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)

            gmail.ehlo()

            gmail.starttls()

            gmail.login('riss.athulchandran@gmail.com', 'cjcyiddroayvvpqn')

        except Exception as e:
            print("Couldn't setup email!!" + str(e))

        msg = MIMEText("Your Password is " + str(psw))

        msg['Subject'] = 'Verification'

        msg['To'] = eml

        msg['From'] = 'riss.athulchandran@gmail.com'

        try:

            gmail.send_message(msg)

        except Exception as e:

            print("COULDN'T SEND EMAIL", str(e))
        return HttpResponse("<script>alert('Data Added');window.location='/view_transport#aaa'</script>")


def view_transport(request):
    request.session['head'] = 'View Transport'
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        trs = Transport.objects.all()
        return render(request, 'admin/view transport.html', {'data': trs})


def edit_transport(request, tid):
    request.session['head'] = 'edit Transport'
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        co = Transport.objects.get(id=tid)
        return render(request, 'admin/edit transport.html', {'data': co})


def edit_transport_post(request, tid):
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        nme = request.POST['textfield']
        phn = request.POST['textfield3']
        pls = request.POST['textfield4']
        pst = request.POST['textfield5']
        pin = request.POST['textfield6']
        Transport.objects.filter(id=tid).update(
            name=nme,
            phone=phn,
            place=pls,
            post=pst,
            pin=pin
        )
        return HttpResponse("<script>alert('edited'); window.location='/view_transport#aaa'</script>")


def delete_transport(request, tid):
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        Login.objects.get(id=tid).delete()
        return HttpResponse("<script>alert('deleted'); window.location='/view_transport#aaa'</script>")


def add_hospital(request):
    request.session['head'] = 'Add Hospital'
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        return render(request, 'admin/add hospital.html')


def add_hospital_post(request):
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        global gmail
        psw = random.randint(0000, 9999)
        nme = request.POST['textfield']
        eml = request.POST['textfield2']
        phn = request.POST['textfield3']
        pls = request.POST['textfield4']
        pst = request.POST['textfield5']
        pin = request.POST['textfield6']
        lat = request.POST['textfield7']
        lng = request.POST['textfield8']
        if Login.objects.filter(username=eml).exists():
            return HttpResponse("<script>alert('user exists'); window.location='/add_hospital#aaa'</script>")
        log = Login(
            username=eml,
            user_type='hospital',
            password=psw
        )
        log.save()

        obj = Hospital(
            LOGIN=log,
            name=nme,
            email=eml,
            phone=phn,
            place=pls,
            post=pst,
            pin=pin,
            latitude=lat,
            longitude=lng,
        )
        obj.save()
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)

            gmail.ehlo()

            gmail.starttls()

            gmail.login('riss.athulchandran@gmail.com', 'cjcyiddroayvvpqn')

        except Exception as e:
            print("Couldn't setup email!!" + str(e))

        msg = MIMEText("Your Password is " + str(psw))

        msg['Subject'] = 'Verification'

        msg['To'] = eml

        msg['From'] = 'riss.athulchandran@gmail.com'

        try:

            gmail.send_message(msg)

        except Exception as e:

            print("COULDN'T SEND EMAIL", str(e))
        return HttpResponse("<script>alert('Data Added');window.location='/view_hospital#aaa'</script>")


def view_hospital(request):
    request.session['head'] = 'View Hospital'
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        trs = Hospital.objects.all()
        return render(request, 'admin/view hospital.html', {'data': trs})


def edit_hospital(request, tid):
    request.session['head'] = 'edit Hospital'
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        co = Hospital.objects.get(id=tid)
        return render(request, 'admin/edit hospital.html', {'data': co})


def edit_hospital_post(request, tid):
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        nme = request.POST['textfield']
        phn = request.POST['textfield3']
        pls = request.POST['textfield4']
        pst = request.POST['textfield5']
        pin = request.POST['textfield6']
        lat = request.POST['textfield7']
        lng = request.POST['textfield8']
        Hospital.objects.filter(id=tid).update(
            name=nme,
            phone=phn,
            place=pls,
            post=pst,
            pin=pin,
            latitude=lat,
            longitude=lng
        )
        return HttpResponse("<script>alert('edited'); window.location='/view_hospital#aaa'</script>")


def delete_hospital(request, tid):
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        Login.objects.get(id=tid).delete()
        return HttpResponse("<script>alert('deleted'); window.location='/view_hospital#aaa'</script>")


def add_panchayat(request):
    request.session['head'] = 'Add Panchayat'
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        return render(request, 'admin/add panchayat.html')


def add_panchayat_post(request):
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        global gmail
        psw = random.randint(0000, 9999)
        nme = request.POST['textfield']
        eml = request.POST['textfield2']
        phn = request.POST['textfield3']
        pls = request.POST['textfield4']
        pst = request.POST['textfield5']
        pin = request.POST['textfield6']
        if Login.objects.filter(username=eml).exists():
            return HttpResponse("<script>alert('user exists'); window.location='/add_panchayat#aaa'</script>")
        log = Login(
            username=eml,
            user_type='panchayat',
            password=psw
        )
        log.save()

        obj = Panchayat(
            LOGIN=log,
            name=nme,
            email=eml,
            phone=phn,
            place=pls,
            post=pst,
            pin=pin,
        )
        obj.save()
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)

            gmail.ehlo()

            gmail.starttls()

            gmail.login('riss.athulchandran@gmail.com', 'cjcyiddroayvvpqn')

        except Exception as e:
            print("Couldn't setup email!!" + str(e))

        msg = MIMEText("Your Password is " + str(psw))

        msg['Subject'] = 'Verification'

        msg['To'] = eml

        msg['From'] = 'riss.athulchandran@gmail.com'

        try:

            gmail.send_message(msg)

        except Exception as e:

            print("COULDN'T SEND EMAIL", str(e))
        return HttpResponse("<script>alert('Data Added');window.location='/view_panchayat#aaa'</script>")


def view_panchayat(request):
    request.session['head'] = 'View Panchayat'
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        trs = Panchayat.objects.all()
        return render(request, 'admin/view panchayat.html', {'data': trs})


def edit_panchayat(request, tid):
    request.session['head'] = 'edit Panchayat'
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        co = Panchayat.objects.get(id=tid)
        return render(request, 'admin/edit panchayat.html', {'data': co})


def edit_panchayat_post(request, tid):
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        nme = request.POST['textfield']
        phn = request.POST['textfield3']
        pls = request.POST['textfield4']
        pst = request.POST['textfield5']
        pin = request.POST['textfield6']
        Panchayat.objects.filter(id=tid).update(
            name=nme,
            phone=phn,
            place=pls,
            post=pst,
            pin=pin
        )
        return HttpResponse("<script>alert('edited'); window.location='/view_panchayat#aaa'</script>")


def delete_panchayat(request, tid):
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        Login.objects.get(id=tid).delete()
        return HttpResponse("<script>alert('deleted'); window.location='/view_panchayat#aaa'</script>")


def transport_home(request):
    request.session['head'] = ''
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    return render(request, 'transport/index.html')


def view_user_request(request):
    request.session['head'] = 'View User Request'
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        trs = Concession.objects.filter(TRANSPORT__LOGIN=request.session['lid'], status='pending')
        return render(request, 'transport/view user request.html', {'data': trs})


def view_user_request_status(request):
    request.session['head'] = 'View User Request Status'
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        trs = Concession.objects.filter(TRANSPORT__LOGIN=request.session['lid']).exclude(status='pending')
        return render(request, 'transport/view user request status.html', {'data': trs})


def approve_concession(request, tid):
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        Concession.objects.filter(id=tid).update(status='approved')
        return HttpResponse("<script>alert('approved'); window.location='/view_user_request#aaa'</script>")


def reject_concession(request, tid):
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        Concession.objects.filter(id=tid).update(status='rejected')
        return HttpResponse("<script>alert('rejected'); window.location='/view_user_request#aaa'</script>")


######          USER

def user_register(request):
    return render(request, "User/register.html")
def user_register_post(request):
    file=request.FILES['f1']
    name=request.POST['t1']
    email=request.POST['t2']
    phone=request.POST['t3']
    place=request.POST['t4']
    post=request.POST['t5']
    pin=request.POST['t6']
    password=request.POST['t7']
    d=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fs=FileSystemStorage()
    fs.save(r"F:\DisabilityAid\disability_aid\static\pics\\" + d + ".jpg", file)
    path="/static/pics" +  d + ".jpg"

    obj=Login()
    obj.username=email
    obj.password=password
    obj.user_type="user"
    obj.save()

    obj2=User()
    obj2.name=name
    obj2.photo=path
    obj2.email=email
    obj2.phone=phone
    obj2.place=place
    obj2.post=post
    obj2.pin=pin
    obj2.LOGIN=obj
    obj2.save()
    return HttpResponse("<script>alert('Registered'); window.location='/'</script>")




def user_home(request):
    return render(request, "User/index.html")


def user_view_transport(request):
    request.session['head'] = 'View Transport'
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        trs = Transport.objects.all()
        return render(request, 'User/view transport.html', {'data': trs})

def user_add_concession(request, id):
    return render(request, "User/add_concession.html", {'id':id})
def user_Add_concession_post(request, id):
    type=request.POST['textfield']
    from_place=request.POST['textfield4']
    to_place=request.POST['textfield5']
    obj=Concession()
    obj.concession=type
    obj.from_place=from_place
    obj.to_place=to_place
    obj.status="pending"
    obj.USER=User.objects.get(LOGIN_id=request.session['lid'])
    obj.TRANSPORT_id=id
    obj.save()
    return HttpResponse("<script>alert('Request sent'); window.location='/user_view_transport'</script>")

def user_view_concession_request(request):
    res=Concession.objects.filter(USER__LOGIN_id=request.session['lid'])
    return render(request, "User/view_concession_request_status.html", {'data':res})


def user_view_hospital(request):
    request.session['head'] = 'View Hospital'
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        trs = Hospital.objects.all()
        return render(request, 'User/view hospital.html', {'data': trs})
def user_send_feedback(request):
    return render(request, "User/send_feedback.html")
def user_send_feedback_post(request):
    feed=request.POST['textfield']
    obj=Feedback()
    obj.date=datetime.datetime.now().date()
    obj.feedback=feed
    obj.USER=User.objects.get(LOGIN_id=request.session['lid'])
    obj.save()
    return HttpResponse("<script>alert('Feedback sent'); window.location='/'</script>")
def user_view_panchayat(request):
    request.session['head'] = 'View Panchayat'
    if request.session == '':
        return HttpResponse("<script>alert('please login'); window.location='/'</script>")
    else:
        trs = Panchayat.objects.all()
        return render(request, 'User/view panchayat.html', {'data': trs})

def user_send_pension_request(request, id):
    return render(request, "User/pension.html", {'id':id})
def user_send_Request_post(request, id):
    file=request.FILES['textfield5']
    d=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fs=FileSystemStorage()
    fs.save(r"F:\DisabilityAid\disability_aid\static\pics\\" + d + ".pdf", file)
    path = "/static/pics" + d + ".pdf"
    obj=PEnsion()
    obj.file=path
    obj.USER=User.objects.get(LOGIN_id=request.session['lid'])
    obj.date=datetime.datetime.now().date()
    obj.PANCHAYAT_id=id
    obj.status="pending"
    obj.save()
    return HttpResponse("<script>alert('Requested'); window.location='/user_view_panchayat'</script>")




##################              PANCHAYT
def panchayat_home(request):
    return render(request, "panchayath/index.html")

def panchayat_view_requests(request):
    res=PEnsion.objects.filter(PANCHAYAT__LOGIN_id=request.session['lid'], status="pending")
    return render(request, "panchayath/view user request.html", {'data':res})

def pan_appr_request(request, id):
    PEnsion.objects.filter(id=id).update(status="Approved")
    return HttpResponse("<script>alert('Accepted'); window.location='/panchayat_view_requests'</script>")

def pan_rej_request(request, id):
    PEnsion.objects.filter(id=id).update(status="Rejected")
    return HttpResponse("<script>alert('Accepted'); window.location='/panchayat_view_requests'</script>")
