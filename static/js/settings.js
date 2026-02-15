function getItemWithDefault(keyName, defaultValue) {
    let v = localStorage.getItem(keyName);
    if (v === null) 
        return defaultValue;
    return v;
}

function loadSettings() {
    wide_checkbox = document.getElementById("wide-checkbox");
    invert_color_scheme_checkbox = document.getElementById("invert-color-scheme-checkbox");
    wide_checkbox.checked = eval(getItemWithDefault("wide", false));
    invert_color_scheme_checkbox.checked = eval(getItemWithDefault("invert_color_scheme", false));
    // Delete temporary CSS
    document.getElementById("temp-css").remove();
}

function saveSettings() {
    wide_checkbox = document.getElementById("wide-checkbox");
    invert_color_scheme_checkbox = document.getElementById("invert-color-scheme-checkbox");
    localStorage.setItem("wide", wide_checkbox.checked);
    localStorage.setItem("invert_color_scheme", invert_color_scheme_checkbox.checked);
}


/*
This function is called immediately, it's purpose is to create a temporary <style>
which sets CSS variables to match the non-default settings (and to temporarly hide
the setting elements) until the page (and thus checkboxes) is completely loaded.
It's then deleted so that the checkboxes and CSS can take over; the purpose of this
function is to avoid having the page flash the wrong colors or wrong width while
it's not completely loaded, which looks really ugly.
And yes, the whole reason this mess is needed is just that I really wanted to have
a pure CSS color theme/width toggle implementation :).
*/
function tempCSS() {
    let prefers_dark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    let invert_color_scheme = eval(getItemWithDefault("invert_color_scheme", "false"));
    let wide = eval(getItemWithDefault("wide", "false"));
    var partial_css = '';
    if (invert_color_scheme) {
        let prefix;
        // Here we're setting the OPPOSITE scheme to the one reported as preferred
        if (prefers_dark) 
            prefix = "LIGHT";
        else 
            prefix = "DARK";
        // Add CSS related to colors
        partial_css = `${partial_css} --background-color: var(--${prefix}-background-color) !important; 
            --color: var(--${prefix}-color) !important; 
            --noscript-warning-color: var(--${prefix}-noscript-warning-color) !important; 
            --link-color: var(--${prefix}-link-color) !important;`;
    }
    if (wide) {
        // Add CSS for width
        partial_css = `${partial_css} --width-limit: initial !important;`
    }
    // Source - https://stackoverflow.com/a/524721
    // Posted by Christoph, modified by community. See post 'Timeline' for change history
    // Retrieved 2026-02-15, License - CC BY-SA 4.0
    let css = `#header-buttons {visibility: hidden !important;} :root{ ${partial_css} }`,
        head = document.head,
        style = document.createElement('style');
    style.id = "temp-css"
    head.appendChild(style);
    style.appendChild(document.createTextNode(css));
}

tempCSS();