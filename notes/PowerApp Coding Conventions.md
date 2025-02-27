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
'hMainBodyFormButtonsSubmit' is too unwieldy. So, nested controls should only try
and be as distinctive as their screen name and *lowest significant parent*.

> hFormSubmit

But with objects like the popups, this does get ugly, as we need to distinguish 
between the 'Load Error' popup and the 'Warning' popup structures.

> hPopupLoadErrorHeader

> hPopupWarningHeader

We wont need to go so in depth for content. We just need to go deep enough into
the tree to make it distinguishable between other objects within the same level.

> ~~hLayoutMainBodyFormParentFormButtonsSubmit~~
>
> hFormSubmit

> ~~hLayoutPopupsWarningBodyConfirm~~
>
> hPopupWarningConfirm

For items that only appear once I break all the rules and only prefix the screen
of the control. Like a bug report button would not need to describe its located
within the header or footer, but only that its the bug button for that page.

> ~~hMainHeaderReportBug~~
>
> hReportBug

## Variables

> Update Jan 28 2025: I really liked using the simpler 'g' from 'gbl or 'l' from
> 'loc' for naming variables. But it was unfortunately hard to read sometimes.
> Changing my convention to always use the three letter prefix instead.

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
    Set(gblStyles, Theme.Mode.Dark);
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
be manipulated without needing to worry about delegation. Collections can even be
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
    //Collect each record into colProduction
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
variables with the Patch() function. There is a drawback to this method. To use
the dot notation, you need to use the First() function to access the record. 
However, through extensive testing, this is the only way to make mutable data
structures and variables that can use dot notation.

- Mutable Records
    - Use Collect() for initialization.
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

# Initialization

Current versions of the PowerApp app properties include the OnStart action. This
action has been planned to be removed from future versions of PowerApps. This
poses a problem because many of the apps I build need to have various variables
and processes run before the applications hand over control to the user.

This includes simple instructions like setting global variables for formatting.
However, this also includes instructions for updating login settings and user
tracking. If power apps as a platform decides to remove the OnStart property
from the editor, I needed to future proof these instructions by utilizing a
stable initialization method.

This brings us to the Init screen. I utilize a starting screen to init
instructions into the app instead of the OnStart property. Currently, this
system is automatic, as the OnStart property is still available. I create a
CONSTANT that determines weather or not to load these initial instructions,
explained why later.

```cpp
Set(INITIALIZE, true);
```

When the application loads, it first sets this constant. Then immediately 
transfers the app to the screen stored in the 'StartScreen' property. I use
the screen 'Init' for this purpose.

This causes another action to fire for the Init screen called 'OnVisible'. If
INITIALIZE is set to true, then the OnVisible property inits the instructions
through the OnSelect property of a button.

```cpp
// The button is called iInit
If(INITIALIZE, Select(iInit));
```

The flow of these properties and information causes an infinite loop that cannot
be broken when the app starts this way. That is why I set the INITIALIZE
constant at all. It gives me the ability to stop the automatic process and edit
the init code as I need.

In the future when PowerApps disables the OnStart property, this automatic
process will most likely be offloaded onto a simple manual button press that
starts the init instructions.

```
╔════════════════════╗
║Click Here to Enter!║
╚════════════════════╝
```

## Standard Variables

The Templates come with some standard variables to use within the apps. 
Navigation, Popups, and Icons have been separated and explained more in depth
later on. These next variables I use as standard practice to increase some of
the flexibility of the template.

```cpp

/*  
    APP_NAME helps keep areas of the application consistent with the bug
    reporting tool
*/  
Set(APP_NAME, "DMS Management Template");

//  Setting a global padding helps keeps visuals consistent.
Set(gblPadding, Round(App.Width * 0.005,0));

/* 
    Setting time variables is important because static objects will not
    update these functions without a direct update to them. Setting these
    functions to a variable updates this info whenever they load, in turn
    updating the static objects.
*/
Set(gblTime,{Today:Today(),Now:Now()});

/*
    Using a global variable to pull in static data with dot notation is always
    very valuable. These lists are used constantly throughout the app, for
    many various applications.
*/
Set(gblLists,
    {
        Shifts: [
            "C","A","B"
        ],
        Lines: [
            "XL1", "XL2", "XL3", "XL4", "XL5",
            "XLT", "XLT2", "XLT3",
            "SSC", "SSC2"
        ],
        Downtime_Reasons: [
            "Reason 1","Reason 2","Reason 3","Reason 4",
            "Reason 5","Reason 6","Reason 7","Reason 8",
        ]
    }
);
```

## Navigation

The navigation system that I apply to my apps uses a collection of screens.

