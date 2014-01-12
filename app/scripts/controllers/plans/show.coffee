'use strict'

angular.module('planMateApp')
  .controller 'PlansShowCtrl', [
    '$scope', '$routeParams', 'Plan', 'FlashAlertService',
    ($scope, $routeParams, Plan, FlashAlertService) ->
      # ModelCore
      $scope.plan = new Plan
      $scope.plan.$get($routeParams.planId).
        error ->
          FlashAlertService.prepareRedirect()
          FlashAlertService.error 'Fail to get the Plan data.'
          history.back()

      ###
    '$scope', '$routeParams', '$http', 'endpoint', 'FlashAlertService', 'Plan',
    ($scope, $routeParams, $http, endpoint, FlashAlertService, Plan) ->
      request = $http.get endpoint + '/plans/' + $routeParams.planId

      request.success (response) ->
        $scope.plan = response

      request.error (response) ->
        FlashAlertService.prepareRedirect()
        FlashAlertService.error 'Fail to get the Plan data.'
        history.back()

      $scope.attend = ->
        request = $http.post endpoint + '/plans/' + $routeParams.planId + '/attend'
        request.success (response) ->
          FlashAlertService.success 'You applied attending this plan.'
          $scope.plan = response

        request.error (response) ->
          FlashAlertService.error 'Fail to apply attending.'
      ###

  ]
