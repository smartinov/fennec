/**
 * Created by smartinov on 6/1/14.
 */
var notifications_base = '/api/notifications/';

var NotificationsPopover = function ($scope, $http) {
    $http.get(notifications_base+'?seen=false').success(function (data, status) {
        $scope.popover = {
            'content': data
        };
    });
    $scope.remove = function (index) {
        var notification = $scope.content[index];
        notification.seen_on = new Date().toJSON();
        $http.put(notifications_base  + notification.id, notification).success(function (data, status) {
            $scope.content.splice(index, 1);
        });
    };
};

