'use strict'

angular.module('planMateApp')
  .controller 'UsersPlansNewCtrl', [
    '$scope', '$http', '$location', '$rootScope', 'endpoint', 'FlashAlertService',
    ($scope, $http, $location, $rootScope, endpoint, FlashAlertService) ->

      $scope.submit = (plan) ->
        request = $http.post endpoint + '/me/plans', plan
        #request = $http.get endpoint + '/me/plans-new', plan

        request.success (response) ->
          $rootScope.$storage['plans-'+response.id] = response

          FlashAlertService.update "Registered a new plan", 'success'
          $location.path '/plans/' + response.id

        request.error (response) ->
          FlashAlertService.error "Failed to register a new plan"

  ]
