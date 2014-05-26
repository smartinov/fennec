var projectsRoot = '/rest/projects'

function Projects($scope,$http) {
  $scope.projects = [];
  $scope.load = function(){
    $http.get(projectsRoot).success(function(data, status) {
        $scope.projects = data;
    });
  }
}
