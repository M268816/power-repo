UpdateContext({locLoading:{Visible: true, Value: 15, Text: "Updating"}});

/*Today and Now function updates*/
Set(varNow, Now());
Set(varNowDay, Today());

/*Set Shift*/
If(
    Hour(varNow) >= 23,
    Set(varShiftSelect, "C Shift"),
    Hour(varNow) >= 15,
    Set(varShiftSelect, "B Shift"),
    Hour(varNow) >= 7,
    Set(varShiftSelect, "A Shift"),
    Set(varShiftSelect, "C Shift")
);

/*Set hourly goals per line and catalog*/
UpdateContext({locLoading:{Visible: true, Value: 16, Text: "Setting Hourly Goal"}});
With({thisSize:
        If(varProductionLine in ["SSC", "SSC2"],
            Mid(varCatalog,6,3),
            Mid(varCatalog,6,2)
        )
    },
    /* XLT Special Catalog Catch SN serial numbers */
    If(And(
            Left(varCatalog,2) = "SN",
            varProductionLine in ["XLT", "XLT2", "XLT3"]
        ),
        Set(varGoals, LookUp(Goal_Settings, And(Line.Value = varProductionLine, Size.Value = "SN")).Goal_Setting),
        Set(varGoals,LookUp(Goal_Settings, And(Line.Value = varProductionLine, Size.Value = thisSize)).Goal_Setting)
    ) 
);

/*Check logged in personnel and get labor hours.*/
UpdateContext({locLoading:{Visible: true, Value: 20, Text: "Setting Labor Hours"}});
Set(
    varLaborHours,
    /*Sum of Hours per logged in person*/
    Round(
        Sum(
            CountRows(varRunner)*8,
            CountRows(varMiddle)*8,
            CountRows(varPackager)*8,
            CountRows(varBagger)*8
        ) /
        /*Divided By total hours per line*/
        Switch(
            varProductionLine,
            "SSC", 16,
            "SSC2", 16,
            "XL1", 24,
            "XL2", 24,
            "XL3", 32,
            "XL4", 32,
            "XL5", 40,
            "XLT", 24,
            "XLT2", 24,
            "XLT3", 24,
            1
        ),
        2
    )
);
/*Returns decimal (percent) of calculated labor hours*/

/*Set goal per labor hour by multiplying line's goal by labor hour percent*/
Set(varGoalsPerLaborHours, RoundUp((varGoals * varLaborHours),0));

/*Set adjusted goal, that is, goal per labor hour plus an additional 5% increase per Leela, hardcoded for now, variable later?*/
Set(varAdjustedGoals, RoundUp(varGoalsPerLaborHours * 1.05, 0));

/*Create and reset Schema for displaying hourly informaiton*/
UpdateContext({locLoading:{Visible: true, Value: 25, Text: "Creating Hour By Hour Table"}});
ClearCollect(
    collectHourlySchema,
    {
        SCH_Hour_Starting: DateAdd(DateTime(Year(Now()),Month(Now()),Day(Now()),0,0,0), -1, TimeUnit.Hours),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),0,0,0),
        SCH_Shift_Letter: "C"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),0,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),1,0,0),
        SCH_Shift_Letter: "C"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),1,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),2,0,0),
        SCH_Shift_Letter: "C"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),2,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),3,0,0),
        SCH_Shift_Letter: "C"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),3,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),4,0,0),
        SCH_Shift_Letter: "C"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),4,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),5,0,0),
        SCH_Shift_Letter: "C"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),5,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),6,0,0),
        SCH_Shift_Letter: "C"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),6,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),7,0,0),
        SCH_Shift_Letter: "C"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),7,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),8,0,0),
        SCH_Shift_Letter: "A"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),8,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),9,0,0),
        SCH_Shift_Letter: "A"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),9,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),10,0,0),
        SCH_Shift_Letter: "A"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),10,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),11,0,0),
        SCH_Shift_Letter: "A"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),11,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),12,0,0),
        SCH_Shift_Letter: "A"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),12,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),13,0,0),
        SCH_Shift_Letter: "A"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),13,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),14,0,0),
        SCH_Shift_Letter: "A"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),14,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),15,0,0),
        SCH_Shift_Letter: "A"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),15,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),16,0,0),
        SCH_Shift_Letter: "B"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),16,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),17,0,0),
        SCH_Shift_Letter: "B"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),17,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),18,0,0),
        SCH_Shift_Letter: "B"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),18,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),19,0,0),
        SCH_Shift_Letter: "B"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),19,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),20,0,0),
        SCH_Shift_Letter: "B"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),20,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),21,0,0),
        SCH_Shift_Letter: "B"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),21,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),22,0,0),
        SCH_Shift_Letter: "B"
    },
    {
        SCH_Hour_Starting: DateTime(Year(Now()),Month(Now()),Day(Now()),22,0,0),
        SCH_Hour_Ending: DateTime(Year(Now()),Month(Now()),Day(Now()),23,0,0),
        SCH_Shift_Letter: "B"
    }
);

