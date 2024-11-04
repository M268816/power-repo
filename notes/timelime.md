# Aggressively Realistic Timeline

## High Level
| Process            | Status            | Target Date       | Completion Date   |
| ------------------ |:-----------------:|------------------:| ----------------- |
| Custom Data Retrieval  | Final Testing | 01 DEC 2024 | --- |
| PowerApp Initial Build | WIP | 31 DEC 2024 | --- |
| Backup Deliverables - Manual Method | Alpha | 31 JAN 2025 | --- |
| Databases Fully Established | WIP | 14 FEB 2025 | --- |
| Service Computer Setup | On Hold | 24 FEB 2025 | --- |
| OEE Algorithms Completed | --- | 03 MAR 2025 | --- |
| PowerApp Launch | --- | 31 MAR 2025 | --- |

## Low Level
| Process            | Status            | Target Date       | Challenges        |
| ------------------ |:-----------------:|------------------:| ----------------- |
| PowerApp for Production | Cancelled | --- | Time loss |
| New FE Reject Database | Cancelled | --- | Time loss |
| Initial Database Setup | Cancelled | --- | Time loss |
| Custom CSV Loader Program - Flet | Completed | 25 OCT 2024 | Pleaters loads data 15-20 mins late? |
| Custom CSV Loader Program - CLI | Completed | 25 OCT 2024 | Pleaters loads data 15-20 mins late? |
| Access DB connection to PowerApp Established | Completed | 15 NOV 2024 | --- |
| Complete Constraint Data | On Hold | 17 JAN 2025 | --- |
| Backup Deliverable - Production | Alpha | 31 JAN 2025 | Time loss |
| Backup Deliverable - Management | Alpha | 31 JAN 2025 | Time loss |
| Data Connections Established - Initial | On Hold | 31 JAN 2025 | --- |
| PowerApp for Management - Initial Build | WIP | 14 FEB 2025 | --- |
| Power Bi connection to PowerApp Established | Cancelled | 21 FEB 2025 | --- |
| Service PC Setup | On Hold | 24 FEB 2025 | --- |
| Data Connections Established - Final | --- | 24 FEB 2025 | --- |
| OEE Algorithms Completed | WIP | 03 MAR 2025 | --- |
| PowerApp for Management - Alpha | --- | 10 MAR 2025 | Bug Fixes |
| PowerApp for Management - Beta | --- | 17 MAR 2025 | Bug Fixes |
| PowerApp for Management - Launch | --- | 31 MAR 2025 | Projected Launch Day |


*Subject to changes*

## Current Challenges

- Time loss due to scope change
    - The first three weeks of work on the project were essentially scrapped as new information made all previous work obsolete.

- Time loss due to SADM account problems 

- Time extension due to scope change
    - Previously acquired assets from the Encapsulation Application are non-transferrable. (Old app templates, database structure)
    - Formula and Algorithm scope has changed, more complex, non-transferrable
    - New knowledge of processes, programs and data transfer are required before actionable progress can be made. 
    - The new work constraints have created a large change of scope for the project.

- These new project constraints include:
    - No new inputs for Operators
    - Working with legacy data sources, Access, CSV files
    - Legacy data structures cannot be altered, only hooked into
    - Large databases inhibit automatic information transfer and manipulation

Currently, because of the state of the data collection of downtime and line data The Front End DMS Management Suite will not have the same
functionality or useability as the Encapsulation version of the PowerApp.

- Missing Lot Information for downtime collection
    - Downtime tracking will not be as robust as the Encapsulation version.
    - A simple graphing version can still be made for downtime reasons, but only the built in reasons from the CSV and not the updated LSPS tracking
    - OEE2 Calculations will be simplified, robust data filtering cannot be achieved
    - A new system will need to be created to track Planned Runtime
        - Extracting the planned runtime cannot be achieved in the same way its calculated with the Encapsulation version

- Constraint data not complete
    - Data pulled from databases cannot be parsed though OEE algorithm without constraint data.
    - OEE2 will not accurately reflect data from all lines.

- Backup Deliverable
    - Current access and csv databases and the bridge solutions are too incomplete and unpredictable to affirm completion of a semi-automatic DMS system
    - Creating a backup deliverable with Manual Inputs and Sharepoint Databases
    - Time Loss