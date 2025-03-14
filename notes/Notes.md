# Todo

## Shared Account Remediation

Risk assessment form needed to continue.
    - S Account Numbers needed to complete form.
        - S Account numbers cannot be accounted for.
    - Asset IDs needed
        - Opti
        - Main Room
        - Finishing Cells
        - Encapsulation
        - Express
        - Lamination

## Encapsulation Staffing Challenge

Determine the staffing needs through Catalog run percentages by line.

Determine total demand demonstrated by output per shift.

Data points/Headers to consider:
 - Catalog
 - Average Good Units per Lot Run
 - Line
 - Date
 - Count of Catalog per Line

## Front End Pleater DMS

### Aervent and High Area Calculations

Completed

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
    FE_OEE2_Trends

Solidify Constraint Database perm location.
    FE_Constraints
        Supplemented with the Pleater Speed collection.

Solidify SlitPostPleat Database perm location.
    FE_SlitsPostPleat


### PowerApp Building

Permanent home for databases needed. Can run from my account for a while, but
should be offloaded onto its own sharepoint environment.

DOR and tier 2 reporting, needs scope definition from Jonathan

#### Home
    Completed
#### Outputs
    Completed
#### Downtime
    Completed
#### OEE
    Completed
#### Loss
    Completed
#### Trend
    Completed
#### Bugs
    Completed
#### Daily Operations Report 
Scope definition needed from management.
#### Tier 2
Scope definition needed from management.
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

Databases being built by Michelle Thompson

Alpha build can begin soon.

# Notes

## Footage Algorithm
> (Ending S# - Beginning S# + 1) * ((Pleats per Unit * Pleat Height) / 6)

(73 + 1) * ((127 * 0.455) / 6)

(74) * (9.6308)

712.6792 ft


## Stable PowerApp Versions
Encap Production = 1303
Encap Management = ????
Encap Accountability = ????
FE DataBridge DMS = ????