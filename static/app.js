function onSubmitData()
{
    var startDate = document.getElementById('startDate').value
    var endDate = document.getElementById('endDate').value

    if(startDate!==null && startDate!=='' && endDate!==null && endDate!=='') {
        $.ajax({
            url: "/getEventJsonData",
            type: "GET",
            contentType: 'application/json;charset=UTF-8',
            data: {
                'startDate': startDate,
                'endDate': endDate
            },
            dataType: "json",
            success: function (data) {
                var length=Object.keys(data).length;
                var responseText=""
                if(length>0)
                {
                    responseText = JSON.stringify(data, undefined, 4);
                    $('#jsonResponse').removeAttr( 'style' );
                }
                else
                {
                    responseText = "Sorry, there isn't any NFL event available between selected dates" + String.fromCodePoint(128580);
                     $("#jsonResponse").css({"color": "red", "font-size": "3.0rem"});
                }
               $('#jsonResponse').text(responseText);

            }
        });
    }
    else
    {
        alert("please enter valid startDate and endDate")
    }
}
