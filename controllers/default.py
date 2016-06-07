# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################


def textbox():
    form = SQLFORM(Post, formstyle='divs',labels=None,submit_button='Send',showid=False)
    if form.process().accepted:
        #js = "jQuery('.new').slideDown('slow')"
        #comet_send('http://127.0.0.1:8888', js, 'mykey', 'mygroup')
        pass
    messages = db(Post).select(orderby=~Post.created_on)
    return dict(form=form, messages=messages)

def index():
    return dict()

def search():
    keywords = request.vars.keywords.split() if request.vars.keywords else []
    price = request.vars.price
    page = int(request.vars.page or 0)
    queries = []
    if keywords:
        queries.append(reduce(lambda a,b:a&b,
                              [db.product.keywords.contains(k) for k in keywords]))
    if price:
        queries.append(db.product.unit_price<=float(price))
    if not queries: query = db.product
    else: query = reduce(lambda a,b: a&b, queries)    
    return db(query).select(limitby=(page*100,page*100+100), orderby=~db.product.rating).as_json()

def submit_order():
    import json
    session.cart = json.loads(request.vars.cart)
    return 'ok'

def postRating():
    prod_id = request.vars.product
    avg = db.review.rating.avg()
    row = db(db.review.prodID == prod_id).select(avg).first()
    product = db(db.product.id == prod_id).select().first()
    product.rating = row[avg]
    product.update_record()
    redirect(URL('default', 'product', vars = dict(value = prod_id)))

@auth.requires_login()
def order_info():
    if not session.cart:
        redirect(URL('index'))
    db.purchase_order.buyer_name.default = '%(first_name)s %(last_name)s' % auth.user
    form = SQLFORM(db.purchase_order).process()
    if form.accepted:
        total_balance = 0
        for item in session.cart:
            item['product'] = item['id']
            item['purchase_order'] = form.vars.id
            del item['id']
            db.purchase_item.insert(**item)
            total_balance += item['unit_price']*int(item['quantity_in_cart'])
        session.cart = None
        db(db.purchase_order.id==form.vars.id).update(total_balance=total_balance)
        redirect(URL('pay',args=form.vars.id, hmac_key=STRIPE_SECRET_KEY))
    return dict(form=form)

def pay():
    if not URL.verify(request, hmac_key=STRIPE_SECRET_KEY):
        redirect(URL('index'))
    from gluon.contrib.stripe import StripeForm
    response.flash = None # never show a response.flash
    order = db.purchase_order(request.args(0,cast=int))
    if not order or order.amount_paid:
        session.flash = 'you paid already!'
        redirect(URL('index'))
    amount = order.total_balance
    description ="..."
    form = StripeForm(
        pk=STRIPE_PUBLISHABLE_KEY,
        sk=STRIPE_SECRET_KEY,
        amount=int(100*amount),
        description=description).process()
    if form.accepted:
        code = '[%s/%s]' % (order.id,form.response['id'])
        auth.settings.mailer.send(
            to=auth.user.email,
            subject='...',
            message='Your payment of $%.2f has been processed %s' % (
                amount, code))
        order.update_record(total_balance=0,amount_paid=amount,
                            payment_id=form.response['id'],
                            paid_on=request.now)
        redirect(URL('thank_you', vars=dict(code=code), hmac_key=STRIPE_SECRET_KEY))
    elif form.errors:
        redirect(URL('pay_error'))
    return dict(form=form)

def product():
    pID = request.get_vars.value
    prod = db(db.product.id == pID).select()
    if prod[0] is not None:
        pName = prod[0]['name']
        pDescription = prod[0]['description']
        pImage = prod[0]['image']
        pAvgRating = prod[0]['rating']
        pType = prod[0]['category']
        pOrgID = prod[0]['v_ID']
        org = db(db.hospitals.id == pOrgID).select()
        oName = org[0]['h_Name']
        pPrice = prod[0]['unit_price']
        pStock = prod[0]['qty_in_stock']
        reviews = db(db.review.prodID == pID).select()

    return locals()

def orgDetails():
    org = db(db.hospitals.id == request.get_vars.value).select()
    if org[0] is not None:
        oName = org[0]['h_Name']
        oSize = org[0]['h_size']
        oForProfit = org[0]['for_Profit']
        oContactEmail = org[0]['contact_Email']
        oEmployees = db(auth.settings.table_user.Organization_id == request.get_vars.value).select()

    return locals()

