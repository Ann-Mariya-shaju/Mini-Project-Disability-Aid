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


