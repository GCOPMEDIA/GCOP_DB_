from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
import json
from datetime import date
from .forms import UserDetailsForm, FurtherQuestionsForm, NextForm, FatherForm, MotherForm, SurvivorForm, SpouseForm

# Utility function to convert date fields to strings
def convert_dates_to_strings(data):
    """Recursively converts all date objects in a dictionary to string format (YYYY-MM-DD)."""
    for key, value in data.items():
        if isinstance(value, date):
            data[key] = value.strftime('%Y-%m-%d')
    return data
def login_(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('user_form')
        else:
            return HttpResponse(status=403)
    else:
        return render(request,'registration/login.html',{})

# Utility function to update session data
def update_session_data(request, new_data):
    """Merge new form data into session storage (final_data5) to accumulate all responses."""
    user_data = json.loads(request.session.get('final_data5', '{}'))  # Load existing session data
    user_data.update(new_data)  # Merge new data
    request.session['final_data5'] = json.dumps(user_data, cls=DjangoJSONEncoder)  # Store back
    request.session.modified = True  # Ensure session is saved

# Step 1: User Details Form
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
    else:return HttpResponse(status=403)

# Step 2: Further Questions (Collecting number of children and survivors)
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

# Step 8: Success Page (Shows collected data)
def form_success_view(request):
    data = json.loads(request.session.get('final_data5', '{}'))  # Load all collected data
    return render(request, 'form_success.html', {'data': data})  # Render success page