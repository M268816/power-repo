# OEE2 Algorithm

## Preferred OEE
> OEE = Availability * Performance * Quality 

Availability = (Runtime - Downtime) / Total Time

Performance = (Total Widgets / (Runtime - Downtime)) / Ideal Cycle Time

Quality = Good Widgets / Total Widgets

## Millipore OEE1/OEE2 Calculations 
> OEE1 = Output / (Ideal Output * Total Runtime)

> OEE2 = Output / (Ideal Output * Planned Runtime)

The ideal output is the constraint speed for each line, the slowest process of any line. For most XL lines this is the Uson Tester.

## The authenticity issues.

I see a problem with displaying the Millipore OEE2 algorithm as a competitive and comparable data from the standard OEE model. I feel this is misdirecting our customers and our own data analysis by artificially inflating the OEE percentages. This is because the OEE2 method simplifies the process of the algorithm to only include a performance metric, not taking into account lost availability and quality.

Here's an example of line production numbers broken down between both algorithms. Let’s say XL1 is planned to run a full shift, with a planned PM and a half hour worth of mechanical issues. According to our downtime code splits, Planned Preventive Maintenance are covered under OEE1 as planned downtime, and mechanical issues are covered under OEE2 as an unplanned downtime event.

### Baseline metrics for a single shift, on a single line

Line - XL1 - 5 inch units  
Good Units - 256  
Total Units - 300  
Runtime - 8 Hours  
Unplanned Downtime - 0.5 Hours for mechanical issues  
Planned Downtime - 1 Hour for a scheduled P.M  
Total Available Time - 8 Hours  
Output - 39.3846 units/hr  
Ideal Output - 46.9 units/hr  

### Millipore OEE2

> OEE2 = Output / (Ideal Output * Planned Runtime)

> OEE2 = 256 / (46.9 * 7)

> OEE2 = 77.98%

### Standard OEE

Availability = (Runtime - Downtime) / Total Time

> A = (7 - 0.5) / 8

Performance = (Total Widgets / (Runtime - Downtime)) / Ideal Cycle Time

> P = (256 / (7 - 0.5)) / 46.9

Quality = Good Widgets / Total Widgets

> Q = 256 / 300

> OEE = 0.8125 * 0.8397 * 0.8533

> OEE = 58.22%

### Conclusion

There is a 19.76% difference between the calculation that Millipore is basing its data analysis on and the industry standard process. For efficiency analysis, this means we are misrepresenting our own data and potentially ignoring or downplaying possible problems within our processes because the OEE% are so agreeable. For outside parties who may only know of the standard OEE process, if we try and share this data within our own industry, other industry leaders, customers, or competitors, we are misrepresenting our efficiency and therefore the capacity of our processes.


# OEE2 Algorithm Breakdown.

The algorithm we use to gather and calculate OEE2 uses the same premise as the LSPS OEE2 calculation but needed to be adapted to consider the ideal output constraint variances from each catalog and line. So, as a line switches products, we need to also change the constraint for the specific catalogs that run.

To adjust for this, the ideal output is calculated for each catalog run on the line. For example, if we run a 10-inch product for 3 hours at 40 units per hour, and a 3-inch product for 4 hours at a 30 units per hour and 1 hour of planned downtime. We multiply the 3 hours of 10-inch by 40, the 4 hours of 3-inch by 30, sum them, then parse them through the OEE2 calculation afterard. The single hour of planned downtime is not added, as we only need the total planned runtime. Let’s also say the total output was only 100 units that shift as well.

> OEE2 = 100 / ((3\*40)+(4\*30))

> OEE2 = 0.4166 or 41.66% OEE

Let's say that the last hour of the shift was planned runtime, that extra hour would then be added onto the 3 inch product and counted as lost production, reducing the OEE percentage.

> OEE2 = 100 / ((40\*3)+(30\*5))

> OEE2 = 0.3703 or 37.03%

This first step described above is added to a "constraint goal" array that will be used in the calculation to represent the Ideal Ouput multiplied by Planned Runtime.

> OEE2 = Output / **(Ideal Output \* Planned Runtime)**

> OEE2 = Output / ***Constraint Goal***

