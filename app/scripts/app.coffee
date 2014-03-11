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
  'RestangularProvider', 'endpoint',# 'FlashAlertService',
  (RestangularProvider, endpoint) ->
    RestangularProvider.setBaseUrl endpoint
    #TODO
    #RestangularProvider.setDefaultHttpFields
    #  cache: $angularCacheFactory 'httpCache'

    RestangularProvider.setMethodOverriders ['put']


    RestangularProvider.setResponseExtractor((response) ->
      newResponse = response

      if angular.isArray(response)
        angular.forEach newResponse, (value, key) ->
          newResponse[key].originalElement = angular.copy value
      else
        newResponse.originalElement = angular.copy response

      return newResponse
    )
]


# Initializations
app.run [
  '$rootScope', '$http', '$location', 'Restangular', '$localStorage',
  '$angularCacheFactory', 'FlashAlertService', 'AuthenticationService',
  ($rootScope, $http, $location, Restangular, $localStorage,
  $angularCacheFactory, FlashAlertService, AuthenticationService) ->

    # Formats
    $rootScope.formats =
      DATE: 'EEE, MM/dd/yyyy'
      MOMENT_DATE: 'ddd, L'

    # ngStorage
    $rootScope.$storage = $localStorage

    #TODO angular-cache
    $http.defaults.cache = false
    #httpCache = $angularCacheFactory 'httpCache'
    #$http.defaults.cache = httpCache
    #Restangular.setDefaultHttpFields cache:httpCache

    # FlashAlert
    $rootScope.flashAlert ?= {}
    FlashAlertService.setStorage $rootScope.flashAlert
    FlashAlertService.init()

    # Restangular (couldn't set up in .config())
    Restangular.setErrorInterceptor((response) ->
      FlashAlertService.error response.data.message
      return false
    )

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
            FlashAlertService.error "Please logout to move to the page"
            FlashAlertService.prepareRedirect()
            $location.path redirectPath
      else
        for path,redirectPath of needLoginRoutes
          if $location.path() is path
            FlashAlertService.error "Please login to move to the page"
            FlashAlertService.prepareRedirect()
            $location.path redirectPath

      FlashAlertService.reset()
]
