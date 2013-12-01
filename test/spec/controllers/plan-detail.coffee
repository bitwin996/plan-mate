'use strict'

describe 'Controller: PlanDetailCtrl', () ->

  # load the controller's module
  beforeEach module 'planMateApp'

  PlanDetailCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope = $rootScope.$new()
    PlanDetailCtrl = $controller 'PlanDetailCtrl', {
      $scope: scope
    }

  it 'should attach a list of awesomeThings to the scope', () ->
    expect(scope.awesomeThings.length).toBe 3
