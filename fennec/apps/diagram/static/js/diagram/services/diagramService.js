//This handles retrieving data and is used by controllers. 3 options (server, factory, provider) with 
//each doing the same thing just structuring the functions/data differently.

angular.module('myApp.services')
.service('diagramService', function () {


    this.getTablesData = function () {
        var tablesData = [{
            id:"t1", title:"Table 1",width:300,height:150,xPos:100, yPos:100,
            attrs:[{id:"c11", name:"Column t1_1", dataType:"INT" },{id:"c12", name:"Column t1_2", dataType:"INT" }]
        },{
            id:"t2", title:"Table 2",width:300,height:150,xPos:600, yPos:100,
            attrs:[{id:"c21", name:"Column t2_1", dataType:"TEXT" },{id:"c22", name:"Column t2_2", dataType:"TEXT" }]
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


    this.insertCustomer = function (firstName, lastName, city) {
        var topID = customers.length + 1;
        customers.push({
            id: topID,
            firstName: firstName,
            lastName: lastName,
            city: city
        });
    };

    this.deleteCustomer = function (id) {
        for (var i = customers.length - 1; i >= 0; i--) {
            if (customers[i].id === id) {
                customers.splice(i, 1);
                break;
            }
        }
    };
























































































































































































































































































































































    this.getCustomer = function (id) {
        for (var i = 0; i < customers.length; i++) {
            if (customers[i].id === id) {
                return customers[i];
            }
        }
        return null;
    };



});