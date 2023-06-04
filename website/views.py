from io import BytesIO, StringIO
from flask import Blueprint, redirect, render_template, request, flash, Response, make_response, send_file, url_for
from flask_login import current_user, login_required
from sqlalchemy import and_
from .models import *
from . import db
import datetime
from datetime import date, timedelta
from sqlalchemy.sql import func
import pdfkit

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    format_str = '%Y-%m-%d'
    date = datetime.datetime.now().strftime(format_str)
    print(date)
    
    check = db.session.query(daily_price).filter(daily_price.date == date).all()
    print(check)

    # sdate_obj = datetime.datetime.now()
    # edate_obj = datetime.datetime.now()
    # salelist = db.session.query(sales).filter(sales.date.between(sdate_obj, edate_obj)).all()
    # print(salelist)


    a = 1
    if not check:
        a = 0
    resp = make_response(render_template("home.html", user=current_user, a=a, check = check))
    # resp.set_cookie("username")
    return resp

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
    format_str = '%Y-%m-%d'
    daily = db.session.query(daily_price).filter(daily_price.date == datetime.datetime.now().strftime('%Y-%m-%d')).first()
            
    # date1 = datetime.datetime.now().strftime(format_str)
    # print(date1)
    
    # daily = db.session.query(duty_posting).filter(duty_posting.date == date1).all()
    # print(daily)
    
    if request.method == 'POST':
        
        date_obj = datetime.datetime.strptime(date, format_str)
        print("check")
        sale = sales.query.filter_by(date = date_obj).first()
        check = db.session.query(employee).filter(employee.emp_id==emp_id).first()
        check.excess_short = check.excess_short + float(diff)
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
        saleid = db.session.query(func.max(sales.sid)).first()[0]
        if not saleid:
            saleid = 0
        for item in items:
            units_sold = int(request.form.get("units_sold"+str(item.inv_id)))
            amount = request.form.get("units_sale"+str(item.inv_id))
            item1 = inventory.query.filter_by(inv_id = item.inv_id).first()
            item1.stock -= units_sold
            itemsale = itemsales(sid = saleid+1,inv_id = item.inv_id,sale = amount)
            db.session.add(itemsale)



            # print(units_sold)
            # print(amount)

        # salelast = int(db.session.query(func.max(sale.sid)).scalar())+1
        # # salelast = int(sale.query.last().sid) + 1
        # print(salelast)
        # denom = denomination(sid=salelast, two_thousand=two_thousand, five_hundred=five_hundred, two_hundred=two_hundred, one_hundred=one_hundred, fifty=fifty, twenty=twenty, ten=ten, coins=coins)
        # db.session.add(denom)
        # db.session.commit()



        sale1 = sales(emp_id=emp_id, bay=bay, date=date_obj, shift=shift, ms_opening=ms_opening, ms_closing=ms_closing, ms_sales=ms_sales, ms_amount=ms_amount, hsd_opening=hsd_opening, hsd_closing=hsd_closing, hsd_sales=hsd_sales, hsd_amount=hsd_amount, two_thousand=two_thousand, five_hundred=five_hundred, two_hundred=two_hundred, one_hundred=one_hundred, fifty=fifty, twenty=twenty, ten=ten, coins=coins, pos=pos, ufill=ufill, upi=upi, smartfleet=smartfleet, smartdrive= smartdrive, pinelabs=pinelabs, stotal=s_total, dtotal=dtotal, diff=diff)
        db.session.add(sale1)
        db.session.commit()
        str1="Sale total ="+s_total+"*Collected = "+dtotal+"*Difference = "+diff
        flash(str1, category=True)


    # print(sales.query.all())
    employees = employee.query.all()
    bays = bay_manager.query.all()
    salelist=[]
    #salelist = db.session.query(sales).filter(sales.emp_id == "2").all()
    #print(salelist)
    # for k in sales1:
    #     print(k)

    # print(sales1)
    # print(sales1.coins)
    # print(sales1.twenty)
    # print(sales1.hsd_amount)
    # print(sales1.ms_amount)

    pays = payment_methods.query.all()
    # print(pays)
    return render_template("dailysales.html",user=current_user, employees=employees, items=items, bays=bays, pays=pays, daily=daily, date=datetime.datetime.now().strftime('%Y-%m-%d'))



