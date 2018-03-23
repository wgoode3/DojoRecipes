# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def register(self, post_data):

		response = {
			"isValid": True,
			"errors": [],
			"user": None
		}

		if len(post_data["username"]) < 1:
			response["isValid"] = False
			response["errors"].append("Username is required")
		elif len(post_data["username"]) < 3:
			response["isValid"] = False
			response["errors"].append("Username must be 3 characters or longer")

		if len(post_data["email"]) < 1:
			response["isValid"] = False
			response["errors"].append("Email is required")
		elif not EMAIL_REGEX.match(post_data["email"]):
			response["isValid"] = False
			response["errors"].append("Invalid email")
		else:
			list_of_users_matching_email = User.objects.filter(email=post_data["email"].lower())
			if len(list_of_users_matching_email) > 0:
				response["isValid"] = False
				response["errors"].append("Email is already in use")

		if len(post_data["password"]) < 1:
			response["isValid"] = False
			response["errors"].append("Password is required")
		elif len(post_data["password"]) < 8:
			response["isValid"] = False
			response["errors"].append("Password must be 8 characters or longer")

		if len(post_data["confirm"]) < 1:
			response["isValid"] = False
			response["errors"].append("Confim Password is required")
		elif post_data["confirm"] != post_data["password"]:
			response["isValid"] = False
			response["errors"].append("Confim Password must match Password")

		if response["isValid"]:
			response["user"] = User.objects.create(
				username = post_data["username"],
				email = post_data["email"].lower(),
				password = bcrypt.hashpw(post_data["password"].encode(), bcrypt.gensalt())
			)

		return response

	def login(self, post_data):
		
		response = {
			"isValid": True,
			"errors": [],
			"user": None
		}

		if len(post_data["email"]) < 1:
			response["isValid"] = False
			response["errors"].append("Email is required")
		elif not EMAIL_REGEX.match(post_data["email"]):
			response["isValid"] = False
			response["errors"].append("Invalid email")
		else:
			list_of_users_matching_email = User.objects.filter(email=post_data["email"].lower())
			if len(list_of_users_matching_email) < 1:
				response["isValid"] = False
				response["errors"].append("Unknown email {}".format(post_data["email"]))

		if len(post_data["password"]) < 1:
			response["isValid"] = False
			response["errors"].append("Password is required")
		elif len(post_data["password"]) < 8:
			response["isValid"] = False
			response["errors"].append("Password must be 8 characters or longer")

		if response["isValid"]:
			user = list_of_users_matching_email[0]
			if not bcrypt.checkpw(post_data["password"].encode(), user.password.encode()):
				response["isValid"] = False
				response["errors"].append("Incorrect password")
			else:
				response["user"] = user
			
		return response

class User(models.Model):
	username = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()
