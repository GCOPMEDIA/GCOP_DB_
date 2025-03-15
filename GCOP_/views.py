from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from datetime import date
import json

from .forms import *
from .models import Member
from .utils import print_pdf, member_entry


# ================================
# Authentication & Utility Functions
# ================================

def login_(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'user_form')  # Redirect to intended page
            return redirect(next_url)
        else:
            return HttpResponse(status=403)
    return render(request, 'registration/login.html', {})


def convert_dates_to_strings(data):
    """Recursively converts all date objects in a dictionary to string format (YYYY-MM-DD)."""
    for key, value in data.items():
        if isinstance(value, date):
            data[key] = value.strftime('%Y-%m-%d')
    return data



def update_session_data(request, new_data):
    """Merge new form data into session storage to accumulate all responses."""
    user_data = json.loads(request.session.get('final_data5', '{}'))
    user_data.update(new_data)
    request.session['final_data5'] = json.dumps(user_data, cls=DjangoJSONEncoder)
    request.session.modified = True


# ================================
# Multi-Step Form Views
# ================================

class UserFormView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        form = UserDetailsForm()
        return render(request, 'form_template.html', {'form': form, 'step': '1'})

    def post(self, request):
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            cleaned_data = convert_dates_to_strings(form.cleaned_data)
            update_session_data(request, cleaned_data)
            return redirect('further_questions')
        return render(request, 'form_template.html', {'form': form, 'step': '1'})


class FurtherQuestionsView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        form = FurtherQuestionsForm()
        return render(request, 'form_template.html', {'form': form, 'step': '2'})

    def post(self, request):
        form = FurtherQuestionsForm(request.POST)
        if form.is_valid():
            cleaned_data = convert_dates_to_strings(form.cleaned_data)
            request.session.update({
                'number_of_children': int(cleaned_data.get('number_of_children', 0)),
                'number_of_survivors': int(cleaned_data.get('number_of_survivors', 0)),
                'marital_status': cleaned_data.get('marital_status', 'single'),
                'parent_status': cleaned_data.get('parent_status', 'None')
            })
            update_session_data(request, cleaned_data)

            if request.session['marital_status'] == 'married':
                return redirect('spouse_details')
            elif request.session['number_of_children'] > 0:
                return redirect('child_details', child_index=1)
            elif request.session['parent_status'] != 'None':
                return redirect('father_details')
            return redirect('survivor_details', survivor_index=1)


class SpouseDetailsView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        form = SpouseForm()
        return render(request, 'form_template.html', {'form': form, 'step': 'spouse'})

    def post(self, request):
        form = SpouseForm(request.POST)
        if form.is_valid():
            cleaned_data = convert_dates_to_strings(form.cleaned_data)
            update_session_data(request, cleaned_data)

            if request.session.get('number_of_children', 0) > 0:
                return redirect('child_details', child_index=1)
            elif request.session.get('parent_status', 'None') != 'None':
                return redirect('father_details')
            return redirect('survivor_details', survivor_index=1)



class ChildDetailsView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request, child_index):
        number_of_children = request.session.get('number_of_children', 0)
        if number_of_children == 0:
            return redirect('father_details')

        form = NextForm()
        return render(request, 'form_template.html', {'form': form, 'step': f'child_{child_index}'})

    def post(self, request, child_index):
        form = NextForm(request.POST)
        if form.is_valid():
            cleaned_data = convert_dates_to_strings(form.cleaned_data)
            update_session_data(request, {f'child_{child_index}': cleaned_data})

            if child_index < request.session.get('number_of_children', 0):
                return redirect('child_details', child_index=child_index + 1)

            return redirect('father_details')



class FatherDetailsView(LoginRequiredMixin, View):
    def get(self, request):
        if request.session.get('parent_status') in ['Both', 'Only Father']:
            form = FatherForm()
            return render(request, 'form_template.html', {'form': form, 'step': '4'})
        return redirect('mother_details')

    def post(self, request):
        form = FatherForm(request.POST)
        if form.is_valid():
            update_session_data(request, convert_dates_to_strings(form.cleaned_data))
            return redirect('mother_details')
        return render(request, 'form_template.html', {'form': form, 'step': '4'})





class SurvivorDetailsView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request, survivor_index):
        number_of_survivors = request.session.get('number_of_survivors', 0)
        if number_of_survivors == 0:
            return redirect('form_success')

        form = SurvivorForm()
        return render(request, 'form_template.html', {'form': form, 'step': '7', 'survivor_index': survivor_index})

    def post(self, request, survivor_index):
        form = SurvivorForm(request.POST)
        if form.is_valid():
            cleaned_data = convert_dates_to_strings(form.cleaned_data)
            update_session_data(request, {f'survivor_{survivor_index}': cleaned_data})

            if survivor_index < request.session.get('number_of_survivors', 0):
                return redirect('survivor_details', survivor_index=survivor_index + 1)

            return redirect('form_success')





class FormSuccessView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        data = json.loads(request.session.get('final_data5', '{}'))
        member_entry(data)
        return render(request, 'form_success.html', {'data': data})



# ================================
# Member Management Views
# ================================




class MembersWithoutImagesView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        members = Member.objects.filter(member_image__isnull=True)
        return render(request, 'members_without_images.html', {'members': members})




  # Import the form