@views.route('/baymanager', methods=['GET','POST'])
@login_required
def baymanager():
    bay_no = request.form.get("bay_no")
    MS = request.form.get("MS")
    HSD = request.form.get("HSD")
    if request.method == 'POST':
        bay = bay_manager(name=bay_no,hsd=HSD,ms=MS)
        db.session.add(bay)
        db.session.commit()
        flash("Data added!", category=True)
        print(MS,HSD)
    bays = bay_manager.query.order_by(bay_manager.name)
    return render_template("baymanager.html", bays = bays, user=current_user)

@views.route('/certificates', methods=['GET','POST'])
@login_required
def certificates():
    name = request.form.get("name")
    issue_date = request.form.get("issue_date")
    exp_date = request.form.get("exp_date")
    
    print(func.now)
    if request.method == 'POST':
        file = request.files["file"]

        format_str = '%Y-%m-%d'
        issue_date_obj = datetime.datetime.strptime(issue_date, format_str)
        exp_date_obj = datetime.datetime.strptime(exp_date, format_str)
        new_certificate = certificate(name=name, file_name = file.filename, exp_date=exp_date_obj, issue_date=issue_date_obj, file=file.read())
        db.session.add(new_certificate)
        db.session.commit()
        flash("Data added!", category=True)
        print("check")
    # format_str = '%Y-%m-%d' # The format
    # exp_date_obj = datetime.datetime.strptime(exp_date, '%Y-%m-%d')
    # print(datetime_obj.date())
    # print(exp_date)
    # print(datetime_obj)
    certificates = certificate.query.all()
    return render_template("certificates.html",certificates=certificates, user=current_user)

@views.route('/certificates/<name>')
def download(name):
    upload = certificate.query.filter_by(name=name).first()
    return send_file(BytesIO(upload.file),download_name=upload.file_name)

@views.route('/dutyposting', methods=['GET','POST'])
@login_required
def dutyposting():
    date = request.form.get("date")
    format_str = '%Y-%m-%d'
    if not date:
        date = datetime.datetime.now() 
    else:
        date = datetime.datetime.strptime(date, format_str)
    date1 = date.strftime(format_str)
    dutyposting = duty_posting.query.filter_by(date=date1).all() 
    # name = {}
    # shift1 = {}
    # bay1 = {}
    
    # for employee1 in employee.query.all():
    #     shift1[employee1.emp_id] = request.form.get("shift" + str(employee1.emp_id))
    #     bay1[employee1.emp_id] = request.form.get("bay" + str(employee1.emp_id))
    # for employee1 in employee.query.all():
    #     for duty in duty_posting.query.all():
    #         if duty.emp_id == employee1.emp_id:
    #             name.update({employee1.emp_id : employee1.name})
    #             shift1.update({employee1.emp_id : duty.shift})
    #             bay1.update({employee1.emp_id : duty.bay})
    if request.method == 'POST':
        for employees in employee.query.all():
            check = 1
            shift = request.form.get("shift" + str(employees.emp_id))
            print(shift)
            bay = request.form.get("bay" + str(employees.emp_id))
            print(bay)
            for duty in dutyposting:
                if duty.emp_id == employees.emp_id:
                    if shift and bay:
                        check = 0
                        duty.shift = shift
                        duty.bay = bay
                        print(check)
            if shift and bay and check:
                duty = duty_posting(date=date, emp_id=employees.emp_id, shift=shift, bay=bay, name=employees.name)
                print(check)
                db.session.add(duty)
            db.session.commit()
            # flash("Data added!", category=True)
            print("check")
    # print(shift)
    # print(bay)
    employees = employee.query.all()
    bays = bay_manager.query.all()
    print(employees)
    print(dutyposting)
    return render_template("dutyposting.html", user=current_user, employees = employees, dutyposting=dutyposting, bays=bays, date=datetime.datetime.now().strftime('%Y-%m-%d'))