```cpp
ClearCollect(colNavigation,
    {Screen: Home, Label: "Home"},
    {Screen: Filterable, Label: "Filterable"},
    {Screen: Singleton, Label: "Singleton"},
    {Screen: Data, Label: "Data"}
);
```

It holds the Screen Object in 'Screen' and a text label in 'Label'.

With this collection initialization, it creates a data structure I can use to
populate a gallery for navigation on each screen. This data structure can be
edited from initialization and automatically update all other instances of the
navigation gallery throughout the whole application.

```yaml
- hNavigationGallery:
    Control: Gallery@2.15.0
    Variant: Vertical
    Properties:
      AlignInContainer: =AlignInContainer.SetByContainer
      Items: =colNavigation
      LayoutMinHeight: =10
      LayoutMinWidth: =10
      TemplatePadding: =gblPadding
      TemplateSize: =40
    Children:
      - hNavGalleryButton:
          Control: Classic/Button@2.2.0
          Properties:
            BorderThickness: =1
            Color: =gblTheme.Text_Dark
            DisplayMode: -|
                =If(App.ActiveScreen.Name = ThisItem.Screen.Name,
                    DisplayMode.Disabled,
                    DisplayMode.Edit
                )
            Fill: =gblTheme.Accent
            FontWeight: =FontWeight.Normal
            Height: =Parent.TemplateHeight
            OnSelect: =Navigate(ThisItem.Screen,ScreenTransition.Fade)
            RadiusBottomLeft: =Self.RadiusTopLeft
            RadiusBottomRight: =Self.RadiusTopLeft
            RadiusTopLeft: =100
            RadiusTopRight: =Self.RadiusTopLeft
            Size: =Self.Height / 4
            Text: =ThisItem.Label
            Width: =Parent.TemplateWidth
```

## The popup manager

The popup manager uses a collection to store a single global record. This record
is then mutable anywhere in the application. It allow us to dynamically change
any variable associated with the record and pull the information through dot
notation.

```cpp
// Popup Manager
ClearCollect(recPopups,
    {
        Display_Text: "Not Loading",
        Value: -1,
        Popup: "",
        Visible: false
    }
);
// Setter: Patch(recPopups,First(recPopups),{Value: 10});
// Getter: First(recPopups).Value
```

I'm not going to lie the variables that I use are very jank.

Display_Text is used to display any type of loading information through any
text object or property.

Value is used to determine the status of the loading and spinner objects. I 
typically use -1 to determine if properties should be turned off or
indeterminate. For example, in a progress bar, the bar will cycle like a 
spinner when indeterminate is set to true. Otherwise it will set the position of
the inner colored loading bar.

Visible is fairly well explained, as it determines if the popup manager should
be visible.

Popup, on the other hand is a very messy way I determined what popup should be
displaying. Some screens have various popups that need to display, like
errors, or simple loading prompts. To determine what popup to show, I use a
string variable that describes the popup. For example, the loading popup would
be named 'loading'. An error for bad information would be called 'error'. And 
a confirmation dialog would be 'confirm'.

The parent object that controls all popups will use the 'Visible' variable to
determine weather or not to show a popup.

But the 'Popup' variable determines what popup to display in the parent object.

```yaml
# Parent Properties
- hPopups:
    Control: GroupContainer@1.3.0
    Variant: AutoLayout
    Properties:
      Visible: =First(recPopups).Visible # show the manager via boolean
```

```yaml
# Child Properties
- hPopupError:
    Control: GroupContainer@1.3.0
    Variant: AutoLayout
    Properties:
      Visible: = First(recPopups).Popup = 'error' # show the popup via equality
```

## Themes and theme modes

A manual theme system was totally optional and I had no reason to implement it
except that... I wanted dark mode.

There are two steps to setting up this theme system.

1. Define each style or mode.
2. Apply a selected style or mode.

Defining the styles or modes can be as complicated as you wish. For me, I just
wanted a way to switch between light and dark modes that was controlled all in
one place.

This next large hunk of code is just the setup. I defined what each key
represented and what each color value those were assigned. I did try my best
to use the coloring guidelines from global that can be found [here]('https://brand-hub.emdgroup.com/en/login.html?requestUri=https://brand-hub.emdgroup.com/en/design-basics/colors.html').



