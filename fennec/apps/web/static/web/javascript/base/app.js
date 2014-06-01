/**
 * Created by smartinov on 6/1/14.
 */


var NotificationsPopover = function ($scope, $http) {
    $http.get("/api/notifications").success(function (data, status) {
        $scope.popover = {
            'content': data
        };
    });
};

