from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
import json
import qrcode
import base64
from io import BytesIO
from django.shortcuts import render
from datetime import date
from .forms import UserDetailsForm, FurtherQuestionsForm, NextForm, FatherForm, MotherForm, SurvivorForm, SpouseForm
from .utils import *
from django.contrib.auth.decorators import login_required


# Utility function to convert date fields to strings
def convert_dates_to_strings(data):
    """Recursively converts all date objects in a dictionary to string format (YYYY-MM-DD)."""
    for key, value in data.items():
        if isinstance(value, date):
            data[key] = value.strftime('%Y-%m-%d')
    return data


from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.http import HttpResponse


def login_(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Try to get the 'next' parameter from either GET or POST
        next_url = request.GET.get('next') or request.POST.get('next')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url) if next_url else redirect('user_form')  # Redirect to next URL or default
        else:
            return HttpResponse(status=403)  # Or render with an error message

    next_url = request.GET.get('next', '')  # Preserve 'next' parameter for redirection
    return render(request, 'registration/login.html', {'next': next_url})


# Utility function to update session data
@login_required
def update_session_data(request, new_data):
    """Merge new form data into session storage (final_data5) to accumulate all responses."""
    user_data = json.loads(request.session.get('final_data5', '{}'))  # Load existing session data
    user_data.update(new_data)  # Merge new data
    request.session['final_data5'] = json.dumps(user_data, cls=DjangoJSONEncoder)  # Store back
    request.session.modified = True  # Ensure session is saved


# Step 1: User Details Form
@login_required(login_url='/', redirect_field_name='next')
def user_form_view(request):
    if User.is_authenticated:

        if request.method == 'POST':
            form = UserDetailsForm(request.POST)
            if form.is_valid():
                cleaned_data = convert_dates_to_strings(form.cleaned_data)
                update_session_data(request, cleaned_data)
                return redirect('further_questions')  # Move to Step 2
        else:
            form = UserDetailsForm()
        return render(request, 'form_template.html', {'form': form, 'step': '1'})
    else:
        return HttpResponse(status=403)


# Step 2: Further Questions (Collecting number of children and survivors)
@login_required(login_url='/', redirect_field_name='next')
def further_questions_view(request):
    if request.method == 'POST':
        form = FurtherQuestionsForm(request.POST)
        if form.is_valid():
            cleaned_data = convert_dates_to_strings(form.cleaned_data)

            # Store numbers for child & survivor processing
            request.session['number_of_children'] = int(cleaned_data.get('number_of_children', 0))
            request.session['number_of_survivors'] = int(cleaned_data.get('number_of_survivors', 0))
            request.session['marital_status'] = cleaned_data.get('marital_status', 'single')
            request.session['parent_status'] = cleaned_data.get('parent_status', 'None')

            update_session_data(request, cleaned_data)

            # Determine the next step based on conditions
            if request.session['marital_status'] == 'married':
                return redirect('spouse_details')
            elif request.session['number_of_children'] > 0:
                return redirect('child_details', child_index=1)
            elif request.session['parent_status'] != 'None':
                return redirect('father_details')
            else:
                return redirect('survivor_details', survivor_index=1)

    else:
        form = FurtherQuestionsForm()

    return render(request, 'form_template.html', {'form': form, 'step': '2'})


# Step 3: Spouse Details (Only shown if married)
@login_required(login_url='/', redirect_field_name='next')
def spouse_details(request):
    if request.method == 'POST':
        form = SpouseForm(request.POST)
        if form.is_valid():
            cleaned_data = convert_dates_to_strings(form.cleaned_data)
            update_session_data(request, cleaned_data)

            if request.session.get('number_of_children', 0) > 0:
                return redirect('child_details', child_index=1)
            elif request.session.get('parent_status', 'None') != 'None':
                return redirect('father_details')
            else:
                return redirect('survivor_details', survivor_index=1)

    else:
        form = SpouseForm()

    return render(request, 'form_template.html', {'form': form, 'step': 'spouse'})


