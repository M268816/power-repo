# Agressively Realistic Timeline

| Process            | Status            | Challanges        | Target Date       |
| ------------------ |:-----------------:| ----------------- |------------------:|
| PowerApp for Production | Cancelled | Time loss | --- |
| New FE Reject Database | Cancelled | Time loss | --- |
| Inital Database Setup | Cancelled | Time loss | --- |
| Custom CSV Loader Program Completed | WIP | input csv files cannot be altered, error checking required | 25 OCT 2024 |
| Access DB connection to PowerApp Established | FOCUS | All transfer methods of old data failing | 15 NOV 2024 |
| Relocate CSV outputs to cloud location | WIP | --- | 01 DEC 2024 |
| Constraint data Updated and Complete | On Hold | OEE2 algorithm inaccuracies | 17 JAN 2025 |
| PowerApp SharePoint List Databases Structured | On Hold | Pertains to progress with previous steps | 31 JAN 2025 |
| PowerApp for Management - Inital Build Completed | On Hold | Templates/formulas from Encap apps non-transferrable | 14 FEB 2025 |
| Power Bi connection to PowerApp Established | On Hold | Progress determined by dashboard configuration | 21 FEB 2025 |
| SharePoint List DB to PowerApp Data Algorithms Completed | --- | New data connections not plug and play from old system | 24 FEB 2025 |
| OEE Algorithms Completed | --- | OEE calculation vastly more complex than encapsulation, research needed | 03 MAR 2025 |
| PowerApp for Management - Alpha | --- | Bug Fixes | 10 MAR 2025 |
| PowerApp for Management - Beta | --- | Bug Fixes | 17 MAR 2025 |
| PowerApp for Management - Launch | --- | Projected Launch Day | 31 MAR 2025 |

*Subject to changes*

## Current Challanges

- Time loss due to scope change
    - The first three weeks of work on the project were essentialy scrapped as new information made all previous work obsolete.

- Time extention due to scope change
    - Preveiously aquired assets from the Encapsulation Application are non-transferrable. (Old app templates, database structure)
    - Formula and Algorithm scope has changed, more complex, non-transferrable
    - New knowlege of processes, programs and data transfer are required before actionable progress can be made. 
    - The new work constraints have created a large change of scope for the project.

- These new constraints include:
    - No new inputs for Operators
    - Working with legacy data sources, Access, CSV files
    - Legacy data structures cannot be altered, only hooked into
    - Large databases inhibit automatic information transfer and manipulation

Currently, because of the state of the data collection of downtime and line data The Front End DMS Management Suite will not have the same
functionality or useability as the Encapsualtion version of the PowerApp.

- Missing Lot Information for downtime collection
    - Downtime tracking will not be as robust as the Enap version.
    - A simple graphing version can still be made for downtime reasons, but only the built in reasons from the CSV and not the updated LSPS tracking
    - OEE2 Calculations will be simplified, robust data filtering cannot be achieved
    - A new system will need to be created to track Planned Runtime
        - Extracting the planned runtime cannot be achieved in the same way its calculated with the Encap version
- Constraint data not complete and may be invalid
    - Running the currently obtainable data from the Pleater DB incurs problems with the OEE2 calculation
    - OEE2 percentages are much higher than they should be
    - Problems may lie with the PowerApp algorithms, but from trials, constraint data seems to be the culprit.