@views.route('/employeemanager', methods=['GET','POST'])
@login_required
def employeemanager(id=0):
    id = request.form.get("id")
    name = request.form.get("name")
    dob = request.form.get("dob")
    address = request.form.get("address")
    phone = request.form.get("phone")
    advance = request.form.get("advance")
    excess_short = request.form.get("excess_short")
    check = db.session.query(employee).filter(employee.emp_id==id).first()
    check = employee.query.get(id)
    print(check)
    if request.method == 'POST':
        if check:
            check.name = name
            # check.dob = dob_obj
            check.address = address
            check.phone = phone
            check.advance = advance
            check.excess_short = excess_short
            db.session.commit()
        else:
            format_str = '%Y-%m-%d'
            dob_obj = datetime.datetime.strptime(dob, format_str)
            emp = employee(name=name,dob = dob_obj, address=address, phone=phone, advance=advance, excess_short=0)
            db.session.add(emp)
            db.session.commit()
        print("check")
    employees = employee.query.all()
    return render_template("employeemanager.html", user=current_user, employees = employees, check = check)

@views.route('/fueldetails', methods=['GET','POST'])
@login_required
def fueldetails():
    type = request.form.get("type")
    date = request.form.get("date")
    morning_density = request.form.get("morning_density")
    morning_temp = request.form.get("morning_temp")
    density15 = request.form.get("density15")
    rec_invoice = request.form.get("rec_invoice")
    rec_qty = request.form.get("rec_qty")
    rec_obs_density = request.form.get("rec_obs_density")
    rec_obs_temp = request.form.get("rec_obs_temp")
    rec_density15 = request.form.get("rec_density15")
    cash_density15 = request.form.get("cash_density15")
    diff = request.form.get("diff")
    afterdeca_obs_density = request.form.get("afterdeca_obs_density")
    afterdeca_obs_temp = request.form.get("afterdeca_obs_temp")
    afterdeca_obs_density15 = request.form.get("afterdeca_obs_density15")
    check=[]
    # format_str = '%Y-%m-%d'
    # if date:
    #     date_obj = datetime.datetime.strptime(date, format_str)
    #     date2_obj = date_obj.strftime(format_str)
    #     print("3")
    #     print(date2_obj)
    # else:
    #     date_obj = datetime.datetime.now()
    #     date2_obj = date_obj.strftime(format_str)
    #     print(date2_obj)
    #     print("4")

    
    # check = db.session.query(fuel_reg).filter(date == date2_obj).first()
    # print(db.session.query(fuel_reg).first().date)

    # print(check)
    

    format_str = '%Y-%m-%d'
    if date:
        date_obj = datetime.datetime.strptime(date, format_str)
        date2_obj = date_obj.strftime(format_str)
        print("3")
        print(date2_obj)
    else:
        date_obj = datetime.datetime.now()
        date2_obj = date_obj.strftime(format_str)
        print(date2_obj)
        print("4")


    check = db.session.query(fuel_reg).filter(fuel_reg.date==date2_obj,fuel_reg.type==type).first()
    # print(db.session.query(fuel_reg).first().date)


    if request.method == 'POST':

        print(check)
        if check:
            check.type=type
            check.date=date_obj
            check.morning_density=morning_density
            check.morning_temp=morning_temp
            check.density15=density15
            check.rec_invoice=rec_invoice
            check.rec_qty=rec_qty
            check.rec_obs_density=rec_obs_density
            check.rec_obs_temp=rec_obs_temp
            check.rec_density15=rec_density15
            check.cash_density15=cash_density15
            check.diff=diff
            check.afterdeca_obs_density=afterdeca_obs_density
            check.afterdeca_obs_temp=afterdeca_obs_temp
            check.afterdeca_obs_density15=afterdeca_obs_density15
            print("2")
            db.session.commit()
            flash("Data added!", category=True)

        else:
            newfuel = fuel_reg(type=type, date=date_obj, morning_density=morning_density, morning_temp=morning_temp, density15=density15, rec_invoice=rec_invoice, rec_qty=rec_qty, rec_obs_density=rec_obs_density, rec_obs_temp=rec_obs_temp, rec_density15=rec_density15, cash_density15=cash_density15, diff=diff, afterdeca_obs_density=afterdeca_obs_density, afterdeca_obs_temp=afterdeca_obs_temp, afterdeca_obs_density15=afterdeca_obs_density15)
            db.session.add(newfuel)
            print("1")
            db.session.commit()
            flash("Data added!", category=True)
        print("check")
    return render_template("fueldetails.html", user=current_user, check=check, date=datetime.datetime.now().strftime('%Y-%m-%d'))

