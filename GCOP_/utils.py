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
                emergency_num=data['emergency'],
                occupation=data['occupation'],
                   nxt_of_kin=data['nxt_of_kin'],
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
                      is_member=data['father_is_member'],member_id=m.member_id)

        f.save()
        ##print('Saved father data')
        m = Relations(f_name=data['mother_first_name'],
                      l_name=data['mother_other_name'],
                      phone_number=data['mother_phone_number'],
                      relationship='Mother',
                      is_member=data['mother_is_member'],member_id=m.member_id)

        m.save()
        ##print('Saved mother data')
    elif data['parent_status']=='Only Father':
        f = Relations(f_name=data['father_first_name'],
                      l_name=data['father_other_name'],
                      phone_number=data['father_phone_number'],
                      relationship='Father',
                      is_member=data['father_is_member'],member_id=m.member_id)

        f.save()
        ##print('Saved father data')
    elif data['parent_status']=='Only Mother':
        m = Relations(f_name=data['mother_first_name'],
                      l_name=data['mother_other_name'],
                      phone_number=data['mother_phone_number'],
                      relationship='Mother',
                      is_member=data['mother_is_member'],member_id=m.member_id)

        m.save()
        ##print('Saved mother data')


    for c in range(data['number_of_children']):
        cd = data[f"child_{c+1}"]
        cc = Relations(f_name=cd['child_first_name'],
                      l_name=cd['child_other_name'],
                      phone_number=cd['child_phone_number'],
                      relationship='Child',
                      is_member=cd['child_is_member'],member_id=m.member_id)

        cc.save()
        ##print('Saved child data')

    for s in range(data['number_of_survivors']):
        sd = data[f"survivor_{s+1}"]
        cc = Relations(f_name=sd['survivor_first_name'],
                      l_name=sd['survivor_other_name'],
                      phone_number=sd['survivor_phone_number'],
                      relationship='Close Relative',
                      is_member=sd['survivor_is_member'],member_id=m.member_id)

        cc.save()
        ##print('Saved survivor data')


    if data['marital_status'] == 'married':
        sp = Relations(f_name=data['spouse_first_name'],
                      l_name=data['spouse_other_name'],
                      phone_number=data['spouse_phone_number'],
                      relationship='Spouse',
                      is_member=data['spouse_is_member'],member_id=m.member_id)
        sp.save()
    ##print('Saved spouse data')

def user_without_image():
    users = Member.objects.filter(member_image__isnull=True)
    data = {}
    for i in users:
        data = { 'id':i.member_id,
                 'first_name':i.f_name,
                 "last_name":i.l_name
        }

    return data
from django.db.models import Q

def get_member(f_name, l_name, phone_num):
    data = {}
    try:
        members = Member.objects.filter(
            Q(f_name__iexact=f_name) | Q(l_name__iexact=l_name) | Q(phone_number=phone_num)
        )
        for i in members:
            data = {'id': i.member_id,
                    'first_name': i.f_name,
                    "last_name": i.l_name
                    }

        return data
    except:
        return None


from fpdf import FPDF
from jinja2 import Environment, FileSystemLoader
from .models import Member, Relations, ChurchPositions, Branches, Groups, Joinedgroups  # Ensure correct imports


