# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

def index(request):
	return render(request, "user_app/index.html")

def register(request):
	response = User.objects.register(request.POST)
	if response["isValid"]:
		request.session["user_id"] = response["user"].id
		messages.add_message(request, messages.SUCCESS, "You have successfully made an account, good job!")
		return redirect("/dashboard")
	else:
		for error in response["errors"]:
			messages.add_message(request, messages.ERROR, error)
		return redirect("/")

def login(request):
	response = User.objects.login(request.POST)
	if response["isValid"]:
		request.session["user_id"] = response["user"].id
		messages.add_message(request, messages.SUCCESS, "You remembered your password, GJ!")
		return redirect("/dashboard")
	else:
		for error in response["errors"]:
			messages.add_message(request, messages.ERROR, error)
		return redirect("/")

def logout(request):
	request.session.clear()
	messages.add_message(request, messages.SUCCESS, "Wait don't go!")
	return redirect("/")