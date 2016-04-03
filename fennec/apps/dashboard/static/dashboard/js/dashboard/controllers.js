var projectsRoot = '/api/projects/';
var branchesRoot = '/api/branches/';
var usersRoot = '/api/users/';
var notification_popup_template = '../';
var app = angular.module('fennec.dashboard', ['mgcrea.ngStrap', 'ngAnimate','ui-notification', 'ngResource', 'ngSanitize', 'ngDialog']);
var add_branch_html_template = '<div class="ngdialog-message">' +
                               '  <h2>Add new branch</h2>' +
                               '<div style="margin-top: 5%;">'+
                               '  <span>Name:</span>' +
                               ' <input type="text" name="name" ng-model="addBranchModel.name" style="margin-left: 10%;"><br>'+
                               '</div>'+
                               '<div style="margin-top: 5%;">'+
                               '  <span>Type:</span>'+
                               ' <input type="text" name="type" ng-model="addBranchModel.type" style="margin-left: 11.5%;"><br>'+
                               '</div>'+
                                '<div style="margin-top: 5%;">'+
                               ' <span>Description:</span>'+
                               ' <input type="text" name="description" ng-model="addBranchModel.description" style="margin-left: 1%;"></div><br>'+
                               '    <div class="ngdialog-buttons">' +
                               '      <button type="button" class="ngdialog-button" ng-click="add_branch()">Add</button>' +
                               '      <button type="button" class="ngdialog-button" ng-click="closeThisDialog()">Cancel</button>' +
                               '    </div>' +
                               '</div>';


app.factory('Project', function($resource){
    return $resource('/api/projects/:id', {'id':'@id'},
        {
            'update':{method:'PUT'}
        }
    );
});

app.factory('ProjectBranches', ['$http', function($http){
    var url_base =  '/api/branches/';
    var obj = {};
    obj.getProjectBranches = function(id){
        return $http.get(url_base+'?project_ref='+id);
    }
    obj.addProjectBranch = function(b_name, b_type, b_description, b_project, b_created_by){
        return $http.post(branchesRoot, {name:b_name, type:b_type, description:b_description, current_version:0, project_ref:b_project, created_by:b_created_by});
    }
    return obj;
}]);

app.config(['$httpProvider', '$interpolateProvider', 'ngDialogProvider', function ($httpProvider, $interpolateProvider, ngDialogProvider) {
     /* for compatibility with django teplate engine */
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    //Interpolate angular start and end symbols
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
    ngDialogProvider.setDefaults({
        className: 'ngdialog-theme-plain',
        plain: true,
        showClose: true,
        closeByDocument: true,
        closeByEscape: true
    });
}]);

app.controller("ProjectsController",
    function ($scope, $http, Notification, Project, ProjectBranches, ngDialog) {
        $scope.UserFullName = 'Nikola Latinovic';
        $scope.criteria = {parameter:'All'};
        $scope.add_project = {};
        $scope.add_new = false;
        $scope.selected_project_branches = [];
        $scope.selectedBranch = {};
        $scope.addBranchModel = {};

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

        /////// Project Branches Operations //////////////////////////////////////////////////////////
        $scope.load_project_branches = function(){
            ProjectBranches.getProjectBranches($scope.selectedProject.id)
                .then(function(response){
                    $scope.selected_project_branches = response.data;
                    $scope.selectedBranch = $scope.selected_project_branches[0];
                }, function(error){
                    $scope.selected_project_branches = [];
                    Notification.error('We have a temporary issue retrieving branches. Please try again.');
                });
        }
        $scope.open_add_branch = function(){
            ngDialog.open({ template: add_branch_html_template,
                            scope: $scope});
        }

        $scope.add_branch = function(){
             $http.post(branchesRoot, {name:$scope.addBranchModel.name, type: $scope.addBranchModel.type, description: $scope.addBranchModel.description, current_version:0, project_ref:$scope.selectedProject.id, created_by:'1'}).
                  success(function(){$scope.load_project_branches(); ngDialog.close(); Notification.success('Branch added successfully.');}).
                  error(function () {Notification.error('We have a temporary issue with saving branch. Please try again.');});
             $scope.addBranchModel = {}
        }
        //////////////////////////////////////////////////////////////////////////////////////////////

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
                    $scope.load_project_branches();
                }else{
                    $("#sidebar-wrapper-rigth").toggleClass("toggled");
                }
            }else{
                 $scope.selectedProject = item;
                 $scope.load_project_branches();
                $("#sidebar-wrapper-rigth").toggleClass("toggled");
            }
            //Reset Selected project if there is no sidebar
            if(!$("#sidebar-wrapper-rigth").hasClass('toggled')) {
                $scope.selectedProject = undefined;
                $scope.selected_project_branches = [];
            }
        };
        ///////////////////////////////////////////////////////////////////////////////////////

        //Projects filtering methods
        $scope.criteriaMatch = function( criteria ) {
    	    return function( item ) {
    		    switch (criteria.parameter){
    			    case 'All':
    				    return true;
    			    case 'Mine':
    				    return item.created_by == 1;
    			    case 'Shared':
    				    //return item.members.length > 0;
                        //add members to project function required
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
        /////////////////////////////////////////////////////////////////////////////////////////
    });

