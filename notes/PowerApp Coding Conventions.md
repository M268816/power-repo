# PowerApps coding conventions and syntax

> UPDATE 19 MAR 2025:
>
> After engorging myself with python tutorials and docs from various libraries,
> I took to the YouTubes to enlighten myself to the current programming culture
> and study the market for driven self taught little coding Jimmies. I found
> myself listening to a rant by Michael B Paulson, also known as ThePrimeagen,
> and realized I may have made a mistake. I name... *everything* in my PowerApps
> projects like a structurizing *psychopath*.
>
> Prime's high pitched, nasally little temper told me that what I was doing in
> PowerApps was unhinged. His 10+ year Netflix pedigree turned internet
> personality convinced me at least, the way I tried to use different naming
> conventions to describe the type of object I work with is more taxing than
> just keeping consistency. I blame my foray into python and big brother
> PEP 8 for showing me things like, variables use snake case, but classes use
> pascal. Like Alice I too then traveled down the rabbit hole, went *a bit*
> overboard, and used too many of these conventions to define separate
> objects. A self taught vibe coding rookie over correction that over the next
> few days I will be nuking with an orbital space laser and rectifying.
>
> Your little Jimmy,
>
> Ray

## Table of contents
1. [Conventions and Syntax](#powerapps-coding-conventions-and-syntax)
    1. [Initial Setup](#initial-setup)
    2. [Commenting](#commenting)
    3. [Snake-Case](#deciding-on-snake_case)
    4. [Versioning](#versioning)
    5. [Databases and Data Sources](#databases-or-data-sources)
    6. [User Preferences](#userpreferences)
    7. [Screens](#screens)
    8. [Objects / Controls](#objects--controls)
    9. [Variables](#variables)
        1. [Constant](#constant)
        2. [Local](#local)
        3. [Global](#global)
        4. [Universal](#universal)
    10. [Dates and Times](#dates-and-times)
    11. [Collections](#collections)
    12. [Records](#records)
    13. [Field Names](#field-names)
2. [Using the Templates](#using-the-templates)
    1. [Initialization](#initialization)
    2. [Standard Variables](#standard-variables)
    3. [Navigation](#navigation)
    4. [The popup manager](#the-popup-manager)
    5. [Themes](#themes-and-theme-modes)
    6. [Icon Manager](#icon-manager)
    7. [Login Catching](#login-catching)

## Initial Setup

[Back To Top](#powerapps-coding-conventions-and-syntax)

Before putting pen to paper... or I guess fingers to keys... mouse to clicks?
It's best to setup the applications Update settings. Enter the Settings menu in
the application editor, located at the bottom left as a gear icon, then select
'Updates'. From here select the 'Retired' tab and turn off all options. Next,
turn off all options within the 'Experimental' tab. You can turn these on if
you need them later, but for now should not be used by default. Under the
preview tab, you can turn on pretty much everything as these features are
currently in testing and should be available soon anyway. I highly recommend
turning off any copilot features though, most of them are simply annoying.
Within the 'New' tab, its best to leave Coauthoring off unless working closely
on a joint project. Modern controls and themes can be turned on, as creating a
new default theme comes in very handy when changing the font style of the whole 
application. New analysis engine should be turned on along with the rest of this
tab. Again, I do highly recommend turning off the copilot features.

## Commenting

[Back To Top](#powerapps-coding-conventions-and-syntax)

No big comment rules here, just be sure to use comments for tricky parts of
formulas or functions

```cpp
// Inline Comments!

/*
    Block
    Comments!

*/
```

## Deciding on snake_case

[Back To Top](#powerapps-coding-conventions-and-syntax)

Previous versions of my conventions and syntax included multiple kinds of
naming conventions to distinguish between types of objects in a PowerApp. This
included Using PascalCase for databases, Proper_Snake for table headers, and
the disastrous kebob-case for PowerApp widgets.

I'm going to throw that all out the window and use snake_case, beloved by
python devs and [PEP 8](https://peps.python.org/pep-0008/) users everywhere.

Some takeaways from this type of naming are using PascalCase for custom
functions (like Classes with python), CAPITAL or SCREAMING_SNAKE_CASE
for constants, and always using lowercase for variables and applying snake_case
to improve readability.

I believe this will also help us with visibility, as the PowerApp conventions
like to use camel case. So we will be able to determine with greater accuracy 
what part of the code is built it PowerFX and what is our written scripting.

I will explore some syntax for these conventions later on.

## Versioning

The default PowerApp updater is lost to many users. The apps unfortunately do
not automatically update for users when the app is opened. Instead, it prompts
the user with a very small banner at the top of the app to refresh the app to
update to a new version. Because the update banner can be missed so easily,
users seem to miss updates consistently.

This has prompted me to include a version control system that uses an external
database to check the current version of an app to the stored version manually.

I plan to use a simple [semver](https://semver.org/) system.

## Databases or data sources

[Back To Top](#powerapps-coding-conventions-and-syntax)

When using outside data sources, it's good practice to first create the database
you want to pull the information from. Once the initial database structure is
built, it makes linking to PowerApps a much simpler process.

For ease of setup and dissuade any Premium charges on built applications,
I use SharePoint Lists as Databases for my applications. In naming lists I will
use these conventions:

### user_preferences

| first_name | last_name | email                             | theme_mode |
|:---------- |:--------- |:--------------------------------- |:---------- |
| Raymond    | Comeau    | raymond.comeau@milliporesigma.com | Light      |
| Someone    | Else      | someone.else@milliporesigma.com   | Dark       |

## Screens

[Back To Top](#powerapps-coding-conventions-and-syntax)

> scr_home

> scr_order_materials

Screen objects within PowerApps will be prefixed with 'scr' and referenced in
the tree structure by their first letter. Naming objects down the tree is
explained in the next section.

```cpp
|_. scr_home
    |_. h_widget_name

|_. scr_order_materials
    |_. o_widget_name
```

## Objects / Controls

[Back To Top](#powerapps-coding-conventions-and-syntax)

Because the complexity of object trees can increase quickly naming objects in
the app can get out of hand quickly. To combat this, I begin the name of an
object with the first initial of its parent screen then add the highest significant
parent of the object on the tree until I need to use a unique identifier. For
example, A button that would submit information on the home page, located in the
main form content of the screen may be named 'h_form_submit_btn'. Notice the 
suffix 'btn'. I also add widget types to the end of the name when applicable.

The parent structure now looks like this.

```cpp
|_. scr_Home
    |_. h_popups
        |_. h_popup_error
        |_. h_popup_error_header
        |_. h_popup_error_body
        |_. h_popup_error_footer
    |_. h_popup_warning
      |_. h_popup_warning_header
      |_. h_popup_warning_body
      |_. h_popup_warning_footer
    |_. h_main
        |_. h_header
            |_. h_title
        |_. h_body
        |_. h_form_parent
            |_. h_form_title
            |_. h_form
            |_. h_form_buttons
                |_. h_form_submit
                |_. h_form_cancel
        |_. h_footer
            |_. h_legal
```

Each object starts with the first letter of the screen's name. Then they receive
either, their own name, become a parent, or take their parent's name. We can see
this with the submit button. The submit button in this tree takes its parent
name 'form' to describe it is the submit button for the form. But, because this
form may not be the only form within the application, we also give the form its
parent screen's initial with 'h'. Therefore the button that submits the form on 
the home screen would be called 'h_form_submit'.

To reinforce that nested widgets should only try to be as distinctive as their 
*highest significant parent*, we can also see the button does not need to relate
to the body of the screen or even that it's a child of the 'h_form_buttons'
container, but only that it relates to the form itself.

But with objects like the popups, this does get ugly. If we need to distinguish 
between a loading error and a type error the names get pretty long.
```cpp
|_. h_popup_error_404_parent
    |_. h_popup_error_404
    |_. h_popup_error_404_buttons
        |_. h_popup_error_404_submit
        |_. h_popup_error_404_cancel
|_.h_popup_error_502_parent
    |_. h_popup_error_502
    |_. h_popup_error_502_buttons
        |_. h_popup_error_502_submit
        |_. h_popup_error_502_cancel
```

Now what about the trailing suffix that I alluded to?

When working with objects that have the same principle, adding the widget type
as a suffix will help determine what widget to access. For instance, lets take a
date filtering system. We need a date picker widget to allow a filtering 
selection, and also a label to help the user determine what the date picker does.

```cpp
|_. h_filters_parent
    |_. h_start_date_lbl
    |_. h_start_date
    |_. h_filter_separator // A rectangle used as a horizontal rule
    |_. h_end_date_lbl
    |_. h_end_date_dpk

```

Here are two examples of how you could apply the suffixes. For the start date
widgets, we only stated that the label widget as _lbl, but allowed the widget
we would access in the formulas as the start_date.

```cpp
Filter(some_data, Date >= h_start_date.SelectedDate)
```

The second use with the end date is also valid, you can supply a suffix for both
the label and the dropdown. As long as you know what widget to access to pull
the date selection from.

```cpp
Filter(some_data, Date < h_end_date_dpk.SelectedDate)
```

## Variables

[Back To Top](#powerapps-coding-conventions-and-syntax)

PowerApp development is in a fight with itself over where it wants to store its 
variables. Instead of having a nice clean universal variable handler instead we
need to use two functions: Set() and UpdateContext({}).

Set() is used for variables that need to span the entire app. They can be set
and accessed anywhere in the app. Set() variables are immutable, so to update a
record used with Set() the whole variable must be updated. Individual pieces of
the record cannot be updated separately.

UpdateContext({}) creates variables that can only be set and accessed in the
screen they were initialized. UpdateContext({}) record variables are mutable with
the Patch() function.

```cpp
Set(gbl_variable, value);

UpdateContext({loc_variable: value});
```

The variable scopes I use in a PowerApp are constant, local, global, and
something I call universal. Here are the conventions that I use.

### Constant

- Variables that should be set, and not changed.
    - Use the Set() function.
    - Screaming Snake case.
    - The actual concept of constants do no exist within PowerApps, so this must
    be self regulated. Whenever you need a constant set it on the app start
    property then make sure to only read the variable and not write it.
    ```cpp
    Set(THEME_MODE, styles.dark);
    ```

### Local

- Variables that only need to apply to the current loaded screen.
    - Use the UpdateContext({}) function.
    - Prefix with 'loc'.
    ```cpp
    UpdateContext({loc_theme_mode: styles.dark});
    ```

### Global

- Variables that need to be applied across the whole application.
    - Use the Set() function.
    - Prefix with 'gbl'.
    ```cpp
    Set(gbl_theme_mode, styles.dark);
    ```
### Universal

- Variables that need to be applied across application *sessions*.
    - Use the Set() function.
    - Prefix with 'UNI'.
    - Screaming Snake case.
    - Init the value from a data source.
    - Set new values to the data source.
    ```cpp
    // Init the value from the data source
    Set(UNI_THEME_MODE,
        LookUp(user_preferences, email=User().Email).theme_mode
    )
    
    // To set the variable, use Patch()
    Patch(user_preferences,
        LookUp(user_preferences, email=User().Email).id,
        {
            Theme_Mode: {Value: "Dark"}
        }
    );
    ```
    
Because variables init at runtime, variables that need to be set and remembered
across sessions cannot be used natively in PowerApps. Let's use the dark mode
variable above as an example.

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

[Back To Top](#powerapps-coding-conventions-and-syntax)

The Today() and Now() functions will only update their values when called or
used to set parameters. This means for widgets like the Text Label, when
Today() and Now() are used it only pulls in the value stored the last time they
were called. Other times it works as intended. These are so inconsistent that
I fix this by assigning the functions to variables.

The variables are set at a global level each time a screen is loaded or 
logic needs to be run. The variables I set for these purposes is as follows:

```cpp
Set(gbl_today, Today());

Set(gbl_now, Now());

Set(gbl_hour, Hour(Now()));

/*Or to allow for dot notation*/

Set(gbl_time,
    {
        today: Today(),
        now: Now(),
        hour: Hour(Now())
    }
);

// getter: gbl_time.today etc
```

## Collections

[Back To Top](#powerapps-coding-conventions-and-syntax)

Collections in PowerApps are powerful data structures that can be used for a
large variety of data management. These collections can be used to not only
store and display data from within the app, but you can pull data from outside
databases like share point lists to create local copies. These local copies can
be manipulated without needing to worry about delegation and are often much
more performant. Collections can even be used to create static lists,
dictionaries, arrays, or tables of variables.

- Collections
    - Use Collect() for initialization, or within ForALL() loops.
    - Use ClearCollect() for everything else.
    - Prefix the collection with 'col'

```cpp
// Clear the collection for new data
Clear(col_production);
// For all Records in this data
ForAll(encapsulation_production,
    //Collect each record into colProduction
    Collect(col_production,
        {
            id: ThisRecord.ID,
            line: ThisRecord.line,
            unit_start: ThisRecord.unit_start,
            unit_end: ThisRecord.unit_end,
            date_start: ThisRecord.date_start,
            date_end: ThisRecord.date_end,
            shift: ThisRecord.shift_letter,
        }
    )
);
```

## Records

[Back To Top](#powerapps-coding-conventions-and-syntax)

Single record collections are useful for creating mutable variables accessible
with dot notation. I make sure to only ever init the collection, then change its
variables with the Patch() function. There is a drawback to this method. To use
the dot notation, you need to use the First() function to access the record. 
However, through extensive testing, this is the only way to make mutable data
structures and variables that can use dot notation.

- Mutable Records
    - Use Collect() for initialization.
    - Prefix the collection with 'rec'
    - Set new values with Patch()
    - Get values with First()

```cpp
// Initialize
ClearCollect(rec_popups,
    {
        display_text: "Not Loading",
        value: -1,
        popup: "",
        visible: false
    }
);

// Setter
Patch(rec_popups,First(rec_popups),{value: 10});
// Getter
First(rec_popups).Value
```

When we only need to store a single immutable record. Instead of using a
collection, we use the Set() function like we would set a variable. We structure
the variable just like we would structure a record in a collection. Using single
records this way allows us to use dot notation to pull in data more readily.
I'm not sure that this method ensures we use as little memory as possible within
the app, but when I changed to this system I seen recognizable performance
increases. It seems setting a record variable is less intensive than setting up
a collection for a single record. The downside to this, is that Set() records
must be updated in their entirety, as the Patch() function will not work with
Set().

- Immutable Records
    - Use Set() for initialization.
    - Prefix the record with 'rec'

```cpp
// Initialize and Setter
Set(rec_oee,
    {
        oee2: 0.5,
        amount_built: 100,
        goal: 200,
        rejects: 5
    }
);

// Getter
rec_oee.goal
```

## Field Names

[Back To Top](#powerapps-coding-conventions-and-syntax)

As shown in earlier examples when naming field names within collections, tables,
lists or dictionaries the field or column name will use regular snake case and
should try to keep the same name as its parent database.

```cpp
// Copying the original data source into a local copy.
ForAll(data_Source,
    Collect(col_local_collection,
        {
            id: ThisRecord.ID,
            datetime: ThisRecord.datetime,
            first_unit: ThisRecord.first_unit,
            last_unit: ThisRecord.last_unit
        }
    )
);
```

Because sharepoint has many fields that we may not use, if you need only a select
group of information, using the ShowColumns() function is also a great way to
improve performance. This will make sure that the initial lookup of the database
only pulls in the relevant information to copy into the collection.

```cpp
// Copying the original data source into a local copy.
ForAll(data_Source,
    Collect(
        ShowColumns(col_local_collection,
            id,
            datetime
        ),
        {
            id: ThisRecord.ID,
            datetime: ThisRecord.datetime
        }
    )
);
```

# Using the Templates

[Back To Top](#powerapps-coding-conventions-and-syntax)

Using the yaml templates from the git repo is pretty simple. To get started,
first create a new screen, then copy the yaml code form the repo, and paste it
into the screen using the paste code menu item.

The yaml code for the Init and Bug Report Screens have pre-configured naming
conventions. Other yaml code should be configured with 'find and replace' to set
the naming conventions appropriately.

For example, in PowerApps make a scr_init and scr_home screen. Then, paste the
appropriate yaml into those screens. The naming conventions for initialization
is already setup, but then the home screen will need to have the prefix changed.
Within this template, the names of the controls need to be changed from the
placeholder prefix 'xHx' to 'h' for home. Use can find and replace in any text
editor with any template to find and replace the prefix with the prefix of the
screen you are setting up.

## Initialization

[Back To Top](#powerapps-coding-conventions-and-syntax)

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
If(INITIALIZE, Select(i_init));
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

[Back To Top](#powerapps-coding-conventions-and-syntax)

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
Set(gbl_padding, Round(App.Width * 0.005,0));

/* 
    Setting time variables is important because static objects will not
    update these functions without a direct update to them. Setting these
    functions to a variable updates this info whenever they load, in turn
    updating the static objects.
*/
Set(gbl_time,{Today:Today(),Now:Now()});

/*
    Using a global variable to pull in static data with dot notation is always
    very valuable. These lists are used constantly throughout the app, for
    many various applications.
*/
Set(gbl_lists,
    {
        shifts: [
            "C","A","B"
        ],
        lines: [
            "XL1", "XL2", "XL3", "XL4", "XL5",
            "XLT", "XLT2", "XLT3",
            "SSC", "SSC2"
        ],
        downtime_reasons: [
            "Reason 1","Reason 2","Reason 3","Reason 4",
            "Reason 5","Reason 6","Reason 7","Reason 8",
        ]
    }
);
```

## Navigation

[Back To Top](#powerapps-coding-conventions-and-syntax)

The navigation system that I apply to my apps uses a collection of screens.

```cpp
ClearCollect(col_navigation,
    {screen: Home, label: "Home"},
    {screen: Filterable, label: "Filterable"},
    {screen: Singleton, label: "Singleton"},
    {screen: Data, label: "Data"}
);
```

It holds the Screen Object in 'Screen' and a text label in 'Label'.

With this collection initialization, it creates a data structure I can use to
populate a gallery for navigation on each screen. This data structure can be
edited from initialization and automatically update all other instances of the
navigation gallery throughout the whole application.

```yaml
- h_navigation_gallery:
    Control: Gallery@2.15.0
    Variant: Vertical
    Properties:
      AlignInContainer: =AlignInContainer.SetByContainer
      Items: =col_navigation
      LayoutMinHeight: =10
      LayoutMinWidth: =10
      TemplatePadding: =gbl_Padding
      TemplateSize: =40
    Children:
      - hNavGalleryButton:
          Control: Classic/Button@2.2.0
          Properties:
            BorderThickness: =1
            Color: =gbl_theme.text_dark
            DisplayMode: -|
                =If(App.ActiveScreen.Name = ThisItem.Screen.Name,
                    DisplayMode.Disabled,
                    DisplayMode.Edit
                )
            Fill: =gbl_theme.accent
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

[Back To Top](#powerapps-coding-conventions-and-syntax)

The popup manager uses a collection to store a single global record. This record
is then mutable anywhere in the application. It allow us to dynamically change
any variable associated with the record and pull the information through dot
notation.

```cpp
// Popup Manager
ClearCollect(rec_popups,
    {
        display_text: "Not Loading",
        value: -1,
        popup: "",
        visible: false
    }
);
// Setter: Patch(rec_popups,First(rec_popups),{value: 10});
// Getter: First(rec_popups).value
```

I'm not going to lie the variables that I use are very jank.

'display_text' is used to display any type of loading information through any
text object or property.

'value' is used to determine the status of the loading and spinner objects. I 
typically use -1 to determine if properties should be turned off or
indeterminate. For example, in a progress bar, the bar will cycle like a 
spinner when indeterminate is set to true. Otherwise it will set the position of
the inner colored loading bar.

'visible' is fairly well explained, as it determines if the popup manager should
be visible.

'popup', on the other hand is a very messy way I determined what popup should be
displaying. Some screens have various popups that need to display, like
errors, or simple loading prompts. To determine what popup to show, I use a
string variable that describes the popup. For example, the loading popup would
be named 'loading'. An error for bad information would be called 'error'. And 
a confirmation dialog would be 'confirm'.

The parent object that controls all popups will use the 'visible' variable to
determine weather or not to show a popup.

But the 'popup' variable determines what popup to display in the parent object.

```yaml
# Parent Properties
- h_popups:
    Control: GroupContainer@1.3.0
    Variant: AutoLayout
    Properties:
      Visible: =First(rec_popups).visible # show the manager via boolean
```

```yaml
# Child Properties
- h_popup_error:
    Control: GroupContainer@1.3.0
    Variant: AutoLayout
    Properties:
      Visible: = First(rec_popups).popup = "error" # show the popup via equality
```

## Themes and theme modes

[Back To Top](#powerapps-coding-conventions-and-syntax)

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
Set(gbl_styles,
    {
        light:
        {
            style: "light",
            text_dark: ColorValue("#000000"),
            text_on_dark: ColorValue("#FFFFFF"),
            Text_Light: ColorValue("#FFFFFF"),
            Text_On_Light: ColorValue("#000000"),
            background: ColorValue("#FFFFFF"),
            midground: ColorValue("#EEEEEE"),
            foreground: ColorValue("#DDDDDD"),
            primary: ColorValue("#503291"),
            pri_complement: ColorValue("#2DBECD"),
            secondary: ColorValue("#0f69af"),
            sec_complement: ColorValue("#FFDBC9"),
            accept: ColorValue("#149B5f"),
            deny: ColorValue("#e61e50"),
            accent: ColorValue("#FFC832"),
            chart_black: "#121212",
            chart_white: "#FFFFFF",
            chart_red: "#e61e50",
            chart_blue: "#503291",
            chart_accent: "#FFC832",
            chart_dim: "#787878"
        },
        dark:
        {
            Style: "dark",
            text_dark: ColorValue("#000000"),
            text_on_dark: ColorValue("#000000"),
            Text_Light: ColorValue("#FFFFFF"),
            Text_On_Light: ColorValue("#FFFFFF"),
            background: ColorValue("#121212"),
            midground: ColorValue("#232323"),
            foreground: ColorValue("#343434"),
            primary: ColorValue("#565656"),
            pri_complement: ColorValue("#ec9d99"),
            secondary: ColorValue("#676767"),
            sec_complement: ColorValue("#af9ecf"),
            accept: ColorValue("#98d3b2"),
            deny: ColorValue("#f68da5"),
            accent: ColorValue("#ffdf85"),
            chart_black: "#FFFFFF",
            chart_white: "#121212",
            chart_red: "#f68da5",
            chart_blue: "#0f69af",
            chart_accent: "#ffdf85",
            chart_dim: "#565656"
        }
    }
);
```

Step two, make these settings easily accessible with dot notation.

```cpp
Set(gbl_theme, gbl_styles.light);
```

I also set up a way to check what theme is currently active. Although, it does
use the simple string system like the popup manager does. This is a simple setup
to change from dark mode to light mode.

```cpp
If(gbl_theme.Style = "light",
    Set(gbl_theme, gbl_styles.dark),
    Set(gbl_theme, gbl_styles.light)
)

// I should probably change the variables to be more readable though, like this
If(gbl_theme.Style = "light",
    Set(gbl_theme, gbl_styles.dark),
    Set(gbl_theme, gbl_styles.light)
)
```

## Icon manager

[Back To Top](#powerapps-coding-conventions-and-syntax)

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
- h_bugs:
    Control: Image@2.2.3
    Properties:
      BorderColor: =RGBA(0, 18, 107, 1)
      HoverFill: =gbl_theme.pri_complement
      Image: =gbl_icons.bug # EZPZ
      ImagePosition: =ImagePosition.Fill
      LayoutMinHeight: =10
      OnSelect: =Navigate(scr_bugs,ScreenTransition.Fade)
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

[Back To Top](#powerapps-coding-conventions-and-syntax)

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