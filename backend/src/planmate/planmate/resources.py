from planmate.lib.helpers import AuthenticationHelper
from planmate.lib.resources import *
from planmate.models.user import User
from planmate.models.plan import *


class Root(object):
  def __init__(self, request):
    self.request = request


class AppRoot(RootResource):
  def init_resources(self):
    def set_user_key(entity):
      user_key = AuthenticationHelper.instance().get_user_key()
      entity.user_key = user_key

    users = ModelResource(self.request, name='users', model=User)
    plans = ModelResource(self.request, name='plans', model=Plan, pre_put_hook=set_user_key)
    plan_attendants = ModelResource(self.request, name='attendants', model=PlanAttendant)
    plan_schedules = ModelResource(self.request, name='schedules', model=PlanSchedule)
    plan_comments = ModelResource(self.request, name='comments', model=PlanComment)
    plans.add_model_resources([plan_attendants, plan_schedules, plan_comments])
    users.add_model_resource(plans)
    self.add_model_resource(users)

    me = MyResource(self.request, name='me')
    my_plans = ModelResource(self.request, name='plans', model=Plan)
    my_plan_attendants = ModelResource(self.request, name='attendants', model=PlanAttendant)
    my_plan_schedules = ModelResource(self.request, name='schedules', model=PlanSchedule)
    my_plan_comments = ModelResource(self.request, name='comments', model=PlanComment)
    my_plans.add_model_resources([my_plan_attendants, my_plan_schedules, my_plan_comments])
    me.add_model_resource(my_plans, me)
    self.add_model_resource(me)


class MyResource(BaseEntityResource):
  def __init__(self, *args, **kwds):
    super(MyResource, self).__init__(args, kwds)
    self.__name__ = kwds.get('name')

    AuthenticationHelper.instance().set_session(self.request.session)
    key = AuthenticationHelper.instance().get_user_key()
    self.key = key

  def __getitem__(self, name):
    model_resource = self.get_model_resource(name)
    if not model_resource: raise KeyError
    return model_resource