@views.route('/invmanager', methods=['GET','POST'])
@login_required
def invmanager():
    name = request.form.get("name")
    stock = request.form.get("stock")
    price = request.form.get("price")
    check = db.session.query(inventory).filter(inventory.name==name).first()

    if request.method == 'POST' and name:
        print(name)
        if check:
            check.name = name
            check.stock = stock
            check.price = price
        else:
            inv = inventory(name=name, stock=stock, price=price)
            db.session.add(inv)
        db.session.commit()
        flash("Data added!", category=True)
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
    if not sdate:
        sdate="2000-01-01"
    edate = request.form.get("edate")
    if not edate:
        edate="3000-01-01"
    type = request.form.get("type")
    salelist=[]
    if request.method == 'POST':
        format_str = '%Y-%m-%d'
        sdate_obj = datetime.datetime.strptime(sdate, format_str)
        edate_obj = datetime.datetime.strptime(edate, format_str)
        sdate_obj = sdate_obj - timedelta(days=1)

        if(sdate > edate):
          flash("Start date should be before end date",category="False")

        # print(sdate)
        # print(edate)
        # print(emp_id)
        # print("check")

        else:
            salelist = db.session.query(fuel_reg).filter(fuel_reg.date.between(sdate_obj, edate_obj),fuel_reg.type == type).all()

        print(salelist)
    return render_template("fuelregister.html", user=current_user, salelist=salelist, sdate=sdate, edate=edate, type=type)

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
    if not sdate:
        sdate="2000-01-01"
    edate = request.form.get("edate")
    if not edate:
        edate="3000-01-01"
    salelist = []
    itemlist = []
    items1 = inventory.query.all()
    # pdf = FPDF()
    # pdf.add_page()
    if request.method == 'POST':
        if(sdate > edate):
          flash("Start date should be before end date",category="False")
        
        else:
            format_str = '%Y-%m-%d'
            sdate_obj = datetime.datetime.strptime(sdate, format_str)
            edate_obj = datetime.datetime.strptime(edate, format_str)
            sdate_obj = sdate_obj - timedelta(days=1)

            salelist = db.session.query(sales).filter(sales.date.between(sdate_obj, edate_obj)).all()
            for sale in salelist:
                itemss = db.session.query(itemsales).filter(itemsales.sid == sale.sid).all()
                if itemss != []:
                    itemlist.append(itemss)

            print(items1)

        for items in items1:
            for item1 in itemlist:
                for item in item1:
                    if items.inv_id == item.inv_id:
                        items.price = items.price + item.sale

    

        
        print("check")
    employees = employee.query.all()
    items = inventory.query.all()
    return render_template("salesreport.html", user=current_user, salelist=salelist, sdate=sdate, edate=edate, itemlist=itemlist, items=items, employees=employees, items1=items1)


@views.route('/addpaymentmethod', methods=['GET', 'POST'])
@login_required
def addpaymentmethod():
    pay = request.form.get("payment_method")
    if request.method == 'POST':
        payment = payment_methods(payment_method=pay)
        db.session.add(payment)
        db.session.commit()
        flash("Data added!", category=True)
    print("check")
    pays = payment_methods.query.all()
    return render_template("addpaymentmethod.html", user=current_user, pays=pays)


