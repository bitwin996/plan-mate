'use strict'

angular.module('planMateApp')
  .factory 'PlanComment', [
    '$resource', 'endpoint',
    ($resource, endpoint) ->
      $resource endpoint + '/plans/:planId/comments/:planCommentId',
          planCommentId:'@id'
          planId:'@plan_id'
        ,
          query:
            method:'GET'
            isArray:false
  ]
