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
//     $('.diagram').css('cursor', "pointer");

    if(state == fennecStates.new_table){
        $('svg').css('cursor',"url(http://findicons.com/files/icons/1722/gnome_2_18_icon_theme/24/stock_draw_rectangle.png), auto");
    }

    if(state == fennecStates.new_link){
        clearTmpLinks();
    }
}

