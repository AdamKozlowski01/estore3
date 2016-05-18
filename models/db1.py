NE = IS_NOT_EMPTY()

db.define_table(
    'customer',
    Field('user_ID',unique = True, NE),
    Field('firstName'),
    Field('middleName',required = False),
    Field('lastName'),
    Field('profession'),
    Field('email'),
    Field('is_Authorized','boolean'),
    Field('password'),
    Field('group_ID'),
    Field('organization_ID'),
<<<<<<< HEAD
    Field('is_Hospital','boolean')
=======
    Field('is_Hospital',boolean),
    auth.signature
>>>>>>> Adam
    )
db.define_table(
    'address',
    Field('organization_ID'),
    Field('typeofAddress'),
    Field('streetAddress'),
    Field('city'),
<<<<<<< HEAD
    Field('address_state'),
    Field('zip')
=======
    Field('state'),
    Field('zip'),
    auth.signature
>>>>>>> Adam
    )
db.define_table(
    'wishList',
    Field('user_ID'),
    Field('product_ID'),
    auth.signature
    )
db.define_table(
<<<<<<< HEAD
    'hospitals',
    Field('h_ID',unique = True),
    Field('h_Name',required = True),
    Field('email_Format'),
    Field('h_size'),
    Field('esn_ID',unique = True),
<<<<<<< HEAD
    Field('for_Profit','boolean'),
    Field('contact_Email')
=======
    Field('for_Profit',boolean),
    Field('contact_Email'),
    Field('billingAdd_ID'),
    Field('shippingAdd_ID'),
    auth.signature
>>>>>>> Adam
    )
db.define_table(
=======
>>>>>>> master
    'vendors',
    Field('v_ID',unique = True,required = True),
    Field('v_Name'),
<<<<<<< HEAD
    Field('p_Type')
    )
db.define_table(
=======
    Field('contant_Email'),

    auth.signature)
db.define_Table(
>>>>>>> Adam
    'product_Type',
    Field('pType_ID'),
    Field('v_ID'),
    Field('category'),
    Field('vendorID')
    auth.signature
    )
db.define_table(
    'product',
    Field('code',requires=NE),
    Field('name',requires=NE),
    Field('description',requires=NE),
    Field('qty_in_stock','integer'),
    Field('unit_price','decimal(10,2)'),
    Field('image','upload'),
    Field('tags'),
    Field('p_Type'),
    Field('popularity','integer',default=0),
    Field('featured','boolean',default=False),
    Field('on_sale','boolean',default=False),
    Field('tax','decimal(10,2)'),
    Field('keywords',required=True,
          compute=lambda r: "%(code)s %(name)s %(tags)s %(p_Type)s" % r),
    auth.signature)

db.define_table(
    'purchase_order',
    Field('buyer_name'),
    Field('shipping_address'),
    Field('shipping_city'),
    Field('shipping_zip'),
    Field('shipping_state'),
    Field('shipping_country'),
    Field('total_price','decimal(10,2)',readable=False,writable=False),
    Field('total_tax','decimal(10,2)',readable=False,writable=False),
    Field('total_balance','decimal(10,2)',readable=False,writable=False),
    Field('amount_paid','decimal(10,2)',readable=False,writable=False),
    Field('payment_id',readable=False,writable=False),
    Field('paid_on','datetime',readable=False,writable=False),
    Field('status',requires=IS_IN_SET(('submitted','shipped','received','returned')),
          default='submitted',readable=False,writable=False),
    Field('notes','text'),
    auth.signature)

db.define_table(
    'purchase_item',
    Field('purchase_order','reference purchase_order'),
    Field('product','reference product'),
    db.product, # yes we copy the product description at the moment of an order
    Field('quantity_in_cart','integer'),
    auth.signature)

#db(db.auth_user.id>1).delete()
#db(db.product).delete()
if db(db.product).count()==0:
    import re
    import os
    file = open(os.getcwd()+'/applications/estore3/models/save.txt', 'r')
    for line in file:
        l = re.split('\|',line)
        db.product.insert(
            code=l[0],
            name=l[1],
            description=l[2],
            qty_in_stock=int(l[3]),
            unit_price=float(l[4]),
            image=l[5],
            tags=l[6],
            p_Type=l[7],
            popularity=int(l[8]),
            featured=int(l[9]),
            on_sale=int(l[9]),
            tax=0.10,)
