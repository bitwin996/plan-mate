'use strict'

angular.module('planMateApp')
  .controller 'MainCtrl', [
    '$scope', 'AuthenticationService', '$http', 'endpoint',
    ($scope, AuthenticationService, $http, endpoint) ->

      #TODO delete
      $scope.endpoint = endpoint
      $scope.debug = ->
        request = $http.get endpoint + '/auth/debug'

        request.success (response) =>
          console.log 'DEBUG SUCCESS', response

        request.error (response) ->
          console.log 'DEBUG ERROR', response


      $scope.updateAuth = ->
        AuthenticationService.update()
  ]
