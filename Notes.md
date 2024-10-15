# Notes
PROBLEM! I received an email with this warning on 15-OCT
Your flow has used more than 80% of its Power Platform Requests (https://aka.ms/pa-ppr) limit in the past 24 hours. The performance is currently not impacted as it is below limits. But if the usage grows, further actions may be throttled or slowed down. Power Platform Requests used: 8197, Power Platform Requests transition limit: 10000.

https://learn.microsoft.com/en-us/power-automate/limits-and-config#power-platform-request-limits

License name	PPR official limit per 24 hours	PPR transition period limit per 24 hours
Power Automate Premium - 40k per user -	200k per cloud flow
Power Automate Process - 250k per license -	500k per license
Power Automate Hosted Process -	250k per license - 500k per license
Power Automate Per-user plan (legacy) -	40k per user - 200k per cloud flow
Power Automate Per-flow plan (legacy) -	250k per license - 500k per license
Power Automate Free - 6k per user- 10k per cloud flow
Office 365 - 6k per user	10k per cloud flow
Power Apps Premium - 40k per user	200k per cloud flow
Dynamics 365 professional -	40k per user	200k per cloud flow
Dynamics 365 Enterprise applications - 40k per user	200k per cloud flow
Dynamics 365 Team member - 6k per user	10k per cloud flow

![Plan Tiers](/ref-images/Plan_teirs.PNG)

![Transfer Limits](/ref-images/CRUD%20limits.PNG)

Bad news, free plans will not be enough to capture all CRUD api calls for power automate, good news, we only need to upgrade one level to account for Encap and FE data collection to go from 10,000 to 200,000 calls per 24 hrs.

Because of all the limitations that power suite data limits are imposing, I suggest we complete this project as best we can, then either change the way we collect data, posting all gathered raspi data/etc directly to  sharepoint lists or dataverse, or start/continue the work stephen had started building an in house application using local sql and a web-app. The limitations of expanding this project for a site wide solution for OEE management is not sustainable with current work-arounds.

Manual entry for all data would be expandable, but auto collection through flows and custom apps at this time seem unobtainbale.




# Todo
Move csv raspi data push to onedrive location
    run small python program to pull most recent data from raspi
    run a flow to pull csv data from python output to sharepoint

Access db Roll_data columns need to be successfully transferred to sharepoint list
    sharepoint connections to and from a migrated database whould work without conflict
    access db form pointers need to update to connected sharepoint db instead of roll_data db

Power Bi models need to have dashboards
    data visualizations need to be added to dashboards as tiles
    tiles can then be imported to powerapps
        powerapps power bi integration needs users to have a pro licence
            create/aquire a community service account to lower license requirements

Production facing PowerApp can then be scrapped
    all inputs will now be manual or entered through access
    functionality found in encapsulation can be determined after setup of OEE app.
        priority one, get OEE running.

Management app needs to be built
    proper data analysis formulas need to be written for OEE view
        properly connected sharepoint lists will then have access to parse this data
        bower bi tiles will be avaiable for visualisations