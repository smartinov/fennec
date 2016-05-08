var projectsRoot = '/api/projects/';
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
var edit_project_html_template = '<div class="ngdialog-message">' +
                               '  <h2>Edit [[selectedProject.title]]</h2>' +
                               '<div style="margin-top: 5%;">'+
                               '  <span>Name:</span>' +
                               ' <input type="text" name="name" ng-model="selectedProject.name" style="margin-left: 10%; width:75%;"><br>'+
                               '</div>'+
                               '<div style="margin-top: 5%;">'+
                               ' <span>Description:</span>'+
                               ' <textarea name="description" ng-model="selectedProject.description" style="margin-left: 1%; width:75%;"></textarea></div><br>'+
                               '    <div class="ngdialog-buttons">' +
                               '      <button type="button" class="ngdialog-button" ng-click="save_edit_project()">Save</button>' +
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
    var url_branch = '/api/branch-revisions/replace_id/branch/';
    var obj = {};
    obj.getProjectBranches = function(id){
        return $http.get(url_base+'?project_ref='+id);
    }
    obj.branchFromBranchRevision = function(revision_id, b_name, b_type, b_description){
        var url = url_branch.replace('replace_id', revision_id);
        return $http.post(url, {'name': b_name, 'type':b_type, 'description': b_description});
    }

    obj.addProjectBranch = function(b_name, b_type, b_description, b_project, b_created_by){
        return $http.post(url_base, {name:b_name, type:b_type, description:b_description, current_version:0, project_ref:b_project, created_by:b_created_by});
    }
    return obj;
}]);

app.factory('BranchRevisions',['$http', function($http) {
    var url_base = '/api/branch-revisions/';
    var url_commit = '/api/branch-revisions/revision_id/commit/';
    var obj = {};
    obj.getBranchRevisions = function(id){
        return $http.get(url_base+'?branch_ref='+id);
    }
    obj.postCommitRevision = function(id){
        return $http.post(url_commit.replace('revision_id', id));
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
    function ($scope, $http, Notification, Project, ProjectBranches, ngDialog, BranchRevisions, $location, $window) {
        $scope.UserFullName = 'Nikola Latinovic';
        $scope.criteria = {parameter:'All'};
        $scope.add_project = {};
        $scope.add_new = false;
        $scope.selected_project_branches = [];
        $scope.selectedBranch = undefined;
        $scope.selectedRevision = undefined;
        $scope.selectedBracnhRevisions = [];
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
        $scope.edit_project = function(){
            $scope.selectedProject.title = $scope.selectedProject.name;
            ngDialog.open({ template: edit_project_html_template,
                               scope: $scope});
        }
        $scope.save_edit_project = function(){
             $http.put(projectsRoot+$scope.selectedProject.id+'/', {name:$scope.selectedProject.name, description:$scope.selectedProject.description, created_by:$scope.selectedProject.created_by}).
                 success(function() {
                    ngDialog.close();
                    Notification.success('Project saved successfully.');
                 }).error(function() {
                    Notification.error('We have a temporary issue with saving project. Please try again.');
                 });
        }
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
        }

        $scope.open_project = function(){
            if($scope.selectedBranch != undefined && $scope.selectedRevision != undefined){
               var redirect_url = 'diagram/projects/pid/branches/bid/branch-revision/rid';
               $window.location.href = redirect_url.replace('pid',$scope.selectedProject.id).replace('bid',$scope.selectedBranch.id)
                   .replace('rid',$scope.selectedRevision.id);
            }else{
                 Notification.error('Please select branch and revision first.');
            }
        }
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

        $scope.updateBranch = function(){
            if($scope.selectedBranch != undefined) {
                BranchRevisions.getBranchRevisions($scope.selectedBranch.id)
                    .success(function (response) {
                        $scope.selectedBracnhRevisions = response;
                        $scope.selectedRevision = response[0];
                    })
                    .error(function () {
                        Notification.error('Error retrieving branch revisions.');
                    });
            }
        };

        $scope.open_add_branch = function(){
            if($scope.selectedBranch != undefined && $scope.selectedRevision != undefined) {
               ngDialog.open({ template: add_branch_html_template,
                               scope: $scope});
            }else{
                Notification.error('Please select branch to branch from.');
            }
        }

        $scope.add_branch = function(){
             ProjectBranches.branchFromBranchRevision($scope.selectedRevision.id,  $scope.addBranchModel.name, $scope.addBranchModel.type, $scope.addBranchModel.description).
                  success(function(){$scope.load_project_branches(); ngDialog.close(); Notification.success('Branched successfully.');}).
                  error(function () {Notification.error('We have a temporary issue with saving branch. Please try again.');});
             $scope.addBranchModel = {}
        }

        $scope.commit_branch = function(){
            if($scope.selectedRevision!=undefined){
                BranchRevisions.postCommitRevision($scope.selectedRevision.id)
                    .success(function(){Notification.success('Changes commited successfully.');})
                    .error(function (){Notification.error('We have a temporary issue commiting changes. Please try again.');});

            }else{
                Notification.error('Please select revision to commit.');
            }
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

