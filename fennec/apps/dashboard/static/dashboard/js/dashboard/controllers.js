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
        $scope.projects = [];
        $scope.reload = function () {
            $scope.projects = Projects.query();
        };

        $scope.create = function (name) {
            project = {
                "name": name,
                "description": "No description provided",
                "created_by": "http://127.0.0.1:8000/api/users/1/"
            };

            data = angular.toJson(project);
            $http.post(projectsRoot, data)
                .success(function (data, status) {
                    $scope.reload();
                    $scope.project_name = '';
                    var myAlert = $alert({title: 'Success!', content: 'Project creation successful!   ', type: 'info', show: true});
                }).error(function (data, status) {

                });
        }
    });
