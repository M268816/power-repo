# Notes
Cleared for next meeting.


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