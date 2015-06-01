//This handles retrieving data and is used by controllers. 3 options (server, factory, provider) with 
//each doing the same thing just structuring the functions/data differently.
var projectsRoot = '/api/branch-revisions/1/change/';
var branchRevisionRoot = '/api/branch-revisions/';

angular.module('myApp.services')
    .service('diagramService', function ($http, $q) {


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

        // *** SAVE FUNCTIONS ***
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
                "content": tableDataContent,
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
                    console.log("Table data saved successfully");
                }).error(function () {
                    console.log("Saving table data failed")
                });
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
                    console.log("Table element saved successfully");
                }).error(function () {
                    console.log("Saving element data failed")
                });
        }

        //var tables = [{data:{...}, element:{..}, dataModified, elModified }]			dataModified, elModified = true, false
        this.getTablesData = function () {
            var tablesData = [
                {data: {
                    id: "t1", name: "Table 1", "comment": "no comment", "collation": "utf-8", namespaceRef: "",
                    columns: [{
                        cdata: {
                             id:"125ca512-5c8e-4952-9c68-1f9623d5eaaa",
                             name:"userId",
                             comment:"some comment",
                             column_type:"INT"
                             // and all of column attributes
                        },
                        modified: 0
                        }
                    ], indexes: [], foreignKeys: [], schemaRef: "642c3eae-bdd9-4b80-aed1-15614d34021e"
                },
                 element: {
                        id: "e1", positionX: 100, positionY: 100, width: 300, height: 150, tableRef: "t1",
                        diagramRef: "f199449d-357e-4f6e-8190-8d0446216c3f", color: "#FFFFFF", collapsed: false
                 },
                 dataModified: 0,
                 elModified: 0,
                    //width:300,height:150,xPos:100, yPos:100,
                    attrs: []
                    //attrs:[{id:"c11", name:"Column t1_1", dataType:"INT" }]
                }
            ];

//        var tablesData = [{
//            id:"t1", title:"Table 1",width:300,height:150,xPos:100, yPos:100,
//            attrs:[]//[{id:"c11", name:"Column t1_1", dataType:"INT" },{id:"c12", name:"Column t1_2", dataType:"INT" }]
//        },{
//            id:"t2", title:"Table 2",width:300,height:150,xPos:600, yPos:100,
//            attrs:[]//[{id:"c21", name:"Column t2_1", dataType:"TEXT" },{id:"c22", name:"Column t2_2", dataType:"TEXT" }]
//        }];
            return tablesData;
        };
        this.getLinksData = function () {
            var linksData = [
                {id: "fbc3a98-64d0-4321-b387-b8f4053e1d09",
                    source: { x: 400, y: 136, tableId: "t1", attr: {id: "c11", name: "Column t1_2", dataType: "int" }},
                    target: { x: 600, y: 136, tableId: "t2", attr: {id: "c21", name: "Column t2_2", dataType: "string" }},
                    biDirection: false
                }
            ];
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


    });