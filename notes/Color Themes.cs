/*
    Theme Colors

    RGBA(80, 50, 145, 1)    //Rich Purple
    RGBA(15, 105, 175, 1)   //Rich Blue
    RGBA(20, 155, 95, 1)    //Rich Green
    RGBA(230, 30, 80, 1)    //Rich Red
    RGBA(235, 060, 150, 1)  //Vibrant Magenta
    RGBA(45, 190, 205, 1)   //Vibrant Cyan
    RGBA(165, 205, 80, 1)   //Vibrant Green
    RGBA(255, 200, 50, 1)   //Vibrant Yellow
    RGBA(150, 215, 210, 1)  //Sensitive Blue
    RGBA(255, 195, 205, 1)  //Sensitive Pink
    RGBA(180, 220, 150, 1)  //Sensitive Green
    RGBA(255, 220, 185, 1)  //Sensitive Yellow


    #503291                 //Rich Purple Hex
    #0F69AF                 //Rich Blue Hex
    #149B5F                 //Rich Green Hex
    #E61E50                 //Rich Red Hex
    #EB3C96                 //Vibrant Magenta Hex
    #2DBECD                 //Vibrant Cyan Hex   
    #A5CD50                 //Vibrant Green Hex
    #FFC832                 //Vibrant Yellow Hex
    #96D7D2                 //Sensitive Blue Hex
    #FFC3CD                 //Sensitive Pink Hex
    #B4DC96                 //Sensitive Green Hex
    #FFDBC9                 //Sensitive Yellow Hex
    
    // Color deficiency ?
    #FFD48E                 //sunset
    #FFAF2F                 //Orange
    #2DBECD                 //Robin Egg Blue
    #6052A5                 //ultra violet
    #503291                 //tekhelet

    //Dark Mode?
    //Light
    #000000 Black
    #FFFFFF White
    #503291 Primary Purple
    #739132 Primary Green Complementary
    #0F69AF Secondary Blue
    #AF540F Secondary Orange Complementary
    #149B5F Accept Green
    #E61E50 Deny Red
    #FFC832 Accent Yellow
    
    //Dark
    #121212 Black
    #FFFFFF White
    #373737 Primary Gray
    #B5C97B Primary Green Complementary
    #717171 Secondary Gray
    #ed771b Secondary Orange Complementary
    #98d3b2 Accept Green
    #fabac9 Deny Red
    #fff8e2 Accent Yellow

*/

/*New Themes*/

If(
    /* Merck Blue */
    Self.SelectedText.Value = "Merck Blue",
    
    Set(varColor0, Color.Black);
    Set(varColor1, RGBA(80, 50, 145, 1));       //Rich Purple
    Set(varColor2, RGBA(15, 105, 175, 1));      //Rich Blue
    Set(varColor3, RGBA(45, 190, 205, 1));      //Vibrant Cyan
    Set(varColor4, RGBA(255, 220, 185, 1));     //Sensitive Yellow
    Set(varColor5, Color.White);
    Set(varColorAccent, RGBA(255, 200, 50, 1)); //Vibrant Yellow
    Set(varColorYes, RGBA(20, 155, 95, 1));     //Rich Green
    Set(varColorNo, RGBA(230, 30, 80, 1));      //Rich Red
    Set(varHexRich, "#503291");
    Set(varHexAccent, "#FFC832");
    Set(varHexYes, "#149B5F");
    Set(varHexNo, "#E61E50");,

    /* Merck Green */
    Self.SelectedText.Value = "Merck Green",
    
    Set(varColor0, Color.Black);
    Set(varColor1, RGBA(80, 50, 145, 1));       //Rich Purple
    Set(varColor2, RGBA(20, 155, 95, 1));       //Rich Green
    Set(varColor3, RGBA(180, 220, 150, 1));     //Sensitive Green
    Set(varColor4, RGBA(150, 215, 210, 1));     //Sansitive Blue
    Set(varColor5, Color.White);
    Set(varColorAccent, RGBA(165, 205, 80, 1)); //Vibrant Green
    Set(varColorYes, RGBA(15, 105, 175, 1));    //Rich Blue
    Set(varColorNo, RGBA(230, 30, 80, 1));      //Rich Red
    Set(varHexRich, "#503291");
    Set(varHexAccent, "#FFC832");
    Set(varHexYes, "#0F69AF");
    Set(varHexNo, "#E61E50");
)

/*Old Themes*/


