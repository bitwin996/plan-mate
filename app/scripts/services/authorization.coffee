'use strict'

angular.module('planMateApp')
  .service 'AuthorizationService', [
    '$http', '$q', 'endpoint', 'baseUrl',
    ($http, $q, endpoint, baseUrl) ->

      # AngularJS will instantiate a singleton by calling "new" on this function
      @get = ->
        console.log baseUrl, endpoint
        deferred = $q.defer()
        request = $http.get endpoint + '/auth/status'
        request.success = (data) ->
          console.log data
          deferred.resolved data
        deferred.promise

      #TODO use localStorage to initialize this value
      @isLoggedIn = false

  ]
