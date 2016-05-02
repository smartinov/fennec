(function () {
    'use strict';

    var module = angular.module('myApp.controllers')
        .controller('DiagramController', function ($scope, $filter ,$location,$log,
                                                   diagramService, spinnerService,Notification) {

            init();
            function init() {
                $scope.projectInfo = {};
                $scope.schemas = [];
                $scope.activeSchema = {};
                $scope.openedDiagrams = [];
                $scope.closedDiagrams = [];

                var absoluteURL = $location.$$absUrl;
                var branchRevisionId = absoluteURL.substr(absoluteURL.lastIndexOf('/') + 1);
                $scope.branchRevisionId = branchRevisionId;  // app/diagram/branches/1/revisions/1
                clearDiagramSpecificsScopes();
                clearDeletedScopes();

                $log.debug("ctrl-> fetching data from server for brevision:" + $scope.branchRevisionId);
                loadBranchRevisionProjectAndDiagram($scope.branchRevisionId);
            }
            function clearDiagramSpecificsScopes() {
                $log.debug("ctrl-> clearing diagram specifics scopes");

                $scope.diagramData= {tables: [], links: []};
                $scope.selectedTable = null;
                clearTableSpecificScopes();
            }
            function clearTableSpecificScopes(){
                $scope.selectedTableForeignKeys = [];
                $scope.selectedTableForeignKeyColumns=[]; // refIndexColumns - it contain only columns which are indexed
                $scope.selectedTableIndexes = [];
                $scope.indexColumns = [];
                $scope.selectedIndexComment = "";
            }
            function clearDeletedScopes(){
                $log.debug("ctrl-> clearing deleted scopes");
                $scope.deletedTableElements = []; // for now only deleting table elements
                $scope.deletedColumnsData = [];
                $scope.deletedLinks = [];
                $scope.deletedIndexes = [];
            }


            // ****** TAB HANDLER ******
            $scope.selectedDiagram = 0; //set selected tab to the 1st by default.
            $scope.addDiagram = function () {
                if($scope.activeDiagram!=undefined && confirm("You are going to create new diagram, save changes on ["+$scope.activeDiagram.data.name+"] diagram") == true) {
                    // save current diagram
                    $scope.saveDiagramButton();
                }
                var extNewDiagramInfo = {data:{id:genGuid(),name:"new diagram",description:"description",url:""},modified:true};
                $scope.openedDiagrams.push(extNewDiagramInfo);
                $scope.selectedDiagram = $scope.openedDiagrams.length - 1; //set the newly added tab active.

                // clear scopes from previous diagram and set new diagram to active
                clearDiagramSpecificsScopes();
//                this was before $scope.activeDiagram = angular.copy(extNewDiagramInfo);
                $scope.activeDiagram = extNewDiagramInfo;
            }
            $scope.closeDiagram = function (index, closingDiagram) {
                $scope.closedDiagrams.push(closingDiagram);
                $scope.openedDiagrams.splice(index, 1); // remove the object from the array based on index

                // if active diagram is closing
                if ($scope.selectedDiagram == index) {
                    clearDiagramSpecificsScopes();
                    // if there are more open diagrams (tabs) select another
                    if ($scope.openedDiagrams.length > 0) {
                        $scope.selectDiagram(0); // select first diagram tab
                    }
                }
            }
            $scope.selectDiagram = function (index) {
                if($scope.activeDiagram!=undefined && confirm("You are going to move to another diagram, save changes on ["+$scope.activeDiagram.data.name+"] diagram") == true) {
                    // save current diagram
                    $scope.saveDiagramButton();
                }

                $scope.selectedDiagram = index;
                clearDiagramSpecificsScopes();

                loadBranchRevisionProjectAndDiagram($scope.branchRevisionId, $scope.openedDiagrams[index].data.id, true);
            }


            // ******* LOAD FUNCTIONS *******
            function loadBranchRevisionProjectAndDiagram(branchRevisionId, diagramId, isTabChange) {
                spinnerService.showSpinner();
                var projectStateRequest = diagramService.loadBranchRevisionProjectState(branchRevisionId);
                projectStateRequest.then(function (branchRevisionData) {
                    //$log.debug(result);
                    if (diagramId == undefined) {
                        if (branchRevisionData.diagrams.length > 0) {
                            diagramId = branchRevisionData.diagrams[0].id;
                        }
                    }
                    var diagramRequest = diagramService.loadDiagramElements(branchRevisionId, diagramId);
                    diagramRequest.then(function (diagramElements) {
                        if(isTabChange == undefined || isTabChange == false){
                            createDiagramsInfoForTabs(branchRevisionData, diagramId);
                        }
                        prepareDiagramData(branchRevisionData, diagramElements, diagramId);
                        spinnerService.hideSpinner();
                    });
                });
                projectStateRequest.catch(function (error) {
                    $log.debug("ERROR: LoadBranchRevisionProjectState");
                    var errorMsg = "ERROR: LoadBranchRevisionProjectState->Loading diagram (branchRevisionId:'" + branchRevisionId + "') Status: " + error.status + " msg :" + error.data.detail + " (requested url:" + error.config.url + ")";
                    $log.debug(errorMsg);
                    alert("Error loading diagram! \n\nStatus: " + error.status + " Msg :" + error.data.detail + "\n\nClick to redirect on dashboard");
                    var dashboardURL = window.location.protocol + "//" + window.location.host + "/app/dashboard";
                    window.location.replace(dashboardURL);
                });
                projectStateRequest.finally(function (nesto) {
                    //$log.debug("log loadBranchRevisionProjectStatefinally");
                });
            }
            $scope.ifPrimarySetAsUnique = function(primary, column){
                if(primary){
                    column.unique = true;
                }
            }
            function createDiagramsInfoForTabs(branchRevisionData, diagramId) {
                // ADD DIAGRAMS info (name,description) to scope for tabs
                for (var i= 0, len=branchRevisionData.diagrams.length;i<len; i++) {
                    var extDiagram = {data: branchRevisionData.diagrams[i], modified: false};
                    $scope.openedDiagrams.push(extDiagram);
                }
                $log.debug("Diagrams: ");
                $log.debug($scope.openedDiagrams);
            }

            function prepareDiagramData(branchRevisionData, diagramElements, diagramId) {
                $log.debug(branchRevisionData);
                $log.debug(diagramElements);
                // ADD PROJECT INFO to scope
                $scope.projectInfo = branchRevisionData.project;
                $log.debug("ProjectInfo: ");
                $log.debug($scope.projectInfo);

                if (diagramId == undefined) {
                    $scope.activeDiagram = $scope.openedDiagrams[0];
                }else{
                    for (var i = 0,len=$scope.openedDiagrams.length; i < len; i++) {
                        var extDiagram = $scope.openedDiagrams[i];
                        if (diagramId == extDiagram.data.id) {
                            $log.debug("Active diagram:" + extDiagram.data.name);
                            $scope.activeDiagram = extDiagram;
                        }
                    }
                }

                // ADD SCHEMAS to scope
                setSchemasAndCreateDataToDisplay(branchRevisionData, diagramElements);
                $log.debug("Front diagram data:");
                $log.debug($scope.diagramData);
            }
            function setSchemasAndCreateDataToDisplay(branchRevisionData, diagramElements) {
                // Load all data with project_state and then load diagram elements and bound the two together
                $scope.schemas = [];

                for (var i= 0,len= branchRevisionData.schemas.length; i<len;i++) {
                    // SET SCHEMAS
                    var schema = {  data:{
                                        id: branchRevisionData.schemas[i].id,
                                        databaseName: branchRevisionData.schemas[i].databaseName,
                                        comment: branchRevisionData.schemas[i].comment,
                                        collation: branchRevisionData.schemas[i].collation,
                                        namespaces: branchRevisionData.schemas[i].namespaces
                                    },
                                    modified: false
                                };
                    $scope.schemas.push(schema);

                    // SET DIAGRAM TABLES
                    for (var j= 0, jLen= branchRevisionData.schemas[i].tables.length;j<jLen; j++) {
                        var dataTable = branchRevisionData.schemas[i].tables[j];

                        // CHECK IF TABLE EXISTS ON CURRENT DIAGRAM
                        for (var k= 0, kLen =  diagramElements.tableElements.length; k<kLen;k++) {
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
                                for (var l= 0, lLen=dataTable.columns.length;l<lLen;l++) {
                                    columns.push({
                                        cdata: dataTable.columns[l],
                                        modified: false
                                    });
                                }
                                table.data.columns = sortTableColumns(columns);

                                // IF foreignKeys EXISTS on table data CHECK ON DIAGRAM AND CREATE LINK
                                for (var l= 0, lLen= dataTable.foreignKeys.length;l<lLen; l++) {
                                    var foreignKey = dataTable.foreignKeys[l];
                                    for(var m= 0, mLen = diagramElements.relationshipElements.length;m<mLen; m++){
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

                                // Indexes
                                if (dataTable.indexes.length > 0) {
                                    var tableExtendedIndexes = [];
                                    for (var l= 0, lLen = dataTable.indexes.length;l<lLen; l++) {
                                        var indexData = dataTable.indexes[l];
                                        indexData.columns = JSON.parse(indexData.columns); // need to convert to list i got it like string from server
                                        var extendedIndex = {
                                            data: indexData,
                                            modified: false,
                                            new: false
                                        };
                                        tableExtendedIndexes.push(extendedIndex);
                                    }
                                    table.data.indexes=tableExtendedIndexes;
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
            function sortTableColumns(columns){
                return columns.sort(function(a, b) {
                    var textA = a.cdata.ordinal;
                    var textB = b.cdata.ordinal;
                    return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
                });
            }

            // ******* OPEN/SAVE/EDIT DIAGRAM *******
            $scope.isOpenDiagramPopupShown = false;
            $scope.showOpenDiagramPopup = function(){
                $scope.isOpenDiagramPopupShown = true;
                $scope.openDiagramData = {data:""};
            }
            $scope.openDiagram = function () {
                $scope.isOpenDiagramPopupShown = false;
                $scope.openedDiagrams.push($scope.openDiagramData.data);
                // remove diagram from closed diagram
                for(var i= 0,len =$scope.closedDiagrams.length;i<len; i++){
                    var diagram = $scope.closedDiagrams[i];
                    if(diagram.data.id == $scope.openDiagramData.data.data.id){
                        $scope.closedDiagrams.splice(i,1);
                    }
                }

                // select the opening diagram as active
                $scope.selectDiagram($scope.openedDiagrams.length-1);
            }
            $scope.cancelDiagramPopup = function(){
                $scope.isOpenDiagramPopupShown = false;
            }

            $scope.saveDiagramButton = function () {
                if(confirm("You are going to save diagram ["+$scope.activeDiagram.data.name+"], are you sure?") == false) {return;}

                $log.debug("Saving diagram["+$scope.activeDiagram.data.name+"] be patient..");
                var success = true;
                try{
                var branchRevisionId = $scope.branchRevisionId;

                // save new schemas
                for(var i= 0, len = $scope.schemas.length; i<len; i++){
                    if($scope.schemas[i].modified){
                        diagramService.saveSchema(branchRevisionId,$scope.schemas[i].data);
                    }
                }

                // save diagram data change
                if($scope.activeDiagram.modified){
                    diagramService.saveDiagramInfo(branchRevisionId,$scope.activeDiagram.data);
                }

                // save/update table
                for (var i= 0, len = $scope.diagramData.tables.length; i<len; i++) {
                    var table = $scope.diagramData.tables[i];

                    if (table.dataModified) {
                        diagramService.saveTableData(branchRevisionId, table.data);
                        table.dataModified = false; // reset it
                    }
                    if (table.elModified) {
                        diagramService.saveTableElement(branchRevisionId, table.element);
                        table.elModified = false; // reset it
                    }

                    for(var j= 0, jLen=table.data.columns.length; j<jLen; j++){
                        // var column = table.data.columns[(table.data.columns.length-1)-j]; // colak from back is saving columns to database
                        var column = table.data.columns[j]; // colak from back is saving columns to database
                        if(column.modified){
                            diagramService.saveColumn(branchRevisionId,column.cdata);
                            column.modified = false; // reset it
                        }
                    }

                    // save indexes
                    for(var k= 0,kLen = table.data.indexes.length; k<kLen; k++){
                        var index = table.data.indexes[k];
                        if(index.modified){
                            diagramService.saveIndex(branchRevisionId,index.data);
                            index.modified = false;
                        }
                    }
                }

                // save/update foreignKeys and relationElements
                for(var i= 0, len = $scope.diagramData.links.length; i<len; i++){
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
                for(var i= 0, len = $scope.deletedTableElements.length; i<len; i++){
                    var delTableElement = $scope.deletedTableElements[i];
                    diagramService.deleteTableElement(branchRevisionId, delTableElement);
                }

                // delete columns
                for(var i= 0, len= $scope.deletedColumnsData.length;i<len; i++){
                    var delColumnData = $scope.deletedColumnsData[i];
                    diagramService.deleteColumn(branchRevisionId, delColumnData);
                }

                // delete foreign keys
                for(var i= 0, len = $scope.deletedLinks.length; i<len; i++){
                    var link = $scope.deletedLinks[i];
                    diagramService.deleteTableForeignKey(branchRevisionId, link.fk_data);
                    diagramService.deleteRelationshipElement(branchRevisionId, link.element);
                }

                // delete indexes
                for(var i= 0, len =$scope.deletedIndexes.length;i<len;i++){
                    var index = $scope.deletedIndexes[i];
                    diagramService.deleteIndex(branchRevisionId, index.data);
                }

                }catch (err){
                    success = false;
                    $log.debug("Saving diagram["+$scope.activeDiagram.data.name+"] failed with msg:"+err);
                    Notification.error("Saving diagram["+$scope.activeDiagram.data.name+"] failed with msg:"+err);
                }
                if(success){
                    $log.debug("Diagram["+$scope.activeDiagram.data.name+"] content saved successfully");
                    clearDeletedScopes();
                    Notification.success("Diagram["+$scope.activeDiagram.data.name+"] content saved successfully");
                }
            }

            $scope.setTableToModified = function(selectedTable){
                selectedTable.dataModified = true;
            }
            $scope.$on('deleteTableEvent', function (scope, deletedTable) {
                deleteTableElement(deletedTable.data.id, $scope.diagramData.tables);

                // when select the table this method is called
                if ($scope.selectedTable != null && $scope.selectedTable.data.id == deletedTable.data.id) {
                     $scope.selectedTable = null;
                }
                $scope.$apply();
            });
            // ****** INDEX TAB - LEFT ******
            $scope.indexTypes =["PRIMARY","INDEX","UNIQUE"];
            $scope.addIndex = function () {
                var tableDataId = $scope.selectedTable.data.id;
                $scope.inserted = {
                    data: {
                        id: genGuid(),
                        name: "index",
                        comment: "",
                        type: "INDEX",
                        columns: [],
                        tableRef: tableDataId
                    },
                    modified: true,
                    new: true
                };
                var tableIndex = findTablePositionInArray(tableDataId, $scope.diagramData.tables);
                if (tableIndex != null) {
                    $scope.diagramData.tables[tableIndex].data.indexes.push($scope.inserted);
                }
                $log.debug("ctrl-> new index initialized");
            };
            $scope.deleteIndex = function(deletedExtendedIndex, selectedTableIndexes){
                for(var i= 0, len = selectedTableIndexes.length;i<len;i++){
                    var index = selectedTableIndexes[i];
                    if(deletedExtendedIndex.data.id == index.data.id){
                        selectedTableIndexes.splice(i,1);
                        if(deletedExtendedIndex.new == false){
                            $scope.deletedIndexes.push(deletedExtendedIndex);
                        }
                        break;
                    }
                }
                $log.debug("index successfully deleted");
            }
            $scope.showIndexColumns = function(extendedIndex){
                $log.debug(extendedIndex);
                $scope.selectedIndexComment = extendedIndex.data.comment;

                var table = getTableForId(extendedIndex.data.tableRef);
                $scope.indexColumns = {extendedIndex:extendedIndex,columns:[]};
                for(var i= 0, len = table.data.columns.length; i<len; i++){
                    var column = table.data.columns[i];
                    var indexColumn = {id: column.cdata.id, name: column.cdata.name, selected: false};
                    if(extendedIndex.data.columns.length>0) {
                        for (var j= 0, jLen = extendedIndex.data.columns.length;j<jLen; j++) {
                            if(extendedIndex.data.columns[j] == column.cdata.id){
                                 indexColumn.selected = true;
                            }
                        }
                    }
                    $scope.indexColumns.columns.push(indexColumn);
                }
            }

            // ****** INDEX TAB - RIGHT ******
            $scope.saveChangesOnIndexColumns = function(extendedIndex,selectedIndexComment){
                for(var i= 0, len=$scope.indexColumns.columns.length;i<len;i++){
                    var column = $scope.indexColumns.columns[i];
                    if(column.selected){
                        extendedIndex.data.columns.push(column.id);
                    }else{
                        // remove if not selected
                        for(var j = extendedIndex.data.columns.length-1; j>=0;j--){
                            var columnId = extendedIndex.data.columns[j];
                            if(columnId == column.id){
                                extendedIndex.data.columns.splice(j, 1);
                            }
                        }
                    }
                    extendedIndex.modified = true;
                }

                extendedIndex.data.comment= selectedIndexComment;
                Notification.success("Index column changed successfully");
            }


            // ****** FOREIGN KEY TAB - LEFT ******
            $scope.editForeignKeyName = function(data,foreignKey){
                foreignKey.data.name = data.fkName;
                foreignKey.data.dataModified = true;
            }
            $scope.showForeignKeyColumns = function(selectedForeignKey){
                //selectedForeignKey {data:foreignKey, table:table};
                $scope.selectedTableForeignKeyColumns=[{foreignKey:{}, sourceColumn:{},refIndexColumns:[]}];// refIndexColumns - it contain only columns which are indexed

                var sourceTable = getTableForId(selectedForeignKey.data.fk_data.tableRef);
                var column= getColumnForId(selectedForeignKey.data.fk_data.sourceColumn, sourceTable.data.columns);
//                var refColumn= getColumnForId(selectedForeignKey.data.fk_data.referencedColumn, selectedForeignKey.table.data.columns);

                // TODO: get indexes for referenced table and then found columns
                // TODO: for now show all column
                var referencedTableIndexColumns = selectedForeignKey.refTable.data.columns;

                $scope.selectedTableForeignKeyColumns = [{foreignKey:selectedForeignKey.data, sourceColumn:column,refTable:selectedForeignKey.refTable, refIndexColumns:referencedTableIndexColumns}];
                $log.debug( $scope.selectedTableForeignKeyColumns);
//                $log.debug(column.cdata.name);
//                $log.debug(refColumn.cdata.name);
            }
            $scope.deleteReferencedKey = function(foreignKey,foreignKeys){
                $log.debug("Delete referenced key with name:"+foreignKey.data.fk_data.name);
                // delete foreign key from links
                deleteColumnLink(foreignKey.data.fk_data.sourceColumn, $scope.diagramData.links);

                // foreign key tab has own list delete from it
                for(var i= 0,len=foreignKeys.length;i<len;i++){
                    var fk = foreignKeys[i];
                    if(fk.data.fk_data.id == foreignKey.data.fk_data.id){
                        foreignKeys.splice(i,1);
                        break;
                    }
                }
            }
            // ****** FOREIGN KEY TAB - SELECTED DETAILS ******
            $scope.showReferencedColumnName = function (refColumnId,refIndexColumns) {
                if(refColumnId == undefined){
                    return "Not selected";
                }
                for(var a= 0, len=refIndexColumns.length;a<len;a++){
                    var column = refIndexColumns[a];
                    if(refColumnId == column.cdata.id){
                        return column.cdata.name;
                    }
                }
                return "Not selected";
            };
            $scope.recal = "";
            $scope.saveReferencedKeyDetails = function(data,fkDetails){
                fkDetails.foreignKey.dataModified = true;
                fkDetails.foreignKey.elModified = true;
                fkDetails.foreignKey.fk_data.comment = data.comment;
                updateTableLinks(fkDetails.refTable);
            }
            function updateTableLinks(table){
                // this actually work buy double binding with directive
                $scope.recal = table;
            }


             // ********* REMOVE TABLE *********
            function deleteTableElement(tableId, tables) {
                for (var i = 0, len=tables.length; i < len; i++) {
                    if (tables[i].data.id === tableId) {
                        $log.debug("ctrl -> table[" + tables[i].data.name + "] is deleted");
                        $scope.deletedTableElements.push(tables[i].element);
                        tables.splice(i, 1);
                        break;
                    }
                }
                deleteTableLinks(tableId,$scope.diagramData.links);
            }
            function deleteTableLinks(tableId, diagramLinks) {
                for(var i = diagramLinks.length-1; i>=0;i--){
                    var link = diagramLinks[i];  // contain fk_data, element and dataModified, elModified
                    if (link.fk_data.tableRef == tableId || link.fk_data.referencedTableRef == tableId) {
                        $log.debug("ctrl -> link[" + link.fk_data.name + "] is deleted");
                        var exists = checkIfForeignKeyExistsOnBack(link.fk_data.tableRef,link.fk_data.id);
                        if(exists) {
                            $log.debug("FK exist on server add to delete");
                            $scope.deletedLinks.push(link);
                        }
                        diagramLinks.splice(i, 1);
                    }
                }
            }

            // ********* ADD/EDIT COLUMN *********
            $scope.addColumn = function () {
                var tableDataId = $scope.selectedTable.data.id;
                var tableCollation = $scope.selectedTable.data.collation;
                var ordinal = $scope.selectedTable.data.columns.length+1;
                $log.debug("Selected table id: " + tableDataId);
                $scope.inserted = {
                    cdata: {
                        id: genGuid(),
                        name: "column",
                        comment: "add some comment",
                        column_type: "INT",
                        length: 150,
                        precision: 0.0,
                        default: "default",
                        collation: tableCollation,
                        ordinal: ordinal,
                        primary: false,
                        nullable: false,
                        unique: false,
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
                $log.debug("ctrl-> new column initialized");
            };
            $scope.saveColumn = function (data, columnId) {
                var tableId = $scope.selectedTable.data.id;
                var tableIndex = findTablePositionInArray(tableId, $scope.diagramData.tables);
                var selectedTableColumns = $scope.diagramData.tables[tableIndex].data.columns;
                var column = getColumnForId(columnId, selectedTableColumns);
                column.cdata.column_type = data.column_type;
                column.modified = true;

                // TODO: create index or if there already primary key that bound to that index
                // TODO: primary key index (primary:primary) columns checked (primary cannot be deleted only when column is deleted )

                $log.debug("Column: " + data.name + " ordinal: " + column.cdata.ordinal);
                $log.debug("Column successfully saved");
            };
            function getColumnForId(columnId, columns) {
                for (var i = 0, len = columns.length; i < len; i++) {
                    if (columns[i].cdata.id == columnId) {
                        return columns[i];
                    }
                }
            }

            // ********* MOVE COLUMN IN TABLE *********
            $scope.moveColumnUp = function(column, columns){
                $log.debug("ctrl-> move up");
                if(column.cdata.ordinal==1){
                    // if first we cannot move it up
                    return;
                }

                var indexA = column.cdata.ordinal-1;
                var indexB = column.cdata.ordinal-2;
                columns = swapColumnsAndUpdateOrdinals(columns, indexA, indexB);

                for(var i= 0, len=columns.length; i < len; i++){
                    console.log(columns[i].cdata.name+" ordinal:");
                    console.log(columns[i].cdata.ordinal);
                }
            }
            $scope.moveColumnDown = function(column, columns){
                $log.debug("ctrl-> move down");

                if(column.cdata.ordinal==columns.length){
                    // if last we cannot move it up
                    return;
                }

                var indexA = column.cdata.ordinal-1;
                var indexB = column.cdata.ordinal;
                columns = swapColumnsAndUpdateOrdinals(columns, indexA, indexB);

                for(var i= 0, len = columns.length; i < len; i++){
                    $log.debug(columns[i].cdata.name+" ordinal:");
                    $log.debug(columns[i].cdata.ordinal);
                }
            }
            function swapColumnsAndUpdateOrdinals(arr, indexA, indexB) {
                var aOrdinal =  arr[indexA].cdata.ordinal;
                var bOrdinal = arr[indexB].cdata.ordinal;

                var temp = arr[indexA];
                arr[indexA] = arr[indexB];
                arr[indexB] = temp;

                arr[indexA].cdata.ordinal = aOrdinal;
                arr[indexA].modified = true;
                arr[indexB].cdata.ordinal = bOrdinal;
                arr[indexB].modified = true;

                // update link position if table has ref id
                var table = getTableForId(arr[indexA].cdata.tableRef);
                updateTableLinks(table);
                return arr;
            };


            // ********* REMOVE COLUMN *********
            $scope.removeTableColumn = function (index) {
                // delete links if exists
                var columnData = $scope.selectedTable.data.columns[index].cdata;
                deleteColumnLink(columnData.id, $scope.diagramData.links);

                // remove column from table
                $scope.selectedTable.data.columns.splice(index, 1);
                updateColumnsOrdinal($scope.selectedTable.data.columns);

                $scope.deletedColumnsData.push(columnData);
                $log.debug("ctrl -> column[" + columnData.name + "] successfully deleted");
            };
            function updateColumnsOrdinal(columns){
                for(var i = 0, len = columns.length ; i< len; i++){
                    var column = columns[i];
                    column.cdata.ordinal = i + 1;
                    $log.debug("Column:"+column.cdata.name+" ordinal: "+column.cdata.ordinal);
                }
            }
            function deleteColumnLink(columnId, diagramLinks) {
                 for(var i = diagramLinks.length-1; i>=0;i--){
                    var link = diagramLinks[i];  // contain fk_data, element and dataModified, elModified
                    if (link.fk_data.sourceColumn == columnId  || link.fk_data.referencedColumn == columnId) {
                        $log.debug("ctrl -> link[" + link.fk_data.name + "] is deleted");

                        var exists = checkIfForeignKeyExistsOnBack(link.fk_data.tableRef,link.fk_data.id);
                        if(exists) {
                            $log.debug("FK exist on server add to delete");
                            $scope.deletedLinks.push(link); //if not exists on back no need to send delete request to the back
                        }
                        diagramLinks.splice(i, 1);
                    }
                }
            }

            // ********* CREATE SCHEMA *********
            $scope.isCreateSchemaPopupShown = false;
            $scope.showCreateSchemaPopup = function(){
                $scope.isCreateSchemaPopupShown = true;
                $scope.newSchema = {id:genGuid(),databaseName:"",collation:""};
            }
            $scope.createSchemaOk = function(){
                $scope.schemas.push({data:$scope.newSchema,modified: true});
                $scope.isCreateSchemaPopupShown = false;
                if($scope.schemas.length == 1){
                    showCurrentSchemaInDropDown($scope.schemas[0].data);
                }
            }
            $scope.createSchemaCancel = function(){
                $scope.isCreateSchemaPopupShown = false;
            }
            function showCurrentSchemaInDropDown(schemaData) {
                  $scope.activeSchema = schemaData;
            }

            // ********* GET SCHEMA **************
            $scope.getSchemaName = function(schemaId){
                if(schemaId == undefined) return;
                var schemaArray = $filter('filter')($scope.schemas, schemaId); // return array
                return schemaArray.length ? schemaArray[0].data.databaseName : 'Not set';
            }

            // ******** THIS CONTROLLER UTIL FUNCTION ********
            function findTablePositionInArray(tableId, tables) {
                for (var i = 0, len = tables.length; i < len; i++) {
                    if (tables[i].data.id == tableId) {
                        return i;
                    }
                }
                    $log.debug("Table not found for id: " + tableId);
                return null;
            }
            $scope.columnTypes = ['ID', 'RefID', 'TEXT', 'INT', 'BIGINT','DECIMAL','DOUBLE','FLOAT','TINYINT','BOOL','BOOLEAN'];

            // remove not necessary scopes for foreign key and index tab
            $scope.$watch('selectedTable', function(newValue,oldValue) {
                if($scope.selectedTable == null){
                    clearTableSpecificScopes();
                }

                 if(oldValue!=null && newValue!=null && newValue.data.id !== oldValue.data.id){
                       $scope.indexColumns = [];
                       $scope.selectedIndexComment = "";
                       $scope.selectedTableForeignKeyColumns=[]; // refIndexColumns - it contain only columns which are indexed
                 }
            },true);

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
            function checkIfForeignKeyExistsOnBack(sourceTableId, foreignKeyId){
                // it will check the source table fks
                var table = getTableForId(sourceTableId);
                if(table == null){
                    $log.debug("Could not found table for id:"+sourceTableId);
                    return false;
                }
                for(var i= 0, len = table.data.foreignKeys.length;i<len;i++){
                    var fkData =table.data.foreignKeys[i];
                    if(fkData.id == foreignKeyId){
                        return true;
                    }
                }
                return false;
            }
            function getTableForId(id) {
            for (var i = 0, len=$scope.diagramData.tables.length; i < len; i++) {
                if (id == $scope.diagramData.tables[i].data.id) {
                    return $scope.diagramData.tables[i];
                }
            }
            return null;
        }



        });

}());