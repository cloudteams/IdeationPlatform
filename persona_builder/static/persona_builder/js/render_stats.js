            $(function() {
                function getColors(keys) {
                    var colors = [];
                    var default_colors = [
                        '#BFBFBF', // silver
                        '#446CB3', // blue
                        '#D64541', // red
                        '#03C9A9', // green
                        '#F5AB35', // yellow
                        '#D2527F', // pink
                        '#59ABE3'  // light blue
                    ];

                    var i = 1;
                    for (key in keys) {
                        if ((typeof(label) == 'undefined') || (label == 'null') || (label == '')) {
                            colors.push(default_colors[6]);
                        } else {
                            colors.push(default_colors[i]);
                        }
                        i++;
                    }

                    return colors;
                }

                var p = new PersonaStats();
                for (prop in p.property_values) {
                    var keys = [];
                    var values = [];
                    var dataProvider = [];
                    for (var key in p.property_values[prop]) {
                        var label = key;
                        if ((typeof(label) == 'undefined') || (label == 'null') || (label == '')) {
                            label = 'Unknown/None';
                        }
                        keys.push(label);
                        values.push(p.property_values[prop][key]);
                        dataProvider.push({'title': label, 'value': p.property_values[prop][key]})
                    }

                    if (keys.length > 7) {
                        $("#chart-" + prop).closest('.property-stats').remove();
                        continue;
                    }

                    var chart = AmCharts.makeChart("chart-" + prop, {
                        "type": "pie",
                        "theme": "light",
                        "dataProvider": dataProvider,
                        "titleField": "title",
                        "valueField": "value",

                        "labelRadius": 5,

                        "angle": 20,
                        "depth3D": 5,
                        "borderAlpha": 0,
                        "outlineThickness": 0,
                        "radius": "42%",
                        "innerRadius": "60%",
                        "color": '#ccc',
                        "labelTickColor": "#ccc",

                        "labelText": "[[title]]",
                        "export": {
                            "enabled": true
                        }
                    });
                }
            });