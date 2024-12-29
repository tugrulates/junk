# instagram

These scripts are to be run on the web console of a browser.

## [`discover`](discover.js)

Discover relevant accounts to follow on Instagram.

Paste the whole file into web console, and call these functions.

### On any page

```js
openNotifications();
openNotificationFilters();
enableFollowsFilter();
applyFilters();
const profiles = getProfiles();
profiles;
```

### On a post page

```js
openPostLikes();
scrollToLikesDialogBottom();
const profiles = getProfiles();
profiles;
```

## [`follows`](follows.js)

Pull follower information on Instagram.

### On any page

Paste the whole file into web console, and wait for results.

```js
follows.following;
follows.followers;
follows.dontFollowBack;
follows.notFollowingBack;
copy(follows);
```

## [`stats`](instagram/stats.js)

Pull post insights on Instagram.

Paste the whole file into web console, and call these functions.

### On a profile page

```js
const posts = getPosts();
posts;
window.open(posts[0]);
```

### On a post page

```js
openPostMetrics();
const metrics = getMetrics();
metrics;
```
