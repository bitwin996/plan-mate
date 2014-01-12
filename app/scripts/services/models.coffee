'use strict'

app = angular.module('planMateApp')

app.factory 'Plan', [
  'ModelCore', '$http', 'endpoint',
  (ModelCore, $http, endpoint) ->
    ModelCore.instance
      $type: 'Plan'
      $pkField: 'id'
      $settings:
        urls:
          #base: endpoint + '/plans/:id'
          base: endpoint + '/plans-list'
        dataField:
          one: 'content'
          many: 'items'

      $attend: ->
        #console.log @$call, @$toObject()
        url = endpoint + '/plans/' + @id + '/attend'
        params = @
        @$call
          url: url 'attend', params
          method: 'POST'
          data: @$toObject()

        #console.log moment().add('days', 10).format()
        console.log 'DATA', @
        $http.post endpoint + '/plans/' + @id + '/attend', @
]
