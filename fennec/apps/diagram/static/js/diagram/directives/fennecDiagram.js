(function () {
  'use strict';

  angular.module('myApp.directives')
    //.directive('d3Bars',  ['d3Service','$compile', function(d3Service,$compile) {
    .directive('fennecDiagram',  ['d3Service','$compile', function(d3Service,$compile) {
      return {
        restrict: 'EA',
        scope: {
           data: "=",
          stable: "="
        },
        template:"<div class='diagram'  ></div>",
        link: function(scope, iElement, iAttrs) {
          d3Service.then(function(d3) {
            var tablesData = scope.data.tables;
            var linksData = scope.data.links;

            var tableDefaultWidth = 300;
            var tableDefaultHeight = 150;
            var modelDefaultWidth = 2500;
            var modelDefaultHeight = 1500;
            var resizeRectSize = 16;

            scope.$watch('data.tables', function() {
              //console.log(tablesData[0].attrs);
              console.log("Dir-> changes occur on dir input table data: ");
              console.log(tablesData);
              restart(true);
            },true);

            var drag = d3.behavior.drag()
                .origin(function() {
                  var current = d3.select(this);
                  return {x: current.attr("x"), y: current.attr("y") };
                })
                .on("drag", move);

            var resize = d3.behavior.drag()
                .origin(function() {
                  var current = d3.select(this);
                  return {x: current.attr("x"), y: current.attr("y") };
                })
                .on("drag", dragResize);

            var svg;
            initSvgDiagram();
            function initSvgDiagram(){
              console.log("Init svg diagram");
              svg = d3.select(".diagram")
                  .style("outline","1px solid black")
                  .style("width","100%")
                  .style("height","100%")
                  .style("float","left")
                  .style("overflow","auto")
                  .append("svg").attr('width', modelDefaultWidth).attr('height', modelDefaultHeight).on("click", mouseClick);

              svg.append('svg:defs').append('svg:marker')
                  .attr('id', 'end-arrow')
                  .attr('viewBox', '0 -5 10 10')
                  .attr('refX', 6)
                  .attr('markerWidth', 3)
                  .attr('markerHeight', 3)
                  .attr('orient', 'auto')
                  .append('svg:path')
                  .attr('d', 'M0,-5L10,0L0,5')
                  .attr('fill', '#000');

              svg.append('svg:defs').append('svg:marker')
                  .attr('id', 'start-arrow')
                  .attr('viewBox', '0 -5 10 10')
                  .attr('refX', 4)
                  .attr('markerWidth', 3)
                  .attr('markerHeight', 3)
                  .attr('orient', 'auto')
                  .append('svg:path')
                  .attr('d', 'M10,-5L0,0L10,5')
                  .attr('fill', '#000');
            }
            var selected_table = null,
                selected_link = null,
                mousedown_link = null,
                mousedown_node = null,
                mouseup_node = null;

            function resetMouseVars() {
              mousedown_node = null;
              mouseup_node = null;
              mousedown_link = null;
            }

            //restart();
            function restart(redrawAll){
              if(redrawAll){
                d3.select(".diagram").selectAll("*").remove();
                initSvgDiagram();
              }

              // Create table links
              redrawLines();

              redrawTables();
            }
            function redrawTables(){
              // Create table with attributes
              var svgTables = svg.selectAll("g.table").data(tablesData);
              var table = svgTables.enter().append("g").classed("table", true).attr("id", function(d,i) { return "table"+i})
              table.append("rect").classed("table", true).on("click", mouseClick);
              var t = table.append("rect").classed("titleBox", true).call(drag);
              table.append("text").classed("title", true).data(tablesData);

              var attributes =  table.append("g").classed("attributes",true).selectAll("attribute").data(function(d) { return d.attrs});
              var attribute = attributes.enter().append("text").classed("attribute", true).attr("id", function(d,i) { return "attribute"+i}).on("click", mouseClick);
              table.append("rect").classed("resize-icon", true).call(resize);

              table.selectAll("rect.table")
                  .attr({
                    x: function(d) { return d.xPos; },
                    y: function(d) { return d.yPos; },
                    width: function(d) { return d.width; },
                    height: function(d) { return d.height; }
                  })

              table.selectAll("rect.titleBox")
                  .classed("drag", true)
                  .attr({
                    x: function(d) { return d.xPos; },
                    y: function(d) { return d.yPos; },
                    width: function(d) { return d.width; },
                    height: 25,
                    fill: "#ADD8E6"
                  })

              table.selectAll("text.title")
                  .attr({
                    x: function(d) { return d.xPos + 10; },
                    y: function(d) { return d.yPos+ 20; },
                    width: function(d) { return d.width; },
                    height: 25,
                    fill: "#ffffff"
                  })
                  .text(function(d) {
                    return d.title;
                  })

              // TODO: find better way than using getAttributeTableMethod
              table.selectAll("text.attribute")
                  .attr({
                    x: function(d) {
                      var table = getAttributeTable(d.id);
                      return table.xPos + 10;
                    },
                    y: function(d,i) {
                      var table = getAttributeTable(d.id);
                      return table.yPos+45+((i==0)?0:(20*i));
                    },
                    width: function(d) { return d.width; },
                    height: 25,
                    fill: "#999999"
                  })
                  .text(function(d) {
                    return d.name+ " (" + getTypeNameForValue(d.dataType)+")";
                  })

              table.selectAll("rect.resize-icon")
                  .attr({
                    x: function(d) { return d.xPos + d.width-resizeRectSize; },
                    y: function(d) { return d.yPos + d.height - resizeRectSize; },
                    width: resizeRectSize,
                    height: resizeRectSize,
                    fill: "#999999"
                  })
              svgTables.exit().remove();
            }

            //TODO: find way to skip this and pass dataType as value
            function getTypeNameForValue(dataTypeValue){

              var dataTypes =  [
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

              if(isNumber(dataTypeValue)== false){
                return dataTypeValue;
              }else{
                for(var i =0;i<dataTypes.length;i++){
                  if(dataTypes[i].value == dataTypeValue){
                    return dataTypes[i].text;
                  }
                }
              }
            }
            function isNumber(n) {
              return !isNaN(parseFloat(n)) && isFinite(n);
            }
            function getAttributeTable(attrId){
              // TODO: latter extend to check all attr just in case
              for(var i=0;i<tablesData.length;i++){
                for(var j=0;j<tablesData[i].attrs.length;j++){
                  if(tablesData[i].attrs[j].id == attrId){
                    return tablesData[i];
                  }
                }
              }
            }
            function redrawLines(){
              d3.select(".diagram").selectAll("g.link").remove();

              var svgLinks = svg.selectAll("g.link").data(linksData);
              var link = svgLinks.enter().append("g").classed("link", true);
              link.append("svg:line").classed("link",true).attr("id", function(d) { return d.id});
              link.selectAll("line.link")
                  .attr({
                    x1: function(d) { return d.source.x; },
                    y1: function(d) { return d.source.y; },
                    x2: function(d) { return d.target.x; },
                    y2: function(d) { return d.target.y; }
                  }).style("stroke", "rgb(6,120,155)").style("stroke-width", 3)
                  .style('marker-start', function(d) { return (d.biDirection==true) ? 'url(#start-arrow)' : ''; })
                  .style('marker-end', function(d) { return  'url(#end-arrow)'; });
              svgLinks.exit().remove();
            }


            var tmpSourceTableLink = null;
            var tmpTargetTableLink= null;
            function clearTmpLinks(){
              tmpSourceTableLink = null;
              tmpTargetTableLink= null;
            }

            // MOUSE EVENTS
            function mouseClick(d) {
              d3.event.stopPropagation();
              var dragTarget = d3.select(this);
              selected_table = d3.select(this.parentNode);
              var translateCoord = parseTranslateString(selected_table.attr("transform"));
              var point = d3.mouse(this)

              var mouseClickX = point[0];
              var mouseClickY = point[1];
              //console.log("mouseClick on x:"+mouseClickX+" y: "+mouseClickY);
              if(actionStates == fennecStates.new_table){
                tablesData.push({id:tablesData.length+1,
                  title:"Table"+(tablesData.length+1),
                  xPos:mouseClickX,
                  yPos:mouseClickY,
                  height:tableDefaultHeight,
                  width:tableDefaultWidth,
                  attrs:[{id:genGuid(), name:"Attribute 2", dataType:"int" }]});
                restart(true);
                innerLayout.close('south');
                changeState(fennecStates.select);
              }
              if(actionStates == fennecStates.select){
                if(selected_table != null){
                  var tableData = selected_table.node().__data__;
                  if(tableData != undefined){
                    console.log("Dir-> Table selected: "+tableData.id);
                    scope.stable = tableData;
                    scope.$apply();
                    //passing value to controller if this directive will be private (zatvoren)
                    //scope.$emit('selectedTableEvent', tableData );
                  }
                }
              }
              if(actionStates == fennecStates.delete_obj){
                if(selected_table != null){
                  var tableData = selected_table.node().__data__;
                  if(tableData != undefined){
                    console.log("Dir-> Table deleted: "+tableData.id);
                    scope.$emit('deleteTableEvent', tableData );
                  }
                }
              }
              if(actionStates == fennecStates.new_link){
                // TODO: check is link already exist between table and if exist and direction is opposite then set biDirection to true
                // TODO: link table to self
                var selectedAttributeArrays = d3.select(this);                       // [[text#attribute0.attribute]]
                var tableOfAttrArrays = d3.select(this.parentNode.parentNode);               // [[g#table0.table]]
                var tableData =tableOfAttrArrays.node().__data__;
                var attrData = selectedAttributeArrays.node().__data__;  // console.log(attrData);
                if(tmpSourceTableLink == null ){
                  tmpSourceTableLink = {x:0,y:0, table:tableData, attr:attrData};
                  return;
                }
                if(tmpTargetTableLink == null){
                  tmpTargetTableLink = {x:0,y:0, table:tableData, attr:attrData};
                }

                var linkPosition= calculateLinkPosition(tmpSourceTableLink,tmpTargetTableLink);
                tmpSourceTableLink = linkPosition.sourceTableLink;
                tmpTargetTableLink = linkPosition.targetTableLink;
                // console.log("Source("+tmpSourceTableLink.x+","+ tmpSourceTableLink.y+") Target("+tmpTargetTableLink.x+","+tmpTargetTableLink.y+")" );

                linksData.push({id:genGuid(),
                  source:{x:tmpSourceTableLink.x, y:tmpSourceTableLink.y, tableId:tmpSourceTableLink.table.id, attr:tmpSourceTableLink.attr},
                  target:{x:tmpTargetTableLink.x, y:tmpTargetTableLink.y, tableId:tmpTargetTableLink.table.id, attr:tmpTargetTableLink.attr},
                  biDirection:linkPosition.biDirection});
                clearTmpLinks();
                changeState(fennecStates.select);
                redrawLines();
              }
            }
            function calculateLinkPosition(sourceTableLink,targetTableLink){
              if(sourceTableLink.table.xPos < targetTableLink.table.xPos){
                var linkCoord = getLinkPosition(sourceTableLink.table, sourceTableLink.attr,true);
                sourceTableLink.x = linkCoord.x;
                sourceTableLink.y = linkCoord.y
                linkCoord = getLinkPosition(targetTableLink.table, targetTableLink.attr,false);
                targetTableLink.x = linkCoord.x;
                targetTableLink.y = linkCoord.y
              }else{
                // source is right table
                var linkCoord = getLinkPosition(targetTableLink.table, targetTableLink.attr,true);
                targetTableLink.x = linkCoord.x;
                targetTableLink.y = linkCoord.y
                linkCoord = getLinkPosition(sourceTableLink.table, sourceTableLink.attr,false);
                sourceTableLink.x = linkCoord.x;
                sourceTableLink.y = linkCoord.y
              }
              var result = {
                sourceTableLink: sourceTableLink,
                targetTableLink: targetTableLink
              };
              return result;
            }

            function getLinkPosition(tableData,attrData,isLinkStartOnTableRightSide){
              // isLinkStartOnTableRightSide - link start from a table right side
              var attrPositionInList = arrayObjectIndexOf(tableData.attrs,attrData.id,"id");
              // console.log("getLinkPosition() => "+attrPositionInList);
              var linkCoordinate
              if(isLinkStartOnTableRightSide){
                linkCoordinate = {
                  x: tableData.xPos + tableData.width,
                  y: tableData.yPos + 45 + (attrPositionInList*20) - (20/2-1)
                }
              }else{
                linkCoordinate = {
                  x: tableData.xPos,
                  y: tableData.yPos + 45 + (attrPositionInList*20) - (20/2-1)
                }
              }
              return linkCoordinate;
            }

            var relativeMovePosX=0;
            var relativeMovePosY=0;
            function move(){
              var resizeTableTitleArrays = d3.select(this);          // [[rect.titleBox.drag]]
              var movingTableObject = d3.select(this.parentNode);    // [[g#table0.table]]

              // console.log("d3.event.x:"+d3.event.x+" d3.event.y:"+d3.event.y);
              var startTableXPosition = parseInt(resizeTableTitleArrays.attr('x'));       // ovo je isto uvek
              var startTableYPosition = parseInt(resizeTableTitleArrays.attr('y'));       // ovo je isto uvek
              // console.log("move() => startTableXPosition: "+startTableXPosition+" startTableYPosition: "+startTableYPosition);

              relativeMovePosX += d3.event.x - startTableXPosition;
              relativeMovePosY += d3.event.y - startTableYPosition;
              //console.log("move() => relativeMovePosX:"+relativeMovePosX+" relativeMovePosY:"+relativeMovePosY);

              movingTableObject.attr("transform", "translate(" + relativeMovePosX + "," + relativeMovePosY + ")");
              updateTablePosition(movingTableObject,startTableXPosition+relativeMovePosX, startTableYPosition+relativeMovePosY);
              //var link = getLinkForTableId(movingTableObject);
              //if(link != null){
              //    var linkObjArrays = d3.select("#"+link.id);   //		[[line#id-from-link.link]]
              //    console.log(linkObjArrays);
              //    linkObjArrays.attr("transform", "translate(" + relativeMovePosX + "," + relativeMovePosY + ")");
              //}
              updateLinkPosition(movingTableObject);
            };
            function updateTablePosition(movingTableObject,x,y) {
              var tableId = movingTableObject.node().__data__.id;
              for (var i in tablesData) {
                if (tablesData[i].id == tableId) {
                  tablesData[i].xPos = x;
                  tablesData[i].yPos = y;
                  //console.log("updateTablePosition() => x: "+x+" y: "+y);
                  break;
                }
              }
            }
            function updateLinkPosition(movingTableObject){
              var redraw = false;
              var table = movingTableObject.node().__data__;
              for(var i=0;i<linksData.length;i++){
                if(linksData[i].source.tableId == table.id){
                  var tableLink = linksData[i];
                  //console.log("updateLinkPosition(movingTableObject) => link id: "+tableLink.id);
                  updateLinkData(tableLink);
                  redraw = true;
                }
                if(linksData[i].target.tableId == table.id){
                  var tableLink = linksData[i];
                  // console.log("updateLinkPosition(movingTableObject) => link id: "+tableLink.id);
                  updateLinkData(tableLink);
                  redraw = true;
                }
              }
              if(redraw) {
                redrawLines();
              }
            }
            function updateLinkData(link){
              var linkTables = findLinkTables(link.source.tableId,link.target.tableId);
              var sourceTableLink = {x:0,y:0, table:linkTables.sourceTable, attr:link.source.attr};
              var targetTableLink = {x:0,y:0, table:linkTables.targetTable, attr:link.target.attr};
              var linkPosition= calculateLinkPosition(sourceTableLink,targetTableLink);
              //console.log("updateLinkData(link) => linkId: "+link.id);
              //console.log("updateLinkData(link) before => source("+link.source.x+","+link.source.y+"), target("+link.target.x+","+  link.target.y+")");
              link.source.x = linkPosition.sourceTableLink.x;
              link.source.y = linkPosition.sourceTableLink.y;
              link.target.x = linkPosition.targetTableLink.x;
              link.target.y = linkPosition.targetTableLink.y;
              //console.log("updateLinkData(link) after update=> source("+link.source.x+","+link.source.y+"), target("+link.target.x+","+  link.target.y+")");
            }
            function findLinkTables(sourceTableId, targetTableId){
              var result = {
                sourceTable:null,
                targetTable:null
              };
              for(var i=0;i<tablesData.length;i++) {
                if(tablesData[i].id == sourceTableId){
                  result.sourceTable = tablesData[i];
                  if(result.targetTable == null){
                    continue;
                  }else{
                    break;
                  }
                }
                if(tablesData[i].id == targetTableId){
                  result.targetTable = tablesData[i];
                  if(result.sourceTable == null){
                    continue;
                  }else{
                    break;
                  }
                }
              }
              return result;
            }

            var resizeRectXPos ;
            var resizeRectYPos;
            function dragResize(){
              var resizeIconObject = d3.select(this);                 // [[rect.resize-icon]]
              var resizeTableObject = d3.select(this.parentNode);     // [[g#table0.table]]
              var resizeTableArrays = resizeTableObject.select("rect.table");                // [[rect.table]]
              var resizeTableTitleArrays = resizeTableObject.select("rect.titleBox");        // [[rect.titleBox.drag]]


              var selectedTableData = resizeTableArrays.node().__data__;
              var tableWidth = selectedTableData.width;
              var tableHeight = selectedTableData.height;

              var translateCoord = parseTranslateString(resizeTableObject.attr("transform"));
              // console.log("dragResize()=> translateCoord x: "+translateCoord.x +" , y: "+translateCoord.y);
              var resizeRectCoord = calculateResizeRectPosition(resizeTableArrays,translateCoord,tableWidth,tableHeight);
              resizeRectXPos = resizeRectCoord.x;
              resizeRectYPos = resizeRectCoord.y;
              // console.log("resize dx:"+dx+" dy:"+dy);
              // console.log("d3.event.x:"+d3.event.dx+" d3.event.y:"+d3.event.dy);

              var oldx = resizeRectXPos;
              var oldy = resizeRectYPos;

              resizeRectXPos = Math.max(0, Math.min(resizeRectXPos + modelDefaultWidth - (16 / 2), d3.event.x));
              resizeRectYPos = Math.max(0, Math.min(resizeRectYPos + modelDefaultHeight - (16 ), d3.event.y));

              resizeIconObject.attr("x", function(d) { return resizeRectXPos }).attr("y", function(d) { return resizeRectYPos })

              tableWidth = tableWidth - (oldx - resizeRectXPos) + translateCoord.x;
              tableHeight = tableHeight - (oldy - resizeRectYPos) + translateCoord.y;

              resizeTableArrays.attr("width", tableWidth).attr("height", tableHeight);
              resizeTableTitleArrays.attr("width", tableWidth);

              hideAttributesOnResize(resizeTableObject,tableWidth, tableHeight,selectedTableData.attrs);       // console.log("dragResize()=> tableHeight: "+tableHeight+" tableWidth: "+tableWidth );
              updateTableSize(selectedTableData,tableHeight,tableWidth);
              updateLinkPosition(resizeTableObject);
            };
            function calculateResizeRectPosition(resizeTableArrays,translateCoord,tableWidth,tableHeight){
              var startTableXPosition = parseInt(resizeTableArrays.attr('x'));  // this is the table first coordinates and it will not change until next reload
              var startTableYPosition = parseInt(resizeTableArrays.attr('y'));

              var tableXPos = startTableXPosition + translateCoord.x;
              var tableYPos = startTableYPosition + translateCoord.y;
              //console.log("calculateResizeRectPosition=> tableHeight: "+tableHeight + " tableWidth: "+tableWidth);
              var resizeRectXPos = tableXPos + tableWidth - resizeRectSize;
              var resizeRectYPos = tableYPos + tableHeight - resizeRectSize;
              //var resizeRectXPos = tableWidth - resizeRectSize;
              //var resizeRectYPos = tableHeight - resizeRectSize;
              //console.log("resizeRectXPos: "+resizeRectXPos+ " resizeRectYPos: "+resizeRectYPos);
              return {x:resizeRectXPos, y:resizeRectYPos};
            }
            function updateTableSize(selectedTableData,tableHeight, tableWidth){
              var tableId = selectedTableData.id;
              for (var i in tablesData) {
                if (tablesData[i].id == tableId) {
                  tablesData[i].height = tableHeight;
                  tablesData[i].width = tableWidth;
                  break;
                }
              }
            }

            function hideAttributesOnResize(resizeTableObject,tableWidth,tableHeight, tableAttributes){
              // TODO: find how to truncate text on resizing left
              // TODO: find way need to minus 100 from dragx , what is that 100 (-> (dragx-100))
              var attributesObjectsFromPage = [];
              var attrNumber =tableAttributes.length;
              //attribute0, attribute1
              for (var i = attrNumber-1; i>= 0; i--) {
                // Note: when select attribute(child element) from resizeTableObject, the data will be inherited from parent object in this case from table, we lose attribute data
                // to fix this d3 logic :), add attribute data here ( this is how d3 work, it is build to inherit all data from parent to childs because of data consistency)
                var attrObjArray = resizeTableObject.select("#attribute"+i).data($(tableAttributes[i]));
                attributesObjectsFromPage.push(attrObjArray);
              }
              for(var i=0;i<attrNumber;i++){
                var attrObjArray = attributesObjectsFromPage[i];
                // console.log(attrObjArray.node().__data__);
                var attrObject= $(attrObjArray[0]);
                var attrPos = getAttributesLocationInTable(attrObject);

                // 16 is the header of table
                //console.log("childOffset.left "+attrPos.left);
                //console.log("dragx-100 "+(dragx-100));
                attrObjArray.attr("opacity", function(d) { return (((tableWidth-100) < attrPos.left || tableHeight - 16<attrPos.top)?0:1); });
              }
            }
            function getAttributesLocationInTable(attrObject){
              var childPos = attrObject.offset();
              var parentPos = attrObject.parent().parent().offset();
              var childOffset = {
                top: childPos.top - parentPos.top  ,
                left: childPos.left - parentPos.left
              }
              return childOffset;
            }

// Moje dodato
            var lastKeyDown;

            function keydown() {
              d3.event.preventDefault();

              if(lastKeyDown !== -1) return;
              lastKeyDown = d3.event.keyCode;

              switch(d3.event.keyCode) {
                case 8: // backspace
                case 46: // delete
                  if(selected_table) {
                    tablesData.splice(tablesData.indexOf(selected_table), 1);
                  }
                  selected_table = null;
                  restart();
                  break;
                case 66: // B
                  if(selected_link) {
                    // set link direction to both left and right
                    selected_link.left = true;
                    selected_link.right = true;
                  }
                  restart();
                  break;
                case 76: // L
                  if(selected_link) {
                    // set link direction to left only
                    selected_link.left = true;
                    selected_link.right = false;
                  }
                  restart();
                  break;
                case 82: // R
                  if(selected_table) {
                    // toggle node reflexivity
                    selected_table.reflexive = !selected_table.reflexive;
                  } else if(selected_link) {
                    // set link direction to right only
                    selected_link.left = false;
                    selected_link.right = true;
                  }
                  restart();
                  break;
              }
            }

            function keyup() {
              lastKeyDown = -1;

              // ctrl
              if(d3.event.keyCode === 17) {
                circle
                    .on('mousedown.drag', null)
                    .on('touchstart.drag', null);
                svg.classed('ctrl', false);
              }
            }

            d3.select(window)
                // editable table messing with this, find way to ignore this methods on edit
                //.on('keydown', keydown)
                //.on('keyup', keyup);

// *************** HELPER FUNCTIONS **************************
            function getLinkForTableId(movingTableObject){
              // TODO: this is not good , need to set like in add links part
              var table = movingTableObject.node().__data__;
              for(var i=0;i<linksData.length;i++){
                //{id:11111, source: { x:400, y:100, tableId:0, attrId:0, attrName: "Attribute 1"}, target: { x:600, y:100, tableId:1, attrId:2, attrName: "Attribute 2"}, biDirection: true }
                if(linksData[i].source.tableId == table.id){
                  return linksData[i];
                }
                if(linksData[i].target.tableId == table.id){
                  return linksData[i];
                }
              }
              return null;
            }
            function genGuid(){
              //  id-s started with number is not recognized by d3.select function
              var id = guid();
              id = id.slice(1);
              var possible = "abcdef";
              var hexLetter = possible.charAt(Math.floor(Math.random() * possible.length))
              id = hexLetter+id;
              console.log(id);
              return id;
            }
            function parseAllTransformation (a)
            {
              var b={};
              for (var i in a = a.match(/(\w+\((\-?\d+\.?\d*,?)+\))+/g))
              {
                var c = a[i].match(/[\w\.\-]+/g);
                b[c.shift()] = c;
              }
              return b;
            }
            function parseTranslateString(trans){
              if(trans == 'undefined' || trans == null){
                return {x:0,y:0};
              }
              var translateObject = parseAllTransformation(trans);
              var resultObject = {
                x: parseInt(translateObject.translate[0]),
                y: parseInt(translateObject.translate[1])
              }
              return resultObject;
            }

            var guid = (function() {
              function s4() {
                return Math.floor((1 + Math.random()) * 0x10000)
                    .toString(16)
                    .substring(1);
              }
              return function() {
                return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
                    s4() + '-' + s4() + s4() + s4();
              };
            })();
            function arrayObjectIndexOf(myArray, searchTerm, property) {
              for(var i = 0, len = myArray.length; i < len; i++) {
                if (myArray[i][property] === searchTerm) return i;
              }
              return -1;
            }


          });
        }
      };
    }]);

}());