Each "constraint goal" is added together like we did above before returning the percantage from the total output.

This relies on the filters given to the instructions for data collection beforehand. This means you can return a percentile of a single line, for a single day; or every line for months. Because of this constraint agnostic behaviour, the data *should* be extreamly reliable.

The problem with this method is the data collection itself. It relies on an operator facing data entry method with only volunteer verification of the data from leads.


## Collecting Shift Specific OEE2 Data

To parse the data for OEE2 as accurately as possible, data must be collected for each shift, line, and catalog. The most important being each catalog, as each has its own operational constraint. From those filters we collect the unit output, constraint data, and runtime data.

``` cs
/*Gather Shift Specific OEE Data*/
Set(varLoading,{Visible: true, Value: 60, Text: "Gathering OEE2 Data for Shifts"});
/*Init this collection here or powerapps breaks*/
ClearCollect(collectShiftOEE2Data, {shift: "A"});
/*
    For each Shift,
    for each Line,
    for each Catalog,
    collect outputs, constraints, and runtime.
*/
Clear(collectShiftOEE2Data);
With(
    {
        theseLines:
            If(
                oee_line.Selected.Value = "All",
                ["XL1", "XL2", "XL3", "XL4", "XL5", "SSC", "SSC2", "XLT", "XLT2", "XLT3"],
                oee_line.Selected.Value = "Only SSCs",
                ["SSC", "SSC2"],
                oee_line.Selected.Value = "Only XLs",
                ["XL1", "XL2", "XL3", "XL4", "XL5"],
                oee_line.Selected.Value = "Only XLTs",
                ["XLT", "XLT2", "XLT3"],
                [oee_line.Selected.Value]
            ),
        theseCatalogs:
            If(
                oee_line.Selected.Value = "All",
                ["51", "02", "03", "04", "05", "10", "015", "003", "006", "1F", "1H", "1S", "1T", "1Z", "2F", "2H", "2S", "2T", "2Z", "3F", "3H", "3S", "3T", "3Z"],
                oee_line.Selected.Value = "Only SSCs",
                ["015", "003", "006"],
                oee_line.Selected.Value = "Only XLs",
                ["51", "02", "03", "04", "05", "10"],
                oee_line.Selected.Value = "Only XLTs",
                ["1F", "1H", "1S", "1T", "1Z", "2F", "2H", "2S", "2T", "2Z", "3F", "3H", "3S", "3T", "3Z"],
                ["51", "02", "03", "04", "05", "10", "015", "003", "006", "1F", "1H", "1S", "1T", "1Z", "2F", "2H", "2S", "2T", "2Z", "3F", "3H", "3S", "3T", "3Z"]
            ),
        theseShifts:
            ["A","B","C"]
    },
    ForAll(theseShifts,
        With({thisShift: ThisRecord.Value},
            ForAll(theseLines,
                With({thisLine: ThisRecord.Value},
                    ForAll(theseCatalogs,
                        With({thisCatalog: ThisRecord.Value},
                            If(
                                Sum(
                                    Filter(collectProduction,
                                        And(
                                            hour_starting >= DateAdd(oee_start_date.SelectedDate, -1, TimeUnit.Hours),
                                            hour_ending <= DateAdd(oee_end_date.SelectedDate, 23, TimeUnit.Hours)
                                        ),
                                        line = thisLine,
                                        size = thisCatalog,
                                        shift = thisShift
                                    ),
                                    amount_built
                                ) > 0,
                            
                                Collect(collectShiftOEE2Data,
                                    {
                                        shift: thisShift,
                                        
                                        line: thisLine,
                                        
                                        catalog: thisCatalog,
                                        
                                        constraint_setting:
                                            IfError(
                                                Average(
                                                    Filter(Goal_Settings,
                                                        Line.Value = thisLine,
                                                        Size.Value = thisCatalog,
                                                        Constraint_Setting > 0
                                                    ), Constraint_Setting
                                                ),
                                                0
                                            ),
                                            
                                        output:
                                            Sum(
                                                Filter(collectProduction,
                                                    And(
                                                        hour_starting >= DateAdd(oee_start_date.SelectedDate, -1, TimeUnit.Hours),
                                                        hour_ending <= DateAdd(oee_end_date.SelectedDate, 23, TimeUnit.Hours)
                                                    ),
                                                    line = thisLine,
                                                    size = thisCatalog,
                                                    shift = thisShift
                                                ),
                                                amount_built
                                            ),
                                        
                                        runtime:
                                            (
                                                /*Collect Runtime Minutes From Production*/
                                                (CountRows(
                                                    Filter(collectCombinedData,
                                                        amount_built > 0,
                                                        line = thisLine,
                                                        size = thisCatalog,
                                                        shift = thisShift
                                                    )
                                                ) * 60) +
                                                /*Collect Runtime Minues From Downtime*/
                                                Sum(
                                                    Filter(collectCombinedData,
                                                        line = thisLine,
                                                        size = thisCatalog,
                                                        shift = thisShift,
                                                        Not(reason = "Planned Downtime" || reason = "No Scheduled Work" || reason = "Engineering DT")
                                                    ),
                                                    total
                                                )
                                            )/60,
                                    
                                        constraint_goal:
                                            /*Constraint *  Runtime*/
                                            /*Constraint*/
                                            IfError(
                                                Average(
                                                    Filter(Goal_Settings,
                                                        Line.Value = thisLine,
                                                        Size.Value = thisCatalog,
                                                        Constraint_Setting > 0
                                                    ), Constraint_Setting
                                                ),
                                                0
                                            ) *
                                            /* Runtime */
                                            (
                                                /*Collect Runtime Minutes From Production*/
                                                (CountRows(
                                                    Filter(collectCombinedData,
                                                        amount_built > 0,
                                                        line = thisLine,
                                                        size = thisCatalog,
                                                        shift = thisShift
                                                    )
                                                ) * 60) +
                                                /*Collect Runtime Minues From Downtime*/
                                                Sum(
                                                    Filter(collectCombinedData,
                                                        line = thisLine,
                                                        size = thisCatalog,
                                                        shift = thisShift,
                                                        Not(reason = "Planned Downtime" || reason = "No Scheduled Work" || reason = "Engineering DT")
                                                    ),
                                                    total
                                                )
                                            ) / 60
                                    }
                                )
                            )
                        )
                    )
                )
            )
        )
    )
);
```