If(
    /* Merck Blue */
    Self.SelectedText.Value = "Merck Blue",
    
    Set(varColor0, Color.Black);
    Set(varColor1, RGBA(80, 50, 145, 1));       //Rich Purple
    Set(varColor2, RGBA(15, 105, 175, 1));      //Rich Blue
    Set(varColor3, RGBA(255, 195, 205, 1));     //Sensitive Pink
    Set(varColor4, RGBA(255, 220, 185, 1));     //Sensitive Yellow
    Set(varColor5, Color.White);
    Set(varColorAccent, RGBA(255, 200, 50, 1)); //Vibrant Yellow
    Set(varColorYes, RGBA(20, 155, 95, 1));     //Rich Green
    Set(varColorNo, RGBA(230, 30, 80, 1));      //Rich Red
    Set(varHexRich, "#503291");
    Set(varHexAccent, "#FFC832");
    Set(varHexYes, "#149B5F");
    Set(varHexNo, "#E61E50");,

    /* Merck Green */
    Self.SelectedText.Value = "Merck Green",
    
    Set(varColor0, Color.Black);
    Set(varColor1, RGBA(80, 50, 145, 1));       //Rich Purple
    Set(varColor2, RGBA(165, 205, 80, 1));      //Vibrant Green
    Set(varColor3, RGBA(255, 220, 185, 1));     //Sensitive Yellow
    Set(varColor4, RGBA(45, 190, 205, 1));      //Vibrant Cyan
    Set(varColor5, Color.White);
    Set(varColorAccent, RGBA(255, 200, 50, 1)); //Vibrant Yellow
    Set(varColorYes, RGBA(20, 155, 95, 1));     //Rich Green
    Set(varColorNo, RGBA(230, 30, 80, 1));      //Rich Red
    Set(varHexRich, "#503291");
    Set(varHexAccent, "#FFC832");
    Set(varHexYes, "#149B5F");
    Set(varHexNo, "#E61E50");,

    /* Blue Theme */
    Self.SelectedText.Value = "Blue Theme",
    
    Set(varColor0, Color.Black);
    Set(varColor1, RGBA(56, 96, 178, 1));
    Set(varColor2, RGBA(84, 123, 201, 1));
    Set(varColor3, RGBA(115, 147, 210, 1));
    Set(varColor4, RGBA(146, 171, 221, 1));
    Set(varColor5, Color.White);
    Set(varColorAccent, RGBA(255, 215, 145, 1));
    Set(varColorYes, Color.ForestGreen);
    Set(varColorNo, Color.IndianRed);
    Set(varHexAccent, "#FFD791");,

    /* Blue Steel Theme */
    Self.SelectedText.Value = "Blue Steel Theme",
    
    Set(varColor0, Color.Black);
    Set(varColor1, RGBA(0, 78, 152, 1));
    Set(varColor2, RGBA(58, 110, 165, 1));
    Set(varColor3, RGBA(192, 192, 192, 1));
    Set(varColor4, RGBA(235, 235, 235, 1));
    Set(varColor5, Color.White);
    Set(varColorAccent, RGBA(192,192,235,1));
    Set(varColorYes, RGBA(103,148,54,1));
    Set(varColorNo, RGBA(223,41,53,1));
    Set(varHexAccent, "#C0C0EB");,

    /* Earthen Theme */
    Self.SelectedText.Value = "Earthen Theme",

    Set(varColor0, Color.Black);
    Set(varColor1, RGBA(65, 82, 31, 1));
    Set(varColor2, RGBA(168, 159, 104, 1));
    Set(varColor3, RGBA(208, 177, 122, 1));
    Set(varColor4, RGBA(245, 253, 198, 1));
    Set(varColor5, Color.White);
    Set(varColorAccent, RGBA(245, 195, 150, 1));
    Set(varColorYes, RGBA(4,114,77,1));
    Set(varColorNo, RGBA(201,93,99,1));
    Set(varHexAccent, "#F5C396");,

    /*Grayscale Theme*/
    Self.SelectedText.Value = "Grayscale Theme",

    Set(varColor0, Color.Black);
    Set(varColor1, RGBA(41, 41, 41, 1));
    Set(varColor2, RGBA(82, 82, 82, 1));
    Set(varColor3, RGBA(143, 143, 143, 1));
    Set(varColor4, RGBA(200, 200, 200, 1));
    Set(varColor5, Color.White);
    Set(varColorAccent, RGBA(220, 232, 238, 1));
    Set(varColorYes, Color.Green);
    Set(varColorNo, Color.Red);
    Set(varHexAccent, "#DCE8EE");,

    /*Professional Theme*/
    Self.SelectedText.Value = "Professional Theme",
    
    Set(varColor0, Color.Black);
    Set(varColor1, ColorValue("#252125"));
    Set(varColor2, ColorValue("#737686"));
    Set(varColor4, ColorValue("#1C9FE0"));
    Set(varColor3, ColorValue("#60B9D2"));
    Set(varColor5, ColorValue("#F5ECED"));
    Set(varColorAccent, ColorValue("#E6EBD6"));
    Set(varColorYes, ColorValue("#4F9D69"));
    Set(varColorNo, ColorValue("#CC0025"));,

    /*Default - Grayscale Theme*/
    Set(varColor0, Color.Black);
    Set(varColor1, RGBA(41, 41, 41, 1));
    Set(varColor2, RGBA(82, 82, 82, 1));
    Set(varColor3, RGBA(143, 143, 143, 1));
    Set(varColor4, RGBA(200, 200, 200, 1));
    Set(varColor5, Color.White);
    Set(varColorAccent, RGBA(220, 232, 238, 1));
    Set(varColorYes, Color.Green);
    Set(varColorNo, Color.Red);
    Set(varHexAccent, "#DCE8EE");
);

