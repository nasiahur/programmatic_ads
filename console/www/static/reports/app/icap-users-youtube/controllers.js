//
//
//
var reportControllers = angular.module('reportControllers', []);

//
//
//
reportControllers.controller('ListCtrl', ['$scope', '$http', function ($scope, $http) {

	$http.get('data/users.json').success(function(data) {
		$scope.users = data;
	});

	$http.get('data/meta.json').success(function(data) {
		$scope.meta = data;
	});
}]);

//
//
//
reportControllers.controller('DetailCtrl', ['$scope', '$routeParams', '$http', function($scope, $routeParams, $http) {
    $scope.item = $routeParams.item;

    	$http.get('data/users.json').success(function(data) {
		$scope.users = data;
	});

    $scope.isCurrentUser = function(user) {
        return user.name === $scope.item;
    };
}]);

//
//
//
reportControllers.controller('LogCtrl', ['$scope', '$http', function($scope, $http) {

    $http.get('data/report.log').success(function(data) {
		$scope.log = data;
	});
}]);