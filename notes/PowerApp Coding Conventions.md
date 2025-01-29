# PowerApps coding conventions and syntax

In an attempt to create some sort of consistency with my own code, I'm going to
write up a code of ethics and conventions for writing PowerApps code and try and
adhere to them.

## Commenting

No big comment rules here, just be sure to use comments for tricky parts of
formulas or functions

```cpp
// Inline comments have so much rizz

/*
    I Got a lot to say here:
    Look at all this freaking
    code here.

    It does something that chatGPT
    told me worked so well.

    It took 5 hrs to debug tho.
    Thanks chatGPT 👎
    Not very skibity of you.

*/
```

## Databases or data sources

When using outside data sources, it's good practice to first create the database
you want to pull the information from. Once the initial data base structure is
built, it makes linking to PowerApps a much simpler process.

Currently I use SharePoint Lists and format list names in pascal case, column
names in capitalized snake case. Values can be formatted appropriately for
their needs.

### UserPreferences

| First_Name | Last_Name | E_Mail                            | Theme_Mode |
|:---------- |:--------- |:--------------------------------- |:---------- |
| Raymond    | Comeau    | raymond.comeau@milliporesigma.com | ( Light )  |
| Someone    | Else      | someone.else@milliporesigma.com   | ( Dark )   |

## Screens
> Home

> OrderMaterials

Screen objects within PowerApps can be named in Pascal case and referenced in
the tree structure by their first letter. Naming objects down the tree is
explained in the next section.

```
Home
  |_. hControl

OrderMaterials
  |_. oControl
```

## Objects / Controls

> Update Jan 28 2025: PowerApps handles kebab case by adding single quotes to the
> yaml code. Using this for a while, I noticed how absolutely annoying it was.
> It makes editing objects in yaml to import into the Editor a big
> pain, changed conventions to use camelCaseInstead.

```
<screen><Parent><Object><Iteration>
```

Because the complexity of object trees can increase quickly naming objects in
the app can get out of hand quickly. To combat this, I will use ~~kebab case~~
camel case to distinguish between objects and variables. I begin the name of an
object with the first initial of its parent screen then add the lowest significant
parent of the object on the tree until I need to use a unique identifier. For
example, A button that would submit information on the home page, located in the
main form content of the screen may be named 'hFormSubmit'.

The parent structure looks like this.

```
Home
  |_. hPopups
    |_. hPopupLoadError
      |_. hPopupLoadErrorHeader
      |_. hPopupLoadErrorBody
      |_. hPopupLoadErrorFooter
    |_. hPopupWarning
      |_. hPopupWarningHeader
      |_. hPopupWarningBody
      |_. hPopupWarningFooter
  |_. hMain
    |_. hHeader
    |_. hBody
      |_. hFormParent
        |_. hForm
        |_. hFormButtons
          |_. hFormSubmit
          |_. hFormCancel
    |_. hFooter
```

Each object starts with the first letter of the screen's name. Then they receive
either, their own name, becoming a parent, or their parent's name. With the
submit button nested so far within the tree, naming it something like
'h-main-body-form-submit' is too unwieldy. So, nested controls should only try
and be as distinctive as their screen name and *lowest significant parent*.

> hFormSubmit

But with objects like the popups, this does get ugly, as we need to distinguish 
between the 'Load Error' popup and the 'Warning' popup structures.

> hPopupLoadErrorHeader

> hPopupWarningHeader

However, we wont need to go so in depth for the content. We just need to go deep
enough into the tree as to make it distinguishable between other objects within
the same level.

> ~~hMainBodyFormParentFormButtonsSubmit~~
>
> hFormSubmit

> ~~hPopupWarningBodyConfirm~~
>
> hPopupWarningConfirm

I break this rule for items that would only appear once. Like a bug report
button would not need to describe its located within the header or footer, but
that its the bug button for that page.

> ~~hMainHeaderReportBug~~
>
> hReportBug

## Variables

> Update Jan 28 2025: I really liked using the simpler 'g' or 'l' for naming
> variables. But it was unfortunately hard to read sometimes. Changing the 
> my convention to always use the three letter prefix instead.

PowerApp development is in a fight with itself over where it wants to store its 
variables using two functions 'Set()' and 'UpdateContext({})'. Set() is used
for variables that need to span the entire app. They can be set and accessed
anywhere in the app. UpdateContext({}) creates variables that can only be set
and accessed in the screen they were initiated. You can use Set() to create any
data structure you would need. UpdateContext({}) stores everything in a record.
But, record values can then be set to whatever type you may need.

```cpp
Set(variable, value);

UpdateContext({variable: value});
```

The variable scopes I use in a PowerApp are constant, local, global, and
something I call universal. Here are the conventions that I use.

### Constant

- Variables that should be set, and not changed.
    - Use the Set() function.
    - Screaming Snake case.
    - All capital letters.
    - The actual concept of constants do no exist within PowerApps, so this must
    be self regulated. Whenever you need a constant set it on the app start
    property then make sure to only read the variable and not write it.
    ```cpp
    Set(THEME_MODE, Theme.Mode.Dark);
    ```

### Local

- Variables that only need to apply to the current loaded screen.
    - Use the UpdateContext({}) function.
    - Prefix with 'loc'.
    - Camel case.
    ```cpp
    UpdateContext({locThemeMode: Theme.Mode.Dark});
    ```

### Global

- Variables that need to be applied across the whole application.
    - Use the Set() function.
    - Prefix with 'gbl'.
    - Camel Case.
    ```cpp
    Set(gblThemeMode, Theme.Mode.Dark);
    ```
### Universal

