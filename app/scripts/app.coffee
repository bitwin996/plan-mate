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
  'ngStorage'
  'jmdobry.angular-cache'
  'ModelCore'
])


app.constant('baseUrl', "%BASE_URL%")
app.constant('endpoint', "%BASE_URL%/api")

###
# CORS
app.config [
  '$httpProvider',
  ($httpProvider) ->
    $httpProvider.defaults.useXDomain = true
    delete $httpProvider.defaults.headers.common['X-Requested-With']
]
###

# Cache
app.config [
  '$angularCacheFactoryProvider',
  ($angularCacheFactoryProvider) ->
    $angularCacheFactoryProvider.setCacheDefaults
      maxAge: 900000
      cacheFlushInterval: 6000000
      deleteOnExpire: 'aggressive'
      storageMode: 'localStorage'
]

# Initializations
app.run [
  '$rootScope', '$localStorage', '$location', '$angularCacheFactory', '$http',
  'FlashAlertService', 'AuthenticationService',
  ($rootScope, $localStorage, $location, $angularCacheFactory, $http,
  FlashAlertService, AuthenticationService) ->

    # ngStorage
    $rootScope.$storage = $localStorage

    # angular-cache
    $http.defaults.cache = $angularCacheFactory 'httpCache'

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
            FlashAlertService.prepareRedirect()
            $location.path redirectPath

      FlashAlertService.reset()
]
