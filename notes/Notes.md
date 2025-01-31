# Todo

## Aervent and HA Calculations

ClearCollect(colAerventCatalogs,
    {Value: "CTGR01TP1"}, {Value: "CTGR02TP1"}, {Value: "CTGR03TP1"}, // Code 0
    {Value: "CTGR75S01"}, {Value: "CTGR71TP1"}, {Value: "CTGR72TP1"}, {Value: "CTGR73TP1"} // Code 7
);

ClearCollect(colHighAreaCatalogs,
    // Code 7
    {Value: "CHGE71HS3"}, {Value: "CHGE72HS3"}, {Value: "CHGE73HS3"},
    {Value: "CHVE71HS3"}, {Value: "CHVE72HS3"}, {Value: "CHVE73HS3"}
);

## Power Automate Flow Fixes

## Nephele needs review.

## Daily Operations Report / End of Day Processing

## Tier 1?

## Tier 2

- Safety
    - Safety Moments
    - Safety Incidents
    - Overdue EHS Actions
    - Upcoming EHS Actions
    - Overdue Critical PMs
- Quality
    - Deviations
    - ROEs
- Supply
    - Daily Targets
- Completions
    - Weekly Targets
- Action Tracker
    - Area
    - Downtime
    - Issue
    - Primary Action
    - Follow up Action
    - Owner
    - Due Date
    - Comments

## Tier 3

## Power Bi Integration

- Requires pro license.

# Footage Algorithm
> CHAD: (Ending S# - Beginning S# + 1) * ((Pleats per Unit * Pleat Height) / 6)

(73 + 1) * ((127 * 0.455) / 6)

(74) * (9.6308)

712.6816 ft

> PowerApp: ((End Cart # - Start Cart # + 1) * Pleats per Unit * pleat height) / 6

((73 + 1) * 127 * 0.455) / 6

(4276.09)/6

712.6816 ft

# Stable PowerApp Versions

Encap Production = 1303