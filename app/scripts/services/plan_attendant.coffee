'use strict'

angular.module('planMateApp')
  .factory 'PlanAttendant', [
    '$resource', 'endpoint',
    ($resource, endpoint) ->
      $resource endpoint + '/plans/:planId/attendants/:planAttendantId',
          planAttendantId:'@id'
          planId:'@plan_id'
        ,
          query:
            method:'GET'
            isArray:false
  ]

