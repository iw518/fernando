/**
 * Created by Administrator on 2017/3/3 0003.
 */
var paper = Snap('#paper');

function plotting_section(section, layers) {
    paper.clear();
    console.log(section);
    plotting_scale(15);
    plotting_holes(section, layers);
}

function plotting_scale(n) {
    for (var i = 1; i < n; i++) {
        var rect = paper.rect(10, (i - 1) * 40, 5, 40);
        rect.attr({
            stroke: "#000",
            strokeWidth: 2
        });
        if (i % 2 == 1) {
            var line = paper.line(10, (i - 1) * 40, 50, (i - 1) * 40);

            line.attr({
                stroke: "#000",
                strokeWidth: 1
            });
            var text = paper.text(50, (i - 1) * 40, i);
            rect.attr({
                fill: "#000"
            });
        }
        else {
            rect.attr({
                fill: "#fff"
            });
        }
    }
    var line = paper.line(10, (n - 1) * 40, 50, (n - 1) * 40);
    line.attr({
        stroke: "#000",
        strokeWidth: 1
    });
    var text = paper.text(50, (n - 1) * 40, i);
}

function plotting_holes(section, layers) {
    var distance = 0;
    var paper_width = parseInt($("#paper").css("width"));
    var text = paper.text(paper_width / 2 - 80, 20, "工程地质剖面图" + section.name);
    text.attr({fontSize: 20});
    /*确保留白 */
    var section_offset = 75;
    for (var i = 0; i < section.items.length; i++) {
        var item = section.items[i];
        var distance = distance + item.distance;
    }
    var scale_x = 1;
    if (distance < (paper_width - section_offset * 2)) {
        scale_x = parseInt((paper_width - section_offset * 2) / distance);
    }
    else {
        scale_x = parseInt((paper_width - section_offset * 2) / distance);
    }
    var scale_y = 20;
    /* 使剖面图居中 */
    distance = (paper_width - distance * scale_x) / 2;
    for (var i = 0; i < section.items.length; i++) {
        /*必须用safe，使其不转义*/
        var item = section.items[i];
        var hole = item.hole;
        plotting_hole(hole, distance, scale_y);
        var x1 = distance;
        distance = distance + item.distance * scale_x;
        var x2 = distance;
        for (var j = 0; j < layers.length; j++) {
            if (i < section.items.length - 1) {
                if (hole.layers.length > j && section.items[i + 1].hole.layers.length > j) {
                    if (hole.layers[j].endDep - hole.layers[j].startDep > 0) {
                        var y1 = hole.layers[j].startDep;
                        var y2 = section.items[i + 1].hole.layers[j].startDep;
                        var line = paper.line(x1, y1 * scale_y, x2, y2 * scale_y);
                        line.attr({
                            stroke: "#000",
                            strokeWidth: 1
                        });
                    }
                }
            }
        }
    }
}

function plotting_hole(hole, distance, scale_y) {
    var holeName_text = paper.text(distance, 10, hole.holeName);
    holeName_text.attr({fontSize: 5});
    /* for (var item in items)中item是string类型,故一般不要用for in */
    for (var i = 0; i < hole.layers.length; i++) {
        var layer = hole.layers[i];
        var line = paper.line(x1 = distance, y1 = layer.startDep * scale_y, x2 = distance, y2 = layer.endDep * scale_y);
        line.attr({
            stroke: "#000",
            strokeWidth: 1
        });
        var text = paper.text(distance, layer.endDep * scale_y, parseFloat(layer.endDep).toFixed(2));
        text.attr({fontSize: 4});
    }
}



