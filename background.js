const BLOCK_DURATION = 1 * 60 * 1000; // 20 minutes
const WAIT_DURATION = 3 * 60 * 60 * 1000; // 3 hours

let blockedSites = [];
let lastAccessTime = 0;

browser.storage.local.get(["blockedSites", "lastAccessTime"], (data) => {
  blockedSites = data.blockedSites || [];
  lastAccessTime = data.lastAccessTime || 0;
});

function shouldBlock(url) {
  const now = Date.now();
  if (now - lastAccessTime > WAIT_DURATION + BLOCK_DURATION) {
    lastAccessTime = now;
    browser.storage.local.set({ lastAccessTime });
    return false;
  }
  if (now - lastAccessTime < BLOCK_DURATION) {
    return false;
  }
  return blockedSites.some(site => url.includes(site));
}

browser.webRequest.onBeforeRequest.addListener(
  (details) => {
    if (shouldBlock(details.url)) {
      return { cancel: true };
    }
  },
  { urls: ["<all_urls>"] },
  ["blocking"]
);