@views.route('/employeereport', methods=['GET','POST'])
@login_required
def employeereport():
    employees=employee.query.all()
    sdate = request.form.get("sdate")
    if not sdate:
        sdate="2000-01-01"
    edate = request.form.get("edate")
    if not edate:
        edate="3000-01-01"
    emp_id = request.form.get("emp_id")
    salelist=[]
    itemlist = []
    response = make_response()
    if request.method == 'POST':
        format_str = '%Y-%m-%d'
        sdate_obj = datetime.datetime.strptime(sdate, format_str)
        edate_obj = datetime.datetime.strptime(edate, format_str)
        sdate_obj = sdate_obj - timedelta(days=1)

        if(sdate > edate):
          flash("Start date should be before end date",category="False")

        else:
            salelist = db.session.query(sales).filter(sales.date.between(sdate_obj, edate_obj),sales.emp_id == emp_id).all()
            for sale in salelist:
                itemss = db.session.query(itemsales).filter(itemsales.sid == sale.sid).all()
                if itemss != []:
                    itemlist.append(itemss)

    #     html = render_template("employeereport.html", user=current_user, employees=employees, salelist=salelist)

    # # Convert HTML to PDF
    #     options = {
    #         'page-size': 'A4',
    #         'margin-top': '0.75in',
    #         'margin-right': '0.75in',
    #         'margin-bottom': '0.75in',
    #         'margin-left': '0.75in',
    #         }
    #     pdf = pdfkit.from_string(html, False, options=options)

    # Return the PDF as a response
        # response = make_response(pdf)
        # response.headers['Content-Type'] = 'application/pdf'
        # response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
    print(salelist)
    items = inventory.query.all()
    return render_template("employeereport.html", user=current_user, employees=employees, salelist=salelist, sdate=sdate, edate=edate, emp_id=emp_id, itemlist=itemlist, items=items )

@views.route('/dailyprice', methods=['GET','POST'])
@login_required
def dailyprice():
    date1 = request.form.get("date")
    ms = request.form.get("ms_price")
    hsd = request.form.get("hsd_price")
    date=datetime.datetime.now().strftime('%Y-%m-%d')
    daily = db.session.query(daily_price).filter(daily_price.date == date).first()
    if request.method == 'POST':
        if date1:
            format_str = '%Y-%m-%d'
            date1_obj = datetime.datetime.strptime(date1, format_str)
            date_obj = datetime.datetime.strptime(date1, format_str).strftime(format_str)
            print(date_obj)
            daily = db.session.query(daily_price).filter(daily_price.date == date_obj).first()
            print(daily)
            if daily:
                daily.ms_price = ms
                daily.hsd_price = hsd
                print("1")
            else:
                daily = daily_price(date=date1_obj,ms_price=ms,hsd_price=hsd)
                db.session.add(daily)
                print("2")
            db.session.commit() 
            flash("Data added!", category=True)
            return redirect(url_for('views.home'))
        else:
            flash("Enter date", category=False)  
        
        print("check")
    print(daily)
    return render_template("dailyprice.html", user=current_user, date=datetime.datetime.now().strftime('%Y-%m-%d'),daily=daily)



@views.route('/dailypricereport', methods=['GET','POST'])
@login_required
def dailypricereport():
    # daily = daily_price.query.all()
    sdate = request.form.get("sdate")
    if not sdate:
        sdate="2000-01-01"
    edate = request.form.get("edate")
    if not edate:
        edate="3000-01-01"
    dailylist=[]
    if request.method == 'POST':
        format_str = '%Y-%m-%d'
        sdate_obj = datetime.datetime.strptime(sdate, format_str)
        edate_obj = datetime.datetime.strptime(edate, format_str)
        sdate_obj = sdate_obj - timedelta(days=1)

        if(sdate > edate):
          flash("Start date should be before end date",category="False")

        else:
            dailylist = db.session.query(daily_price).filter(daily_price.date.between(sdate_obj, edate_obj)).all()

    # print(salelist)
    return render_template("dailypricereport.html", user=current_user, dailylist=dailylist, sdate=sdate, edate=edate)


