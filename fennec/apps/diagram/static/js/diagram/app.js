/*#######################################################################

 Sandor Klebecko
 Sandor Klebecko

 Normally like to break AngularJS apps into the following folder structure
 at a minimum:

 /app
 /controllers
 /directives
 /services
 /partials
 /views

 #######################################################################*/

(function () {
    'use strict';

    // create the angular app
    var app = angular.module('myApp', ['myApp.services', 'myApp.controllers', 'myApp.directives']);

    // setup dependency injection
    angular.module('d3', []);
    angular.module('myApp.services', []);
    angular.module('myApp.controllers', ["xeditable",'ui.bootstrap','ui-notification']);
    angular.module('myApp.directives', ['d3']);

    app.config(['$httpProvider', '$interpolateProvider', function ($httpProvider, $interpolateProvider) {
        /* for compatibility with django template engine */
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        //Interpolate angular start and end symbols
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
    }]);

    app.config(['$logProvider', function($logProvider){
        $logProvider.debugEnabled(true);
    }]);


}());