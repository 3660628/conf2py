# -*- coding: utf-8 -*- 

response.menu = [
    [T('Home'), False,URL(request.application,'default','index'), []],
    [T('Attendees'), False,URL(request.application,'default','attendees'), []],
    [T('Papers'), False,URL(request.application,'default','list_papers'), []],
    [T('Agenda'), False,URL(request.application,'default','agenda'), []],
    [T('Directions'), False,URL(request.application,'default','directions'), []],
   ]

