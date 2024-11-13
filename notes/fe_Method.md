# OEE2

> OEE2 = Total Widgets / (Ideal Output * Planned Runtime)

## Gathering the information

Because PowerApps does not have a robust database structure, all data needs to be imported for manipulation in data structures called collections. Two of these collections are created when the app calls for a new set of data to manipulate. This is done on first page load, and various button presses and selections.

### Production

The first data structure that the app collects is the roll data, stored in a collection I call 'Production'. This collection is filtered by the selected dates within the app. Because of how large the dataset in the Sharepoint List is, it must also be sorted by date by most recent to increase collection speed. Big note here, because the Roll Data only collects the day of entry and not time, the data is skewed by a single hour. Processing the start and end of c shift is impossible with the current date time data format.

```cpp
ClearCollect(collectProduction,
    ForAll(
        Filter(Sort(Roll_Data_Filtered_SPL, Date, SortOrder.Descending),
            Date = locStartDate
        ),
        {
            id: Value(ThisRecord.ID),
            shift: Text(ThisRecord.Shift),
            line: Text(Upper(ThisRecord.Pleater)),
            date: DateValue(ThisRecord.Date),
            lot: Text(ThisRecord.Lot_No),
            catalog: Text(ThisRecord.Catalog),
            amount_built: Value(ThisRecord.'End Cart #') - Value(ThisRecord.'Begin Cart #') + 1,
            unit_starting: Value(ThisRecord.'Begin Cart #'),
            unit_ending: Value(ThisRecord.'End Cart #'),
            reject_pleats: Value(ThisRecord.Total_Reject_Pleats),
            pleats_per_pack: Value(ThisRecord.PleatPerPack),
            pleats_height: Value(ThisRecord.Pleat_Height)
        }
    )
);
```

### Downtime

The second data structure I create is called Downtime, also stored in a collection filtered and sorted in the same way as production. This datetime data can be collected properly, but then it would skew the data once again, so instead I conform to the date range possible with the Roll Data database. Another challenge with the database is that it also contains records for E and D shifts. Because the Roll Data only collects A B and C shifts, I need to lookup the time of the E or D shift entry post and convert it to A, B, or C shift entry instead.

```cpp
Set(varLoading,{Visible: true, Value: 20, Text: "Collecting Downtime Data"});
ClearCollect(collectDowntime,
    ForAll(
        Filter(Sort(FE_Express_DT_Events, DateTime, SortOrder.Descending),
            DateTime < DateAdd(locEndDate, 1, TimeUnit.Days),
            DateTime >= locStartDate
        ),
        {
            id: Value(ThisRecord.ID),
            csv_id: Value(ThisRecord.CSV_ID),
            shift:
                If(
                    Or(
                        ThisRecord.' Shift' = "E",
                        ThisRecord.' Shift' = "D"
                    ),
                    If(
                        And(
                            TimeValue(ThisRecord.DateTime) >= TimeValue("7:00 AM"),
                            TimeValue(ThisRecord.DateTime) < TimeValue("3:00 PM")
                        ),
                        "A",
                        And(
                            TimeValue(ThisRecord.DateTime) >= TimeValue("3:00 PM"),
                            TimeValue(ThisRecord.DateTime) < TimeValue("11:00 PM")
                        ),
                        "B",
                        "C"
                    ),
                    ThisRecord.' Shift'
                ),
            line: Text(ThisRecord.Pleater),
            date: ThisRecord.DateTime,
            reason: Text(ThisRecord.' Downtime Reason'),
            total: Value(ThisRecord.' Downtime Minutes'),
            comments: Text(ThisRecord.' Comments')
        }
    )
);
```

## Total widgets

To find the total widget part of the OEE formula, the Roll Data Access DB records a beginning and ending cartridge number. I take these numbers and retrieve an amount built from it.

``` cpp
amount_built: Value(ThisRecord.'End Cart #') - Value(ThisRecord.'Begin Cart #') + 1
```

This is complicated by the structure of the Roll Data DB, as it splits the line per lane. This means I need to collect each individual lane's cart output then combine these amount_built values into a single line record. The next piece of code is in part from a larger function, but here is the argument that collects the build amount into a variable called output we use later.

```cpp
output:
    Sum(
        Filter(locProdFilter,
            line in thisLine,       // For the line value in the line iteration, like 'E' in 'EF'
            catalog = thisCatalog
        ),
        amount_built                // Sum the amount built to combine 'E' and 'F' into 'EF'
    )
```
## Collecting the base OEE information

To collect the information for the OEE formula the Production and Downtime collections need to be collected into two separately generated data structures. One for base OEE data, and a second to gather the constraint data. These collections need to iterate over each line, each catalog and the shift.

