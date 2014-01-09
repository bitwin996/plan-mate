'use strict'

angular.module('planMateApp')
  .service 'AuthenticationService', [
    '$http', '$rootScope', 'endpoint', 'FlashAlert',
    ($http, $rootScope, endpoint, FlashAlert) ->

      # AngularJS will instantiate a singleton by calling "new" on this function
      @update = ->
        request = $http.get endpoint + '/auth/status'

        request.success (response) =>
          $rootScope.$storage.authentication.isLoggedIn = response.data.isLoggedIn
        request.error (response) ->
          FlashAlert.update 'Fail to get login status', 'danger'

      return @
  ]
