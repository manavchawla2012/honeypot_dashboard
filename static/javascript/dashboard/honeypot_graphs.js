async function get_graph_data(graph_type, title, query_id, url, to_date, from_date) {
    var csrftoken = $("[name='csrfmiddlewaretoken']").val();
    $.ajax({
        url: url,
        type: "post",
        dataType: "json",
        headers: {"X-CSRFToken": csrftoken},
        data: {
            query_id: query_id,
            to_date: to_date ? to_date.toString() : to_date,
            from_date: from_date ? from_date.toString() : from_date
        },
        success: function (data) {
            if (data.success) {
                let chart_id = "chart" + query_id.toString();
                create_chart(graph_type, data.data, chart_id)
            } else {
                console.log("Fail");
            }
        }
        ,
        error: function (data) {
            console.log("js error");
        }
    });
}

function create_chart(graphType, data, graph_div, months) {
    let chart = ""
    let chart_id = graph_div
    let prev_theme = sessionStorage.getItem('prev_theme');
    if(prev_theme === "dark") {
        am4core.useTheme(am4themes_dark);
    }
    am4core.useTheme(am4themes_animated);
    switch (graphType) {
        case 1: //pie chart
            chart = am4core.create(chart_id, am4charts.PieChart);
            //chart.padding(50, 50, 50, 50);
            chart.hiddenState.properties.opacity = 0;
            chart.legend = new am4charts.Legend();
            chart.legend.maxWidth = undefined;
            chart.data = data
            var pieSeries = chart.series.push(new am4charts.PieSeries());
            pieSeries.ticks.template.disabled = true;
            pieSeries.dataFields.value = "count";
            pieSeries.dataFields.category = "name";
            pieSeries.labels.template.disabled = true;

            break;
        case 2:
            chart = am4core.create(chart_id, am4charts.PieChart);
            chart.innerRadius = am4core.percent(40)
            //chart.padding(50, 50, 50, 50);
            chart.hiddenState.properties.opacity = 0;
            chart.legend = new am4charts.Legend();
            chart.legend.maxWidth = undefined;
            chart.data = data
            var series = chart.series.push(new am4charts.PieSeries());
            series.dataFields.value = "count";
            series.dataFields.category = "name";
            series.ticks.template.disabled = true;
            series.labels.template.disabled = true;
            break;
        case 3://bar chart
            chart = am4core.create(chart_id, am4charts.XYChart);
            chart.padding(40, 40, 40, 40);
            chart.data = data
            var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
            categoryAxis.renderer.grid.template.location = 0;
            categoryAxis.dataFields.category = "name";
            categoryAxis.renderer.minGridDistance = 60;
            categoryAxis.renderer.inversed = true;
            //categoryAxis.renderer.grid.template.disabled = true;

            var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
            valueAxis.min = 0;
            valueAxis.extraMax = 0.1;
            var series = chart.series.push(new am4charts.ColumnSeries());
            series.dataFields.categoryX = "name";
            series.dataFields.valueY = "count";
            series.tooltipText = "{valueY.value}"
            series.calculatePercent = true;
            series.columns.template.strokeOpacity = 0;
            series.columns.template.column.cornerRadiusTopRight = 10;
            series.columns.template.column.cornerRadiusTopLeft = 10;
            var labelBullet = series.bullets.push(new am4charts.LabelBullet());
            labelBullet.label.verticalCenter = "bottom";
            labelBullet.label.dy = -10;
            //labelBullet.label.text = "{values.valueY.workingValue.formatNumber('#.')}";
            labelBullet.label.text = "{valueY.percent}%";
            //chart.zoomOutButton.disabled = true;
            series.columns.template.adapter.add("fill", function (fill, target) {
                return chart.colors.getIndex(target.dataItem.index);
            });
            chart.cursor = new am4charts.XYCursor();
            break;
        case 4://multi bar
            chart = am4core.create(chart_id, am4charts.XYChart);
            chart.padding(40, 40, 40, 40);
            chart.cursor = new am4charts.XYCursor();
            chart.scrollbarX = new am4core.Scrollbar();
            chart.numberFormatter.numberFormat = "#.";

// will use this to store colors of the same items
            var colors = {};

            var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
            categoryAxis.dataFields.category = "category";
            categoryAxis.renderer.minGridDistance = 60;
            categoryAxis.renderer.grid.template.location = 0;
            categoryAxis.dataItems.template.text = "{realName}";
            categoryAxis.adapter.add("tooltipText", function (tooltipText, target) {
                return categoryAxis.tooltipDataItem.dataContext.realName;
            })


            var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
            //valueAxis.tooltip.disabled = true;
            valueAxis.min = 0;
            valueAxis.extraMax = 0.1;

// single column series for all data
            var columnSeries = chart.series.push(new am4charts.ColumnSeries());
            columnSeries.columns.template.width = am4core.percent(80);
            columnSeries.tooltipText = "{provider}: {realName}, {valueY}";
            columnSeries.dataFields.categoryX = "category";
            columnSeries.dataFields.valueY = "value";
            //columnSeries.calculatePercent = true;


// second value axis for quantity
            var valueAxis2 = chart.yAxes.push(new am4charts.ValueAxis());
            valueAxis2.renderer.opposite = true;
            valueAxis2.syncWithAxis = valueAxis;
            valueAxis2.tooltip.disabled = true;

// quantity line series
            var lineSeries = chart.series.push(new am4charts.LineSeries());
            lineSeries.tooltipText = "{valueY}";
            lineSeries.dataFields.categoryX = "category";
            lineSeries.dataFields.valueY = "quantity";
            lineSeries.yAxis = valueAxis2;
            lineSeries.bullets.push(new am4charts.CircleBullet());
            lineSeries.stroke = chart.colors.getIndex(13);
            lineSeries.fill = lineSeries.stroke;
            lineSeries.strokeWidth = 2;
            lineSeries.snapTooltip = true;


// when data validated, adjust location of data item based on count
            lineSeries.events.on("datavalidated", function () {
                lineSeries.dataItems.each(function (dataItem) {
                    // if count divides by two, location is 0 (on the grid)
                    if (dataItem.dataContext.count / 2 == Math.round(dataItem.dataContext.count / 2)) {
                        dataItem.setLocation("categoryX", 0);
                    }
                    // otherwise location is 0.5 (middle)
                    else {
                        dataItem.setLocation("categoryX", 0.5);
                    }
                })
            })

// fill adapter, here we save color value to colors object so that each time the item has the same name, the same color is used
            columnSeries.columns.template.adapter.add("fill", function (fill, target) {
                var name = target.dataItem.dataContext.realName;
                if (!colors[name]) {
                    colors[name] = chart.colors.next();
                }
                target.stroke = colors[name];
                return colors[name];
            })


            var rangeTemplate = categoryAxis.axisRanges.template;
            rangeTemplate.tick.disabled = false;
            rangeTemplate.tick.location = 0;
            rangeTemplate.tick.strokeOpacity = 0.6;
            rangeTemplate.tick.length = 60;
            rangeTemplate.grid.strokeOpacity = 0.5;
            rangeTemplate.label.tooltip = new am4core.Tooltip();
            rangeTemplate.label.tooltip.dy = -10;
            rangeTemplate.label.cloneTooltip = false;

///// DATA
            var chartData = [];
            var lineSeriesData = [];
            var graphData = data;
            for (var providerName in graphData) {
                var providerData = graphData[providerName];

                // add data of one provider to temp array

                // add items
                if (!$.isEmptyObject(providerData)) {
                    var tempArray = [];
                    var count = 0;
                    for (var itemName in providerData) {
                        if (itemName != "quantity") {
                            count++;
                            // we generate unique category for each column (providerName + "_" + itemName) and store realName
                            tempArray.push({
                                category: providerName + "_" + itemName,
                                realName: itemName,
                                value: providerData[itemName],
                                provider: providerName
                            })
                        }
                    }
                } else {
                    providerData.pop
                }
                // sort temp array
                if (months === 0) {
                    tempArray.sort(function (a, b) {
                        if (a.value > b.value) {
                            return 1;
                        } else if (a.value < b.value) {
                            return -1
                        } else {
                            return 0;
                        }
                    })
                }

                // add quantity and count to middle data item (line series uses it)
                var lineSeriesDataIndex = Math.floor(count / 2);
                var labelBullet = columnSeries.bullets.push(new am4charts.LabelBullet());
                labelBullet.label.verticalCenter = "bottom";
                labelBullet.label.dy = 0;
                labelBullet.label.text = "{values.valueY.workingValue.formatNumber('#.')}";
                //labelBullet.label.text = "{valueY.percent}%";

                tempArray[lineSeriesDataIndex].count = count;
                // push to the final data
                am4core.array.each(tempArray, function (item) {
                    chartData.push(item);
                })

                // create range (the additional label at the bottom)
                var range = categoryAxis.axisRanges.create();
                range.category = tempArray[0].category;
                range.endCategory = tempArray[tempArray.length - 1].category;
                range.label.text = tempArray[0].provider;
                range.label.dy = 30;
                range.label.truncate = true;
                range.label.fontWeight = "bold";
                range.label.tooltipText = tempArray[0].provider;

                range.label.adapter.add("maxWidth", function (maxWidth, target) {
                    var range = target.dataItem;
                    var startPosition = categoryAxis.categoryToPosition(range.category, 0);
                    var endPosition = categoryAxis.categoryToPosition(range.endCategory, 1);
                    var startX = categoryAxis.positionToCoordinate(startPosition);
                    var endX = categoryAxis.positionToCoordinate(endPosition);
                    return endX - startX;
                })
            }

            chart.data = chartData;


// last tick
            var range = categoryAxis.axisRanges.create();
            range.category = chart.data[chart.data.length - 1].category;
            range.label.disabled = true;
            range.tick.location = 1;
            range.grid.location = 1;
            break;
        default:
            console.log("Graph Not Found");


    }
}
