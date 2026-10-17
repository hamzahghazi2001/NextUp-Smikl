# NextUp Project Charter

## 1. The product in one paragraph
This is my capstone project. It uses the Simkl API to build a list as the source, which is continuously updated based on the user's next aired episode for each title marked "Plan to Watch" or "Watching".

## 2. Product vision (end state)
V1-V8 in my own words:

**V1: Direct Simkl link.** The NextUp account links directly to the user's Simkl profile. No middle account or extra auth is required.

**V2: One link, one manifest.** A single link and manifest that updates automatically based on the user's saved preferences.

**V3: Custom list controls.** Users choose how they see their list, with toggles for:
- Content type: anime, TV, or both
- Which lists to include: Watching, Plan to Watch, and Completed shows that get new episodes

**V4: Poster studio.** A complete studio for customizing the poster look.

**V5: Dub release info.** An optional toggle for dub release information on anime titles. Users bring their own AnimeSchedule API key.

**V6: Bring your own keys.** Users add their own TVDB and MDBList keys, with simple steps for getting one.

**V7: Full enrichment.** Every user gets status tags, latest and next episode, TMDB artwork, logos and ratings, TVDB seasons and stills, and MAL scores on anime. Features that need a user's own key switch on once the key is added.

**V8: Live settings.** Saving settings changes what the same link shows.

# NextUp Architecture (End State)

## 1. Vision in one paragraph
NextUp turns a user's Simkl lists into one Nuvio catalog that stays current with their next aired episodes. Each user gets one personal install link and a settings page. Settings live on the server, so saving them changes what the same link shows, with no reinstall. Core builds only the thin slice (one account, TV, Watching), but the design leaves room for everything else.

## 2. Blocks
| Block | Its one job | In Core? |
|---|---|---|
| API (FastAPI) | Answers manifest, catalog and /health requests | Yes |
| Database (PostgreSQL) | Keeps all state that must survive a restart | Yes |
| Sync | Copies Simkl changes into the database | Yes (manual) |
| Simkl adapter | Only block that talks to Simkl | Yes |
| Other adapters (TMDB, TVDB, MDBList, AnimeSchedule) | One block per service, each the only one that talks to it | No |
| Poster renderer | Builds poster image URLs and generated artwork | Basic Simkl poster only |
| Settings & link service | Login, preferences, personal install links | No |

## 3. Outside services
| Service | Adapter | Whose key | Layer / task |
|---|---|---|---|
| Simkl | Simkl adapter | App secret + user's token | A: NEXTUP-INITIAL-SYNC; D: NEXTUP-ALPHA-OAUTH |
| TMDB | TMDB adapter | App's own | B*: NEXTUP-TMDB-ENRICHMENT |
| MDBList | MDBList adapter | User's own | C: NEXTUP-ID-FALLBACK-MDBLIST |
| TVDB | TVDB adapter | User's own | C: NEXTUP-TVDB-CLIENT |
| AnimeSchedule | AnimeSchedule adapter | User's own | Open item (v2) |
| MyAnimeList | MAL adapter | App's own | Open item |

## 4. One request, end to end
Personal link → token lookup → account → that account's settings → library rows + show data → filter and style → catalog answer

In Core, the token lookup always returns the single default account and default settings.

## 5. Sync, per account
- First run pulls the user's library once.
- Later runs check Simkl activity and merge only the delta, using a cursor stored per account.
- Core: manual, on demand, one account, Watching only.
- Simkl decides each title's type (TV or anime). The copy follows it, and the anime/TV/both toggle filters on the current type at read time. Toggling never changes the database.
- A failed sync keeps the last-known-good data.

## 6. End-state tables (mark the Core ones)
| Table | Holds | Core? |
|---|---|---|
| account | One row per user | Yes (one row) |
| show | Each show once, shared by everyone | Yes |
| library | account_id + show_id + list status | Yes |
| next_episode | Latest aired and next unwatched per show | Yes |
| sync | Cursor and last-run info per account | Yes |
| settings | account_id, media types, lists, poster style, dub toggle | No |
| user_key | account_id, provider, encrypted key | No |
| install_token | token_hash, account_id | No |

Every user-owned table carries account_id, and every query filters by it.

## 7. Secrets
| Secret | Lives in | Never in |
|---|---|---|
| Simkl client secret | Environment variable | Git, logs |
| TMDB / MAL app keys | Environment variable | Git, logs |
| User's Simkl token | Database, encrypted | URLs, logs, catalog JSON |
| User's TVDB / MDBList / AnimeSchedule keys | Database, encrypted | URLs, logs, catalog JSON |
| Install token | Database, stored hashed | Logs |

## 8. One install link and the settings page
- Link format: `https://nextup.example/<random-token>/manifest.json`. The token is random and means nothing by itself.
- Nuvio shows a Configure button (`behaviorHints.configurable: true`) that opens the `/configure` page.
- Settings are saved on the server, never inside the address.
- The manifest always has one catalog and never changes, so users never reinstall.
- Settings change only what is in the catalog and how posters look.
- Poster URLs include the user's style version, so new styles show up instead of cached images.
- A leaked link is cancelled by revoking its token. The Simkl account stays safe.

## 9. Hosted vs self-hosted
| | Hosted | Self-hosted |
|---|---|---|
| Who stores user keys | Me | Each user |
| Login | Log in with Simkl (OAuth) | Token pasted into settings |
| Personal links | Needed | Copy is already personal |
| Cost and risk | Server, security, support | Almost none |

Both are recorded. The decision comes later (v2).

## 10. Core path and the seams Core keeps
**Core path:** Simkl → Simkl adapter → sync → PostgreSQL → FastAPI → one catalog in Nuvio, plus /health.

**Seams:**
- account_id on every user-owned table
- Media type and lists as settings, not hard-coded
- One stable catalog in the manifest
- One adapter per outside service
- Catalog route first asks "whose settings apply?" (Core: the defaults)
- Poster URLs built in one function
- Secrets from the environment only, and none in any URL

## 11. Open items
- Automatic hourly sync
- MAL scores on anime
- TV ratings
- English-dub progress and per-show override (V5)
- Settings page: toggles, poster studio, own keys (V3, V4, V6)
- Rebuild or drop the episode list copied into each card (B20), decided in NEXTUP-PARITY-ACCEPTANCE