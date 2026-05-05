---
name: lap-aggregators-api-service
description: "Aggregators API Service API skill. Use when working with Aggregators API Service for podcast-bot, api, stats. Covers 61 endpoints."
version: 1.0.0
generator: lapsh
metadata:
  openclaw:
    requires:
      env:
        - AGGREGATORS_API_SERVICE_API_KEY
---

# Aggregators API Service
API version: 0.80-ffcc0de

## Auth
ApiKey X-Auth-Token in header

## Base URL
https://api.zeno.fm

## Setup
1. Set your API key in the appropriate header
2. GET /podcast-bot/podcasts/list -- verify access
3. POST /stats/mounts/{mount}/auth-cache/reload -- create first reload

## Endpoints

61 endpoints across 4 groups. See references/api-spec.lap for full details.

### podcast-bot
| Method | Path | Description |
|--------|------|-------------|
| GET | /podcast-bot/podcasts/{podcastKey} | Get podcast |
| PUT | /podcast-bot/podcasts/{podcastKey} | Update podcast info |
| DELETE | /podcast-bot/podcasts/{podcastKey} | Delete podcast |
| GET | /podcast-bot/podcasts/{podcastKey}/recordingConfig | Get podcast recording configuration |
| PUT | /podcast-bot/podcasts/{podcastKey}/recordingConfig | Update podcast recording configuration |
| DELETE | /podcast-bot/podcasts/{podcastKey}/recordingConfig | Delete podcast recording configuration |
| GET | /podcast-bot/podcasts/{podcastKey}/processingPresets | Get podcast processing presets |
| PUT | /podcast-bot/podcasts/{podcastKey}/processingPresets | Update podcast processing presets |
| GET | /podcast-bot/podcasts/{podcastKey}/interviewPresets | Get podcast interview extraction presets |
| PUT | /podcast-bot/podcasts/{podcastKey}/interviewPresets | Update podcast interview extraction presets |
| PUT | /podcast-bot/podcasts/{podcastKey}/episodes/{episodeKey}/unpublish | Unpublish podcast episode |
| PUT | /podcast-bot/podcasts/{podcastKey}/episodes/{episodeKey}/publish | Publish podcast episode |
| GET | /podcast-bot/podcasts/{podcastKey}/aiAdsPresets | Get podcast AI Ads presets |
| PUT | /podcast-bot/podcasts/{podcastKey}/aiAdsPresets | Update podcast AI Ads presets |
| POST | /podcast-bot/workflows/process-file | Process file |
| POST | /podcast-bot/podcasts/{podcastKey}/upload/prerollAudio | Upload pre-roll audio - prepended to every episode |
| POST | /podcast-bot/podcasts/{podcastKey}/upload/postrollAudio | Upload post-roll audio - appended to every episode |
| POST | /podcast-bot/podcasts/{podcastKey}/upload/editOutroAudio | Upload outro audio for edit recording |
| POST | /podcast-bot/podcasts/{podcastKey}/upload/editIntroAudio | Upload intro audio for edit recording |
| POST | /podcast-bot/podcasts/{podcastKey}/episodes/{episodeKey}/reprocess | Reprocess episode |
| POST | /podcast-bot/podcasts/{podcastKey}/episodes/{episodeKey}/reprocess/custom | Reprocess episode with custom presets |
| POST | /podcast-bot/podcasts/recording/create | Create recording podcast |
| GET | /podcast-bot/workflows/{workflowId}/details | Get workflow details |
| GET | /podcast-bot/podcasts/{podcastKey}/episodes | Get podcast episodes |
| GET | /podcast-bot/podcasts/{podcastKey}/episodes/{episodeKey} | Get podcast episode |
| DELETE | /podcast-bot/podcasts/{podcastKey}/episodes/{episodeKey} | Delete podcast episode |
| GET | /podcast-bot/podcasts/{podcastKey}/episodes/{episodeKey}/transcript | Get transcript for a podcast episode |
| GET | /podcast-bot/podcasts/{podcastKey}/episodes/{episodeKey}/metadata | Get metadata for a podcast episode |
| GET | /podcast-bot/podcasts/{podcastKey}/episodes/{episodeKey}/adsMarkers | Get Ads markers info for a podcast episode |
| GET | /podcast-bot/podcasts/{podcastKey}/episodes/interviews | Get podcast interviews |
| GET | /podcast-bot/podcasts/list | List podcasts |
| GET | /podcast-bot/jobs/podcasts/{podcastKey} | Get all processing jobs for a podcast |
| GET | /podcast-bot/jobs/podcasts/{podcastKey}/episodes/{episodeKey} | Get processing jobs for a podcast episode |

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v2/podcasts/{podcastKey} | Get podcast |
| PUT | /api/v2/podcasts/{podcastKey} | Update podcast |
| DELETE | /api/v2/podcasts/{podcastKey} | Delete podcast |
| GET | /api/v2/podcasts/{podcastKey}/episodes/{episodeKey} | Get podcast episode |
| PUT | /api/v2/podcasts/{podcastKey}/episodes/{episodeKey} | Update podcast episode |
| DELETE | /api/v2/podcasts/{podcastKey}/episodes/{episodeKey} | Delete podcast episode |
| POST | /api/v2/stations/search | Search stations |
| POST | /api/v2/stations/listener/location | Get top stations by listener location |
| POST | /api/v2/podcasts/{podcastKey}/episodes/create | Create podcast episode |
| POST | /api/v2/podcasts/search | Search podcasts |
| POST | /api/v2/podcasts/create | Create podcast |
| GET | /api/v2/stations/{stationKey} | Get station |
| GET | /api/v2/stations/list | List stations |
| GET | /api/v2/stations/languages | Get the list of Languages that can be used to filter stations in the search stations request |
| GET | /api/v2/stations/genres | Get the list of Genres that can be used to filter stations in the search stations request |
| GET | /api/v2/stations/countries | Get the list of Countries that can be used to filter stations in the search stations request |
| GET | /api/v2/stations/browse | Browse all stations |
| GET | /api/v2/podcasts/{podcastKey}/episodes | Get podcast episodes |
| GET | /api/v2/podcasts/languages | Get the list of Languages that can be used to filter podcasts in the search podcasts request |
| GET | /api/v2/podcasts/countries | Get the list of Countries that can be used to filter podcasts in the search podcasts request |
| GET | /api/v2/podcasts/categories | Get the list of Categories that can be used to filter podcasts in the search podcasts request |