@views.route('/dailypricepdf')
def dailypricepdf():
    sdate = request.args.get('sdate',None)
    edate = request.args.get('edate',None)
    dailylist=[]
    
    format_str = '%Y-%m-%d'
    sdate_obj = datetime.datetime.strptime(sdate, format_str)
    edate_obj = datetime.datetime.strptime(edate, format_str)
    sdate_obj = sdate_obj - timedelta(days=1)

    if(sdate > edate):
      flash("Start date should be before end date",category="False")

    else:
        dailylist = db.session.query(daily_price).filter(daily_price.date.between(sdate_obj, edate_obj)).all()

    print(list)
    html =  render_template("dailypricepdf.html", dailylist=dailylist, sdate=sdate, edate=edate)

    # Convert HTML to PDF
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }
    pdf = pdfkit.from_string(html, False, options=options)
    print(id)
    print(sdate)
    # Return the PDF as a response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=dailyprice.pdf'
    return response

@views.route('/dutypostingreport', methods=['GET','POST'])
@login_required
def dutypostingreport():
    # daily = daily_price.query.all()
    sdate = request.form.get("sdate")
    if not sdate:
        sdate="2000-01-01"
    edate = request.form.get("edate")
    if not edate:
        edate="3000-01-01"
    dailylist=[]
    if request.method == 'POST':
        format_str = '%Y-%m-%d'
        sdate_obj = datetime.datetime.strptime(sdate, format_str)
        edate_obj = datetime.datetime.strptime(edate, format_str)
        sdate_obj = sdate_obj - timedelta(days=1)

        if(sdate > edate):
          flash("Start date should be before end date",category="False")

        else:
            dailylist = db.session.query(duty_posting).filter(duty_posting.date.between(sdate_obj, edate_obj)).all()

    # print(salelist)
    return render_template("dutypostingreport.html", user=current_user, dailylist=dailylist, sdate=sdate, edate=edate)


@views.route('/dutypostingpdf')
def dutypostingpdf():
    sdate = request.args.get('sdate',None)
    edate = request.args.get('edate',None)
    dailylist=[]
    
    format_str = '%Y-%m-%d'
    sdate_obj = datetime.datetime.strptime(sdate, format_str)
    edate_obj = datetime.datetime.strptime(edate, format_str)
    sdate_obj = sdate_obj - timedelta(days=1)

    if(sdate > edate):
      flash("Start date should be before end date",category="False")

    else:
        dailylist = db.session.query(duty_posting).filter(duty_posting.date.between(sdate_obj, edate_obj)).all()

    print(list)
    html =  render_template("dutypostingpdf.html", dailylist=dailylist, sdate=sdate, edate=edate)

    # Convert HTML to PDF
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }
    pdf = pdfkit.from_string(html, False, options=options)
    print(id)
    print(sdate)
    # Return the PDF as a response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=dutyposting.pdf'
    return response

