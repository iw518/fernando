/**
 * Created by Administrator on 2017/3/3 0003.
 */
function expand_section_info(section) {
    var items = section.items;
    var section_info_list = new Array();
    for (var i = 0; i < items.length; i++) {
        var item = items[i];
        section_info_list.push(expand_hole_info(item));
    }
    return section_info_list;
}

function expand_hole_info(item) {
    var hole = item.hole;
    var distance = item.distance;
    var info_list = new Array();
    info_list.push(hole.holeName, distance, hole.Dep, hole.elevation);
    if (hole.waterLevel > 0) {
        info_list.push(hole.waterLevel);

    }
    else {
        info_list.push('');
    }
    for (var i = 0; i < hole.layers.length; i++) {
        if (layer.thickness > 0) {
            info_list.push(layer.endDep);

        }
        else {
            info_list.push(0);
        }
    }
    return info_list;
}
