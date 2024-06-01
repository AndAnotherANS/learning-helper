chrome.browserAction.onClicked.addListener(function() {
    chrome.tabs.create({ url: "http://localhost:5000/C2" });
});