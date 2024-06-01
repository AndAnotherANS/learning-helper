chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "startRecord") {
        // Send a message to the background script
        chrome.runtime.sendMessage({action: "startRecord"}, function(response) {
            if (chrome.runtime.lastError) {
                console.error(chrome.runtime.lastError.message);
                return;
            }
            sendResponse(response);
        });
        return true; // Keep the message channel open for sendResponse
    }
});
