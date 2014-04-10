# -*- coding: utf-8 -*-

# Copyright (C) 2014 Luís A. Bastião Silva and Universidade de Aveiro
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



from __future__ import absolute_import

from celery import shared_task
import time

from population_characteristics.aggregator import *

@shared_task
def aggregation(fingerprint_id, values):
    # Operations
    print "start aggregation"
    try:
        ac = AggregationPopulationCharacteristics(values,fingerprint_id, None)
        print "created object"
        new_values = ac.run()
    except:
        print "Exception!!!!!!!"
        import traceback
        traceback.print_exc()
        
    print "ends aggregation"
    return fingerprint_id

