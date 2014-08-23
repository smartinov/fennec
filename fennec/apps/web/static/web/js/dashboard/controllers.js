var projectsRoot = '/api/projects/'
app = angular.module('fennec.dashboard', ['mgcrea.ngStrap','ngAnimate'])

app.config(function($alertProvider) {
      angular.extend($alertProvider.defaults, {
        animation: 'am-fade-and-slide-top',
        placement: 'top-right',
        duration: 3,
        container: '#alert-container'
      });
    }).controller("ProjectsController", ['$scope','$http','$alert',
    function ($scope, $http, $alert) {
        $scope.projects = [];
        $scope.reload = function () {
            $http.get(projectsRoot).success(function (data, status) {
                $scope.projects = data;
            });
        }

        $scope.create = function(name) {
           project = {
              "name":name,
              "description":"No description provided",
              "created_by":"http://127.0.0.1:8000/api/users/1/"
           }

           data = angular.toJson(project);
           $http.post(projectsRoot,data)
           .success(function (data,status) {
                $scope.reload();
                $scope.project_name = '';
                var myAlert = $alert({title: 'Success!', content: 'Project creation successful!   ', type: 'info', show: true});
           }).error(function (data,status) {

           });
        }

    }]);
