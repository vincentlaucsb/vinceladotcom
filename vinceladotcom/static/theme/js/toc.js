/* Also see: tutorial.css for relevant CSS code */

//// Helper Functions
function addClass(elem,cls_name) {
    var temp = elem.getAttribute('class');
    var classes = temp ? temp + " " + cls_name: cls_name;
    elem.setAttribute('class',classes);
};

// Return position of elem top relative to top of page
function relYPos(elem,side="top") {
    if (elem == null) {
        return 0;
    } else { 
        var body = document.getElementsByTagName("body")[0];
        var body_ypos = body.getBoundingClientRect()["top"];
        var elem_ypos = elem.getBoundingClientRect()[side];
        return elem_ypos - body_ypos;
    }
};

//// Some Global Constants (will all be defined on page load)
var HEADERS_LIST = null;
var TOC = null;
var TOC_REL_YPOS = null;
    
//// Section 1: Make menu change styles when user scrolls past a certain point
var toc_repositioned = false;

function menuFade(scroll_pos) {
    //// Table of Contents Special Effects 
    if (scroll_pos > TOC_REL_YPOS && window.innerWidth >= 900) { // Change style if we have scrolled past the desired point
        if (toc_repositioned == false) { // Make sure the style has not yet been changed
            menuPosition(scroll_pos);          
            toc_repositioned = true;
        }
    } else { // Default resting position
        if (toc_repositioned == true) {
            TOC.setAttribute('style','');
            toc_repositioned = false;
        }
    }
};

// Change menu position when user resizes web page
function menuPosition(scroll_pos) {
    var toc_list = document.getElementById("toc-list");
    var toc_list_button = document.getElementById("toc-list-trigger");

    if (window.innerWidth < 900) {
        // Remove Table of Contents
        TOC.setAttribute('style','');
    } else {
        TOC.setAttribute('style','position: fixed; top: 0; background-color: rgba(255,255,255,0);');
    }
}

//// Highlight item in table of contents if we are in that section    
//  Steps:
//  0) Initialize currently_highlighted to null
//  1) Find the next potential items to be highlighted
//   - Find the currently highlighted header
//   - The next item could be the header before or the header after the currently highlighted header
//  2) If scroll position exceeds position of next item, highlight that item
//   - Then go back to step 1

// Initialize variables
var current_hl = null;
var current_hl_top = 0;
var current_toc_hl = null;

function tocHighlight(scroll_pos) { 
    /// Step 1: Get items to higlight
    // Get previous header to highlight (if user scrolls up)
    var getPrevHl = function() {
        // null check: If current_hl is null, return null
        if (current_hl != null) {
            for (var i = 0; i < HEADERS_LIST.length; i++) {
                if (HEADERS_LIST[i] == current_hl) {
                    return HEADERS_LIST[i-1]; 
                }
            }
        }
        return null; // End of list
    };

    // Get next header to highlight (if user scrolls down)
    var getNextHl = function() {
        // null check: If current_hl is null, return first header
        if (current_hl != null) { 
            for (var i = 0; i < HEADERS_LIST.length; i++) {
                if (HEADERS_LIST[i] == current_hl) {
                    return HEADERS_LIST[i+1]; 
                }
            }
            return null; // End of list
        } else {
            return HEADERS_LIST[0];
        }
    };
     
    prev_hl = getPrevHl();
    prev_hl_top = relYPos(prev_hl);

    next_hl = getNextHl();
    next_hl_top = relYPos(next_hl);
    
    /// Step 2: Highlight
    var highlight = function(target) {
        // Case 1: If next or previous item does not exit, merely unhighlight current item.
        //  - Set current item to null
        // Case 2: If next/prev item does exist, also highlight
        
        // Highlight TOC item
        if (target != null) {
            // URL IDs are in the form 0-link, 1-link, ...
            var toc_hl_id = target.getAttribute('id') + '-link';
            var toc_hl = document.getElementById(toc_hl_id);
            toc_hl.setAttribute('style','font-weight: bold');
        }
        
        // Unhighlight current item
        current_hl = target;
        if (current_toc_hl != null) { 
            current_toc_hl.setAttribute('style','');
        }
        
        // Back to Step 1: Find next items to highlight
        current_toc_hl = toc_hl;
        current_hl_top = relYPos(current_hl);
    }
    
    if (scroll_pos + 10 > next_hl_top && next_hl != null) { // User scrolled down
        highlight(next_hl);
    } else if (scroll_pos + 10 < current_hl_top) { // User scrolled up 
        highlight(prev_hl);
    }

};

