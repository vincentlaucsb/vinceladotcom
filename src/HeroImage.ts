const heroImage = document.querySelector<HTMLElement>(".full-bleed-bg");

if (heroImage) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          heroImage.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.15,
    }
  );

  observer.observe(heroImage);
}