### stats
| Method | Path | Description |
|--------|------|-------------|
| POST | /stats/mounts/{mount}/auth-cache/reload | Retrieve total numer of live stats for a specific mount |
| POST | /stats/mounts/{mount}/auth-cache/reload/all | Retrieve total numer of live stats for a specific mount |
| GET | /stats/mounts/{mount}/live/total | Retrieve total numer of live stats for a specific mount |

### partners
| Method | Path | Description |
|--------|------|-------------|
| POST | /partners/streams | Get the partner information for a list of streams. |
| GET | /partners/{partnerId}/ads/stats | Retrieve partner stats |
| GET | /partners/streams/{streamId} | Get the stream partner information. |
| GET | /partners/streams/{streamId}/tracks | Get the stream partner information. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get podcast details?" -> GET /podcast-bot/podcasts/{podcastKey}
- "Update a podcast?" -> PUT /podcast-bot/podcasts/{podcastKey}
- "Delete a podcast?" -> DELETE /podcast-bot/podcasts/{podcastKey}
- "List all recordingConfig?" -> GET /podcast-bot/podcasts/{podcastKey}/recordingConfig
- "List all processingPresets?" -> GET /podcast-bot/podcasts/{podcastKey}/processingPresets
- "List all interviewPresets?" -> GET /podcast-bot/podcasts/{podcastKey}/interviewPresets
- "List all aiAdsPresets?" -> GET /podcast-bot/podcasts/{podcastKey}/aiAdsPresets
- "Get podcast details?" -> GET /api/v2/podcasts/{podcastKey}
- "Update a podcast?" -> PUT /api/v2/podcasts/{podcastKey}
- "Delete a podcast?" -> DELETE /api/v2/podcasts/{podcastKey}
- "Get episode details?" -> GET /api/v2/podcasts/{podcastKey}/episodes/{episodeKey}
- "Update a episode?" -> PUT /api/v2/podcasts/{podcastKey}/episodes/{episodeKey}
- "Delete a episode?" -> DELETE /api/v2/podcasts/{podcastKey}/episodes/{episodeKey}
- "Create a reload?" -> POST /stats/mounts/{mount}/auth-cache/reload
- "Create a all?" -> POST /stats/mounts/{mount}/auth-cache/reload/all
- "Create a process-file?" -> POST /podcast-bot/workflows/process-file
- "Create a prerollAudio?" -> POST /podcast-bot/podcasts/{podcastKey}/upload/prerollAudio
- "Create a postrollAudio?" -> POST /podcast-bot/podcasts/{podcastKey}/upload/postrollAudio
- "Create a editOutroAudio?" -> POST /podcast-bot/podcasts/{podcastKey}/upload/editOutroAudio
- "Create a editIntroAudio?" -> POST /podcast-bot/podcasts/{podcastKey}/upload/editIntroAudio
- "Create a reprocess?" -> POST /podcast-bot/podcasts/{podcastKey}/episodes/{episodeKey}/reprocess
- "Create a custom?" -> POST /podcast-bot/podcasts/{podcastKey}/episodes/{episodeKey}/reprocess/custom
- "Create a create?" -> POST /podcast-bot/podcasts/recording/create
- "Create a stream?" -> POST /partners/streams
- "Create a search?" -> POST /api/v2/stations/search
- "Create a location?" -> POST /api/v2/stations/listener/location
- "Create a create?" -> POST /api/v2/podcasts/{podcastKey}/episodes/create
- "Create a search?" -> POST /api/v2/podcasts/search
- "Create a create?" -> POST /api/v2/podcasts/create
- "List all total?" -> GET /stats/mounts/{mount}/live/total
- "List all details?" -> GET /podcast-bot/workflows/{workflowId}/details
- "List all episodes?" -> GET /podcast-bot/podcasts/{podcastKey}/episodes
- "Get episode details?" -> GET /podcast-bot/podcasts/{podcastKey}/episodes/{episodeKey}
- "Delete a episode?" -> DELETE /podcast-bot/podcasts/{podcastKey}/episodes/{episodeKey}
- "List all transcript?" -> GET /podcast-bot/podcasts/{podcastKey}/episodes/{episodeKey}/transcript
- "List all metadata?" -> GET /podcast-bot/podcasts/{podcastKey}/episodes/{episodeKey}/metadata
- "List all adsMarkers?" -> GET /podcast-bot/podcasts/{podcastKey}/episodes/{episodeKey}/adsMarkers
- "List all interviews?" -> GET /podcast-bot/podcasts/{podcastKey}/episodes/interviews
- "List all list?" -> GET /podcast-bot/podcasts/list
- "Get podcast details?" -> GET /podcast-bot/jobs/podcasts/{podcastKey}
- "Get episode details?" -> GET /podcast-bot/jobs/podcasts/{podcastKey}/episodes/{episodeKey}
- "List all stats?" -> GET /partners/{partnerId}/ads/stats
- "Get stream details?" -> GET /partners/streams/{streamId}
- "List all tracks?" -> GET /partners/streams/{streamId}/tracks
- "Get station details?" -> GET /api/v2/stations/{stationKey}
- "List all list?" -> GET /api/v2/stations/list
- "List all languages?" -> GET /api/v2/stations/languages
- "List all genres?" -> GET /api/v2/stations/genres
- "List all countries?" -> GET /api/v2/stations/countries
- "List all browse?" -> GET /api/v2/stations/browse
- "List all episodes?" -> GET /api/v2/podcasts/{podcastKey}/episodes
- "List all languages?" -> GET /api/v2/podcasts/languages
- "List all countries?" -> GET /api/v2/podcasts/countries
- "List all categories?" -> GET /api/v2/podcasts/categories
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## CLI

```bash
# Update this spec to the latest version
npx @lap-platform/lapsh get aggregators-api-service -o references/api-spec.lap

# Search for related APIs
npx @lap-platform/lapsh search aggregators-api-service
```

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
