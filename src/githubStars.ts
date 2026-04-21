type GitHubRepoResponse = {
  stargazers_count?: number;
};

type StarCacheEntry = {
  stars: number;
  fetchedAt: number;
};

const STAR_CACHE_KEY = "github-repo-stars-v1";
const STAR_CACHE_TTL_MS = 30 * 60 * 1000;

export async function updateGitHubStars(links: HTMLElement[]): Promise<void> {
  const cache = readStarCache();

  await Promise.all(
    links.map(async (link) => {
      const repo = link.getAttribute("data-github-repo");
      if (!repo) {
        return;
      }

      const baseNote = link.getAttribute("note") || "";
      const cached = cache[repo];
      if (cached && Date.now() - cached.fetchedAt < STAR_CACHE_TTL_MS) {
        setStarNote(link, baseNote, cached.stars);
        return;
      }

      try {
        const response = await fetch(`https://api.github.com/repos/${repo}`, {
          headers: {
            Accept: "application/vnd.github+json",
          },
        });

        if (!response.ok) {
          return;
        }

        const payload = (await response.json()) as GitHubRepoResponse;
        if (typeof payload.stargazers_count !== "number") {
          return;
        }

        const count = payload.stargazers_count;
        cache[repo] = {
          stars: count,
          fetchedAt: Date.now(),
        };
        writeStarCache(cache);
        setStarNote(link, baseNote, count);
      } catch {
        // Keep the original note text if GitHub is unavailable or rate-limited.
      }
    })
  );
}

function setStarNote(link: HTMLElement, baseNote: string, stars: number): void {
  const starText = `${stars.toLocaleString()} ${stars === 1 ? "star" : "stars"}`;
  const nextNote = baseNote ? `${baseNote} | ${starText}` : starText;
  const noteElement = link.querySelector<HTMLElement>(".link-note");
  if (noteElement) {
    noteElement.textContent = nextNote;
  }
}

function readStarCache(): Record<string, StarCacheEntry> {
  try {
    const raw = window.localStorage.getItem(STAR_CACHE_KEY);
    if (!raw) {
      return {};
    }

    const parsed = JSON.parse(raw) as Record<string, StarCacheEntry>;
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    return {};
  }
}

function writeStarCache(cache: Record<string, StarCacheEntry>): void {
  try {
    window.localStorage.setItem(STAR_CACHE_KEY, JSON.stringify(cache));
  } catch {
    // Ignore localStorage failures and continue without caching.
  }
}
