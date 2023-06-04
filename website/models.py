from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class logins(db.Model, UserMixin):
    user_id = db.Column(db.String(150), primary_key = True)
    password = db.Column(db.String(150))
    def get_id(self):
           return (self.user_id)

class inventory(db.Model):
    inv_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    stock = db.Column(db.Integer)
    price = db.Column(db.Integer)

class fuel_reg(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(10))
    date = db.Column(db.Date, default=func.now())
    morning_density = db.Column(db.Float)
    morning_temp = db.Column(db.Float)
    density15 = db.Column(db.Float)
    rec_invoice = db.Column(db.Integer)
    rec_qty = db.Column(db.Float)
    rec_obs_density = db.Column(db.Float)
    rec_obs_temp = db.Column(db.Float)
    rec_density15 = db.Column(db.Float)
    cash_density15 = db.Column(db.Float)
    diff = db.Column(db.Float)
    afterdeca_obs_density = db.Column(db.Float)
    afterdeca_obs_temp = db.Column(db.Float)
    afterdeca_obs_density15 = db.Column(db.Float)

class employee(db.Model):
    emp_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    dob = db.Column(db.Date)
    address = db.Column(db.String(150))
    phone = db.Column(db.String(150))
    emp_id_sales = db.relationship('sales')
    emp_id_duty = db.relationship('duty_posting')
    excess_short = db.Column(db.Float)
    advance = db.Column(db.Integer)


class sales(db.Model):
    sid = db.Column(db.Integer, primary_key = True)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))
    bay = db.Column(db.Integer)
    date = db.Column(db.Date)
    shift = db.Column(db.Integer)
    ms_opening = db.Column(db.Float)
    ms_closing = db.Column(db.Float)
    ms_sales = db.Column(db.Float)
    ms_amount = db.Column(db.Float)
    hsd_opening = db.Column(db.Float)
    hsd_closing = db.Column(db.Float)
    hsd_sales = db.Column(db.Float)
    hsd_amount = db.Column(db.Float)
    stotal = db.Column(db.Float)#

    two_thousand = db.Column(db.Integer)
    five_hundred = db.Column(db.Integer)
    two_hundred = db.Column(db.Integer)
    one_hundred = db.Column(db.Integer)
    fifty = db.Column(db.Integer)
    twenty = db.Column(db.Integer)
    ten = db.Column(db.Integer)
    coins = db.Column(db.Integer)

    pos = db.Column(db.Float)#
    ufill = db.Column(db.Float)##
    upi = db.Column(db.Float)#
    smartfleet = db.Column(db.Float)##
    smartdrive = db.Column(db.Float)##
    pinelabs = db.Column(db.Float)##
    dtotal = db.Column(db.Float)#


    diff = db.Column(db.Float)#

class duty_posting(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))
    name = db.Column(db.String(150))
    date = db.Column(db.Date) 
    shift = db.Column(db.Integer)
    bay = db.Column(db.Integer)

class bay_manager(db.Model):
    bay_no = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    hsd = db.Column(db.Integer)
    ms = db.Column(db.Integer)

class certificate(db.Model):
    name = db.Column(db.String(150), primary_key = True)
    file_name = db.Column(db.String(150))
    exp_date = db.Column(db.Date)
    issue_date = db.Column(db.Date)
    file = db.Column(db.LargeBinary)

class daily_price(db.Model):
    date = db.Column(db.Date, default=func.now(), primary_key = True)
    ms_price = db.Column(db.Float)
    hsd_price = db.Column(db.Float)

class payment_methods(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    payment_method = db.Column(db.String(150))

class itemsales(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sid = db.Column(db.Integer)
    inv_id = db.Column(db.Integer)
    sale = db.Column(db.Integer)
