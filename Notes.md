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

Because of all the limitations that power suite data limits are imposing, I suggest we complete this project as best we can, then either change the way we collect data, posting all gathered raspi data/etc directly to  sharepoint lists or dataverse, or re-start/continue the work stephen had started building an in house application using local sql and a web-app. The limitations of expanding this project for a site wide solution for OEE management is not sustainable with current work-arounds.

My manual entry apps for all data would be expandable, but comes with data validity issues. Becasue of the constraints of auto collection through current raspi systems, flows and custom apps at this time a sitewide expansion of this system seems unobtainbale.


# Todo
!!! ERRORS !!! - /*FIXED?*/
    Pulling data into the sharepoint list by CSV_ID will have overlaps from each pleater file
    change flow logic to check for CSV_ID AND Pleater Asset

!!! ERRORS !!!
CSV files have invalid formatting and need to be cleaned
    check to see if these items are okay to remove from the file
    YZ - extra header
    RS - extra header
    JK - item 19113
    LM - line 16067, 16905,
    PQ - line 10349, 14543, 10840, 45300, 45301, 45260 thru 45280, 38396, 56001, 35618, 37603,
    RS - 14683
    WX - 6544, 6545, 7595

!!! POSSIBLE FUTURE ROADBLOCK !!!
Pleater Downtime collection does not contain lot info
    incorperation into my current OEE2 formulas will need refactoring

Move csv raspi data push to onedrive location - /*COMPLETED*/
    run small python program to pull most recent data from raspi
    run a flow to pull csv data from python output to sharepoint

Connect csv flow to perm location

!!! Database transfer errors !!!
Access db Roll_data columns need to be successfully transferred to sharepoint list
    sharepoint connections to and from a migrated database would work without conflict
    access db form pointers need to update to connected sharepoint db instead of roll_data db
    !!!
    New tables and connections work well, exporting and linking old tables are broken
        tried to circumvent by createing an empty table with the proper headers then exporting old data into new table
            new table failed to pull in old data. Linked table is considered read-only. cannot change read-only attribute
                2 attempts to move data over,
                20k record chunk ran for 10 minutes then crashed, ~1k itmes pulled in
                2k record chunk ran for 15 mins then crashed. ~1k items pulled in
    !!!
    Tried instead to migrate only 2024 access records to Davaverse, transfer errors and desktop app crashed, out of resources errors.

    @@@ ONLY NEED TO PULL DATA FOR OEE CALC, USE QUERY TO PULL RELAVENT DATA, CONNECT TO SP LiST, USE 2ND LIST TO STORE CALCULATIONS?


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

access to sharepoint list, query method
    link to main database to create a read-only env to manipulate
    use a query to setup a filtered version of the table, pre populated with data from the start of the year
    use the created filterd version of the table to export the table structure to sharepoint
    create a linked table, import, the sharepoint list into access.
    create a query to append the data to the linked sharepoint table
    create a VBA script to automatically update the sharepoint list with new entries when the form is submitted
        connect directly to main database?
        connect remotely, have to keep access open, script needs to run on a timer instead.