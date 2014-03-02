'use strict'

describe 'Controller: PlansShowSchedulesShowCtrl', () ->

  # load the controller's module
  beforeEach module 'planMateApp'

  PlansShowSchedulesShowCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope = $rootScope.$new()
    PlansShowSchedulesShowCtrl = $controller 'PlansShowSchedulesShowCtrl', {
      $scope: scope
    }

  it 'should attach a list of awesomeThings to the scope', () ->
    expect(scope.awesomeThings.length).toBe 3
