//// Section 1: Make menu change styles when user scrolls past a certain point
// Initialize values
var last_known_scroll_position = 0;
var toc_rel_ypos = 0;
var toc_fixed = false;
var ticking = false;

function menuFade(scroll_pos) {
    var body = document.getElementsByTagName("body")[0];
    var body_ypos = body.getBoundingClientRect()["top"];
    var toc = document.getElementById("toc-container");
    var toc_ypos = toc.getBoundingClientRect()["top"];
 
    var current_style = toc.getAttribute('style');
    
    if (toc_rel_ypos == 0) {
        // Return position of table of contents relative to top of page
        // Should only change if user resizes window
        toc_rel_ypos = toc_ypos - body_ypos;
    }
    
    // Change style if we have scrolled past the desired point
    else if (scroll_pos > toc_rel_ypos) {
        // Make sure the style has not yet been changed
        if (toc_fixed == false) {
            toc.setAttribute('style','position: fixed; top: 0; background-color: #ffffff;')
            toc_fixed = true;
        }
    }
    else {
        toc.setAttribute('style','');
        toc_fixed = false;
    }
}

window.addEventListener('scroll', function(e) {
    last_known_scroll_position = window.scrollY;
    if (!ticking) {
        window.requestAnimationFrame(function() {
            menuFade(last_known_scroll_position);
            ticking = false;
        });
    }
    ticking = true;
});

// Section 2: Populate the table of contents
window.onload = function() {
    // Get a list of h2 and h3 elements
    var headers_list = [];
    
    var content_tree = document.getElementById("content").childNodes;
    for (var i = 0; i < content_tree.length; i++) {
        if (content_tree[i].tagName == "H2" || content_tree[i].tagName == "H3") {
            headers_list.push(content_tree[i]); 
        }
    }
    
    var h2_list = document.getElementsByTagName('h2');

    // Add <h2> Table of Contents text
    var toc_h2 = document.getElementById('toc');
    toc_h2.innerHTML='On This Page';
    
    // Add id tag to all <h2> elements
    for (var i = 0; i < h2_list.length; i++) {
        current_h2 = h2_list[i];
        if (current_h2.innerHTML != 'On This Page') {
            current_h2.setAttribute('id',current_h2.innerHTML);
        }
    }
    
    //// Create a list 
    var list = document.createElement('ul');
    
    for (var i = 0; i < h2_list.length; i++) {
        current_h2 = h2_list[i];
        if (current_h2.innerHTML != 'On This Page') {   
            var bullet = document.createElement('li');
            var link = document.createElement('a');
            link.setAttribute('href','#' + current_h2.getAttribute('id'));
            link.innerHTML=current_h2.innerHTML;
            bullet.appendChild(link);
            list.appendChild(bullet);
        }
    }
    
    var toc_container = document.getElementById('toc-container');
    toc_container.appendChild(list);
    
    console.log(h2_list);
}


// Deal with <h3> elements
var list_h3 = function() {
    
}