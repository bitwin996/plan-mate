'use strict'

app = angular.module('planMateApp', [
  'ngCookies'
  'ngResource'
  'ngSanitize'
  'ngRoute'
  'route-segment'
  'view-segment'
  'ui.bootstrap'
  'angularMoment'
  'ModelCore'
  'ngStorage'
])


app.constant('baseUrl', "%BASE_URL%")
app.constant('endpoint', "%BASE_URL%/api")


# Initializations
app.run([
  '$rootScope', '$localStorage', 'FlashAlertService', 'AuthenticationService',
  ($rootScope, $localStorage, FlashAlertService, AuthenticationService) ->
    # ngStorage
    $rootScope.$storage = $localStorage

    # FlashAlert
    $rootScope.flashAlert ?= {}
    FlashAlertService.setStorage $rootScope.flashAlert
    FlashAlertService.init()

    # Authentication
    $rootScope.$storage.authentication ?= {}
    AuthenticationService.setStorage $rootScope.$storage.authentication
])


###
app.config([
  '$httpProvider',
  ($httpProvider) ->
    # for CORS
    $httpProvider.defaults.useXDomain = true
    delete $httpProvider.defaults.headers.common['X-Requested-With']
])
###
