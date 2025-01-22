/* Merck Colors for PowerApps

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

*/

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
Set(gTheme, gThemeMode.Light);