/*Join Schema (on visible) and Local Unit Data*/
UpdateContext({locLoading:{Visible: true, Value: 30, Text: "Joining production data into Hourly Tables"}});
ClearCollect(collectJoinedUnitDisplay,
    // Iterate through all source records and join to destination collection
    ForAll(

        // Iterate through the source collection
        collectHourlySchema,
        { 
            // Columns to appear in dataset
            ID: LookUp(collectProduction, SCH_Hour_Ending = Hour_Ending).ID,
            Catalog: LookUp(collectProduction, SCH_Hour_Ending = Hour_Ending).Catalog,
            Lot: LookUp(collectProduction, SCH_Hour_Ending = Hour_Ending).Lot,
            Line: LookUp(collectProduction, SCH_Hour_Ending = Hour_Ending).Line,
            Hour_Starting: ThisRecord.SCH_Hour_Starting,
            Hour_Ending: ThisRecord.SCH_Hour_Ending,
            Unit_Starting: LookUp(collectProduction, SCH_Hour_Ending = Hour_Ending).Unit_Starting,
            Unit_Ending: LookUp(collectProduction, SCH_Hour_Ending = Hour_Ending).Unit_Ending,
            Amount_Built: LookUp(collectProduction, SCH_Hour_Ending = Hour_Ending).Amount_Built,
            Goal: LookUp(collectProduction, SCH_Hour_Ending = Hour_Ending).Hourly_Goal,
            QA_Units: LookUp(collectProduction, SCH_Hour_Ending = Hour_Ending).QA_Units,
            Reject_Labels: LookUp(collectProduction, SCH_Hour_Ending = Hour_Ending).Reject_Labels,
            Reject_Units: LookUp(collectProduction, SCH_Hour_Ending = Hour_Ending).Reject_Units,
            Reject_Cartridges: LookUp(collectProduction, SCH_Hour_Ending = Hour_Ending).Reject_Cartridges,
            Quality: LookUp(collectProduction, SCH_Hour_Ending = Hour_Ending).Quality,
            Safety: LookUp(collectProduction, SCH_Hour_Ending = Hour_Ending).Safety,
            Shift_Letter: ThisRecord.SCH_Shift_Letter,
            Edit_Person: LookUp(collectProduction, SCH_Hour_Ending = Hour_Ending).Edit_Person,
            Edit_Reason: LookUp(collectProduction, SCH_Hour_Ending = Hour_Ending).Edit_Reason
        }
    )
);

