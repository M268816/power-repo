# Definitions

Pleats Per Pack
    - The amount of pleats needed to complete a single pack.

Pleat Height
    - The height of an individual pleat in a single direction.
    - A completed pleat, is the height of a pleat up and down the peak of a 
    single pleat.
    - Example: a pleat at 0.455 Height is 0.91 in per pleat.

Packs
    - The amount of pleats created to start the cartridge making process.

Cartridges
    - The name packs transfer to after the pleating process. 

Slits Post Pleat
    - The amount of cuts, or slits made to separate packs into cartridges.


# Formulas

Slit Post Pleats =
    If a catalog is not found within the list of SPP Catalogs
    return 1
    otherwise return the value in the SPP Catalog map.

    Example:
        110605RCVGL in Data = False, Returns 1
        CTGR75S01 in Data = True, Returns
            LookUp(Data, Catalog = CTGE75S01).Slits_Post_Pleat, 2

Truncated Master Rolls =
    The Master Roll number truncating added
    shift letters

    Example:
        333A
        333B
        333C
            -> 333

    EdgeCases:
        1234Y   -> 1234Y
        1234TA  -> 1234T
        0123    -> 123
        123A    -> 123
        123.    -> 123
        123.A   -> 123.


Max Footage =
    Find the Max Recorded Beginning Footage per
    Catalog, Lot, and Truncated Master Roll

    Example:
        Catalog1 - Lot1 - Master1A -> Master1 - 100
        Catalog1 - Lot1 - Master1B -> Master1 - 300
        Catalog1 - Lot1 - Master1C -> Master1 - 1967
            -> 1967

Sum of Max Footage =
    Sum of the Max Recorded Beginning Footage per
    Catalog and Lot

    Example:
        Catalog1 - Lot1 - Master1 - 350
        Catalog1 - Lot1 - Master2 - 650
            TOTAL = 1000
        Catalog1 - Lot2 - Master3 - 1150
        Catalog1 - Lot2 - Master5 - 350
            TOTAL = 1500
        Catalog2 - Lot3 - Master4 - 400
        Catalog2 - Lot3 - Master1 - 300
            TOTAL = 700

Sum of Reject Footage =
    Sum of the rejected pleat count
    Multiplied by pleat hight
    Divided by 6

    Example:
        1500 Pleats * 0.455 Pleat Height / 6
        682.5 / 6
        113.75 ft

Calculated Good Footage =
    A calculated value to retrieve good footage from
    reported bad footage.
    Sum of Max Footage
    Minus Sum of Reject Footage

    Example:
        1000 Sum of Max Footage - 113.75 Reject Footage = 886.25 Good Footage

Footage Per Pack:
    Pleat Height
    Multiplied By Pleats Per Pack
    Divided by 6
    
    Example:
        0.455 * 127 / 6
        9.63 ft per pack

Reject Carts:
    Rejected footage calculated into carts
    Reject Footage
    Divided by Footage Per Pack
    Multiplied By Slits Post Pleat

    Example:
        112 Reject ft / (0.455 Pleat Height * 127 Pleats Per Pack / 6) * 2 Slits Post Pleat
        11.63 packs * 2 Slits Post Pleat
        23.26 Reject Carts
        Rounded up to 24 Carts

Calculated Good Carts:
    Good footage calculated into carts
    Good Footage
    Divided by Footage per pack
    Multiplied by slits post pleat

    Example:
        250 Good ft / (0.300 pleat height * 72 pleats per pack / 6) * 8 slits post pleat
        69.444 packs * 8 slits post pleat
        555.555 carts
        Rounded Down to 555 carts

Total Possible Carts:
    Sum of Max Footage
    Divided by Footage Per Cart
    Multiplied by slits post pleat

    Example:
        1500 Total starting footage / 9.63 ft per pack * 2 slits post pleat
        155.763 packs * 2 slits
        311.526 carts
        rounded down to 311 total possible carts
            (This should equal good carts + reject carts +/- 1 for rounding)