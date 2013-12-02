'use strict'

describe 'Controller: PlansDetailCtrl', () ->

  # load the controller's module
  beforeEach module 'planMateApp'

  PlansDetailCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope = $rootScope.$new()
    PlansDetailCtrl = $controller 'PlansDetailCtrl', {
      $scope: scope
    }

  it 'should attach a list of awesomeThings to the scope', () ->
    expect(scope.awesomeThings.length).toBe 3
