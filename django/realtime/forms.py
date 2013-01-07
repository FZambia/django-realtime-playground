# coding: utf-8
from django import forms
from realtime import models


class MessageForm(forms.ModelForm):
	
	class Meta:
		model = models.Message