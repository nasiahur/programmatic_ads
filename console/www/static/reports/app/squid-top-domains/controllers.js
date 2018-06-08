//
//
//
var reportControllers = angular.module('reportControllers', []);

function compareBySize(a,b) {
  if (a.size > b.size)
    return -1;
  if (a.size < b.size)
    return 1;
  return 0;
}

function function_bytes(bytes) {
    if (isNaN(parseFloat(bytes)) || !isFinite(bytes) || bytes == 0) return '0';
    var units = {1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'},
    measure, floor, precision;
    if (bytes > 1099511627775) {
       measure = 4;
    } else if (bytes > 1048575999 && bytes <= 1099511627775) {
       measure = 3;
    } else if (bytes > 1024000 && bytes <= 1048575999) {
       measure = 2;
    } else if (bytes <= 1024000) {
       measure = 1;
    }
    floor = Math.floor(bytes / Math.pow(1024, measure)).toString().length;
    if (floor > 3) {
       precision = 0
    } else {
       precision = 3 - floor;
    }
    return (bytes / Math.pow(1024, measure)).toFixed(precision) + units[measure];
}

function function_duration(duration) {
    var seconds = Math.floor(duration / 1000);
    if (seconds == 0){
        return duration + " ms"
    }

    var minutes = Math.floor(duration / 60000);
    if (minutes == 0){
        return seconds + " s"
    }

    var hours = Math.floor(minutes / 60);
    if (hours == 0){
        return minutes + " min"
    }
    return hours + " h"
}

function build_domain_table(domains) {
    var rawHeader = "<thead class=\"md-head\">"+
                    "<tr class=\"md-row\">" +
                    "<th class=\"md-column\"><span class=\"bold\">Domain</span></th>" +
                    "<th class=\"md-column\" class=\"md-numeric\">Size</th>" +
                    "<th class=\"md-column\" class=\"md-numeric\">Duration</th>" +
                    "</tr></thead>";

    var rawBody = "<tbody class=\"md-body\">";
    angular.forEach(domains, function(domain, domainIndex) {
        var row = "<tr class=\"md-row\">" +
                  "<td class=\"md-cell\"><a href=\"#/domain/" + domain.id + "\">" + domain.value + "</a></td>" +
                  "<td class=\"md-cell\">" + function_bytes(domain.size) + "</td>" +
                  "<td class=\"md-cell\">" + function_duration(domain.duration) + "</td></tr>";
        rawBody = rawBody + row + "\n";
    });
    rawBody = rawBody + "</tbody>";

    var rawHtml= rawHeader + rawBody;
    var userTable = document.getElementById("domain_table");
    angular.element(userTable).html(rawHtml);
}
reportControllers.controller('DomainsCtrl', ['$scope', '$http', function ($scope, $http) {

    $http.get('data/meta.json').success(function(data) {
        $scope.meta = data;

        $http.get('data/domains/domains.json').success(function(data) {
            $scope.domains = data;
            $scope.domains.sort(compareBySize);
            $scope.domains = $scope.domains.slice(0, $scope.meta['job']['params']['limit_n_entries']);
            build_domain_table($scope.domains);
        });
    });
}]);

function build_domain_users_table(users, domainId) {
    var rawHeader = "<thead class=\"md-head\">"+
                    "<tr class=\"md-row\">" +
                    "<th class=\"md-column\"><span class=\"bold\">User Name</span></th>" +
                    "<th class=\"md-column\" class=\"md-numeric\">Duration</th>" +
                    "<th class=\"md-column\" class=\"md-numeric\">Size</th>" +
                    "</tr></thead>";

    var rawBody = "<tbody class=\"md-body\">";
    angular.forEach(users, function(u, unusedIndex){
        var row = "<tr class=\"md-row\">" +
                  "<td class=\"md-cell\">" + u.value + "</td>" +
                  "<td class=\"md-cell\">" + function_duration(u.duration) + "</td>" +
                  "<td class=\"md-cell\">" + function_bytes(u.size) + "</td></tr>";
        rawBody = rawBody + row + "\n";
    });
    rawBody = rawBody + "</tbody>";

    var rawHtml= rawHeader + rawBody;
    var usersTable = document.getElementById("users_table");
    angular.element(usersTable).html(rawHtml);
}

reportControllers.controller('DomainCtrl', ['$scope', '$routeParams', '$http', function($scope, $routeParams, $http) {
    $scope.domainId = $routeParams.domainId;
    $http.get('data/meta.json').success(function(data) {
        $scope.meta = data;

        $http.get('data/domains/' + $routeParams.domainId + '/detailed')
            .success(function(data) {
              $scope.domain = data["domain"]
              users = data["records"];
              users.sort(compareBySize);
              users = users.slice(0, $scope.meta['job']['params']['limit_n_drilldown']);
              build_domain_users_table(users, $scope.domainId);
	   });
     });
}]);
//
//
//
reportControllers.controller('LogCtrl', ['$scope', '$http', function($scope, $http) {

    $http.get('data/report.log').success(function(data) {
        $scope.log = data;
    });
}]);
