NE = IS_NOT_EMPTY()

db.define_table(
    'customer',
    Field('user_ID',unique = True),
    Field('firstName'),
    Field('middleName',required = False),
    Field('lastName'),
    Field('profession'),
    Field('billingAdd_ID'),
    Field('shippingAdd_ID'),
    Field('email'),
    Field('is_Authorized','boolean'),
    Field('password'),
    Field('group_ID'),
    Field('organization_ID'),
    Field('is_Hospital','boolean')
    )
db.define_table(
    'address',
    Field('user_ID'),
    Field('typeofAddress'),
    Field('streetAddress'),
    Field('city'),
    Field('address_state'),
    Field('zip')
    )
db.define_table(
    'wishList',
    Field('user_ID'),
    Field('product_ID')
    )

db.define_table(
    'vendors',
    Field('v_ID',unique = True,required = True),
    Field('v_Name'),
    Field('p_Type')
    )
db.define_table(
    'product_Type',
    Field('pType_ID'),
    Field('category')
    )

db.define_table(
    'product',
    Field('code',requires=NE,widget=widget(_placeholder='Product Code', _readonly=False)),
    Field('name',requires=NE,widget=widget(_placeholder='Product Name', _readonly=False)),
    Field('description',requires=NE,widget=widget(_placeholder='Product Description', _readonly=False)),
    Field('qty_in_stock','integer'),
    Field('unit_price','decimal(10,2)'),
    Field('image','upload'),
    Field('tags',widget=widget(_placeholder='Product Tags', _readonly=False)),
    Field('category',widget=widget(_placeholder='Product Category', _readonly=False)),
    Field('popularity','integer',default=0),
    Field('featured','boolean',default=False),
    Field('on_sale','boolean',default=False),
    Field('v_ID', 'reference hospitals'),
    Field('tax','decimal(10,2)'),
    Field('rating', 'float', default=3),
    Field('keywords',required=True,
          compute=lambda r: "%(code)s %(name)s %(tags)s" % r),
    auth.signature)

productTable = db['product']
productTable.v_ID.requires = IS_IN_DB(db, db.hospitals.id,'%(h_Name)s')

db.define_table(
    'review',
    Field('prodID', 'reference product'),
    Field('userID', 'reference ' + auth.settings.table_user_name),
    Field('title', length = 128),
    Field('rating', 'float', requires=IS_IN_SET([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])),
    Field('review_text','text')
    )

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

db.define_table(
    'conversations',
    Field('text_file','string'))

db.define_table(
    'current_conv',
    Field('conv','string', default=''),
    auth.signature)

#db(db.auth_user.id>1).delete()
#db(db.product).delete()

'''
db.define_table(
    'product',
    Field('code',requires=NE),
    Field('name',requires=NE),
    Field('description',requires=NE),
    Field('qty_in_stock','integer'),
    Field('unit_price','decimal(10,2)'),
    Field('image','upload'),
    Field('tags'),
    Field('category'),
    Field('popularity','integer',default=0),
    Field('featured','boolean',default=False),
    Field('on_sale','boolean',default=False),
    Field('v_ID', 'reference hospitals'),
    Field('tax','decimal(10,2)'),
    Field('keywords',required=True,
          compute=lambda r: "%(code)s %(name)s %(tags)s" % r),
    auth.signature)
'''

db.product._enable_record_versioning(archive_db=db,archive_name='productArchives',current_record='current_record',is_active='is_active')
db.customer._enable_record_versioning(archive_db=db,archive_name='customerArchives',current_record='current_record',is_active='is_active')

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
            category = l[7],
            popularity=int(l[8]),
            featured=int(l[9]),
            on_sale=int(l[10]),
            v_ID = l[11],
            tax=0.10,)

response.generic_patterns = ['*'] if request.is_local else []
from gluon.tools import Auth, prettydate
auth = Auth(db, hmac_key = Auth.get_or_create_key())
auth.define_tables()

Post = db.define_table("post",
                       Field("textmessage","text",requires=IS_NOT_EMPTY(),notnull=True),
                       auth.signature
                       )
Post.is_active_readable = False
Post.is_active_writable = False
