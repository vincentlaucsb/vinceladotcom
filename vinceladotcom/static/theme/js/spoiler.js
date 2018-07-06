/* spoiler.js by Vincent La

Usage:
* Anything that should be revealed by the click of a spoiler button should have
    * id attribute set
    * class='spoiler'
* The associated spoiler button or buttons should have
    * class='(id of thing to be spoiled)-trigger'
        * e.g. if the thing to be revealed has id='season-2-spoilers' then 
        * button should have class='season-2-spoilers-trigger'
* No other work is needed other than including the spoiler.css file
*/

/// Text to display for spoiler triggers/buttons
var SHOW_BUTTON_TEXT = 'Show';
var HIDE_BUTTON_TEXT = 'Hide';

/*  Helper function: removes class from an element

    elem      HTML element  
    cls_name  name of class to be removed */
function removeClass(elem,cls_name) {
    // classes will be an array of class names
    var temp = elem.getAttribute('class');
    var classes = temp ? temp.split(' ') : [];
    remove_index = classes.indexOf(cls_name);
    classes.splice(remove_index, 1);
    classes = classes.join(' ');
    elem.setAttribute('class',classes);        
};

// Returns true/false if an element has class cls_name or not
function hasClass(elem,cls_name) {
    var temp = elem.getAttribute('class');
    var classes = temp ? temp.split(' ') : []; // If temp is null, set classes = empty array
    return classes.includes(cls_name);
};

function addClass(elem,cls_name) {
    var temp = elem.getAttribute('class');
    var classes = temp ? temp + " " + cls_name: cls_name;
    elem.setAttribute('class',classes);
};

// The actual function that gets called when a show/hide button is clicked
function spoil(id) {
    var elem = document.getElementById(id);
    var spoiled = hasClass(elem,'spoiler-spoiled');
    var triggers = document.getElementsByClassName(id + '-trigger');
    if (spoiled) {
        addClass(elem,'spoiler');
        removeClass(elem,'spoiler-spoiled');
        for (var i = 0; i < triggers.length; i++) {
            triggers[i].innerHTML = SHOW_BUTTON_TEXT;
        }
    } else {
        addClass(elem,'spoiler-spoiled');
        removeClass(elem,'spoiler');
        for (var i = 0; i < triggers.length; i++) {
            triggers[i].innerHTML = HIDE_BUTTON_TEXT;
        }
    }
};

// Finds all items with 'spoiler' or 'spoiler-spoiled' as a class name
// Then finds their triggers and gives them trigger functionality, i.e. sets onclick = "show('spoiler_id')"
window.addEventListener('load', function() {
    spoilers = document.getElementsByClassName('spoiler');
    wrapped = document.getElementsByClassName('spoiler-wrapped');
    spoiled = document.getElementsByClassName('spoiler-spoiled');
    
    // text: Text to make triggers display
    // spoilers: List of elements with "spoiler" or "spoiler-spoiled" as a class
    var make_button_alive = function(spoilers,button_text) {
        for (var i = 0; i < spoilers.length; i++) {
            spoiler_id = spoilers[i].getAttribute('id')
            trigger_cls_name = spoiler_id + '-trigger';
            triggers = document.getElementsByClassName(trigger_cls_name);
            
            // Add onclick = 'spoil(id)' attribute to all triggers
            for (var j = 0; j < triggers.length; j++) {
                triggers[j].setAttribute('onclick',"spoil('" + spoiler_id + "')");
                triggers[j].innerHTML = button_text;
            }
        }
    };
    
    make_button_alive(spoilers,SHOW_BUTTON_TEXT);
    make_button_alive(spoiled,HIDE_BUTTON_TEXT);
});