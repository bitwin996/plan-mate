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
        console.log 'UPDATE'

        request = $http.get endpoint + '/auth/status'

        request.success (response) =>
          console.log 'AUTH UPDATE', response
          #FlashAlertService.success 'Success to get login status'
          for k,v of @storage
            delete @storage[k]
          angular.extend @storage, response

        request.error (response) ->
          console.log 'AUTH UPDATE', response
          #FlashAlertService.error 'Fail to get login status'

      @logout = (callback) ->
        console.log 'LOGOUT'

        request = $http.get endpoint + '/auth/logout'

        request.success (response) =>
          console.log 'LOGOUT SUCCESS', response
          for k,v of @storage
            delete @storage[k]
          callback()

        request.error (response) ->
          FlashAlertService.error 'Fail to log out.'

      @isLoggedIn = ->
        @storage.is_logged_in

      @getUserId = ->
        @storage.user_id

      return @
  ]
