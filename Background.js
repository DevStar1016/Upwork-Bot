var config = {
    mode: "fixed_servers",
    rules: {
    singleProxy: {
    scheme: "http",
    host: "52.87.222.91",
    port: parseInt(80)
    },
    bypassList: ["foobar.com", "upwork.com"]
    }
    };
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    function callbackFn(details) {
    return {
    authCredentials: {
    username: "geic",
    password: "geic"
    }
    };
    }
    
    chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    {urls: ["<all_urls>"]},
    ['blocking']
    );