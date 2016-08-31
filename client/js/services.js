angular.module('blogServices', ['ngResource'])
.blogServices.factory('BlogPost', ['$resource', function($resource){
    return $resource('http://172.16.191.163:8080/api/', {}, {
        get:{method:'GET',cache:false,isArray:false},
        save:{method:'POST',cache:false,isArray:false},
        update:{method:'PUT',cache:false,isArray:false},
        delete:{method:'DELETE',cache:false,isArray:false}
    });
}]);