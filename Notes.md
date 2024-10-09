# Notes

Operator Counts per line still needed from last meeting
locations for probable rejects
reasons for probable rejects
proper sort order of schedules
highlight certain schedule items?
performance wont be available until managemnt side is completed

are operator changes needed?
hourly operator change notifications, change to FE lines and times
ClearCollect(collectNotifyTimes,
    { line: ["XL1","XL2","XLT","XLT2","XLT3"], hour: [3, 8, 11, 16, 19, 23]},
    { line: ["XL3","XL4","XL5"], hour: [2, 5, 8, 10, 13, 16, 18, 21, 23]},
    { line: ["SSC","SSC2"], hour: [8, 16, 23]}
);

Problems with this new projected workload
    I dont want to dissmiss chad's work, or create more inputs for operators.
        but Integrating chad's databases into powerapps is not plug and play,
        and comes with challeneges that i've never had to face.
    This means that integrating chad's databases will take more resources
        this includes research, money and time,
        research because i need to find fixed, workarounds, proper connections for the databases.
        money becasue the best option i found is dataverse, which means premium
        liceses and connectors.
        extending the deadline dependant on how the integration goes
    porting my current powerapps knowlege for front end is fine with my current title and position
        but if we go in this direction, keeping chad's databases, i need to convay that
        becasue of the amount of work it would take to research the connections and refactor my current codebase,
        i dont feel comfortable continuing just as a tech op
        and i think i should be compensated fairly for my work.
        i currently make $24 an hour where starting hourly for a powerapp dev is double, $45-$60/hr
        if this cannot be done, i already have a full git repo of the work
        i've already done, and i can hand it off to someone who

Access does not directly connect to powerapps
    best case,
        keeping current data practices
            keeps current data history
        new production facing powerapp only records data not previously gathered form other sources.
        new management facing powerapp becomes the data analysis hub
        would need to upload the access data to the MS Dataverse, then from the Dataverse to Powerapps
        Dataverse costs $ per user.
        users can quickly increase
            currenly all managers, supers, leads, and backup leads, and all accountability personnel for 3 shifts use the management app for encap
                possible fixes are making a singlular S-account that can login to view the data
    worst case,
        all data entry becomes manual,
        all databases are returned to sharepoint lists
        all currently collected data migrated to new sharepoint lists to try and save data history


downtime csv to sharepoint transfer

csv can be transferred but no live updates

    relocate csv to s-account onedrive.
    use flow to pull data once an hour into sharepoint list
    csv too large for powerautomate 100,000 item limit
    becasue of csv format cannot filter for pulling in smaller range
        create filtered lsit in excel that pulls data from csv.
            no excel automation for 1 hr increments viable

push data to sharepoint list or dataverse table instead of csv?
    requires access and connection
    not sure how data is collected and pushed

roll data can be uploaded to sharepoint, but may need re structuring, total revamp to work with sharepoint
    or powerquery to pull only relevant data into new list connected to the access db
    exporting attempts have failed due to corrupt/wrong data entries
        dates out of range
        ID field not compatable with sharepoint ID data type

Functionality testing before trying to update and connect current access databases
    

Plan: "Burn it all Down"
    Total conversion of access and csv files to instead post to new SPlists
    save all current data, refactor to new sp Lists, continue operations on
    splist backend db

    plan for ms Dataverse fallback for increased capacity