# Step 4: Child Details (Handles multiple children dynamically)
@login_required(login_url='/', redirect_field_name='next')
def child_details_view(request, child_index):
    number_of_children = request.session.get('number_of_children', 0)

    if number_of_children == 0:
        return redirect('father_details')  # Skip if no children

    if request.method == 'POST':
        form = NextForm(request.POST)
        if form.is_valid():
            cleaned_data = convert_dates_to_strings(form.cleaned_data)
            update_session_data(request, {f'child_{child_index}': cleaned_data})

            if child_index < number_of_children:
                return redirect('child_details', child_index=child_index + 1)
            else:
                return redirect('father_details')

    else:
        form = NextForm()

    return render(request, 'form_template.html', {'form': form, 'step': '3', 'child_index': child_index})


# Step 5: Father Details
@login_required(login_url='/', redirect_field_name='next')
def father_details(request):
    parent_status = request.session.get('parent_status', 'None')
    if parent_status in ['Both', 'Only Father']:
        if request.method == 'POST':
            form = FatherForm(request.POST)
            if form.is_valid():
                cleaned_data = convert_dates_to_strings(form.cleaned_data)
                update_session_data(request, cleaned_data)
                return redirect('mother_details')

        else:
            form = FatherForm()

        return render(request, 'form_template.html', {'form': form, 'step': '4'})
    else:
        return redirect('mother_details')


@login_required(login_url='/', redirect_field_name='next')
def mother_details(request):
    parent_status = request.session.get('parent_status', 'None')
    if parent_status in ['Both', 'Only Mother']:
        if request.method == 'POST':
            form = MotherForm(request.POST)
            if form.is_valid():
                cleaned_data = convert_dates_to_strings(form.cleaned_data)
                update_session_data(request, cleaned_data)
                return redirect('survivor_details', survivor_index=1)

        else:
            form = MotherForm()

        return render(request, 'form_template.html', {'form': form, 'step': '5'})
    else:
        return redirect('survivor_details', survivor_index=1)


# Step 6: Mother Details


# Step 7: Survivor Details (Handles multiple survivors dynamically)
@login_required(login_url='/', redirect_field_name='next')
def survivor_details_view(request, survivor_index):
    number_of_survivors = request.session.get('number_of_survivors', 0)

    if number_of_survivors == 0:
        return redirect('form_success')  # Skip if no survivors

    if request.method == 'POST':
        form = SurvivorForm(request.POST)
        if form.is_valid():
            cleaned_data = convert_dates_to_strings(form.cleaned_data)
            update_session_data(request, {f'survivor_{survivor_index}': cleaned_data})

            if survivor_index < number_of_survivors:
                return redirect('survivor_details', survivor_index=survivor_index + 1)
            else:
                return redirect('form_success')

    else:
        form = SurvivorForm()

    return render(request, 'form_template.html', {'form': form, 'step': '7', 'survivor_index': survivor_index})


from django.shortcuts import render
from .models import Member


@login_required(login_url='/', redirect_field_name='next')
def members_without_images(request):
    members = Member.objects.filter(member_image__isnull=True)
    return render(request, 'members_without_images.html', {'members': members})


from django.shortcuts import get_object_or_404, redirect
from .forms import MemberImageUploadForm


@login_required(login_url='/', redirect_field_name='next')
def upload_member_image(request, member_id):
    member = get_object_or_404(Member, member_id=member_id)

    if request.method == 'POST':
        form = MemberImageUploadForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('members_without_images')  # Redirect after upload
    else:
        form = MemberImageUploadForm(instance=member)

    return render(request, 'upload_member_image.html', {'form': form, 'member': member})


# Step 8: Success Page (Shows collected data)
@login_required(login_url='/', redirect_field_name='next')
def form_success_view(request):
    data = json.loads(request.session.get('final_data5', '{}'))
    # Load all collected data
    data['registered_by'] = request.user.first_name
    print(data['registered_by'])
    member_entry(data)
    return render(request, 'form_success.html', {'data': data})  # Render success page


from .forms import MemberSearchForm


