// 这个文件应该仅仅被加载一次
window.addEventListener("DOMContentLoaded", function () {
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

            const static_url = globalThis['_django_static_url'];

            [`${static_url}dj_qiyu_tpl/vendor/rst/minimal.css`, `${static_url}dj_qiyu_tpl/vendor/rst/plain.css`,].forEach(function (href) {
                let style = document.createElement("link");
                style.rel = "stylesheet";
                style.type = "text/css";
                style.href = href;
                shadow.appendChild(style);
            });
        }
    }

    customElements.define("app-doc", AppDocNode, {extends: "div"});
});