> In this example we are only collecting overall OEE so shift data is not being separated in this case.

First I collect the base information. With a For loop, we create a data structure that PowerApps can call into itself to iterate over each lines and catalog. This is a PowerFX specific method, if we don't setup the loop in this way the conditions we try to iterate the data over will be out of 'scope' and PowerApps cannot reference them.

```cpp
/*
    For all Lines,
    For all Catalogs,
    collect output, and base constraint
*/
Clear(collectOEE2Data);
With(
    {
        theseLines:
            If(
                oee_line.Selected.Value = "All",
                Distinct(collectLineSchema, SCH_Line),
                [oee_line.Selected.Value]
            ),
        theseCatalogs: distinct_catalogs
    },
    ForAll(theseLines,
        With({thisLine: ThisRecord.Value},
            ForAll(theseCatalogs,
                With({thisCatalog: ThisRecord.Value},
```

Next I check to make sure the production data has an amount associated with it. This is because some data may come through incomplete. I use an AND operator to check and make sure the catalog has a constraint value as well. A lot of data is filtered out with this step, as a large amount of catalog/line pairings are missing constraint data.

```cpp
                    If(
                        And(
                            Sum(
                                Filter(locProdFilter,
                                    line in thisLine,
                                    catalog = thisCatalog
                                ),
                                amount_built
                            ) > 0,

                            Sum(Filter(FE_Constraints,thisCatalog = Catalog, thisLine = Line.Value),Constraint)>0
                        ),
```

I am missing line/catalog constraint parings and this causes problems with collecting a complete dataset for OEE analysis. This algorithm then can only calculate production data that has constraint data associated with it. All other data is filtered out, and thus does not represent a total representation of OEE.

> For Example, I currently have  a single constraint data point for 'WX' for catalog '110605RCVGL'. My outputs for the 6th of Novemeber show that 'WX' ran 440 units.
>
> ![alt text](./WX%20Output.PNG)
>
> But when pushed through the OEE algorithm, filtered for 'WX', it displays the OEE is at 0% for the day.
>
>![alt text](./WX%20OEE.PNG)

This next piece of the algorithm gathers the output and constraint data for each line/catalog pairing into a collection that will be used with the final OEE formula.

```cpp
                        Collect(collectOEE2Data,
                            {
                                line: thisLine,
                                
                                catalog: thisCatalog,
                                
                                constraint:
                                    IfError(
                                        First(Filter(FE_Constraints, Line.Value = thisLine, Catalog = thisCatalog)).Constraint,
                                        0
                                    ),
                                    
                                output:
                                    Sum(
                                        Filter(locProdFilter,
                                            line in thisLine,
                                            catalog = thisCatalog
                                        ),
                                        amount_built
                                    )
                            }
                        )
                    )
                )
            )
        )   
    )
);
```

### Ideal Output and Planned Runtime

This next collection uses the same strategy as before, but instead collects the 'Ideal Output * Planned Runtime' for OEE, a variable I call the constraint_goal in the algorithm. Previously for Encapsulation this was also collected in the for loop above. However because of the challenges of these databases, it needed to be compiled differently.

To increase the accuracy of OEE, I suggest in this next method that the ideal output of OEE2 must be pulled from the constraint of each catalog and line combination, then multiplied by how long that combination ran. All these catalog\constraint relationships then need to be compiled together to create a constraint goal. A per catalog and line combination that can be added together to capture the 'Ideal Output * Planned Runtime' arguments of the OEE formula. 

> OEE2 = Total Units / (Sum an array of Ideal Output * Planed Runtime)
> 
> OEE2 = 100 / ((20\*3)+(25\*5))

> OEE2 = 54.04%

With the current roll data and downtime database I cannot connect the constraint data to planned runtime. This is done with my Encapsulation algorithm by referencing the date, shift, and lot information relationships between the production and downtime entries. For FE they must be calculated separately because the downtime data only contains information attributing it to a line and shift. Without lot information on the downtime data, this makes the data connections difficult but not impossible.

Yet, the only other avenue I could travel would be trying to create relationships though pure time management. Finding relationships between when downtime was entered, and when production outputs were posted. The downtime data has proper timestamps, the roll data does not, so I cannot extrapolate those relations from time either making the relationships between production and downtime data impossible.

Instead, I changed my original methodology of this part of the OEE formula and I suggest taking the total runtime then subtract any collected planned downtime. The constraint is then averaged from the collected OEE2 data. This causes an unwanted and unavoidable skewing of overall OEE2 to the average constraint of the line rather than a perfect catalog by catalog calculation.

