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
    url: "http://127.0.0.1:8888/attr?name=cp",
    async : false,
    success: (iData) => { 
        data = iData.cp;
        data = data.map((item,key)=>{
            return {
                age:item[0],
                sex:item[1]===1?'male':'female',
                cp:item[2]===1?'typical angin':item[2]===2?'atypical angina':item[2]===3?'non-anginal pain':'asymptomatic'
            } 
        })
    }
});

export default class Jitter extends React.Component {

    render() {
        const scale = {
  city:{
    type:"cat",
    range: [ 0, 1 ]
  },
}
        return (
            <div className={styles.wrap}>
                <Chart height={window.innerHeight-200} data={data} forceFit scale={scale}>
                    <Tooltip
                        crosshairs={{
                            type: "cross"
                        }}
                    />
                    
                    <Legend reversed dx={20}/>
                    <Geom
                        type="point"
                        position="cp*age"
                        color="sex"
                        opacity={0.65}
                        shape="circle"
                        size={4}
                        adjust="jitter"
                    />
                    <Axis name="cp" title  grid={{
                      align: "center",
                      // 网格顶点从两个刻度中间开始
                      lineStyle: {
                        stroke: "#E9E9E9",
                        lineWidth: 1,
                        lineDash: [3, 3]
                      }
                    }}/>
                    <Axis name="age" title grid={null}/>
                </Chart>
            </div>
        );
    }
}
