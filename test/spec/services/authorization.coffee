'use strict'

describe 'Service: Authorization', () ->

  # load the service's module
  beforeEach module 'planMateApp'

  # instantiate service
  Authorization = {}
  beforeEach inject (_Authorization_) ->
    Authorization = _Authorization_

  it 'should do something', () ->
    expect(!!Authorization).toBe true
