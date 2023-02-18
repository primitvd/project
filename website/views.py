from flask import Blueprint, render_template, request, flash, Response, make_response
from flask_login import current_user, login_required
from sqlalchemy import and_
from .models import *
from . import db
import datetime
from datetime import date
from sqlalchemy.sql import func
import pdfkit
# from fpdf import FPDF

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():

    # sdate_obj = datetime.datetime.now()
    # edate_obj = datetime.datetime.now()
    # salelist = db.session.query(sales).filter(sales.date.between(sdate_obj, edate_obj)).all()
    # print(salelist)


    check = 0
    a = 1
    if not check:
        a = 0
    return render_template("home.html", user=current_user, a=a)

@views.route('/dailysales', methods=['GET','POST'])
@login_required
def dailysales():
    items = inventory.query.all()
    date = request.form.get("date")
    emp_id = request.form.get("emp_id")
    bay = request.form.get("bay")
    shift = request.form.get("shift")
    ms_opening = request.form.get("ms_opening")
    ms_closing = request.form.get("ms_closing")
    ms_sales = request.form.get("ms_sales")
    ms_amount = request.form.get("ms_amount")
    hsd_opening = request.form.get("hsd_opening")
    hsd_closing = request.form.get("hsd_closing")
    hsd_sales = request.form.get("hsd_sales")
    hsd_amount = request.form.get("hsd_amount")
    s_total = request.form.get("stotal")

    two_thousand = request.form.get("two_thousand")
    five_hundred = request.form.get("five_hundred")
    two_hundred = request.form.get("two_hundred")
    one_hundred = request.form.get("one_hundred")
    fifty = request.form.get("fifty")
    twenty = request.form.get("twenty")
    ten = request.form.get("ten")
    coins = request.form.get("coins")
    

    pos = request.form.get("pos")
    ufill = request.form.get("ufill")
    upi = request.form.get("upi")
    smartfleet = request.form.get("smartfleet")
    smartdrive = request.form.get("smartdrive")
    pinelabs = request.form.get("pinelabs")
    dtotal = request.form.get("dtotal")
    diff = request.form.get("diff")
    
    if request.method == 'POST':
        format_str = '%Y-%m-%d'
        date_obj = datetime.datetime.strptime(date, format_str)
        print("check")
        sale = sales.query.filter(date=date_obj).first()
        # if sale:
        #     if sale.emp_id==emp_id and sale.shift==shift:
        #         print(sales)
        # if sale:
        #     sale.ms_opening = ms_opening
        #     sale.ms_closing = ms_closing
        #     sale.ms_sale = ms_sales
        #     sale.ms_amount = ms_amount
        #     sale.hsd_opening = hsd_opening
        #     sale.hsd_closing = hsd_closing
        #     sale.hsd_sale = hsd_sales
        #     sale.hsd_amount = hsd_amount
        # else:

        for item in items:
            units_sold = int(request.form.get("units_sold"+str(item.inv_id)))
            amount = request.form.get("units_sale"+str(item.inv_id))
            item1 = inventory.query.filter(inv_id=item.inv_id).first()
            item1.stock -= units_sold
            # print(units_sold)
            # print(amount)

        # salelast = int(db.session.query(func.max(sale.sid)).scalar())+1
        # # salelast = int(sale.query.last().sid) + 1
        # print(salelast)
        # denom = denomination(sid=salelast, two_thousand=two_thousand, five_hundred=five_hundred, two_hundred=two_hundred, one_hundred=one_hundred, fifty=fifty, twenty=twenty, ten=ten, coins=coins)
        # db.session.add(denom)
        # db.session.commit()



        sale1 = sales(emp_id=emp_id, bay=bay, date=date_obj, shift=shift, ms_opening=ms_opening, ms_closing=ms_closing, ms_sales=ms_sales, ms_amount=ms_amount, hsd_opening=hsd_opening, hsd_closing=hsd_closing, hsd_sales=hsd_sales, hsd_amount=hsd_amount, two_thousand=two_thousand, five_hundred=five_hundred, two_hundred=two_hundred, one_hundred=one_hundred, fifty=fifty, twenty=twenty, ten=ten, coins=coins, pos=pos, ufill=ufill, upi=upi, smartfleet=smartfleet, smartdrive= smartdrive, pinelabs=pinelabs)
        db.session.add(sale1)
        db.session.commit()

    # print(sales.query.all())
    employees = employee.query.all()
    salelist=[]
    #salelist = db.session.query(sales).filter(sales.emp_id == "2").all()
    print(salelist)
    # for k in sales1:
    #     print(k)

    # print(sales1)
    # print(sales1.coins)
    # print(sales1.twenty)
    # print(sales1.hsd_amount)
    # print(sales1.ms_amount)

    pays = payment_method.query.all()
    # print(pays)
    return render_template("dailysales.html",user=current_user, employees=employees, items=items,pays=pays)



