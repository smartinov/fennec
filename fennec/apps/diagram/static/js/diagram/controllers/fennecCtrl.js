(function () {
    'use strict';

    // $scope.selectedTable - this is reading from grid
    // $scope.fennecProject - using in d3

    var module = angular.module('myApp.controllers')
        .controller('DiagramController',  function($scope, $filter, $http, diagramService){

            init();
            function init(){
                console.log("Ctrl-> Fetching data from service.");
                $scope.diagramData =  {tables: diagramService.getTablesData(), links: diagramService.getLinksData()};
                $scope.selectedTable = {};
            }

            //$scope.$on('selectedTableEvent', function(scope, selectedTable){
            //    // when select the table this method is called
            //    console.log("Ctrl-> table selected: "+selectedTable.id);
            //    $scope.selectedTable = selectedTable;
            //    $scope.$apply();
            //});
            $scope.$on('deleteTableEvent', function(scope, deletedTable){
                console.log("Ctrl-> table deleted: "+deletedTable.id);

                // when select the table this method is called
                if( $scope.selectedTable!=null &&  $scope.selectedTable.id == deletedTable.id){
                    $scope.selectedTable = null;
                }

                // delete from list
                deleteTable(deletedTable.id, $scope.diagramData.tables);
                $scope.$apply();
            });


            // add user
            $scope.addTable = function() {
                $scope.inserted = {
                    id: genGuid(),
                    name: "column",
                    dataType: "INT"
                };
                var id = $scope.selectedTable.id;
                var tableIndex = findTablePositionInArray(id,  $scope.diagramData.tables);
                if(tableIndex != null){
                    $scope.diagramData.tables[tableIndex].attrs.push($scope.inserted);
                }
                console.log("Ctrl-> addTable init");
            };
            $scope.saveTable = function(data, id) {
                var selected = $filter('filter')($scope.dataTypes, {value: data.dataType});
                if(selected.length !=0){
                    var tableId = $scope.selectedTable.id;
                    var tableIndex = findTablePositionInArray(tableId,  $scope.diagramData.tables);
                    var column = getColumnForId(id, $scope.diagramData.tables[tableIndex].attrs);
                    column.dataType= selected[0].text;
                    data.dataType= selected[0].text;
                }
                console.log("Attribute saved")
                return [200, {status: 'ok'}];
            };
            function getColumnForId(columnId, columns){
                for(var i = 0; i<columns.length;i++){
                    if(columns[i].id==columnId){
                        return columns[i];
                    }
                }
            }

            // remove column
            $scope.removeTableColumn = function(index) {
                // delete links if exists
                var column = $scope.selectedTable.attrs[index];
                deleteLink( $scope.selectedTable.id, column.id , $scope.diagramData.links);

                // remove column from table
                $scope.selectedTable.attrs.splice(index,1);

                console.log("Ctrl-> Column["+column.name+"] deleted");
            };



            $scope.dataTypes = [
                {value: 1, text: 'ID'},
                {value: 2, text: 'RefID'},
                {value: 3, text: 'TEXT'},
                {value: 4, text: 'INT'},
                {value: 5, text: 'BIGINT'},
                {value: 6, text: 'DECIMAL'},
                {value: 7, text: 'DOUBLE'},
                {value: 8, text: 'FLOAT'},
                {value: 9, text: 'TINYINT'},
                {value: 10, text: 'BOOL'},
                {value: 11, text: 'BOOLEAN'}
            ];


            $scope.showDataType = function(user) {
                var selected = [];
                if(user.dataType) {
                    selected = $filter('filter')($scope.dataTypes, {text: user.dataType}); // this is how can we search trough list
                    if(selected.length ==0){
                        selected = $filter('filter')($scope.dataTypes, {value: user.dataType});
                    }
                }
                return selected.length ? selected[0].text : 'Not set';
            };

            $scope.checkName = function(data, id) {
                if (id === 2 && data !== 'awesome') {
                    return "Username 2 should be `awesome`";
                }
            };
            function deleteTable(tableId, tables){
                for(var i = 0; i<tables.length;i++){
                    if(tables[i].id===tableId){
                        console.log("Ctrl-> Table["+tableId+"] is deleted");
                        tables.splice(i,1);
                    }
                }
                deleteTableLinks(tableId, $scope.diagramData.links);
            }
            function deleteTableLinks(tableId, links){
                for(var i = links.length-1; i>=0;i--){
                    if(links[i].source.tableId===tableId || links[i].target.tableId===tableId){
                            console.log("Ctrl-> Link["+links[i].id + "] is deleted");
                            links.splice(i,1);
                    }
                }
            }
            function deleteLink(tableId, columnId , links){
                // if there is a link bound to column, delete link
                for(var i = links.length-1; i>=0;i--){
                    if((links[i].source.tableId===tableId && links[i].source.attr.id === columnId) ||
                        (links[i].target.tableId===tableId && links[i].target.attr.id === columnId) ) {
                        console.log("Ctrl-> Link["+links[i].id + "] is deleted");
                        links.splice(i,1);
                    }
                }
            }



            // ******** THIS CONTROLLER UTIL FUNCTION
            function findTablePositionInArray(tableId, tables){
                for(var i = 0; i<tables.length;i++){
                    if(tables[i].id==tableId){
                        return i;
                    }
                }
                console.log("Table not found for id: "+tableId);
                return null;
            }
            // *************** UTIL FUNCTIONS **************************
            var guid = (function () {
                function s4() {
                    return Math.floor((1 + Math.random()) * 0x10000)
                        .toString(16)
                        .substring(1);
                }

                return function () {
                    return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
                        s4() + '-' + s4() + s4() + s4();
                };
            })();
            function genGuid() {
                //  id-s started with number is not recognized by d3.select function
                var id = guid();
                id = id.slice(1);
                var possible = "abcdef";
                var hexLetter = possible.charAt(Math.floor(Math.random() * possible.length))
                id = hexLetter + id;
                console.log(id);
                return id;
            }
        });

}());