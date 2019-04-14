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
    url: "http://127.0.0.1:8888/attr?name=trestbps",
    async : false,
    success: (iData) => { 
        data = iData.trestbps;
        data = data.map((item,key)=>{
            return {
                age:item[0],
                sex:item[1]===1?'male':'female',
                trestbps:item[2]
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
                    <Axis name="trestbps"  />
                    <Axis name="age" title={'年龄'} />
                    <Legend reversed dx={20}/>
                    <Geom
                        type="point"
                        position="trestbps*age"
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