def print_pdf(member_id):
    try:
        # Fetch member details
        member = Member.objects.get(member_id=member_id)

        # Fetch related people
        mother = Relations.objects.filter(member_id=member.member_id, relationship__iexact='Mother').first()
        father = Relations.objects.filter(member_id=member.member_id, relationship__iexact='Father').first()
        spouse = Relations.objects.filter(member_id=member.member_id, relationship__iexact='Spouse').first()
        close_relative = Relations.objects.filter(member_id=member.member_id,
                                                  relationship__iexact='Close Relative').first()

        # Fetch positions
        positions = ChurchPositions.objects.filter(member=member)
        position_names = ", ".join([pos.position_name for pos in positions]) if positions else "None"

        # Fetch church branch
        church_branch = member.church_branch.branch_name if member.church_branch else "Unknown"

        # Fetch joined groups efficiently
        group_names = Groups.objects.filter(
            group_id__in=Joinedgroups.objects.filter(member=member).values_list('group', flat=True)
        ).values_list('group_name', flat=True)
        group_names = ", ".join(group_names) if group_names else "None"

        # **Retrieve Cloudinary Image URL**
        image_url = member.member_image.url if member.member_image else None

        # Prepare data dictionary
        data = {
            "title": "GCOP MEMBERS FORM Details",
            "image_path": image_url,  # Cloudinary Image URL
            "f_name": member.f_name,
            "l_name": member.l_name,
            "phone_number": member.phone_number or "N/A",
            "date_of_birth": member.date_of_birth.strftime("%Y-%m-%d") if member.date_of_birth else "N/A",
            "address": member.address or "N/A",
            "home_town": member.hometown or "N/A",
            "date_joined": member.date_joined.strftime("%Y") if member.date_joined else "N/A",
            "welfare_card_num": member.welfare_card_num or "N/A",
            "tithe_card_num": member.tithe_card_num or "N/A",
            "church_branch": church_branch,
            "groups": group_names,
            "positions": position_names,
            "occupation": "Unknown",  # Add occupation field if available
            "emergency_number": "N/A",  # Add emergency number field if needed
            "history": member.history or "N/A",
            "marital_status": member.marital_status or "N/A",
            "c_f_name": spouse.f_name if spouse else "N/A",
            "c_l_name": spouse.l_name if spouse else "N/A",
            "c_phone_number": spouse.phone_number if spouse else "N/A",
            "c_is_member": "Yes" if spouse and spouse.is_member else "No",
            "f_f_name": father.f_name if father else "N/A",
            "f_l_name": father.l_name if father else "N/A",
            "f_phone_number": father.phone_number if father else "N/A",
            "f_is_member": "Yes" if father and father.is_member else "No",
            "m_f_name": mother.f_name if mother else "N/A",
            "m_l_name": mother.l_name if mother else "N/A",
            "m_phone_number": mother.phone_number if mother else "N/A",
            "m_is_member": "Yes" if mother and mother.is_member else "No",
            "r_f_name": close_relative.f_name if close_relative else "N/A",
            "r_l_name": close_relative.l_name if close_relative else "N/A",
            "r_phone_number": close_relative.phone_number if close_relative else "N/A",
            "r_is_member": "Yes" if close_relative and close_relative.is_member else "No",
            "nxt_of_kin": spouse.f_name if spouse else "N/A"
        }

        # Set up Jinja2 environment
        env = Environment(loader=FileSystemLoader("GCOP_/templates"))
        template = env.get_template('template.txt')

        # Render the template with data
        rendered_text = template.render(data)

        # Create a PDF object
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Center and Bolden the Title
        pdf.set_font("Arial", style='B', size=16)
        pdf.cell(0, 10, txt=data["title"], ln=True, align='C')
        pdf.ln(10)  # Add space after title

        # Process text line by line
        for line in rendered_text.split("\n"):
            if line.strip().startswith("Image: [IMAGE:"):
                # Extract image path from the line (if exists)
                if image_url:
                    import requests
                    from PIL import Image
                    from io import BytesIO

                    response = requests.get(image_url)
                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content))
                        local_image_path = f"temp_{member_id}.jpg"
                        img.save(local_image_path)  # Save image locally
                        pdf.image(local_image_path, x=10, y=pdf.get_y(), w=80, h=60)  # Insert image
                        pdf.ln(65)  # Move cursor down to avoid overlap
            else:
                # Bolden the Questions
                if ":" in line:
                    question, answer = line.split(":", 1)
                    pdf.set_font("Arial", style='B', size=12)
                    pdf.cell(0, 10, txt=question + ":", ln=False)
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, txt=answer.strip())
                else:
                    pdf.multi_cell(0, 10, txt=line)
                pdf.ln(5)  # Add space between sections

        # Save the PDF
        output_path = f"output_{member_id}.pdf"
        pdf.output(output_path)

        print(f"PDF generated successfully! Saved as {output_path}")

        return output_path

    except Member.DoesNotExist:
        print("Error: Member not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



