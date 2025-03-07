from .models import *

def member_entry(data):
    try:

        if data["first_name"]:
            m = Member(f_name=data['first_name'],
                       l_name=data['other_name'],
                       date_of_birth=data['date_of_birth'],
                       phone_number=data['phone'],
                       )
    except:
        return None