/*Join Schema (on visible) and Local Downtime Data*/
UpdateContext({locLoading:{Visible: true, Value: 80, Text: "Joining downtime data into Hourly Tables"}});
ClearCollect(collectJoinedDowntimeDisplay,
    // Iterate through all source records and join to destination collection
    ForAll(

        // Iterate through the source collection
        collectHourlySchema,
        { 
            // Columns to appear in dataset
            ID:
                LookUp(
                    collectDowntime,
                    /*Both the...*/
                    And(
                        /*Time and total downtime must be...*/
                        Or(
                            /*Either the end time is between than the start and end schema hour*/
                            And(
                                Ended <= SCH_Hour_Ending,
                                Ended > SCH_Hour_Starting
                            ),
                            /*Or the start time is between the start and end schema hour*/
                            And(
                                Started >= SCH_Hour_Starting, 
                                Started < SCH_Hour_Ending
                            ),
                            /*Or the time passes through this hour*/
                            And(
                                Started < SCH_Hour_Starting,
                                Ended > SCH_Hour_Starting
                            )
                        ),
                        /*The total downtime must equal the greatest downtime within the hours*/
                        Value(Total_Downtime) = Max(Value(Total_Downtime))
                    )
                ).ID,

            Line:
                LookUp(
                    collectDowntime,
                    /*Both the...*/
                    And(
                        /*Time and total downtime must be...*/
                        Or(
                            /*Either the end time is between than the start and end schema hour*/
                            And(
                                Ended <= SCH_Hour_Ending,
                                Ended > SCH_Hour_Starting
                            ),
                            /*Or the start time is between the start and end schema hour*/
                            And(
                                Started >= SCH_Hour_Starting,
                                Started < SCH_Hour_Ending
                            ),
                            /*Or the time passes through this hour*/
                            And(
                                Started < SCH_Hour_Starting,
                                Ended > SCH_Hour_Starting
                            )
                        ),
                        /*The total downtime must equal the greatest downtime within the hours*/
                        Value(Total_Downtime) = Max(Value(Total_Downtime))
                    )
                ).Line,

            Lot:
                LookUp(
                    collectDowntime,
                    /*Both the...*/
                    And(
                        /*Time and total downtime must be...*/
                        Or(
                            /*Either the end time is between than the start and end schema hour*/
                            And(
                                Ended <= SCH_Hour_Ending,
                                Ended > SCH_Hour_Starting
                            ),
                            /*Or the start time is between the start and end schema hour*/
                            And(
                                Started >= SCH_Hour_Starting,
                                Started < SCH_Hour_Ending
                            ),
                            /*Or the time passes through this hour*/
                            And(
                                Started < SCH_Hour_Starting,
                                Ended > SCH_Hour_Starting
                            )
                        ),
                        /*The total downtime must equal the greatest downtime within the hours*/
                        Value(Total_Downtime) = Max(Value(Total_Downtime))
                    )
                ).Lot,
            
            Catalog:
                LookUp(
                    collectDowntime,
                    /*Both the...*/
                    And(
                        /*Time and total downtime must be...*/
                        Or(
                            /*Either the end time is between than the start and end schema hour*/
                            And(
                                Ended <= SCH_Hour_Ending,
                                Ended > SCH_Hour_Starting
                            ),
                            /*Or the start time is between the start and end schema hour*/
                            And(
                                Started >= SCH_Hour_Starting,
                                Started < SCH_Hour_Ending
                            ),
                            /*Or the time passes through this hour*/
                            And(
                                Started < SCH_Hour_Starting,
                                Ended > SCH_Hour_Starting
                            )

                        ),
                        /*The total downtime must equal the greatest downtime within the hours*/
                        Value(Total_Downtime) = Max(Value(Total_Downtime))
                    )
                ).Catalog,
            
            Started: ThisRecord.SCH_Hour_Starting,
            Ended: ThisRecord.SCH_Hour_Ending,

            Reason:
                First(
                    Sort(
                        Sort(
                            AddColumns(
                                Filter(
                                    collectDowntime,
                                    /*Both the...*/
                                    And(
                                        /*Time and total downtime must be...*/
                                        Or(
                                            /*Either the end time is between than the start and end schema hour*/
                                            And(
                                                Ended <= SCH_Hour_Ending,
                                                Ended > SCH_Hour_Starting
                                            ),
                                            /*Or the start time is between the start and end schema hour*/
                                            And(
                                                Started >= SCH_Hour_Starting,
                                                Started < SCH_Hour_Ending
                                            ),
                                            /*Or the time passes through this hour*/
                                            And(
                                                Started < SCH_Hour_Starting,
                                                Ended > SCH_Hour_Starting
                                            )
                                        )
                                    )
                                ),
                                Time_Calc,
                                If(
                                    And(
                                        Started >= SCH_Hour_Starting,
                                        Ended <= SCH_Hour_Ending
                                    ),
                                    Total_Downtime,
                                    Total_Downtime -
                                    If(
                                        Started < SCH_Hour_Starting,
                                        DateDiff(Started, SCH_Hour_Starting, TimeUnit.Minutes),
                                        0
                                    ) +
                                    If(
                                        Ended > SCH_Hour_Ending,
                                        DateDiff(Ended, SCH_Hour_Ending, TimeUnit.Minutes),
                                        0
                                    )
                                )
                            ),
                            Time_Calc,
                            SortOrder.Descending
                        ),
                        Total_Downtime,
                        SortOrder.Descending
                    )
                ).Reason,
            
            Total_Downtime:
                If(                   
                    !IsBlank(
                        LookUp(
                            collectDowntime,
                            Or(
                                /*Either the end time is between than the start and end schema hour*/
                                And(
                                    Ended <= SCH_Hour_Ending,
                                    Ended > SCH_Hour_Starting
                                ),
                                /*Or the start time is between the start and end schema hour*/
                                And(
                                    Started >= SCH_Hour_Starting,
                                    Started < SCH_Hour_Ending
                                ),
                                /*Or the time passes through this hour*/
                                And(
                                    Started < SCH_Hour_Starting,
                                    Ended > SCH_Hour_Starting
                                )
                            )
                        )
                    ),

                    Sum(
                        Filter(
                            collectDowntime,
                            Or(
                                /*Either the end time is between than the start and end schema hour*/
                                And(
                                    Ended <= SCH_Hour_Ending,
                                    Ended > SCH_Hour_Starting
                                ),
                                /*Or the start time is between the start and end schema hour*/
                                And(
                                    Started >= SCH_Hour_Starting,
                                    Started < SCH_Hour_Ending
                                ),
                                /*Or the time passes through this hour*/
                                And(
                                    Started < SCH_Hour_Starting,
                                    Ended > SCH_Hour_Starting
                                )
                            )
                        ),
                        /*Difference between endtime and start time*/
                        DateDiff(
                            /*Find the max starting time for that hour*/
                            Max(
                                Started,
                                DateTime(
                                    Year(Started),Month(SCH_Hour_Starting),Day(SCH_Hour_Starting),
                                    Hour(SCH_Hour_Starting),0,0
                                )
                            ),
                            /*Find the min ending time for that hour*/
                            Min(
                                Ended,
                                DateTime(
                                    Year(Ended),Month(SCH_Hour_Ending),Day(SCH_Hour_Ending),
                                    Hour(SCH_Hour_Ending),0,0
                                )
                            ),
                            TimeUnit.Minutes
                        )
                    )
                ),
            
            Comments:
                LookUp(
                    collectDowntime,
                    /*Both the...*/
                    And(
                        /*Time and total downtime must be...*/
                        Or(
                            /*Either the end time is between than the start and end schema hour*/
                            And(
                                Ended <= SCH_Hour_Ending,
                                Ended > SCH_Hour_Starting
                            ),
                            /*Or the start time is between the start and end schema hour*/
                            And(
                                Started >= SCH_Hour_Starting,
                                Started < SCH_Hour_Ending
                            ),
                            /*Or the time passes through this hour*/
                            And(
                                Started < SCH_Hour_Starting,
                                Ended > SCH_Hour_Starting
                            )
                        ),
                        /*The total downtime must equal the greatest downtime within the hours*/
                        Value(Total_Downtime) = Max(Value(Total_Downtime))
                    )
                ).Comments,

            Shift_Letter: ThisRecord.SCH_Shift_Letter,

            Edit_Person:
                LookUp(
                    collectDowntime,
                    /*Both the...*/
                    And(
                        /*Time and total downtime must be...*/
                        Or(
                            /*Either the end time is between than the start and end schema hour*/
                            And(
                                Ended <= SCH_Hour_Ending,
                                Ended > SCH_Hour_Starting
                            ),
                            /*Or the start time is between the start and end schema hour*/
                            And(
                                Started >= SCH_Hour_Starting,
                                Started < SCH_Hour_Ending
                            ),
                            /*Or the time passes through this hour*/
                            And(
                                Started < SCH_Hour_Starting,
                                Ended > SCH_Hour_Starting
                            )
                        ),
                        /*The total downtime must equal the greatest downtime within the hours*/
                        Value(Total_Downtime) = Max(Value(Total_Downtime))
                    )
                ).Edit_Person,

            Edit_Reason:
                LookUp(
                    collectDowntime,
                    /*Both the...*/
                    And(
                        /*Time and total downtime must be...*/
                        Or(
                            /*Either the end time is between than the start and end schema hour*/
                            And(
                                Ended <= SCH_Hour_Ending,
                                Ended > SCH_Hour_Starting
                            ),
                            /*Or the start time is between the start and end schema hour*/
                            And(
                                Started >= SCH_Hour_Starting,
                                Started < SCH_Hour_Ending
                            ),
                            /*Or the time passes through this hour*/
                            And(
                                Started < SCH_Hour_Starting,
                                Ended > SCH_Hour_Starting
                            )
                        ),
                        /*The total downtime must equal the greatest downtime within the hours*/
                        Value(Total_Downtime) = Max(Value(Total_Downtime))
                    )
                ).Edit_Reason
        }
    )
);

/* Stop Loading Prompt */
UpdateContext({locLoading:{Visible: true, Value: 95, Text: "Finishing Up"}});
/*Garbage Collecting*/

/*End*/
UpdateContext({locLoading:{Visible: true, Value: 100, Text: "Completed"}});
UpdateContext({locLoading:{Visible: false, Value: -1, Text: "Not Loading"}});