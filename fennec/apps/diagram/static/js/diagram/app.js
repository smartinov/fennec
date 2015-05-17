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
    angular.module('myApp', ['myApp.services', 'myApp.controllers', 'myApp.directives']);

    // setup dependency injection
    angular.module('d3', []);
    angular.module('myApp.services', []);
    angular.module('myApp.controllers', ["xeditable"]);
    angular.module('myApp.directives', ['d3']);

}());