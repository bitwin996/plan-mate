'use strict'

angular.module('planMateApp')
  .service 'AuthenticationService', [
    '$http', 'endpoint', 'FlashAlertService',
    ($http, endpoint, FlashAlertService) ->
      @storage = {}

      @setStorage = (storage) ->
        unless storage instanceof Object
          throw 'Passed storage should be an object.'
        @oldStorage = @storage
        @storage = storage

      @update = ->
        request = $http.get endpoint + '/auth/status'

        request.success (response) =>
          FlashAlertService.success 'Success to get login status'
          angular.extend @storage, response

        request.error (response) ->
          FlashAlertService.error 'Fail to get login status'

      @logout = (callback) ->
        request = $http.get endpoint + '/auth/logout'

        request.success (response) =>
          @storage = {}
          callback()

        request.error (response) ->
          FlashAlertService.error 'Fail to logout'

      @isLoggedIn = ->
        @storage.is_logged_in

      @getUserId = ->
        @storage.user_id

      return @
  ]
