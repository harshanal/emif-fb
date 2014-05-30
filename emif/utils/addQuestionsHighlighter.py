from questionnaire.models import *
from searchengine.models import *
from django.shortcuts import render_to_response, get_object_or_404
import sys
import re

p = re.compile("(\\d{1,2})(\.\\d{2})*$", re.L)

#qsets = QuestionSet.objects.all()
slugs = []
questionaires = Questionnaire.objects.filter(disable=False)
for quest in questionaires:
	id = quest.id
	obj = {"id":"questionaire_"+str(id)}
	qsets = QuestionSet.objects.filter(questionnaire=quest)
	for qs in qsets:
		#print qs
		questions = qs.questions()
		for q in questions:
			x = q.slug_fk
			key = str(x.slug1) + "_qs"
			obj[key] = q.text
	slugs.append(obj)

		
print slugs

import pysolr

host1 = "localhost"
port1 = str(8983)


solr = pysolr.Solr('http://' +host1+ ':'+ port1+'/solr')
start=0
rows=100
fl=''

solr.add(slugs)

#solr.delete(q="id:questionaire_*")



#if len(wrongs)> 0:
#	for s in changes:
#		questions = Question.objects.filter(id=s["id"])
#		for q in questions:
#			q.number = s["number"]
#			q.save()
#			print "Saved " +str(q)

# for qs in qsets:
#  	print "iterate questions"
#  	print qs
#  	question = create_question(qs)
# 	question.save()
# 	print "Saved Question"
# 	updateSlug(question)

print "QUITTING"