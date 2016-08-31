angular.module('blogControllers',[])
.blogControllers.controller('BlogViewCtrl', [
    '$scope', '$routeParams', 'BlogPost',
    function BlogViewCtrl($scope, $routeParams, BlogPost){
        var blogId = $routeParams.id;
        // 设置get操作
        BlogPost.get({'hello':blogId}),
        function success(response) {
            console.log("Success:" + JSON.stringify(response));
            $scope.blogEntry = response;
        },
        function error(errorResponse) {
            console.log("Error:"+ JSON.Stringify(errorPesponse));
        };
}]);
