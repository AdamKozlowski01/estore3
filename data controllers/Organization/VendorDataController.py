''' vendor data controller '''

def getVendorByID(vendorID):
	return db(db.vendors.v_ID == vendorID)

def getVendorByName(name):
	return db(db.vendors.v_Name == name)

def getHospitalByContactEmail(email):
	return db(db.vendors.contact_Email == email)

def getVendorByUserID(userID):
	user = db(db.customer.user_ID == userID)
	return  db(db.vendors.v_ID == user.organization_ID)

def getVendorsByCity(city):
	vendors = db(db.address.city == city)
	return db(db.vendors.v_ID == vendors.organization_ID)

def getVendorsByZip(zipCode):
	vendors = db(db.address.zip == zipCode)
	return db(db.vendors.v_ID == vendors.organzation_ID)

def getVendorsByState(state):
	vendors = db(db.address.state == state)
	return db(db.vendors.v_ID == vendors.organization_ID)

def getVendorByUserName(firstName, lastName):
	user = db(db.customer.firstName == firstName && db.customer.lastName == lastName)
	return db(db.vendors.v_ID == user.organization_ID)

def getVendorsByUserEmail(email):
	user = db(db.customer.email == email)
	return db(db.vendors.v_ID == user.organization_ID)

def getVendorsByStreetAddress(address):
	vendors = db(db.address.streetAddress == address)
	return db(db.vendors_ID == vendors.organization_ID)

def getVendorByProductID(productID):
	product = db(db.product.code == productID)
	return db(db.vendors.v_ID == product.vendorID)

def getVendorByProductName(name):
	product = db(db.product.name == name)
	return db(db.vendors.v_ID == product.vendorID)

def getVendorsByProductType(typeID):
	products = db(db.product.pType_ID == typeID)
	return db(db.vendors.v_ID == products.vendorID)
