# coding=utf-8
from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField, validators, ValidationError
class ContactForm(Form):
	name = TextField("Name",[validators.Required("Please enter your name. ")])
	email = TextField("Email",[validators.Required("Please enter your email address."),validators.Email("请正确输入您的邮件地址")])
	subject = TextField("Subject",[validators.Required("Please enter a subject.")])
	message = TextAreaField("Message",[validators.Required("Please enter a message.")])
	submit = SubmitField("Send")