The constraint setting is collected through a database that holds all constraint data per catalog. This is collected using an average bacause you can select multiple lines using the controls. Selecting a single line will return the exact amount, while selecting "Only SSCs" will return an average.

``` cs
constraint_setting:
    IfError(
        Average(
            Filter(Goal_Settings,
                Line.Value = thisLine,
                Size.Value = thisCatalog,
                Constraint_Setting > 0
            ), Constraint_Setting
        ),
        0
    ),
```

The output is then collected by gathering the sum of the built units.

``` cs
output:
    Sum(
        Filter(collectProduction,
            And(
                hour_starting >= DateAdd(oee_start_date.SelectedDate, -1, TimeUnit.Hours),
                hour_ending <= DateAdd(oee_end_date.SelectedDate, 23, TimeUnit.Hours)
            ),
            line = thisLine,
            size = thisCatalog,
            shift = thisShift
        ),
        amount_built
    ),
```

The runtime is calculated by finding the sum of all recorded runtime and outlying downtime that does not fall within the already recorded runtime or any OEE1 downtime codes.

``` cs
runtime:
    (
        /*Collect Runtime Minutes From Production*/
        (CountRows(
            Filter(collectCombinedData,
                amount_built > 0,
                line = thisLine,
                size = thisCatalog,
                shift = thisShift
            )
        ) * 60) +
        /*Collect Runtime Minues From Downtime*/
        Sum(
            Filter(collectCombinedData,
                line = thisLine,
                size = thisCatalog,
                shift = thisShift,
                Not(reason = "Planned Downtime" || reason = "No Scheduled Work" || reason = "Engineering DT")
            ),
            total
        )
    )/60,
```

We then find a constraint goal to simplify the alrogithm while calculating OEE2. Within the OEE2 calculation this is determined to be the the Ideal Ouput multiplied by the Planned Runtime. And the following acts as the same calculation.

