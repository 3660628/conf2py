import uuid

db.define_table('coupon',
                Field('code',default=str(uuid.uuid4())),
                Field('description','text'),
                Field('amount','double'),
                Field('created_by',db.auth_user,default=auth.user_id),
                Field('created_on','datetime',default=request.now),
                Field('used','boolean',default=False),
                Field('used_by',db.auth_user,default=auth.user_id),
                Field('used_on','datetime',default=request.now))
