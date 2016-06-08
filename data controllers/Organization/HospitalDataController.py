''' Hospital data controller '''

def getHospitalByID(hospitalID):
	return db(db.hospitals.h_ID == hospitalID)

def getHospitalByName(name):
	return db(db.hospitals.h_Name == name)

def getHospitalByContactEmail(email):
	return db(db.hospitals.contant_Email == email)

def getHospitalByUserID(userID):
	user = db(db.customer.user_ID == userID)
	return  db(db.hospitals.h_ID == user.organization_ID)

def getHospitalsByCity(city):
	hospitals = db(db.address.city == city)
	return db(db.hospitals.h_ID == hospitals.organization_ID)

def getHospitalsByZip(zip):
	hospitals = db(db.address.zip == zip)
	return db(db.hospitals.h_ID == hospitals.organzation_ID)

def getHospitalsByState(state):
	hospitals = db(db.address.state == state)
	return db(db.hospitals.h_ID == hospitals.organization_ID)

def getHospitalByUserName(firstName, lastName):
	user = db(db.customer.firstName == firstName && db.customer.lastName == lastName)
	return db(db.hospitals.h_ID == user.organization_ID)

def getHospitalByUserEmail(email):
	user = db(db.customer.email == email)
	return db(db.hospitals.h_ID == user.organization_ID)

def getHospitalsByStreetAddress(address):
	hospitals = db(db.address.streetAddress == address)
	return db(db.hospitals.h_ID == hospitals.organization_ID)
