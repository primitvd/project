from flask import Blueprint, render_template, request, flash, Response, make_response
from .models import *
from . import db
import datetime
from datetime import date
from sqlalchemy.sql import func
import pdfkit
from fpdf import FPDF

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
def home():
    if login.query.all() == ():
        manager = login(user_id="manager", password="admin")
        admin = login(user_id="admin", password="admin")
        db.session.add(manager)
        db.session.add(admin)
        db.session.commit()
    if request.method == 'POST':
        print("check")
    return render_template("home.html")

@views.route('/addreport', methods=['GET','POST'])
def addreport():
    if request.method == 'POST':
        print("check")
    return render_template("addreport.html")

@views.route('/baymanager', methods=['GET','POST'])
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
    return render_template("baymanager.html", bays = bays)

@views.route('/certificates', methods=['GET','POST'])
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
    return render_template("certificates.html",certificates=certificates)

@views.route('/dutyposting', methods=['GET','POST'])
def dutyposting():
    name = {}
    shift = {}
    bay = {}
    for employee1 in employee.query.all():
        name[employee1.emp_id] = employee.name
        shift[employee1.emp_id] = request.form.get("shift")
        bay[employee1.emp_id] = request.form.get("bay")
    if request.method == 'POST':
        for employee1 in employee.query.all():
            duty = duty_posting(date=date.today(), shift=shift[employee1.emp_id], bay=bay[employee1.emp_id])
            db.session.add(duty)
            db.session.commit()
            print("check")
    employees = employee.query.all()
    dutyposting = duty_posting.query.all()
    return render_template("dutyposting.html", employees = employees, name = name, shift = shift, bay = bay, dutyposting=dutyposting)

@views.route('/employeemanager', methods=['GET','POST'])
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
    return render_template("employeemanager.html", employees = employees)

@views.route('/fueldetails', methods=['GET','POST'])
def fueldetails():
    if request.method == 'POST':
        print("check")
    return render_template("fueldetails.html")

@views.route('/invmanager', methods=['GET','POST'])
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
    return render_template("invmanager.html", items = items)
    

@views.route('/reports', methods=['GET','POST'])
def reports():
    if request.method == 'POST':
        print("check")
    return render_template("reports.html")
    
@views.route('/fuelregister', methods=['GET','POST'])
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
    return render_template("fuelregister.html")

@views.route('/inventoryreport', methods=['GET','POST'])
def inventoryreport():
    if request.method == 'POST':
        print("check")
    return render_template("inventoryreport.html")

@views.route('/salesreport', methods=['GET','POST'])
def salesreport():
    sdate = request.form.get("sdate")
    edate = request.form.get("edate")
    print(sdate)
    print(edate)
    salelist = []
    pdf = FPDF()
    pdf.add_page()
    if request.method == 'POST':
        if(sdate > edate):
          flash("Start date should be before end date",category="False")

        if(sdate == '' or edate == ''):
           flash("Please select both dates",category="False")
        
        else:
            format_str = '%Y-%m-%d'
            sdate_obj = datetime.datetime.strptime(sdate, format_str)
            format_str = '%Y-%m-%d'
            edate_obj = datetime.datetime.strptime(edate, format_str)
            salelist = db.session.query(sales).filter(sales.date.between(sdate_obj, edate_obj)).all()
            print(salelist)


            result = login.query.all()

            
		
            page_width = pdf.w - 2 * pdf.l_margin
		
            pdf.set_font('Times','B',14.0) 
            pdf.cell(page_width, 0.0, 'Employee Data', align='C')
            pdf.ln(10)
            pdf.set_font('Courier', '', 12)
            col_width = page_width/2
		
            pdf.ln(1)
		
            th = pdf.font_size
		

            for row in result:
                pdf.cell(col_width, th, str(row.user_id), border=1)
                pdf.cell(col_width, th, row.password, border=1)
                pdf.ln(th)
		    
            pdf.ln(10)
		
            pdf.set_font('Times','',10.0) 
            pdf.cell(page_width, 0.0, '- end of report -', align='C')

            print(pdf)
        
    #     result = login.query.all()
    #     out = render_template("salesreportdownload.html", result = result)
    
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
    return render_template("salesreport.html", salelist=salelist)
