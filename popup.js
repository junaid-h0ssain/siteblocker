document.getElementById("addSite").addEventListener("click", () => {
    const siteInput = document.getElementById("siteInput");
    const site = siteInput.value.trim();
    if (!site) return;
    
    browser.storage.local.get("blockedSites", (data) => {
      let sites = data.blockedSites || [];
      if (!sites.includes(site)) {
        sites.push(site);
        browser.storage.local.set({ blockedSites: sites });
        updateUI();
      }
    });
    siteInput.value = "";
  });
  
  function updateUI() {
    browser.storage.local.get("blockedSites", (data) => {
      const siteList = document.getElementById("siteList");
      siteList.innerHTML = "";
      (data.blockedSites || []).forEach(site => {
        const li = document.createElement("li");
        li.textContent = site;
        siteList.appendChild(li);
      });
    });
  }
  
  document.addEventListener("DOMContentLoaded", updateUI);
  