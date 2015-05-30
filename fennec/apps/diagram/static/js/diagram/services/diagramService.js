//This handles retrieving data and is used by controllers. 3 options (server, factory, provider) with 
//each doing the same thing just structuring the functions/data differently.
var projectsRoot = '/api/branch-revisions/1/change/';
var branchRevisionRoot = '/api/branch-revisions/';

angular.module('myApp.services')
.service('diagramService', function ($http,$q) {

    this.pythonCreateDiagramSave  = function(){
            var saveBranchRevisionURL = projectsRoot;

            var postStaf = {
               "content":{
                 "url": "",
                  "id":"83654a30-c082-42db-9c27-0b6ff5460c0b",
                  "name":"Diagram from fucking angular",
                  "description":"Diagram from fucking angular"
               },
               "objectType":"Diagram",
               "objectCode":"83654a30-c082-42db-9c27-0b6ff5460c0b",
               "changeType":0,
               "isUIChange":true,
               "made_by":"1"
            }

            $http.post(projectsRoot, postStaf).
            success(function(){
                console.log("POST success");
            }).error(function(){
                console.log("POST failed")
            });
        };



    this.loadBranchRevisionProjectState = function(branchRevisionId) {
           var url = branchRevisionRoot+branchRevisionId+"/project_state";
           console.log(url);
           return $http({method:"GET", url:url}).then(function(result){
                 return result.data;
           });
    }
    this.loadDiagramElements = function(branchRevisionId,diagramId) {
           var url = branchRevisionRoot+branchRevisionId+"/diagram?diagramId="+diagramId;
           console.log(url);
           return $http({method:"GET", url:url}).then(function(result){
                 return result.data;
           });
    }

    this.myXhr = function(branchRevisionId){
         var url = branchRevisionRoot+branchRevisionId+"/project_state";
        var deferred = $q.defer();
        $http({
            url: url,
            method: 'GET',
            headers: {'Content-Type': 'application/json'}
            })
            //if request is successful
            .success(function(data,status,headers,config){
                //resolve the promise
                deferred.resolve('request successful');
            })
            //if request is not successful
            .error(function(data,status,headers,config){
                //reject the promise
                deferred.reject('ERROR');
            });
        //return the promise
        return deferred.promise;
    }

    this.getTablesData = function () {
        var tablesData = [{
            id:"t1", title:"Table 1",width:300,height:150,xPos:100, yPos:100,
            attrs:[]//{id:"c11", name:"Column t1_1", dataType:"INT" },{id:"c12", name:"Column t1_2", dataType:"INT" }]
        },{
            id:"t2", title:"Table 2",width:300,height:150,xPos:600, yPos:100,
            attrs:[]//[{id:"c21", name:"Column t2_1", dataType:"TEXT" },{id:"c22", name:"Column t2_2", dataType:"TEXT" }]
        }];
        return tablesData;
    };
    this.getLinksData = function(){
        var linksData = [
            {id:"fbc3a98-64d0-4321-b387-b8f4053e1d09",
                source: { x:400, y:136, tableId:"t1", attr: {id:"c11", name:"Column t1_2", dataType:"int" }},
                target: { x:600, y:136, tableId:"t2", attr: {id:"c21", name:"Column t2_2", dataType:"string" }},
                biDirection: false
            }
        ];
        return linksData;
    }

    this.getTableForId = function(id){
        var tables = this.getTablesData();
        for(var i =0; i< tables.length;i++){
            if(id == tables[i].id){
                console.log("TableService-> Table found for id: "+id);
                return tables[i];
            }
        }
        return null;
    }




//    this.loadBranchRevisionProjectState = function(branchRevisionId) {
//            var url = branchRevisionRoot+branchRevisionId+"/project_state";
//            console.log(url);
//            var request = new XMLHttpRequest();
//            request.open('GET', url, false);  // `false` makes the request synchronous
//            request.responseType = 'json';
//
//            request.send();
//            if (request.status === 200) {
////                console.log("**********************");
////                console.log(request.responseType);
////                console.log(request.responseContentType);
//                console.log(request.responseText);
//                 console.log("**********************");
//                console.log(request.response);
//
//               //console.log(JSON.parse(request.responseText));
//                return request.response;
//            }
//            return null;
//    }

    this.getCustomer = function (id) {
        for (var i = 0; i < customers.length; i++) {
            if (customers[i].id === id) {
                return customers[i];
            }
        }
        return null;
    };



});