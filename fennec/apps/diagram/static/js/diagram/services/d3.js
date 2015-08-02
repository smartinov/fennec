(function () {
  'use strict';

  angular.module('d3', [])
      .provider('d3Service', function() {
        function createScript($document, callback, success) {
          var scriptTag = $document.createElement('script');
          scriptTag.type = "text/javascript";
          scriptTag.async = true;
          scriptTag.src = 'http://d3js.org/d3.v3.min.js';
          scriptTag.onreadystatechange = function() {
            if (this.readyState == 'complete') {
              callback();
            }
          }
          scriptTag.onload = callback;
          $document.getElementsByTagName('body')[0].appendChild(scriptTag);
        }

        this.$get = ['$document','$q', '$window', '$rootScope',
          function($document, $q, $window, $rootScope) {
            var deferred = $q.defer();
            createScript($document[0], function(callback) {
              $rootScope.$apply(function() { deferred.resolve($window.d3) });
            })
            return deferred.promise;
          }];
      });

}());
