#Customer/User Data Controller

def getUserByID(userID):
        return db(db.customer.userID == userID)

def getUserName(name):
        return db(db.customer.firstName == name)

def getUserMiddleName(middleName):
        return db(db.customer.middleName == middleName)

def getUserLastName(lastName):
        return db(db.customer.lastName = lastName)

def getUserProfesstion(profession):
        return db(db.customer.profession == profession)

def getUserBillingAddID(billingAddID):
        return db(db.customer.billingAdd_ID == billingAddID)

def getUserShippingAddID(shippingAddID):
        return db(db.customer.shippingAdd_ID == shippingAddID)

def getUserEmail(email):
        return db(db.customer.email == email)

def getUserPassword(password):
        return db(db.customer.password == password)

def getUserGroupID(groupID):
        return db(db.customer.group_ID == groupID)

def getUserOrganizationID(orgID):
        return db(db.customer.organization_ID == orgID)

