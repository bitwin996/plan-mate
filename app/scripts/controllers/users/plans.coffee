'use strict'

angular.module('planMateApp')
  .controller 'UsersPlansCtrl', [
    '$scope', '$routeParams', '$http', 'endpoint', 'FlashAlertService',
    ($scope, $routeParams, $http, endpoint, FlashAlertService) ->

      request = $http.get endpoint + '/me/plans'

      request.success (response) ->
        $scope.plans = response

      request.error (response) ->
        FlashAlertService.update "Couldn't connect the remote server", 'danger'

  ]
