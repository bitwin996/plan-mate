'use strict'

describe 'Controller: PlansShowSchedulesCtrl', () ->

  # load the controller's module
  beforeEach module 'planMateApp'

  PlansShowSchedulesCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope = $rootScope.$new()
    PlansShowSchedulesCtrl = $controller 'PlansShowSchedulesCtrl', {
      $scope: scope
    }

  it 'should attach a list of awesomeThings to the scope', () ->
    expect(scope.awesomeThings.length).toBe 3
