/**
 * Created by kleba on 2/15/2015.
 */

var fennecStates = {
    select : 'select',
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

    if(state == fennecStates.new_table){
           $('svg').css('cursor',"url('/static/images/rectangle_32x32_icon.png'), auto");
    }

    if(state == fennecStates.new_link){
//        $('svg').css('cursor',"url('/static/images/link_32x32_icon.png'), auto");
        clearTmpLinks();
    }
}

