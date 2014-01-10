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
          FlashAlertService.update 'Success to get login status', 'info'
          @storage.isLoggedIn = response.isLoggedIn

        request.error (response) ->
          FlashAlertService.update 'Fail to get login status', 'danger'

      @logout = (callback) ->
        request = $http.get endpoint + '/auth/logout'

        request.success (response) =>
          @storage.isLoggedIn = false
          callback()

        request.error (response) ->
          FlashAlertService.update 'Fail to logout', 'danger'

      return @
  ]
