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

