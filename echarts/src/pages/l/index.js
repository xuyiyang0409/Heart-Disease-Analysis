import $ from "jquery";
import React from "react";

import styles from './index.less'
import {
    G2,
    Chart,
    Geom,
    Axis,
    Tooltip,
    Coord,
    Label,
    Legend,
    View,
    Guide,
    Shape,
    Facet,
    Util
} from "bizcharts";

let data;
$.ajax({
    url: "http://127.0.0.1:8888/attr?name=ca",
    async : false,
    success: (iData) => { 
        data = iData.ca;
        data = data.map((item,key)=>{
            return {
                age:item[0],
                sex:item[1]===1?'male':'female',
                ca:item[2]===1?'major':'vessels'
            } 
        })
    }
});

export default class Jitter extends React.Component {
    render() {
        return (
            <div className={styles.wrap}>
                <Chart height={window.innerHeight-200} data={data} forceFit>
                    <Tooltip
                        crosshairs={{
                            type: "cross"
                        }}
                    />
                    <Axis name="ca" title grid={{
                      align: "center",
                      // 网格顶点从两个刻度中间开始
                      lineStyle: {
                        stroke: "#E9E9E9",
                        lineWidth: 1,
                        lineDash: [3, 3]
                      }
                    }}/>
                    <Axis name="age" title grid={null}/>
                    <Legend reversed dx={20}/>
                    <Geom
                        type="point"
                        position="ca*age"
                        color="sex"
                        opacity={0.65}
                        shape="circle"
                        size={4}
                        adjust="jitter"
                    />
                </Chart>
            </div>
        );
    }
}
