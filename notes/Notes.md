# Todo

## Front End Pleater DMS

### Aervent and High Area Calculations

Completed, needs review with chad

### Power Automate Flow Fixes

Implementation needed

New power automate flow properly pulls in downtime data

### Nephele needs review

Implementation needed.

Nephele updated to pull both hourly and daily data.

Hourly Data will be pulled in by hour into sharepoint lists by
the power automate flow.

Daily data will be pulled in once a day at 11:00PM to update/catch
any errant data.

### Database Refactoring

Solidify Production Database structure, data.db transfer, and perm location.
    FE_RollData

Solidify Downtime Database structure, flow connections, and perm location.
    FE_Downtime

Solidify Trend Database perm location.
    FE_OEE2Trends

Solidify Constraint Database perm location.
    FE_Constraints
        Supplemented with the Pleater Speed collection.

Solidify SlitPostPleat Database perm location.
    FE_SlitsPostPleat


### PowerApp Building

Connect to perm databases.

Refactor naming conventions to align with design docs

Integrate new aervent calculations when pulling and parsing data

Review versioning, galleries and quickchart.io connections breaking.

Build T2 and T3 Reports.

#### Home
    Completed
#### Outputs
    Update to new data collection
    Integrate new aervent calculations
#### Downtime
    Update to new data collection
#### OEE
    Update to new data collection
    Integrate new aervent calculations
    Data Collection Review
    General Reformatting
#### Loss
    Data Collection Review
    General Reformatting
#### Trend
    Data Collection Review
    Integrate new aervent calculations
    Check on quickchart.io connection
#### Bugs
    Completed
#### Daily Operations Report 
    Full replacement for dor?
#### Tier 2
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
    - Comments### Power Bi Integration

## Encapsulation ROE/Deviation Update

Nothing yet.

# Footage Algorithm
> (Ending S# - Beginning S# + 1) * ((Pleats per Unit * Pleat Height) / 6)

(73 + 1) * ((127 * 0.455) / 6)

(74) * (9.6308)

712.6792 ft


# Stable PowerApp Versions
Encap Production = 1303
Encap Management = ????
Encap Accountability = ????
FE DataBridge DMS = ????