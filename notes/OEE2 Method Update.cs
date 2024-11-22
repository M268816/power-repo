// Clear Data Structures
Clear(collectOEE2Data);
Clear(collectOEE);
// Collect Lane Data
ForAll(distinct_prod_lines,
    With({thisLane:ThisRecord.Value},
        ForAll(Distinct(Filter(locProdFilter, thisLane in line),pleats_per_pack),
            With({thisPleatPerPack: ThisRecord.Value},

                Collect(collectOEE2Data,
                    {
                        lane: thisLane,
                        total_packs: Sum(Filter(locProdFilter, thisLane = line, pleats_per_pack = thisPleatPerPack),amount_built),
                        pleats_per_pack: thisPleatPerPack,
                        pleats_per_hour: LookUp(pleaterSpeeds, thisLane in Line).Pleats_Per_Hour,
                        pack_per_hour:
                            IfError(
                                Round(
                                    LookUp(pleaterSpeeds, thisLane in Line).Pleats_Per_Hour
                                    / thisPleatPerPack,
                                    4
                                ),
                                0
                            )
                    }
                )
            )
        )
    )
);
// Combine into Line Data, Collect OEE2
ForAll( // Lines
    If(
        oee_line.Selected.Value = "All",
        Distinct(pleaterSpeeds, Line),
        [oee_line.Selected.Value]
    ),
    With({thisLine: ThisRecord.Value},
        If( 
            IfError(Round(Average(Filter(collectOEE2Data, lane in thisLine), pack_per_hour),4) > 0,false),
        
            Collect(collectOEE2,
                {
                    line: thisLine,
                    pack_per_hour: Round(Average(Filter(collectOEE2Data, lane in thisLine), pack_per_hour),4), 
                    total_runtime: 48 * count_of_days, // This is a substitution for planned runtime
                    planned_packs: Round(Average(Filter(collectOEE2Data, lane in thisLine), pack_per_hour) * 48 * count_of_days,4),
                    total_packs: Sum(Filter(collectOEE2Data, lane in thisLine),total_packs),
                    OEE2:
                        If(
                            Sum(Filter(collectOEE2Data, lane in thisLine),total_packs) > 0
                            
                            IfError(
                                Round(
                                    Sum(Filter(collectOEE2Data, lane in thisLine),total_packs)
                                    /  Round(Average(Filter(collectOEE2Data, lane in thisLine), pack_per_hour) * 48 * count_of_days,4)
                                    * 100,
                                    4
                                ),
                                0
                            ),
                            
                            0
                        )
                }
            )
        )
    )   
);
// Patch in Average OEE2
Patch(collectOEE2, Defaults(collectOEE2),
    {
        line: "Average",
        pack_per_hour:Round(Average(collectOEE2, pack_per_hour),4),
        total_packs: Sum(collectOEE2, total_packs),
        planned_packs: Round(Sum(collectOEE2, planned_packs),4),
        total_runtime: Sum(collectOEE2, total_runtime),
        OEE2:
            IfError(
                Round(
                    Sum(collectOEE2, total_packs)
                    / Sum(collectOEE2, planned_packs)
                    * 100,
                    4
                ),
                0
            )   
    }
);