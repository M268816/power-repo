# OEE2

> OEE2 = Total Widgets / (Ideal Output * Planned Runtime)

## Gathering the information

Because PowerApps does not have a robust database structure, all data needs to be imported for manipulation in data structures called collections. Two of these collections are created when the app calls for a new set of data to manipulate. This is done on first page load, and various button presses and selections.

### Production

The first data structure that the app collects is the roll data, stored in a collection I call 'Production'. This collection is filtered by the selected dates within the app. Because of how large the dataset in the Sharepoint List is, it must also be sorted by date by most recent to increase collection speed.

```cpp
ClearCollect(collectProduction,
    ForAll(
        Filter(Sort(Roll_Data_Filtered_SPL, Date, SortOrder.Descending),
            Date <= DateAdd(locEndDate, 1, TimeUnit.Days),
            Date >= locStartDate
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

The second data structure I create is called Downtime, also stored in a collection filtered and sorted in the same way as production.

```cpp
ClearCollect(collectDowntime,
    ForAll(
        Filter(Sort(FE_Express_DT_Events, DateTime, SortOrder.Descending),
            DateTime >= DateAdd(locStartDate, -1, TimeUnit.Hours),
            DateTime <= DateAdd(locStartDate, 23, TimeUnit.Hours)
        ),
        {
            id: Value(ThisRecord.ID),
            csv_id: Value(ThisRecord.CSV_ID),
            shift: Text(ThisRecord.' Shift'),
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

The Roll Data Access DB records a beginning and ending cartridge number. I take these numbers and retrieve an amount built from it.

``` cpp
amount_built: Value(ThisRecord.'End Cart #') - Value(ThisRecord.'Begin Cart #') + 1
```

This is complicated by the structure of the Roll Data DB, as it splits the line per lane. This means I need to then combine these amount_built values I retrieve into a single line record. This is done farther into the algorithm, as I compress all the data into another data structure that collects the basal math for converting into OEE2, but more about that later, this is a small snip from that code.

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
## Ideal Output and Planned Runtime

The ideal output of OEE2 must be pulled from the constraint of a particular catalog, and how long that catalog ran. All these catalog\constraint relationships then need to be calculated separately to get a proper constraint per hour number. However, with current roll data and downtime data base constraints, I cannot pull the total runtime or connecting downtime for this information. Instead, I suggest that the line should run all 24 hours, then subtract any collected downtime from the total possible runtime. The constraint is then averaged from the collected OEE2 data. Using average this way lends more accuracy to single line analysis. The algorithm will only pull in the constraint for say, '110605RCVGLG' on 'EF', essentially cancelling out the average function here. When selecting multiple lines the averaging applies appropriately instead. This causes an unwanted, but unavoidable skewing of overall OEE2 to the average rather than a perfect calculation.

```cpp
Constraint_Goal:
    Round(
        (
            ((count_of_days * 1440)                                         // For each day selected multiply by 1440 minutes
            - Sum(Filter(locDownFilter, thisLine = line),total))            // Subtract, the total amount of downtime for the line in iteration
            / 60                                                            // Divide by 60, to get hours instead of minutes
        )
        * Average(Filter(collectOEE2Data, thisLine = line), constraint),    // Multiply, by the average constraint of the collected
        0                                                                   // OEE2 data in the iteration
    )
```

## Collecting the basal OEE information

To properly collect the OEE information, data from the Production and Downtime collections need to be recursively collected into two separately generated data structures. One for base OEE data, and a second to gather the constraint data. These collections need to iterate over each line, each catalog and in the case of the shift specific version of this algorithm the shift as well.

First lets start with the basic information we need. With a For loop, we create a structure that PowerApps can call into itself to determine specific lines and catalogs to iterate over.

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

Here we need to check to make sure the production data actually has an amount associated with it, as some data comes through incomplete. We use an AND operator to check and make sure the catalog has a constraint value as well.

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

This causes another problem with collecting OEE with the current databases all data cannot be parsed though the algorithm. This algorithm can only calculate production data that has constraint data associated with it. All other data is filtered out, and thus does not represent the total capacity of a selected set of data ranges.

For Example, I currently have  a single constraint data point for 'WX' for catalog '110605RCVGL'. My outputs for the 6th of Novemeber show that 'WX' ran 440 units.

![alt text](./WX%20Output.PNG)

But when pushed through the OEE algorithm show that 'WX' was a 0% OEE for the day.

![alt text](./WX%20OEE.PNG)

This next piece of the puzzle filters the data into a collection that will be used to gather the output and constraint data for specific catalogs. It collects the constraint from a Sharepoint List that houses all the current constraint data I was able to obtain thus far with the help of Jen and the total output of the catalog as well.

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

This next collection uses the same strategy as before, but instead collects the 'Ideal Output * Planned Runtime' for OEE, a variable I call the constraint_goal in the algorithm. Previously for Encapsulation this was also collected in the for loop above. The data sources between production and downtime are inconsistent and this causes a problem. The downtime data does not capture lot data. This created another level of complexity where I cannot simply capture the 'Ideal Output' by catalog and line as with everything else, but only by line meaning I would capture the same downtime data multiple times per line. Thus this step needed to be extracted from the original data filtering and instead parsed though concatenated line data. This unfortunately makes the algorithm much less accurate. Now I cannot capture the Ideal Output for each catalog for the line then iterate over each, instead it essentially averages all of the Ideal Output data.

To try and simplify it into an equation, it takes this:

> OEE2 = Total Units / (Sum an array of Ideal Output * Planed Runtime)
> 
> OEE2 = 100 / ((20\*3)+(25\*5))

> OEE2 = 54.04%

and turns it into this:

> OEE2 = Total Units / ((Average an array of constraints) * Planned Runtime)
> 
> OEE2 = 100 / ((20,25) \* 8)

> OEE2 = 55.56%

It's not ideal. But it's what I can do with what I have to work with.

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

Now that we have collected the data we need to run through the basic OEE Formula, we can complete the process by, again, collecting the resulting data into another data structure that hold the completed data. I use the With() function here to make the creation of OEE more readable. Some items are averaged to setup the view for management, but in all cases of OEE calculation I use as little averaging as possible, instead summing or concatenating data to create as accurate OEE percentages as possible.

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

            possible_runtime: runtime_total // The total amount of runtime possible for each LANE of each line, for the selected date range.
            
        }
    )
);
```

# Conclusion

Collected OEE from the current databases is troublesome at best, and misleading at worst. Because of the challenges of data retrieval and missing constraint data. The usefulness of this tool is highly questionable without a complete constraint dataset or database restructure.

As a precaution against this, I have been also developing a backup deliverable that works the same as the Encapsulation version and only relies on sharepoint lists and manual operator entries. This would mean another satellite system in our ecosystem, anther point of entry for operators, and another management requirement from leads and supervisors to review the manual data entries, like the encapsulation area has adopted.

Both the data retrieval and manual method applications have been stripped of all other functionality to develop them in tandem.
