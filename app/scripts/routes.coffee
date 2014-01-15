'use strict'

app = angular.module('planMateApp')

app.config [
  '$routeSegmentProvider', '$routeProvider',
  ($routeSegmentProvider, $routeProvider) ->

    $routeSegmentProvider.options.autoLoadTemplates = true

    $routeSegmentProvider
      .when('/', 'main')

      .when('/auth/login', 'login')

      .when('/users/:userId/plans', 'users-plans')
      .when('/mypage/plans',            'mypage-plans')
      .when('/mypage/plans/new',        'mypage-plans-new')

      .when('/plans/:planId',            'plans-show')

      #.when('/plans/:planId',            'detail.info')
      .when('/plans/:planId/scheduling', 'detail.scheduling')
      .when('/plans/:planId/comments',   'detail.comments')
      .when('/plans/:planId/attendants', 'detail.attendants')
      .when('/plans/:planId/scheduling', 'detail.scheduling')

      .segment 'main',
        templateUrl: 'views/main.html'
        controller: 'MainCtrl'

      .segment 'login',
        templateUrl: 'views/auth/login.html'
        controller: 'AuthCtrl'

      .segment 'mypage-plans',
        templateUrl: 'views/users/plans.html'
        controller: 'UsersPlansCtrl'
        resolve:
          plans: ['Restangular', (Restangular) ->
            Restangular.one('me').all('plans').getList()
          ]

      .segment 'users-plans',
        templateUrl: 'views/users/plans.html'
        controller: 'UsersPlansCtrl'
        dependencies: ['userId']

      .segment 'mypage-plans-new',
        templateUrl: 'views/plans/new.html'
        controller: 'UsersPlansNewCtrl'

      .segment 'plans-show',
        templateUrl: 'views/plans/show.html'
        controller: 'PlansShowCtrl'
        resolve:
          plan: [
            '$routeParams', 'Restangular', 'FlashAlertService',
            ($routeParams, Restangular, FlashAlertService) ->
              Restangular.one('plans', $routeParams.planId).get().then(
                  (plan) -> plan
                ,
                  ->
                    FlashAlertService.prepareRedirect()
                    FlashAlertService.error 'There\'s not the plan data on the server.'
                    history.back()
              )
          ]

      .segment 'detail',
        templateUrl: 'views/plans/detail.html'
        controller: 'PlansDetailCtrl'

      .within()
        .segment 'info',
          templateUrl: 'views/plans/detail/info.html'
          dependencies: ['planId']
        .segment 'scheduling',
          templateUrl: 'views/plans/detail/scheduling.html'
          dependencies: ['planId']
        .segment 'comments',
          templateUrl: 'views/plans/detail/comments.html'
          dependencies: ['planId']
        .segment 'attendants',
          templateUrl: 'views/plans/detail/attendants.html'
          dependencies: ['planId']

    $routeProvider.otherwise redirectTo: '/'
]