// Scroll and resize handlers
var last_known_scroll_position = 0;
var ticking = false;

window.addEventListener('scroll', function(e) { 
    scroll_handler(e);
});
window.addEventListener('resize', function(e) {
    scroll_handler(e);
});

function scroll_handler(ev) { 
    last_known_scroll_position = window.scrollY;
    if (!ticking) {
        window.requestAnimationFrame(function() {
            if (ev.type == 'scroll') {
                tocHighlight(last_known_scroll_position);
            } else if (ev.type == 'resize') {
                toc_repositioned = true; // Changing this variable allows menuFade to do something
                TOC_REL_YPOS = relYPos(document.getElementById("sidebar"),"bottom");
            }
            menuFade(last_known_scroll_position);
            ticking = false;
        });
    }
    ticking = true;
};

// Page load handler
window.addEventListener('load', function() {
    /// Set global constants
    // Find position of table of contents relative to top of body
    TOC = document.getElementById("toc-container");
    TOC_REL_YPOS = relYPos(TOC);
    
    // headers(): get a list of h2 and h3 elements inside <div id="content">
    var headers = function() {
        var headers_list = [];
        var content_tree = document.getElementById("content").childNodes;
        
        for (var i = 0; i < content_tree.length; i++) {
            if (content_tree[i].tagName == "H2" || content_tree[i].tagName == "H3") {
                headers_list.push(content_tree[i]); 
            }
        }
        
        return headers_list;
    };
    
    HEADERS_LIST = headers();
    
    //// Populate Table of Contents
    // Add <h2> Table of Contents text
    var toc_h2 = document.getElementById('toc');
    toc_h2.innerHTML='On This Page';
    /* Spoiler button:
    <button id="toc-list-trigger" class="toc-list-trigger"></button> */
    
    /// Create a list 
    var list = document.createElement('ul');
    list.setAttribute('id','toc-list'); // Give list id='toc-list'
    addClass(list,'spoiler-spoiled'); // Give list collapsiblility
    
    // Header is an item from HEADERS_LIST (a collection of children of #content that are <h2> or <h3> elements)
    var create_bullet = function(header) {
        var header_name = header.getAttribute('id');
        var bullet = document.createElement('li');

        // Returns <a href="..." id="(header_name)-link">Text</a>
        var create_link = function() {
            html_link_str = "<a href='#" + header_name + "' id='" + header_name + "-link'>" + header.innerHTML + "</a>"
            return html_link_str;
        }

        if (header.tagName == "H2") { // If <h2>, enclose link in <li></li>
            addClass(bullet,'toc-h2');
            bullet.innerHTML = create_link();
        } else {                      // If <h3>, enclose link in <li><ul><li></li></ul></li>
            addClass(bullet,'toc-h3');
            bullet.innerHTML = "<ul><li>" + create_link() + "</li></ul>";
        }
        
        list.appendChild(bullet);
    }
    
    for (var i = 0; i < HEADERS_LIST.length; i++) {
        current_hdr = HEADERS_LIST[i];
        // Add id tag to all <h2>, <h3> elements, id = 1, 2, 3, ...
        current_hdr.setAttribute('id',i); 
        
        // Populate list
        create_bullet(current_hdr,list);
    }
    
    TOC.appendChild(list);
});