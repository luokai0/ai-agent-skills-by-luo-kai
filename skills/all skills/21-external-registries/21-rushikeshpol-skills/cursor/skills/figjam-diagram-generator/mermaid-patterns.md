# Mermaid Patterns for FigJam Diagrams

Reference for generating Mermaid.js syntax compatible with the Figma MCP `generate_diagram` tool. Each section includes the shape/syntax mapping, a working example modeled after the client-reviewed Meal & Rest Break attestation FigJam, and hard constraints from the MCP tool.

---

## MCP Hard Constraints (all diagram types)

- Only supported types: `flowchart`, `graph`, `sequenceDiagram`, `stateDiagram-v2`, `gantt`
- No emojis anywhere in Mermaid code
- No literal `\n` for newlines
- Never use `end` as a node ID or className (reserved word)
- `generate_diagram` creates its own FigJam file per call; do NOT call `create_new_file` first

---

## Flowchart (primary for user flows)

### Direction

Always `flowchart LR`. Define the entry node first in the code — Mermaid places the first-defined node leftmost.

### Shape Mapping

| Purpose | Mermaid Shape | Example |
|---------|--------------|---------|
| Start/End state (actor action) | Stadium `(["..."])` | `A(["Officer taps Clock Out"])` |
| Decision / system check | Diamond `{"..."}` | `B{"System checks shift length"}` |
| Action / screen / system behavior | Rectangle `["..."]` | `C["Show attestation prompt: Click YES / NO"]` |
| Audit / data storage | Cylinder `[("...")]` | `D[("Audit Storage")]` |

### Edge Labels

| Purpose | Syntax | Example |
|---------|--------|---------|
| Decision outcome | `-->\|"label"\|` | `B -->\|"More than 3.5 hrs"\| C` |
| User action | `-->\|"label"\|` | `C -->\|"Officer clicks NO"\| D` |
| Outcome with context | `-->\|"label"\|` | `B -->\|"Less than 3.5 hrs (Skip attestation)"\| E` |
| Simple connection | `-->` | `A --> B` |
| Cross-subgraph handoff | `-.->` | `A -.-> B` |

### Flowchart Constraints

- All node text and edge labels in double quotes
- Standard 5-color palette MUST be applied to every flowchart (see Standard Color Palette section below)
- No back-links (edges from later to earlier nodes). Omit "return to" edges.

### Subgraph Pattern (multi-flow features)

All flows for one feature go into a single diagram using subgraphs. Each subgraph = one flow, titled `[Feature] - [Actor] [action] flow in [System]`.

```
flowchart LR
    subgraph officerFlow ["Meal Break - Officer attestation flow in MyConnect"]
        A(["Officer taps Clock Out"]) --> B{"System checks shift length"}
        B -->|"More than 3.5 hrs"| C["Attestation prompt: I certify all meal and rest periods were provided. Click: YES / NO"]
        B -->|"Less than 3.5 hrs (Skip attestation)"| F["Clock out confirmation (not shown on subsequent clock-outs)"]
        C -->|"Officer clicks YES"| F
        C -->|"Officer clicks NO"| D["Which break missed? Meal / Rest / Both. Provide Reason: ___"]
        D -->|"Officer Submits"| E["MyConnect creates exception in WFM"]
        E --> F
        F --> G(["Officer Clocked Out"])
        E --> H[("Audit Storage: officer response, timestamp, shift details, clock-in method, reason, WFM exception status")]
    end

    subgraph dmFlow ["Meal Break - DM Decision flow in WFM"]
        J["MyConnect creates exception in WFM"] -->|"Immediate or same-day"| K["DM notified"]
        K --> L{"DM acts within current pay cycle?"}
        L -->|"YES"| M["DM reviews: officer response, reason, shift details, break data"]
        L -->|"NO"| N["Current pay cycle closed"]
        N --> O["DM gets reminder one day before next pay cycle"]
        O --> P{"DM acts before next pay cycle?"}
        P -->|"YES"| M
        P -->|"NO"| Q["Penalty pay auto-approved"]
        M --> R{"DM Review"}
        R -->|"Approved"| S["Penalty pay added to officer upcoming pay"]
        R -->|"Rejected"| T["DM adds reason for rejection"]
        S --> U["Officer notified in MyConnect with DM response"]
        T --> U
        Q --> U
        U --> V[("Audit Storage: DM response, DM comment, penalty pay triggered, notification delivered")]
    end

    E -.->|"Handoff: exception created"| J

    classDef terminus fill:#D4EDDA,stroke:#28A745,stroke-width:2px,color:#1E4620
    classDef decision fill:#FFF3CD,stroke:#F59E0B,stroke-width:2px,color:#664D03
    classDef action fill:#CFE2FF,stroke:#0D6EFD,stroke-width:2px,color:#084298
    classDef notification fill:#FFE5CC,stroke:#FB923C,stroke-width:2px,color:#7C2D12
    classDef errorPath fill:#F8D7DA,stroke:#DC3545,stroke-width:2px,color:#58151C

    class A,G terminus
    class B,L,P,R decision
    class C,D,E,F,J,K,M,N,O,S,T,U action
    class H,V action
```

