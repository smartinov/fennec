//This handles retrieving data and is used by controllers. 3 options (server, factory, provider) with 
//each doing the same thing just structuring the functions/data differently.
var projectsRoot = '/api/branch-revisions/1/change/';
var branchRevisionRoot = '/api/branch-revisions/';

angular.module('myApp.services')
    .service('diagramService', function ($http, $q) {

        // ****** LOAD FUNCTIONS ******
        this.loadBranchRevisionProjectState = function (branchRevisionId) {
            var url = branchRevisionRoot + branchRevisionId + "/project_state";
            console.log(url);
            return $http({method: "GET", url: url}).then(function (result) {
                return result.data;
            });
        }
        this.loadDiagramElements = function (branchRevisionId, diagramId) {
            var url = branchRevisionRoot + branchRevisionId + "/diagram?diagramId=" + diagramId;
            console.log(url);
            return $http({method: "GET", url: url}).then(function (result) {
                return result.data;
            });
        }

        // ****** SAVE FUNCTIONS ******
        var loggedUserId = 1;

        this.pythonCreateDiagramSave = function () {
            var saveBranchRevisionURL = projectsRoot;

            var postStaf = {
                "content": {
                    "url": "",
                    "id": "83654a30-c082-42db-9c27-0b6ff5460c0b",
                    "name": "Diagram from fucking angular",
                    "description": "Diagram from fucking angular"
                },
                "objectType": "Diagram",
                "objectCode": "83654a30-c082-42db-9c27-0b6ff5460c0b",
                "changeType": 0,
                "isUIChange": true,
                "made_by": "1"
            }

            $http.post(projectsRoot, postStaf).
                success(function () {
                    console.log("POST success");
                }).error(function () {
                    console.log("POST failed")
                });
        };
        this.saveTableData = function (branchRevisionId, tableDataContent) {
            var url = branchRevisionRoot + branchRevisionId + "/change/";
            console.log("save table data url: " + url);

            var data = {
                "content": this.createPostTableData(tableDataContent),
                "objectType": "Table",
                "objectCode": tableDataContent.id,
                "changeType": 0,
                "isUIChange": false,
                "made_by": loggedUserId
            }
            console.log("Saving table data: ");
            console.log(data);
            $http.post(projectsRoot, data).
                success(function () {
                    console.log("Table["+tableDataContent.name +", "+ tableDataContent.id +"] saved successfully");
                }).error(function () {
                    var msg = "Saving table["+tableDataContent.name +", "+ tableDataContent.id +"] failed";
                    console.log(msg);
                    throw msg;
                });
        }
        this.createPostTableData = function (tableDataContent) {
            return {
                id: tableDataContent.id,
                name: tableDataContent.name,
                "comment": tableDataContent.comment,
                "collation": tableDataContent.collation,
                namespaceRef: tableDataContent.namespaceRef,
                columns: [],
                indexes: [],
                foreignKeys: [],
                schemaRef: tableDataContent.schemaRef
            }
        }
        this.saveTableElement = function (branchRevisionId, tableElementContent) {
            var url = branchRevisionRoot + branchRevisionId + "/change/";
            var data = {
                "content": tableElementContent,
                "objectType": "TableElement",
                "objectCode": tableElementContent.id,
                "changeType": 0,
                "isUIChange": true,
                "made_by": loggedUserId
            }
            console.log("Saving table element: ");
            console.log(data);
            $http.post(projectsRoot, data).
                success(function () {
                    console.log("Table element with id:" + tableElementContent.id + " saved successfully");
                }).error(function () {
                    var msg = "Saving table element with id:" + tableElementContent.id + " failed";
                    console.log(msg);
                    throw msg;
                });
        }
        this.saveTableForeignKey = function (branchRevisionId, foreignKeyContent) {
            var url = branchRevisionRoot + branchRevisionId + "/change/";
            console.log("save foreign key data url: " + url);

            var data = {
                "content": foreignKeyContent,
                "objectType": "ForeignKey",
                "objectCode": foreignKeyContent.id,
                "changeType": 0,
                "isUIChange": false,
                "made_by": loggedUserId
            }
            console.log("Saving foreign key data: ");
            console.log(data);
            $http.post(projectsRoot, data).
                success(function () {
                    console.log("ForeignKey ["+foreignKeyContent.name +", "+ foreignKeyContent.id +"] saved successfully");
                }).error(function () {
                    var msg = "Saving foreignKey ["+foreignKeyContent.name +", "+ foreignKeyContent.id +"] failed";
                    console.log(msg);
                    throw msg;
                });
        }

        this.saveColumn = function (branchRevisionId, columnContent) {
            var url = branchRevisionRoot + branchRevisionId + "/change/";
            var data = {
                "content": columnContent,
                "objectType": "Column",
                "objectCode": columnContent.id,
                "changeType": 0,
                "isUIChange": false,
                "made_by": loggedUserId
            }
            console.log("Saving column: ");
            console.log(data);
            $http.post(projectsRoot, data).
                success(function () {
                    console.log("Column["+columnContent.name +", "+ columnContent.id +"] saved successfully");
                }).error(function () {
                    var msg = "Saving column["+columnContent.name +", "+ columnContent.id +"] failed";
                    console.log(msg);
                    throw msg;
                });
        }
        this.saveRelationshipElement = function (branchRevisionId, relationshipElementContent) {
            var url = branchRevisionRoot + branchRevisionId + "/change/";
            console.log("save relationship element url: " + url);

            var data = {
                "content": relationshipElementContent,
                "objectType": "RelationshipElement",
                "objectCode": relationshipElementContent.id,
                "changeType": 0,
                "isUIChange": true,
                "made_by": loggedUserId
            }
            console.log("Saving relationship element data: ");
            console.log(data);
            $http.post(projectsRoot, data).
                success(function () {
                    console.log("Relationship element ["+ relationshipElementContent.id +"] saved successfully");
                }).error(function () {
                    var msg = "Saving relationship element ["+ relationshipElementContent.id +"] failed";
                    console.log(msg);
                    throw msg;
                });
        }

        // ****** DELETE FUNCTIONS ******
        this.deleteTableElement = function (branchRevisionId, tableElementContent) {
            var url = branchRevisionRoot + branchRevisionId + "/change/";
            var data = {
                "content": tableElementContent,
                "objectType": "TableElement",
                "objectCode": tableElementContent.id,
                "changeType": 2,
                "isUIChange": true,
                "made_by": loggedUserId
            }
            console.log("Deleting table element: ");
            console.log(data);
            $http.post(projectsRoot, data).
                success(function () {
                    console.log("Table element with id:" + tableElementContent.id + " is deleted successfully");
                }).error(function () {
                    var msg = "Deleting table element with id:" + tableElementContent.id + " failed";
                    console.log(msg);
                    throw msg;
                });
        }
        this.deleteColumn = function (branchRevisionId, columnContent) {
            var url = branchRevisionRoot + branchRevisionId + "/change/";
            var data = {
                "content": columnContent,
                "objectType": "Column",
                "objectCode": columnContent.id,
                "changeType": 2,
                "isUIChange": false,
                "made_by": loggedUserId
            }
            console.log("Deleting column: ");
            console.log(data);
            $http.post(projectsRoot, data).
                success(function () {
                    console.log("Column["+columnContent.name +", "+ columnContent.id +"] deleted successfully");
                }).error(function () {
                    var msg = "Deleting column["+columnContent.name +", "+ columnContent.id +"] failed";
                    console.log(msg);
                    throw msg;
                });
        }

        //var tables = [{data:{...}, element:{..}, dataModified, elModified }]			dataModified, elModified = true, false
        this.getTablesData = function () {
            var tablesData = [
                {data: {
                    id: "t1", name: "Table 1", "comment": "no comment", "collation": "utf-8", namespaceRef: "",
                    columns: [
                        {
                            cdata: {
                                id: "125ca512-5c8e-4952-9c68-1f9623d5eaaa",
                                name: "userId",
                                comment: "some comment",
                                column_type: "INT"
                                // and all of column attributes
                            },
                            modified: 0
                        }
                    ], indexes: [],
                    foreignKeys: [
                        {
                            "id": "91a6b2be-9562-4413-b1dc-442d64e503ea",
                            "name": "fk_Account_Tenant",
                            "comment": null,
                            "onUpdate": 3,
                            "onDelete": 3,
                            "sourceColumn": "1111111-9562-4413-b1dc-442d64e503ea",
                            "referencedColumn": "222222-9562-4413-b1dc-442d64e503ea",
                            "tableRef": "bc5d4f7d-a9df-f88b-a3bf-ba88fa08f5d7",
                            "referencedTableRef": "b5f6a3ff-75fe-dbb8-d018-90815beef1d6"
                        }
                    ], schemaRef: "642c3eae-bdd9-4b80-aed1-15614d34021e"
                },
                element: {
                        id: "e1", positionX: 100, positionY: 100, width: 300, height: 150, tableRef: "t1",
                        diagramRef: "f199449d-357e-4f6e-8190-8d0446216c3f", color: "#FFFFFF", collapsed: false
                },
                dataModified: 0,
                elModified: 0
                }
            ];
            return tablesData;
        };
        this.getLinksData = function () {
             var linksData = [
//              Foreign key
                {fk_data: {
                      "id":"91a6b2be-9562-4413-b1dc-442d64e503ea",
                      "name":"fk_Account_Tenant",
                      "onUpdate":3, 										// 0 RESTRICT 1 CASCADE 2 SET NULL 3 NO ACTION
                      "onDelete":3,
                      "sourceColumn":"Tenant_RefID",
                      "referencedColumn":"TenantID",
                      "tableRef":"bc5d4f7d-a9df-f88b-a3bf-ba88fa08f5d7",            //id from table element
                      "referencedTableRef": "b5f6a3ff-75fe-dbb8-d018-90815beef1d6" //id from table element
                 },
//              Relationship element
                 element:{
                      "id":"f0f1df1d-6d4e-4e95-ae70-327125bf9979",
                      "startPositionX":10.0,
                      "startPositionY":10.0,
                      "endPositionX":20.0,
                      "endPositionY":20.0,
                      "drawStyle":0,
                      "cardinality":1,  // 0-one-to-one,1- one-to-many,2- many-to-one,3- many-to-many
                      "foreignKeyRef":"91a6b2be-9562-4413-b1dc-442d64e503ea",
                      "diagramRef":"f199449d-357e-4f6e-8190-8d0446216c3f"
                 },
                 dataModified: false,
                 elModified: false
                }
            ];
//            var linksData = [
//                {   id: "fbc3a98-64d0-4321-b387-b8f4053e1d09",
//                    source: { x: 400, y: 136, tableId: "t1", attr: {id: "c11" }},
//                    target: { x: 600, y: 136, tableId: "t2", attr: {id: "c21" }},
//                    biDirection: false
//                }
//            ];
            return linksData;
        }
        this.getTableForId = function (id) {
            var tables = this.getTablesData();
            for (var i = 0; i < tables.length; i++) {
                if (id == tables[i].id) {
                    console.log("TableService-> Table found for id: " + id);
                    return tables[i];
                }
            }
            return null;
        }

        // ********** HELPER METHODS ****************


    });