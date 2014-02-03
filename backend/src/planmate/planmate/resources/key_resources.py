from copy import copy

from planmate.lib.key_resources import *
from planmate.resources.key_resources import *

from planmate.models.user import *
from planmate.models.plan import *

from planmate.lib.helpers import AuthenticationHelper


class UserKeyResource(KeyResource): pass
class PlanKeyResource(KeyResource): pass
class PlanAttendantKeyResource(KeyResource): pass
class PlanCommentKeyResource(KeyResource): pass
class PlanScheduleKeyResource(KeyResource): pass
class PlanScheduleAttendantKeyResource(KeyResource): pass


class UserModelResource(ModelResource):
  def __init__(self, **options):
    _options = {
      'model': User,
      'name': 'users',
      'key_resource': UserKeyResource}
    _options.update(options)
    super(UserModelResource, self).__init__(**_options)

class CurrentUserKeyResource(RootKeyResource):
  def __init__(self, **options):
    _options = {
      'model': User,
      'name': 'me'}
    _options.update(options)
    super(CurrentUserKeyResource, self).__init__(**_options)

  def set_parent(self, parent):
    self.__parent__ = parent
    self.request = parent.request

    user_key = AuthenticationHelper.instance().get_user_key()
    self.key = user_key

class PlanModelResource(ModelResource):
  def __init__(self, **options):
    _options = {
      'model': Plan,
      'name': 'plans',
      'key_resource': PlanKeyResource
      }
    _options.update(options)
    super(PlanModelResource, self).__init__(**_options)

class PlanAttendantModelResource(ModelResource):
  def __init__(self, **options):
    _options = {
      'model': PlanAttendant,
      'name': 'attendants',
      'key_resource': PlanAttendantKeyResource
      }
    _options.update(options)
    super(PlanAttendantModelResource, self).__init__(**_options)

class PlanCommentModelResource(ModelResource):
  def __init__(self, **options):
    _options = {
      'model': PlanComment,
      'name': 'comments',
      'key_resource': PlanCommentKeyResource
      }
    _options.update(options)
    super(PlanCommentModelResource, self).__init__(**_options)

class PlanScheduleModelResource(ModelResource):
  def __init__(self, **options):
    _options = {
      'model': PlanSchedule,
      'name': 'schedules',
      'key_resource': PlanScheduleKeyResource
      }
    _options.update(options)
    super(PlanScheduleModelResource, self).__init__(**_options)

class PlanScheduleAttendantModelResource(ModelResource):
  def __init__(self, **options):
    _options = {
      'model': PlanScheduleAttendant,
      'name': 'attendants',
      'key_resource': PlanScheduleAttendantKeyResource
      }
    _options.update(options)
    super(PlanScheduleAttendantModelResource, self).__init__(**_options)



class KeyRoot(RootResource):
  def _init_resources(self):
    plans = PlanModelResource()
    plan_attendants = PlanAttendantModelResource()
    plan_comments = PlanCommentModelResource()
    plan_schedules = PlanScheduleModelResource()
    plan_schedule_attendants = PlanScheduleAttendantModelResource()
    plan_schedules.add_model_resource(plan_schedule_attendants)

    plans.add_model_resources([plan_attendants, plan_comments, plan_schedules])

    _plans = copy(plans)
    self.add_resource(_plans)

    me = CurrentUserKeyResource()
    _plans = copy(plans)
    me.add_model_resource(_plans)
    self.add_resource(me)

    users = UserModelResource()
    _plans = copy(plans)
    users.add_model_resource(_plans)
    self.add_resource(users)