### Standard Color Palette

Append after all subgraphs and cross-subgraph edges in every flowchart. Classify every node — no node left unclassified.

| Class | Fill | Stroke | Text | Applies to |
|---|---|---|---|---|
| `terminus` | `#D4EDDA` | `#28A745` | `#1E4620` | All stadium nodes — flow start and end |
| `decision` | `#FFF3CD` | `#F59E0B` | `#664D03` | All diamond nodes — decisions and system checks |
| `action` | `#CFE2FF` | `#0D6EFD` | `#084298` | Rectangles — actions, screens, processing, routing |
| `notification` | `#FFE5CC` | `#FB923C` | `#7C2D12` | Rectangles — push notifications, in-app reminders/alerts |
| `errorPath` | `#F8D7DA` | `#DC3545` | `#58151C` | Rectangles — offline banners, cached/stale fallbacks, degraded paths |

```
classDef terminus fill:#D4EDDA,stroke:#28A745,stroke-width:2px,color:#1E4620
classDef decision fill:#FFF3CD,stroke:#F59E0B,stroke-width:2px,color:#664D03
classDef action fill:#CFE2FF,stroke:#0D6EFD,stroke-width:2px,color:#084298
classDef notification fill:#FFE5CC,stroke:#FB923C,stroke-width:2px,color:#7C2D12
classDef errorPath fill:#F8D7DA,stroke:#DC3545,stroke-width:2px,color:#58151C

class <terminus node IDs> terminus
class <decision node IDs> decision
class <action node IDs> action
class <notification node IDs> notification
class <errorPath node IDs> errorPath
```

**Classification rules:**
- `terminus` — every `(["..."])` stadium
- `decision` — every `{"..."}` diamond
- `notification` — rectangles that compose or send push notifications, or display in-app reminders/alerts to the user
- `errorPath` — rectangles that show offline banners, stale/cached data, fallback states, or blocked paths
- `action` — all remaining rectangles

### Key Patterns in the Example

- **Start/end** use stadium shape `(["..."])`
- **Decisions** use diamond `{"..."}`
- **Rich content** in action nodes: verbatim attestation text, UI affordances ("Click: YES / NO"), form fields ("Provide Reason: ___")
- **Conditional notes** in nodes: "(not shown on subsequent clock-outs)"
- **Edge labels** tell the story: "Officer clicks NO", "More than 3.5 hrs", "Less than 3.5 hrs (Skip attestation)"
- **Audit cylinder** lists every stored field
- **Cross-subgraph handoff** via dotted edge `-.->` with label
- **Time-based branching**: "DM acts within pay cycle?" YES/NO with timeout path to auto-approval
- **Notification endpoint** includes content summary

---

## Sequence Diagram

### Syntax

```
sequenceDiagram
    actor Officer
    participant MyConnect
    participant WFM

    Officer->>MyConnect: Taps Schedule tab
    MyConnect->>WFM: Fetch schedule data
    WFM-->>MyConnect: Schedule response
    MyConnect-->>Officer: Display current week

    alt Shift modified by DM
        WFM->>MyConnect: Schedule change event
        MyConnect->>Officer: Push notification
    end

    alt WFM unavailable
        MyConnect-->>Officer: Show cached schedule + stale banner
    end
```

### Sequence Diagram Constraints

- No notes (MCP does not support them)
- No color styling
- Use `actor` for people, `participant` for systems
- Use `alt`/`opt` blocks for conditional paths
- Use solid arrows (`->>`) for requests, dashed (`-->>`) for responses

---

## State Diagram

### Syntax

```
stateDiagram-v2
    [*] --> Scheduled
    Scheduled --> InProgress: Shift start time reached
    InProgress --> Worked: Shift marked complete in WFM
    Scheduled --> Modified: DM changes shift
    Modified --> Scheduled: Officer views change
    InProgress --> Overnight: Shift spans midnight
    Overnight --> Worked: Shift marked complete in WFM

    state Scheduled {
        [*] --> Default
        Default --> StartingSoon: Within 60 min of start
    }
```

### State Diagram Constraints

- No color styling
- Use `[*]` for initial/final states
- Transition labels describe the trigger event
- Composite states group related sub-states

---

## Gantt Chart

### Syntax

```
gantt
    title MySchedule Feature Timeline
    dateFormat YYYY-MM-DD
    axisFormat %b %d

    section Design
    UX wireframes           :des1, 2026-04-15, 14d
    Design review           :des2, after des1, 5d

    section Development
    FR-1 Past weeks         :dev1, after des2, 10d
    FR-2 Current week       :dev2, after des2, 10d
    FR-5 Notifications      :dev3, after dev1, 14d

    section Testing
    UAT                     :test1, after dev3, 7d
    Launch                  :milestone, after test1, 0d
```

### Gantt Constraints

- No color styling
- Use `after` for dependencies
- Use `milestone` for zero-duration markers
- `dateFormat` and `axisFormat` control date display
