'use strict'

describe 'Service: planComment', () ->

  # load the service's module
  beforeEach module 'planMateApp'

  # instantiate service
  planComment = {}
  beforeEach inject (_planComment_) ->
    planComment = _planComment_

  it 'should do something', () ->
    expect(!!planComment).toBe true
