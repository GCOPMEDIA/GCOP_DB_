from django import forms
from django_select2.forms import Select2MultipleWidget

group_choices = [
    ('youth',"Youth"),
    ("elders","Elders"),
    ('pastors',"Pastors")
]
gender_choices = [
    ('male',"Male"),
    ('female','Female')
]
married_status = [
    ("married",'Married')
    , ('divorced',"Divorced"),
    ('single','Single')
]
yes_or_no = [
    (True,"Yes"),
    (False,"No")

]
church_branches = [
    ('mercy temple','Mercy Temple'),
    ('something',"temple")
]
relation = [
    ('mother','Mother'),
    ('father','Father'),
    ('child','Child'),
    ('sibling',"Sibling")
]

class UserDetailsForm(forms.Form):
    first_name = forms.CharField(max_length=100, label="First Name")
    other_name = forms.CharField(max_length=100, label="Other Names")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    phone = forms.CharField(max_length=15, label="Phone Number", required=False)
    address = forms.CharField(max_length=100, label="Ghana Post Address")
    hometown = forms.CharField(max_length=100, label="Home Town")
    gender = forms.ChoiceField(choices=gender_choices,widget=forms.Select)
    marital_status = forms.ChoiceField(choices=married_status, widget=forms.Select,label='Marital Status')


class FurtherQuestionsForm(forms.Form):
    number_of_children = forms.IntegerField(label='Number Of Children')
    number_of_survivors = forms.IntegerField(label="Number Of Survivors")
    date_joined = forms.DateField( label="What Year Did You Join GCOP", required=False)
    welfare_card_number = forms.CharField(max_length=200, label="Welfare Card Number if any")
    tithe_card_number = forms.CharField(max_length=200, label='Tithe Card Number if any')
    church_branch = forms.ChoiceField(choices=church_branches,widget=forms.Select)
    groups_joined = forms.MultipleChoiceField(choices=group_choices, widget=forms.CheckboxSelectMultiple,label='Which Branch Do You Worship With')


class NextForm(forms.Form):
    child_first_name = forms.CharField(max_length=250, label="Child's First Name")
    child_other_name = forms.CharField(max_length=250, label="Child's Other Names")
    child_phone_number = forms.CharField(max_length=15, label="Child's Phone Number", required=False)
    child_is_member = forms.ChoiceField(choices=yes_or_no, widget=forms.Select, label='Is Your Child A Member Of GCOP?')

class FatherForm(forms.Form):
    father_first_name = forms.CharField(max_length=250, label="Father's First Name")
    father_other_name = forms.CharField(max_length=250, label="Father's Other Names")
    father_phone_number = forms.CharField(max_length=15, label="Father's Phone Number", required=False)
    father_is_member = forms.ChoiceField(choices=yes_or_no, widget=forms.Select,
                                         label='Is Your Father A Member Of GCOP?')
class MotherForm(forms.Form):
    mother_first_name = forms.CharField(max_length=250, label="Mother's First Name")
    mother_other_name = forms.CharField(max_length=250, label="Mother's Other Names")
    mother_phone_number = forms.CharField(max_length=15, label="Mother's Phone Number", required=False)
    mother_is_member = forms.ChoiceField(choices=yes_or_no, widget=forms.Select,
                                         label='Is Your Mother A Member Of GCOP?')
class SurvivorForm(forms.Form):
    survivor_first_name = forms.CharField(max_length=250, label="Survivor's First Name")
    survivor_other_name = forms.CharField(max_length=250, label="Survivor's Other Names")
    survivor_phone_number = forms.CharField(max_length=15, label="Survivor's Phone Number", required=False)
    survivor_relation = forms.ChoiceField(choices=relation,widget=forms.Select,label="Relationship With Survivor")
    survivor_is_member = forms.ChoiceField(choices=yes_or_no, widget=forms.Select,
                                         label='Is Your Survivor A Member Of GCOP?')


