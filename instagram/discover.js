// deno-lint-ignore-file no-unused-vars

/** Open likes dialog for the current post. */
function openPostLikes() {
  Array.from(
    Array.from(document
      .querySelectorAll("span"))
      .find((e) => e.innerText.startsWith("Liked by"))
      .querySelectorAll("a"),
  ).pop().click();
}

/** Returns the opened likes dialog. */
function getLikesDialog() {
  return Array.from(document
    .querySelectorAll('div[role="dialog"]'))
    .find((e) => e.innerText.startsWith("Likes"));
}

/** Scroll to the end of likes list. */
function scrollToLikesDialogBottom() {
  const scrollable = document.querySelector(
    'div[style="height: 356px; overflow: hidden auto;"]',
  );
  scrollable.scroll(10, 1000000);
  scrollable.scroll(10, scrollable.scrollHeight - 500);
}

/** Open notifications sidecar. */
function openNotifications() {
  Array.from(document
    .querySelectorAll('a[href="#"]'))[1]
    .click();
}

/** Show notification filters dialog. */
function openNotificationFilters() {
  Array.from(document
    .querySelectorAll('div[role="button"]'))
    .find((e) => e.innerText.trim() === "Filter")
    .click();
}

/** Show only follow notifications. */
function enableFollowsFilter() {
  Array.from(
    document
      .querySelector('div[role="dialog"]')
      .querySelectorAll("div"),
  )
    .find((e) => e.innerText.trim() === "Follows")
    .click();
}

/** Apply changes to the notification filters. */
function applyFilters() {
  Array.from(
    document
      .querySelector('div[role="dialog"]')
      .querySelectorAll('div[role="button"]'),
  )
    .find((e) => e.innerText.trim() === "Apply")
    .click();
}

/** Returns the profiles with a 'Follow' button. */
function getProfiles() {
  return Array.from(document.querySelectorAll("button")).filter((e) =>
    e.innerText.trim() === "Follow"
  ).map((e) => {
    let parent = e.parentElement.parentElement;
    let link = parent.querySelector("a");
    if (!link) {
      parent = parent.parentElement;
      link = parent.querySelector("a");
    }
    return link.getAttribute("href").match(/[^/]+/)[0];
  });
}
