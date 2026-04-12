import { ProfileLink } from "./ProfileLink";
import "./styles.scss";

// Ensure component is registered
void ProfileLink;

const year = document.getElementById("year");
if (year) {
  year.textContent = String(new Date().getFullYear());
}
