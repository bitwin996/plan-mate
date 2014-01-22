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
  'restangular'
])


app.constant('baseUrl', "%BASE_URL%")
app.constant('endpoint', "%BASE_URL%/api")


# CORS
app.config [
  '$httpProvider',
  ($httpProvider) ->
    $httpProvider.defaults.withCredentials = true
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
    #$httpProvider.defaults.headers.common['X-HTTP-Method-Override'] = 'Access-Control-Allow-Headers'
    #delete $httpProvider.defaults.headers.common['X-Requested-With']
]


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


# Restangular
app.config [
  'RestangularProvider', 'endpoint',
  (RestangularProvider, endpoint) ->
    RestangularProvider.setBaseUrl endpoint
    #RestangularProvider.setDefaultHttpFields
    #  cache: $angularCacheFactory 'httpCache'

    RestangularProvider.setMethodOverriders ['put']
]


# Initializations
app.run [
  '$rootScope', '$http', '$location', 'Restangular', '$localStorage',
  '$angularCacheFactory', 'FlashAlertService', 'AuthenticationService',
  ($rootScope, $http, $location, Restangular, $localStorage,
  $angularCacheFactory, FlashAlertService, AuthenticationService) ->

    # ngStorage
    $rootScope.$storage = $localStorage

    #TODO angular-cache
    #httpCache = $angularCacheFactory 'httpCache'
    #$http.defaults.cache = httpCache
    #Restangular.setDefaultHttpFields cache:httpCache

    # FlashAlert
    $rootScope.flashAlert ?= {}
    FlashAlertService.setStorage $rootScope.flashAlert
    FlashAlertService.init()

    # Authentication
    $rootScope.$storage.authentication ?= {}
    AuthenticationService.setStorage $rootScope.$storage.authentication

    # Authentication route restrictions
    needLoginRoutes = {}
    needLogoutRoutes =
      '/auth/login': '/'

    $rootScope.$on '$routeChangeStart', (event, next, current) ->
      if AuthenticationService.isLoggedIn()
        for path,redirectPath of needLogoutRoutes
          if $location.path() is path
            FlashAlertService.update "Please logout to move to the page", 'danger'
            FlashAlertService.prepareRedirect()
            $location.path redirectPath
      else
        for path,redirectPath of needLoginRoutes
          if $location.path() is path
            FlashAlertService.update "Please login to move to the page", 'danger'
            FlashAlertService.prepareRedirect()
            $location.path redirectPath

      FlashAlertService.reset()
]
