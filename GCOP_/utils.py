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
from .models import Member, Relations, ChurchPositions, Branches, Groups, Joinedgroups
import requests
from PIL import Image
from io import BytesIO


def print_pdf(member_id):
    try:
        # Fetch member details
        member = Member.objects.get(member_id=member_id)

        # Fetch related people
        relations = {
            "Mother": Relations.objects.filter(member_id=member.member_id, relationship__iexact='Mother').first(),
            "Father": Relations.objects.filter(member_id=member.member_id, relationship__iexact='Father').first(),
            "Spouse": Relations.objects.filter(member_id=member.member_id, relationship__iexact='Spouse').first(),
            "Close Relative": Relations.objects.filter(member_id=member.member_id,
                                                       relationship__iexact='Close Relative').first()
        }

        # Fetch positions
        positions = ChurchPositions.objects.filter(member=member)
        position_names = ", ".join([pos.position_name for pos in positions]) if positions else "None"

        # Fetch church branch
        church_branch = member.church_branch.branch_name if member.church_branch else "Unknown"
        church_location = member.church_branch.branch_location if member.church_branch else 'Unknown'

        # Fetch joined groups
        group_names = Groups.objects.filter(
            group_id__in=Joinedgroups.objects.filter(member=member).values_list('group', flat=True)
        ).values_list('group_name', flat=True)
        group_names = ", ".join(group_names) if group_names else "None"

        # Retrieve Cloudinary Image URL
        image_url = member.member_image.url if member.member_image else None

        # Prepare data dictionary
        data = {

            "image_path": image_url,
            "SURNAME": member.f_name,
            "FIRST NAMES": member.l_name,
            "PHONE NUMBER": member.phone_number or "N/A",
            "DATE OF BIRTH": member.date_of_birth.strftime("%Y-%m-%d") if member.date_of_birth else "N/A",
            "GHANA POST ADDRESS": str(member.address).strip() or "N/A",
            "HOME TOWN": member.hometown or "N/A",
            "YEAR JOINED GCOP": member.date_joined.strftime("%Y") if member.date_joined else "N/A",
            "WELFARE CARD NUMBER": member.welfare_card_num or "N/A",
            "TITHE CARD NUMBER": member.tithe_card_num or "N/A",
            "CHURCH BRANCH":  f"({church_location}) {church_branch}",
            "GROUP(S) JOINED": group_names,
            "POSITION(S)": position_names,
            "OCCUPATION": member.occupation or "Unknown",
            "EMERGENCY NUMBER": member.emergency_num or "N/A",
            "BRIEF HISTORY": member.history or "N/A",
            "MARITAL STATUS": member.marital_status or "N/A",
            "CHILD'S SURNAME": relations["Spouse"].f_name if relations["Spouse"] else "N/A",
            "CHILD'S FIRST NAMEs": relations["Spouse"].l_name if relations["Spouse"] else "N/A",
            "CHILD'S PHONE NUMBER": relations["Spouse"].phone_number if relations["Spouse"] else "N/A",
            "IS CHILD A GCOP MEMBER": "Yes" if relations["Spouse"] and relations["Spouse"].is_member else "No",
            "FATHER'S SURNAME": relations["Father"].f_name if relations["Father"] else "N/A",
            "FATHER'S FIRST NAMEs": relations["Father"].l_name if relations["Father"] else "N/A",
            "FATHER'S PHONE NUMBER": relations["Father"].phone_number if relations["Father"] else "N/A",
            "IS FATHER A GCOP MEMBER": "Yes" if relations["Father"] and relations["Father"].is_member else "No",
            "MOTHER'S SURNAME": relations["Mother"].f_name if relations["Mother"] else "N/A",
            "MOTHER'S FIRST NAMEs": relations["Mother"].l_name if relations["Mother"] else "N/A",
            "MOTHER'S PHONE NUMBER": relations["Mother"].phone_number if relations["Mother"] else "N/A",
            "IS MOTHER A GCOP MEMBER": "Yes" if relations["Mother"] and relations["Mother"].is_member else "No",
            "SPOUSE'S SURNAME": relations["Spouse"].f_name if relations["Spouse"] else "N/A",
            "SPOUSE'S FIRST NAMEs": relations["Spouse"].l_name if relations["Spouse"] else "N/A",
            "SPOUSE'S PHONE NUMBER": relations["Spouse"].phone_number if relations["Spouse"] else "N/A",
            "IS SPOUSE A GCOP MEMBER": "Yes" if relations["Spouse"] and relations["Spouse"].is_member else "No",
            "RELATIVE'S SURNAME": relations["Close Relative"].f_name if relations["Close Relative"] else "N/A",
            "RELATIVE'S FIRST NAME": relations["Close Relative"].l_name if relations["Close Relative"] else "N/A",
            "RELATIVE'S PHONE NUMBER": relations["Close Relative"].phone_number if relations["Close Relative"] else "N/A",
            "IS RELATIVE A GCOP MEMBER": "Yes" if relations["Close Relative"] and relations["Close Relative"].is_member else "No",
            "NEXT OF KIN": relations["Spouse"].f_name if relations["Spouse"] else "N/A"
        }

        # Create PDF
        class PDF(FPDF):
            def header(self):
                # Set watermark on every page
                self.set_font("Arial", style='B', size=50)
                self.set_text_color(200, 200, 200)  # Light gray
                self.rotate(45, x=30, y=150)  # Rotate text diagonally
                self.text(30, 150, "Property of G.C.O.P")  # Watermark text
                self.rotate(0)  # Reset rotation after watermark

        # Use the custom PDF class
        pdf = PDF()
        pdf.add_page()

        # Title
        pdf.set_font("Arial", style='B', size=16)
        pdf.set_xy(35, 10)  # Move title closer to the right, near the logo
        pdf.multi_cell(120, 10, "God's Church Of Peace\nMEMBERSHIP FORM", align='C')

        # Image
        if image_url:
            response = requests.get(image_url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                local_image_path = f"temp_{member_id}.jpg"
                img.save(local_image_path)
                pdf.image(local_image_path, x=160, y=10, w=35, h=45)  # Top-right corner
                pdf.ln(20)
        pdf.image("GCOP_/logo.png", x=10, y=10, w=20, h=20)  # Adjust width & height as needed

        # Add watermark


        # Reset text color for main content
        pdf.set_text_color(0, 0, 0)  # Black text for main content
        pdf.set_font("Arial", size=12)  # Reset font size if needed

        # Details Section
        pdf.set_font("Arial", size=10)
        for field, value in data.items():
            if field not in ["title", "image_path"]:
                pdf.set_font("Arial", style='B', size=10)
                pdf.cell(80, 8, f"{field.replace('_', ' ').upper()}:", border=0)
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(100, 8, value)  # Wrap text properly for long values
                pdf.ln(2)  # Add a little space between fields

        # Pastor Signature Section
        pdf.ln(10)
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(80, 8, "PASTOR'S NAME:", border=0)
        pdf.cell(100, 8, "_____________________")
        pdf.ln(10)
        pdf.cell(80, 8, "SIGNATURE:", border=0)
        pdf.cell(100, 8, "_____________________")



        # Save the PDF
        output_path = f"output_{member_id}.pdf"
        pdf.output(output_path)
        print(f"PDF generated successfully! Saved as {output_path}")
        return output_path

    except Member.DoesNotExist:
        print("Error: Member not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
