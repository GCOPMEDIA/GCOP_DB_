from django import forms

positions = [


]

group_choices = [
    ('20',"Good Samaritan"),
    ('19',"Harvest Committee"),
    ('18',"Peace Group"),
    ('17',"Church Committee"),
    ('16',"Men's Fellowship"),
    ('12',"Clergy"),
    ('13',"Elder"),
    ('14',"Worker"),
    ('15',"Media"),
    ('11',"Youth Ministry"),
    ("2","Women's Fellowship"),
    ('3',"Church Choir"),
    ('4','Band'),
    ('5','Ushers'),
    ('6',"Tambourine"),
    ('7',"Prayer"),
    ('8','Children Ministry'),
    ('9','Singing Band'),
    ('10','Mercy Ladies'),
    ("1","Lyric Group")
]
gender_choices = [
    ('male',"Male"),
    ('female','Female')
]
married_status = [
    ("married",'Married')
    , ('divorced',"Divorced"),
    ('single','Single'),
    ('widowed','Widowed')
]
yes_or_no = [
    (True,"Yes"),
    (False,"No")

]
church_branches = [
    ('Mercy Temple','Mercy Temple'),
    ('Shalom Temple',"Shalom Temple"),
    ("Great is Jehovah","Great is Jehovah"),
    ("Christ the King","Christ the King"),
    ("Nhyira Temple","Nhyira Temple"),
    ("USA","USA"),
    ("CANADA","CANADA")
]
relation = [
    ('mother','Mother'),
    ('father','Father'),
    ('child','Child'),
    ('sibling',"Sibling"),
    ('aunty',"Aunty"),
    ('uncle','Uncle'),
    ('cousin',"Cousin"),
    ('niece',"Niece"),
    ('nephew','Nephew'),
    ('grandparent',"GrandParent")
]
parents = [
    ('Both',"Yes Both Are Alive"),
    ('Only Father','Yes But Only My Father'),
    ('Only Mother',"Yes But Only My Mother"),
    ('None',"No Both Are Dead")
]


class UserDetailsForm(forms.Form):
    first_name = forms.CharField(max_length=100, label="Surname ")
    other_name = forms.CharField(max_length=100, label="Other Names")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    phone = forms.CharField(max_length=15, label="Phone Number", required=False)
    emergency = forms.CharField(max_length=15,label='Emergency Contact',required=False)
    occupation = forms.CharField(max_length=100,label='Occupation',required=False)
    nxt_of_kin = forms.CharField(max_length=100,label='Name Of Next Of Kin',required=False)
    address = forms.CharField(max_length=100, label="Ghana Post Address")
    place_of_residence = forms.CharField(max_length=200, label="Place Of Residence",required=False)
    hometown = forms.CharField(max_length=100, label="Home Town")
    gender = forms.ChoiceField(choices=gender_choices,widget=forms.Select,label='Gender')
    baptism = forms.ChoiceField(choices=yes_or_no,widget=forms.Select,label='Have You Been Baptized? ')
    baptist_at_gcop = forms.ChoiceField(choices=yes_or_no,widget=forms.Select,label='Were You Baptized At GCOP?')
    history = forms.CharField(widget=forms.Textarea(attrs={'row':4,'cols':100}),label='Brief History')




class FurtherQuestionsForm(forms.Form):
    marital_status = forms.ChoiceField(choices=married_status, widget=forms.Select, label='Marital Status')
    number_of_children = forms.IntegerField(label='Number Of Children')
    number_of_survivors = forms.IntegerField(label="Number Of Close Relatives")
    parent_status = forms.ChoiceField(label='Are Your Parents Still Alive?',choices=parents)
    date_joined = forms.DateField( label="What Year Did You Join GCOP", required=False,help_text='mm/dd/yy')
    welfare_card_number = forms.CharField(max_length=200, label="Welfare Card Number if any",required=False)
    tithe_card_number = forms.CharField(max_length=200, label='Tithe And Dues Card Number if any',required=False)
    church_branch = forms.ChoiceField(choices=church_branches,widget=forms.Select)
    group_name = forms.MultipleChoiceField(choices=group_choices,widget=forms.SelectMultiple(attrs={'class': 'multi-dropdown'}))
    position = forms.CharField(max_length=250, label='What Position Do You Hold')


class NextForm(forms.Form):
    child_first_name = forms.CharField(max_length=250, label="Child's Surname")
    child_other_name = forms.CharField(max_length=250, label="Child's Other Names")
    child_phone_number = forms.CharField(max_length=15, label="Child's Phone Number", required=False)
    child_is_member = forms.ChoiceField(choices=yes_or_no, widget=forms.Select, label='Is Your Child A Member Of GCOP?')

class FatherForm(forms.Form):
    father_first_name = forms.CharField(max_length=250, label="Father's Surname")
    father_other_name = forms.CharField(max_length=250, label="Father's Other Names")
    father_phone_number = forms.CharField(max_length=15, label="Father's Phone Number", required=False)
    father_is_member = forms.ChoiceField(choices=yes_or_no, widget=forms.Select,
                                         label='Is Your Father A Member Of GCOP?')
class MotherForm(forms.Form):
    mother_first_name = forms.CharField(max_length=250, label="Mother's Surname")
    mother_other_name = forms.CharField(max_length=250, label="Mother's Other Names")
    mother_phone_number = forms.CharField(max_length=15, label="Mother's Phone Number", required=False)
    mother_is_member = forms.ChoiceField(choices=yes_or_no, widget=forms.Select,
                                         label='Is Your Mother A Member Of GCOP?')
class SurvivorForm(forms.Form):
    survivor_first_name = forms.CharField(max_length=250, label="Relative's Surname")
    survivor_other_name = forms.CharField(max_length=250, label="Relative's Other Names")
    survivor_phone_number = forms.CharField(max_length=15, label="Relative's Phone Number", required=False)
    survivor_relation = forms.ChoiceField(choices=relation,widget=forms.Select,label="Relationship With Relative")
    survivor_is_member = forms.ChoiceField(choices=yes_or_no, widget=forms.Select,
                                         label='Is Your Relative A Member Of GCOP?')

class SpouseForm(forms.Form):
    spouse_first_name = forms.CharField(max_length=250, label="Spouse's Surname")
    spouse_other_name = forms.CharField(max_length=250, label="Spouse's Other Names")
    spouse_phone_number = forms.CharField(max_length=15, label="Spouse's Phone Number")
    spouse_is_member = forms.ChoiceField(choices=yes_or_no, widget=forms.Select,
                                         label='Is Your Spouse A Member Of GCOP?')

from django import forms
from .models import Member

class MemberImageUploadForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['member_image']


from django import forms

class MemberSearchForm(forms.Form):
    f_name = forms.CharField(label="Surname", max_length=100,required=False )
    l_name = forms.CharField(label="Other Names", max_length=100,required=False )
    phone_num = forms.CharField(label="Phone Number", max_length=15,required=False )



