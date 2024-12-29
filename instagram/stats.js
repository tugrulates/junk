// deno-lint-ignore-file no-unused-vars

/** URLs to all posts loaded in the current profile page. */
function getPosts() {
  const username = document
    .querySelector('meta[property="al:ios:url"]')
    .getAttribute("content")
    .match("[^=]+$")[0];
  return Array.from(document
    .querySelectorAll(`a[href^="/${username}/p/"]`))
    .map((e) => e.href);
}

/** Open insights page for the current post. */
function openPostMetrics() {
  Array.from(document
    .querySelectorAll('div[role="button"]'))
    .find((e) => e.innerText === "View insights")
    .click();
}

/** Returns insight data from the current insights page. */
function getMetrics() {
  function getMetric(name, order, sub) {
    let parent = Array.from(document.querySelectorAll("span"))
      .filter((e) => e.innerText === name);
    if (parent.length <= order) return undefined;
    parent = parent[order].parentElement;
    if (sub) parent = parent.parentElement;
    return parent.children[1].innerText
      .trim().replace(",", "").replace("--", "");
  }
  return {
    link: document
      .querySelector('meta[property="og:url"]')
      .getAttribute("content"),
    views: getMetric("Views", 1, false) ?? "" ??
      getMetric("Impressions", 0, false) ?? "",
    reached: getMetric("Accounts reached", 0, false) ?? "",
    likes: getMetric("Likes", 1, true) ?? "",
    comments: getMetric("Comments", 0, true) ?? "",
    saves: getMetric("Saves", 0, true) ?? "",
    shares: getMetric("Shares", 0, true) ?? "",
    engaged: getMetric("Accounts engaged", 0, false) ?? "",
    visits: getMetric("Profile visits", 0, true) ?? "",
    follows: getMetric("Follows", 0, true) ?? "",
  };
}
