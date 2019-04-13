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
    url: "http://127.0.0.1:8888/attr?name=oldpeak",
    async : false,
    success: (iData) => { 
        data = iData.oldpeak;
        data = data.map((item,key)=>{
            return {
                age:item[0],
                sex:item[1]===1?'male':'female',
                oldpeak:item[2]
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
                    <Axis name="age" title/>
                    <Axis name="oldpeak"  title/>
                    
                    <Legend reversed dx={20}/>
                    <Geom
                        type="point"
                        position="age*oldpeak"
                        color="sex"
                        shape="circle"
                        size={4}
                        adjust="jitter"
                    />
                </Chart>
            </div>
        );
    }
}
