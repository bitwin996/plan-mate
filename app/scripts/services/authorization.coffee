'use strict'

angular.module('planMateApp')
  .service 'AuthorizationService', [
    '$http', '$q', 'endpoint', 'baseUrl',
    ($http, $q, endpoint, baseUrl) ->

      #TODO use localStorage to initialize this value
      @isLoggedIn = false

      # AngularJS will instantiate a singleton by calling "new" on this function
      @update = ->
        $http.get(endpoint + '/auth/status').
          success (response) =>
            @isLoggedIn = response.data.isLoggedIn

            #TODO save to localStorage

      return @
  ]
