var projectsRoot = '/api/projects/';
var usersRoot = '/api/users/';
var notification_popup_template = '../';
var app = angular.module('fennec.dashboard', ['mgcrea.ngStrap', 'ngAnimate','ui-notification', 'ngResource', 'ngSanitize']);


app.factory('Project', function($resource){
    return $resource('/api/projects/:id', {'id':'@id'},
        {
            'update':{method:'PUT'}
        }
    );
});



app.config(['$httpProvider', '$interpolateProvider', function ($httpProvider, $interpolateProvider) {
     /* for compatibility with django teplate engine */
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    //Interpolate angular start and end symbols
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

}]);

app.controller("ProjectsController",
    function ($scope, $http, Notification, Project) {
        $scope.UserFullName = 'Nikola Latinovic';
        $scope.criteria = {parameter:'All'};
        $scope.add_project = {};
        $scope.add_new = false;

        //Projects manipulation operations//////////////////////////////////////////////////
        //Method will be called on ng-init of controller
        $scope.load_projects = function(){
            $scope.projects = Project.query({'created_by':'1'},
                function(){},

                function(){
                    //function called if there is an error retrieveing projects.
                     $scope.projects = [];
                    Notification.error('We have a temporary issue with retrieving projects. Please try again.');
                });
        };

         $scope.add_new_project = function () {
            $http.post(projectsRoot, {name:$scope.add_project.name, created_by:'1'}).
            success(function(){
                $scope.load_projects();
                Notification.success('Project added successfully.');
            }).error(function(){
                Notification.error('We have a temporary issue with saving project. Please try again.');
            });
            $scope.cancel_add_project();
        };

        $scope.remove_project = function(){
            Project.remove({'id':$scope.selectedProject.id},
                function(){
                    $scope.load_projects();
                    $scope.selectedProject = undefined;
                    $("#sidebar-wrapper-rigth").toggleClass("toggled");
                    Notification.success('Project removed successfully.');
                },
                function(){
                    Notification.error('We have a temporary issue. Please try again.');
                });
        };
        ///////////////////////////////////////////////////////////////////////////////////////////////

        // UI relevant update methods
        $scope.cancel_add_project = function(){
            $scope.add_new = false;
            $scope.add_project = {};
        }

        $scope.start_add_project = function(){
            $scope.add_new = true;
            $scope.add_project = {};
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
        ///////////////////////////////////////////////////////////////////////////////////////


        $scope.criteriaMatch = function( criteria ) {
    	    return function( item ) {
    		    switch (criteria.parameter){
    			    case 'All':
    				    return true;
    			    case 'Mine':
    				    return item.created_by == 1;
    			    case 'Shared':
    				    //return item.members.length > 0;
                        return item;
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
            if($scope.projects != undefined && $scope.projects.length >0) {
                switch (criteria) {
                    case 'Mine':
                        return $.grep($scope.projects, function (item) {
                            return item.created_by == 1
                        }).length;
                    case 'Shared':
                        //return $.grep($scope.projects, function(item){return item.members.length > 0}).length;
                        return 0;
                    case 'InProgress':
                        return $.grep($scope.projects, function (item) {
                            return item.percentage_complete != 100
                        }).length;
                    case 'Completed':
                        return $.grep($scope.projects, function (item) {
                            return item.percentage_complete == 100
                        }).length;
                }
            }else{
                return 0;
            }
        }
    });

