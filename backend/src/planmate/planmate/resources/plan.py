from planmate.lib.resources import ModelResource,EntityResource
from planmate.resources.plan import *

from planmate.models.user import User
from planmate.models.plan import *


class PlanEntityResource(EntityResource): pass
class PlanAttendantEntityResource(EntityResource): pass
class PlanCommentEntityResource(EntityResource): pass
class PlanScheduleEntityResource(EntityResource): pass
class PlanScheduleAttendantEntityResource(EntityResource): pass

class PlanModelResource(ModelResource):
  def __init__(self, *args, **kwds):
    _kwds = {
      'model': Plan,
      'name': 'plans',
      'entity_resource': PlanEntityResource
      }
    _kwds.update(kwds)
    super(PlanModelResource, self).__init__(*args, **_kwds)

class PlanAttendantModelResource(ModelResource):
  def __init__(self, *args, **kwds):
    _kwds = {
      'model': PlanAttendant,
      'name': 'attendants',
      'entity_resource': PlanAttendantEntityResource
      }
    _kwds.update(kwds)
    super(PlanAttendantModelResource, self).__init__(*args, **_kwds)

class PlanCommentModelResource(ModelResource):
  def __init__(self, *args, **kwds):
    _kwds = {
      'model': PlanComment,
      'name': 'comments',
      'entity_resource': PlanCommentEntityResource
      }
    _kwds.update(kwds)
    super(PlanCommentModelResource, self).__init__(*args, **_kwds)

class PlanScheduleModelResource(ModelResource):
  def __init__(self, *args, **kwds):
    _kwds = {
      'model': PlanSchedule,
      'name': 'schedules',
      'entity_resource': PlanScheduleEntityResource
      }
    _kwds.update(kwds)
    super(PlanScheduleModelResource, self).__init__(*args, **_kwds)

class PlanScheduleAttendantModelResource(ModelResource):
  def __init__(self, *args, **kwds):
    _kwds = {
      'model': PlanScheduleAttendant,
      'name': 'attendants',
      'entity_resource': PlanScheduleAttendantEntityResource
      }
    _kwds.update(kwds)
    super(PlanScheduleAttendantModelResource, self).__init__(*args, **_kwds)

