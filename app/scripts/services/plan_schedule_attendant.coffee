'use strict'

angular.module('planMateApp')
  .factory 'PlanScheduleAttendant', [
    '$resource', 'endpoint',
    ($resource, endpoint) ->
      $resource endpoint + '/plans/:planId/schedules/:planScheduleId/attendants/:planScheduleAttendantId',
          planScheduleAttendantId:'@id'
          planScheduleId:'@plan_schedule_id'
          planId:'@plan_id'
        ,
          query:
            method:'GET'
            isArray:false
  ]
