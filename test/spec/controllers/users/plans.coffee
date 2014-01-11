'use strict'

describe 'Controller: UsersPlansCtrl', () ->

  # load the controller's module
  beforeEach module 'planMateApp'

  UsersPlansCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope = $rootScope.$new()
    UsersPlansCtrl = $controller 'UsersPlansCtrl', {
      $scope: scope
    }

  it 'should attach a list of awesomeThings to the scope', () ->
    expect(scope.awesomeThings.length).toBe 3
