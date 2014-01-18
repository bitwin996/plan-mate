'use strict'

angular.module('planMateApp')
  .controller 'UsersPlansNewCtrl', [
    '$scope', '$http', '$location', '$rootScope', 'endpoint', 'Restangular', 'FlashAlertService',
    ($scope, $http, $location, $rootScope, endpoint, Restangular, FlashAlertService) ->

      $scope.submit = (plan) ->
        Restangular.one('me').all('plans').post plan

      ###
      $scope.submit = (plan) ->
        request = $http.post endpoint + '/me/plans', plan
        #request = $http.get endpoint + '/me/plans-new', plan

        request.success (response) ->
          $rootScope.$storage['plans-'+response.id] = response

          FlashAlertService.success "Registered a new plan"
          $location.path '/plans/' + response.id

        request.error (response) ->
          FlashAlertService.error "Failed to register a new plan"
      ###
  ]
