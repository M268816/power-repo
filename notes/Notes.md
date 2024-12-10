# Roll Data Pleater Speed

# 11/18/24 Meeting Notes

> OEE2 = Total Packs / Planned Packs

Total Packs = (Ending S# - Beginning S# + 1) \
Total Packs = (1156 - 1001 + 1) \
Total Packs = 156

Planned Packs = (Packs Per Hour * Planned Runtime Hours) \
Planned Packs = (28.3464 * 7) \
Planned Packs = 198.4248

> OEE2 = 156 / 198.4248
> OEE2 = 79.0174%

Pack Per Hour = Pleats Per Hour / Pleats Per Pack \
Pleats Per Hour = Pleats Per Minute * 60 (3600 or 7200)

> Main Line - 60 ppm - EF GH \
> Opti - 60ppm - LM RS \
> HighSpeed - 120ppm - WX YZ \
> Express - 120ppm - 12 34 JK* NO PQ

> Design for 80%, approx Less 10%, Excludes GH aervent and LM/RS slit post pleat also JK high area, revisit \
> Exclude V Line, GH Aervent, Lm/RS Slit post pleat, JK High Area

Pack Per Hour = Pleats Per Hour / Pleats Per Unit \
Pack Per Hour = 3600 / 127 \
Pack Per Hour = 28.3464 Packs Per Hour

> Per Pleater Side, Team has the option to run one or both side for volume reqs \
> Split Operators per line \
> Hours obtained, linear? E and F or EF?

## Now Calculate OEE for Multiple Catalogs?

> NOT NEEDED IF RUNNING FOR SINGULAR LINE

> Overall OEE2 = Total Good Packs Per Lane / Total Planned Packs Per Lane

Line E = 3600 Pleats Per Hour, 127 Pleats Per Pack, 28.3464 Planned Packs, 226.7712 Planned Packs per Hour, 50 Completed Packs, 8 Hour Runtime \
Line F = 3600 Pleats Per Hour, 127 Pleats Per Pack, 28.3464 Planned Packs, 226.7712 Planned Packs per Hour, 75 Completed Packs, 8 Hour Runtime

Line N = 7200 Pleats Per Hour, 107 Pleats Per Pack, 67.2897 Planned Packs, 336.4485 Planned Packs per Hour, 100 Completed Packs, 5 Hour Runtime \
Line O = 7200 Pleats Per Hour, 107 Pleats Per Pack, 67.2897 Planned Packs, 538.3176 Planned Packs per Hour, 100 Completed Packs, 8 Hour Runtime

Total Packs = 325 \
Planned Packs = 1328.3085

OEE2 = 325 / 1328.3085 \
OEE2 = 24.4672%

# Notes Before 11/19/24

Collect all data form Master Roll #


PROBLEM! I received an email with this warning on 15-OCT
Your flow has used more than 80% of its Power Platform Requests (https://aka.ms/pa-ppr) limit in the past 24 hours. The performance is currently not impacted as it is below limits. But if the usage grows, further actions may be throttled or slowed down. Power Platform Requests used: 8197, Power Platform Requests transition limit: 10000.

(https://learn.microsoft.com/en-us/power-automate/limits-and-config#power-platform-request-limits)

[Current] Power Automate Free - 6k per user- 10k per cloud flow

Power Automate Premium - 40k per user -	200k per cloud flow

Power Apps Premium - 40k per user	200k per cloud flow

![Plan Tiers](/ref-images/Plan_teirs.PNG)

![Transfer Limits](/ref-images/CRUD%20limits.PNG)

Bad news, free plans will not be enough to capture all CRUD api calls for power automate, good news, we only need to upgrade one level to account for Encap and FE data collection to go from 10,000 to 200,000 calls per 24 hrs.

# Todo
Pleater Downtime collection pulls in a crazy amount of short stop data
    cull data into single entry per day? designate with 'SS#Date'?
    for each file    
        for each line
            for each day
                sum all Short Stop
                    make a new entry called 'SS#2024-10-15' to reduce record count

Pleater Downtime collection does not contain lot info
    incorporation into my current OEE2 formulas will need refactoring

Move csv raspi data push to onedrive location

Connect csv flow to perm location

ONLY NEED TO PULL DATA FOR OEE CALC, USE QUERY TO PULL RELEVANT DATA, CONNECT TO SP LiST, USE 2ND LIST TO STORE CALCULATIONS?


https://support.microsoft.com/en-us/office/get-started-migrate-access-data-to-dataverse-013c8bab-7737-46ca-ad2e-892bbf26287d

Production facing PowerApp can then be scrapped
    all inputs will now be manual or entered through access
    functionality found in encapsulation can be determined after setup of OEE app.
        priority one, get OEE running.

Management app needs to be built - /*WIP*/
    proper data analysis formulas need to be written for OEE view
        properly connected sharepoint lists will then have access to parse this data
        bower bi tiles will be avaiable for visualisations

Power Bi models need to have dashboards
    data visualizations need to be added to dashboards as tiles
    tiles can then be imported to powerapps
        powerapps power bi integration needs users to have a pro licence
            create/aquire a community service account to lower license requirements

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