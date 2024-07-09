import requests

def make_anilist_request(mediaId, page = 1):
    """Makes a request to AniList"""
    url = "https://graphql.anilist.co"
    query = """
    query ($mediaId: Int, $page: Int) {
        Page(page: $page, perPage: 500) {
            pageInfo {
                hasNextPage
            }
            activities(userId: 5613718, mediaId: $mediaId) {
                ... on ListActivity {
                    createdAt
                    media {
                        title {
                            userPreferred
                        }
                    }
                    status
                    progress
                }
            }
        }
    }
    """
    variables = {
        "mediaId": mediaId,
        "page": page
    }

    return requests.post(url, json={"query": query, "variables": variables}, timeout=60)