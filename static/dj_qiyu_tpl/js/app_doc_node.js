class AppDocNode extends HTMLDivElement {
    constructor() {
        super();

        const shadow = this.attachShadow({mode: 'closed'});

        shadow.innerHTML = this.innerHTML;
        // remove first empty node [indent failed eg]
        //
        //   import os
        // import sys
        //
        shadow.querySelectorAll("code").forEach(function (code) {
            let first = code.firstChild;
            if (first === null) {
                return;
            }
            if (first.nodeName === "#text" && first.textContent.trim() === "") {
                code.removeChild(first);
            }
        });

        [
            "/static/dj_qiyu_tpl/vendor/rst/minimal.css",
            "/static/dj_qiyu_tpl/vendor/rst/plain.css",
        ].forEach(function (href) {
            let style = document.createElement("link");
            style.rel = "stylesheet";
            style.type = "text/css";
            style.href = href;
            shadow.appendChild(style);
        });
    }
}

customElements.define("app-doc", AppDocNode, {extends: "div"});
