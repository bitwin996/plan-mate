'use strict'

angular.module('planMateApp')
  .factory 'Plan', [
    '$resource', 'endpoint',
    ($resource, endpoint) ->
      $resource endpoint + '/plans/:planId', planId:'@id'
  ]

