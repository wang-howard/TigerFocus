"""
Commonly used functions in code to avoid repitition
"""
import random
from datetime import datetime, timezone
from .. import db
from ..models import User, Course, Assignment

def generate_course_id():
    course_id = str(random.randint(1000000, 9999999))
    while True:
        query = Course.query.get(course_id)
        if query == None:
            break
        else:
            course_id = str(random.randint(1000000, 9999999))
    return course_id

def generate_assignment_id():
    assignment_id = str(random.randint(1000000, 9999999))
    while True:
        query = Assignment.query.get(assignment_id)
        if query == None:
            break
        else:
            assignment_id = str(random.randint(1000000, 9999999))
    return assignment_id

def get_utc():
    return timezone.now(timezone.utc)