SELECT 
    [Roll Data].[Id] AS Old_Id, 
    [Roll Data].[Date], 
    [Roll Data].[Shift], 
    [Roll Data].[Pleater], 
    [Roll Data].[Work Order #] as WorkOrder, 
    [Roll Data].[Lot_No] as Lot, 
    [Roll Data].[Catalog], 
    [Roll Data].[Master Roll #] as MasterRoll, 
    IIf(
        Right(Trim([Roll Data].[Master Roll #]), 2) = "NA" OR 
        Right(Trim([Roll Data].[Master Roll #]), 2) = "/A" OR 
        Len(Trim([Roll Data].[Master Roll #])) = 2, 
        Trim([Roll Data].[Master Roll #]), 
        IIf(
            Right(Trim([Roll Data].[Master Roll #]), 1) IN ('A', 'B', 'C', 'D', 'E', '.'), 
            Left(Trim([Roll Data].[Master Roll #]), Len(Trim([Roll Data].[Master Roll #])) - 1), 
            Trim([Roll Data].[Master Roll #])
        )
    ) AS TruncatedMasterRoll,
    (
        Nz([Roll Data].[Startup], 0) +
        Nz([Roll Data].[RollChange], 0) +
        Nz([Roll Data].[Membrane], 0) +
        Nz([Roll Data].[Lamination], 0) +
        Nz([Roll Data].[Support], 0) +
        Nz([Roll Data].[OOS_Pleat_Heights], 0) +
        Nz([Roll Data].[Pack_Ext], 0) +
        Nz([Roll Data].[Flagging], 0) +
        Nz([Roll Data].[Slitters], 0) +
        Nz([Roll Data].[Pack_Damage], 0) +
        Nz([Roll Data].[Under Heat], 0) +
        Nz([Roll Data].[Choppy_Pleat], 0) +
        Nz([Roll Data].[Filter_Wrinkles], 0) +
        Nz([Roll Data].[Machine_Dump], 0) +
        Nz([Roll Data].[Tracking], 0) +
        Nz([Roll Data].[Poly_Issue], 0) +
        Nz([Roll Data].[Under_post_Heat], 0) +
        Nz([Roll Data].[Seaming], 0) +
        Nz([Roll Data].[Pleat_Count], 0) +
        Nz([Roll Data].[Contamination], 0) +
        Nz([Roll Data].[Filter_Other], 0) +
        Nz([Roll Data].[Filter_Splice], 0) +
        Nz([Roll Data].[Incorrect_Threading], 0) +
        Nz([Roll Data].[Lamination_Separation], 0) +
        Nz([Roll Data].[Pack_Density], 0) +
        Nz([Roll Data].[Snaking], 0)
    ) AS TotalRejectPleats,
    [Roll Data].[Begin Footage] as Footage,
    [Roll Data].[Good] as SlitPostPleatCarts,
    [Roll Data].[Begin Cart #] as StartingCartridge, 
    [Roll Data].[End Cart #] as EndingCartridge, 
    [Roll Data].[PleatPerPack], 
    [Roll Data].[Pleat_Height] as PleatHeight 
INTO Temp_Table
FROM [Roll Data]
WHERE [Roll Data].[Date] = #01/01/1111#;


INSERT INTO Temp_Table 
    ( 
        Old_Id, 
        [Date], 
        Shift, 
        Pleater, 
        WorkOrder, 
        MasterRoll, 
        TruncatedMasterRoll,
        Lot, 
        [Catalog],
        TotalRejectPleats, 
        Footage,
        SlitPostPleatCarts,
        StartingCartridge, 
        EndingCartridge, 
        PleatPerPack, 
        PleatHeight 
    )
SELECT
    [Roll Data].[Id], 
    [Roll Data].[Date], 
    [Roll Data].[Shift], 
    UCase([Roll Data].[Pleater]) AS Pleater,
    [Roll Data].[Work Order #], 
    [Roll Data].[Master Roll #], 
    IIf(
        Right(Trim([Roll Data].[Master Roll #]), 2) = "NA" OR 
        Right(Trim([Roll Data].[Master Roll #]), 2) = "/A" OR 
        Len(Trim([Roll Data].[Master Roll #])) = 2, 
        Trim([Roll Data].[Master Roll #]), 
        IIf(
            Right(Trim([Roll Data].[Master Roll #]), 1) IN ('A', 'B', 'C', 'D', 'E', '.'), 
            Left(Trim([Roll Data].[Master Roll #]), Len(Trim([Roll Data].[Master Roll #])) - 1), 
            Trim([Roll Data].[Master Roll #])
        )
    ) AS TruncatedMasterRoll,
    [Roll Data].[Lot_No], 
    [Roll Data].[Catalog], 
    [Roll Data].[Total_Reject_Pleats],
    [Roll Data].[Begin Footage],
    [Roll Data].[Good],
    [Roll Data].[Begin Cart #], 
    [Roll Data].[End Cart #], 
    [Roll Data].[PleatPerPack], 
    [Roll Data].[Pleat_Height]
FROM
    [Roll Data]
WHERE
    [Roll Data].[Date] = #02/10/2025#
    AND (Nz([Roll Data].[Good], 0) > 0 OR Nz([Roll Data].[End Cart #], 0) > 0)
    AND [Roll Data].[Id] NOT IN (
        SELECT [Old_Id] FROM FE_Roll_Data_TEST WHERE [Old_Id] IS NOT NULL
    )
    AND UCase([Roll Data].[Pleater]) <> 'V';
