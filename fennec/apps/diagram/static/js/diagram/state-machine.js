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

    if(state == fennecStates.new_link){
        clearTmpLinks();
    }
}

