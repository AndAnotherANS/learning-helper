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

// function startRecord() {
//     chrome.windows.getCurrent({}, function(e) {
//         chrome.windows.create({
//             url: "preview.html",
//             type: "popup",
//             width: 266,
//             height: 200,
//         }, function(e) {
//             cameraWindowId = e.id, chrome.windows.onRemoved.addListener(function(e) {
//                 e == cameraWindowId && console.log("window closed")
//             })
//         })
//     })
// }