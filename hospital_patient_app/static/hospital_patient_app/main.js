/**
 * Created by darkfree on 02.05.18.
 */
angular.module("patient_view", [])
    .component("authorization", {
        controller: function ($scope, $http) {
            $scope.login = "";
            $scope.password = "";
            $scope.message = "";
            $scope.authorize = function () {
                $http.post().success(function (_data) {
                    console.log(_data.data)
                });
                $scope.message = $scope.login;
            }
        },
        template: `
<style>
    #auth_form{
        text-align: center;
        width: {{ $ctrl.width }}px;
        height: {{ $ctrl.height }}px;
        background: gray;
    }
    #auth_form>input{
        width: 98%;
        margin: 5px 1% 0 1%;
        height: {{ $ctrl.height/3 - 10 }}px;
    }
</style>
<form ng-submit="authorize()" id="auth_form">
    <input type="text" placeholder="Електронна пошта" ng-model="login">
    <input type="password" ng-model="password">
    <input type="submit" value="Увійти">
    {{ message }}
</form>
`,
        bindings: {
            width: '@',
            height: '@',
            fontSize: '@',
        }
    });