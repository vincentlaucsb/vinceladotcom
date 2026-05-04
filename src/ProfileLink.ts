export class ProfileLink extends HTMLElement {
  connectedCallback() {
    const label = this.getAttribute("label") || "";
    const note = this.getAttribute("note") || "";
    const href = this.getAttribute("href") || "#";
    const customActions = Array.from(this.querySelectorAll<HTMLAnchorElement>("a[href]")).map((action) => ({
      href: action.href,
      label: action.textContent?.trim() || "Open",
    }));

    const card = document.createElement("div");
    card.className = "link-anchor";

    const content = document.createElement("div");
    content.className = "link-content";

    const title = document.createElement("span");
    title.className = "link-label";
    title.textContent = label;

    const subtitle = document.createElement("span");
    subtitle.className = "link-note";
    subtitle.textContent = note;

    content.append(title, subtitle);

    const actions = document.createElement("div");
    actions.className = "link-actions";
    actions.append(createAction(href, "Open"));

    for (const action of customActions) {
      actions.append(createAction(action.href, action.label));
    }

    card.append(content, actions);
    this.replaceChildren(card);
  }
}

function createAction(href: string, label: string): HTMLAnchorElement {
  const action = document.createElement("a");
  action.href = href;
  action.target = "_blank";
  action.rel = "noreferrer noopener";
  action.className = "link-arrow";
  action.textContent = label;
  return action;
}

customElements.define("profile-link", ProfileLink);
