from django import forms

positions = [


]

group_choices = [
    ('clergy',"Clergy"),
    ('elder',"Elder"),
    ('worker',"Worker"),
    ('media',"Media"),
    ('12',"Youth"),
    ("2","Women's Fellowship"),
    ('4',"Choir"),
    ('5','Band'),
    ('6','Ushers'),
    ('7',"Tambourine"),
    ('8',"Prayer"),
    ("9",'Youth Choir'),
    ('10','Singing Band'),
    ('11','Mercy Ladies'),
    ("1","Lyric Group")
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
parents = [
    ('Both',"Yes Both Are Alive"),
    ('Only Father','Yes But Only My Father'),
    ('Only Mother',"Yes But Only My Mother"),
    ('None',"No Both Are Dead")
]


class UserDetailsForm(forms.Form):
    first_name = forms.CharField(max_length=100, label="First Name")
    other_name = forms.CharField(max_length=100, label="Other Names")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    phone = forms.CharField(max_length=15, label="Phone Number", required=False)
    address = forms.CharField(max_length=100, label="Ghana Post Address")
    hometown = forms.CharField(max_length=100, label="Home Town")
    gender = forms.ChoiceField(choices=gender_choices,widget=forms.Select)




class FurtherQuestionsForm(forms.Form):
    marital_status = forms.ChoiceField(choices=married_status, widget=forms.Select, label='Marital Status')
    number_of_children = forms.IntegerField(label='Number Of Children')
    number_of_survivors = forms.IntegerField(label="Number Of Close Relatives")
    parent_status = forms.ChoiceField(label='Are Your Parents Still Alive?',choices=parents)
    date_joined = forms.CharField( label="What Year Did You Join GCOP", required=False,help_text='eg:2025')
    welfare_card_number = forms.CharField(max_length=200, label="Welfare Card Number if any",required=False)
    tithe_card_number = forms.CharField(max_length=200, label='Tithe Card Number if any',required=False)
    church_branch = forms.ChoiceField(choices=church_branches,widget=forms.Select)
    group_name = forms.MultipleChoiceField(choices=group_choices,widget=forms.SelectMultiple(attrs={'class': 'multi-dropdown'}))
    position = forms.CharField(max_length=250, label='What Position Do You Hold')


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
    survivor_first_name = forms.CharField(max_length=250, label="Relative's First Name")
    survivor_other_name = forms.CharField(max_length=250, label="Relative's Other Names")
    survivor_phone_number = forms.CharField(max_length=15, label="Relative's Phone Number", required=False)
    survivor_relation = forms.ChoiceField(choices=relation,widget=forms.Select,label="Relationship With Relative")
    survivor_is_member = forms.ChoiceField(choices=yes_or_no, widget=forms.Select,
                                         label='Is Your Relative A Member Of GCOP?')

class SpouseForm(forms.Form):
    spouse_first_name = forms.CharField(max_length=250, label="Spouse's First Name")
    spouse_other_name = forms.CharField(max_length=250, label="Spouse's Other Names")
    spouse_phone_number = forms.CharField(max_length=15, label="Spouse's Phone Number")
    spouse_is_member = forms.ChoiceField(choices=yes_or_no, widget=forms.Select,
                                         label='Is Your Spouse A Member Of GCOP?')



