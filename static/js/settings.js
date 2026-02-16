function getItemWithDefault(keyName, defaultValue) {
    let v = localStorage.getItem(keyName);
    if (v === null) 
        return defaultValue;
    return v;
}

function loadSettings() {
    let wide_checkbox = document.getElementById("wide-checkbox");
    wide_checkbox.checked = parseInt(getItemWithDefault("wide", "0"));

    let color_scheme = getItemWithDefault("color_scheme", "auto");
    document.getElementById(`color-scheme-${color_scheme}-radio`).checked = true;

    // Delete temporary CSS
    document.getElementById("temp-css").remove();
}

function saveSettings() {
    wide_checkbox = document.getElementById("wide-checkbox");
    color_scheme = document.querySelector("input[name='color-scheme']:checked").value;
    // Convert bool to int, which is then converted to string
    localStorage.setItem("wide", +wide_checkbox.checked); 
    localStorage.setItem("color_scheme", color_scheme);
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
    let wide = parseInt(getItemWithDefault("wide", "0"));
    let color_scheme = getItemWithDefault("color_scheme", "auto")
    var partial_css = '';
    if (color_scheme != "auto") {
        let prefix;
        if (color_scheme == "light") 
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
    let css = `#header-buttons {display: none !important;} :root{ ${partial_css} }`,
        head = document.head,
        style = document.createElement('style');
    style.id = "temp-css"
    head.appendChild(style);
    style.appendChild(document.createTextNode(css));
}

tempCSS();