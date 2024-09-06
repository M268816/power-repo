UpdateContext({
    locSelectedEndTime:
    DateTime(
        Year(DateValue4.SelectedDate),
        Month(DateValue4.SelectedDate),
        Day(DateValue4.SelectedDate),
        If(n_f_start_AMPM.Selected.Value = "PM", 12, 0) + Mod(Value(HourValue4.SelectedText.Value), 12),
        Value(MinuteValue4.SelectedText.Value),
        0
    ),
    locSelectedStartTime:
        DateTime(
            Year(DateValue3.SelectedDate),
            Month(DateValue3.SelectedDate),
            Day(DateValue3.SelectedDate),
            If(n_f_end_AMPM.Selected.Value = "PM", 12, 0) + Mod(Value(HourValue3.SelectedText.Value), 12),
            Value(MinuteValue3.SelectedText.Value),
            0
        )
});

/*Check for overlapping Time*/
Clear(hackFoundTime);

/*Super Hacknied time check*/
ForAll(Filter(collectDowntime, Line = varProductionLine),
    /*Of the selected times are...*/
    If(
        Or(
            /*... between recorded times*/
            And(
                locSelectedStartTime >= DateTimeValue(Started),

                locSelectedStartTime < TimeValue(Ended)
            ),
            /*Or the end time is between the recorded start and end time */
            And(
                locSelectedEndTime > DateTimeValue(Started),
                
                locSelectedEndTime <= DateTimeValue(Ended)
            ),
            /*Or the selected start time is between the recorded start and end time*/
            And(
                locSelectedStartTime >= DateTimeValue(Started),
                
                locSelectedStartTime < DateTimeValue(Ended)
            ),
            /*Or the selected times are encompassing a recorded time*/
            And(
                locSelectedStartTime < DateTimeValue(Started),
                
                locSelectedEndTime >  DateTimeValue(Ended)
            )
        ),
        
        Collect(hackFoundTime, {set: true}),
        
        Collect(hackFoundTime, {set: false})
    )
);

/*If anything in the hack is true then return true and set the variable*/
If(true in hackFoundTime, Set(varFoundTime, true), Set(varFoundTime, false));

/*Check for entry errors*/
If(
    /*If in edit mode editor person and reason are needed*/
    And(n_form.Mode = FormMode.Edit, Or(DataCardValue28.Selected.DisplayName=Blank(), DataCardValue29.Text = "")),
    /*Show the error*/
    UpdateContext({locPopups: {Visible: true, Value: "editor"}});,

    /*Hour ended must be later than hour started*/
    locSelectedEndTime <= locSelectedStartTime,
    /*Show the error*/
    UpdateContext({locPopups: {Visible: true, Value: "time"}});,

    /*If Quality or Safety not Selected, show error*/
    Or(Radio1.Selected.Value = Blank(), Radio2.Selected.Value = Blank()),
    /*Show the error*/
    UpdateContext({locPopups: {Visible: true, Value: "radio"}});,

    /*If times selected span more than 1 hour*/
    DateDiff(
        locSelectedStartTime,
        locSelectedEndTime,
        TimeUnit.Hours
    ) > 1,
    /*Show the error*/
    UpdateContext({locPopups: {Visible: true, Value: "timespan"}});,
    
    /*If the ending number is less than the starting number*/
    Value(DataCardValue19.Text) < Value(DataCardValue18.Text),
    /*Show the error*/
    UpdateContext({locPopups: {Visible: true, Value:"unit"}});,
        
    /*If the sum of rejects and QAs, exceeds the sum of obtained units*/
    Sum(Value(DataCardValue21.Text), Value(DataCardValue22.Text), Value(DataCardValue20.Text))
    > Sum(Value(DataCardValue19.Text), -Value(DataCardValue18.Text), 1),
    /*Show the error*/
    UpdateContext({locPopups: {Visible: true, Value: "sum"}});,
    
    /*If the start and end times already exist, aka duplicate entry*/
    And(
        n_form.Mode = FormMode.New,
        !IsBlank(
            LookUp(collectProduction,
                DateTimeValue(Hour_Starting) = locSelectedStartTime
            )
        ),
        !IsBlank(
            LookUp(collectProduction,
                DateTimeValue(Hour_Ending) = locSelectedEndTime
            )
        )
    ),
    /*Show the error*/
    UpdateContext({locPopups: {Visible: true, Value: "dupe"}});,

    /*
        If youre submitting a new entry,
        the hack check does not find a downtime reason,
        and the actual units built is less than the labor hour goal
    */
    And(
        varFoundTime = false,
        n_form.Mode = FormMode.New,
        (Value(DataCardValue19.Text) - Value(DataCardValue18.Text) + 1) - Sum(Value(DataCardValue20.Text),Value(DataCardValue21.Text),Value(DataCardValue22.Text))
        < varGoalsPerLaborHours
    ),
    /*Show the error*/
    UpdateContext({locPopups: {Visible: true, Value: "goal"}});,
    
    /*If the last hour has no entry*/
    IsBlank(
        LookUp(collectProduction,
            DateTimeValue(Hour_Ending) = DateTimeValue(DateAdd(locSelectedEndTime, -1, TimeUnit.Hours))
        )
    ),
    /*Show the error*/
    UpdateContext({locPopups: {Visible: true, Value: "missing"}});,

    /*Otherwise, clear the popup errors and submit the form*/
    UpdateContext({locPopups: {Visible: false, Value: Blank()}});
    SubmitForm(n_form);
      
);