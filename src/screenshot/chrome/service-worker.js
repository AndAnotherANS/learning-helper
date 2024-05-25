// Listen for a click on the camera icon. On that click, take a screenshot.
chrome.action.onClicked.addListener(async function () {
  console.log("git screenshot 1")
    const screenshotUrl = await chrome.tabs.captureVisibleTab();
    const viewTabUrl = chrome.runtime.getURL('screenshot.html');
    let targetId = null;
  
    chrome.tabs.onUpdated.addListener(function listener(tabId, changedProps) {
      console.log("git screenshot 4")

      // We are waiting for the tab we opened to finish loading.
      // Check that the tab's id matches the tab we opened,
      // and that the tab is done loading.
      if (tabId != targetId || changedProps.status != 'complete') return;
  
      // Passing the above test means this is the event we were waiting for.
      // There is nothing we need to do for future onUpdated events, so we
      // use removeListner to stop getting called when onUpdated events fire.
      chrome.tabs.onUpdated.removeListener(listener);
  
      // Send screenshotUrl to the tab.
      // ---------------- here we have our image of screenshot -------------------
      console.log(screenshotUrl)
      // chrome.tabs.sendMessage(tabId, { msg: 'screenshot', data: screenshotUrl });
    });
    console.log("git screenshot 5")

    const tab = await chrome.tabs.create({ url: viewTabUrl });
    targetId = tab.id;
  });

