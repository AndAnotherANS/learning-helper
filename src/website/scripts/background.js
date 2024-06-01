"use strict";



function startRecord() {
    chrome.windows.getCurrent({}, function(e) {
        chrome.windows.create({
            url: "preview.html",
            type: "popup",
            width: 400,
            height: 400
        })
    })
}
