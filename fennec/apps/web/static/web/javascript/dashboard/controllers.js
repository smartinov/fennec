var projectsRoot = '/api/projects'
app = angular.module('fennec.dashboard',  ['mgcrea.ngStrap'])

app.controller("ProjectsController", ['$scope', '$http',
    function ($scope, $http) {
        $scope.projects = [];
        $scope.load = function () {
            $http.get(projectsRoot).success(function (data, status) {
                $scope.projects = data;
            });
        }
    }]);
