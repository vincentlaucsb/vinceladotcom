export class ProfileLink extends HTMLElement {
  connectedCallback() {
    const label = this.getAttribute("label") || "";
    const note = this.getAttribute("note") || "";
    const href = this.getAttribute("href") || "#";

    const anchor = document.createElement("a");
    anchor.href = href;
    anchor.target = "_blank";
    anchor.rel = "noreferrer noopener";
    anchor.className = "link-anchor";

    const title = document.createElement("span");
    title.className = "link-label";
    title.textContent = label;

    const subtitle = document.createElement("span");
    subtitle.className = "link-note";
    subtitle.textContent = note;

    const arrow = document.createElement("span");
    arrow.className = "link-arrow";
    arrow.textContent = "Open";

    anchor.append(title, subtitle, arrow);
    this.append(anchor);
  }
}

customElements.define("profile-link", ProfileLink);
