from copy import copy

from planmate.lib.resources import RootResource
from planmate.resources.user import UserModelResource,MyResource
from planmate.resources.plan import *


class ApiRoot(RootResource):
  def init_resources(self):
    plans = PlanModelResource(self.request)
    plan_attendants = PlanAttendantModelResource(self.request)
    plan_comments = PlanCommentModelResource(self.request)
    plan_schedules = PlanScheduleModelResource(self.request)
    plan_schedule_attendants = PlanScheduleAttendantModelResource(self.request)
    plan_schedules.add_model_resource(plan_schedule_attendants)
    plans.add_model_resources([plan_attendants, plan_comments, plan_schedules])

    _plans = copy(plans)
    self.add_model_resource(_plans)

    me = MyResource(self.request)
    _plans = copy(plans)
    me.add_model_resource(_plans)
    self.add_model_resource(me)

    users = UserModelResource(self.request)
    _plans = copy(plans)
    users.add_model_resource(_plans)
    self.add_model_resource(users)

"""
class AppRoot(RootResource):
  def init_resources(self):

    plans = ModelResource(self.request, name='plans', model=Plan)
    plan_attendants = ModelResource(self.request, name='attendants', model=PlanAttendant)
    plan_schedules = ModelResource(self.request, name='schedules', model=PlanSchedule)
    plan_comments = ModelResource(self.request, name='comments', model=PlanComment)
    plans.add_model_resources([plan_attendants, plan_schedules, plan_comments])

    #TODO deepcopy
    _plans = copy(plans)

    users = ModelResource(self.request, name='users', model=User)
    users.add_model_resource(_plans)
    self.add_model_resource(users)

    _plans = copy(plans)

    me = MyResource(self.request, name='me')
    
    #my_plans = ModelResource(self.request, name='plans', model=Plan)
    #my_plan_attendants = ModelResource(self.request, name='attendants', model=PlanAttendant)
    #my_plan_schedules = ModelResource(self.request, name='schedules', model=PlanSchedule)
    #my_plan_comments = ModelResource(self.request, name='comments', model=PlanComment)
    #my_plans.add_model_resources([my_plan_attendants, my_plan_schedules, my_plan_comments])

    me.add_model_resource(_plans, me)
    self.add_model_resource(me)

    _plans = copy(plans)
    self.add_model_resource(_plans)
"""