Set(varColorTheme, Self.SelectedText.Value);


// NEWEST Light/Dark Theme
Set(gThemeMode, 
    {
        Light:
        {
            Mode: "Light",
            Text_Dark: ColorValue("#000000"),
            Text_Light: ColorValue("#FFFFFF"),
            Text_Header: ColorValue("#FFFFFF"),
            Text_Accent: ColorValue("#000000"),
            Background_0: ColorValue("#FFFFFF"),
            Background_1: ColorValue("#EEEEEE"),
            Primary: ColorValue("#503291"),
            Pri_Complement: ColorValue("#2DBECD"),
            Secondary: ColorValue("#0f69af"),
            Sec_Complement: ColorValue("#AD540F"),
            Accept: ColorValue("#149B5f"),
            Deny: ColorValue("#e61e50"),
            Accent: ColorValue("#FFC832")
        },
        Dark:
        {
            Mode: "Dark",
            Text_Dark: ColorValue("#FFFFFF"),
            Text_Light: ColorValue("#000000"),
            Text_Header: ColorValue("#FFFFFF"),
            Text_Accent: ColorValue("#000000"),
            Background_0: ColorValue("#121212"),
            Background_1: ColorValue("#232323"),
            Primary: ColorValue("#373737"),
            Pri_Complement: ColorValue("#444444"),
            Secondary: ColorValue("#717171"),
            Sec_Complement: ColorValue("#af9ecf"),
            Accept: ColorValue("#98d3b2"),
            Deny: ColorValue("#f68da5"),
            Accent: ColorValue("#ffdf85")
        }
    }
);

Set(gTheme, gThemeMode.Light);


Set(gThemeMode, 
    {
        Light:
        {
            Mode: "Light",
            Text_On_Light: ColorValue("#000000"),
            Text_On_Dark: ColorValue("#FFFFFF"),
            Text_Dark: ColorValue("#000000"),
            Text_Light: ColorValue("#FFFFFF"),
            Text_Header: ColorValue("#FFFFFF"),
            Text_Accent: ColorValue("#000000"),
            Background: ColorValue("#FFFFFF"),
            Foreground: ColorValue("#EEEEEE"),
            Primary: ColorValue("#503291"),
            Pri_Complement: ColorValue("#2DBECD"),
            Secondary: ColorValue("#0f69af"),
            Sec_Complement: ColorValue("#AD540F"),
            Accept: ColorValue("#149B5f"),
            Deny: ColorValue("#e61e50"),
            Accent: ColorValue("#FFC832")
        },
        Dark:
        {
            Mode: "Dark",
            Text_On_Light: ColorValue("#FFFFFF"),
            Text_On_Dark: ColorValue("#000000"),
            Text_Dark: ColorValue("#000000"),
            Text_Light: ColorValue("#FFFFFF"),
            Text_Header: ColorValue("#FFFFFF"),
            Text_Accent: ColorValue("#000000"),
            Background: ColorValue("#121212"),
            Foreground: ColorValue("#232323"),
            Primary: ColorValue("#373737"),
            Pri_Complement: ColorValue("#444444"),
            Secondary: ColorValue("#717171"),
            Sec_Complement: ColorValue("#af9ecf"),
            Accept: ColorValue("#98d3b2"),
            Deny: ColorValue("#f68da5"),
            Accent: ColorValue("#ffdf85")
        }
    }
);

Set(gTheme, gThemeMode.Light);


/*Default Formatting Variables*/
Set(gThemeMode, 
    {
        Light:
        {
            Mode: "Light",
            Text_Dark: ColorValue("#000000"),
            Text_Light: ColorValue("#FFFFFF"),
            Text_Header: ColorValue("#FFFFFF"),
            Text_Accent: ColorValue("#000000"),
            Background_0: ColorValue("#FFFFFF"),
            Background_1: ColorValue("#EEEEEE"),
            Background_2: ColorValue("#DDDDDD"),
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
            Mode: "Dark",
            Text_Dark: ColorValue("#FFFFFF"),
            Text_Light: ColorValue("#000000"),
            Text_Header: ColorValue("#FFFFFF"),
            Text_Accent: ColorValue("#000000"),
            Background_0: ColorValue("#121212"),
            Background_1: ColorValue("#232323"),
            Background_2: ColorValue("#343434"),
            Primary: ColorValue("#454545"),
            Pri_Complement: ColorValue("#ec9d99"),
            Secondary: ColorValue("#565656"),
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