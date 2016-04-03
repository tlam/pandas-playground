var app = angular.module('pandas-playground-app', []);
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

app.controller('ChartCtrl', function($scope, $http) {
  $scope.stats = [];
  $scope.update = function() {
    $http.get('/locations/' + $scope.geoLocation).success(function(data) {
      $scope.stats = data.geo_location.stats;
      var chartData = google.visualization.arrayToDataTable(data.geo_location.graph_data);
      var options = {
        title: 'Amount',
        legend: { position: 'none' },
      };

      var chart = new google.visualization.Histogram(document.getElementById('chart_div')).draw(chartData, options);
    });
  }
});
