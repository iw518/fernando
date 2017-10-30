/**
 * Created by Administrator on 2017/3/3 0003.
 */
let paper = Snap('#paper');

function plotting_section({ {
    hwidth
}
},
name;
)
{
    paper.clear();
    plotting_scale(15);
    plotting_holes({;
    {
        hwidth
    }
},
    name;
)
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

function plotting_holes(hwidth, name) {
    let paper_width = parseInt($("#paper").css("width"));
    let text = paper.text(paper_width / 2 - 80, 20, "工程地质剖面图" + name);
    text.attr({fontSize: 20});
    /*确保留白 */
    let section_offset = 75;
    let scale_x = 1;
    if (hWidth < (paper_width - section_offset * 2)) {
        scale_x = parseInt((paper_width - section_offset * 2) / hWidth);
    }
    else {
        scale_x = parseInt((paper_width - section_offset * 2) / hWidth);
    }
    let scale_y = 20;
    /* 使剖面图居中 */


    for (let i = 0; i < {{curves}}
.
    length;
    i++;
)
    {
        var curve = curves[i];
        for (let j = 0; j < {{curves}}
    .
        length;
        i++;
    )
        {
            let segment = {;
            {
                curve[j]
            }
        }
            for (let k = 0; k < segment.length - 1; k++) {
                let x1 = segment[k][0] * scale_x + section_offset;
                let y1 = segment[k][1] * scale_y;
                let x2 = segment[k + 1][0] * scale_x + section_offset;
                let y2 = segment[k + 1][1] * scale_y;
                let line = paper.line(x1, y1, x2, y2);
                line.attr({
                    stroke: "#000",
                    strokeWidth: 1
                });
            }
        }
    }
}





