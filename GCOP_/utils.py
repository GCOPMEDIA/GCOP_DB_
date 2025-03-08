from .models import *

def member_entry(data):


    if data["first_name"]:
        m = Member(f_name=data['first_name'],
               l_name=data['other_name'],
               date_of_birth=data['date_of_birth'],
               phone_number=data['phone'],
               address=data['address'],
               hometown=data['hometown'],
               gender = data['gender'],
               marital_status=data['marital_status'],
               date_joined = data['date_joined'],

                welfare_card_num=data['welfare_card_number'],
               tithe_card_num=data['tithe_card_number'],
               history=data['history'],
               baptism_status=data['baptism'],
               baptist_at_gcop=data['baptist_at_gcop']
               )
        m.save()
        church_branch = Branches.objects.get(branch_name=data['church_branch'])
        m.church_branch = church_branch
        m.save()
        ##print('Saved member data')

    for p in (data['position']).split(','):
        position = ChurchPositions(position_name=p,member=m)
        position.save()
        ##print('Saved position data')

    for g in data['group_name']:
        group = Groups.objects.get(group_id=int(g))
        jgroup = Joinedgroups(group=group,member=m)
        jgroup.save()
        ##print('Saved group data')

    if data['parent_status']=='Both':
        f = Relations(f_name=data['father_first_name'],
                      l_name=data['father_other_name'],
                      phone_number=data['father_phone_number'],
                      relationship='Father',
                      is_member=data['father_is_member'],member_id=m)

        f.save()
        ##print('Saved father data')
        m = Relations(f_name=data['mother_first_name'],
                      l_name=data['mother_other_name'],
                      phone_number=data['mother_phone_number'],
                      relationship='Mother',
                      is_member=data['mother_is_member'],member_id=m)

        m.save()
        ##print('Saved mother data')
    elif data['parent_status']=='Only Father':
        f = Relations(f_name=data['father_first_name'],
                      l_name=data['father_other_name'],
                      phone_number=data['father_phone_number'],
                      relationship='Father',
                      is_member=data['father_is_member'],member_id=m)

        f.save()
        ##print('Saved father data')
    elif data['parent_status']=='Only Mother':
        m = Relations(f_name=data['mother_first_name'],
                      l_name=data['mother_other_name'],
                      phone_number=data['mother_phone_number'],
                      relationship='Mother',
                      is_member=data['mother_is_member'],member_id=m)

        m.save()
        ##print('Saved mother data')


    for c in range(data['number_of_children']):
        cd = data[f"child_{c+1}"]
        cc = Relations(f_name=cd['child_first_name'],
                      l_name=cd['child_other_name'],
                      phone_number=cd['child_phone_number'],
                      relationship='Child',
                      is_member=cd['child_is_member'],member_id=m)

        cc.save()
        ##print('Saved child data')

    for s in range(data['number_of_survivors']):
        sd = data[f"survivor_{s+1}"]
        cc = Relations(f_name=sd['survivor_first_name'],
                      l_name=sd['survivor_other_name'],
                      phone_number=sd['survivor_phone_number'],
                      relationship='Close Relative',
                      is_member=sd['survivor_is_member'],member_id=m)

        cc.save()
        ##print('Saved survivor data')



    sp = Relations(f_name=data['spouse_first_name'],
                  l_name=data['spouse_other_name'],
                  phone_number=data['spouse_phone_number'],
                  relationship='Spouse',
                  is_member=data['spouse_is_member'],member_id=m)

    sp.save()
    ##print('Saved spouse data')

