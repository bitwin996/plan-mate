'use strict'

describe 'Controller: AuthLoginCompleteCtrl', () ->

  # load the controller's module
  beforeEach module 'planMateApp'

  AuthLoginCompleteCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope = $rootScope.$new()
    AuthLoginCompleteCtrl = $controller 'AuthLoginCompleteCtrl', {
      $scope: scope
    }

  it 'should attach a list of awesomeThings to the scope', () ->
    expect(scope.awesomeThings.length).toBe 3