```cpp
// Theme Mode Setup
Set(gblStyles,
    {
        Light:
        {
            Style: "Light",
            Text_Dark: ColorValue("#000000"),
            Text_On_Dark: ColorValue("#FFFFFF"),
            Text_Light: ColorValue("#FFFFFF"),
            Text_On_Light: ColorValue("#000000"),
            Background: ColorValue("#FFFFFF"),
            Midground: ColorValue("#EEEEEE"),
            Foreground: ColorValue("#DDDDDD"),
            Primary: ColorValue("#503291"),
            Pri_Complement: ColorValue("#2DBECD"),
            Secondary: ColorValue("#0f69af"),
            Sec_Complement: ColorValue("#FFDBC9"),
            Accept: ColorValue("#149B5f"),
            Deny: ColorValue("#e61e50"),
            Accent: ColorValue("#FFC832"),
            Chart_Black: "#121212",
            Chart_White: "#FFFFFF",
            Chart_Red: "#e61e50",
            Chart_Blue: "#503291",
            Chart_Accent: "#FFC832",
            Chart_Dim: "#787878"
        },
        Dark:
        {
            Style: "Dark",
            Text_Dark: ColorValue("#000000"),
            Text_On_Dark: ColorValue("#000000"),
            Text_Light: ColorValue("#FFFFFF"),
            Text_On_Light: ColorValue("#FFFFFF"),
            Background: ColorValue("#121212"),
            Midground: ColorValue("#232323"),
            Foreground: ColorValue("#343434"),
            Primary: ColorValue("#565656"),
            Pri_Complement: ColorValue("#ec9d99"),
            Secondary: ColorValue("#676767"),
            Sec_Complement: ColorValue("#af9ecf"),
            Accept: ColorValue("#98d3b2"),
            Deny: ColorValue("#f68da5"),
            Accent: ColorValue("#ffdf85"),
            Chart_Black: "#FFFFFF",
            Chart_White: "#121212",
            Chart_Red: "#f68da5",
            Chart_Blue: "#0f69af",
            Chart_Accent: "#ffdf85",
            Chart_Dim: "#565656"
        }
    }
);
```

Step two, make these settings easily accessible with dot notation.

```cpp
Set(gblTheme, gblStyles.Light);
```

I also set up a way to check what theme is currently active. Although, it does
use the simple string system like the popup manager does. This is a simple setup
to change from dark mode to light mode.

```cpp
If(gblTheme.Style = "Light",
    Set(gblTheme, gblStyles.Dark),
    Set(gblTheme, gblStyles.Light)
)

// I should probably change the variables to be more readable though, like this
If(gblTheme.Style = "Light",
    Set(gblTheme, gblStyles.Dark),
    Set(gblTheme, gblStyles.Light)
)
```

## Icon manager

The icon manager that I have included uses raw SVG code encoded from the
[global branding icon package]('https://brand-hub.emdgroup.com/en/design-basics/icons.html').

Icons are set as variables that can be input into the app with image objects.
I use SVGs instead of plain images because they scale cleaner and their colors
can be updated on the fly.

```js
// Just look for this piece of code and change the hex color
{fill:#0F69AF;}
```

The objects an simply use dot notation to apply them.

```yaml
- hBugs:
    Control: Image@2.2.3
    Properties:
      BorderColor: =RGBA(0, 18, 107, 1)
      HoverFill: =gblTheme.Pri_Complement
      Image: =gblIcons.Bug # EZPZ
      ImagePosition: =ImagePosition.Fill
      LayoutMinHeight: =10
      OnSelect: =Navigate(Bugs,ScreenTransition.Fade)
      PaddingLeft: =
      RadiusBottomLeft: =Self.Width
      RadiusBottomRight: =Self.RadiusBottomLeft
      RadiusTopLeft: =Self.RadiusBottomLeft
      RadiusTopRight: =Self.RadiusBottomLeft
      Width: =Self.Height

```

To add your own icons to this list you need pull the raw SVG code from icons
taken from the global package and add them to the list. The easiest way would to
copy and paste a key value pair and change the SVG code as necessary. Finally,
run a find and replace on the SVG code block, change all double quotes (") into
single quotes (').


## Login catching

One of the strangest things that I never thought that I would need to add.

A way to capture who is logging into the application. I wanted to make sure the
supervisors of my area were actually using the application. Office politics as
it stands is a rough road to travel. I was asked to integrate more functionality
into the apps but I needed to confirm user activity. I didn't want to waste time
making features if the app wasn't being used.

Its a simple patch function that needs to pull from the azure directory to 
properly populate the sharepoint list that tracks the login info. What makes it
interesting is the way you need to pull the person field, but it's pretty self
explanatory. Its safe to remove completely if you don't want to setup login
tracking.

```cpp
Patch(
    LoginTracking,
    Defaults(LoginTracking), 
    {
        Person: {
            '@odata.type':"#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
            Claims: "i:0#.f|membership|" & User().Email,
            Department: "",
            DisplayName: User().FullName,
            Email: User().Email,
            JobTitle: "",
            Picture: ""
        },

        Application: APP_NAME
    }
);
```