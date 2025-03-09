
from fpdf import FPDF
from jinja2 import Environment, FileSystemLoader

# member = Member.objects.get(member_id=25)
#
# # Fetch related people
# mother = Relations.objects.filter(member_id=member.member_id, relationship__iexact='Mother').first()
# father = Relations.objects.filter(member_id=member.member_id, relationship__iexact='Father').first()
# spouse = Relations.objects.filter(member_id=member.member_id, relationship__iexact='Spouse').first()
# close_relative = Relations.objects.filter(member_id=member.member_id,
#                                           relationship__iexact='Close Relative').first()
#
# # Fetch positions
# positions = ChurchPositions.objects.filter(member=member)
# position_names = ", ".join([pos.position_name for pos in positions]) if positions else "None"
#
# # Fetch church branch
# church_branch = member.church_branch.branch_name if member.church_branch else "Unknown"
#
# # Fetch joined groups efficiently
# group_names = Groups.objects.filter(
#     group_id__in=Joinedgroups.objects.filter(member=member).values_list('group', flat=True)
# ).values_list('group_name', flat=True)
# group_names = ", ".join(group_names) if group_names else "None"
#
# # **Retrieve Cloudinary Image URL**
# image_url = member.member_image.url if member.member_image else None
#
# # Example data (replace with database fetch)
data = {
            "title": "Member Details",
            "image_path": "WhatsApp Image 2025-03-08 at 19.30.54_eb1b4aa6.jpg",  # Cloudinary Image URL
            "f_name": None,
            "l_name": None,
            "phone_number": None or "N/A",
            "date_of_birth": None,
            "address": None or "N/A",
            "home_town": None or "N/A",
            "date_joined": None,
            "welfare_card_num": None or "N/A",
            "tithe_card_num": None or "N/A",
            "church_branch": None,
            "groups": None,
            "positions": None,
            "occupation": "Unknown",  # Add occupation field if available
            "emergency_number": "N/A",  # Add emergency number field if needed
            "history": None or "N/A",
            "marital_status": None or "N/A",
            "c_f_name":  "N/A",
            "c_l_name":"N/A",
            "c_phone_number":  "N/A",
            "c_is_member": "Yes" "No",
            "f_f_name": "N/A",
            "f_l_name": "N/A",
            "f_phone_number":  "N/A",
            "f_is_member": "Yes"  "No",
            "m_f_name": "N/A",
            "m_l_name":  "N/A",
            "m_phone_number":  "N/A",
            "m_is_member": "Yes"  "No",
            "r_f_name":  "N/A",
            "r_l_name":  "N/A",
            "r_phone_number": "N/A",
            "r_is_member": "Yes"  "No",
            "nxt_of_kin": "N/A"
        }

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.txt')

# Render the template with data
rendered_text = template.render(data)

# Create a PDF object
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Add rendered text to the PDF
pdf.multi_cell(0, 10, txt=rendered_text)

# Add image (if placeholder exists)
if "[IMAGE:" in rendered_text:
    start = rendered_text.find("[IMAGE:") + len("[IMAGE:")
    end = rendered_text.find("]", start)
    image_path = rendered_text[start:end]
    pdf.image(image_path, x=10, y=pdf.get_y(), w=100)  # Adjust size and position

# Save the PDF
pdf.output("output.pdf")

print("PDF generated successfully!")