from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
import json
from datetime import date
from .forms import UserDetailsForm, FurtherQuestionsForm, NextForm, FatherForm, MotherForm, SurvivorForm

# Utility function to convert date fields to strings
def convert_dates_to_strings(data):
    """Recursively converts all date objects in a dictionary to string format (YYYY-MM-DD)."""
    for key, value in data.items():
        if isinstance(value, date):
            data[key] = value.strftime('%Y-%m-%d')
    return data

# Utility function to update session data
def update_session_data(request, new_data):
    """Merge new form data into session storage (final_data5) to accumulate all responses."""
    user_data = json.loads(request.session.get('final_data5', '{}'))  # Load existing session data
    user_data.update(new_data)  # Merge new data
    request.session['final_data5'] = json.dumps(user_data, cls=DjangoJSONEncoder)  # Store back
    request.session.modified = True  # Ensure session is saved


# Step 1: User Details Form
def user_form_view(request):
    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            cleaned_data = convert_dates_to_strings(form.cleaned_data)
            update_session_data(request, cleaned_data)
            return redirect('further_questions')  # Move to Step 2

    else:
        form = UserDetailsForm()

    return render(request, 'form_template.html', {'form': form, 'step': '1'})


# Step 2: Further Questions (Collecting number of children and survivors)
def further_questions_view(request):
    if request.method == 'POST':
        form = FurtherQuestionsForm(request.POST)
        if form.is_valid():
            cleaned_data = convert_dates_to_strings(form.cleaned_data)

            # Store numbers for child & survivor processing
            request.session['num_children'] = int(cleaned_data.get('number_of_children', 0))
            request.session['num_survivors'] = int(cleaned_data.get('number_of_survivors', 0))

            update_session_data(request, cleaned_data)
            return redirect('child_details', child_index=1)  # Start with first child

    else:
        form = FurtherQuestionsForm()

    return render(request, 'form_template.html', {'form': form, 'step': '2'})


# Step 3: Child Details (Handles multiple children dynamically)
def child_details_view(request, child_index):
    num_children = request.session.get('num_children', 0)

    if request.method == 'POST':
        form = NextForm(request.POST)
        if form.is_valid():
            cleaned_data = convert_dates_to_strings(form.cleaned_data)
            update_session_data(request, {f'child_{child_index}': cleaned_data})

            if child_index < num_children:
                return redirect('child_details', child_index=child_index + 1)
            else:
                return redirect('father_details')

    else:
        form = NextForm()

    return render(request, 'form_template.html', {'form': form, 'step': '3', 'child_index': child_index})


# Step 4: Father Details
def father_details(request):
    if request.method == 'POST':
        form = FatherForm(request.POST)
        if form.is_valid():
            cleaned_data = convert_dates_to_strings(form.cleaned_data)
            update_session_data(request, cleaned_data)
            return redirect('mother_details')

    else:
        form = FatherForm()

    return render(request, 'form_template.html', {'form': form, 'step': '4'})


# Step 5: Mother Details
def mother_details(request):
    if request.method == 'POST':
        form = MotherForm(request.POST)
        if form.is_valid():
            cleaned_data = convert_dates_to_strings(form.cleaned_data)
            update_session_data(request, cleaned_data)

            # Ensure survivor index is tracked properly
            request.session['current_survivor_index'] = 1  # Initialize survivor index
            return redirect('survivor_details', survivor_index=1)

    else:
        form = MotherForm()

    return render(request, 'form_template.html', {'form': form, 'step': '5'})


# Step 6: Survivor Details (Handles multiple survivors dynamically)
def survivor_details_view(request, survivor_index):
    num_survivors = request.session.get('num_survivors', 0)

    if request.method == 'POST':
        form = SurvivorForm(request.POST)
        if form.is_valid():
            cleaned_data = convert_dates_to_strings(form.cleaned_data)
            update_session_data(request, {f'survivor_{survivor_index}': cleaned_data})

            if survivor_index < num_survivors:
                return redirect('survivor_details', survivor_index=survivor_index + 1)
            else:
                return redirect('form_success')

    else:
        form = SurvivorForm()

    return render(request, 'form_template.html', {'form': form, 'step': '6', 'survivor_index': survivor_index})


# Step 7: Success Page (Shows collected data)
def form_success_view(request):
    data = json.loads(request.session.get('final_data5', '{}'))  # Load all collected data
    return render(request, 'form_success.html', {'data': data})  # Render success page
