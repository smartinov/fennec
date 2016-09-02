/**
 * Created by kleba on 2/15/2015.
 */

var fennecStates = {
    select : 'select',
    drag: 'drag',
    new_table: 'new_table',
    new_link: 'new_link',
    delete_obj: 'delete_obj'
}

// STATE STAFFS
var actionStates = 'select';
var isKeyShortcutActive = true;
var activeColor = "#0088cc";

function changeState(state){
    this.actionStates = state;

    if(state == fennecStates.select){
        $('svg').css('cursor',"default");
    }

    if(state == fennecStates.drag){
        $('svg').css('cursor',"url('/static/images/grab_cursor.png'), auto");
    }

    if(state == fennecStates.new_table){
           $('svg').css('cursor',"url('/static/images/table_pointer.cur'), auto");
    }

    if(state == fennecStates.new_link){
        $('svg').css('cursor',"url('/static/images/link-pointer.cur'), auto");
    }

    if(state == fennecStates.delete_obj){
        $('svg').css('cursor',"url('/static/images/delete_pointer.cur'), auto");
    }
}

function changeColor(){
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    activeColor = color;
    setColor("btnColor", activeColor);
}
function setColor(btn, color) {
        var property = document.getElementById(btn);
        property.style.backgroundColor = color;
}

