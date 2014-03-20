'use strict'

angular.module('planMateApp')
  .factory 'Plan', [
    '$resource', '$filter', 'endpoint',
    ($resource, $filter, endpoint) ->
      $resource endpoint + '/plans/:planId', planId:'@id',
        query:
          method:'GET'
          isArray:false

        fix:
          method: 'PUT'
          transformRequest: (data, headersGetter) ->
            attrs = ['date']
            params = {}

            for attr in attrs
              params[attr] = data[attr]

            json = $filter('json') params
            return json

        cancelFixing:
          method: 'PUT'
          transformRequest: (data, headersGetter) ->
            params = {'date':null}

            json = $filter('json') params
            return json

  ]

