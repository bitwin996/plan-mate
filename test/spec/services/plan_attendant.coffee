'use strict'

describe 'Service: planAttendant', () ->

  # load the service's module
  beforeEach module 'planMateApp'

  # instantiate service
  planAttendant = {}
  beforeEach inject (_planAttendant_) ->
    planAttendant = _planAttendant_

  it 'should do something', () ->
    expect(!!planAttendant).toBe true