@views.route('/baymanager', methods=['GET','POST'])
@login_required
def baymanager():
    MS = request.form.get("MS")
    HSD = request.form.get("HSD")
    if request.method == 'POST':
        bay = bay_manager(hsd=HSD,ms=MS)
        db.session.add(bay)
        db.session.commit()
        data1 = bay_manager.query.all()
        print(MS,HSD)
    bays = bay_manager.query.all()
    return render_template("baymanager.html", bays = bays, user=current_user)

@views.route('/certificates', methods=['GET','POST'])
@login_required
def certificates():
    name = request.form.get("name")
    issue_date = request.form.get("issue_date")
    exp_date = request.form.get("exp_date")
    file = request.form.get("file")
    print(func.now)
    if request.method == 'POST':
        format_str = '%Y-%m-%d'
        issue_date_obj = datetime.datetime.strptime(issue_date, format_str)
        exp_date_obj = datetime.datetime.strptime(exp_date, format_str)
        new_certificate = certificate(name=name, exp_date=exp_date_obj, issue_date=issue_date_obj)
        db.session.add(new_certificate)
        db.session.commit()
        print("check")
    # format_str = '%Y-%m-%d' # The format
    # exp_date_obj = datetime.datetime.strptime(exp_date, '%Y-%m-%d')
    # print(datetime_obj.date())
    # print(exp_date)
    # print(datetime_obj)
    certificates = certificate.query.all()
    return render_template("certificates.html",certificates=certificates, user=current_user)

@views.route('/dutyposting', methods=['GET','POST'])
@login_required
def dutyposting():
    date = request.form.get("date")
    name = {}
    shift1 = {}
    bay1 = {}
    
    for employee1 in employee.query.all():
        shift1[employee1.emp_id] = request.form.get("shift" + str(employee1.emp_id))
        bay1[employee1.emp_id] = request.form.get("bay" + str(employee1.emp_id))
    # for employee1 in employee.query.all():
    #     for duty in duty_posting.query.all():
    #         if duty.emp_id == employee1.emp_id:
    #             name.update({employee1.emp_id : employee1.name})
    #             shift1.update({employee1.emp_id : duty.shift})
    #             bay1.update({employee1.emp_id : duty.bay})
    if request.method == 'POST':
        if date:
            format_str = '%Y-%m-%d'
            date = datetime.datetime.strptime(date, format_str)
        for employee1 in employee.query.all():
            duty = duty_posting(date=date, emp_id=employee1.emp_id, shift=shift1[employee1.emp_id], bay=bay1[employee1.emp_id])
            db.session.add(duty)
            db.session.commit()
            print("check")
    print(shift1)
    print(bay1)
    employees = employee.query.all()
    print(employees)
    dutyposting = duty_posting.query.filter(date=date).all()
    print(dutyposting)
    return render_template("dutyposting.html", user=current_user, employees = employees, name = name, shift = shift1, bay = bay1, dutyposting=dutyposting)

@views.route('/employeemanager', methods=['GET','POST'])
@login_required
def employeemanager():
    name = request.form.get("name")
    dob = request.form.get("dob")
    address = request.form.get("address")
    phone = request.form.get("phone")
    advance = request.form.get("advance")
    if request.method == 'POST':
        format_str = '%Y-%m-%d'
        dob_obj = datetime.datetime.strptime(dob, format_str)
        emp = employee(name=name, dob=dob_obj, address=address, phone=phone, advance=advance, excess_short=0)
        db.session.add(emp)
        db.session.commit()
        print("check")
    employees = employee.query.all()
    return render_template("employeemanager.html", user=current_user, employees = employees)

@views.route('/fueldetails', methods=['GET','POST'])
@login_required
def fueldetails():

    if request.method == 'POST':
        print("check")
    return render_template("fueldetails.html", user=current_user)

@views.route('/invmanager', methods=['GET','POST'])
@login_required
def invmanager():
    name = request.form.get("name")
    stock = request.form.get("stock")
    price = request.form.get("price")
    
    if request.method == 'POST':
        inv = inventory(name=name, stock=stock, price=price)
        db.session.add(inv)
        db.session.commit()
        print("check")
    items = inventory.query.all()
    return render_template("invmanager.html", user=current_user, items = items)
    

@views.route('/reports', methods=['GET','POST'])
@login_required
def reports():
    if request.method == 'POST':
        print("check")
    return render_template("reports.html", user=current_user)
    
@views.route('/fuelregister', methods=['GET','POST'])
@login_required
def fuelregister():
    sdate = request.form.get("sdate")
    edate = request.form.get("edate")
    print(sdate)
    print(edate)
    if request.method == 'POST':
        sdate = request.form.get("sdate")
        edate = request.form.get("edate")
        print(sdate)
        print(edate)
        print("check")
    return render_template("fuelregister.html", user=current_user)