```cs
constraint_goal:
    /*Constraint *  Runtime*/
    /*Constraint*/
    IfError(
        Average(
            Filter(Goal_Settings,
                Line.Value = thisLine,
                Size.Value = thisCatalog,
                Constraint_Setting > 0
            ), Constraint_Setting
        ),
        0
    ) *
    /* Runtime */
    (
        /*Collect Runtime Minutes From Production*/
        (CountRows(
            Filter(collectCombinedData,
                amount_built > 0,
                line = thisLine,
                size = thisCatalog,
                shift = thisShift
            )
        ) * 60) +
        /*Collect Runtime Minues From Downtime*/
        Sum(
            Filter(collectCombinedData,
                line = thisLine,
                size = thisCatalog,
                shift = thisShift,
                Not(reason = "Planned Downtime" || reason = "No Scheduled Work" || reason = "Engineering DT")
            ),
            total
        )
    ) / 60
```

## Calculating the Shift Specific OEE2

The collected data is then calculated through the OEE2 algorithm.

``` cs
/*Calculate Shift Specific OEE Data*/
Set(varLoading,{Visible: true, Value: 65, Text: "Calculating OEE2 for Shifts"});
Clear(collectShiftOEE);
ForAll(collectShiftSchema,
    Collect(collectShiftOEE,
        {
            constraint_average:
                IfError(
                    Average(
                        Filter(collectShiftOEE2Data,
                            output > 0 ,
                            shift = SCH_Shift
                        ),
                        constraint_setting
                    ),
                    0
                ),

            constraint_goal:
                IfError(
                    Sum(
                        Filter(collectShiftOEE2Data,
                            output > 0,
                            shift = SCH_Shift
                        ),
                        constraint_goal
                    ),
                    0
                ),
            
            downtime_planned:
                Sum(
                    Filter(locDefaultDowntimeFilter,
                        shift = SCH_Shift,
                        reason = "No Scheduled Work" || reason = "Engineering DT" || reason = "Planned Downtime"
                    ),
                    total
                ),

            OEE2:
                IfError(
                    Round(
                        Sum(
                            Filter(collectShiftOEE2Data, output > 0, shift = SCH_Shift),
                            output
                        ) /
                        Sum(
                            Filter(collectShiftOEE2Data, output > 0, shift = SCH_Shift),
                            constraint_goal
                        ) * 100,
                        2
                    ),
                    0
                ),

            output:
                IfError(
                    Sum(
                        Filter(collectShiftOEE2Data,
                            output > 0,
                            shift = SCH_Shift
                        ),
                        output
                    ),
                    0
                ),

            runtime_hours: 
                Sum(
                    Filter(collectShiftOEE2Data,
                        output > 0,
                        shift = SCH_Shift
                    ),
                    runtime
                ),

            runtime_total:
                (If(
                oee_line.Selected.Value = "All",
                count_of_days * 9,
                oee_line.Selected.Value = "Only SSCs",
                count_of_days * 2,
                oee_line.Selected.Value = "Only XLs",
                count_of_days * 5,
                oee_line.Selected.Value = "Only XLTs",
                count_of_days * 2,
                count_of_days
                ) * 480)/60, 
            
            shift: SCH_Shift

        }
    )
);
```

OEE2 is calculated as the sum of the unit output / the constraint goal. It is converted to a percentile and rounded to the nearest thousandth.

``` cs
OEE2:
    IfError(
        Round(
            Sum(
                Filter(collectShiftOEE2Data, output > 0, shift = SCH_Shift),
                output
            ) /
            Sum(
                Filter(collectShiftOEE2Data, output > 0, shift = SCH_Shift),
                constraint_goal
            ) * 100,
            2
        ),
        0
    ),
```

The other data collected in the intial algorithm is used to display the data on the OEE Analysis screen.

## Collecting All/Overall OEE2 Data

Collecting the OEE data works in a simmilar fashion, but without the need to distinguish between each shift. The biggest difference in this algorithm is that it collects much more "display" data. This extra data is pushed to the screen to verify the final OEE2 percentage.