class UploadMemberImageView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request, member_id):
        member = get_object_or_404(Member, member_id=member_id)
        form = MemberImageUploadForm(instance=member)
        return render(request, 'upload_member_image.html', {'form': form, 'member': member})

    def post(self, request, member_id):
        member = get_object_or_404(Member, member_id=member_id)
        form = MemberImageUploadForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('members_without_images')

        return render(request, 'upload_member_image.html', {'form': form, 'member': member})





class DownloadPDFView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request, member_id):
        try:
            output_path = print_pdf(member_id)
            with open(output_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="member_{member_id}.pdf"'
                return response
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)



















# ================================
# Authentication & Utility Functions
# ================================





def update_session_data(request, new_data):
    """Merge new form data into session storage to accumulate all responses."""
    user_data = json.loads(request.session.get('final_data5', '{}'))
    user_data.update(new_data)
    request.session['final_data5'] = json.dumps(user_data, cls=DjangoJSONEncoder)
    request.session.modified = True


# ================================
# Multi-Step Form Views
# ================================

class MotherDetailsView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        if request.session.get('parent_status') in ['Both', 'Only Mother']:
            form = MotherForm()
            return render(request, 'form_template.html', {'form': form, 'step': '5'})
        return redirect('survivor_details', survivor_index=1)

    def post(self, request):
        form = MotherForm(request.POST)
        if form.is_valid():
            update_session_data(request, convert_dates_to_strings(form.cleaned_data))
            return redirect('survivor_details', survivor_index=1)
        return render(request, 'form_template.html', {'form': form, 'step': '5'})


class MemberFormView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = MemberSearchForm()
        return render(request, 'member_form.html', {'form': form})

    def post(self, request):
        form = MemberSearchForm(request.POST)
        if form.is_valid():
            return redirect('users_search_view', search_query=form.cleaned_data['search_query'])
        return render(request, 'member_form.html', {'form': form})




class UsersSearchView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        search_query = request.GET.get('search_query', '').strip()
        members = Member.objects.filter(name__icontains=search_query) if search_query else None
        return render(request, 'users_search.html', {'members': members, 'search_query': search_query})




class PrintView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request, member_id):
        """Displays a member's details for printing."""
        member = get_object_or_404(Member, member_id=member_id)
        return render(request, 'print_view.html', {'member': member})


# ================================
# Other Views (Previously Included)
# ===========


# from django.contrib.auth.mixins import UserPassesTestMixin
#
# class SuperAdminRequiredMixin(UserPassesTestMixin):
#     login_url = '/'  # Redirect to homepage or login if needed
#
#     def test_func(self):
#         return self.request.user.is_superuser  # Only allow superadmins
#
#     def handle_no_permission(self):
#         return redirect('user_form')  # Redirect unauthorized users to UserFormView
#
#
# class MembersWithoutImagesView(LoginRequiredMixin, SuperAdminRequiredMixin, View):
#     def get(self, request):
#         members = Member.objects.filter(member_image__isnull=True)
#         return render(request, 'members_without_images.html', {'members': members})
#
#
# class UploadMemberImageView(LoginRequiredMixin, SuperAdminRequiredMixin, View):
#     def get(self, request, member_id):
#         member = get_object_or_404(Member, member_id=member_id)
#         form = MemberImageUploadForm(instance=member)
#         return render(request, 'upload_member_image.html', {'form': form, 'member': member})
#
#     def post(self, request, member_id):
#         member = get_object_or_404(Member, member_id=member_id)
#         form = MemberImageUploadForm(request.POST, request.FILES, instance=member)
#         if form.is_valid():
#             form.save()
#             return redirect('members_without_images')
#         return render(request, 'upload_member_image.html', {'form': form, 'member': member})
#
#
# class PrintView(LoginRequiredMixin, SuperAdminRequiredMixin, View):
#     def get(self, request, member_id):
#         member = get_object_or_404(Member, member_id=member_id)
#         return render(request, 'print_view.html', {'member': member})
#
#
# class MemberFormView(LoginRequiredMixin, SuperAdminRequiredMixin, View):
#     def get(self, request):
#         form = MemberSearchForm()
#         return render(request, 'member_form.html', {'form': form})
#
#     def post(self, request):
#         form = MemberSearchForm(request.POST)
#         if form.is_valid():
#             return redirect('users_search_view', search_query=form.cleaned_data['search_query'])
#         return render(request, 'get_user_form.html', {'form': form})
#
#
# class UsersSearchView(LoginRequiredMixin, SuperAdminRequiredMixin, View):
#     def get(self, request):
#         search_query = request.GET.get('search_query', '').strip()
#         members = Member.objects.filter(name__icontains=search_query) if search_query else None
#         return render(request, 'users_search.html', {'members': members, 'search_query': search_query})
#
#
# class DownloadPDFView(LoginRequiredMixin, SuperAdminRequiredMixin, View):
#     def get(self, request, member_id):
#         try:
#             output_path = print_pdf(member_id)
#             with open(output_path, 'rb') as pdf_file:
#                 response = HttpResponse(pdf_file.read(), content_type='application/pdf')
#                 response['Content-Disposition'] = f'attachment; filename="member_{member_id}.pdf"'
#                 return response
#         except Exception as e:
#             return HttpResponse(f"An error occurred: {e}", status=500)
#
#
#
