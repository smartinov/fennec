var projectsRoot = '/api/projects/';
var app = angular.module('fennec.dashboard', ['mgcrea.ngStrap', 'ngAnimate', 'ngResource']);

app.factory('Projects', function ($resource) {
    return $resource('/api/projects/:id'); // Note the full endpoint address
});
app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.headers.common['X-CSRFToken'] = '{{ csrf_token|escapejs }}';
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
        $scope.projects = [];
        $scope.reload = function () {
            $scope.projects = Projects.query();
        }

        $scope.create = function (name) {
            project = {
                "name": name,
                "description": "No description provided",
                "created_by": "http://127.0.0.1:8000/api/users/1/"
            }

            data = angular.toJson(project);
            $http.post(projectsRoot, data)
                .success(function (data, status) {
                    $scope.reload();
                    $scope.project_name = '';
                    var myAlert = $alert({title: 'Success!', content: 'Project creation successful!   ', type: 'info', show: true});
                }).error(function (data, status) {

                });
        };

        $scope.toggleSidebar = function(item){
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
    				    return item.owner == $scope.UserFullName;
    			    case 'Shared':
    				    return item.members.length > 0;
    			    case 'InProgress':
    				    return item.percentage_complete != 100;
    			    case 'Completed':
    				    return item.percentage_complete == 100;
    			    case 'Archived':
    				    return item.isArchived == 'true';
    		    }
    	    };
  	    };

        $scope.filterBy = function(filter_parameter){
    	    $scope.criteria = {parameter: filter_parameter};
        };


    });