``` cs
/*Gather OEE Data*/
Set(varLoading,{Visible: true, Value: 70, Text: "Gathering OEE2 Data"});
/*
    For all Lines,
    For all Catalogs,
    collect output, constraints, and runtime
*/
Clear(collectOEE2Data);
With(
    {
        theseLines:
            If(
                oee_line.Selected.Value = "All",
                ["XL1", "XL2", "XL3", "XL4", "XL5", "SSC", "SSC2", "XLT", "XLT2", "XLT3"],
                oee_line.Selected.Value = "Only SSCs",
                ["SSC", "SSC2"],
                oee_line.Selected.Value = "Only XLs",
                ["XL1", "XL2", "XL3", "XL4", "XL5"],
                oee_line.Selected.Value = "Only XLTs",
                ["XLT", "XLT2", "XLT3"],
                [oee_line.Selected.Value]
            ),
        theseCatalogs:
            If(
                oee_line.Selected.Value = "All",
                ["51", "02", "03", "04", "05", "10", "015", "003", "006", "1F", "1H", "1S", "1T", "1Z", "2F", "2H", "2S", "2T", "2Z", "3F", "3H", "3S", "3T", "3Z"],
                oee_line.Selected.Value = "Only SSCs",
                ["015", "003", "006"],
                oee_line.Selected.Value = "Only XLs",
                ["51", "02", "03", "04", "05", "10"],
                oee_line.Selected.Value = "Only XLTs",
                ["1F", "1H", "1S", "1T", "1Z", "2F", "2H", "2S", "2T", "2Z", "3F", "3H", "3S", "3T", "3Z"],
                ["51", "02", "03", "04", "05", "10", "015", "003", "006", "1F", "1H", "1S", "1T", "1Z", "2F", "2H", "2S", "2T", "2Z", "3F", "3H", "3S", "3T", "3Z"]
            )
    },
    ForAll(theseLines,
        With({thisLine: ThisRecord.Value},
            ForAll(theseCatalogs,
                With({thisCatalog: ThisRecord.Value},
                    If(
                        Sum(
                            Filter(collectProduction,
                                And(
                                    hour_starting >= DateAdd(oee_start_date.SelectedDate, -1, TimeUnit.Hours),
                                    hour_ending <= DateAdd(oee_end_date.SelectedDate, 23, TimeUnit.Hours)
                                ),
                                line = thisLine,
                                size = thisCatalog
                            ),
                            amount_built
                        ) > 0,
                    
                        Collect(collectOEE2Data,
                            {
                                line: thisLine,
                                
                                catalog: thisCatalog,
                                
                                constraint_setting:
                                    IfError(
                                        First(Filter(Goal_Settings, Line.Value = thisLine, Size.Value = thisCatalog)).Constraint_Setting,
                                        0
                                    ),
                                    
                                output:
                                    Sum(
                                        Filter(collectProduction,
                                            And(
                                                hour_starting >= DateAdd(oee_start_date.SelectedDate, -1, TimeUnit.Hours),
                                                hour_ending <= DateAdd(oee_end_date.SelectedDate, 23, TimeUnit.Hours)
                                            ),
                                            line = thisLine,
                                            size = thisCatalog
                                        ),
                                        amount_built
                                    ),
                                
                                runtime:
                                    (
                                        /*Collect runtime minutes from production*/
                                        (CountRows(
                                            Filter(collectCombinedData,
                                                amount_built > 0,
                                                line = thisLine,
                                                size = thisCatalog
                                            )
                                        ) * 60) +
                                        /*Collect runtime minutes from downtime*/
                                        Sum(
                                            Filter(collectCombinedData,
                                                line = thisLine,
                                                size = thisCatalog,
                                                Not(reason = "Planned Downtime" || reason = "No Scheduled Work" || reason = "Engineering DT")
                                            ),
                                            total
                                        )
                                    )/60,
                            
                                constraint_goal:
                                    /*Constraint *  Runtime*/
                                    /*Constraint*/
                                    IfError(
                                        First(Filter(Goal_Settings, Line.Value = thisLine, Size.Value = thisCatalog)).Constraint_Setting,
                                        0
                                    ) *
                                    /* Runtime */
                                    (
                                        /*Collect runtime minutes from production*/
                                        (CountRows(
                                            Filter(collectCombinedData,
                                                amount_built > 0,
                                                line = thisLine,
                                                size = thisCatalog
                                            )
                                        ) * 60) +
                                        /*Collect runtime minutes from downtime*/
                                        Sum(
                                            Filter(collectCombinedData,
                                                line = thisLine,
                                                size = thisCatalog,
                                                Not(reason = "Planned Downtime" || reason = "No Scheduled Work" || reason = "Engineering DT")
                                            ),
                                            total
                                        )
                                    ) / 60
                            }
                        )
                    )
                )
            )
        )   
    )
);

/*Collect OEE2*/
Set(varLoading,{Visible: true, Value: 75, Text: "Calculating OEE2"});
Clear(collectOEE2);
With(
    {
        constraint_average:
            IfError(
                Average(Filter(collectOEE2Data, constraint_setting > 0),
                    constraint_setting
                ),
                0
            ),

        constraint_goal:
            IfError(
                Sum(collectOEE2Data,
                    constraint_goal
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
                1440 * 9 * count_of_days,
                oee_line.Selected.Value = "Only SSCs",
                1440 * 2 * count_of_days,
                oee_line.Selected.Value = "Only XLs",
                1440 * 5 * count_of_days,
                oee_line.Selected.Value = "Only XLTs",
                1440 * 3 * count_of_days,
                1440 * count_of_days
            ),
        
        total:
            Sum(
                locDefaultProductionFilter,
                reject_cartridges + reject_units + amount_built
            ),
        
        uptime:
            IfError(
                Sum(collectOEE2Data,
                    runtime
                ),
                0
            )
    },
    Collect(collectOEE2,
        {
            availability:
                IfError(
                    Round(
                        (uptime / (runtime_total / 60)) * 100,
                        0
                    ),
                    0
                ),
            
            constraint_goal: constraint_goal,

            constraint_average: constraint_average,
            
            downtime_planned:
                Sum(
                    Filter(locDefaultDowntimeFilter,
                        reason = "No Scheduled Work" || reason = "Engineering DT" || reason = "Planned Downtime"
                    ),
                    total
                )*1,
            
            downtime_unplanned:
                Sum(
                    Filter(locDefaultDowntimeFilter,
                        Not(reason = "No Scheduled Work" || reason = "Engineering DT" || reason = "Planned Downtime")
                    ),
                    total
                )*1,
                            
            OEE2:
                IfError(
                    Round(
                        (output / constraint_goal),
                        2
                    ) * 100,
                    0
                ),

            
            output: output,
            
            performance:
                IfError(
                    Round(
                        (output / constraint_goal) * 100,
                        0
                    ),
                    0
                ),
            
            rejects:
                Sum(
                    locDefaultProductionFilter,
                    reject_cartridges + reject_units
                ),
            
            runtime_total: runtime_total/60,
            
            uptime: uptime,
            
            target:
                If(
                    oee_line.Selected.Value = "All",
                    ((varWeeklySSCTarget + varWeeklyXLTarget + varWeeklyXLTTarget)/5) * count_of_days,
                    oee_line.Selected.Value = "Only SSCs",
                    (varWeeklySSCTarget/5) * count_of_days,
                    oee_line.Selected.Value = "Only XLs",
                    (varWeeklyXLTarget/5) * count_of_days,
                    oee_line.Selected.Value = "Only XLTs",
                    (varWeeklyXLTTarget/5) * count_of_days,
                    "SSC" in oee_line.Selected.Value,
                    ((varWeeklySSCTarget / 2)/5) * count_of_days,
                    "XLT" in oee_line.Selected.Value,
                    ((varWeeklyXLTTarget / 2)/5) * count_of_days,
                    ((varWeeklyXLTarget / 5)/5) * count_of_days
                ),
            
            total: total,
            
            yield:
                IfError(
                    Round(
                        (output / total) * 100,
                        0
                    ),
                    0
                )
            
        }
    )
);
```

This algoritm collects all constraint data for evey line and catalog, so when gathering the overall OEE it *DOES NOT* average out the constraint data. This makes the overall OEE2 algorithm the most accurate way to display OEE2.

```cs
constraint_setting:
    IfError(
        First(Filter(Goal_Settings, Line.Value = thisLine, Size.Value = thisCatalog)).Constraint_Setting,
        0
    ),
```