> OEE2 = Total Units / ((Average an array of constraints) * Planned Runtime)
> 
> OEE2 = 100 / ((20,25) \* 8)

> OEE2 = 55.56%

It's not ideal. But, from tests it works.

```cpp
Clear(collectConstraintArray);
With({theseLines:Distinct(collectOEE2Data, line)},
    ForAll(theseLines,
        With({thisLine:ThisRecord.Value},
            If(
                CountRows(Filter(collectOEE2Data, thisLine = line)) > 0,

                Collect(collectConstraintArray,
                    {
                        line: thisLine,

                        Constraint_Goal:
                            Round(
                                (
                                    ((count_of_days * 1440)
                                    - Sum(Filter(locDownFilter, thisLine = line),total))
                                    / 60
                                )
                                * Average(Filter(collectOEE2Data, thisLine = line), constraint),
                                0
                            )
                    }
                )
            )
        )
    )
);
```

The data we need to run through the basic OEE Formula is now collected. I complete the process by, again, collecting the resulting data into another data structure that holds the final OEE data. I use the With() function here to make the creation of OEE more readable.

```cpp
/*Collect OEE2*/
Set(varLoading,{Visible: true, Value: 75, Text: "Calculating OEE2"});
Clear(collectOEE2);
With(
    {
        constraint_average:
            IfError(
                Average(Filter(collectOEE2Data, constraint > 0),
                    constraint
                ),
                0
            ),

        constraint_goal:
            IfError(
                Sum(collectConstraintArray,
                    Constraint_Goal
                ),
                0
            ),

        output:
            IfError(
                Sum(collectOEE2Data,
                    output
                ),
                0
            ),

        runtime_total:
            If(
                oee_line.Selected.Value = "All",
                1440 * 14 * count_of_days,
                1440 *  count_of_days
            ) / 60
    },
    Collect(collectOEE2,
        {          
            OEE2: // This collects our overall OEE2 percentage. It is most accurate with single lines selected in the filters.
                IfError(
                    Round((output/constraint_goal)*100,0),
                    0
                ),

            total_units: output, // The total unit output

            reject_pleats: Sum(locProdFilter, reject_pleats), // Currently all reject data is captured as pleats.

            constraint_goal: constraint_goal, // How many units are considered the Ideal Output by the amount of time selected, minus downtime.

            target_units: constraint_average * runtime_total, // This is usually calculated with a planning goal setting, but currently just uses the constraint data
            
            downtime_planned: // The amount of planned downtime within the selected date range.
                Round(
                    Sum(
                        Filter(locDownFilter,
                            reason = "No Scheduled Work" || reason = "Engineering DT" || reason = "Planned Downtime" || reason = "Did Not Run"
                        ),
                        total
                    )*1,
                    0
                ),
            
            downtime_unplanned: // The amount of unplanned downtime within the selected date range.
                Round(
                    Sum(
                        Filter(locDownFilter,
                            Not(reason = "No Scheduled Work" || reason = "Engineering DT" || reason = "Planned Downtime" || reason = "Did Not Run")
                        ),
                        total
                    )*1,
                    0
                ),

            possible_runtime: runtime_total // The total amount of runtime possible for each line by the selected date range.
            
        }
    )
);
```

# Conclusion

With what I'm trying to accomplish, collected OEE from the current databases is troublesome at best and misleading always. Because of the challenges of data retrieval and missing constraint data, the usefulness of this tool is highly questionable without a complete constraint dataset and/or database restructure. This is also under the assumption that the cart data that i'm pulling for unit counts is correct and operators enter it accurately.

This can be seen when selecting filters with bad data. Even with all the validation, duct tape, and bubblegum that I use to clean and thoroughly inspect data for consistent OEE calculations, the state of the databases contort and disturb the algorithm to vast inaccuracies when erroneous data is passed into the algorithm. 

> This is data from the 4th of November, this day has information that conforms with the OEE algorithm.

![alt text](OEE1.PNG)


> This is data from the 7th of October, Because of all the glue holding this OEE together, I cant pinpoint what is the main cause of this problem, but the constraint data is lower than it should be, and the output data is higher.

![alt text](OEE2.PNG)

As a precaution against these database problems, stretching myself thin a little bit to be honest, I have also been developing a backup deliverable that works the same as the Encapsulation version and only relies on sharepoint lists and manual operator entries. This would mean another satellite system in our ecosystem, another point of entry for operators, and another management requirement from leads and supervisors to review the manual data entries, but I would rather be able to deliver a working finished product rather than none at all.

Both the data retrieval and manual method applications have been stripped of all other functionality to develop them in tandem.