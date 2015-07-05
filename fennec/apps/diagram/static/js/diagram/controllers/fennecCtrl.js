(function () {
    'use strict';

    var module = angular.module('myApp.controllers')
        .controller('DiagramController', function ($scope, $filter, $http, diagramService, spinnerService) {

            init();
            function init() {
                $scope.projectInfo = {};
                $scope.schemas = [];
                $scope.activeSchema = {};
                $scope.diagrams = [];
                $scope.branchRevisionId = 1; // read from URL             // TODO: get from url branchRevisionId
                $scope.newSchema = {id:"",databaseName:"",collation:""};
                clearDiagramSpecificsScopes();
                clearDeletedScopes();

                console.log("ctrl-> fetching data from server for brevision:" + $scope.branchRevisionId);
                loadBranchRevisionProjectAndDiagram($scope.branchRevisionId);
            }
            function clearDiagramSpecificsScopes() {
                console.log("ctrl-> clearing diagram specifics scopes");

                $scope.diagramData= {tables: [], links: []};
                $scope.selectedTable = {};
                $scope.selectedTableForeignKeys = [];
                $scope.selectedTableForeignKeyColumns=[]; // refIndexColumns - it contain only columns which are indexed
                $scope.selectedTableIndexes = [];
                $scope.activeDiagramEditData = {};  // for edit form
            }
            function clearDeletedScopes(){
                console.log("ctrl -> clearing deleted scopes");
                $scope.deletedTableElements = []; // for now only deleting table elements
                $scope.deletedColumnsData = [];
                $scope.deletedLinks = [];
            }


            // ****** TAB HANDLER ******
            $scope.selectedDiagram = 0; //set selected tab to the 1st by default.
            $scope.addDiagram = function () {
                if($scope.activeDiagram!=undefined && confirm("You are going to create new diagram, save changes on ["+$scope.activeDiagram.data.name+"] diagram") == true) {
                    // save current diagram
                    $scope.saveDiagramButton();
                }
                var extNewDiagramInfo = {data:{id:genGuid(),name:"new diagram",description:"description",url:""},modified:true};
                $scope.diagrams.push(extNewDiagramInfo);
                $scope.selectedDiagram = $scope.diagrams.length - 1; //set the newly added tab active.

                // clear scopes from previous diagram and set new diagram to active
                clearDiagramSpecificsScopes();
                $scope.activeDiagram = angular.copy(extNewDiagramInfo);
                $scope.activeDiagramEditData = angular.copy(extNewDiagramInfo); // for edit form
            }
            $scope.closeDiagram = function (index) {
                $scope.diagrams.splice(index, 1); //remove the object from the array based on index
                clearDiagramSpecificsScopes();

                loadBranchRevisionProjectAndDiagram($scope.branchRevisionId, $scope.diagrams[index].data.id);
            }
            $scope.selectDiagram = function (index) {
                if($scope.activeDiagram!=undefined && confirm("You are going to create new diagram, save changes on ["+$scope.activeDiagram.data.name+"] diagram") == true) {
                    // save current diagram
                    $scope.saveDiagramButton();
                }

                $scope.selectedDiagram = index;
                clearDiagramSpecificsScopes();

                loadBranchRevisionProjectAndDiagram($scope.branchRevisionId, $scope.diagrams[index].data.id);
            }


            // ******* LOAD FUNCTIONS *******
            function loadBranchRevisionProjectAndDiagram(branchRevisionId, diagramId) {
                spinnerService.showSpinner();
                var projectStateRequest = diagramService.loadBranchRevisionProjectState(branchRevisionId);
                projectStateRequest.then(function (brState) {  // this is only run after $http completes
                    //console.log(result);
                    if (diagramId == undefined) {
                        if (brState.diagrams.length > 0) {
                            diagramId = brState.diagrams[0].id;
                        }
                    }
                    var diagramRequest = diagramService.loadDiagramElements(branchRevisionId, diagramId);
                    diagramRequest.then(function (diagramElements) {
                        prepareDiagramData(brState, diagramElements,diagramId);
                        spinnerService.hideSpinner();
                    });
                });
                projectStateRequest.catch(function (nesto) {
                    console.log("log loadBranchRevisionProjectState error");
                });

                projectStateRequest.finally(function (nesto) {
                    //console.log("log loadBranchRevisionProjectStatefinally");
                });
            }
            function prepareDiagramData(branchRevisionStatusData, diagramElements,diagramId) {
                console.log(branchRevisionStatusData);
                console.log(diagramElements);
                // ADD PROJECT INFO to scope
                $scope.projectInfo = branchRevisionStatusData.project;
                console.log("ProjectInfo: ");
                console.log($scope.projectInfo);

                // ADD DIAGRAMS to scope

                    for(var i in branchRevisionStatusData.diagrams){
                        // load diagrams on page refresh(on tab change don't load)
                        var extDiagram = {data: branchRevisionStatusData.diagrams[i], modified: false};
                        if($scope.diagrams.length<branchRevisionStatusData.diagrams.length) {
                            $scope.diagrams.push(extDiagram);
                        }
                        console.log("Current processing diagram name:"+branchRevisionStatusData.diagrams[i].name);
                        if(diagramId == branchRevisionStatusData.diagrams[i].id){
                            console.log("Active diagram:"+extDiagram.data.name);
                            $scope.activeDiagram = extDiagram;
                            $scope.activeDiagramEditData = angular.copy(extDiagram);
                        }
                    }
                    console.log("Diagrams: ");console.log($scope.diagrams);

                if(diagramId == undefined){
                    $scope.activeDiagram = $scope.diagrams[0];
                    $scope.activeDiagramEditData =  angular.copy($scope.activeDiagram);
                }

                // ADD SCHEMAS to scope
                setSchemasAndCreateDataToDisplay(branchRevisionStatusData, diagramElements);
                console.log("Front diagram data:");
                console.log($scope.diagramData);
            }
            function setSchemasAndCreateDataToDisplay(branchRevisionStatusData, diagramElements) {
                // Load all data with project_state and then load diagram elements and bound the two together
                $scope.schemas = [];

                for (var i in branchRevisionStatusData.schemas) {
                    // SET SCHEMAS
                    var schema = {data:{
                                        id: branchRevisionStatusData.schemas[i].id,
                                        databaseName: branchRevisionStatusData.schemas[i].databaseName,
                                        comment: branchRevisionStatusData.schemas[i].comment,
                                        collation: branchRevisionStatusData.schemas[i].collation,
                                        namespaces: branchRevisionStatusData.schemas[i].namespaces
                                    },
                                    modified: false };
                    $scope.schemas.push(schema);

                    // SET DIAGRAM TABLES
                    for (var j in branchRevisionStatusData.schemas[i].tables) {
                        var dataTable = branchRevisionStatusData.schemas[i].tables[j];

                        // CHECK IF TABLE EXISTS ON CURRENT DIAGRAM
                        for (var k in diagramElements.tableElements) {
                            if (dataTable.id == diagramElements.tableElements[k].tableRef) {
                                // TABLE EXISTS ON CURRENT DIAGRAM, CREATE FRONT TABLE DATA
                                var table = {
                                    data: dataTable,
                                    element: diagramElements.tableElements[k],
                                    dataModified: false,
                                    elModified: false
                                };

                                // ADD COLUMNS TO TABLE
                                var columns = [];
                                for (var j in dataTable.columns) {
                                    columns.push({
                                        cdata: dataTable.columns[j],
                                        modified: false
                                    });
                                }
                                table.data.columns = columns;

                                // IF foreignKeys EXISTS on table data CHECK ON DIAGRAM AND CREATE LINK
                                for (var j in dataTable.foreignKeys) {
                                    var foreignKey = dataTable.foreignKeys[j];
                                    for(var m in diagramElements.relationshipElements){
                                        var relationElement = diagramElements.relationshipElements[m];
                                        if(foreignKey.id == relationElement.foreignKeyRef){
                                            var link ={
                                                fk_data: foreignKey,
                                                element:relationElement,
                                                dataModified: false,
                                                elModified: false
                                            }
                                            $scope.diagramData.links.push(link);
                                            break;
                                        }
                                    }
                                }

                                // add to scope
                                $scope.diagramData.tables.push(table);
                                break;
                            }
                        }
                    }
                }

                if($scope.schemas.length>0){
                    showCurrentSchemaInDropDown($scope.schemas[0].data);
                }else{
                    $scope.showCreateSchemaPopup();
                }
            }


            // ******* SAVE DIAGRAM ON BUTTON *******
            $scope.saveDiagramButton = function () {
                if(confirm("You are going to save diagram ["+$scope.activeDiagram.data.name+"], are you sure?") == false) {return;}

                console.log("Saving diagram["+$scope.activeDiagram.data.name+"] be patient..");
                var success = true;
                try{
                var branchRevisionId = $scope.branchRevisionId;

                // save new schemas
                for(var i in $scope.schemas){
                    if($scope.schemas[i].modified){
                        diagramService.saveSchema(branchRevisionId,$scope.schemas[i].data);
                    }
                }

                // save diagram data change
                if($scope.activeDiagram.modified){
                    diagramService.saveDiagramInfo(branchRevisionId,$scope.activeDiagram.data);
                }

                // save/update table
                for (var i in $scope.diagramData.tables) {
                    var table = $scope.diagramData.tables[i];

                    if (table.dataModified) {
                        diagramService.saveTableData(branchRevisionId, table.data);
                        table.dataModified = false; // reset it
                    }
                    if (table.elModified) {
                        diagramService.saveTableElement(branchRevisionId, table.element);
                        table.elModified = false; // reset it
                    }

                    for(var j in table.data.columns){
                        // var column = table.data.columns[(table.data.columns.length-1)-j]; // colak from back is saving columns to database
                        var column = table.data.columns[j]; // colak from back is saving columns to database
                        if(column.modified){
                            diagramService.saveColumn(branchRevisionId,column.cdata);
                            column.modified = false; // reset it
                        }
                    }
                }

                // save/update foreignKeys and relationElements
                for(var i in $scope.diagramData.links){
                    var link = $scope.diagramData.links[i];
                    if(link.dataModified){
                        diagramService.saveTableForeignKey(branchRevisionId,link.fk_data);
                        link.dataModified = false;
                    }
                    if(link.elModified){
                        diagramService.saveRelationshipElement(branchRevisionId,link.element);
                        link.elModified = false;
                    }
                }

                // delete table elements
                for(var i in $scope.deletedTableElements){
                    var delTableElement = $scope.deletedTableElements[i];
                    diagramService.deleteTableElement(branchRevisionId, delTableElement);
                }

                // delete columns
                for(var i in $scope.deletedColumnsData){
                    var delColumnData = $scope.deletedColumnsData[i];
                    diagramService.deleteColumn(branchRevisionId, delColumnData);
                }

                for(var i in $scope.deletedLinks){
                    var link = $scope.deletedLinks[i];
                    diagramService.deleteTableForeignKey(branchRevisionId, link.fk_data);
                    diagramService.deleteRelationshipElement(branchRevisionId, link.element);
                }

                }catch (err){
                    success = false;
                    console.log("Saving diagram["+$scope.activeDiagram.data.name+"] failed with msg:"+err);
                }
                if(success){
                    console.log("Diagram["+$scope.activeDiagram.data.name+"] content saved successfully");
                    clearDeletedScopes();
                }
            }

            $scope.editDiagramButton = function(){
                $scope.activeDiagramEditData.modified = true;
                $scope.activeDiagram = angular.copy($scope.activeDiagramEditData);
                for(var i in $scope.diagrams){
                    if($scope.diagrams[i].data.id == $scope.activeDiagram.data.id){
                        $scope.diagrams[i].data.name = $scope.activeDiagram.data.name;
                    }
                }
            }
            $scope.setTableToModified = function(selectedTable){
                selectedTable.dataModified = true;
            }
            $scope.$on('deleteTableEvent', function (scope, deletedTable) {
                deleteTableElement(deletedTable.data.id, $scope.diagramData.tables);

                    // when select the table this method is called
                if ($scope.selectedTable != null && $scope.selectedTable.id == deletedTable.id) {
                     $scope.selectedTable = null;
                }
                $scope.$apply();
            });


            // ****** FOREIGN KEY TAB ******
            $scope.editForeignKeyName = function(data,id){
                    console.log($scope.inserted);
            }
            $scope.showForeignKeyColumns = function(selectedForeignKeyData){
                //selectedForeignKeyData {data:foreignKey, table:table};
                $scope.selectedTableForeignKeyColumns=[{column:"",refColumn:"",refIndexColumns:[]}];// refIndexColumns - it contain only columns which are indexed

                var sourceTable = getTableForId(selectedForeignKeyData.data.tableRef);
                var column= getColumnForId(selectedForeignKeyData.data.sourceColumn, sourceTable.data.columns);
                var refColumn= getColumnForId(selectedForeignKeyData.data.referencedColumn, selectedForeignKeyData.table.data.columns);
                // TODO: get indexes for referenced table and then found columns
                // TODO: for now show all column
                var referencedTableIndexColumns = selectedForeignKeyData.table.data.columns;

                $scope.selectedTableForeignKeyColumns = [{column:column, refColumn:refColumn,comment:"", refIndexColumns:referencedTableIndexColumns}];
                console.log( $scope.selectedTableForeignKeyColumns);
//                console.log(column.cdata.name);
//                console.log(refColumn.cdata.name);
            }
            $scope.showReferencedColumnName = function (column) {
                if(column == undefined){
                    return "Not selected";
                }
                return column.cdata.name;
            };


            // ********* ADD/EDIT COLUMN *********
            $scope.addColumn = function () {
                var tableDataId = $scope.selectedTable.data.id;
                console.log("Selected table id: " + tableDataId);
                $scope.inserted = {
                    cdata: {
                        id: genGuid(),
                        name: "column",
                        comment: "add some comment",
                        column_type: "INT",
                        length: 150,
                        precision: 0.0,
                        default: "default",
                        collation: "utf-8",
                        ordinal: 0,
                        primary: true,
                        nullable: true,
                        unique: true,
                        autoIncrement: false,
                        dictionary: false,
                        tableRef: tableDataId
                    },
                    modified: true
                };
                var tableIndex = findTablePositionInArray(tableDataId, $scope.diagramData.tables);
                if (tableIndex != null) {
                    $scope.diagramData.tables[tableIndex].data.columns.push($scope.inserted);
                }
                console.log("ctrl-> new column initialized");
            };
            $scope.saveColumn = function (data, id) {
                var selected = $filter('filter')($scope.dataTypes, {value: data.dataType});
                if (selected.length != 0) {
                    var tableId = $scope.selectedTable.data.id;
                    var tableIndex = findTablePositionInArray(tableId, $scope.diagramData.tables);
                    var selectedTableColumns = $scope.diagramData.tables[tableIndex].data.columns;
                    var column = getColumnForId(id, selectedTableColumns);
                    column.cdata.column_type = selected[0].text;
                    column.modified = 1;
                }
                console.log("Column successfully saved")
                return [200, {status: 'ok'}];
            };
            function getColumnForId(columnId, columns) {
                for (var i = 0; i < columns.length; i++) {
                    if (columns[i].cdata.id == columnId) {
                        return columns[i];
                    }
                }
            }

            // ********* REMOVE COLUMN *********
            $scope.removeTableColumn = function (index) {
                // delete links if exists
                var columnData = $scope.selectedTable.data.columns[index].cdata;
                deleteColumnLink(columnData.id, $scope.diagramData.links);

                // remove column from table
                $scope.selectedTable.data.columns.splice(index, 1);

                $scope.deletedColumnsData.push(columnData);
                console.log("ctrl -> column[" + columnData.name + "] successfully deleted");
            };
            function deleteColumnLink(columnId, diagramLinks) {
                 for(var i = diagramLinks.length-1; i>=0;i--){
                    var link = diagramLinks[i];  // contain fk_data, element and dataModified, elModified
                    if (link.fk_data.sourceColumn == columnId  || link.fk_data.referencedColumn == columnId) {
                        console.log("ctrl -> link[" + link.fk_data.name + "] is deleted");
                        $scope.deletedLinks.push(link);
                        diagramLinks.splice(i, 1);
                    }
                }
            }

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
            $scope.showColumnType = function (column) {
                var selected = [];
                if (column.cdata.column_type) {
                    selected = $filter('filter')($scope.dataTypes, {text: column.cdata.column_type}); // this is how can we search trough list
                    if (selected.length == 0) {
                        selected = $filter('filter')($scope.dataTypes, {value: column.cdata.column_type});
                    }
                }
                return selected.length ? selected[0].text : 'Not set';
            };

            $scope.checkName = function (data, id) {
                if (id === 2 && data !== 'awesome') {
                    return "Username 2 should be `awesome`";
                }
            };
            function deleteTableElement(tableId, tables) {
                for (var i = 0; i < tables.length; i++) {
                    if (tables[i].data.id === tableId) {
                        console.log("ctrl -> table[" + tables[i].data.name + "] is deleted");
                        $scope.deletedTableElements.push(tables[i].element);
                        tables.splice(i, 1);
                    }
                }
                deleteTableLinks(tableId,$scope.diagramData.links);
            }

            function deleteTableLinks(tableId, diagramLinks) {
                for(var i = diagramLinks.length-1; i>=0;i--){
                    var link = diagramLinks[i];  // contain fk_data, element and dataModified, elModified
                    if (link.fk_data.tableRef == tableId || link.fk_data.referencedTableRef == tableId) {
                        console.log("ctrl -> link[" + link.fk_data.name + "] is deleted");
                        $scope.deletedLinks.push(link);
                        diagramLinks.splice(i, 1);
                    }
                }
            }


            // ********* CREATE SCHEMA *********
            $scope.isCreateSchemaPopupShown = false;
            $scope.showCreateSchemaPopup = function(){
                $scope.isCreateSchemaPopupShown = true;
            }
            $scope.createSchemaOk = function(){
                $scope.newSchema.id = genGuid();
                $scope.schemas.push({data:$scope.newSchema,modified: true});
                $scope.newSchema = {id:"",databaseName:"",collation:""};
                $scope.isCreateSchemaPopupShown = false;
                if($scope.schemas.length == 1){
                    showCurrentSchemaInDropDown($scope.schemas[0].data);
                }
            }
            $scope.createSchemaCancel = function(){
                $scope.isCreateSchemaPopupShown = false;
                $scope.newSchema = {id:"",databaseName:"",collation:""};
            }
            function showCurrentSchemaInDropDown(schemaData) {
                  $scope.activeSchema = schemaData; // select first schema in dropdown
            }

            // ******** THIS CONTROLLER UTIL FUNCTION ********
            function findTablePositionInArray(tableId, tables) {
                for (var i = 0; i < tables.length; i++) {
                    if (tables[i].data.id == tableId) {
                        return i;
                    }
                }
                    console.log("Table not found for id: " + tableId);
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
                return id;
            }

            function getTableForId(id) {
            for (var i = 0; i < $scope.diagramData.tables.length; i++) {
                if (id == $scope.diagramData.tables[i].data.id) {
                    return $scope.diagramData.tables[i];
                }
            }
            return null;
        }



        });

}());