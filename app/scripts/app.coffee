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
  '$rootScope', '$localStorage', '$location', 'FlashAlertService', 'AuthenticationService',
  ($rootScope, $localStorage, $location, FlashAlertService, AuthenticationService) ->
    # ngStorage
    $rootScope.$storage = $localStorage

    # FlashAlert
    $rootScope.flashAlert ?= {}
    FlashAlertService.setStorage $rootScope.flashAlert
    FlashAlertService.init()

    # Authentication
    $rootScope.$storage.authentication ?= {}
    AuthenticationService.setStorage $rootScope.$storage.authentication

    # AuthN route restrictions
    needLoginRoutes = {}
    needLogoutRoutes =
      '/auth/login': '/'

    $rootScope.$on '$routeChangeStart', (event, next, current) ->
      if AuthenticationService.isLoggedIn()
        for path,redirectPath of needLogoutRoutes
          if $location.path() is path
            FlashAlertService.update "Please logout to move to the page", 'danger'
            FlashAlertService.setRedirect()
            $location.path redirectPath
      else
        for path,redirectPath of needLoginRoutes
          if $location.path() is path
            FlashAlertService.update "Please login to move to the page", 'danger'
            FlashAlertService.setRedirect()
            $location.path redirectPath

      FlashAlertService.reset()
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
