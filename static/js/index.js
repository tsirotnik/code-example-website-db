/*jslint browser: true*/
/*global  $*/


$(document).ready(function() {
    "use strict";

    // slider creation
    var slider = $("#slideFilter").slider(),
        sliderval = 0;

    // slider stop event
    $("#slideFilter").on("slideStop", function(slideEvt) {
        $('#sliderValue').text(slideEvt.value);
        sliderval = slideEvt.value;
        // disable the slider until data is reloaded
        slider.slider('disable');
        $("#jsGrid").jsGrid("reset");
    });

    // slider sliding
    $("#slideFilter").on("slide", function(slideEvt) {
        $('#sliderValue').text(slideEvt.value);
    });


    // slider set min/max
    function setSlideMinMax(min, max, step) {
        $("#slideFilter").slider({
            step: step,
            min: min,
            max: max
        });
    }


    // set the min and max for the slider..
    // assuming all scores in the range of 0-5
    // tbd: determine if this is true
    //      if not return values from database
    setSlideMinMax(0, 5, 0.1);

    $("#jsGrid").jsGrid({
        width: "100%",

        autoload: true,
        pageButtonCount: 5,
        pageFirstText: "<<",
        pageIndex: 1,
        pageLastText: ">>",
        pageLoading: true,
        pageNavigatorNextText: "&#8230;",
        pageNavigatorPrevText: "&#8230;",
        pageNextText: ">",
        pagePrevText: "<",
        pageSize: 10,
        pagerFormat: "current page: {pageIndex} &nbsp;&nbsp; {first} {prev} {pages} {next} {last} &nbsp;&nbsp; total pages: {pageCount}",
        paging: true,

        controller: {
            loadData: function(filter) {
                var startIndex = (filter.pageIndex - 1) * filter.pageSize,
                    data = $.Deferred();
                $.ajax({
                    type: "GET",
                    contentType: "application/json; charset=utf-8",
                    url: "/items/" + startIndex.toString() + "/" + sliderval.toString(),
                    dataType: "json"
                }).done(function(response) {
                                        // loop over the incoming json data
                                        // wrap image url with html
                                        // format the rating for 2 decimal places
                                        for (var i=0; i < response.data.length; i++)
                                        {
                                            response.data[i].Photo = "<img style=\"max-width:50px;max-height:50px\" src=\"" + response.data[i].Photo + "\">";
                                            response.data[i].Rating = Number(response.data[i].Rating).toFixed(2);
                                        }
                    data.resolve(response);
                });
                // turn the slider back on after data reload
                slider.slider('enable');
                return data.promise();
            }
        },

        fields: [{
            name: "Photo",
            type: "text",
            width: 30,
            align: "center"
        }, {
            name: "Sitter",
            type: "text",
            width: 60,
            align: "center"
        }, {
            name: "Rating",
            type: "text",
            width: 50,
            align: "center"
        }, ]
    });

});
