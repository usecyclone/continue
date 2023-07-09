import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { Provider } from "react-redux";
import store from "./redux/store";
import "./index.css";

import posthog from "posthog-js";
import { PostHogProvider } from "posthog-js/react";

// @ts-ignore rrweb does not have type info
import rrwebRecord from "rrweb/es/rrweb/packages/rrweb/src/record";

posthog.init("phc_JS6XFROuNbhJtVCEdTSYk6gl5ArRrTNMpCcguAXlSPs", {
  api_host: "https://app.posthog.com",
});

// posthog does not post rrweb messages to the top level VSCode window, so we need to
// forward them ourselves.
rrwebRecord({
  emit(event: any) {
    window.top?.postMessage(
      { type: "rrweb", event, origin: window.location.origin },
      "*"
    );
  },
});

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <PostHogProvider client={posthog}>
      <Provider store={store}>
        <App />
      </Provider>
    </PostHogProvider>
  </React.StrictMode>
);