@views.route('/delete_employee/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    employees = employee.query.get(id)
    db.session.delete(employees)
    db.session.commit()
    flash('Employee details have been deleted!', 'success')
    return redirect(url_for('views.employeemanager'))

@views.route('/clear_employee/<int:id>', methods=['GET', 'POST'])
@login_required
def clear_employee(id):
    employees = employee.query.get(id)
    employees.excess_short = 0 
    db.session.commit()
    msg = "Excess/Short for "+employees.name+" has been cleared "
    flash(msg, 'success')
    return redirect(url_for('views.employeemanager'))
    

@views.route('/delete_bay/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_bay(id):
    bay = bay_manager.query.get(id)
    db.session.delete(bay)
    db.session.commit()
    flash('Bay details have been deleted!', 'success')
    return redirect(url_for('views.baymanager'))

@views.route('/delete_inventory/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_inventory(id):
    item = inventory.query.get(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item details have been deleted!', 'success')
    return redirect(url_for('views.invmanager'))

@views.route('/delete_payment/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_payment(id):
    pay = payment_methods.query.get(id)
    db.session.delete(pay)
    db.session.commit()
    flash('Payment method has been deleted!', 'success')
    return redirect(url_for('views.addpaymentmethod'))

@views.route('/delete_certificate/<name>', methods=['GET', 'POST'])
@login_required
def delete_certificate(name):
    cert = certificate.query.get(name)
    db.session.delete(cert)
    db.session.commit()
    flash('Certificate has been deleted!', 'success')
    return redirect(url_for('views.certificates'))


@views.route('/employeepdf')
def employeepdf():
    itemlist = []
    sdate = request.args.get('sdate',None)
    edate = request.args.get('edate',None)
    id = request.args.get('id',None)


    format_str = '%Y-%m-%d'
    sdate_obj = datetime.datetime.strptime(sdate, format_str)
    edate_obj = datetime.datetime.strptime(edate, format_str)
    sdate_obj = sdate_obj - timedelta(days=1)

    salelist = db.session.query(sales).filter(sales.date.between(sdate_obj, edate_obj),sales.emp_id == id).all()
    for sale in salelist:
        itemss = db.session.query(itemsales).filter(itemsales.sid == sale.sid).all()
        if itemss != []:
            itemlist.append(itemss)
    # salelist = request.args.get('salelist',None)
    print(salelist)
    
    items = inventory.query.all()
    html = render_template("employeepdf.html", salelist=salelist, itemlist=itemlist, items=items)

    # Convert HTML to PDF
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }
    pdf = pdfkit.from_string(html, False, options=options)
    print(id)
    print(sdate)
    # Return the PDF as a response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=employee '+id+'.pdf'
    return response


@views.route('/salespdf')
def salespdf():
    itemlist = []
    sdate = request.args.get('sdate',None)
    edate = request.args.get('edate',None)


    format_str = '%Y-%m-%d'
    sdate_obj = datetime.datetime.strptime(sdate, format_str)
    edate_obj = datetime.datetime.strptime(edate, format_str)
    sdate_obj = sdate_obj - timedelta(days=1)

    
    salelist = db.session.query(sales).filter(sales.date.between(sdate_obj, edate_obj)).all()
    salelist = db.session.query(sales).filter(sales.date.between(sdate_obj, edate_obj)).all()
    for sale in salelist:
        itemss = db.session.query(itemsales).filter(itemsales.sid == sale.sid).all()
        if itemss != []:
            itemlist.append(itemss)
    # salelist = request.args.get('salelist',None)
    print(salelist)
    
    employees = employee.query.all()
    items = inventory.query.all()

    html = render_template("salespdf.html", salelist=salelist, itemlist=itemlist, items=items, employees=employees, items1=items1)

    # Convert HTML to PDF
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }
    pdf = pdfkit.from_string(html, False, options=options)
    print(id)
    print(sdate)
    # Return the PDF as a response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=sales '+edate+' - '+sdate+'.pdf'
    return response



@views.route('/fuelpdf')
def fuelpdf():
    sdate = request.args.get('sdate',None)
    edate = request.args.get('edate',None)
    type = request.args.get('type',None)


    format_str = '%Y-%m-%d'
    sdate_obj = datetime.datetime.strptime(sdate, format_str)
    edate_obj = datetime.datetime.strptime(edate, format_str)
    sdate_obj = sdate_obj - timedelta(days=1)
    
    salelist = db.session.query(fuel_reg).filter(fuel_reg.date.between(sdate_obj, edate_obj),fuel_reg.type == type).all()
    # salelist = request.args.get('salelist',None)
    print(salelist)
    

    html = render_template("fuelpdf.html", salelist=salelist)

    # Convert HTML to PDF
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'orientation': 'landscape',
    }
    pdf = pdfkit.from_string(html, False, options=options)

    print(sdate)
    # Return the PDF as a response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=fuel '+sdate+' - '+edate+'.pdf'
    return response



























