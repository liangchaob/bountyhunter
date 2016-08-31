// 引导
angular.module('blogApp',['ngRoute','blogControllers','blogServices'])
.blogApp.config(['$routeProvider','$locationProvider',
    function($routeProvider,$locationProvider) {
        $routeProvider.when('/blogPost/',{
                templateUrl:'partials/blogPost.html',
                controller:'BlogViewCtrl'
            });
        $locationProvider.html5Mode(false).hashPrefix('!');
        }
    ]);

