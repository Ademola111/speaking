from flask import render_template, request, redirect, flash, session
from abdieapp import app, db
from abdieapp.models import (Booking, Coaching)
from abdieapp.mail_utils import send_email, send_email_alert
from abdieapp.signals import (bookappointment_signal, coaching_signal)


""" homepage section """
@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template('user/index.html')
    
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        fullname = name.split()

        if name=="" or email=="":
            flash("one or more field is empty", "warning")
            return render_template('user/form.html', name=name, email=email, fullname=fullname)
        else:
            session['fullname']=fullname
            session['email']=email
            return redirect("/bookappointment/")


""" About section """
@app.route('/about/', methods=['GET', 'POST'])
def about():
    return render_template('user/about.html')


""" Speaking Section """
@app.route('/speaking/', methods=['GET', 'POST'])
def speaking():
    return render_template('user/speaking.html')


"""Coaching Section """
@app.route('/coaching/', methods=['GET', 'POST'])
def coaching():
    if request.method=='GET':
        return render_template('user/coaching.html')
    
    if request.method == 'POST':
        getfor = request.form
        fullname = getfor.get('fullname')
        phone = getfor.get('phone')
        email = getfor.get('email')
        
        if fullname =="" and phone =="" and email=="":
            flash('Kindly fill each fields', 'warning')
            return redirect(request.url)
        else:
            coachapp=Coaching(ch_fullname=fullname, ch_phone=phone, ch_email=email)
            db.session.add(coachapp)
            db.session.commit()
            commenter=Coaching.query.filter_by().first()
            commenter_email="abdiemohamed.tech@gmail.com"
            custom=commenter.ch_fullname
            recipients={"custom":custom}
            coaching_signal.send(app, comment=commenter, post_author_email=commenter_email, recipients=recipients)
            flash(f'You can start your assessment now ', 'success')
            jjj='https://docs.google.com/forms/d/e/1FAIpQLSdnOA1hL--euJHLAG7ICDoztr-3FNApSE1mnNxBD2J7A4GdnA/viewform?usp=header'
        return redirect(jjj)


""" book speaking appointment """
@app.route('/bookappointment/', methods=['GET', 'POST'])
def book_appointment():
    email = session.get('email')
    fullname = session.get('fullname')

    if request.method == 'GET':
        return render_template('user/form.html', fullname=fullname, email=email)

    if request.method == 'POST':
        getfor = request.form
        organisation = getfor.get('organisation')
        fname = getfor.get('fname')
        lname = getfor.get('lname')
        phone = getfor.get('phone')
        email = getfor.get('email')
        messag = getfor.get('message')
        budget = getfor.get('budget')
        datea = getfor.get('date')
        duration = getfor.get('duration')
        if organisation =="" or fname =="" or lname =="" or phone =="" or datea=="" or email=="" or messag =="" or budget=="" or duration=="":
            flash('Kindly fill each fields', 'warning')
            return redirect(request.url)
        else:
            bookapp=Booking(bk_organisation=organisation, bk_fname=fname,
                            bk_lname=lname, bk_phone=phone, bk_email=email, bk_bdate=datea,
                            bk_message=messag, bk_budget=budget, bk_duration=duration)
            db.session.add(bookapp)
            db.session.commit()
            commenter=Booking.query.filter_by().first()
            commenter_email="abdiemohamed.tech@gmail.com"
            custom=commenter.bk_fname + " " + commenter.bk_lname
            recipients={"custom":custom}
            bookappointment_signal.send(app, comment=commenter, 
                                        post_author_email=commenter_email, recipients=recipients)
            flash(f'You have made a successful booking with {custom}', 'success')
        return redirect('/')


""" signals connects """
@bookappointment_signal.connect
def send_bookappointment_email_alert(sender, comment, post_author_email, recipients): 
    subject = f"New Booking Alert {comment.bk_date}"
    body = (
        f"Hi Abdie Mohamed, \n\n"
        f"You have a booking from {comment.bk_fname}"+" "+ f" {comment.bk_lname}.\n"
        f"Organisation: {comment.bk_organisation}\n"
        f"Email: {comment.bk_email}\n"
        f"Phone Number: {comment.bk_phone}\n"
        f"Budget: ${comment.bk_budget} \n" 
        f"Message: {comment.bk_message} \n"
        f"Duration: {comment.bk_duration}\n"
        f"Event Date: {comment.bk_date} \n"
        )
    send_email_alert(subject, body, [post_author_email])

@coaching_signal.connect
def send_coaching_email_alert(sender, comment, post_author_email, recipients): 
    subject = f"New Coaching Alert {comment.ch_date}"
    body = (
        f"Hi Abdie Mohamed, \n\n"
        f"You have a new mentee {comment.ch_fullname}.\n"
        f"Email: {comment.ch_email}\n"
        f"Phone Number: {comment.ch_phone}\n"
        )
    send_email_alert(subject, body, [post_author_email])