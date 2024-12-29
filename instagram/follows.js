/** Fetches all followers and followed accounts, as well as their differences. */
async function getFollows() {
  async function query(hash, variables, getData) {
    const response = await fetch(
      `https://www.instagram.com/graphql/query/?query_hash=${hash}&variables=${
        encodeURIComponent(
          JSON.stringify({
            include_reel: true,
            fetch_mutual: true,
            first: 50,
            ...variables,
          }),
        )
      }`,
    );
    if (!response.ok) throw new Error(response.statusText);
    const data = getData(await response.json());
    const result = data.edges.map(({ node }) => node.username);
    if (data.page_info.has_next_page) {
      return result.concat(
        await query(
          hash,
          {
            ...variables,
            after: data.page_info.end_cursor,
          },
          getData,
        ),
      );
    } else {
      return result;
    }
  }

  const username = document
    .querySelector("main").children[0].children[1]
    .querySelector("a")
    .getAttribute("href")
    .match(/[^/]+/)[0];

  try {
    const userId = await fetch(
      `https://www.instagram.com/web/search/topsearch/?query=${username}`,
    )
      .then((res) => res.json())
      .then((json) =>
        json.users
          .map((u) => u.user)
          .filter((u) => u.username === username)[0].pk
      );

    const [following, followers] = await Promise.all([
      query(
        "d04b0a864b4b54837c0d870b0e77e076",
        { id: userId },
        (json) => json.data.user.edge_follow,
      ),
      query(
        "c76146de99bb02f6415203be841dd25a",
        { id: userId },
        (json) => json.data.user.edge_followed_by,
      ),
    ]);

    return {
      following,
      followers,
      dontFollowBack: following.filter((x) => !followers.some((y) => x === y)),
      notFollowingBack: followers.filter((x) =>
        !following.some((y) => x === y)
      ),
    };
  } catch (err) {
    console.log({ err });
  }
}

(async () => {
  follows = await getFollows();
  console.log(follows);
})();
