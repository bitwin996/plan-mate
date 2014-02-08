'use strict'

app = angular.module('planMateApp')

app.config [
  '$routeSegmentProvider', '$routeProvider',
  ($routeSegmentProvider, $routeProvider) ->

    $routeSegmentProvider.options.autoLoadTemplates = true

    apiResolveFailed = [
      'FlashAlertService', (FlashAlertService) ->
        FlashAlertService.prepareRedirect()
        FlashAlertService.error 'Failed to get data from server.'
    ]

    $routeSegmentProvider
      .when('/', 'main')

      .when('/auth/login', 'login')

      .when('/users/:userId/plans', 'users-plans')
      .when('/mypage/plans',            'mypage-plans')
      .when('/mypage/plans/new',        'mypage-plans-new')

      .when('/plans/:planId',            'plans-show.info')
      .when('/plans/:planId/attendants', 'plans-show.attendants')
      .when('/plans/:planId/schedules',  'plans-show.schedules')
      .when('/plans/:planId/comments',   'plans-show.comments')


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
          plansResponse: [
            'Restangular',
            (Restangular) ->
              #Restangular.one('me').all('plans').getList()
              Restangular.one('me').getList('plans')
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
          apiResponse: [
            'Plan', '$routeParams',
            (Plan, $routeParams) ->
              request = Plan.get planId:$routeParams.planId
              request.$promise
          ]
        resolveFailed:
          apiResponse: apiResolveFailed

      .within()
        .segment 'info',
          templateUrl: 'views/plans/show/info.html'
          dependencies: ['planId']

        .segment 'attendants',
          templateUrl: 'views/plans/show/attendants.html'
          controller: 'PlansShowAttendantsCtrl'
          dependencies: ['planId']
          resolve:
            apiResponse: [
              'PlanAttendant', '$routeParams',
              (PlanAttendant, $routeParams) ->
                request = PlanAttendant.query planId:$routeParams.planId
                request.$promise
            ]
          resolveFailed:
            apiResponse: apiResolveFailed

        .segment 'comments',
          templateUrl: 'views/plans/show/comments.html'
          controller: 'PlansShowCommentsCtrl'
          dependencies: ['planId']
          resolve:
            apiResponse: [
              'PlanComment', '$routeParams',
              (PlanComment, $routeParams) ->
                request = PlanComment.query planId:$routeParams.planId
                request.$promise
            ]
          resolveFailed:
            apiResponse: apiResolveFailed

        .segment 'schedules',
          templateUrl: 'views/plans/show/schedules.html'
          controller: 'PlansShowSchedulesCtrl'
          dependencies: ['planId']
          resolve:
            schedulesResponse: [
              '$routeParams', 'Restangular',
              ($routeParams, Restangular) ->
                Restangular.one('plans', $routeParams.planId).getList('schedules')
            ]
            #resolveFailed:
            #  schedules: [
            #    'FlashAlertService',
            #    (FlashAlertService) ->
            #      FlashAlertService.prepareRedirect()
            #      FlashAlertService.error 'Failed to get schedules of the plan.'
            #  ]

      ###

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
      ###

    $routeProvider.otherwise redirectTo: '/'
]
