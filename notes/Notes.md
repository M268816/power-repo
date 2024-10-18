# Notes

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