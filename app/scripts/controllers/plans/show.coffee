'use strict'

angular.module('planMateApp')
  .controller 'PlansShowCtrl', [
    '$scope', '$routeParams', '$http', 'endpoint', 'FlashAlertService',
    ($scope, $routeParams, $http, endpoint, FlashAlertService) ->

      request = $http.get endpoint + '/plans/' + $routeParams.planId

      request.success (response) ->
        $scope.plan = response

      request.error (response) ->
        FlashAlertService.error 'Fail to get server data'
  ]
