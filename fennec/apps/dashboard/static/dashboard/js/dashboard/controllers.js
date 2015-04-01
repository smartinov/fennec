var projectsRoot = '/api/projects/';
var app = angular.module('fennec.dashboard', ['mgcrea.ngStrap', 'ngAnimate', 'ngResource', 'ngCookies']);


app.factory('Projects', ['$resource', function($resource){
    return $resource("/api/projects/", {'id': '@id'});
}]);

app.config(['$httpProvider', '$interpolateProvider', '$resourceProvider', function ($httpProvider, $interpolateProvider, $resourceProvider) {
     /* for compatibility with django teplate engine */
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    //** django urls loves trailling slashes which angularjs removes by default.
    //$resourceProvider.defaults.stripTrailingSlashes = false;
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');

}]);
app.config(function ($alertProvider) {
    angular.extend($alertProvider.defaults, {
        animation: 'am-fade-and-slide-top',
        placement: 'top-right',
        duration: 3,
        container: '#alert-container'
    });
});

app.controller("ProjectsController",
    function ($scope, $http, $alert, Projects) {
        $scope.UserFullName = 'Nikola Latinovic';
        $scope.criteria = {parameter:'All'};
        $scope.projects = Projects.query();
        $scope.AddProject = {};
        $scope.add_new = false;

        $scope.add_new_project = function () {
            var project = {
                "name": $scope.AddProject.Name,
                "created_by":"http://127.0.0.1:8000/api/users/1/"
            }
            var data = angular.toJson(project);
            $http.post(projectsRoot, data)
                .success(function (data, status) {
                    $scope.AddProject = {};
                    $scope.projects = Projects.query();
                }).error(function (data, status) {

                });
        };

        $scope.toogle_add_project = function(value){
            $scope.add_new = value;
            $scope.AddProject = {};
            $("#sidebar-wrapper-rigth").toggleClass("toggled");
        }

        $scope.toggleSidebar = function(item){
            $scope.add_new = false;
            if($scope.selectedProject != undefined){
                if(item != $scope.selectedProject){
                    $scope.selectedProject = item;
                }else{
                    $("#sidebar-wrapper-rigth").toggleClass("toggled");
                }
            }else{
                $scope.selectedProject = item;
                $("#sidebar-wrapper-rigth").toggleClass("toggled");
            }
            //Reset Selected project if there is no sidebar
            if(!$("#sidebar-wrapper-rigth").hasClass('toggled'))
                $scope.selectedProject = undefined;
        };

        $scope.criteriaMatch = function( criteria ) {
    	    return function( item ) {
    		    switch (criteria.parameter){
    			    case 'All':
    				    return true;
    			    case 'Mine':
    				    return item.created_by == 1;
    			    case 'Shared':
    				    return item.members.length > 0;
    			    case 'InProgress':
     				    return item.percentage_complete != 100;
    			    case 'Completed':
    				    return item.percentage_complete == 100;
    		    }
    	    };
  	    };

        $scope.filterBy = function(filter_parameter){
    	    $scope.criteria = {parameter: filter_parameter};
        };

        $scope.criteriaMatchLength = function(criteria){
            switch (criteria){
    			    case 'Mine':
                        return $.grep($scope.projects, function(item){return item.created_by == 1}).length;
    			    case 'Shared':
                        //return $.grep($scope.projects, function(item){return item.members.length > 0}).length;
                    return 0;
    			    case 'InProgress':
                        return $.grep($scope.projects, function(item){return item.percentage_complete != 100}).length;
    			    case 'Completed':
    				    return $.grep($scope.projects, function(item){return item.percentage_complete == 100}).length;
    		}
        }
    });

