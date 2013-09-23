# -*- coding: utf-8 -*-

# Copyright (C) 2013 Luís A. Bastião Silva and Universidade de Aveiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
import re
from searchengine.models import Nomenclature
from datetime import datetime
from searchengine.search_indexes import CoreEngine
from searchengine.models import Slugs

from questionnaire.models import Question, Questionnaire, QuestionSet

import md5
import random

from django.conf import settings


def generate_hash():
    hash = md5.new()
    hash.update("".join(map(lambda i: chr(random.randint(0, 255)), range(16))))
    hash.update(settings.SECRET_KEY)
    key = hash.hexdigest()
    return key


def convert_text_to_slug(text):
    #TODO: optimize
    return text.replace(' ', '_').replace('?','').replace('.', '').replace(',','')


def clean_value(v):
    if isinstance(v, str):
        logging.debug("Value: " + v)
        #print "Value: " + v

        v = re.sub(r"\[|\]", "", v)
        logging.debug("Value after clean: " + v)
    elif isinstance(v, list):
        print "list"
        for v_aux in v:
            v += v_aux + " "
    return v

def convert_date(d):
    new_date = datetime.strptime(d, '%Y-%m-%d %H:%M:%S.%f')
    return new_date.strftime("%Y-%m-%d %H:%M")


def get_nomenclature(institution_name, database_name):
    """
    Get the nomenclature to the database based on institution name 
    """
    value = clean_value(institution_name+"_"+database_name)
    slug = convert_text_to_slug(value)
    return slug



def database_exists(database_name):
    """
    Verify if the nomenclature database name already exists
    """
    results = Nomenclature.objects.filter(name=database_name)
    if len(results)==0:
        return False
    else:
        return True

class Database:
    id = ''
    name = ''
    date = ''
    institution = ''
    location = ''
    email_contact = ''
    number_patients = ''
    ttype = ''
    logo = ''

class ordered_dict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self._order = self.keys()

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        if key in self._order:
            self._order.remove(key)
        self._order.append(key)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._order.remove(key)

    def order(self):
        return self._order[:]

    def ordered_items(self):
        return [(key,self[key]) for key in self._order]


        
class Tag:
        
        def __init__(self):
            self.tag = ''
            self.value = ''
            self.extra = ''   

        def __eq__(self, other):
            return other.tag == self.tag


        def __cmp__(self, other):
            return cmp(other.tag, self.tag)

        def __str__(self):
            return self.tag + ", " + self.value 

class QuestionGroup:
    
    def __init__(self):
        self.list_ordered_tags = []
        self.name = ""
        self.sortid = ""

    def __eq__(self, other):
        return other.name == self.name

    def __lt__ (self, other):
        
        return self.sortid < other.sortid

    def __gt__ (self, other):
        return other.__lt__(self)

    def __str__(self):
        return self.name
        #for tag in list_ordered_tags:
        #    print tag
def get_database_from_id(id):
    c = CoreEngine()
    results = c.search_fingerprint("id:"+id)
    database_aux = None
    for r in results:
        try:
            database_aux = Database()
            print r['id']
            print r['created_t']
            print r['database_name_t']
            database_aux.id = r['id']
            database_aux.date = convert_date(r['created_t'])
           
            database_aux.name = r['database_name_t']
            
            break
        except:
            pass
    return database_aux

def get_database_from_id_with_tlv(db):
    c = CoreEngine()
    results = c.search_fingerprint('id:'+db.id)
    class Tag:
        tag = ''
        value = ''

    list_values = []
    blacklist = ['created_t', 'type_t', '_version_']
    name = "Not defined"
    
    for result in results:
        for k in result:
            if k in blacklist:
                continue
            t = Tag()
            results = Slugs.objects.filter(slug1=k)
            if len(results)>0:
                text = results[0].description 
            else:
                text = k
            info = text[:75] + (text[75:] and '..')

            t.tag = info

            value = clean_value(str(result[k]))
            value = value[:75] + (value[75:] and '..')
            t.value = value
            if k== "database_name_t":
                name = t.value
            list_values.append(t)
        break
    db.fields = list_values
    return db

WORKSPACE_PATH={'Workspace'}
 
def convert_dict_to_query(params):
    query = ""
    i = 0 
    size_params = len(params)
    for key in params:
        query += key+"_t:" + params[key]+"*"
        i = i + 1 
        if (size_params != i ):
            query += " AND "

    return query


def convert_qvalues_to_query(qvalues, questionnaire_id):
    questionsets = QuestionSet.objects.filter(questionnaire=questionnaire_id)
    
    questions = Question.objects.filter(questionset__in=questionsets)
    
    numbers = {}

    for q in questions:
        numbers[q.number] = q.slug
    query_parameters = {}
    query = ""  
    for k in qvalues:
        try:
            #print qvalues[k]
            #print numbers[k]
            
            if (qvalues[k]!=None and qvalues[k]!="" ):
                query_parameters[numbers[k]] = qvalues[k]
            query = query + " " + qvalues[k]
        except:
            pass
    
    return convert_dict_to_query(query_parameters)








    