'use strict'

angular.module('planMateApp')
  .factory 'PlanSchedule', [
    '$resource', 'endpoint',
    ($resource, endpoint) ->
      $resource endpoint + '/plans/:planId/schedules/:planScheduleId',
          planScheduleId:'@id'
          planId:'@plan_id'
        ,
          query:
            method:'GET'
            isArray:false
  ]
