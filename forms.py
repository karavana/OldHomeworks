from django import forms

class AddPlaceForm(forms.Form):
	name = forms.CharField(label='Name',max_length=100)
	address = forms.CharField(label='Address',max_length=100)
	xcoord = forms.FloatField(label='X-Coord')
	ycoord = forms.FloatField(label='Y-Coord')
	
class CreateForm(forms.Form):
	username = forms.CharField(label='Username',max_length=100)
	password = forms.CharField(label='Password',max_length=100)

class LoginForm(forms.Form):
	username = forms.CharField(label='Username',max_length=100)
	password = forms.CharField(label='Password',max_length=100)

class AddEventForm(forms.Form):
	name = forms.CharField(label='Name',max_length=100)
	etype = forms.CharField(label='Type',max_length=100)
	age = forms.IntegerField(label='Age Limit')
	cap = forms.IntegerField(label='Capacity')

class ChangeRegionForm(forms.Form):
	xcoord_min = forms.FloatField(label='X-min')
	ycoord_min = forms.FloatField(label='Y-min')
	xcoord_max = forms.FloatField(label='X-max')
	ycoord_max = forms.FloatField(label='Y-max')
