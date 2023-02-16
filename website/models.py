from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class login(db.Model):
    user_id = db.Column(db.String(150), primary_key = True)
    password = db.Column(db.String(150))

class inventory(db.Model):
    inv_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    stock = db.Column(db.Integer)
    price = db.Column(db.Integer)

class fuel_reg(db.Model):
    date = db.Column(db.DateTime(timezone=True), default=func.now(), primary_key = True)
    morning_density = db.Column(db.Integer)
    morning_temp = db.Column(db.Integer)
    density15 = db.Column(db.Integer)
    rec_invoice = db.Column(db.Integer)
    rec_qty = db.Column(db.Integer)
    rec_obs_desity = db.Column(db.Integer)
    rec_obs_temp = db.Column(db.Integer)
    rec_density15 = db.Column(db.Integer)
    cash_density15 = db.Column(db.Integer)
    diff = db.Column(db.Integer)
    afterdeca_obs_density = db.Column(db.Integer)
    afterdeca_obs_temp = db.Column(db.Integer)
    afterdeca_obs_density15 = db.Column(db.Integer)

class employee(db.Model):
    emp_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    dob = db.Column(db.Date)
    address = db.Column(db.String(300))
    phone = db.Column(db.String(150))
    emp_id_sales = db.relationship('sales')
    emp_id_duty = db.relationship('duty_posting')
    excess_short = db.Column(db.Integer)
    advance = db.Column(db.Integer)


class sales(db.Model):
    sid = db.Column(db.Integer, primary_key = True)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))
    bay = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    shift = db.Column(db.Integer)
    ms_opening = db.Column(db.Float)
    ms_closing = db.Column(db.Float)
    ms_sale = db.Column(db.Float)
    ms_amount = db.Column(db.Float)
    hsd_opening = db.Column(db.Float)
    hsd_closing = db.Column(db.Float)
    hsd_sale = db.Column(db.Float)
    hsd_amount = db.Column(db.Float)
    lube = db.Column(db.Integer)
    lube_sale = db.Column(db.Float)
    lube_amount = db.Column(db.Float)
    stotal = db.Column(db.Float)
    denom = db.relationship('denomination')
    pos = db.relationship('pos')
    excess_short = db.relationship('excess_short')

class denomination(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sid = db.Column(db.Integer, db.ForeignKey('sales.sid'))
    two_thousand = db.Column(db.Integer)
    five_hundred = db.Column(db.Integer)
    two_hundred = db.Column(db.Integer)
    one_hundred = db.Column(db.Integer)
    fifty = db.Column(db.Integer)
    twenty = db.Column(db.Integer)
    ten = db.Column(db.Integer)
    coins = db.Column(db.Integer)
    upi = db.Column(db.Integer)
    card = db.Column(db.Integer)
    lube = db.Column(db.Integer)
    dtotal = db.Column(db.Integer)

class pos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sid = db.Column(db.Integer, db.ForeignKey('sales.sid'))
    amount = db.Column(db.Integer)

class excess_short(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sid = db.Column(db.Integer, db.ForeignKey('sales.sid'))
    stotal = db.Column(db.Integer)
    dtotal = db.Column(db.Integer)
    diff = db.Column(db.Integer)

class duty_posting(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date) 
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))
    shift = db.Column(db.Integer)
    bay = db.Column(db.Integer)

class bay_manager(db.Model):
    bay_no = db.Column(db.Integer, primary_key = True)
    hsd = db.Column(db.Integer)
    ms = db.Column(db.Integer)

class certificate(db.Model):
    name = db.Column(db.String(200), primary_key = True)
    exp_date = db.Column(db.Date)
    issue_date = db.Column(db.Date)
    # file = db.Column(db.VARBINARY(max))

class daily_price(db.Model):
    date = db.Column(db.DateTime, default=func.now(), primary_key = True)
    ms_price = db.Column(db.Float)
    hsd_price = db.Column(db.Float)