@login_required(login_url='/', redirect_field_name='next')
def member_form_view(request):
    if request.method == "POST":
        form = MemberSearchForm(request.POST)
        if form.is_valid():
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            phone = form.cleaned_data['phone_num']
            return redirect('users_search_view', f_name=f_name or 'none', l_name=l_name or 'none',
                            phone_num=phone or 'none')
    else:
        form = MemberSearchForm()

    return render(request, 'get_user_form.html', {'form': form})


from django.http import HttpResponse


@login_required(login_url='/', redirect_field_name='next')
def print_view(request, member_id):
    try:

        member = Member.objects.get(member_id=member_id)

        print(member.f_name)
        return render(request, 'print_view.html', {'member': member})
    except:
        return HttpResponse("Member not found.", status=404)

    # Handle member not found


@login_required(login_url='/', redirect_field_name='next')
def users_search_view(request, f_name, l_name, phone_num):
    members = Member.objects.filter(
        Q(f_name__iexact=f_name) | Q(l_name__iexact=l_name) | Q(phone_number=phone_num)
    )
    if members:
        return render(request, 'users_search_view.html', {'members': members})
    else:
        return HttpResponse("Member not found.", status=404)


from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Member
from .utils import print_pdf  # Import the utility function


@login_required(login_url='/', redirect_field_name='next')
def download_pdf(request, member_id):
    # print_pdf(member_id)
    try:
        # Generate the PDF using the utility function
        output_path = print_pdf(member_id)
        member = Member.objects.get(member_id=member_id)  # Get a single object
        member.is_printed = True  # Update the field
        member.save()  # Save changes to the database

        # Serve the PDF as a downloadable file
        with open(output_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="member_{member_id}.pdf"'
            return response

    except Exception as e:
        return HttpResponse("Member not found.", status=404)
def church_id(id_):
    len_ = str(id_)
    if len(len_)<5:
        l = len_.zfill(5)
    else:
        l = len_
    return f"GCOP-{l}"


@login_required(login_url='/', redirect_field_name='next')
def card_details(request, member_id):
    # print_pdf(member_id)
    # try:

        # Generate the PDF using the utility function
        member = Member.objects.get(member_id=member_id)


        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(church_id(member_id))  # Example data
        qr.make(fit=True)

        # Generate image in-memory
        img = qr.make_image(fill="black", back_color="white")

        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        church_branch = member.church_branch
        position = ChurchPositions.objects.get(member_id=member_id)# Get a single object
        return render(request, 'card_details.html', {'member': member,"church_branch":church_branch.branch_name,'position':position.position_name,"qr_code": qr_base64,'church_id':church_id(member_id)})

    # except Exception as e:
    #     return HttpResponse("Member not found.", status=404)


@login_required(login_url='/', redirect_field_name='next')
def to_print(request):
    members = Member.objects.filter(is_printed=False, member_image__isnull=False)

    return render(request, 'to_print.html', {'members': members})

    # return HttpResponse("No Members to print.", status=404)


@login_required(login_url='/', redirect_field_name='next')
def qr_code(request):
    return render(request, 'qr_scanner.html')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt  # Disable CSRF for testing (use proper security in production)
def check_id(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            scanned_id = data.get("id")

            # Check if ID exists in the database
            person_id = (ChurchID.objects.filter(gcop_id=scanned_id).first()).member_id
            person = Member.objects.get(member_id=person_id)


            if not person:
                return JsonResponse({"exists": False})

            # Check if the member has already been registered today
            today = now().date()
            already_registered = Attendance.objects.filter(
                member=person, scanned_at__date=today
            ).exists()

            if already_registered:
                return JsonResponse({
                    "exists": True,
                    "message": "Member has already been registered today",
                    "first_name": person.f_name,
                    "last_name": person.l_name
                })

            # Register attendance
            Attendance.objects.create(member=person)
            return JsonResponse({
                "exists": True,
                "message": "Attendance recorded successfully",
                "first_name": person.f_name,
                "last_name": person.l_name
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
