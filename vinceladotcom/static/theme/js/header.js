// Goal:  Find nav menu (with id="header") and fix it after user
// scrolls down past it 

var header = {
    /* For scrolling */
    last_known_scroll_position: 0,
    ticking: false,
    
    get_scroll: function(scroll_pos) {
        if (scroll_pos > header.breakpoint) {
            header.remove_class(header.target, "navbar-unfixed");
            header.add_class(header.target, "navbar-fixed");
        } else {
            header.remove_class(header.target, "navbar-fixed");
            
            // This class does nothing but play a receding shadow animation
            header.add_class(header.target, "navbar-unfixed");
        }
    },
    
    //  Helper Functions
    /*  Removes class from an element
        elem      HTML element  
        cls_name  name of class to be removed */
    remove_class: function(elem, cls_name) {
        // classes will be an array of class names
        var temp = elem.getAttribute('class');
        var classes = temp ? temp.split(' ') : [];
        var remove_index = classes.indexOf(cls_name);
        
        if (remove_index > -1) {
            classes.splice(remove_index, 1);
            classes = classes.join(' ');
            elem.setAttribute('class',classes);
        }
    },

    /*  Adds a class to an element */
    add_class: function(elem, cls_name) {
        var temp = elem.getAttribute('class');
        
        // Make sure class is not already there
        var already_there = temp.indexOf(cls_name);
        
        if (already_there == -1) {
            var classes = temp ? temp + " " + cls_name: cls_name;
            elem.setAttribute('class',classes);
        }
    }
}

// Need to wait for document to load before getting target
document.onreadystatechange = function () {
    if (document.readyState === "complete") {
        console.log("Loaded");
        header.target = document.getElementById('navbar-top');
        header.breakpoint = header.target.getBoundingClientRect()["top"];
        
        // Add scrolling listener
        window.addEventListener('scroll', function(e) {
            header.last_known_scroll_position = window.scrollY;
            
            if (!header.ticking) {
                window.requestAnimationFrame(function() {
                    header.get_scroll(header.last_known_scroll_position);
                    header.ticking = false;
                });
            }
            
            header.ticking = true;
        });
    }
}