# PowerApps coding conventions and syntax

In an attempt to create some sort of consistency with my own code, I'm going to
write up a code of ethics and conventions for writing PowerApps code and try and
adhere to them.

## Databases or data sources

when using outside data sources, it's good practice to first create the database
you want to pull the information from. Once the initial data base structure is
built, it makes linking to PowerApps a much simpler process.

Currently I use SharePoint Lists and format list names in Pascal case, column
names in snake case and with all first letters capitalized. Values can be 
formatted appropriately for their needs.

### UserPreferences

| First_Name | Last_Name | E_Mail                            | Theme_Mode |
|:---------- |:--------- |:--------------------------------- |:---------- |
| Raymond    | Comeau    | raymond.comeau@milliporesigma.com | "Light"    |
| Someone    | Else      | someone.else@milliporesigma.com   | "Dark"     |

## Objects / Controls

Because the complexity of object trees can increase quickly naming objects in
the app can get out of hand very quickly. To combat this, I use kebab case as my
naming convention as a distinguishing factor between variables, then begin the
name with a parent screen. Next, the lowest significant parent of the object on
on the tree is added to the name until I need to use an unique identifier. For
example, A submit button on the home page in the main content of the screen may
be named 'h-form-submit'. The parent structure looks like this.
```
Home
  |_. h-popups
    |_. h-pop-load-error
      |_. h-pop-le-header
      |_. h-pop-le-body
      |_. h-pop-le-footer
    |_. h-pop-warning
      |_. h-pop-warn-header
      |_. h-pop-warn-body
      |_. h-pop-warn-footer
  |_. h-main
    |_. h-header
    |_. h-body
      |_. h-form-parent
        |_. h-form
        |_. h-form-submit
    |_. h-footer
```
Each object starts with the first letter of the screen's name. Then they receive
either, their own name, becoming a parent, or their first significant parent's
name. With the submit button nested so far within the tree, naming it something
like 'h-main-body-form-submit' is too unwieldy. So, nested controls should only
try and be as distinctive as their screen name and lowest significant parent.
> h-form-submit

But with objects like the popups, this does get ugly, as we need to distinguish 
between the 'Load Error' popup and the 'Warning' popup structures.
> h-pop-le-header

> h-pop-warn-header

However, we wont need to go so in depth for the content. We just need to go deep
enough into the tree as to make it distinguishable between other objects within
the same level. I even use short hand for longer names like 'Load Error', and
just use 'le' instead.
> ~~h-pop-le-header-title~~
>
> h-pop-le-title

> ~~h-pop-le-body-confirm~~
>
> h-pop-le-confirm

> ~~h-pop-warn-header-title~~
>
> h-pop-warn-title

> ~~h-pop-warn-body-confirm~~
>
> h-pop-warn-confirm

I break this rule for items that would only appear once. Like a bug report
button would not need to describe its located within the header or footer, but
that its the bug button for that page.
> ~~h-main-header-report-bug~~
>
> h-report-bug

## Variables

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

- Constants: Variables that should be set, and not changed.
    - Use the Set() function.
    - Snake case.
    - All capital letters.
    - The actual concept of constants do no exist within PowerApps, so this must
    be self regulated. Whenever you need a constant set it on the app start
    property then make sure to only read the variable and not write it.
    ```cpp
    Set(THEME_MODE, Theme.Mode.Dark);
    ```
- Local: Variables that only need to apply to the current loaded screen.
    - Use the UpdateContext({}) function.
    - Prefix with 'l' or 'loc'.
    - Camel case.
    ```cpp
    UpdateContext({lThemeMode: Theme.Mode.Dark});
    ```
- Global: Variables that need to be applied across the whole application.
    - Use the Set() function.
    - Prefix with 'g' or 'gbl'.
    - Camel Case.
    ```cpp
    Set(gThemeMode, Theme.Mode.Dark);
    ```
- Universal: Variables that need to be applied across application *sessions*.
    - Use the Set() function.
    - Prefix with 'U' or 'UNI'.
    - Snake case.
    - All capital letters.
    - Init the value from a data source.
    - Set new values to the data source.
    ```cpp
    // Init the value from the data source
    Set(U_THEME_MODE, LookUp(UserPreferences, E_Mail = User().Email).Theme_Mode)
    
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
    - Prefix the collection with 'c' or 'collect'
    - Camel case.
```cpp
Collect(cProduction,
    {
        Id: 1,
        Line: "",
        Unit_Start: 1,
        Unit_End: 50,
        Date_Start: "2024-01-31 8:00 AM",
        Date_End: "2024-01-31 9:00 AM",
        Shift: "A",
    }
);
```

### Filed Names

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
    Collect(cTopLevelData,
        {
            Id: ThisRecord.ID,
            DateTime: ThisRecord.DateTime,
            First_Unit: ThisRecord.First_Unit,
            Last_Unit: ThisRecord.Last_Unit
        }
    )
);

// Create a sub-collection, a modified/filtered version.
ForAll(Filter(cTopLevelData, DateTime = Today()),
    Collect(cLowerLevelData,
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
## Galleries