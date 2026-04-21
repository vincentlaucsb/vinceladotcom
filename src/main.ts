import { ProfileLink } from "./ProfileLink";
import { updateGitHubStars } from "./githubStars";
import "./HeroImage";
import "./styles.scss";

// Ensure component is registered
void ProfileLink;

const year = document.getElementById("year");
if (year) {
  year.textContent = String(new Date().getFullYear());
}

const projectLinks = Array.from(
  document.querySelectorAll<HTMLElement>("profile-link[data-github-repo]")
);

void updateGitHubStars(projectLinks);