def userDetails():
    user = db(db.auth.settings.table_user == request.get_vars.value).select()
    if user[0] is not None:
        pFirstName = user[0]['first_name']
        pLastName = user[0]['last_name']
        pPosition = user[0]['job_title']
        pOrganizationID = user[0]['Organization_id']
        org = db(db.hospitals.id == pOrganizationID).select()
        oName = org[0]['h_Name']
    return locals()
    

def thank_you():
    if not URL.verify(request, hmac_key=STRIPE_SECRET_KEY):
        redirect(URL('index'))
    return locals()

def pay_error():
    return locals()

@auth.requires_membership('manager')
def my_orders():
    db.purchase_order._common_filter = lambda query: query&(db.purchase_order.created_by==auth.user.id)
    return dict(grid=SQLFORM.smartgrid(db.purchase_order,create=False,editable=False,deletable=False,csv=False))

@auth.requires_membership('manager')
def manage_products():
    return dict(grid=SQLFORM.grid(db.product))

@auth.requires_membership('manager')
def manage_orders():
    return dict(grid=SQLFORM.smartgrid(db.purchase_order))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    form=auth()            
    return dict(form=form)

def RegisterOrganization():

    formOrg = SQLFORM(db.hospitals)
    if formOrg.process().accepted:
        response.flash = 'form accepted'
        #check to see if this user needs to have highest privledges
        redirect(URL('user/register'))
    elif formOrg.errors:
        response.flash = 'form has errors'

    return dict(form = formOrg)

@auth.requires_login()
def orgAdmin():
    """
    if the user is logged in check to see if they should be the admin
    """
    me = auth.user_id
    orgAdminID = 3 #retrieved from auth_group
    user = db(auth.settings.table_user.id == me).select()
    if user[0] is not None:
        org = db(db.hospitals.id == user[0].Organization_id).select(db.hospitals.contact_Email)
        if org[0].contact_Email is not None:
            db.auth_membership.insert(user_id = me, group_id = orgAdminID)
            redirect(URL('index'))
            response.flash = "You are an OrgAdmin now, congratulations!"
    return locals()

@auth.requires_login()
def postReview():


    #prod_id = request.vars.product
    #vote = db.vote(prod_id, created_by=auth.user.id)
    #if vote:  vote.update_record(rating = request.vars.rating)
    #else:     db.vote.insert(prodID = prod_id, rating = request.vars.rating)
    #avg = db.vote.rating.avg()
    #row = db(db.vote.prodID == prod_id).select(avg).first()
    #db(db.product.id == prod_id).update(rating = row[avg])
    me = auth.user_id
    pID = request.get_vars.product
    rows = db(db.product.id == pID).select()
    product = rows[0]
    pName = product.name
    pRating = product.rating
    #change to SQL form and remove prodID and UserID
    #form = FORM('Title:', INPUT(title='title'), 'Review:', INPUT(review = 'review'), INPUT(_type='submit'))
    form = SQLFORM(db.review, fields = ['title', 'rating','review_text'], labels = {'title': 'Title your Review',\
     'review_text': 'Give others your thoughts'}, formstyle = 'bootstrap3_stacked')
    form.vars.prodID = pID
    form.vars.userID = me
    if form.process().accepted:
        redirect(URL('default', 'postRating', vars=dict(product=pID, rating = form.vars.rating)))
        response.flash = "Form accepted"

    return locals()

@auth.requires_membership('OrgAdmin')
def manageProducts():
    me = auth.user_id
    user = db(auth.settings.table_user.id == me).select()
    products = db(db.product.v_ID == user[0].Organization_id).select(db.product.ALL)

    #products = products.as_dict()
    return products.as_dict()

@auth.requires_membership('OrgAdmin')
def uploadProduct():
    form = SQLFORM(db.product)
    #Needs to handle adding the product to the database
    return dict(form = form);

@auth.requires_membership('OrgAdmin')
def editProduct():
    record = db.product(request.args(0))
    form = SQLFORM(db.product, record)
    if form.process().accepted:
        #needs to handle updating products in the db
        redirect(URL('manageProducts'))
    return dict(form=form)


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