@views.route('/inventoryreport', methods=['GET','POST'])
@login_required
def inventoryreport():
    if request.method == 'POST':
        print("check")
    return render_template("inventoryreport.html", user=current_user)

@views.route('/salesreport', methods=['GET','POST'])
@login_required
def salesreport():
    sdate = request.form.get("sdate")
    edate = request.form.get("edate")
    print(sdate)
    print(edate)
    salelist = []
    # pdf = FPDF()
    # pdf.add_page()
    if request.method == 'POST':
        if(sdate > edate):
          flash("Start date should be before end date",category="False")

        if(sdate == '' or edate == ''):
           flash("Please select both dates",category="False")
        
        else:
            format_str = '%Y-%m-%d'
            sdate_obj = datetime.datetime.strptime(sdate, format_str)
            edate_obj = datetime.datetime.strptime(edate, format_str)
            salelist = db.session.query(sales).filter(sales.date.between(sdate_obj, edate_obj)).all()
            print(salelist)


            result = logins.query.all()

            
		
            # page_width = pdf.w - 2 * pdf.l_margin
		
            # pdf.set_font('Times','B',14.0) 
            # pdf.cell(page_width, 0.0, 'Employee Data', align='C')
            # pdf.ln(10)
            # pdf.set_font('Courier', '', 12)
            # col_width = page_width/2
		
            # pdf.ln(1)
		
            # th = pdf.font_size
		

            # for row in result:
            #     pdf.cell(col_width, th, str(row.user_id), border=1)
            #     pdf.cell(col_width, th, row.password, border=1)
            #     pdf.ln(th)
		    
            # pdf.ln(10)
		
            # pdf.set_font('Times','',10.0) 
            # pdf.cell(page_width, 0.0, '- end of report -', align='C')

            # print(pdf)
        
    #     result = login.query.all()
    #     out = render_template("salesreportdownload.html", user=current_user, result = result)
    
    # # PDF options   
    #     options = {
    #         "orientation": "landscape",
    #         "page-size": "A4",
    #         "margin-top": "1.0cm",
    #         "margin-right": "1.0cm",
    #         "margin-bottom": "1.0cm",
    #         "margin-left": "1.0cm",
    #         "encoding": "UTF-8",
    #     }
    
    # # Build PDF from HTML 
    #     pdf = pdfkit.from_string(out, options=options)


        # response = make_response(pdf)
        # response.headers["Content-Type"] = "application/pdf"
        # response.headers["Content-Disposition"] = "inline; filename=output.pdf"




        print("check")
    return render_template("salesreport.html", user=current_user, salelist=salelist)

@views.route('/addpaymentmethod', methods=['GET','POST'])
@login_required
def addpaymentmethod():
    pay = request.form.get("payment_method")
    pays = []
    if request.method == 'POST':
        if not pays:
            payment = payment_method(payment_method=pay)
            db.session.add(payment)
            db.session.commit()
        else:
            flash('Payment method already exists', category='error')
        print("check")
    pays = payment_method.query.all()
    return render_template("addpaymentmethod.html", user=current_user, pays=pays)


@views.route('/employeereport', methods=['GET','POST'])
@login_required
def employeereport():
    sdate = request.form.get("sdate")
    edate = request.form.get("edate")
    emp_id = request.form.get("emp_id")
    print(sdate)
    print(edate)
    salelist=[]
    if request.method == 'POST':
        format_str = '%Y-%m-%d'
        sdate_obj = datetime.datetime.strptime(sdate, format_str)
        edate_obj = datetime.datetime.strptime(edate, format_str)
        print(sdate)
        print(edate)
        print(emp_id)
        print("check")
        #salelist = db.session.query(sales).filter(sales.date.between(sdate_obj, edate_obj)).all()


        salelist = db.session.query(sales).filter(
        sales.date.between(sdate_obj, edate_obj),
        sales.emp_id == emp_id).all()

        print(salelist)
    employees=employee.query.all()
    return render_template("employeereport.html", user=current_user, employees=employees, salelist=salelist)

@views.route('/dailyprice', methods=['GET','POST'])
@login_required
def dailyprice():
    date1 = request.form.get("date")
    ms = request.form.get("ms_price")
    hsd = request.form.get("hsd_price")
    
    if request.method == 'POST':
        # print(date)
        # print(ms)
        # print(hsd)
        if date1:
            format_str = '%Y-%m-%d'
            date_obj = datetime.date.strptime(date1, format_str)
            print(date_obj)
            daily = db.session.query(daily_price).filter(date == date_obj).first()
            if daily:
                daily.ms_price = ms
                daily.hsd_price = hsd
                print("1")
            else:
                daily = daily_price(date=date_obj,ms_price=ms,hsd_price=hsd)
                db.session.add(daily)
                print("2")
            #db.session.commit() 
        else:
            flash("Enter date", category=False)  
        
        print("check")
        
    return render_template("dailyprice.html", user=current_user)