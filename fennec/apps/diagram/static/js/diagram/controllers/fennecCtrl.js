(function () {
    'use strict';

    // $scope.selectedTable - this is reading from grid
    // $scope.fennecProject - using in d3

    var module = angular.module('myApp.controllers')
        .controller('DiagramController',  function($scope, $filter, $http, diagramService){

            $scope.tabs = [{
			id:1,
			content:'This is a default tab on load'
		}]

		$scope.counter = 1;
		/** Function to add a new tab **/
		$scope.addTab = function(){
			$scope.counter++;
			$scope.tabs.push({id:$scope.counter,content:'Any Content'});
			$scope.selectedTab = $scope.tabs.length - 1; //set the newly added tab active.
		}

		/** Function to delete a tab **/
		$scope.deleteTab = function(index){
			$scope.tabs.splice(index,1); //remove the object from the array based on index
		}

		$scope.selectedTab = 0; //set selected tab to the 1st by default.

		/** Function to set selectedTab **/
		$scope.selectTab = function(index){
			$scope.selectedTab = index;
		}

            // TODO: get from url branchRevisionId
            // TODO: 1. load project_state(diagram,schemas) this is data
            //       2. Load the selected diagram elements(symbols)
            //       3. Copy the data to angular scope

            init();
            function init() {
                console.log("Ctrl-> fetching data from python service");
                $scope.diagramData = {tables: [], links: []};
                //$scope.diagramData = {tables: diagramService.getTablesData(), links: []}; //{tables: [], links: []};
                $scope.selectedTable = {};
                $scope.projectInfo = {};
                $scope.schemasInfo = [];
                $scope.diagrams = [];
                $scope.activeDiagram = {};
                $scope.branchRevisionId = 1; // read from URL

                //pythonCreateDiagramSave();
//                console.log("start loading data");
//                getBranchRevisionProjectState(1);
//                var millisecondsToWait = 1000;
//               setTimeout(function() {
//                    console.log($scope.brState);
//                }, millisecondsToWait);
//                console.log("end loading data");
//                testLoad(1);

                //var diagramId = "f199449d-357e-4f6e-8190-8d0446216c3f";
                loadBranchRevisionProjectAndDiagram(1);
            }

            // LOAD FUNCTIONS
            function loadBranchRevisionProjectAndDiagram(branchRevisionId,diagramId){
                var projectStateRequest = diagramService.loadBranchRevisionProjectState(branchRevisionId);
                   projectStateRequest.then(function(brState) {  // this is only run after $http completes
                          //console.log(result);
                           if(diagramId == undefined){
                                if(brState.diagrams.length>0){
                                    diagramId = brState.diagrams[0].id;
                                  //  console.log("Setting default diagram id:");
                                //    console.log(diagramId);
                                }
                           }
                           var diagramRequest = diagramService.loadDiagramElements(branchRevisionId,diagramId);
                            diagramRequest.then(function(diagramData){
                                  //console.log(diagramResult);
                                  //var diagramData = diagramResult;
                                  //console.log($scope.brState);

                                  //$scope.diagramData.tables[0].title = "Anyadat te geci";
                                prepareDiagramData(brState,diagramData);
                             });
                    });
                    projectStateRequest.catch(function(nesto){
                       console.log("log loadBranchRevisionProjectState error");
                    });

                    projectStateRequest.finally(function(nesto){
                       //console.log("log loadBranchRevisionProjectStatefinally");
                    });
            }
            function prepareDiagramData(branchRevisionStatusData,diagramData) {
                console.log(branchRevisionStatusData); console.log(diagramData);
                // ADD PROJECT INFO to scope
//                  "project": {
//                    "id": 1,
//                    "name": "Project 1",
//                    "description": null,
//                    "url": "Project object",
//                    "branch": {
//                        "id": 1,
//                        "name": "master",
//                        "revision": 0
//                    }
//                }
                $scope.projectInfo = branchRevisionStatusData.project;
                console.log("ProjectInfo: ");console.log($scope.projectInfo);
                // ADD DIAGRAMS to scope
//                "diagrams": [
//                    {
//                        "id": "f199449d-357e-4f6e-8190-8d0446216c3f",
//                        "name": "Diagram 1",
//                        "description": "Diagram 1",
//                        "url": "f199449d-357e-4f6e-8190-8d0446216c3f"
//                    }
//                ]
                $scope.diagrams = branchRevisionStatusData.diagrams;
                console.log("Diagrams: ");console.log($scope.diagrams);
                $scope.activeDiagram = $scope.diagrams[0];
                // PADD SCHEMAS to scope

                setSchemasAndCreateFrontData(branchRevisionStatusData,diagramData);
                console.log("Front diagram data:");
                console.log($scope.diagramData);
            }
            function setSchemasAndCreateFrontData(branchRevisionStatusData,diagramData) {
                $scope.schemasInfo = [];

                for(var i in branchRevisionStatusData.schemas){
                    // SET SCHEMAS
                    $scope.schemasInfo.push({
                        id: branchRevisionStatusData.schemas[i].id,
                        databaseName:branchRevisionStatusData.schemas[i].databaseName,
                        comment: branchRevisionStatusData.schemas[i].comment,
                        collation: branchRevisionStatusData.schemas[i].collation,
                        namespaces: branchRevisionStatusData.schemas[i].namespaces
                    });

                    // SET DIAGRAM TABLES
                    for(var j in branchRevisionStatusData.schemas[i].tables){
                         // CHECK IF TABLE EXISTS ON CURRENT DIAGRAM
                         for(var k in diagramData.tableElements){
                              var dataTable = branchRevisionStatusData.schemas[i].tables[j];
                              if(dataTable.id == diagramData.tableElements[k].tableRef){
                                  // CREATE FRONT TABLE DATA
                                  var table ={
                                        data: dataTable,
                                        element: diagramData.tableElements[k],
                                        dataModified: 0,
                                        elModified: 0,
                                        attrs:[] // for now we need it
                                  };

                                  // ADD COLUMNS TO TABLE
                                  var columns = [];
                                  for(var j in dataTable.columns){
                                      columns.push({
                                            cdata: dataTable.columns[j],
                                            modified: 0
                                      });
                                  }
                                  table.data.columns = columns;
                                  // add to scope
                                  $scope.diagramData.tables.push(table);
                                  break;
                              }
                         }
                    }
                }
            }

            // SAVE DIAGRAM ON BUTTON
            $scope.saveDiagramButton = function(){
                console.log("Saving diagram be patient..");
                console.log("element modified: "+$scope.diagramData.tables[0].elModified);
                console.log($scope.diagramData.tables[0].dataModified);

                for(var i in $scope.diagramData.tables){
                    var table = $scope.diagramData.tables[i];
                    diagramService.saveTableData($scope.activeDiagram.id,table.data);

                    if(table.elModified == 1){
                        diagramService.saveTableElement($scope.activeDiagram.id,table.element);
                        table.elModified = 0; // reset it
                    }
                }
            }

            function getDiagramTableElements(branchRevisionId, diagramId){

            }

            function pythonSave(){
                  diagramService.pythonSave();
//                    projects.then(function(result) {  // this is only run after $http completes
//                       $scope.data = result;
//                    });
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

            // ********* ADD/EDIT COLUMN *********
            $scope.addTable = function() {
                var tableDataId = $scope.selectedTable.data.id;
                console.log("Selected table id: "+tableDataId);
                $scope.inserted = {
                    cdata:{
                        id: genGuid(),
                        name: "column",
                        comment:"add some comment",
                        column_type: "INT",
                        length:150,
                        precision:0.0,
                        default:"default",
                        collation:"utf-8",
                        ordinal:0,
                        primary: true,
                        nullable: true,
                        unique:true,
                        autoIncrement:false,
                        dictionary:false,
                        tableRef:tableDataId
                    },
                    modified: 1
                };
                var tableIndex = findTablePositionInArray(tableDataId,  $scope.diagramData.tables);
                if(tableIndex != null){
                    $scope.diagramData.tables[tableIndex].data.columns.push($scope.inserted);
                }
                console.log("ctrl-> new column initialized");
            };
            $scope.saveTable = function(data, id) {
                var selected = $filter('filter')($scope.dataTypes, {value: data.dataType});
                if(selected.length !=0){
                    var tableId = $scope.selectedTable.data.id;
                    var tableIndex = findTablePositionInArray(tableId,  $scope.diagramData.tables);
                    var selectedTableColumns = $scope.diagramData.tables[tableIndex].data.columns;
                    var columnData = getColumnDataForId(id, selectedTableColumns);
                    columnData.column_type= selected[0].text;
                    data.column_type= selected[0].text;
                }
                console.log("Column successfully saved")
                return [200, {status: 'ok'}];
            };
            function getColumnDataForId(columnId, columns){
                for(var i = 0; i<columns.length;i++){
                    if(columns[i].cdata.id==columnId){
                        return columns[i].cdata;
                    }
                }
            }

            // ********* REMOVE COLUMN *********
            $scope.removeTableColumn = function(index) {
                // delete links if exists
                var columnData = $scope.selectedTable.data.columns[index].cdata;
                deleteLink( $scope.selectedTable.id, columnData.id , $scope.diagramData.links);

                // remove column from table
                $scope.selectedTable.data.columns.splice(index,1);

                console.log("ctrl -> column["+columnData.name+"] deleted successfully");
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

            $scope.showColumnType = function(column) {
                var selected = [];
                if(column.cdata.column_type) {
                    selected = $filter('filter')($scope.dataTypes, {text: column.cdata.column_type}); // this is how can we search trough list
                    if(selected.length ==0){
                        selected = $filter('filter')($scope.dataTypes, {value: column.cdata.column_type});
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


            // ******** THIS CONTROLLER UTIL FUNCTION ********
            function findTablePositionInArray(tableId, tables){
                for(var i = 0; i<tables.length;i++){
                    if(tables[i].data.id==tableId){
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