- Variables that need to be applied across application *sessions*.
    - Use the Set() function.
    - Prefix with 'UNI'.
    - Screaming Snake case.
    - All capital letters.
    - Init the value from a data source.
    - Set new values to the data source.
    ```cpp
    // Init the value from the data source
    Set(UNI_THEME_MODE, LookUp(UserPreferences, E_Mail = User().Email).Theme_Mode)
    
    // To set the variable, use Patch()
    Patch(UserPreferences,
        LookUp(UserPreferences, E_Mail = User().Email).ID,
        {
            Theme_Mode: {Value: "Dark"}
        }
    );
    ```
    
Because variables init at runtime, variables that need to be set and remembered
across sessions cannot be used natively in PowerApps, they are not saved in
memory. Let's use the dark mode variable above as an example.

A user wants to set the application to dark mode and have this setting
remembered every time the application opens with their credentials. We need to
store this dark mode variable as a universal variable outside of the scope of
the application memory. The easiest way to do this is creating a database with
the user credentials as a key, like their email address, and a data column with
the value.

We can use a SharePoint list to store this information, and when the user opens
the app, access the list, detect the user, and detect that user's preferences
and load them into the application on launch.

## Dates and Times

The Today() and Now() functions will only update their values when first called
or used to set parameters. This means for objects like the Text Label, when
Today() and Now() are used it only pulls in the value stored the last time they
were called. Other times it works as intended. These are so inconsistent that
I fix this by assigning the functions to variables.

The variables are set at a global level each time a screen is loaded or 
logic needs to be run. The variables I set for these purposes is as follows:

```cpp
Set(gblToday, Today());

Set(gblNow, Now());

Set(gblHour, Hour(Now()));

/*Or to allow for dot notation*/

Set(gblTime,
    {
        Today: Today(),
        Now: Now(),
        Hour: Hour(Now())
    }
);
```

## Collections

Collections in PowerApps are powerful data structures that can be used for a
large variety of data management. These collections can be used to not only
store and display data from within the app, but you can pull data from outside
databases like share point lists to create local copies. These local copies can
be manipulated without need to worry about delegation. Collections can even be
used to create static lists, dictionaries, arrays, or tables of variables.

- Collections
    - Use Collect() for initialization, or within ForALL() loops.
    - Use ClearCollect() for everything else.
    - Prefix the collection with 'col'
    - Camel case.

```cpp
// Clear the collection for new data
Clear(colProduction);
// For all Records in this data
ForAll(EncapsulationProductionData,
    //Collect each record into cProduction
    Collect(colProduction,
        {
            Id: ThisRecord.Id,
            Line: ThisRecord.Line,
            Unit_Start: ThisRecord.Unit_Start,
            Unit_End: ThisRecord.Unit_End,
            Date_Start: ThisRecord.Date_Start,
            Date_End: ThisRecord.Date_End,
            Shift: ThisRecord.Shift_Letter,
        }
    )
);
```

## Records

Single record collections are useful for creating mutable variables accessible
with dot notation. I make sure to only ever init the collection, then change its
variables with the Patch() function. There is a drawback to this method, to use
the dot notation, you need to use the First() function to access the record. 
However, through extensive testing, this is the only way to make mutable data
structures and variables that can use dot notation.

- Mutable Records
    - Use ClearCollect() for initialization.
    - Prefix the collection with 'rec'
    - Use camel case.
    - Set new values with Patch()
    - Get values with First()

```cpp
// Initialize
ClearCollect(recPopups,
    {
        Display_Text: "Not Loading",
        Value: -1,
        Popup: "",
        Visible: false
    }
);

// Setter
Patch(recPopups,First(recPopups),{Value: 10});
// Getter
First(recPopups).Value
```

When we only need to store a single immutable record. Instead of using a
collection, we use the Set() function like we would set a variable. We structure
the variable just like we would structure a record in a collection. Using single
records this way allows us to use dot notation to pull in data more readily.
This method also ensure we are using as little memory as possible with the app,
as setting a record variable is less intensive than setting up a collection for
a single record. The downside to this, is that Set() records must be updated in
their entirety, as the Patch() function will not work with Set().

- Records
    - Use Set() for initialization.
    - Prefix the record with 'rec'
    - Use camel case.

```cpp
// Initialize and Setter
Set(recOEE,
    {
        OEE2: 0.5,
        Amount_Built: 100,
        Goal: 200,
        Rejects: 5
    }
);

// Getter
recOEE.Goal
```

## Field Names

When naming field names within collections, tables, lists or dictionaries the
field or column name will use snake case. Global collections will capitalize
their first letters in field names, while sub collections or 'local' collections
should use all lower case.

For example. We collect production data directly from a data source like a share
point list. This data is a copy from the production date source and will be used
throughout the app and can be considered the top level data structure for the
production data for the application. Let's say, we then want to change the data,
and filter it for another data display.
```cpp
// Copy the original data source into a local copy. 'Top Level Collection'
ForAll(DataSource,
    Collect(colTopLevelData,
        {
            Id: ThisRecord.ID,
            DateTime: ThisRecord.DateTime,
            First_Unit: ThisRecord.First_Unit,
            Last_Unit: ThisRecord.Last_Unit
        }
    )
);

// Create a sub-collection, a modified/filtered version.
ForAll(Filter(colTopLevelData, DateTime = gblTime.Today),
    Collect(colLowerLevelData,
        {
            id: ThisRecord.Id,
            date: DateValue(ThisRecord.DateTime),
            time: TimeValue(ThisRecord.DateTune),
            total_units:
                ThisRecord.Last_Unit
                - ThisRecord. First_Unit
                + 1
        }
    )
);
```